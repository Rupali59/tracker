import os
import requests
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Optional
import config

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('github_tracker.log')
    ]
)
logger = logging.getLogger(__name__)

class GitHubStats:
    def __init__(self):
        self.token = config.GITHUB_TOKEN
        self.username = config.GITHUB_USERNAME
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
    def get_user_repos(self) -> List[Dict]:
        """Get all repositories for the user"""
        logger.info(f"Fetching repositories for user: {self.username}")
        url = f"https://api.github.com/users/{self.username}/repos"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        repos = response.json()
        logger.info(f"Found {len(repos)} repositories")
        return repos
    
    def get_commits_for_repo(self, repo_name: str, since_date: datetime, until_date: datetime) -> List[Dict]:
        """Get commits for a specific repository within a date range"""
        logger.info(f"Fetching commits for repository: {repo_name}")
        logger.info(f"Date range: {since_date.strftime('%Y-%m-%d')} to {until_date.strftime('%Y-%m-%d')}")
        
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/commits"
        params = {
            'author': self.username,
            'since': since_date.isoformat(),
            'until': until_date.isoformat(),
            'per_page': 100
        }
        
        commits = []
        page = 1
        
        while True:
            params['page'] = page
            logger.debug(f"Fetching page {page} for {repo_name}")
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            page_commits = response.json()
            if not page_commits:
                logger.debug(f"No more commits found for {repo_name}")
                break
            
            # Filter out Quartz sync commits if enabled
            filtered_commits = []
            for commit in page_commits:
                if config.FILTER_QUARTZ_SYNC:
                    message = commit['commit']['message'].lower()
                    # Skip Quartz sync commits
                    if any(keyword in message for keyword in config.QUARTZ_FILTER_KEYWORDS):
                        logger.debug(f"Skipping Quartz sync commit: {commit['commit']['message'][:50]}...")
                        continue
                filtered_commits.append(commit)
            
            commits.extend(filtered_commits)
            logger.debug(f"Found {len(page_commits)} commits, filtered to {len(filtered_commits)} on page {page} for {repo_name}")
            page += 1
            
            if len(page_commits) < 100:
                break
        
        logger.info(f"Total commits found for {repo_name}: {len(commits)} (after filtering)")
        return commits
    
    def get_commit_details(self, repo_name: str, commit_sha: str) -> Optional[Dict]:
        """Get detailed information about a specific commit"""
        logger.debug(f"Fetching details for commit {commit_sha[:8]} in {repo_name}")
        url = f"https://api.github.com/repos/{self.username}/{repo_name}/commits/{commit_sha}"
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 404:
            logger.warning(f"Commit {commit_sha[:8]} not found in {repo_name}")
            return None
            
        response.raise_for_status()
        commit_details = response.json()
        logger.debug(f"Successfully fetched details for commit {commit_sha[:8]}")
        return commit_details
    
    def analyze_file_changes(self, commit_details: Dict) -> Dict:
        """Analyze file changes in a commit"""
        files_changed = commit_details.get('files', [])
        logger.debug(f"Analyzing {len(files_changed)} files in commit")
        
        analysis = {
            'total_files': len(files_changed),
            'additions': 0,
            'deletions': 0,
            'file_types': defaultdict(int),
            'files': []
        }
        
        for file_info in files_changed:
            filename = file_info['filename']
            status = file_info['status']
            additions = file_info.get('additions', 0)
            deletions = file_info.get('deletions', 0)
            
            analysis['additions'] += additions
            analysis['deletions'] += deletions
            
            # Get file extension
            file_ext = os.path.splitext(filename)[1].lower()
            if file_ext:
                analysis['file_types'][file_ext] += 1
            else:
                analysis['file_types']['no_extension'] += 1
            
            analysis['files'].append({
                'filename': filename,
                'status': status,
                'additions': additions,
                'deletions': deletions
            })
        
        logger.debug(f"Commit analysis: {analysis['total_files']} files, +{analysis['additions']} -{analysis['deletions']} lines")
        return analysis
    
    def generate_commit_summary(self, commit: Dict, commit_details: Optional[Dict] = None) -> Dict:
        """Generate a summary for a commit"""
        repo_name = commit['repository']['name']
        sha = commit['sha']
        message = commit['commit']['message']
        date = datetime.fromisoformat(commit['commit']['author']['date'].replace('Z', '+00:00'))
        
        logger.debug(f"Generating summary for commit {sha[:8]} in {repo_name}: {message[:50]}...")
        
        # Make commit message more human-readable if enabled
        if config.MAKE_COMMITS_READABLE:
            readable_message = self.make_commit_readable(message)
        else:
            readable_message = message
        
        summary = {
            'repo': repo_name,
            'sha': sha[:8],
            'message': message,
            'readable_message': readable_message,
            'date': date,
            'url': commit['html_url']
        }
        
        if commit_details:
            analysis = self.analyze_file_changes(commit_details)
            summary.update(analysis)
        
        return summary
    
    def make_commit_readable(self, message: str) -> str:
        """Convert commit message to human-readable format"""
        # Remove common prefixes
        prefixes_to_remove = [
            'feat:', 'fix:', 'docs:', 'style:', 'refactor:', 'test:', 'chore:',
            'add:', 'update:', 'remove:', 'delete:', 'create:', 'modify:',
            '[feat]', '[fix]', '[docs]', '[style]', '[refactor]', '[test]', '[chore]',
            'feat(', 'fix(', 'docs(', 'style(', 'refactor(', 'test(', 'chore('
        ]
        
        readable = message.strip()
        
        # Remove prefixes
        for prefix in prefixes_to_remove:
            if readable.lower().startswith(prefix.lower()):
                readable = readable[len(prefix):].strip()
                break
        
        # Handle conventional commit format
        if '(' in readable and ')' in readable:
            # Remove scope: feat(scope): message -> message
            colon_index = readable.find(':')
            if colon_index != -1:
                readable = readable[colon_index + 1:].strip()
        
        # Capitalize first letter
        if readable:
            readable = readable[0].upper() + readable[1:]
        
        # Remove trailing punctuation
        readable = readable.rstrip('.!?')
        
        # Handle multi-line messages (take first line)
        if '\n' in readable:
            readable = readable.split('\n')[0].strip()
        
        # If message is too long, truncate
        if len(readable) > 100:
            readable = readable[:97] + "..."
        
        return readable if readable else message
    
    def get_daily_commits(self, days_back: int = 30) -> Dict[str, List[Dict]]:
        """Get commits organized by date for the last N days"""
        logger.info(f"Starting to fetch commits for the last {days_back} days")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        logger.info(f"Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Get all user repositories
        repos = self.get_user_repos()
        
        # Collect commits from all repositories
        all_commits = []
        
        for repo in repos:
            repo_name = repo['name']
            try:
                commits = self.get_commits_for_repo(repo_name, start_date, end_date)
                for commit in commits:
                    commit['repository'] = {'name': repo_name}
                    all_commits.append(commit)
            except Exception as e:
                logger.error(f"Error fetching commits from {repo_name}: {e}")
        
        logger.info(f"Total commits collected: {len(all_commits)}")
        
        # Group commits by date
        daily_commits = defaultdict(list)
        
        for commit in all_commits:
            date = datetime.fromisoformat(commit['commit']['author']['date'].replace('Z', '+00:00'))
            date_key = date.strftime('%Y-%m-%d')
            
            # Get detailed commit information
            repo_name = commit['repository']['name']
            commit_details = self.get_commit_details(repo_name, commit['sha'])
            
            summary = self.generate_commit_summary(commit, commit_details)
            daily_commits[date_key].append(summary)
        
        # Sort commits within each day by time
        for date in daily_commits:
            daily_commits[date].sort(key=lambda x: x['date'], reverse=True)
        
        logger.info(f"Organized commits into {len(daily_commits)} days")
        for date, commits in daily_commits.items():
            logger.info(f"  {date}: {len(commits)} commits")
        
        return dict(daily_commits) 
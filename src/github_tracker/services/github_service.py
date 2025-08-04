"""
GitHub service for handling GitHub-related business logic.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from ..config.settings import Settings
from ..core.github_client import GitHubClient

logger = logging.getLogger(__name__)


class GitHubService:
    """Service for handling GitHub-related operations."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.github_client = GitHubClient(settings)
    
    def get_daily_commits(self, days_back: int = 30) -> Dict[str, List[Dict]]:
        """Get commits organized by date for the last N days."""
        logger.info(f"Fetching daily commits for the last {days_back} days")
        return self.github_client.get_daily_commits(days_back)
    
    def get_today_commits(self) -> List[Dict]:
        """Get commits for today only."""
        logger.info("Fetching today's commits")
        daily_commits = self.github_client.get_daily_commits(1)  # Only last 1 day
        
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        
        if today_str not in daily_commits or not daily_commits[today_str]:
            logger.info("No commits found for today")
            return []
        
        return daily_commits[today_str]
    
    def get_commit_summary_stats(self, daily_commits: Dict[str, List[Dict]]) -> Dict:
        """Get summary statistics for the processed commits."""
        if not daily_commits:
            return {
                'total_commits': 0,
                'total_days': 0,
                'total_additions': 0,
                'total_deletions': 0,
                'repos_worked_on': set(),
                'daily_summary': {}
            }
        
        total_commits = sum(len(commits) for commits in daily_commits.values())
        total_days = len(daily_commits)
        total_additions = sum(
            sum(commit.get('additions', 0) for commit in commits)
            for commits in daily_commits.values()
        )
        total_deletions = sum(
            sum(commit.get('deletions', 0) for commit in commits)
            for commits in daily_commits.values()
        )
        repos_worked_on = set()
        for commits in daily_commits.values():
            repos_worked_on.update(commit['repo'] for commit in commits)
        
        daily_summary = {}
        for date_str, commits in daily_commits.items():
            daily_additions = sum(commit.get('additions', 0) for commit in commits)
            daily_deletions = sum(commit.get('deletions', 0) for commit in commits)
            daily_repos = set(commit['repo'] for commit in commits)
            
            daily_summary[date_str] = {
                'commits': len(commits),
                'repos': len(daily_repos),
                'additions': daily_additions,
                'deletions': daily_deletions
            }
        
        return {
            'total_commits': total_commits,
            'total_days': total_days,
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'repos_worked_on': repos_worked_on,
            'daily_summary': daily_summary
        } 
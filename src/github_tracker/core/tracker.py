"""
Main tracker class that orchestrates GitHub data fetching and Obsidian updates.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from ..config.settings import Settings
from .github_client import GitHubClient
from .obsidian_manager import ObsidianManager

logger = logging.getLogger(__name__)


class GitHubTracker:
    """Main tracker class that coordinates GitHub data fetching and Obsidian updates."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.github_client = GitHubClient(settings)
        self.obsidian_manager = ObsidianManager(settings)
    
    def run_backfill(self) -> Dict[str, List[Dict]]:
        """Run the main backfill process."""
        logger.info("Starting GitHub tracker backfill process")
        
        # Get commit history
        daily_commits = self.github_client.get_daily_commits(self.settings.days_to_backfill)
        
        if not daily_commits:
            logger.info("No commits found in the specified time range")
            return {}
        
        # Update Obsidian daily notes
        self.obsidian_manager.backfill_daily_notes(daily_commits)
        
        # Create daily notes for all days in the range, even without commits
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.settings.days_to_backfill)
        self.obsidian_manager.create_daily_notes_for_range(start_date, end_date)
        
        logger.info("Backfill process completed successfully")
        return daily_commits
    
    def run_daily_update(self) -> Dict[str, List[Dict]]:
        """Run the daily update process for today only."""
        logger.info("Starting GitHub tracker daily update process")
        
        # Get today's date
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        
        # Get commits for today only
        daily_commits = self.github_client.get_daily_commits(1)  # Only last 1 day
        
        if today_str not in daily_commits or not daily_commits[today_str]:
            logger.info("No commits found for today")
            commits = []
        else:
            commits = daily_commits[today_str]
        
        # Update today's daily note
        self.obsidian_manager.update_daily_note(today, commits)
        
        # Ensure monthly calendar exists for this month
        self.obsidian_manager.create_monthly_calendar(today.year, today.month)
        
        logger.info("Daily update process completed successfully")
        return daily_commits
    
    def get_summary_stats(self, daily_commits: Dict[str, List[Dict]]) -> Dict:
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
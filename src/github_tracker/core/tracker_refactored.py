"""
Refactored main tracker class that orchestrates GitHub data fetching and Obsidian updates.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from ..config.settings import Settings
from ..services.github_service import GitHubService
from ..services.obsidian_service import ObsidianService

logger = logging.getLogger(__name__)


class GitHubTracker:
    """Main tracker class that coordinates GitHub data fetching and Obsidian updates."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.github_service = GitHubService(settings)
        self.obsidian_service = ObsidianService(settings)
    
    def run_backfill(self) -> Dict[str, List[Dict]]:
        """Run the main backfill process."""
        logger.info("Starting GitHub tracker backfill process")
        
        # Get commit history
        daily_commits = self.github_service.get_daily_commits(self.settings.days_to_backfill)
        
        if not daily_commits:
            logger.info("No commits found in the specified time range")
            return {}
        
        # Update Obsidian daily notes
        self.obsidian_service.backfill_notes(daily_commits)
        
        logger.info("Backfill process completed successfully")
        return daily_commits
    
    def run_daily_update(self) -> Dict[str, List[Dict]]:
        """Run the daily update process for today only."""
        logger.info("Starting GitHub tracker daily update process")
        
        # Get today's commits
        commits = self.github_service.get_today_commits()
        
        # Update today's daily note
        self.obsidian_service.update_today_note(commits)
        
        logger.info("Daily update process completed successfully")
        return {datetime.now().strftime('%Y-%m-%d'): commits}
    
    def get_summary_stats(self, daily_commits: Dict[str, List[Dict]]) -> Dict:
        """Get summary statistics for the processed commits."""
        return self.github_service.get_commit_summary_stats(daily_commits) 
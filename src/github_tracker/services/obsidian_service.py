"""
Obsidian service for handling Obsidian-related business logic.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from ..config.settings import Settings
from ..core.obsidian_manager_refactored import ObsidianManager

logger = logging.getLogger(__name__)


class ObsidianService:
    """Service for handling Obsidian-related operations."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.obsidian_manager = ObsidianManager(settings)
    
    def update_today_note(self, commits: List[Dict]):
        """Update today's daily note with GitHub activity."""
        today = datetime.now()
        logger.info(f"Updating today's note with {len(commits)} commits")
        self.obsidian_manager.update_daily_note(today, commits)
        
        # Ensure monthly calendar exists for this month
        self.obsidian_manager.create_monthly_calendar(today.year, today.month)
    
    def backfill_notes(self, daily_commits: Dict[str, List[Dict]]):
        """Backfill daily notes with GitHub activity."""
        logger.info(f"Starting backfill for {len(daily_commits)} days")
        self.obsidian_manager.backfill_daily_notes(daily_commits)
        
        # Create daily notes for all days in the range, even without commits
        if daily_commits:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=self.settings.days_to_backfill)
            self.obsidian_manager.create_daily_notes_for_range(start_date, end_date)
        
        logger.info("Backfill process completed")
    
    def create_notes_for_range(self, start_date: datetime, end_date: datetime):
        """Create daily notes for a specific date range."""
        logger.info(f"Creating notes for range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        self.obsidian_manager.create_daily_notes_for_range(start_date, end_date)
    
    def create_monthly_calendar(self, year: int, month: int):
        """Create a monthly calendar file."""
        logger.info(f"Creating monthly calendar for {year}-{month:02d}")
        self.obsidian_manager.create_monthly_calendar(year, month) 
"""
Refactored Obsidian integration for managing daily notes and monthly calendars.
"""

import logging
from datetime import datetime, timedelta
from typing import Dict, List
from ..config.settings import Settings
from .file_operations.daily_note_manager import DailyNoteManager
from .file_operations.calendar_manager import CalendarManager

logger = logging.getLogger(__name__)


class ObsidianManager:
    """Manages Obsidian daily notes and monthly calendars with better separation of concerns."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.daily_note_manager = DailyNoteManager(settings)
        self.calendar_manager = CalendarManager(settings)
    
    def update_daily_note(self, date: datetime, commits: List[Dict]):
        """Update a daily note with GitHub activity."""
        self.daily_note_manager.update_daily_note(date, commits)
    
    def backfill_daily_notes(self, daily_commits: Dict[str, List[Dict]]):
        """Backfill daily notes with GitHub activity."""
        self.daily_note_manager.backfill_daily_notes(daily_commits)
    
    def create_daily_notes_for_range(self, start_date: datetime, end_date: datetime):
        """Create daily notes for a date range, even if no commits exist."""
        # Create monthly calendar files for the range
        self.calendar_manager.create_monthly_calendars_for_range(start_date, end_date)
        
        # Create daily notes
        self.daily_note_manager.create_daily_notes_for_range(start_date, end_date)
    
    def create_monthly_calendar(self, year: int, month: int):
        """Create a monthly calendar file for the specified year and month."""
        self.calendar_manager.create_monthly_calendar(year, month) 
"""
Daily note file operations for Obsidian integration.
"""

import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ...config.settings import Settings
from ..formatters.daily_note_formatter import DailyNoteFormatter

logger = logging.getLogger(__name__)


class DailyNoteManager:
    """Handles file operations for daily notes."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.vault_path = settings.obsidian_vault_path
        self.daily_notes_folder = settings.daily_notes_folder
        self.daily_notes_path = os.path.join(self.vault_path, self.daily_notes_folder)
        self.formatter = DailyNoteFormatter(settings)
    
    def get_daily_note_path(self, date: datetime) -> str:
        """Get the path for a daily note file."""
        # Format: /Users/rupalib59/Study tracker/Calendar/2025/July/18-07-2025.md
        year = date.strftime('%Y')
        month = date.strftime('%B')  # Full month name (January, February, etc.)
        day_month = date.strftime('%d-%m-%Y')  # 18-07-2025 format
        
        # Create the path structure
        month_path = os.path.join(self.vault_path, 'Calendar', year, month)
        filename = f"{day_month}.md"
        return os.path.join(month_path, filename)
    
    def read_daily_note(self, date: datetime) -> Optional[str]:
        """Read the content of a daily note."""
        file_path = self.get_daily_note_path(date)
        logger.debug(f"Reading daily note: {file_path}")
        
        if not os.path.exists(file_path):
            logger.info(f"Daily note does not exist: {file_path}")
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                logger.debug(f"Successfully read daily note: {file_path}")
                return content
        except Exception as e:
            logger.error(f"Error reading daily note {file_path}: {e}")
            return None
    
    def write_daily_note(self, date: datetime, content: str):
        """Write content to a daily note."""
        file_path = self.get_daily_note_path(date)
        logger.info(f"Writing daily note: {file_path}")
        
        # Ensure directory exists
        dir_path = os.path.dirname(file_path)
        if not os.path.exists(dir_path):
            logger.info(f"Creating directory: {dir_path}")
        os.makedirs(dir_path, exist_ok=True)
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Successfully updated daily note: {file_path}")
        except Exception as e:
            logger.error(f"Error writing daily note {file_path}: {e}")
    
    def update_daily_note(self, date: datetime, commits: List[Dict]):
        """Update a daily note with GitHub activity."""
        logger.info(f"Updating daily note for {date.strftime('%Y-%m-%d')} with {len(commits)} commits")
        
        existing_content = self.read_daily_note(date)
        
        if existing_content is None:
            # Create new daily note
            logger.info(f"Creating new daily note for {date.strftime('%Y-%m-%d')}")
            lines = []
            lines.append(self.formatter.format_daily_note_header(date))
            lines.append("")
            # Only add GitHub section if there are commits
            if commits:
                lines.append(self.formatter.format_daily_github_section(commits, date))
            new_content = '\n'.join(lines)
        else:
            # Update existing daily note - preserve all existing content
            logger.info(f"Updating existing daily note for {date.strftime('%Y-%m-%d')}")
            
            start_line, end_line = self.formatter.find_github_section(existing_content)
            
            if commits:
                # Add or update GitHub section with actual commits
                github_section = self.formatter.format_daily_github_section(commits, date)
                new_content = self.formatter.merge_content_with_github_section(existing_content, github_section)
            else:
                # No commits - remove any existing GitHub section
                if start_line is not None and end_line is not None:
                    logger.debug(f"Removing existing GitHub section (lines {start_line}-{end_line})")
                    lines = existing_content.split('\n')
                    new_lines = lines[:start_line] + lines[end_line:]
                    new_content = '\n'.join(new_lines)
                else:
                    # No GitHub section to remove
                    new_content = existing_content
        
        self.write_daily_note(date, new_content)
    
    def backfill_daily_notes(self, daily_commits: Dict[str, List[Dict]]):
        """Backfill daily notes with GitHub activity."""
        logger.info(f"Starting backfill for {len(daily_commits)} days")
        for date_str, commits in daily_commits.items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            logger.info(f"Processing {date_str}: {len(commits)} commits")
            self.update_daily_note(date, commits)
        logger.info("Backfill completed")
    
    def create_daily_notes_for_range(self, start_date: datetime, end_date: datetime):
        """Create daily notes for a date range, even if no commits exist."""
        logger.info(f"Creating daily notes for range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Check if daily note already exists
            existing_content = self.read_daily_note(current_date)
            if existing_content is None:
                logger.info(f"Creating daily note for {date_str} (no existing file)")
                # Create empty daily note without GitHub section
                lines = []
                lines.append(self.formatter.format_daily_note_header(current_date))
                lines.append("")
                new_content = '\n'.join(lines)
                self.write_daily_note(current_date, new_content)
            else:
                logger.info(f"Daily note already exists for {date_str}, checking for empty GitHub sections")
                # Remove any existing empty GitHub sections
                start_line, end_line = self.formatter.find_github_section(existing_content)
                if start_line is not None and end_line is not None:
                    # Check if the section is empty (just the header and "No GitHub activity" message)
                    lines = existing_content.split('\n')
                    section_content = lines[start_line:end_line]
                    if len(section_content) <= 3 and any("*No GitHub activity for this day.*" in line for line in section_content):
                        logger.info(f"Removing empty GitHub section from {date_str}")
                        new_lines = lines[:start_line] + lines[end_line:]
                        new_content = '\n'.join(new_lines)
                        self.write_daily_note(current_date, new_content)
            
            current_date += timedelta(days=1)
        
        logger.info("Daily notes creation completed") 
"""
Obsidian integration for managing daily notes and monthly calendars.
"""

import os
import re
import logging
import calendar
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from ..config.settings import Settings
from ..utils.ai_summarizer import AISummarizer
from .calendar_manager import CalendarManager

logger = logging.getLogger(__name__)


class ObsidianManager:
    """Manages Obsidian daily notes and monthly calendars."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.vault_path = settings.obsidian_vault_path
        self.daily_notes_folder = settings.daily_notes_folder
        self.daily_notes_path = os.path.join(self.vault_path, self.daily_notes_folder)
        self.ai_summarizer = AISummarizer(settings)
        self.calendar_manager = CalendarManager(self.vault_path)
    
    def get_daily_note_path(self, date: datetime) -> str:
        """Get the path for a daily note file."""
        # Format: D:\Study tracker\Calendar\2025\July\18-07-2025.md
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
    
    def format_commit_summary(self, commit: Dict) -> str:
        """Format a commit summary for Obsidian."""
        if self.settings.brief_commit_format:
            return self.format_brief_commit_summary(commit)
        
        lines = []
        
        # Repository and commit info
        repo_name = commit['repo']
        sha = commit['sha']
        message = commit.get('readable_message', commit['message'].strip())
        url = commit['url']
        
        lines.append(f"### [{repo_name}]({url}) - {sha}")
        lines.append(f"**{message}**")
        
        # File changes summary
        if 'total_files' in commit:
            total_files = commit['total_files']
            additions = commit.get('additions', 0)
            deletions = commit.get('deletions', 0)
            
            lines.append(f"- Files changed: {total_files}")
            if additions > 0:
                lines.append(f"- Additions: +{additions}")
            if deletions > 0:
                lines.append(f"- Deletions: -{deletions}")
            
            # File types summary
            file_types = commit.get('file_types', {})
            if file_types:
                type_summary = []
                for ext, count in sorted(file_types.items()):
                    if ext == 'no_extension':
                        type_summary.append(f"{count} files")
                    else:
                        type_summary.append(f"{count} {ext} files")
                lines.append(f"- File types: {', '.join(type_summary)}")
            
            # Individual files (if not too many)
            files = commit.get('files', [])
            if files and len(files) <= 5:
                lines.append("- Files:")
                for file_info in files:
                    filename = file_info['filename']
                    status = file_info['status']
                    additions = file_info.get('additions', 0)
                    deletions = file_info.get('deletions', 0)
                    
                    status_emoji = {
                        'added': '➕',
                        'modified': '✏️',
                        'removed': '🗑️',
                        'renamed': '🔄'
                    }.get(status, '📄')
                    
                    change_info = []
                    if additions > 0:
                        change_info.append(f"+{additions}")
                    if deletions > 0:
                        change_info.append(f"-{deletions}")
                    
                    change_str = f" ({', '.join(change_info)})" if change_info else ""
                    lines.append(f"  - {status_emoji} {filename}{change_str}")
        
        return '\n'.join(lines)
    
    def format_brief_commit_summary(self, commit: Dict) -> str:
        """Format a brief commit summary with smaller font and minimal info."""
        lines = []
        
        # Repository and commit info
        repo_name = commit['repo']
        sha = commit['sha']
        message = commit.get('readable_message', commit['message'].strip())
        url = commit['url']
        
        # Time estimate
        time_estimate = self.ai_summarizer.generate_commit_time_estimate(commit)
        time_str = f" ({time_estimate})" if time_estimate else ""
        
        lines.append(f"<small>**[{repo_name}]({url})** - {sha}{time_str}</small>")
        lines.append(f"<small>{message}</small>")
        
        # Brief file changes summary
        if 'total_files' in commit:
            total_files = commit['total_files']
            additions = commit.get('additions', 0)
            deletions = commit.get('deletions', 0)
            
            # Count file types for summary
            file_types = commit.get('file_types', {})
            type_counts = []
            for ext, count in sorted(file_types.items()):
                if ext == 'no_extension':
                    type_counts.append(f"{count} files")
                else:
                    type_counts.append(f"{count} {ext}")
            
            # Create one-line summary
            summary_parts = []
            if total_files > 0:
                summary_parts.append(f"{total_files} files")
            if additions > 0:
                summary_parts.append(f"+{additions}")
            if deletions > 0:
                summary_parts.append(f"-{deletions}")
            if type_counts:
                summary_parts.extend(type_counts[:2])  # Limit to 2 file types
            
            if summary_parts:
                lines.append(f"<small>📄 {', '.join(summary_parts)}</small>")
        
        return '\n'.join(lines)
    
    def format_daily_github_section(self, commits: List[Dict], date: datetime = None) -> str:
        """Format the GitHub section for a daily note."""
        if not commits:
            return ""
        
        lines = []
        lines.append("## 📊 GitHub Activity")
        lines.append("")
        
        # AI Summary (if enabled)
        if date and self.settings.enable_ai_summary:
            ai_summary = self.ai_summarizer.generate_daily_summary(commits, date)
            if ai_summary:
                lines.append("### 🤖 AI Summary")
                lines.append(ai_summary)
                lines.append("")
        
        # Summary statistics
        total_commits = len(commits)
        total_additions = sum(commit.get('additions', 0) for commit in commits)
        total_deletions = sum(commit.get('deletions', 0) for commit in commits)
        repos_worked_on = set(commit['repo'] for commit in commits)
        
        lines.append(f"**Summary:** {total_commits} commits across {len(repos_worked_on)} repositories")
        if total_additions > 0 or total_deletions > 0:
            lines.append(f"**Changes:** +{total_additions} -{total_deletions} lines")
        lines.append("")
        
        # Individual commits
        for commit in commits:
            lines.append(self.format_commit_summary(commit))
            lines.append("")
        
        return '\n'.join(lines)
    
    def find_github_section(self, content: str) -> tuple[Optional[int], Optional[int]]:
        """Find the GitHub section in the content."""
        lines = content.split('\n')
        
        start_line = None
        end_line = None
        
        for i, line in enumerate(lines):
            if line.strip() == "## 📊 GitHub Activity":
                start_line = i
                break
        
        if start_line is None:
            return None, None
        
        # Find the end of the section (next section or end of file)
        for i in range(start_line + 1, len(lines)):
            if lines[i].strip().startswith('## ') and lines[i].strip() != "## 📊 GitHub Activity":
                end_line = i
                break
        
        if end_line is None:
            end_line = len(lines)
        
        logger.debug(f"Found GitHub section at lines {start_line}-{end_line}")
        return start_line, end_line
    
    def update_daily_note(self, date: datetime, commits: List[Dict]):
        """Update a daily note with GitHub activity."""
        logger.info(f"Updating daily note for {date.strftime('%Y-%m-%d')} with {len(commits)} commits")
        
        existing_content = self.read_daily_note(date)
        
        if existing_content is None:
            # Create new daily note
            logger.info(f"Creating new daily note for {date.strftime('%Y-%m-%d')}")
            lines = []
            lines.append(f"# {date.strftime('%A, %B %d, %Y')}")
            lines.append("")
            # Only add GitHub section if there are commits
            if commits:
                lines.append(self.format_daily_github_section(commits, date))
            new_content = '\n'.join(lines)
        else:
            # Update existing daily note - preserve all existing content
            logger.info(f"Updating existing daily note for {date.strftime('%Y-%m-%d')}")
            
            start_line, end_line = self.find_github_section(existing_content)
            lines = existing_content.split('\n')
            
            if commits:
                # Add or update GitHub section with actual commits
                github_section = self.format_daily_github_section(commits, date)
                
                if start_line is not None and end_line is not None:
                    # Replace existing GitHub section
                    logger.debug(f"Replacing existing GitHub section (lines {start_line}-{end_line})")
                    new_lines = lines[:start_line] + [github_section] + lines[end_line:]
                else:
                    # Add GitHub section at the end, preserving all existing content
                    logger.debug("Adding new GitHub section at the end")
                    # Add a blank line before the GitHub section if the file doesn't end with one
                    if lines and lines[-1].strip():
                        lines.append("")
                    new_lines = lines + [github_section]
            else:
                # No commits - remove any existing GitHub section
                if start_line is not None and end_line is not None:
                    logger.debug(f"Removing existing GitHub section (lines {start_line}-{end_line})")
                    new_lines = lines[:start_line] + lines[end_line:]
                else:
                    # No GitHub section to remove
                    new_lines = lines
            
            new_content = '\n'.join(new_lines)
        
        self.write_daily_note(date, new_content)
    
    def backfill_daily_notes(self, daily_commits: Dict[str, List[Dict]]):
        """Backfill daily notes with GitHub activity."""
        logger.info(f"Starting backfill for {len(daily_commits)} days")
        for date_str, commits in daily_commits.items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            logger.info(f"Processing {date_str}: {len(commits)} commits")
            self.update_daily_note(date, commits)
        logger.info("Backfill completed")
    
    def create_monthly_calendars_for_range(self, start_date: datetime, end_date: datetime):
        """Create monthly calendar files for the date range."""
        self.calendar_manager.create_calendars_for_range(start_date, end_date)
    
    def create_monthly_calendar(self, year: int, month: int):
        """Create a monthly calendar file for the specified year and month."""
        self.calendar_manager.create_monthly_calendar(year, month)
    
    def create_daily_notes_for_range(self, start_date: datetime, end_date: datetime):
        """Create daily notes for a date range, even if no commits exist."""
        logger.info(f"Creating daily notes for range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Create monthly calendar files for the range
        self.create_monthly_calendars_for_range(start_date, end_date)
        
        current_date = start_date
        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            
            # Check if daily note already exists
            existing_content = self.read_daily_note(current_date)
            if existing_content is None:
                logger.info(f"Creating daily note for {date_str} (no existing file)")
                # Create empty daily note without GitHub section
                lines = []
                lines.append(f"# {current_date.strftime('%A, %B %d, %Y')}")
                lines.append("")
                new_content = '\n'.join(lines)
                self.write_daily_note(current_date, new_content)
            else:
                logger.info(f"Daily note already exists for {date_str}, checking for empty GitHub sections")
                # Remove any existing empty GitHub sections
                start_line, end_line = self.find_github_section(existing_content)
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
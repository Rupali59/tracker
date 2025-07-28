import os
import re
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import config

logger = logging.getLogger(__name__)

class ObsidianUpdater:
    def __init__(self):
        self.vault_path = config.OBSIDIAN_VAULT_PATH
        self.daily_notes_folder = config.DAILY_NOTES_FOLDER
        self.daily_notes_path = os.path.join(self.vault_path, self.daily_notes_folder)
        
    def get_daily_note_path(self, date: datetime) -> str:
        """Get the path for a daily note file"""
        # Format: D:\Study tracker\Calendar\2025\July\18-07-2025.md
        year = date.strftime('%Y')
        month = date.strftime('%B')  # Full month name (January, February, etc.)
        day_month = date.strftime('%d-%m-%Y')  # 18-07-2025 format
        
        # Create the path structure
        month_path = os.path.join(self.vault_path, 'Calendar', year, month)
        filename = f"{day_month}.md"
        return os.path.join(month_path, filename)
    
    def read_daily_note(self, date: datetime) -> Optional[str]:
        """Read the content of a daily note"""
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
        """Write content to a daily note"""
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
        """Format a commit summary for Obsidian"""
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
    
    def format_daily_github_section(self, commits: List[Dict]) -> str:
        """Format the GitHub section for a daily note"""
        if not commits:
            return ""
        
        lines = []
        lines.append("## 📊 GitHub Activity")
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
        """Find the GitHub section in the content"""
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
        """Update a daily note with GitHub activity"""
        logger.info(f"Updating daily note for {date.strftime('%Y-%m-%d')} with {len(commits)} commits")
        
        existing_content = self.read_daily_note(date)
        
        if existing_content is None:
            # Create new daily note
            logger.info(f"Creating new daily note for {date.strftime('%Y-%m-%d')}")
            lines = []
            lines.append(f"# {date.strftime('%A, %B %d, %Y')}")
            lines.append("")
            if commits:
                lines.append(self.format_daily_github_section(commits))
            else:
                # Create empty daily note with placeholder
                lines.append("## 📊 GitHub Activity")
                lines.append("")
                lines.append("*No GitHub activity for this day.*")
            new_content = '\n'.join(lines)
        else:
            # Update existing daily note - preserve all existing content
            logger.info(f"Updating existing daily note for {date.strftime('%Y-%m-%d')}")
            
            # Always add GitHub section, regardless of whether there are commits
            if commits:
                github_section = self.format_daily_github_section(commits)
            else:
                github_section = "## 📊 GitHub Activity\n\n*No GitHub activity for this day.*"
            
            start_line, end_line = self.find_github_section(existing_content)
            
            lines = existing_content.split('\n')
            
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
            
            new_content = '\n'.join(new_lines)
        
        self.write_daily_note(date, new_content)
    
    def backfill_daily_notes(self, daily_commits: Dict[str, List[Dict]]):
        """Backfill daily notes with GitHub activity"""
        logger.info(f"Starting backfill for {len(daily_commits)} days")
        for date_str, commits in daily_commits.items():
            date = datetime.strptime(date_str, '%Y-%m-%d')
            logger.info(f"Processing {date_str}: {len(commits)} commits")
            self.update_daily_note(date, commits)
        logger.info("Backfill completed")
    
    def create_daily_notes_for_range(self, start_date: datetime, end_date: datetime):
        """Create daily notes for a date range, even if no commits exist"""
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
                self.update_daily_note(current_date, [])  # Empty commits list
            else:
                logger.info(f"Daily note already exists for {date_str}, adding GitHub section if missing")
                # Check if GitHub section exists, if not add it
                start_line, end_line = self.find_github_section(existing_content)
                if start_line is None:
                    logger.info(f"Adding GitHub section to existing daily note for {date_str}")
                    self.update_daily_note(current_date, [])  # This will add the GitHub section
                else:
                    logger.debug(f"GitHub section already exists for {date_str}, skipping")
            
            current_date += timedelta(days=1)
        
        logger.info("Daily notes creation completed")
    
    def create_monthly_calendars_for_range(self, start_date: datetime, end_date: datetime):
        """Create monthly calendar files for the date range"""
        logger.info(f"Creating monthly calendars for range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        # Get all months in the range
        current_date = start_date.replace(day=1)  # Start from first day of month
        end_month = end_date.replace(day=1)
        
        while current_date <= end_month:
            year = current_date.year
            month = current_date.month
            
            # Create monthly calendar file
            self.create_monthly_calendar(year, month)
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        logger.info("Monthly calendars creation completed")
    
    def create_monthly_calendar(self, year: int, month: int):
        """Create a monthly calendar file for the specified year and month"""
        month_name = datetime(year, month, 1).strftime('%B')
        calendar_filename = f"{month_name}.md"
        calendar_path = os.path.join(self.vault_path, 'Calendar', str(year), calendar_filename)
        
        logger.info(f"Creating monthly calendar: {calendar_path}")
        
        # Check if calendar file already exists
        if os.path.exists(calendar_path):
            logger.debug(f"Monthly calendar already exists: {calendar_path}")
            return
        
        # Try to copy from existing months in the same year
        existing_template = self.find_existing_monthly_calendar_template(year)
        if existing_template:
            logger.info(f"Copying template from existing calendar: {existing_template}")
            self.copy_monthly_calendar_template(existing_template, calendar_path, year, month)
        else:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(calendar_path), exist_ok=True)
            
            # Generate calendar content
            calendar_content = self.generate_monthly_calendar_content(year, month)
            
            try:
                with open(calendar_path, 'w', encoding='utf-8') as f:
                    f.write(calendar_content)
                logger.info(f"Successfully created monthly calendar: {calendar_path}")
            except Exception as e:
                logger.error(f"Error creating monthly calendar {calendar_path}: {e}")
    
    def find_existing_monthly_calendar_template(self, year: int) -> Optional[str]:
        """Find an existing monthly calendar file to use as template"""
        calendar_dir = os.path.join(self.vault_path, 'Calendar', str(year))
        
        if not os.path.exists(calendar_dir):
            return None
        
        # Look for existing month files
        for filename in os.listdir(calendar_dir):
            if filename.endswith('.md') and filename != 'README.md':
                template_path = os.path.join(calendar_dir, filename)
                logger.debug(f"Found existing calendar template: {template_path}")
                return template_path
        
        return None
    
    def copy_monthly_calendar_template(self, template_path: str, target_path: str, year: int, month: int):
        """Copy and adapt a monthly calendar template"""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Adapt the template for the new month
            adapted_content = self.adapt_monthly_calendar_template(template_content, year, month)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
            
            logger.info(f"Successfully copied and adapted monthly calendar: {target_path}")
            
        except Exception as e:
            logger.error(f"Error copying monthly calendar template: {e}")
            # Fallback to generating new content
            calendar_content = self.generate_monthly_calendar_content(year, month)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(calendar_content)
    
    def adapt_monthly_calendar_template(self, template_content: str, year: int, month: int) -> str:
        """Adapt a monthly calendar template for a different month"""
        month_name = datetime(year, month, 1).strftime('%B')
        
        # Replace the title
        adapted_content = template_content.replace(
            re.search(r'# [A-Za-z]+ \d{4}', template_content).group(),
            f"# {month_name} {year}"
        )
        
        # Regenerate the calendar view section
        import calendar
        cal = calendar.monthcalendar(year, month)
        
        # Find and replace the calendar view section
        calendar_section_start = template_content.find("## 📅 Calendar View")
        if calendar_section_start != -1:
            # Find the end of the calendar section (next section or end of file)
            lines = template_content.split('\n')
            start_line = None
            end_line = None
            
            for i, line in enumerate(lines):
                if line.strip() == "## 📅 Calendar View":
                    start_line = i
                elif start_line is not None and line.strip().startswith('## ') and line.strip() != "## 📅 Calendar View":
                    end_line = i
                    break
            
            if end_line is None:
                end_line = len(lines)
            
            # Generate new calendar content
            calendar_lines = []
            calendar_lines.append("## 📅 Calendar View")
            calendar_lines.append("")
            calendar_lines.append("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
            calendar_lines.append("|-----|-----|-----|-----|-----|-----|-----|")
            
            for week in cal:
                week_line = "|"
                for day in week:
                    if day == 0:
                        week_line += " |"
                    else:
                        daily_note_filename = f"{day:02d}-{month:02d}-{year}.md"
                        week_line += f" [[{daily_note_filename}|{day}]] |"
                calendar_lines.append(week_line)
            
            # Replace the calendar section
            new_lines = lines[:start_line] + calendar_lines + lines[end_line:]
            adapted_content = '\n'.join(new_lines)
        
        # Update quick links section
        quick_links_start = adapted_content.find("## 🔗 Quick Links")
        if quick_links_start != -1:
            lines = adapted_content.split('\n')
            start_line = None
            end_line = None
            
            for i, line in enumerate(lines):
                if line.strip() == "## 🔗 Quick Links":
                    start_line = i
                elif start_line is not None and line.strip().startswith('## ') and line.strip() != "## 🔗 Quick Links":
                    end_line = i
                    break
            
            if end_line is None:
                end_line = len(lines)
            
            # Generate new quick links
            quick_links = []
            quick_links.append("## 🔗 Quick Links")
            quick_links.append("")
            
            _, last_day = calendar.monthrange(year, month)
            for day in range(1, last_day + 1):
                daily_note_filename = f"{day:02d}-{month:02d}-{year}.md"
                date_obj = datetime(year, month, day)
                day_name = date_obj.strftime('%A')
                quick_links.append(f"- [[{daily_note_filename}|{day_name}, {month_name} {day}]]")
            
            # Replace the quick links section
            new_lines = lines[:start_line] + quick_links + lines[end_line:]
            adapted_content = '\n'.join(new_lines)
        
        return adapted_content
    
    def generate_monthly_calendar_content(self, year: int, month: int) -> str:
        """Generate content for a monthly calendar file"""
        month_name = datetime(year, month, 1).strftime('%B')
        
        # Get calendar for the month
        import calendar
        cal = calendar.monthcalendar(year, month)
        
        lines = []
        lines.append(f"# {month_name} {year}")
        lines.append("")
        lines.append("## 📅 Calendar View")
        lines.append("")
        
        # Add calendar header
        lines.append("| Mon | Tue | Wed | Thu | Fri | Sat | Sun |")
        lines.append("|-----|-----|-----|-----|-----|-----|-----|")
        
        # Add calendar weeks
        for week in cal:
            week_line = "|"
            for day in week:
                if day == 0:
                    week_line += " |"
                else:
                    # Create link to daily note
                    daily_note_filename = f"{day:02d}-{month:02d}-{year}.md"
                    week_line += f" [[{daily_note_filename}|{day}]] |"
            lines.append(week_line)
        
        lines.append("")
        lines.append("## 📊 Monthly Summary")
        lines.append("")
        lines.append("*GitHub activity and notes will be added here.*")
        lines.append("")
        
        # Add quick links to daily notes
        lines.append("## 🔗 Quick Links")
        lines.append("")
        
        # Get number of days in month
        _, last_day = calendar.monthrange(year, month)
        
        for day in range(1, last_day + 1):
            daily_note_filename = f"{day:02d}-{month:02d}-{year}.md"
            date_obj = datetime(year, month, day)
            day_name = date_obj.strftime('%A')
            lines.append(f"- [[{daily_note_filename}|{day_name}, {month_name} {day}]]")
        
        return '\n'.join(lines)
    
    def append_github_section_to_existing(self, date: datetime, commits: List[Dict]):
        """Safely append GitHub section to existing daily note without overwriting content"""
        logger.info(f"Appending GitHub section to existing daily note for {date.strftime('%Y-%m-%d')}")
        
        existing_content = self.read_daily_note(date)
        if existing_content is None:
            logger.warning(f"No existing content found for {date.strftime('%Y-%m-%d')}, creating new file")
            self.update_daily_note(date, commits)
            return
        
        # Check if GitHub section already exists
        start_line, end_line = self.find_github_section(existing_content)
        if start_line is not None:
            logger.info(f"GitHub section already exists for {date.strftime('%Y-%m-%d')}, updating it")
            self.update_daily_note(date, commits)
            return
        
        # Append GitHub section to existing content
        if commits:
            github_section = self.format_daily_github_section(commits)
        else:
            github_section = "## 📊 GitHub Activity\n\n*No GitHub activity for this day.*"
        
        # Ensure there's a blank line before the new section
        lines = existing_content.split('\n')
        if lines and lines[-1].strip():
            lines.append("")
        
        new_content = '\n'.join(lines) + '\n' + github_section
        self.write_daily_note(date, new_content)
        logger.info(f"Successfully appended GitHub section to existing daily note for {date.strftime('%Y-%m-%d')}") 
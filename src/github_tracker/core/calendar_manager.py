"""
Calendar Manager for creating and managing monthly calendar files.
"""

import os
import calendar
import logging
from datetime import datetime, timedelta
from typing import Optional

logger = logging.getLogger(__name__)


class CalendarManager:
    """Manages monthly calendar file creation and organization."""
    
    def __init__(self, vault_path: str):
        """Initialize the calendar manager."""
        self.vault_path = vault_path
        self.calendar_path = os.path.join(vault_path, 'Calendar')
        
        # Ensure calendar directory exists
        if not os.path.exists(self.calendar_path):
            os.makedirs(self.calendar_path)
            logger.info(f"Created calendar directory: {self.calendar_path}")
    
    def create_monthly_calendar_content(self, year: int, month: int) -> str:
        """Generate content for a monthly calendar file."""
        month_name = datetime(year, month, 1).strftime('%B')
        
        # Get calendar for the month
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
                    # Create link to daily note with correct path
                    daily_note_filename = f"{day:02d}-{month:02d}-{year}.md"
                    # Use standard markdown link format with correct path
                    month_folder = datetime(year, month, 1).strftime('%B')
                    file_path = f"{year}/{month_folder}/{daily_note_filename}"
                    week_line += f" [{day}]({file_path}) |"
            lines.append(week_line)
        
        lines.append("")
        lines.append("## 📊 Monthly Summary")
        lines.append("")
        lines.append("*GitHub activity and notes will be added here.*")
        lines.append("")
        
        return '\n'.join(lines)
    
    def get_calendar_file_path(self, year: int, month: int) -> str:
        """Get the path for a monthly calendar file."""
        month_name = datetime(year, month, 1).strftime('%B')
        year_path = os.path.join(self.calendar_path, str(year))
        month_folder = os.path.join(year_path, month_name)
        return os.path.join(month_folder, f"{month_name}.md")
    
    def create_monthly_calendar(self, year: int, month: int) -> bool:
        """Create a monthly calendar file."""
        calendar_file_path = self.get_calendar_file_path(year, month)
        
        # Check if file already exists
        if os.path.exists(calendar_file_path):
            logger.debug(f"Calendar file already exists: {calendar_file_path}")
            return False
        
        # Create year and month directories if they don't exist
        year_path = os.path.dirname(calendar_file_path)
        os.makedirs(year_path, exist_ok=True)
        
        # Generate calendar content
        content = self.create_monthly_calendar_content(year, month)
        
        # Write the file
        with open(calendar_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Created monthly calendar: {calendar_file_path}")
        return True
    
    def create_calendars_for_range(self, start_date: datetime, end_date: datetime):
        """Create calendar files for all months in a date range."""
        logger.info(f"Creating monthly calendars for range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
        
        current_date = start_date.replace(day=1)  # Start from first day of month
        
        while current_date <= end_date:
            year = current_date.year
            month = current_date.month
            
            self.create_monthly_calendar(year, month)
            
            # Move to next month
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)
        
        logger.info("Monthly calendars creation completed")
    
    def create_all_calendars(self, start_year: int = 2024, end_year: int = 2026):
        """Create calendar files for all months in the specified year range."""
        logger.info(f"Creating calendar files for years {start_year}-{end_year}")
        
        created_count = 0
        existing_count = 0
        
        for year in range(start_year, end_year + 1):
            for month in range(1, 13):
                if self.create_monthly_calendar(year, month):
                    created_count += 1
                else:
                    existing_count += 1
        
        logger.info(f"Calendar creation summary: {created_count} created, {existing_count} existing")
        return created_count, existing_count
    
    def reorganize_calendars(self):
        """Reorganize existing calendar files into month folders."""
        logger.info("Reorganizing calendar structure into month folders")
        
        moved_count = 0
        created_count = 0
        
        # Process each year directory
        for year_dir in os.listdir(self.calendar_path):
            year_path = os.path.join(self.calendar_path, year_dir)
            
            # Skip if not a directory or not a year
            if not os.path.isdir(year_path) or not year_dir.isdigit():
                continue
                
            year = int(year_dir)
            logger.info(f"Processing year: {year}")
            
            # Process each month file in the year directory
            for filename in os.listdir(year_path):
                if not filename.endswith('.md'):
                    continue
                    
                # Extract month name from filename
                month_name = filename.replace('.md', '')
                
                # Create month folder path
                month_folder = os.path.join(year_path, month_name)
                
                # Create month folder if it doesn't exist
                if not os.path.exists(month_folder):
                    os.makedirs(month_folder)
                    logger.info(f"Created month folder: {year}/{month_name}")
                    created_count += 1
                
                # Move the calendar file to the month folder
                old_file = os.path.join(year_path, filename)
                new_file = os.path.join(month_folder, filename)
                
                if os.path.exists(new_file):
                    logger.debug(f"Skipping existing: {year}/{month_name}/{filename}")
                else:
                    os.rename(old_file, new_file)
                    logger.info(f"Moved: {year}/{month_name}/{filename}")
                    moved_count += 1
        
        logger.info(f"Reorganization summary: {created_count} folders created, {moved_count} files moved")
        return created_count, moved_count
    
    def remove_quick_links_section(self, content: str) -> str:
        """Remove the Quick Links section from calendar content."""
        lines = content.split('\n')
        new_lines = []
        skip_section = False
        
        for line in lines:
            # Start skipping when we hit the Quick Links section
            if line.strip() == "## 🔗 Quick Links":
                skip_section = True
                continue
            
            # Stop skipping when we hit the next section or end of file
            if skip_section and line.strip().startswith('## '):
                skip_section = False
            
            # Add line if we're not in the Quick Links section
            if not skip_section:
                new_lines.append(line)
        
        return '\n'.join(new_lines)
    
    def clean_calendar_files(self):
        """Remove Quick Links sections from all calendar files."""
        logger.info("Cleaning calendar files - removing Quick Links sections")
        
        import glob
        calendar_files = glob.glob(os.path.join(self.calendar_path, '**', '*.md'), recursive=True)
        
        processed_count = 0
        modified_count = 0
        
        for file_path in calendar_files:
            filename = os.path.basename(file_path)
            
            # Check if it's a month file
            month_names = ['January', 'February', 'March', 'April', 'May', 'June', 
                          'July', 'August', 'September', 'October', 'November', 'December']
            
            if any(month in filename for month in month_names):
                try:
                    # Read the file
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    original_content = content
                    
                    # Remove Quick Links section
                    new_content = self.remove_quick_links_section(content)
                    
                    # Write back if content changed
                    if new_content != original_content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        
                        rel_path = os.path.relpath(file_path, self.calendar_path)
                        logger.info(f"Modified: {rel_path}")
                        modified_count += 1
                    
                    processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing {file_path}: {e}")
        
        logger.info(f"Calendar cleaning summary: {processed_count} processed, {modified_count} modified")
        return processed_count, modified_count 
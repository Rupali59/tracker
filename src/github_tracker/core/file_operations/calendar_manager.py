"""
Calendar file operations for Obsidian integration.
"""

import os
import logging
from datetime import datetime
from typing import Optional
from ...config.settings import Settings
from ..formatters.calendar_formatter import CalendarFormatter

logger = logging.getLogger(__name__)


class CalendarManager:
    """Handles file operations for monthly calendars."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.vault_path = settings.obsidian_vault_path
        self.formatter = CalendarFormatter(settings)
    
    def create_monthly_calendar(self, year: int, month: int):
        """Create a monthly calendar file for the specified year and month."""
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
            calendar_content = self.formatter.generate_monthly_calendar_content(year, month)
            
            try:
                with open(calendar_path, 'w', encoding='utf-8') as f:
                    f.write(calendar_content)
                logger.info(f"Successfully created monthly calendar: {calendar_path}")
            except Exception as e:
                logger.error(f"Error creating monthly calendar {calendar_path}: {e}")
    
    def find_existing_monthly_calendar_template(self, year: int) -> Optional[str]:
        """Find an existing monthly calendar file to use as template."""
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
        """Copy and adapt a monthly calendar template."""
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            
            # Adapt the template for the new month
            adapted_content = self.formatter.adapt_monthly_calendar_template(template_content, year, month)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(adapted_content)
            
            logger.info(f"Successfully copied and adapted monthly calendar: {target_path}")
            
        except Exception as e:
            logger.error(f"Error copying monthly calendar template: {e}")
            # Fallback to generating new content
            calendar_content = self.formatter.generate_monthly_calendar_content(year, month)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(calendar_content)
    
    def create_monthly_calendars_for_range(self, start_date: datetime, end_date: datetime):
        """Create monthly calendar files for the date range."""
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
"""
Calendar formatting utilities for Obsidian integration.
"""

import logging
import calendar
import re
from datetime import datetime
from typing import Optional
from ...config.settings import Settings

logger = logging.getLogger(__name__)


class CalendarFormatter:
    """Handles formatting of monthly calendars for Obsidian."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
    
    def generate_monthly_calendar_content(self, year: int, month: int) -> str:
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
    
    def adapt_monthly_calendar_template(self, template_content: str, year: int, month: int) -> str:
        """Adapt a monthly calendar template for a different month."""
        month_name = datetime(year, month, 1).strftime('%B')
        
        # Replace the title
        adapted_content = template_content.replace(
            re.search(r'# [A-Za-z]+ \d{4}', template_content).group(),
            f"# {month_name} {year}"
        )
        
        # Regenerate the calendar view section
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
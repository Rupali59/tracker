"""
Settings management for GitHub Tracker.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Configuration settings for GitHub Tracker."""
    
    def __init__(self):
        # GitHub Configuration
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = os.getenv('GITHUB_USERNAME')
        
        # Obsidian Configuration
        self.obsidian_vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
        self.daily_notes_folder = os.getenv('DAILY_NOTES_FOLDER', 'Calendar')
        
        # Application Configuration
        self.days_to_backfill = int(os.getenv('DAYS_TO_BACKFILL', '30'))
        self.max_commits_per_day = int(os.getenv('MAX_COMMITS_PER_DAY', '10'))
        
        # GitHub Filtering and Formatting
        self.filter_quartz_sync = os.getenv('FILTER_QUARTZ_SYNC', 'true').lower() == 'true'
        self.make_commits_readable = os.getenv('MAKE_COMMITS_READABLE', 'true').lower() == 'true'
        self.quartz_filter_keywords = os.getenv('QUARTZ_FILTER_KEYWORDS', 'quartz,sync,update,auto').split(',')
    
    def validate(self) -> List[str]:
        """Validate required settings and return list of missing variables."""
        missing_vars = []
        
        if not self.github_token:
            missing_vars.append('GITHUB_TOKEN')
        
        if not self.github_username:
            missing_vars.append('GITHUB_USERNAME')
        
        if not self.obsidian_vault_path:
            missing_vars.append('OBSIDIAN_VAULT_PATH')
        
        return missing_vars
    
    def is_valid(self) -> bool:
        """Check if all required settings are present."""
        return len(self.validate()) == 0 
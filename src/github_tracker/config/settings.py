"""
Settings management for GitHub Tracker.
"""

import os
import logging
from typing import List
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


class Settings:
    """Configuration settings for GitHub Tracker."""
    
    def __init__(self):
        # GitHub Configuration
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = os.getenv('GITHUB_USERNAME')
        
        # Obsidian Configuration
        self.obsidian_vault_path = os.getenv('OBSIDIAN_VAULT_PATH', '/Users/rupalib59/Study tracker')
        self.daily_notes_folder = os.getenv('DAILY_NOTES_FOLDER', 'Calendar')
        
        # Application Configuration
        self.days_to_backfill = int(os.getenv('DAYS_TO_BACKFILL', '90'))
        self.max_commits_per_day = int(os.getenv('MAX_COMMITS_PER_DAY', '10'))
        
        # GitHub Filtering and Formatting
        self.filter_quartz_sync = os.getenv('FILTER_QUARTZ_SYNC', 'true').lower() == 'true'
        self.make_commits_readable = os.getenv('MAKE_COMMITS_READABLE', 'true').lower() == 'true'
        self.quartz_filter_keywords = os.getenv('QUARTZ_FILTER_KEYWORDS', 'quartz,sync,update,auto').split(',')
        
        # AI Integration
        self.enable_ai_summary = os.getenv('ENABLE_AI_SUMMARY', 'true').lower() == 'true'
        self.ai_summary_prompt = os.getenv('AI_SUMMARY_PROMPT', 'Generate a brief daily summary of the GitHub activity, focusing on key accomplishments and progress made.')
        # Use Cursor's API key if available, otherwise fall back to environment variable
        self.openai_api_key = os.getenv('CURSOR_OPENAI_API_KEY') or os.getenv('OPENAI_API_KEY')
        
        # Commit Display Settings
        self.show_commit_time = os.getenv('SHOW_COMMIT_TIME', 'true').lower() == 'true'
        self.brief_commit_format = os.getenv('BRIEF_COMMIT_FORMAT', 'true').lower() == 'true'
        self.max_files_displayed = int(os.getenv('MAX_FILES_DISPLAYED', '3'))
    
    def validate(self) -> List[str]:
        """Validate required settings and return list of missing variables."""
        missing_vars = []
        
        if not self.github_token:
            missing_vars.append('GITHUB_TOKEN')
        
        if not self.github_username:
            missing_vars.append('GITHUB_USERNAME')
        
        if not self.obsidian_vault_path:
            missing_vars.append('OBSIDIAN_VAULT_PATH')
        
        # Note: OpenAI API key is optional - AI summaries will be disabled if not provided
        if self.enable_ai_summary and not self.openai_api_key:
            logger.warning("AI summaries enabled but no OpenAI API key found. AI features will be disabled.")
        
        return missing_vars
    
    def is_valid(self) -> bool:
        """Check if all required settings are present."""
        return len(self.validate()) == 0 
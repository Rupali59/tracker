import os
from dotenv import load_dotenv

load_dotenv()

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
GITHUB_USERNAME = os.getenv('GITHUB_USERNAME')

# Obsidian Configuration
OBSIDIAN_VAULT_PATH = os.getenv('OBSIDIAN_VAULT_PATH')
DAILY_NOTES_FOLDER = os.getenv('DAILY_NOTES_FOLDER', 'Calendar')

# Application Configuration
DAYS_TO_BACKFILL = int(os.getenv('DAYS_TO_BACKFILL', '30'))
MAX_COMMITS_PER_DAY = int(os.getenv('MAX_COMMITS_PER_DAY', '10'))

# GitHub Filtering and Formatting
FILTER_QUARTZ_SYNC = os.getenv('FILTER_QUARTZ_SYNC', 'true').lower() == 'true'
MAKE_COMMITS_READABLE = os.getenv('MAKE_COMMITS_READABLE', 'true').lower() == 'true'
QUARTZ_FILTER_KEYWORDS = os.getenv('QUARTZ_FILTER_KEYWORDS', 'quartz,sync,update,auto').split(',') 
#!/usr/bin/env python3
"""
Daily Scheduler for GitHub Statistics Tracker

This script can be used to run the GitHub tracker daily and update only today's daily note.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from github_stats import GitHubStats
from obsidian_updater import ObsidianUpdater
import config

# Set up logging for scheduler
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('github_tracker.log')
    ]
)
logger = logging.getLogger(__name__)

def update_today_only():
    """Update only today's daily note with GitHub activity"""
    logger.info("Starting GitHub Statistics Tracker - Daily Update")
    print("🚀 GitHub Statistics Tracker - Daily Update")
    print("=" * 50)
    
    # Check configuration
    if not check_configuration():
        sys.exit(1)
    
    try:
        # Initialize components
        logger.info("Initializing GitHub statistics tracker...")
        print("📊 Initializing GitHub statistics tracker...")
        github_stats = GitHubStats()
        
        logger.info("Initializing Obsidian updater...")
        print("📝 Initializing Obsidian updater...")
        obsidian_updater = ObsidianUpdater()
        
        # Get today's date
        today = datetime.now()
        today_str = today.strftime('%Y-%m-%d')
        logger.info(f"Processing commits for today: {today_str}")
        
        # Get commits for today only
        logger.info("Fetching GitHub commits for today...")
        print(f"🔍 Fetching GitHub commits for {today_str}...")
        daily_commits = github_stats.get_daily_commits(1)  # Only last 1 day
        
        if today_str not in daily_commits or not daily_commits[today_str]:
            logger.info("No commits found for today, creating empty daily note")
            print("ℹ️  No commits found for today, creating empty daily note.")
            commits = []
        else:
            commits = daily_commits[today_str]
        
        # Display summary
        if commits:
            total_additions = sum(commit.get('additions', 0) for commit in commits)
            total_deletions = sum(commit.get('deletions', 0) for commit in commits)
            repos_worked_on = set(commit['repo'] for commit in commits)
            
            summary_msg = f"Found {len(commits)} commits across {len(repos_worked_on)} repositories, +{total_additions} -{total_deletions} lines"
            logger.info(summary_msg)
            print(f"✅ Found {len(commits)} commits across {len(repos_worked_on)} repositories")
            print(f"📈 Changes: +{total_additions} -{total_deletions} lines")
        else:
            logger.info("No commits found, creating empty daily note")
            print("📝 Creating empty daily note for today")
        
        # Update today's daily note
        logger.info("Updating today's daily note...")
        print("📝 Updating today's daily note...")
        obsidian_updater.update_daily_note(today, commits)
        
        # Ensure monthly calendar exists for this month
        logger.info("Ensuring monthly calendar exists...")
        print("📅 Checking monthly calendar...")
        obsidian_updater.create_monthly_calendar(today.year, today.month)
        
        logger.info("Successfully updated today's daily note")
        print("✅ Successfully updated today's daily note!")
        
    except Exception as e:
        logger.error(f"Daily update error: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        sys.exit(1)

def check_configuration():
    """Check if all required configuration is set"""
    logger.info("Checking configuration for daily update...")
    required_vars = [
        ('GITHUB_TOKEN', config.GITHUB_TOKEN),
        ('GITHUB_USERNAME', config.GITHUB_USERNAME),
        ('OBSIDIAN_VAULT_PATH', config.OBSIDIAN_VAULT_PATH)
    ]
    
    missing_vars = []
    for var_name, var_value in required_vars:
        if not var_value:
            missing_vars.append(var_name)
        else:
            logger.debug(f"Configuration variable {var_name} is set")
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        return False
    
    logger.info("Configuration check passed for daily update")
    return True

if __name__ == "__main__":
    update_today_only() 
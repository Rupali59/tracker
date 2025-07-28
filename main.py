#!/usr/bin/env python3
"""
GitHub Statistics Tracker for Obsidian Daily Notes

This application fetches your GitHub commit history and updates your Obsidian daily notes
with detailed information about your coding activity.
"""

import os
import sys
import logging
from datetime import datetime, timedelta
from github_stats import GitHubStats
from obsidian_updater import ObsidianUpdater
import config

# Set up logging for main application
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('github_tracker.log')
    ]
)
logger = logging.getLogger(__name__)

def check_configuration():
    """Check if all required configuration is set"""
    logger.info("Checking configuration...")
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
    
    logger.info("Configuration check passed")
    return True

def main():
    """Main application function"""
    logger.info("Starting GitHub Statistics Tracker for Obsidian")
    print("🚀 GitHub Statistics Tracker for Obsidian")
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
        
        # Get commit history
        logger.info(f"Fetching GitHub commits for the last {config.DAYS_TO_BACKFILL} days...")
        print(f"🔍 Fetching GitHub commits for the last {config.DAYS_TO_BACKFILL} days...")
        daily_commits = github_stats.get_daily_commits(config.DAYS_TO_BACKFILL)
        
        if not daily_commits:
            logger.info("No commits found in the specified time range")
            print("ℹ️  No commits found in the specified time range.")
            return
        
        # Display summary
        total_commits = sum(len(commits) for commits in daily_commits.values())
        total_days = len(daily_commits)
        logger.info(f"Found {total_commits} commits across {total_days} days")
        print(f"✅ Found {total_commits} commits across {total_days} days")
        
        # Update Obsidian daily notes
        logger.info("Starting to update Obsidian daily notes...")
        print("📝 Updating Obsidian daily notes...")
        obsidian_updater.backfill_daily_notes(daily_commits)
        
        # Create daily notes for all days in the range, even without commits
        logger.info("Creating daily notes for all days in range...")
        print("📅 Creating daily notes for all days...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=config.DAYS_TO_BACKFILL)
        obsidian_updater.create_daily_notes_for_range(start_date, end_date)
        
        logger.info("Successfully updated all daily notes")
        print("✅ Successfully updated all daily notes!")
        
        # Show summary by date
        logger.info("Generating summary by date...")
        print("\n📈 Summary by date:")
        for date_str in sorted(daily_commits.keys(), reverse=True):
            commits = daily_commits[date_str]
            total_additions = sum(commit.get('additions', 0) for commit in commits)
            total_deletions = sum(commit.get('deletions', 0) for commit in commits)
            repos = set(commit['repo'] for commit in commits)
            
            summary_line = f"  {date_str}: {len(commits)} commits, {len(repos)} repos, +{total_additions} -{total_deletions} lines"
            logger.info(summary_line.strip())
            print(summary_line)
        
        logger.info("Application completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 
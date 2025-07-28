"""
Main entry point for GitHub Tracker.
"""

import sys
import logging
from .config.settings import Settings
from .core.tracker import GitHubTracker
from .utils.logger import setup_logging
from .utils.validator import validate_configuration, print_missing_variables

logger = logging.getLogger(__name__)


def main():
    """Main application function."""
    # Set up logging
    setup_logging()
    
    logger.info("Starting GitHub Statistics Tracker for Obsidian")
    print("🚀 GitHub Statistics Tracker for Obsidian")
    print("=" * 50)
    
    # Load and validate configuration
    settings = Settings()
    missing_vars = validate_configuration(settings)
    
    if missing_vars:
        print_missing_variables(missing_vars)
        sys.exit(1)
    
    try:
        # Initialize tracker
        tracker = GitHubTracker(settings)
        
        # Run backfill process
        daily_commits = tracker.run_backfill()
        
        if not daily_commits:
            print("ℹ️  No commits found in the specified time range.")
            return
        
        # Get and display summary
        stats = tracker.get_summary_stats(daily_commits)
        
        print(f"✅ Found {stats['total_commits']} commits across {stats['total_days']} days")
        print(f"📈 Total changes: +{stats['total_additions']} -{stats['total_deletions']} lines")
        print(f"🏗️  Repositories worked on: {len(stats['repos_worked_on'])}")
        
        # Show summary by date
        print("\n📈 Summary by date:")
        for date_str in sorted(stats['daily_summary'].keys(), reverse=True):
            daily_stats = stats['daily_summary'][date_str]
            print(f"  {date_str}: {daily_stats['commits']} commits, "
                  f"{daily_stats['repos']} repos, "
                  f"+{daily_stats['additions']} -{daily_stats['deletions']} lines")
        
        logger.info("Application completed successfully")
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
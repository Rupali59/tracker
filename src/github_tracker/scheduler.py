"""
Daily scheduler entry point for GitHub Tracker.
"""

import sys
import logging
from .config.settings import Settings
from .core.tracker import GitHubTracker
from .utils.logger import setup_logging
from .utils.validator import validate_configuration, print_missing_variables

logger = logging.getLogger(__name__)


def main():
    """Daily update scheduler function."""
    # Set up logging
    setup_logging()
    
    logger.info("Starting GitHub Statistics Tracker - Daily Update")
    print("🚀 GitHub Statistics Tracker - Daily Update")
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
        
        # Run daily update process
        daily_commits = tracker.run_daily_update()
        
        # Get today's stats
        stats = tracker.get_summary_stats(daily_commits)
        
        if stats['total_commits'] > 0:
            print(f"✅ Found {stats['total_commits']} commits for today")
            print(f"📈 Changes: +{stats['total_additions']} -{stats['total_deletions']} lines")
            print(f"🏗️  Repositories: {len(stats['repos_worked_on'])}")
        else:
            print("📝 Created empty daily note for today")
        
        logger.info("Daily update completed successfully")
        
    except Exception as e:
        logger.error(f"Daily update error: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 
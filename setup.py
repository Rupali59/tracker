#!/usr/bin/env python3
"""
Setup script for GitHub Statistics Tracker

This script helps users configure the application by creating the .env file
and providing guidance on getting the required tokens and paths.
"""

import os
import sys

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from github_tracker.config.settings import Settings
from github_tracker.utils.validator import validate_configuration, print_missing_variables


def create_env_file():
    """Create a .env file with user input"""
    print("🚀 GitHub Statistics Tracker Setup")
    print("=" * 50)
    print()
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != 'y':
            print("Setup cancelled.")
            return
    
    print("Please provide the following information:")
    print()
    
    # Get GitHub token
    print("1. GitHub Personal Access Token")
    print("   - Go to: https://github.com/settings/tokens")
    print("   - Click 'Generate new token (classic)'")
    print("   - Select scopes: 'repo' and 'read:user'")
    print("   - Copy the generated token")
    print()
    
    github_token = input("Enter your GitHub token: ").strip()
    if not github_token:
        print("❌ GitHub token is required!")
        return
    
    # Get GitHub username
    github_username = input("Enter your GitHub username: ").strip()
    if not github_username:
        print("❌ GitHub username is required!")
        return
    
    # Get Obsidian vault path
    print()
    print("2. Obsidian Vault Path")
    print("   - This should be the full path to your Obsidian vault folder")
    print("   - Example: D:\\Study tracker")
    print("   - Your daily notes will be stored in: [vault]\\Calendar\\[year]\\[month]\\[date].md")
    print()
    
    obsidian_path = input("Enter your Obsidian vault path: ").strip()
    if not obsidian_path:
        print("❌ Obsidian vault path is required!")
        return
    
    # Validate Obsidian path
    if not os.path.exists(obsidian_path):
        print(f"⚠️  Warning: Path '{obsidian_path}' does not exist!")
        response = input("Continue anyway? (y/N): ").lower()
        if response != 'y':
            return
    
    # Get daily notes folder
    daily_notes_folder = input("Enter daily notes folder name (default: 'Calendar'): ").strip()
    if not daily_notes_folder:
        daily_notes_folder = "Calendar"
    
    # Get configuration options
    print()
    print("3. Configuration Options")
    print()
    
    days_backfill = input("Days to backfill (default: 30): ").strip()
    if not days_backfill:
        days_backfill = "30"
    
    max_commits = input("Max commits per day (default: 10): ").strip()
    if not max_commits:
        max_commits = "10"
    
    # Get filtering options
    print()
    print("4. GitHub Filtering Options")
    print()
    
    filter_quartz = input("Filter out Quartz sync commits? (Y/n): ").strip().lower()
    if not filter_quartz or filter_quartz == 'y':
        filter_quartz = "true"
    else:
        filter_quartz = "false"
    
    make_readable = input("Make commit messages readable? (Y/n): ").strip().lower()
    if not make_readable or make_readable == 'y':
        make_readable = "true"
    else:
        make_readable = "false"
    
    # Create .env file
    env_content = f"""# GitHub Configuration
GITHUB_TOKEN={github_token}
GITHUB_USERNAME={github_username}

# Obsidian Configuration
OBSIDIAN_VAULT_PATH={obsidian_path}
DAILY_NOTES_FOLDER={daily_notes_folder}

# Application Configuration
DAYS_TO_BACKFILL={days_backfill}
MAX_COMMITS_PER_DAY={max_commits}

# GitHub Filtering and Formatting
FILTER_QUARTZ_SYNC={filter_quartz}
MAKE_COMMITS_READABLE={make_readable}
QUARTZ_FILTER_KEYWORDS=quartz,sync,update,auto
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        
        print()
        print("✅ Configuration saved to .env file!")
        print()
        print("Next steps:")
        print("1. Test the configuration: python main.py")
        print("2. For daily updates: python scheduler.py")
        print("3. Set up a scheduled task to run daily")
        print()
        print("For Windows Task Scheduler:")
        print("- Create a new task")
        print("- Set trigger to daily")
        print("- Action: Start a program")
        print("- Program: python")
        print("- Arguments: scheduler.py")
        print("- Start in: [path to this folder]")
        
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return


def test_configuration():
    """Test the current configuration"""
    print("🧪 Testing Configuration")
    print("=" * 30)
    
    if not os.path.exists('.env'):
        print("❌ .env file not found!")
        print("Run setup first: python setup.py")
        return
    
    try:
        # Test configuration
        settings = Settings()
        missing_vars = validate_configuration(settings)
        
        if missing_vars:
            print_missing_variables(missing_vars)
            return
        
        print("✅ All required variables are set")
        
        # Test Obsidian path
        if os.path.exists(settings.obsidian_vault_path):
            print("✅ Obsidian vault path exists")
        else:
            print("⚠️  Obsidian vault path does not exist")
        
        # Test GitHub connection
        print("🔍 Testing GitHub connection...")
        from github_tracker.core.github_client import GitHubClient
        
        github = GitHubClient(settings)
        repos = github.get_user_repos()
        print(f"✅ Connected to GitHub! Found {len(repos)} repositories")
        
        print()
        print("🎉 Configuration test successful!")
        print("You can now run: python main.py")
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")


def main():
    """Main setup function"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_configuration()
    else:
        create_env_file()


if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Setup script for GitHub Statistics Tracker

This script helps users configure the application by creating the .env file
and providing guidance on getting the required tokens and paths.
"""

import os
import sys
from pathlib import Path

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
        # Import config to test
        import config
        
        # Test required variables
        required_vars = [
            ('GITHUB_TOKEN', config.GITHUB_TOKEN),
            ('GITHUB_USERNAME', config.GITHUB_USERNAME),
            ('OBSIDIAN_VAULT_PATH', config.OBSIDIAN_VAULT_PATH)
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value:
                missing_vars.append(var_name)
        
        if missing_vars:
            print("❌ Missing required variables:")
            for var in missing_vars:
                print(f"   - {var}")
            return
        
        print("✅ All required variables are set")
        
        # Test Obsidian path
        if os.path.exists(config.OBSIDIAN_VAULT_PATH):
            print("✅ Obsidian vault path exists")
        else:
            print("⚠️  Obsidian vault path does not exist")
        
        # Test GitHub connection
        print("🔍 Testing GitHub connection...")
        from github_stats import GitHubStats
        
        github = GitHubStats()
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
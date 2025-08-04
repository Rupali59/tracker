#!/usr/bin/env python3
"""
Simple script to help set up environment variables.
"""

import os

def setup_env():
    """Set up environment variables for GitHub Tracker."""
    print("🔧 GitHub Tracker Environment Setup")
    print("=" * 40)
    
    # Get GitHub username
    github_username = input("Enter your GitHub username: ").strip()
    
    # Get GitHub token
    print("\nTo get your GitHub token:")
    print("1. Go to https://github.com/settings/tokens")
    print("2. Click 'Generate new token (classic)'")
    print("3. Give it a name like 'Obsidian Tracker'")
    print("4. Select scopes: 'repo' and 'read:user'")
    print("5. Copy the generated token")
    print()
    
    github_token = input("Enter your GitHub token: ").strip()
    
    # Get OpenAI API key (optional)
    print("\nOpenAI API key is optional (for AI summaries).")
    openai_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    # Read current .env file
    env_content = ""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_content = f.read()
    
    # Update the content
    env_content = env_content.replace('your_github_username_here', github_username)
    env_content = env_content.replace('your_github_personal_access_token_here', github_token)
    
    if openai_key:
        env_content = env_content.replace('your_openai_api_key_here', openai_key)
    
    # Write updated .env file
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print(f"\n✅ Environment file updated!")
    print(f"GitHub username: {github_username}")
    print(f"GitHub token: {'*' * len(github_token)}")
    if openai_key:
        print(f"OpenAI key: {'*' * len(openai_key)}")
    else:
        print("OpenAI key: Not set (AI features will be disabled)")
    
    print("\nYou can now run: python3 main.py")

if __name__ == "__main__":
    setup_env() 
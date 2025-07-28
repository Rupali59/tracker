# Installation Guide

This guide will help you set up the GitHub Statistics Tracker for Obsidian.

## Prerequisites

1. **Python 3.7 or higher**
   - Download from [python.org](https://python.org)
   - Make sure Python is added to your PATH

2. **GitHub Account**
   - You'll need a GitHub account to generate an access token

3. **Obsidian Vault**
   - An existing Obsidian vault where you want to store daily notes

## Step 1: Install Dependencies

Open a terminal/command prompt in the tracker directory and run:

```bash
pip install -r requirements.txt
```

## Step 2: Configure the Application

### Option A: Interactive Setup (Recommended)

Run the interactive setup script:

```bash
python setup.py
```

This will guide you through:
- Getting your GitHub token
- Setting your Obsidian vault path
- Configuring other options

### Option B: Manual Configuration

1. Copy `env_example.txt` to `.env`
2. Edit the `.env` file with your information:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_USERNAME=your_github_username_here

# Obsidian Configuration
OBSIDIAN_VAULT_PATH=C:\Users\YourUsername\Documents\Obsidian\YourVaultName
DAILY_NOTES_FOLDER=Daily Notes

# Application Configuration
DAYS_TO_BACKFILL=30
MAX_COMMITS_PER_DAY=10
```

## Step 3: Get Your GitHub Token

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a descriptive name like "Obsidian Tracker"
4. Select the following scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:user` (Read user profile data)
5. Click "Generate token"
6. **Copy the token immediately** (you won't see it again)
7. Paste it in your `.env` file

## Step 4: Test the Configuration

Run the test command:

```bash
python setup.py test
```

This will verify:
- All required variables are set
- GitHub connection works
- Obsidian vault path exists

## Step 5: Run the Application

### Initial Backfill (Optional)

To fill in historical data for the last 30 days:

```bash
python main.py
```

### Daily Updates

To update only today's daily note:

```bash
python scheduler.py
```

## Step 6: Set Up Daily Automation

### Windows Task Scheduler

1. Open Task Scheduler (search in Start menu)
2. Click "Create Basic Task"
3. Name: "GitHub Tracker Daily"
4. Trigger: Daily
5. Action: Start a program
6. Program: `python`
7. Arguments: `scheduler.py`
8. Start in: `[path to your tracker folder]`

### Windows Batch File

You can also use the provided batch file:

```bash
run_daily.bat
```

### PowerShell Script

For better error handling:

```powershell
.\run_daily.ps1
```

## Troubleshooting

### Common Issues

1. **"Python is not recognized"**
   - Install Python and add it to PATH
   - Or use `python3` instead of `python`

2. **"GitHub token invalid"**
   - Generate a new token with correct permissions
   - Make sure to include `repo` and `read:user` scopes

3. **"Obsidian vault not found"**
   - Check the path in your `.env` file
   - Use the full path to your Obsidian vault folder

4. **"No commits found"**
   - This is normal if you haven't made commits recently
   - Try increasing `DAYS_TO_BACKFILL` in your `.env` file

### Getting Help

1. Check the console output for error messages
2. Verify your `.env` file has all required variables
3. Test your GitHub token manually
4. Ensure your Obsidian vault path is correct

## Configuration Options

You can customize the behavior by editing your `.env` file:

- `DAYS_TO_BACKFILL`: How many days of history to process (default: 30)
- `MAX_COMMITS_PER_DAY`: Maximum commits to show per day (default: 10)
- `DAILY_NOTES_FOLDER`: Folder name for daily notes in your vault (default: "Daily Notes")

## Security Notes

- Keep your `.env` file secure and don't share it
- Your GitHub token has access to your repositories
- Consider using a dedicated GitHub account for automation
- Regularly rotate your GitHub token

## Support

If you encounter issues:

1. Check the console output for error messages
2. Verify all configuration steps were completed
3. Test individual components (GitHub connection, Obsidian path)
4. Check the README.md for additional information 
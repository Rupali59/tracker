# GitHub Statistics Tracker for Obsidian

A Python application that fetches your GitHub commit history and automatically updates your Obsidian daily notes with detailed information about your coding activity.

## Features

- 🔍 **Comprehensive Commit Analysis**: Fetches commit history from all your GitHub repositories
- 📊 **Detailed Statistics**: Analyzes file changes, additions, deletions, and file types
- 📝 **Obsidian Integration**: Automatically updates your daily notes with GitHub activity
- 🔄 **Backfill Support**: Fills in historical data for previous days
- 📈 **Rich Formatting**: Beautiful markdown formatting with emojis and links
- 🚫 **Smart Filtering**: Automatically filters out Quartz sync commits and other noise
- 📝 **Human-Readable Commits**: Converts technical commit messages to readable format
- 📅 **Monthly Calendars**: Automatically creates monthly calendar overview files
- ⚙️ **Configurable**: Customizable settings for date ranges and output format

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up configuration:
   - Copy `env_example.txt` to `.env`
   - Fill in your GitHub token and Obsidian vault path

## Configuration

Create a `.env` file with the following variables:

```env
# GitHub Configuration
GITHUB_TOKEN=your_github_personal_access_token_here
GITHUB_USERNAME=your_github_username_here

# Obsidian Configuration
OBSIDIAN_VAULT_PATH=D:\Study tracker
DAILY_NOTES_FOLDER=Calendar

# Application Configuration
DAYS_TO_BACKFILL=30
MAX_COMMITS_PER_DAY=10

# GitHub Filtering and Formatting
FILTER_QUARTZ_SYNC=true
MAKE_COMMITS_READABLE=true
QUARTZ_FILTER_KEYWORDS=quartz,sync,update,auto
```

### Getting Your GitHub Token

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name like "Obsidian Tracker"
4. Select the following scopes:
   - `repo` (Full control of private repositories)
   - `read:user` (Read user profile data)
5. Copy the generated token to your `.env` file

## Usage

Run the application:

```bash
python main.py
```

The application will:
1. Fetch your GitHub commit history for the specified number of days
2. Analyze each commit for file changes and statistics
3. Update your Obsidian daily notes with the GitHub activity section
4. Display a summary of processed data

## Output Format

The application adds a "📊 GitHub Activity" section to your daily notes with:

- **Summary statistics**: Total commits, repositories worked on, lines changed
- **Individual commits**: Repository name, commit message, file changes
- **File analysis**: File types, additions/deletions, individual file changes
- **Links**: Direct links to commits on GitHub

Example output:
```markdown
## 📊 GitHub Activity

**Summary:** 3 commits across 2 repositories
**Changes:** +45 -12 lines

### [my-project](https://github.com/username/my-project/commit/abc12345) - abc12345
**Add new feature for user authentication**
- Files changed: 2
- Additions: +25
- Deletions: -5
- File types: 1 .py files, 1 .md files
- Files:
  - ✏️ src/auth.py (+20 -3)
  - ✏️ README.md (+5 -2)
```

## Features in Detail

### Commit Analysis
- Fetches commits from all your repositories
- Analyzes file changes (additions, deletions, file types)
- Provides detailed statistics for each commit
- Links directly to GitHub commit pages
- Filters out Quartz sync commits and other noise
- Converts technical commit messages to human-readable format

### Obsidian Integration
- Automatically creates daily notes if they don't exist
- Updates existing daily notes with GitHub sections
- Preserves existing content in daily notes
- Uses proper markdown formatting for Obsidian
- Supports date-based folder structure: `Calendar/[year]/[month]/[date].md`
- Creates monthly calendar overview files: `Calendar/[year]/[Month].md`

### Backfill Support
- Processes historical data for specified number of days
- Can be run multiple times safely
- Updates only the GitHub section, preserving other content

## Configuration Options

- `DAYS_TO_BACKFILL`: Number of days to look back (default: 30)
- `MAX_COMMITS_PER_DAY`: Maximum commits to show per day (default: 10)
- `DAILY_NOTES_FOLDER`: Folder name for daily notes in your vault (default: "Calendar")
- `FILTER_QUARTZ_SYNC`: Filter out Quartz sync commits (default: true)
- `MAKE_COMMITS_READABLE`: Convert commit messages to readable format (default: true)
- `QUARTZ_FILTER_KEYWORDS`: Keywords to filter out (comma-separated)

## Troubleshooting

### Common Issues

1. **GitHub API Rate Limits**: The application respects GitHub's rate limits. If you hit limits, wait a few minutes and try again.

2. **Missing Daily Notes**: The application will create daily notes automatically if they don't exist.

3. **Permission Errors**: Ensure your GitHub token has the necessary permissions (`repo` and `read:user` scopes).

4. **Path Issues**: Make sure your `OBSIDIAN_VAULT_PATH` points to the correct Obsidian vault folder.

### Debug Mode

For troubleshooting, you can add debug prints by modifying the code or check the console output for detailed information about the process.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

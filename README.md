# GitHub Statistics Tracker for Obsidian

A Python application that fetches your GitHub commit history and automatically updates your Obsidian daily notes with detailed information about your coding activity.

## Features

- 🔍 **Comprehensive Commit Analysis**: Fetches commit history from all your GitHub repositories
- 📊 **Detailed Statistics**: Analyzes file changes, additions, deletions, and file types
- 📝 **Obsidian Integration**: Automatically updates your daily notes with GitHub activity
- 🔄 **Backfill Support**: Fills in historical data for previous days
- 🤖 **AI-Powered Summaries**: Automatic daily summaries using OpenAI
- ⏱️ **Time Estimates**: Estimated time spent on each commit
- 📱 **Brief Format**: Compact commit display with smaller font

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
OBSIDIAN_VAULT_PATH=/Users/rupalib59/Study tracker
DAILY_NOTES_FOLDER=Calendar

# Application Configuration
DAYS_TO_BACKFILL=30
MAX_COMMITS_PER_DAY=10

# GitHub Filtering and Formatting
FILTER_QUARTZ_SYNC=true
MAKE_COMMITS_READABLE=true
QUARTZ_FILTER_KEYWORDS=quartz,sync,update,auto

# AI Integration (Optional)
ENABLE_AI_SUMMARY=true
OPENAI_API_KEY=your_openai_api_key_here
AI_SUMMARY_PROMPT=Generate a brief daily summary of the GitHub activity, focusing on key accomplishments and progress made.

# Commit Display Settings
SHOW_COMMIT_TIME=true
BRIEF_COMMIT_FORMAT=true
MAX_FILES_DISPLAYED=3
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

The application adds a "📊 GitHub Activity" section to your daily notes with AI summaries, commit details, and time estimates.

Example output:
```markdown
## 📊 GitHub Activity

### 🤖 AI Summary
Today I worked on improving the user authentication system and fixing several bugs in the API.

**Summary:** 3 commits across 2 repositories
**Changes:** +45 -12 lines

<small>**[my-project](https://github.com/username/my-project/commit/abc12345)** - abc12345 (~30 min)</small>
<small>Add new feature for user authentication</small>
<small>📄 2 files, +25, -5, 1 .py, 1 .js</small>
```

## Documentation

For detailed documentation, see the [docs](docs/) folder.

## TODO / Upcoming Features

### 🔄 **WakaTime Integration**
- [ ] **WakaTime API Integration**: Fetch coding activity data from WakaTime API
- [ ] **Coding Time Tracking**: Display daily coding hours and activity patterns
- [ ] **Language Statistics**: Show programming languages used and time spent
- [ ] **Project Breakdown**: Track time spent on different projects/repositories
- [ ] **Productivity Insights**: Compare coding time with GitHub commits

### 📊 **Google Timeline History**
- [ ] **Location Data**: Import location history from Google Timeline
- [ ] **Activity Patterns**: Track daily movement and location patterns
- [ ] **Travel Insights**: Identify travel days and locations visited
- [ ] **Time-based Analysis**: Correlate location data with coding activity
- [ ] **Privacy Controls**: Configurable data retention and privacy settings

### 🔍 **Search History & Web Activity**
- [ ] **Browser Search History**: Import search queries from Chrome/Firefox/Safari
- [ ] **Search Patterns**: Analyze what you searched for and when
- [ ] **Topic Clustering**: Group related searches by topic and time
- [ ] **Research Tracking**: Track research sessions and learning patterns
- [ ] **Search Insights**: Identify trending topics and interests over time
- [ ] **Cross-Platform Search**: Aggregate searches from multiple browsers and devices

### 💰 **Financial Information**
- [ ] **Expense Tracking**: Import and categorize financial transactions
- [ ] **Spending Patterns**: Analyze daily/weekly/monthly spending habits
- [ ] **Budget Integration**: Track budget vs actual spending
- [ ] **Financial Goals**: Monitor progress towards financial objectives
- [ ] **Expense Categories**: Auto-categorize transactions (food, transport, etc.)

### 🧠 **NLP & AI Capabilities**
- [ ] **Daily Activity Summarization**: Use NLP to generate natural language summaries of daily activities
- [ ] **Intent Recognition**: Understand what you were trying to accomplish each day
- [ ] **Topic Modeling**: Automatically categorize activities and interests
- [ ] **Sentiment Analysis**: Analyze mood and productivity patterns from activities
- [ ] **Pattern Recognition**: Identify recurring activities and habits
- [ ] **Smart Categorization**: Auto-categorize activities using AI (work, learning, entertainment, etc.)
- [ ] **Contextual Understanding**: Understand relationships between different activities
- [ ] **Predictive Insights**: Predict productivity patterns and suggest optimizations

### 🎯 **Enhanced Analytics**
- [ ] **Cross-Platform Correlation**: Link GitHub activity with WakaTime, location, finances, and search history
- [ ] **Productivity Metrics**: Calculate productivity scores based on multiple data sources
- [ ] **Trend Analysis**: Identify patterns across coding, location, spending, and search behavior
- [ ] **Goal Tracking**: Set and monitor personal development goals
- [ ] **Data Visualization**: Create charts and graphs for better insights
- [ ] **Activity Timeline**: Create comprehensive daily activity timelines
- [ ] **Behavioral Insights**: Understand your daily routines and patterns

### 🔧 **Technical Improvements**
- [ ] **Modular Architecture**: Extend current class-based structure for new data sources
- [ ] **API Rate Limiting**: Implement proper rate limiting for all external APIs
- [ ] **Data Caching**: Cache API responses to reduce API calls
- [ ] **Error Handling**: Robust error handling for network issues and API failures
- [ ] **Configuration Management**: Enhanced settings for new integrations
- [ ] **NLP Pipeline**: Integrate spaCy, NLTK, or transformers for text processing
- [ ] **Search History Parsers**: Create parsers for different browser history formats
- [ ] **Data Privacy**: Implement encryption and secure storage for sensitive data
- [ ] **Real-time Processing**: Stream processing for live activity tracking

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.

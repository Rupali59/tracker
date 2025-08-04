# Changelog

## Version 2.0.0 - AI-Powered GitHub Tracker

### 🆕 New Features

#### 🤖 AI Integration
- **Automatic Daily Summaries**: AI-powered summaries of daily GitHub activity using OpenAI GPT
- **Smart Time Estimates**: Automatic estimation of time spent on each commit based on changes
- **Configurable AI Prompts**: Customizable prompts for AI summary generation
- **Optional AI Features**: AI features can be enabled/disabled via environment variables

#### 📱 Brief Commit Format
- **Compact Display**: Smaller font size for commit information using `<small>` tags
- **One-line Summaries**: Concise file change summaries (files modified, additions, deletions)
- **Time Estimates**: Display estimated time spent on each commit
- **File Type Summary**: Brief overview of file types changed

#### 📍 Improved Layout
- **Bottom Placement**: GitHub activity section now placed at the bottom of daily notes
- **Better Organization**: AI summary appears at the top of the GitHub section
- **Cleaner Format**: Reduced visual clutter with compact formatting

#### ⚙️ Enhanced Configuration
- **Updated Path**: Default Obsidian vault path updated to `/Users/rupalib59/Study tracker`
- **New Environment Variables**: Added support for AI and display settings
- **Flexible Settings**: More granular control over commit display format

### 🔧 Technical Improvements

#### New Dependencies
- Added `openai==0.28.1` for AI integration
- Updated all existing dependencies to latest stable versions

#### New Modules
- `src/github_tracker/utils/ai_summarizer.py`: AI-powered summarization
- Enhanced `src/github_tracker/core/obsidian_manager.py`: Brief format support
- Updated `src/github_tracker/config/settings.py`: New configuration options

#### Code Quality
- Improved error handling for AI integration
- Better separation of concerns between AI and display logic
- Enhanced logging for debugging

### 📝 Configuration Changes

#### New Environment Variables
```env
# AI Integration (Optional)
ENABLE_AI_SUMMARY=true
OPENAI_API_KEY=your_openai_api_key_here
AI_SUMMARY_PROMPT=Generate a brief daily summary of the GitHub activity, focusing on key accomplishments and progress made.

# Commit Display Settings
SHOW_COMMIT_TIME=true
BRIEF_COMMIT_FORMAT=true
MAX_FILES_DISPLAYED=3
```

#### Updated Default Path
- Changed from `D:\Study tracker` to `/Users/rupalib59/Study tracker`

### 🎯 User Experience Improvements

#### Visual Enhancements
- **Smaller Font**: Commit information displayed in smaller font for better readability
- **Time Estimates**: Each commit shows estimated time spent (e.g., "~30 min")
- **Brief Summaries**: One-line summaries of file changes and types
- **AI Summaries**: Professional daily summaries generated automatically

#### Better Organization
- **Bottom Placement**: GitHub section moved to bottom of daily notes
- **AI Summary First**: AI-generated summary appears at the top of GitHub section
- **Cleaner Layout**: Reduced visual clutter with compact formatting

### 🚀 Getting Started

1. **Install Dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure Environment**:
   ```bash
   cp env_example.txt .env
   # Edit .env with your GitHub token and OpenAI API key
   ```

3. **Run the Application**:
   ```bash
   python3 main.py
   ```

### 📊 Example Output

```markdown
## 📊 GitHub Activity

### 🤖 AI Summary
Today I worked on improving the user authentication system and fixing several bugs in the API. Made significant progress on the frontend components and backend validation logic.

**Summary:** 3 commits across 2 repositories
**Changes:** +45 -12 lines

<small>**[my-project](https://github.com/username/my-project/commit/abc12345)** - abc12345 (~30 min)</small>
<small>Add new feature for user authentication</small>
<small>📄 2 files, +25, -5, 1 .py, 1 .js</small>
```

### 🔮 Future Enhancements

- **Custom AI Models**: Support for different AI models and providers
- **Advanced Time Tracking**: More sophisticated time estimation algorithms
- **Commit Categories**: Automatic categorization of commits by type
- **Performance Metrics**: Code quality and productivity metrics
- **Integration APIs**: Support for other productivity tools

---

**Note**: This version introduces AI features that require an OpenAI API key. The AI features are optional and can be disabled by setting `ENABLE_AI_SUMMARY=false` in your environment configuration. 
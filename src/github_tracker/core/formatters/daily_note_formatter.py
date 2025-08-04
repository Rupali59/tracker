"""
Daily note formatting utilities for Obsidian integration.
"""

import logging
from datetime import datetime
from typing import Dict, List, Optional
from ...config.settings import Settings
from ...utils.ai_summarizer import AISummarizer
from .commit_formatter import CommitFormatter

logger = logging.getLogger(__name__)


class DailyNoteFormatter:
    """Handles formatting of daily notes and GitHub sections."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.ai_summarizer = AISummarizer(settings)
        self.commit_formatter = CommitFormatter(settings)
    
    def format_daily_github_section(self, commits: List[Dict], date: datetime = None) -> str:
        """Format the GitHub section for a daily note."""
        if not commits:
            return ""
        
        lines = []
        lines.append("## 📊 GitHub Activity")
        lines.append("")
        
        # AI Summary (if enabled)
        if date and self.settings.enable_ai_summary:
            ai_summary = self.ai_summarizer.generate_daily_summary(commits, date)
            if ai_summary:
                lines.append("### 🤖 AI Summary")
                lines.append(ai_summary)
                lines.append("")
        
        # Summary statistics
        total_commits = len(commits)
        total_additions = sum(commit.get('additions', 0) for commit in commits)
        total_deletions = sum(commit.get('deletions', 0) for commit in commits)
        repos_worked_on = set(commit['repo'] for commit in commits)
        
        lines.append(f"**Summary:** {total_commits} commits across {len(repos_worked_on)} repositories")
        if total_additions > 0 or total_deletions > 0:
            lines.append(f"**Changes:** +{total_additions} -{total_deletions} lines")
        lines.append("")
        
        # Individual commits
        for commit in commits:
            lines.append(self.commit_formatter.format_commit(commit))
            lines.append("")
        
        return '\n'.join(lines)
    
    def format_empty_github_section(self) -> str:
        """Format an empty GitHub section."""
        return "## 📊 GitHub Activity\n\n*No GitHub activity for this day.*"
    
    def format_daily_note_header(self, date: datetime) -> str:
        """Format the header for a daily note."""
        return f"# {date.strftime('%A, %B %d, %Y')}"
    
    def find_github_section(self, content: str) -> tuple[Optional[int], Optional[int]]:
        """Find the GitHub section in the content."""
        lines = content.split('\n')
        
        start_line = None
        end_line = None
        
        for i, line in enumerate(lines):
            if line.strip() == "## 📊 GitHub Activity":
                start_line = i
                break
        
        if start_line is None:
            return None, None
        
        # Find the end of the section (next section or end of file)
        for i in range(start_line + 1, len(lines)):
            if lines[i].strip().startswith('## ') and lines[i].strip() != "## 📊 GitHub Activity":
                end_line = i
                break
        
        if end_line is None:
            end_line = len(lines)
        
        logger.debug(f"Found GitHub section at lines {start_line}-{end_line}")
        return start_line, end_line
    
    def merge_content_with_github_section(self, existing_content: str, github_section: str) -> str:
        """Merge existing content with a new GitHub section."""
        start_line, end_line = self.find_github_section(existing_content)
        
        lines = existing_content.split('\n')
        
        if start_line is not None and end_line is not None:
            # Replace existing GitHub section
            logger.debug(f"Replacing existing GitHub section (lines {start_line}-{end_line})")
            new_lines = lines[:start_line] + [github_section] + lines[end_line:]
        else:
            # Add GitHub section at the end, preserving all existing content
            logger.debug("Adding new GitHub section at the end")
            # Add a blank line before the GitHub section if the file doesn't end with one
            if lines and lines[-1].strip():
                lines.append("")
            new_lines = lines + [github_section]
        
        return '\n'.join(new_lines) 
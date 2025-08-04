"""
Commit formatting utilities for Obsidian integration.
"""

import logging
from typing import Dict
from ...config.settings import Settings
from ...utils.ai_summarizer import AISummarizer

logger = logging.getLogger(__name__)


class CommitFormatter:
    """Handles formatting of GitHub commits for Obsidian."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.ai_summarizer = AISummarizer(settings)
    
    def format_commit(self, commit: Dict) -> str:
        """Format a commit summary for Obsidian."""
        if self.settings.brief_commit_format:
            return self.format_brief_commit(commit)
        return self.format_detailed_commit(commit)
    
    def format_detailed_commit(self, commit: Dict) -> str:
        """Format a detailed commit summary."""
        lines = []
        
        # Repository and commit info
        repo_name = commit['repo']
        sha = commit['sha']
        message = commit.get('readable_message', commit['message'].strip())
        url = commit['url']
        
        lines.append(f"### [{repo_name}]({url}) - {sha}")
        lines.append(f"**{message}**")
        
        # File changes summary
        if 'total_files' in commit:
            total_files = commit['total_files']
            additions = commit.get('additions', 0)
            deletions = commit.get('deletions', 0)
            
            lines.append(f"- Files changed: {total_files}")
            if additions > 0:
                lines.append(f"- Additions: +{additions}")
            if deletions > 0:
                lines.append(f"- Deletions: -{deletions}")
            
            # File types summary
            file_types = commit.get('file_types', {})
            if file_types:
                type_summary = []
                for ext, count in sorted(file_types.items()):
                    if ext == 'no_extension':
                        type_summary.append(f"{count} files")
                    else:
                        type_summary.append(f"{count} {ext} files")
                lines.append(f"- File types: {', '.join(type_summary)}")
            
            # Individual files (if not too many)
            files = commit.get('files', [])
            if files and len(files) <= 5:
                lines.append("- Files:")
                for file_info in files:
                    filename = file_info['filename']
                    status = file_info['status']
                    additions = file_info.get('additions', 0)
                    deletions = file_info.get('deletions', 0)
                    
                    status_emoji = {
                        'added': '➕',
                        'modified': '✏️',
                        'removed': '🗑️',
                        'renamed': '🔄'
                    }.get(status, '📄')
                    
                    change_info = []
                    if additions > 0:
                        change_info.append(f"+{additions}")
                    if deletions > 0:
                        change_info.append(f"-{deletions}")
                    
                    change_str = f" ({', '.join(change_info)})" if change_info else ""
                    lines.append(f"  - {status_emoji} {filename}{change_str}")
        
        return '\n'.join(lines)
    
    def format_brief_commit(self, commit: Dict) -> str:
        """Format a brief commit summary with smaller font and minimal info."""
        lines = []
        
        # Repository and commit info
        repo_name = commit['repo']
        sha = commit['sha']
        message = commit.get('readable_message', commit['message'].strip())
        url = commit['url']
        
        # Time estimate
        time_estimate = self.ai_summarizer.generate_commit_time_estimate(commit)
        time_str = f" ({time_estimate})" if time_estimate else ""
        
        lines.append(f"<small>**[{repo_name}]({url})** - {sha}{time_str}</small>")
        lines.append(f"<small>{message}</small>")
        
        # Brief file changes summary
        if 'total_files' in commit:
            total_files = commit['total_files']
            additions = commit.get('additions', 0)
            deletions = commit.get('deletions', 0)
            
            # Count file types for summary
            file_types = commit.get('file_types', {})
            type_counts = []
            for ext, count in sorted(file_types.items()):
                if ext == 'no_extension':
                    type_counts.append(f"{count} files")
                else:
                    type_counts.append(f"{count} {ext}")
            
            # Create one-line summary
            summary_parts = []
            if total_files > 0:
                summary_parts.append(f"{total_files} files")
            if additions > 0:
                summary_parts.append(f"+{additions}")
            if deletions > 0:
                summary_parts.append(f"-{deletions}")
            if type_counts:
                summary_parts.extend(type_counts[:2])  # Limit to 2 file types
            
            if summary_parts:
                lines.append(f"<small>📄 {', '.join(summary_parts)}</small>")
        
        return '\n'.join(lines) 
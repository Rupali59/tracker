"""
AI-powered summarization for GitHub activity.
"""

import logging
import openai
from typing import List, Dict, Optional
from datetime import datetime
from ..config.settings import Settings

logger = logging.getLogger(__name__)


class AISummarizer:
    """AI-powered summarization for GitHub activity."""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.api_key = settings.openai_api_key if hasattr(settings, 'openai_api_key') else None
        
        if self.api_key and self.api_key != 'your_ope************here':
            openai.api_key = self.api_key
        else:
            self.api_key = None
            logger.info("No valid OpenAI API key found. AI summaries will be disabled.")
    
    def generate_daily_summary(self, commits: List[Dict], date: datetime) -> Optional[str]:
        """Generate a brief AI summary of the day's GitHub activity."""
        if not self.settings.enable_ai_summary or not self.api_key:
            return None
        
        if not commits:
            return "No GitHub activity today."
        
        try:
            # Prepare commit data for AI
            commit_summaries = []
            total_files = 0
            total_additions = 0
            total_deletions = 0
            repos_worked_on = set()
            
            for commit in commits:
                repo = commit['repo']
                message = commit.get('readable_message', commit['message'])
                files_changed = commit.get('total_files', 0)
                additions = commit.get('additions', 0)
                deletions = commit.get('deletions', 0)
                
                commit_summaries.append(f"- {repo}: {message}")
                total_files += files_changed
                total_additions += additions
                total_deletions += deletions
                repos_worked_on.add(repo)
            
            # Create prompt for AI
            prompt = f"""
            {self.settings.ai_summary_prompt}
            
            Date: {date.strftime('%A, %B %d, %Y')}
            Total commits: {len(commits)}
            Repositories worked on: {', '.join(repos_worked_on)}
            Files changed: {total_files}
            Lines added: {total_additions}
            Lines deleted: {total_deletions}
            
            Commits:
            {chr(10).join(commit_summaries)}
            
            Please provide a brief, professional summary (2-3 sentences) of today's development work.
            """
            
            # Generate summary using OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes GitHub development activity in a concise, professional manner."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content.strip()
            logger.info(f"Generated AI summary for {date.strftime('%Y-%m-%d')}")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating AI summary: {e}")
            return None
    
    def generate_commit_time_estimate(self, commit: Dict) -> Optional[str]:
        """Estimate time spent on a commit based on changes."""
        if not self.settings.show_commit_time:
            return None
        
        files_changed = commit.get('total_files', 0)
        additions = commit.get('additions', 0)
        deletions = commit.get('deletions', 0)
        
        # Simple heuristic for time estimation
        total_changes = additions + deletions
        
        if total_changes == 0:
            return "~5 min"
        elif total_changes < 50:
            return "~15 min"
        elif total_changes < 200:
            return "~30 min"
        elif total_changes < 500:
            return "~1 hour"
        else:
            return "~2+ hours" 
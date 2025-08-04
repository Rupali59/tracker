#!/usr/bin/env python3
"""
Script to remove empty GitHub activity sections from daily notes.
"""

import os
import re
import logging
from datetime import datetime, timedelta
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_daily_notes(vault_path: str) -> List[str]:
    """Find all daily note files in the vault."""
    daily_notes = []
    calendar_path = os.path.join(vault_path, 'Calendar')
    
    if not os.path.exists(calendar_path):
        logger.warning(f"Calendar path not found: {calendar_path}")
        return daily_notes
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(calendar_path):
        for file in files:
            if file.endswith('.md') and re.match(r'\d{2}-\d{2}-\d{4}\.md', file):
                daily_notes.append(os.path.join(root, file))
    
    return daily_notes


def remove_empty_github_section(content: str) -> str:
    """Remove empty GitHub activity sections from content."""
    # Pattern to match the empty GitHub section
    pattern = r'\n## 📊 GitHub Activity\n\n\*No GitHub activity for this day\.\*\n'
    
    # Remove the pattern
    cleaned_content = re.sub(pattern, '', content)
    
    # Also remove if there's no content after the header
    pattern2 = r'\n## 📊 GitHub Activity\n\n'
    cleaned_content = re.sub(pattern2, '', cleaned_content)
    
    return cleaned_content


def cleanup_daily_note(file_path: str) -> bool:
    """Clean up a single daily note file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        cleaned_content = remove_empty_github_section(content)
        
        # Only write if content changed
        if cleaned_content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            logger.info(f"Cleaned: {file_path}")
            return True
        else:
            logger.debug(f"No changes needed: {file_path}")
            return False
            
    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")
        return False


def main():
    """Main cleanup function."""
    vault_path = "/Users/rupalib59/Study tracker"
    
    print("🧹 Cleaning up empty GitHub activity sections...")
    print(f"Vault path: {vault_path}")
    print("=" * 50)
    
    # Find all daily notes
    daily_notes = find_daily_notes(vault_path)
    print(f"Found {len(daily_notes)} daily note files")
    
    if not daily_notes:
        print("❌ No daily notes found!")
        return
    
    # Clean up each file
    cleaned_count = 0
    for file_path in daily_notes:
        if cleanup_daily_note(file_path):
            cleaned_count += 1
    
    print(f"\n✅ Cleanup completed!")
    print(f"📁 Files processed: {len(daily_notes)}")
    print(f"🧹 Files cleaned: {cleaned_count}")
    
    if cleaned_count > 0:
        print(f"✅ Removed empty GitHub sections from {cleaned_count} files")
    else:
        print("ℹ️  No empty GitHub sections found")


if __name__ == "__main__":
    main() 
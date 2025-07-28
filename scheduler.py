#!/usr/bin/env python3
"""
GitHub Statistics Tracker for Obsidian - Daily Scheduler

This script runs the daily update process to update today's Obsidian daily note
with GitHub commit history.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from github_tracker.scheduler import main

if __name__ == "__main__":
    main() 
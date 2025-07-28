#!/usr/bin/env python3
"""
GitHub Statistics Tracker for Obsidian - Main Entry Point

This script runs the main backfill process to update your Obsidian daily notes
with GitHub commit history.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from github_tracker.main import main

if __name__ == "__main__":
    main() 
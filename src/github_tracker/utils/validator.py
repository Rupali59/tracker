"""
Configuration validation utilities.
"""

import logging
from typing import List
from ..config.settings import Settings

logger = logging.getLogger(__name__)


def validate_configuration(settings: Settings) -> List[str]:
    """Validate configuration and return list of missing variables."""
    logger.info("Validating configuration...")
    
    missing_vars = settings.validate()
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
    else:
        logger.info("Configuration validation passed")
    
    return missing_vars


def print_missing_variables(missing_vars: List[str]) -> None:
    """Print missing variables in a user-friendly format."""
    if not missing_vars:
        return
    
    print("❌ Missing required environment variables:")
    for var in missing_vars:
        print(f"   - {var}")
    print("\nPlease set these variables in your .env file or environment.") 
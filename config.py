"""Configuration settings for ainews scraper."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'data'
LOGS_DIR = BASE_DIR / 'logs'

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Logging configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = LOGS_DIR / 'ainews.log'

# Scraper configuration
SCRAPER_TIMEOUT = int(os.getenv('SCRAPER_TIMEOUT', 10))
SCRAPER_RETRIES = int(os.getenv('SCRAPER_RETRIES', 3))
SCRAPER_DELAY = int(os.getenv('SCRAPER_DELAY', 1))  # Delay between requests in seconds

# News sources to scrape
NEWS_SOURCES = [
    {
        'name': 'BBC News',
        'url': 'https://www.bbc.com/news',
        'category': 'world',
    },
    # Add more news sources here
]

# Database configuration (optional)
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///ainews.db')

# API configuration (optional)
API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', 8000))

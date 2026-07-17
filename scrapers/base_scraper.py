"""Base scraper class with common functionality."""

import logging
import time
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class BaseScraper(ABC):
    """Base class for all web scrapers."""
    
    def __init__(self, name: str, timeout: int = 10, retry_attempts: int = 3):
        """Initialize the base scraper.
        
        Args:
            name: Name of the scraper
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts
        """
        self.name = name
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.session = self._create_session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def _create_session(self) -> requests.Session:
        """Create a session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.retry_attempts,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a webpage.
        
        Args:
            url: URL to fetch
            
        Returns:
            Page content or None if failed
        """
        try:
            response = self.session.get(
                url,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def parse_html(self, html: str) -> BeautifulSoup:
        """Parse HTML content.
        
        Args:
            html: HTML content to parse
            
        Returns:
            BeautifulSoup object
        """
        return BeautifulSoup(html, 'html.parser')
    
    @abstractmethod
    def scrape(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Scrape data from source.
        
        Must be implemented by subclasses.
        
        Returns:
            List of dictionaries containing scraped data
        """
        pass
    
    def run(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """Run the scraper with error handling."""
        try:
            logger.info(f"Starting scraper: {self.name}")
            results = self.scrape(*args, **kwargs)
            logger.info(f"Scraper {self.name} completed successfully. Found {len(results)} items.")
            return results
        except Exception as e:
            logger.error(f"Error in scraper {self.name}: {e}", exc_info=True)
            return []
    
    def close(self):
        """Close the session."""
        self.session.close()

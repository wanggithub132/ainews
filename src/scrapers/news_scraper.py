"""News scraper implementation."""

import logging
from typing import List, Dict, Any
from datetime import datetime
from urllib.parse import urljoin

from .base_scraper import BaseScraper

logger = logging.getLogger(__name__)

class NewsScraper(BaseScraper):
    """Scraper for news articles."""
    
    def __init__(self, base_url: str):
        """Initialize news scraper.
        
        Args:
            base_url: Base URL of the news source
        """
        super().__init__(name=f"NewsScraper({base_url})")
        self.base_url = base_url
    
    def scrape(self, category: str = 'latest') -> List[Dict[str, Any]]:
        """Scrape news articles.
        
        Args:
            category: News category to scrape
            
        Returns:
            List of news articles
        """
        articles = []
        
        # Construct URL
        url = f"{self.base_url}/{category}"
        
        # Fetch page
        html = self.fetch_page(url)
        if not html:
            return articles
        
        # Parse HTML
        soup = self.parse_html(html)
        
        # Extract articles (adjust selectors based on target website)
        article_elements = soup.find_all('article', limit=20)
        
        for element in article_elements:
            try:
                article = self._extract_article(element)
                if article:
                    articles.append(article)
            except Exception as e:
                logger.warning(f"Error extracting article: {e}")
                continue
        
        return articles
    
    def _extract_article(self, element) -> Dict[str, Any]:
        """Extract article data from HTML element.
        
        Args:
            element: BeautifulSoup element
            
        Returns:
            Article dictionary
        """
        try:
            # Extract title
            title_elem = element.find('h2', class_='title')
            title = title_elem.text.strip() if title_elem else 'No title'
            
            # Extract URL
            link_elem = element.find('a', href=True)
            url = urljoin(self.base_url, link_elem['href']) if link_elem else ''
            
            # Extract description
            desc_elem = element.find('p', class_='description')
            description = desc_elem.text.strip() if desc_elem else ''
            
            # Extract date
            date_elem = element.find('time')
            date_str = date_elem.get('datetime', '') if date_elem else ''
            
            # Extract image
            img_elem = element.find('img')
            image_url = img_elem.get('src', '') if img_elem else ''
            
            return {
                'title': title,
                'url': url,
                'description': description,
                'date': date_str,
                'image_url': image_url,
                'scraped_at': datetime.now().isoformat(),
                'source': self.base_url
            }
        except Exception as e:
            logger.error(f"Error extracting article data: {e}")
            return None

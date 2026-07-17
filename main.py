"""Main scraper runner."""

import logging
import time
from datetime import datetime
from typing import List, Dict, Any

from config import LOG_LEVEL, LOG_FILE, SCRAPER_DELAY, NEWS_SOURCES
from scrapers import NewsScraper

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_all_scrapers() -> Dict[str, List[Dict[str, Any]]]:
    """Run all configured scrapers.
    
    Returns:
        Dictionary with scraper names as keys and results as values
    """
    results = {}
    
    logger.info("Starting ainews scraper run...")
    start_time = datetime.now()
    
    for source in NEWS_SOURCES:
        try:
            scraper = NewsScraper(source['url'])
            articles = scraper.run(category=source.get('category', 'latest'))
            results[source['name']] = articles
            scraper.close()
            
            # Delay between requests to be respectful to servers
            time.sleep(SCRAPER_DELAY)
        except Exception as e:
            logger.error(f"Error running scraper for {source['name']}: {e}")
            results[source['name']] = []
    
    elapsed = (datetime.now() - start_time).total_seconds()
    logger.info(f"Scraper run completed in {elapsed:.2f} seconds")
    
    return results

def main():
    """Main entry point."""
    results = run_all_scrapers()
    
    # Print summary
    total_articles = sum(len(articles) for articles in results.values())
    print(f"\n{'='*50}")
    print(f"Scraping completed!")
    print(f"Total articles found: {total_articles}")
    print(f"{'='*50}\n")
    
    for source, articles in results.items():
        print(f"{source}: {len(articles)} articles")
        for article in articles[:3]:  # Print first 3 articles
            print(f"  - {article['title']}")
            print(f"    URL: {article['url']}")
        if len(articles) > 3:
            print(f"  ... and {len(articles) - 3} more")
        print()

if __name__ == '__main__':
    main()

#!/usr/bin/env python
"""Demo scraper to show the project functionality without WeChat dependency."""

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def demo_scrape():
    """Demo: Show what the scraper would fetch."""
    try:
        import feedparser
        
        logger.info("🚀 Starting tech news scraper demo...")
        logger.info("=" * 60)
        
        RSS_FEEDS = [
            {'name': 'HackerNews', 'url': 'https://news.ycombinator.com/rss'},
            {'name': 'TechCrunch', 'url': 'https://feeds.techcrunch.com/TechCrunch/'},
        ]
        
        all_articles = []
        
        for feed_config in RSS_FEEDS:
            try:
                logger.info(f"\n📡 Fetching from {feed_config['name']}...")
                feed = feedparser.parse(feed_config['url'])
                
                logger.info(f"   Found {len(feed.entries)} entries from {feed_config['name']}")
                
                for i, entry in enumerate(feed.entries[:3], 1):
                    try:
                        article = {
                            'title': entry.get('title', 'No title')[:128],
                            'url': entry.get('link', ''),
                            'summary': entry.get('summary', '')[:200],
                            'source': feed_config['name'],
                            'published_at': datetime.now().isoformat(),
                        }
                        all_articles.append(article)
                        logger.info(f"   [{i}] {article['title'][:60]}...")
                        if article['url']:
                            logger.info(f"       URL: {article['url'][:70]}...")
                    except Exception as e:
                        logger.warning(f"   ⚠ Error parsing entry: {e}")
                        continue
            except Exception as e:
                logger.error(f"❌ Error scraping {feed_config['name']}: {e}")
                continue
        
        logger.info("\n" + "=" * 60)
        logger.info(f"✅ Scraped {len(all_articles)} articles total")
        logger.info("=" * 60)
        
        # Display summary
        logger.info("\n📊 Summary by Source:")
        from collections import Counter
        source_counts = Counter(a['source'] for a in all_articles)
        for source, count in source_counts.items():
            logger.info(f"   {source}: {count} articles")
        
        # Show sample articles
        logger.info("\n📰 Sample Articles (for WeChat push):")
        for i, article in enumerate(all_articles[:5], 1):
            logger.info(f"\n   [{i}] {article['title']}")
            logger.info(f"       Source: {article['source']}")
            logger.info(f"       Summary: {article['summary'][:100]}...")
        
        if len(all_articles) > 5:
            logger.info(f"\n   ... and {len(all_articles) - 5} more articles")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return False

if __name__ == '__main__':
    import sys
    success = demo_scrape()
    sys.exit(0 if success else 1)

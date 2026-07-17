#!/usr/bin/env python
"""Main script to scrape tech news and send to WeChat."""

import os
import sys
import logging
from pathlib import Path
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

def scrape_tech_news():
    """Scrape tech news from RSS feeds."""
    import feedparser
    
    logger.info("🚀 Starting tech news scraper...")
    
    RSS_FEEDS = [
        {'name': 'HackerNews', 'url': 'https://news.ycombinator.com/rss'},
        {'name': 'TechCrunch', 'url': 'https://feeds.techcrunch.com/TechCrunch/'},
    ]
    
    all_articles = []
    
    for feed_config in RSS_FEEDS:
        try:
            logger.info(f"📡 Fetching from {feed_config['name']}...")
            feed = feedparser.parse(feed_config['url'])
            
            for entry in feed.entries[:3]:  # 每个源获取3条
                try:
                    article = {
                        'title': entry.get('title', 'No title')[:128],
                        'url': entry.get('link', ''),
                        'summary': entry.get('summary', '')[:200],
                        'source': feed_config['name'],
                        'published_at': datetime.now().isoformat(),
                    }
                    all_articles.append(article)
                    logger.info(f"  ✓ {article['title'][:50]}...")
                except Exception as e:
                    logger.warning(f"  ⚠ Error parsing entry: {e}")
                    continue
        except Exception as e:
            logger.error(f"❌ Error scraping {feed_config['name']}: {e}")
            continue
    
    logger.info(f"✅ Scraped {len(all_articles)} articles total")
    return all_articles

def send_to_weixin(articles, webhook_key):
    """Send articles to WeChat."""
    import requests
    
    if not webhook_key:
        logger.error("❌ WEIXIN_WEBHOOK_KEY not set")
        return False
    
    webhook_url = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"
    
    logger.info(f"📤 Preparing to send {len(articles)} articles to WeChat...")
    
    # Build article list
    items = []
    for article in articles[:5]:  # Max 5 articles
        item = {
            "title": article['title'],
            "description": article['summary'],
            "url": article['url'],
        }
        items.append(item)
    
    # Build payload
    payload = {
        "msgtype": "news",
        "news": {
            "articles": items
        }
    }
    
    try:
        logger.info(f"🔗 Sending to: {webhook_url[:60]}...")
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        logger.info(f"📡 WeChat Response: {result}")
        
        if result.get('errcode') == 0:
            logger.info(f"✅ Successfully sent {len(items)} articles to WeChat!")
            return True
        else:
            logger.error(f"❌ WeChat API error: {result.get('errmsg')}")
            return False
    except Exception as e:
        logger.error(f"❌ Error sending to WeChat: {e}")
        return False

def main():
    """Main entry point."""
    logger.info("=" * 60)
    logger.info("🤖 Tech News Scraper with WeChat Integration")
    logger.info("=" * 60)
    
    try:
        # Get webhook key
        webhook_key = os.getenv('WEIXIN_WEBHOOK_KEY')
        if not webhook_key:
            logger.error("❌ WEIXIN_WEBHOOK_KEY environment variable not set")
            return False
        
        logger.info(f"✓ Webhook key loaded: {webhook_key[:20]}...")
        
        # Scrape news
        articles = scrape_tech_news()
        if not articles:
            logger.warning("⚠️  No articles scraped")
            return False
        
        # Send to WeChat
        success = send_to_weixin(articles, webhook_key)
        
        logger.info("=" * 60)
        if success:
            logger.info("✅ All tasks completed successfully!")
        else:
            logger.error("❌ Some tasks failed")
        logger.info("=" * 60)
        
        return success
    
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

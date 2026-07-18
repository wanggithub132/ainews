#!/usr/bin/env python
"""Quick start guide and testing utility."""

import os
import sys

def print_section(title):
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_setup():
    """Check if the setup is complete."""
    print_section("📋 Setup Verification")
    
    checks = []
    
    # Check if webhook key is set
    webhook_key = os.getenv('WEIXIN_WEBHOOK_KEY')
    if webhook_key:
        print(f"✅ WEIXIN_WEBHOOK_KEY is set: {webhook_key[:20]}...")
        checks.append(True)
    else:
        print("❌ WEIXIN_WEBHOOK_KEY is not set")
        print("\n   To set it locally:")
        print("   Linux/Mac: export WEIXIN_WEBHOOK_KEY='your_key_here'")
        print("   Windows:   set WEIXIN_WEBHOOK_KEY=your_key_here")
        checks.append(False)
    
    # Check if scraper.py exists
    if os.path.exists('scraper.py'):
        print("✅ scraper.py exists")
        checks.append(True)
    else:
        print("❌ scraper.py not found")
        checks.append(False)
    
    # Check if requirements.txt exists
    if os.path.exists('requirements.txt'):
        print("✅ requirements.txt exists")
        checks.append(True)
    else:
        print("❌ requirements.txt not found")
        checks.append(False)
    
    return all(checks)

def print_next_steps():
    """Print the next steps for configuration."""
    print_section("🚀 Next Steps")
    
    print("""
1️⃣  CONFIGURE GITHUB SECRET
   - Go to: https://github.com/wanggithub132/ainews/settings/secrets/actions
   - Click 'New repository secret'
   - Name: WEIXIN_WEBHOOK_KEY
   - Value: your_webhook_key_here
   - Click 'Add secret'

2️⃣  TRIGGER THE WORKFLOW
   - Go to: https://github.com/wanggithub132/ainews/actions
   - Select 'Daily Tech News Scraper' workflow
   - Click 'Run workflow' button
   - Wait 2-3 minutes for execution

3️⃣  CHECK RESULTS
   - Open your WeChat Enterprise group
   - Look for the news articles pushed by the bot
   - Check the Actions logs for any errors

4️⃣  MONITOR AUTOMATIC RUNS
   - The workflow runs daily at 09:00 UTC (17:00 Beijing time)
   - You can view all runs in the Actions tab
    """)

def print_troubleshooting():
    """Print troubleshooting guide."""
    print_section("🔧 Troubleshooting")
    
    print("""
❌ WeChat didn't receive the news?
   - Verify WEIXIN_WEBHOOK_KEY in GitHub Secrets
   - Check that the key is correct (no URL prefix)
   - Ensure your WeChat group allows robot messages
   - Review the Actions execution logs

❌ Actions workflow not found?
   - Go to Actions tab and enable workflows
   - Check if .github/workflows/daily-scraper.yml exists

❌ Python dependencies missing?
   - Run: pip install -r requirements.txt
   - Or install manually: pip install requests feedparser

❌ Local test failed?
   - Set environment variable: export WEIXIN_WEBHOOK_KEY='your_key'
   - Run: python scraper.py
   - Check the console output for errors
    """)

def main():
    """Main entry point."""
    print_section("🤖 AiNews - Tech News Scraper Setup")
    
    print("""
Welcome to AiNews! This tool automatically scrapes the latest
tech news and pushes them to your WeChat Enterprise group.

Configuration Status:
    """)
    
    if check_setup():
        print("\n✅ Basic setup looks good!")
    else:
        print("\n⚠️  Some setup items need attention")
    
    print_next_steps()
    print_troubleshooting()
    
    print_section("📚 Additional Resources")
    print("""
Documentation:
  - SETUP.md - Complete setup guide
  - README.md - Project overview
  - scraper.py - Main scraper script

WeChat Configuration:
  - Open WeChat Enterprise
  - Go to Group Chat → Group Robot
  - Create a new robot
  - Copy the Webhook URL and extract the 'key' value

Support:
  - Check GitHub Issues for common problems
  - Review Actions logs for execution details
    """)
    
    print(f"\n{'='*60}")
    print("Ready to go! 🎉")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()

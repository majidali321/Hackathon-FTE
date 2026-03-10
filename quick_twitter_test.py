"""
Quick Test - Post to Twitter/X
Simple test to post a single tweet
"""

import sys
import io
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent / "integrations"))

from twitter_integration import post_to_twitter

def quick_twitter_test():
    """Quick test for Twitter posting"""

    content = f"""AI Employee Test - {datetime.now().strftime('%H:%M:%S')}

This tweet was auto-posted by AGents!

#AI #Automation #FTE2026"""

    print("=" * 60)
    print("QUICK TWITTER TEST")
    print("=" * 60)
    print(f"\nContent ({len(content)} chars):\n{content}\n")
    print("Starting Twitter post...")

    success = post_to_twitter(content, headless=False)

    if success:
        print("\n✅ Tweet posted successfully!")
    else:
        print("\n❌ Failed to post tweet")

    return success

if __name__ == "__main__":
    quick_twitter_test()

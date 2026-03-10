"""
Test All Social Media Integrations
Tests Twitter/X, Instagram, and Facebook posting
"""

import sys
import io
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Add integrations to path
sys.path.insert(0, str(Path(__file__).parent / "integrations"))

from twitter_integration import post_to_twitter
from instagram_integration import post_to_instagram
from facebook_integration import post_to_facebook


def test_all_platforms():
    """Test posting to all social media platforms"""

    print("=" * 70)
    print("SOCIAL MEDIA INTEGRATION TEST - ALL PLATFORMS")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    # Common content for all platforms
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Twitter content (280 char limit)
    twitter_content = f"""🤖 AI Employee Automation Test

Auto-posted by my Personal AI Employee!

#AI #Automation #Hackathon #FTE2026

{timestamp}"""

    # Instagram content
    instagram_content = f"""🤖 Testing AI Employee Automation System

This post was automatically generated and published by my Personal AI Employee as part of the Gold Tier implementation!

#AI #Automation #Hackathon #FTE2026 #InstagramAutomation #AIEmployee

Posted: {timestamp}"""

    # Facebook content
    facebook_content = f"""🤖 Testing AI Employee Automation System

This post was automatically generated and published by my Personal AI Employee as part of the Gold Tier implementation!

The system can now post to:
✅ Facebook
✅ Twitter/X
✅ Instagram
✅ LinkedIn

#AI #Automation #Hackathon #FTE2026

Posted: {timestamp}"""

    results = {}

    # Test Twitter/X
    print("\n" + "=" * 70)
    print("1. TESTING TWITTER/X")
    print("=" * 70)
    print(f"Content ({len(twitter_content)} chars):\n{twitter_content}\n")
    try:
        results['twitter'] = post_to_twitter(twitter_content, headless=False)
        if results['twitter']:
            print("✅ Twitter/X: SUCCESS")
        else:
            print("❌ Twitter/X: FAILED")
    except Exception as e:
        print(f"❌ Twitter/X: ERROR - {e}")
        results['twitter'] = False

    # Test Instagram
    print("\n" + "=" * 70)
    print("2. TESTING INSTAGRAM")
    print("=" * 70)
    print(f"Content:\n{instagram_content}\n")
    print("⚠️  Note: Instagram requires an image to post.")
    print("    This test will attempt text-only posting (may fail).\n")
    try:
        results['instagram'] = post_to_instagram(instagram_content, headless=False)
        if results['instagram']:
            print("✅ Instagram: SUCCESS")
        else:
            print("❌ Instagram: FAILED (may need image)")
    except Exception as e:
        print(f"❌ Instagram: ERROR - {e}")
        results['instagram'] = False

    # Test Facebook
    print("\n" + "=" * 70)
    print("3. TESTING FACEBOOK")
    print("=" * 70)
    print(f"Content:\n{facebook_content}\n")
    try:
        results['facebook'] = post_to_facebook(facebook_content, headless=False)
        if results['facebook']:
            print("✅ Facebook: SUCCESS")
        else:
            print("❌ Facebook: FAILED")
    except Exception as e:
        print(f"❌ Facebook: ERROR - {e}")
        results['facebook'] = False

    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    success_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    for platform, success in results.items():
        status = "✅ SUCCESS" if success else "❌ FAILED"
        print(f"{platform.upper()}: {status}")

    print(f"\nTotal: {success_count}/{total_count} platforms successful")
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    return results


if __name__ == "__main__":
    test_all_platforms()

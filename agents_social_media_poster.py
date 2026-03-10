"""
AGents Social Media Poster
Main interface for posting to all social media platforms
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

# Add integrations to path
sys.path.insert(0, str(Path(__file__).parent / "integrations"))

from twitter_integration import post_to_twitter
from instagram_integration import post_to_instagram
from facebook_integration import post_to_facebook


class AGentsSocialMediaPoster:
    """Main class for posting to all social media platforms"""

    def __init__(self):
        self.platforms = {
            'twitter': post_to_twitter,
            'instagram': post_to_instagram,
            'facebook': post_to_facebook
        }

    def post_to_platform(self, platform, content, image_path=None, headless=False):
        """Post to a specific platform"""
        if platform not in self.platforms:
            print(f"❌ Unknown platform: {platform}")
            return False

        print(f"\n📤 Posting to {platform.upper()}...")

        try:
            if platform == 'instagram' and image_path:
                success = self.platforms[platform](content, image_path=image_path, headless=headless)
            else:
                success = self.platforms[platform](content, headless=headless)

            if success:
                print(f"✅ Successfully posted to {platform.upper()}")
            else:
                print(f"❌ Failed to post to {platform.upper()}")

            return success
        except Exception as e:
            print(f"❌ Error posting to {platform.upper()}: {e}")
            return False

    def post_to_all(self, content, image_path=None, headless=False):
        """Post to all platforms"""
        print("=" * 70)
        print("POSTING TO ALL SOCIAL MEDIA PLATFORMS")
        print("=" * 70)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

        results = {}
        for platform in self.platforms.keys():
            results[platform] = self.post_to_platform(platform, content, image_path, headless)

        # Summary
        print("\n" + "=" * 70)
        print("POSTING SUMMARY")
        print("=" * 70)
        success_count = sum(1 for v in results.values() if v)
        total_count = len(results)

        for platform, success in results.items():
            status = "✅ SUCCESS" if success else "❌ FAILED"
            print(f"{platform.upper()}: {status}")

        print(f"\nTotal: {success_count}/{total_count} platforms successful")
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        return results


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='AGents Social Media Poster')
    parser.add_argument('--platform', choices=['twitter', 'instagram', 'facebook', 'all'],
                       default='all', help='Platform to post to')
    parser.add_argument('--content', type=str, required=True, help='Content to post')
    parser.add_argument('--image', type=str, help='Path to image (for Instagram)')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')

    args = parser.parse_args()

    poster = AGentsSocialMediaPoster()

    if args.platform == 'all':
        poster.post_to_all(args.content, args.image, args.headless)
    else:
        poster.post_to_platform(args.platform, args.content, args.image, args.headless)


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("AGents Social Media Poster")
    print("=" * 70)
    print("\nUsage examples:")
    print("\n1. Post to all platforms:")
    print('   python agents_social_media_poster.py --content "Your message here"')
    print("\n2. Post to specific platform:")
    print('   python agents_social_media_poster.py --platform twitter --content "Your tweet"')
    print("\n3. Post to Instagram with image:")
    print('   python agents_social_media_poster.py --platform instagram --content "Caption" --image path/to/image.jpg')
    print("\n4. Run in headless mode:")
    print('   python agents_social_media_poster.py --content "Message" --headless')
    print("\n" + "=" * 70)

    # If no arguments provided, show usage
    if len(sys.argv) == 1:
        print("\nTo post, use the command line arguments shown above.")
        print("Or import this module in your Python code:\n")
        print("from agents_social_media_poster import AGentsSocialMediaPoster")
        print("poster = AGentsSocialMediaPoster()")
        print('poster.post_to_all("Your content here")')
    else:
        main()

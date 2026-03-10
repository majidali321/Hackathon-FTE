"""
Social Media Workflow Manager
Monitors Approved folder and automatically posts to social media platforms
Part of Gold Tier requirements for Hackathon FTE
"""

import time
import logging
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import social media skills
try:
    from social_media_skills import publish_approved_social_posts
    SKILLS_AVAILABLE = True
except ImportError:
    logger.error("social_media_skills module not found")
    SKILLS_AVAILABLE = False


class SocialMediaApprovalHandler(FileSystemEventHandler):
    """Handles file events in the Approved folder"""

    def __init__(self):
        self.last_check = datetime.now()
        self.cooldown = 5  # seconds between checks

    def on_created(self, event):
        """Handle new files in Approved folder"""
        if event.is_directory:
            return

        filepath = Path(event.src_path)

        # Only process social media post files
        if any(platform in filepath.name for platform in ["FACEBOOK_POST", "TWITTER_POST", "INSTAGRAM_POST"]):
            logger.info(f"New approved post detected: {filepath.name}")

            # Wait a moment for file to be fully written
            time.sleep(2)

            # Process the post
            self.process_approved_post(filepath)

    def on_moved(self, event):
        """Handle files moved to Approved folder"""
        if event.is_directory:
            return

        dest_path = Path(event.dest_path)

        # Check if moved TO Approved folder
        if "Approved" in str(dest_path.parent):
            if any(platform in dest_path.name for platform in ["FACEBOOK_POST", "TWITTER_POST", "INSTAGRAM_POST"]):
                logger.info(f"Post moved to Approved: {dest_path.name}")

                # Wait a moment
                time.sleep(2)

                # Process the post
                self.process_approved_post(dest_path)

    def process_approved_post(self, filepath):
        """Process an approved social media post"""
        try:
            # Cooldown check
            now = datetime.now()
            if (now - self.last_check).total_seconds() < self.cooldown:
                logger.info("Cooldown active, skipping...")
                return

            self.last_check = now

            logger.info(f"Processing approved post: {filepath.name}")

            if SKILLS_AVAILABLE:
                results = publish_approved_social_posts()

                # Log results
                if results["facebook"]:
                    logger.info(f"Posted to Facebook: {results['facebook']}")
                if results["twitter"]:
                    logger.info(f"Posted to Twitter: {results['twitter']}")
                if results["instagram"]:
                    logger.info(f"Posted to Instagram: {results['instagram']}")
                if results["errors"]:
                    logger.error(f"Errors: {results['errors']}")
            else:
                logger.error("Social media skills not available")

        except Exception as e:
            logger.error(f"Error processing approved post: {e}")


def start_social_media_workflow():
    """Start the social media workflow monitor"""
    print("=" * 60)
    print("Social Media Workflow Manager")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    print("Monitoring Approved/ folder for social media posts...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()

    # Ensure Approved folder exists
    approved_dir = Path("Approved")
    approved_dir.mkdir(exist_ok=True)

    # Setup file system observer
    event_handler = SocialMediaApprovalHandler()
    observer = Observer()
    observer.schedule(event_handler, str(approved_dir), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\nStopping social media workflow...")
        observer.stop()
        observer.join()
        print("Stopped.")


def manual_publish():
    """Manually trigger publishing of approved posts"""
    print("=" * 60)
    print("Manual Social Media Publishing")
    print("=" * 60)
    print()

    if not SKILLS_AVAILABLE:
        print("❌ Social media skills not available")
        return

    print("Checking Approved/ folder for posts...")
    results = publish_approved_social_posts()

    print()
    print("Results:")
    print("-" * 60)

    if results["facebook"]:
        print(f"✅ Facebook posts published: {len(results['facebook'])}")
        for post in results["facebook"]:
            print(f"   - {post}")

    if results["twitter"]:
        print(f"✅ Twitter posts published: {len(results['twitter'])}")
        for post in results["twitter"]:
            print(f"   - {post}")

    if results["instagram"]:
        print(f"✅ Instagram posts published: {len(results['instagram'])}")
        for post in results["instagram"]:
            print(f"   - {post}")

    if results["errors"]:
        print(f"❌ Errors: {len(results['errors'])}")
        for error in results["errors"]:
            print(f"   - {error}")

    if not any([results["facebook"], results["twitter"], results["instagram"], results["errors"]]):
        print("ℹ️  No approved posts found")

    print("=" * 60)


def interactive_menu():
    """Interactive menu for social media workflow"""
    while True:
        print("\n" + "=" * 60)
        print("Social Media Workflow - Interactive Menu")
        print("=" * 60)
        print()
        print("1. Start Automated Workflow (Monitor Approved folder)")
        print("2. Manually Publish Approved Posts")
        print("3. Create Facebook Post Draft")
        print("4. Create Twitter Post Draft")
        print("5. Create Instagram Post Draft")
        print("6. Exit")
        print()

        choice = input("Select option (1-6): ").strip()

        if choice == "1":
            start_social_media_workflow()

        elif choice == "2":
            manual_publish()

        elif choice == "3":
            if SKILLS_AVAILABLE:
                from social_media_skills import create_facebook_post_draft
                topic = input("Enter topic: ").strip()
                tone = input("Enter tone (professional/casual/inspirational): ").strip() or "professional"
                result = create_facebook_post_draft(topic, tone)
                print(f"\n{result['message']}")
                print(f"File: {result.get('file', 'N/A')}")
            else:
                print("❌ Social media skills not available")

        elif choice == "4":
            if SKILLS_AVAILABLE:
                from social_media_skills import create_twitter_post_draft
                topic = input("Enter topic: ").strip()
                tone = input("Enter tone (professional/casual/inspirational): ").strip() or "professional"
                result = create_twitter_post_draft(topic, tone)
                print(f"\n{result['message']}")
                print(f"File: {result.get('file', 'N/A')}")
                print(f"Characters: {result.get('char_count', 'N/A')}/280")
            else:
                print("❌ Social media skills not available")

        elif choice == "5":
            if SKILLS_AVAILABLE:
                from social_media_skills import create_instagram_post_draft
                topic = input("Enter topic: ").strip()
                tone = input("Enter tone (professional/casual/inspirational): ").strip() or "inspirational"
                result = create_instagram_post_draft(topic, tone)
                print(f"\n{result['message']}")
                print(f"File: {result.get('file', 'N/A')}")
            else:
                print("❌ Social media skills not available")

        elif choice == "6":
            print("\nExiting...")
            break

        else:
            print("\n❌ Invalid option. Please select 1-6.")


if __name__ == "__main__":
    interactive_menu()

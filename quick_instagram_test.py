"""
Quick Test - Post to Instagram
Simple test to post to Instagram (requires image)
"""

import sys
import io
from datetime import datetime
from pathlib import Path

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).parent / "integrations"))

from instagram_integration import post_to_instagram

def quick_instagram_test(image_path=None):
    """Quick test for Instagram posting"""

    content = f"""AI Employee Test

Auto-posted by AGents at {datetime.now().strftime('%H:%M:%S')}

#AI #Automation #FTE2026"""

    print("=" * 60)
    print("QUICK INSTAGRAM TEST")
    print("=" * 60)
    print(f"\nContent:\n{content}\n")

    if not image_path:
        print("⚠️  WARNING: No image provided!")
        print("Instagram requires an image to post.")
        print("Usage: python quick_instagram_test.py path/to/image.jpg")
        return False

    print(f"Image: {image_path}")
    print("\nStarting Instagram post...")

    success = post_to_instagram(content, image_path=image_path, headless=False)

    if success:
        print("\n✅ Instagram post published successfully!")
    else:
        print("\n❌ Failed to publish Instagram post")

    return success

if __name__ == "__main__":
    import sys
    image = sys.argv[1] if len(sys.argv) > 1 else None
    quick_instagram_test(image)

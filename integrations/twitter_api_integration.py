"""
Twitter API Integration using Tweepy
More reliable than Selenium for automated posting
"""

import sys
import io
import logging
from pathlib import Path

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

try:
    import tweepy
except ImportError:
    print("⚠️  tweepy not installed. Installing now...")
    import subprocess
    subprocess.check_call(['pip', 'install', 'tweepy'])
    import tweepy

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TwitterAPIClient:
    """Twitter API client using tweepy"""

    def __init__(self, credentials_path="credentials.json"):
        """Initialize Twitter API client"""
        self.credentials_path = Path(credentials_path)
        self.consumer_key = None
        self.consumer_secret = None
        self.access_token = None
        self.access_token_secret = None
        self.bearer_token = None
        self.client = None
        self.api = None
        self.load_credentials()
        self.authenticate()

    def load_credentials(self):
        """Load Twitter API credentials from credentials.json"""
        try:
            if self.credentials_path.exists():
                with open(self.credentials_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse credentials
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('twitter_consumer_key'):
                        self.consumer_key = line.split('=', 1)[1].strip()
                    elif line.startswith('twitter_consumer_secret'):
                        self.consumer_secret = line.split('=', 1)[1].strip()
                    elif line.startswith('twitter_access_token ='):
                        self.access_token = line.split('=', 1)[1].strip()
                    elif line.startswith('twitter_access_token_secret'):
                        self.access_token_secret = line.split('=', 1)[1].strip()
                    elif line.startswith('twitter_bearer_token'):
                        self.bearer_token = line.split('=', 1)[1].strip()

                if all([self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret]):
                    logger.info("Loaded Twitter API credentials successfully")
                else:
                    logger.warning("Some Twitter API credentials are missing")
            else:
                logger.error(f"Credentials file not found: {self.credentials_path}")
        except Exception as e:
            logger.error(f"Error loading credentials: {e}")

    def authenticate(self):
        """Authenticate with Twitter API"""
        try:
            if not all([self.consumer_key, self.consumer_secret, self.access_token, self.access_token_secret]):
                logger.error("Missing required API credentials")
                return False

            # OAuth 1.0a authentication
            auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
            auth.set_access_token(self.access_token, self.access_token_secret)

            # Create API v1.1 client
            self.api = tweepy.API(auth)

            # Create API v2 client
            self.client = tweepy.Client(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                access_token=self.access_token,
                access_token_secret=self.access_token_secret
            )

            # Verify credentials
            user = self.api.verify_credentials()
            logger.info(f"Authenticated as: @{user.screen_name}")
            return True

        except Exception as e:
            logger.error(f"Authentication failed: {e}")
            return False

    def post_tweet(self, text):
        """Post a tweet using API v2"""
        try:
            if not self.client:
                logger.error("Not authenticated")
                return False

            # Check character limit
            if len(text) > 280:
                logger.warning(f"Tweet exceeds 280 characters ({len(text)}). Truncating...")
                text = text[:277] + "..."

            # Post tweet
            response = self.client.create_tweet(text=text)

            if response.data:
                tweet_id = response.data['id']
                logger.info(f"Tweet posted successfully! ID: {tweet_id}")
                return True
            else:
                logger.error("Failed to post tweet")
                return False

        except Exception as e:
            logger.error(f"Error posting tweet: {e}")
            return False


def post_to_twitter_api(content):
    """
    Convenience function to post to Twitter using API

    Args:
        content (str): The tweet content (max 280 characters)

    Returns:
        bool: True if successful, False otherwise
    """
    client = TwitterAPIClient()
    return client.post_tweet(content)


def test_twitter_api():
    """Test Twitter API posting"""
    from datetime import datetime

    print("=" * 60)
    print("Twitter API Integration Test")
    print("=" * 60)

    test_content = f"""🤖 Testing Twitter API Integration

Auto-posted by AGents using Twitter API!

#AI #Automation #FTE2026

{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    print(f"\nTest Tweet Content:\n{test_content}\n")
    print(f"Character count: {len(test_content)}/280")
    print("\nPosting tweet via Twitter API...")

    success = post_to_twitter_api(test_content)

    if success:
        print("\n✅ Tweet posted successfully via API!")
    else:
        print("\n❌ Failed to post tweet via API")

    return success


if __name__ == "__main__":
    test_twitter_api()

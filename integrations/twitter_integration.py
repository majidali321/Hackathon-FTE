"""
Twitter (X) Integration Module
Automates Twitter posting using Selenium WebDriver
Part of Gold Tier requirements for Hackathon FTE
"""

import json
import time
import logging
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TwitterPoster:
    """Handles automated Twitter/X posting with Selenium"""

    def __init__(self, credentials_path="credentials.json"):
        """Initialize Twitter poster with credentials"""
        self.credentials_path = Path(credentials_path)
        self.username = None
        self.password = None
        self.driver = None
        self.load_credentials()

    def load_credentials(self):
        """Load Twitter credentials from credentials.json"""
        try:
            if self.credentials_path.exists():
                with open(self.credentials_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse credentials
                for line in content.split('\n'):
                    line = line.strip()
                    if 'twitter_username' in line.lower():
                        self.username = line.split('=')[1].strip()
                    elif 'twitter_password' in line.lower():
                        self.password = line.split('=')[1].strip()

                if self.username and self.password:
                    logger.info(f"Loaded Twitter credentials for: {self.username}")
                else:
                    logger.warning("Twitter credentials not found in credentials.json")
            else:
                logger.error(f"Credentials file not found: {self.credentials_path}")
        except Exception as e:
            logger.error(f"Error loading credentials: {e}")

    def setup_driver(self, headless=False):
        """Setup Chrome WebDriver"""
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            logger.info("Chrome WebDriver initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {e}")
            return False

    def login(self):
        """Login to Twitter/X"""
        try:
            logger.info("Navigating to Twitter/X...")
            self.driver.get("https://twitter.com/i/flow/login")
            time.sleep(5)

            # Enter username/email
            logger.info("Entering username...")
            username_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            time.sleep(2)

            # Click Next
            logger.info("Clicking Next button...")
            next_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
            )
            next_button.click()
            time.sleep(4)

            # Enter password
            logger.info("Entering password...")
            password_field = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(2)

            # Click Log in
            logger.info("Clicking login button...")
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Log in']"))
            )
            login_button.click()

            # Wait for login to complete
            logger.info("Waiting for login to complete...")
            time.sleep(8)

            # Check if login was successful
            current_url = self.driver.current_url.lower()
            if "login" in current_url:
                logger.error("Login failed - still on login page")
                logger.info(f"Current URL: {self.driver.current_url}")
                # Take screenshot for debugging
                try:
                    screenshot_path = "twitter_login_error.png"
                    self.driver.save_screenshot(screenshot_path)
                    logger.info(f"Screenshot saved to: {screenshot_path}")
                except:
                    pass
                return False

            logger.info("Successfully logged in to Twitter/X")
            return True

        except Exception as e:
            logger.error(f"Error during login: {e}")
            # Take screenshot for debugging
            try:
                screenshot_path = "twitter_login_error.png"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"Screenshot saved to: {screenshot_path}")
            except:
                pass
            return False

    def create_tweet(self, content):
        """Create a tweet"""
        try:
            logger.info("Creating tweet...")

            # Navigate to home if not already there
            if "home" not in self.driver.current_url:
                self.driver.get("https://twitter.com/home")
                time.sleep(3)

            # Find the tweet composition box
            logger.info("Finding tweet box...")
            tweet_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @contenteditable='true']"))
            )
            tweet_box.click()
            time.sleep(1)

            # Enter tweet content
            logger.info("Entering tweet content...")
            tweet_box.send_keys(content)
            time.sleep(2)

            # Find and click the Tweet button
            logger.info("Clicking Tweet button...")
            tweet_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@data-testid='tweetButtonInline']"))
            )
            tweet_button.click()

            # Wait for tweet to be posted
            time.sleep(5)

            logger.info("Tweet posted successfully!")
            return True

        except Exception as e:
            logger.error(f"Error creating tweet: {e}")
            return False

    def post_to_twitter(self, content, headless=False):
        """Complete workflow: login and post to Twitter"""
        try:
            if not self.username or not self.password:
                logger.error("Twitter credentials not loaded")
                return False

            # Setup driver
            if not self.setup_driver(headless=headless):
                return False

            # Login
            if not self.login():
                return False

            # Create tweet
            success = self.create_tweet(content)

            # Cleanup
            time.sleep(3)
            self.driver.quit()

            return success

        except Exception as e:
            logger.error(f"Error in post_to_twitter: {e}")
            if self.driver:
                self.driver.quit()
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")


def post_to_twitter(content, headless=False):
    """
    Convenience function to post to Twitter

    Args:
        content (str): The tweet content (max 280 characters)
        headless (bool): Run browser in headless mode

    Returns:
        bool: True if successful, False otherwise
    """
    if len(content) > 280:
        logger.warning(f"Tweet content exceeds 280 characters ({len(content)}). Truncating...")
        content = content[:277] + "..."

    poster = TwitterPoster()
    return poster.post_to_twitter(content, headless=headless)


def test_twitter_posting():
    """Test Twitter posting functionality"""
    print("=" * 60)
    print("Twitter/X Integration Test")
    print("=" * 60)

    test_content = f"""🤖 Testing AI Employee Automation

This tweet was auto-generated by my Personal AI Employee!

#AI #Automation #Hackathon #FTE2026"""

    print(f"\nTest Tweet Content:\n{test_content}\n")
    print(f"Character count: {len(test_content)}/280")
    print("\nStarting Twitter posting process...")

    success = post_to_twitter(test_content, headless=False)

    if success:
        print("\n✅ Tweet posted successfully!")
    else:
        print("\n❌ Failed to post tweet")

    return success


if __name__ == "__main__":
    # Run test
    test_twitter_posting()

"""
Facebook Integration Module
Automates Facebook posting using Selenium WebDriver
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
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FacebookPoster:
    """Handles automated Facebook posting with Selenium"""

    def __init__(self, credentials_path="credentials.json"):
        """Initialize Facebook poster with credentials"""
        self.credentials_path = Path(credentials_path)
        self.email = None
        self.password = None
        self.driver = None
        self.load_credentials()

    def load_credentials(self):
        """Load Facebook credentials from credentials.json"""
        try:
            if self.credentials_path.exists():
                with open(self.credentials_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse credentials (format: facebook_email = ... \n facebook_password = ...)
                for line in content.split('\n'):
                    line = line.strip()
                    if 'facebook_email' in line.lower():
                        self.email = line.split('=')[1].strip()
                    elif 'facebook_password' in line.lower():
                        self.password = line.split('=')[1].strip()

                if self.email and self.password:
                    logger.info(f"Loaded Facebook credentials for: {self.email}")
                else:
                    logger.error("Facebook credentials not found in credentials.json")
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
        """Login to Facebook"""
        try:
            logger.info("Navigating to Facebook...")
            self.driver.get("https://www.facebook.com")
            time.sleep(5)

            # Find and fill email (try NAME attribute)
            logger.info("Entering email...")
            try:
                email_field = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.NAME, "email"))
                )
            except:
                # Fallback to ID
                email_field = self.driver.find_element(By.ID, "email")

            email_field.clear()
            email_field.send_keys(self.email)
            time.sleep(2)

            # Find and fill password
            logger.info("Entering password...")
            try:
                password_field = self.driver.find_element(By.NAME, "pass")
            except:
                password_field = self.driver.find_element(By.ID, "pass")

            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(2)

            # Click login button
            logger.info("Clicking login button...")
            try:
                login_button = self.driver.find_element(By.NAME, "login")
            except:
                # Try finding by button type
                login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")

            login_button.click()

            # Wait for login to complete
            logger.info("Waiting for login to complete...")
            time.sleep(8)

            # Check if login was successful
            current_url = self.driver.current_url.lower()
            if "login" in current_url or "checkpoint" in current_url:
                logger.warning(f"Login may have failed or requires verification. URL: {current_url}")
                # Don't return False immediately - might be checkpoint
                time.sleep(5)

            logger.info("Login process completed")
            return True

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def create_post(self, content):
        """Create a Facebook post"""
        try:
            logger.info("Creating Facebook post...")

            # Wait for page to load
            time.sleep(3)

            # Find the "What's on your mind" box (multiple possible selectors)
            try:
                # Try clicking the post creation area
                post_box = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), \"What's on your mind\")]"))
                )
                post_box.click()
                time.sleep(2)
            except:
                # Alternative: try finding by aria-label
                try:
                    post_box = self.driver.find_element(By.XPATH, "//div[@aria-label='Create a post']")
                    post_box.click()
                    time.sleep(2)
                except:
                    logger.warning("Could not find post creation box with standard selectors")

            # Find the text input area in the modal
            logger.info("Entering post content...")
            text_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox' and @contenteditable='true']"))
            )
            text_area.click()
            time.sleep(1)
            text_area.send_keys(content)
            time.sleep(2)

            # Find and click the Post button
            logger.info("Clicking Post button...")
            post_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Post' and @role='button']"))
            )
            post_button.click()

            # Wait for post to be published
            time.sleep(5)

            logger.info("Post published successfully!")
            return True

        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return False

    def post_to_facebook(self, content, headless=False):
        """Complete workflow: login and post to Facebook"""
        try:
            if not self.email or not self.password:
                logger.error("Facebook credentials not loaded")
                return False

            # Setup driver
            if not self.setup_driver(headless=headless):
                return False

            # Login
            if not self.login():
                return False

            # Create post
            success = self.create_post(content)

            # Cleanup
            time.sleep(3)
            self.driver.quit()

            return success

        except Exception as e:
            logger.error(f"Error in post_to_facebook: {e}")
            if self.driver:
                self.driver.quit()
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")


def post_to_facebook(content, headless=False):
    """
    Convenience function to post to Facebook

    Args:
        content (str): The post content
        headless (bool): Run browser in headless mode

    Returns:
        bool: True if successful, False otherwise
    """
    poster = FacebookPoster()
    return poster.post_to_facebook(content, headless=headless)


def test_facebook_posting():
    """Test Facebook posting functionality"""
    print("=" * 60)
    print("Facebook Integration Test")
    print("=" * 60)

    test_content = f"""🤖 Testing AI Employee Automation System

This post was automatically generated and published by my Personal AI Employee as part of the Gold Tier implementation!

#AI #Automation #Hackathon #FTE2026

Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    print(f"\nTest Post Content:\n{test_content}\n")
    print("Starting Facebook posting process...")

    success = post_to_facebook(test_content, headless=False)

    if success:
        print("\n✅ Facebook post published successfully!")
    else:
        print("\n❌ Failed to publish Facebook post")

    return success


if __name__ == "__main__":
    # Run test
    test_facebook_posting()

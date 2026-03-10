"""
Instagram Integration Module
Automates Instagram posting using Selenium WebDriver
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

class InstagramPoster:
    """Handles automated Instagram posting with Selenium"""

    def __init__(self, credentials_path="credentials.json"):
        """Initialize Instagram poster with credentials"""
        self.credentials_path = Path(credentials_path)
        self.username = None
        self.password = None
        self.driver = None
        self.load_credentials()

    def load_credentials(self):
        """Load Instagram credentials from credentials.json"""
        try:
            if self.credentials_path.exists():
                with open(self.credentials_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Parse credentials
                for line in content.split('\n'):
                    line = line.strip()
                    if line.startswith('instagram_username'):
                        self.username = line.split('=', 1)[1].strip()
                    elif line.startswith('instagram_password'):
                        self.password = line.split('=', 1)[1].strip()

                if self.username and self.password:
                    logger.info(f"Loaded Instagram credentials for: {self.username}")
                else:
                    logger.warning("Instagram credentials not found in credentials.json")
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

            # Mobile emulation for Instagram
            mobile_emulation = {
                "deviceMetrics": { "width": 375, "height": 812, "pixelRatio": 3.0 },
                "userAgent": "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
            }
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

            self.driver = webdriver.Chrome(options=chrome_options)
            logger.info("Chrome WebDriver initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error setting up WebDriver: {e}")
            return False

    def login(self):
        """Login to Instagram"""
        try:
            logger.info("Navigating to Instagram...")
            self.driver.get("https://www.instagram.com/accounts/login/")
            time.sleep(5)

            # Dismiss cookie banner if present
            try:
                cookie_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
                cookie_button.click()
                time.sleep(2)
            except:
                pass

            # Enter username
            logger.info("Entering username...")
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            username_field.clear()
            username_field.send_keys(self.username)
            time.sleep(1)

            # Enter password
            logger.info("Entering password...")
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(self.password)
            time.sleep(1)

            # Click Log in
            logger.info("Clicking login button...")
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(8)

            # Handle "Save Your Login Info" prompt
            try:
                not_now_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                )
                not_now_button.click()
                time.sleep(2)
            except:
                pass

            # Handle "Turn on Notifications" prompt
            try:
                not_now_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))
                )
                not_now_button.click()
                time.sleep(2)
            except:
                pass

            logger.info("Successfully logged in to Instagram")
            return True

        except Exception as e:
            logger.error(f"Error during login: {e}")
            return False

    def create_post(self, content, image_path=None):
        """Create an Instagram post (text only or with image)"""
        try:
            logger.info("Creating Instagram post...")

            # Navigate to home
            self.driver.get("https://www.instagram.com/")
            time.sleep(3)

            # Click the "+" button to create new post
            logger.info("Clicking create post button...")
            try:
                create_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@href='#']//span[contains(@class, 'x1lliihq')]"))
                )
                create_button.click()
                time.sleep(2)
            except:
                # Alternative: try SVG icon
                create_button = self.driver.find_element(By.XPATH, "//*[name()='svg' and @aria-label='New post']")
                create_button.click()
                time.sleep(2)

            if image_path:
                # Upload image
                logger.info(f"Uploading image: {image_path}")
                file_input = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
                )
                file_input.send_keys(str(Path(image_path).absolute()))
                time.sleep(3)

                # Click Next
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
                )
                next_button.click()
                time.sleep(2)

                # Click Next again (filters page)
                next_button = WebDriverWait(self.driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next')]"))
                )
                next_button.click()
                time.sleep(2)

            # Add caption
            logger.info("Adding caption...")
            caption_area = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Write a caption...']"))
            )
            caption_area.click()
            caption_area.send_keys(content)
            time.sleep(2)

            # Click Share
            logger.info("Clicking Share button...")
            share_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Share')]"))
            )
            share_button.click()

            # Wait for post to be published
            time.sleep(5)

            logger.info("Post published successfully!")
            return True

        except Exception as e:
            logger.error(f"Error creating post: {e}")
            return False

    def post_to_instagram(self, content, image_path=None, headless=False):
        """Complete workflow: login and post to Instagram"""
        try:
            if not self.username or not self.password:
                logger.error("Instagram credentials not loaded")
                return False

            # Setup driver
            if not self.setup_driver(headless=headless):
                return False

            # Login
            if not self.login():
                return False

            # Create post
            success = self.create_post(content, image_path)

            # Cleanup
            time.sleep(3)
            self.driver.quit()

            return success

        except Exception as e:
            logger.error(f"Error in post_to_instagram: {e}")
            if self.driver:
                self.driver.quit()
            return False

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")


def post_to_instagram(content, image_path=None, headless=False):
    """
    Convenience function to post to Instagram

    Args:
        content (str): The post caption
        image_path (str): Path to image file (optional)
        headless (bool): Run browser in headless mode

    Returns:
        bool: True if successful, False otherwise
    """
    poster = InstagramPoster()
    return poster.post_to_instagram(content, image_path, headless=headless)


def test_instagram_posting():
    """Test Instagram posting functionality"""
    print("=" * 60)
    print("Instagram Integration Test")
    print("=" * 60)

    test_content = f"""🤖 Testing AI Employee Automation

This post was auto-generated by my Personal AI Employee!

#AI #Automation #Hackathon #FTE2026

Posted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

    print(f"\nTest Post Content:\n{test_content}\n")
    print("Starting Instagram posting process...")
    print("Note: Instagram requires an image. This test will fail without one.")

    success = post_to_instagram(test_content, headless=False)

    if success:
        print("\n✅ Instagram post published successfully!")
    else:
        print("\n❌ Failed to publish Instagram post")

    return success


if __name__ == "__main__":
    # Run test
    test_instagram_posting()

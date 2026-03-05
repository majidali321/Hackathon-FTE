#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn API Integration
Real LinkedIn posting using Selenium for authentication and posting.
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class LinkedInIntegration:
    """Real LinkedIn integration using Selenium."""

    def __init__(self, credentials_file: str = "credentials.json"):
        self.credentials_file = Path(credentials_file)
        self.username = None
        self.password = None
        self.driver = None
        self.load_credentials()

    def load_credentials(self):
        """Load LinkedIn credentials from credentials.json."""
        try:
            with open(self.credentials_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse credentials
            lines = content.split('\n')
            for line in lines:
                if 'linkedin username' in line.lower():
                    self.username = line.split('=')[1].strip()
                elif 'password' in line.lower() and 'linkedin' not in line.lower():
                    # Get password from next line or same line
                    if '=' in line:
                        self.password = line.split('=')[1].strip()

            if not self.username or not self.password:
                print("[ERROR] LinkedIn credentials not found in credentials.json")
                print("[INFO] Expected format:")
                print("  linkedin username = your-email@example.com")
                print("  password = your-password")
                return False

            print(f"[OK] Loaded LinkedIn credentials for: {self.username}")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to load credentials: {e}")
            return False

    def setup_driver(self, headless: bool = False):
        """Setup Chrome WebDriver."""
        try:
            chrome_options = Options()
            if headless:
                chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

            self.driver = webdriver.Chrome(options=chrome_options)
            self.driver.maximize_window()
            print("[OK] Chrome WebDriver initialized")
            return True

        except Exception as e:
            print(f"[ERROR] Failed to setup WebDriver: {e}")
            print("[INFO] Make sure Chrome and ChromeDriver are installed")
            return False

    def login(self) -> bool:
        """Login to LinkedIn."""
        try:
            print("[INFO] Navigating to LinkedIn...")
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(2)

            # Enter username
            print("[INFO] Entering username...")
            username_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            username_field.send_keys(self.username)

            # Enter password
            print("[INFO] Entering password...")
            password_field = self.driver.find_element(By.ID, "password")
            password_field.send_keys(self.password)

            # Click login button
            print("[INFO] Clicking login button...")
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()

            # Wait for login to complete
            time.sleep(5)

            # Check if login was successful
            if "feed" in self.driver.current_url or "mynetwork" in self.driver.current_url:
                print("[OK] Successfully logged in to LinkedIn!")
                return True
            else:
                print("[WARNING] Login may have failed or requires verification")
                print(f"[INFO] Current URL: {self.driver.current_url}")
                return False

        except Exception as e:
            print(f"[ERROR] Login failed: {e}")
            return False

    def create_post(self, content: str) -> bool:
        """Create a LinkedIn post."""
        try:
            print("[INFO] Navigating to feed...")
            self.driver.get("https://www.linkedin.com/feed/")
            time.sleep(3)

            # Click "Start a post" button
            print("[INFO] Clicking 'Start a post' button...")
            start_post_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.artdeco-button--secondary"))
            )
            start_post_button.click()
            time.sleep(2)

            # Enter post content
            print("[INFO] Entering post content...")
            post_editor = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.ql-editor"))
            )
            post_editor.click()
            post_editor.send_keys(content)
            time.sleep(2)

            # Click Post button
            print("[INFO] Clicking 'Post' button...")
            post_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.share-actions__primary-action"))
            )
            post_button.click()

            print("[OK] Post published successfully!")
            time.sleep(3)
            return True

        except Exception as e:
            print(f"[ERROR] Failed to create post: {e}")
            return False

    def post_with_approval(self, approval_file: Path) -> bool:
        """Post content from an approved file."""
        try:
            # Read the approval file
            with open(approval_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract post content (between ``` markers)
            start = content.find("```\n") + 4
            end = content.find("\n```", start)
            post_content = content[start:end] if start > 3 and end > start else ""

            if not post_content:
                print("[ERROR] Could not extract post content from approval file")
                return False

            print(f"[INFO] Posting content from: {approval_file.name}")
            print("-" * 70)
            print(post_content)
            print("-" * 70)

            # Setup driver and login
            if not self.setup_driver(headless=False):
                return False

            if not self.login():
                print("[ERROR] Login failed, cannot post")
                return False

            # Create the post
            success = self.create_post(post_content)

            # Close driver
            self.driver.quit()

            return success

        except Exception as e:
            print(f"[ERROR] Failed to post: {e}")
            if self.driver:
                self.driver.quit()
            return False

    def close(self):
        """Close the WebDriver."""
        if self.driver:
            self.driver.quit()
            print("[INFO] WebDriver closed")


def post_to_linkedin(approval_file: Path) -> bool:
    """
    Post approved content to LinkedIn.

    Args:
        approval_file: Path to approved post file

    Returns:
        True if successful, False otherwise
    """
    integration = LinkedInIntegration()
    return integration.post_with_approval(approval_file)


# Demo/Test
if __name__ == "__main__":
    print("=" * 70)
    print("  LINKEDIN INTEGRATION TEST")
    print("=" * 70)

    # Test credentials loading
    integration = LinkedInIntegration()

    if integration.username and integration.password:
        print("\n[TEST] Credentials loaded successfully")
        print(f"[INFO] Username: {integration.username}")
        print(f"[INFO] Password: {'*' * len(integration.password)}")

        # Ask user if they want to test posting
        response = input("\n[PROMPT] Do you want to test LinkedIn posting? (yes/no): ")

        if response.lower() in ['yes', 'y']:
            test_content = """🚀 Testing LinkedIn Integration!

I'm building an AI Employee system that can autonomously post to LinkedIn.

This is a test post from my automated system. Pretty cool, right?

#AI #Automation #Innovation #Testing"""

            print("\n[INFO] Setting up WebDriver...")
            if integration.setup_driver(headless=False):
                print("[INFO] Logging in to LinkedIn...")
                if integration.login():
                    print("[INFO] Creating test post...")
                    integration.create_post(test_content)

                integration.close()
        else:
            print("\n[INFO] Test cancelled by user")
    else:
        print("\n[ERROR] Failed to load credentials")
        print("[INFO] Please add LinkedIn credentials to credentials.json:")
        print("  linkedin username = your-email@example.com")
        print("  password = your-password")

    print("\n" + "=" * 70)
    print("  TEST COMPLETE")
    print("=" * 70)

"""
Simple Facebook Test Script
Posts "ALHAMDULILLAH" to Facebook
"""

from integrations.facebook_integration import FacebookPoster
import time

print("=" * 60)
print("Facebook Integration Test")
print("=" * 60)
print()

print("Initializing Facebook poster...")
poster = FacebookPoster()

print(f"Credentials loaded for: {poster.email}")
print()

print("Starting Facebook posting process...")
print("This will open a browser window.")
print()

try:
    # Setup driver
    print("Setting up Chrome WebDriver...")
    if not poster.setup_driver(headless=False):
        print("Failed to setup WebDriver")
        exit(1)

    print("WebDriver ready!")
    print()

    # Login
    print("Logging in to Facebook...")
    if not poster.login():
        print("Login failed!")
        poster.close()
        exit(1)

    print("Login successful!")
    print()

    # Create post
    print("Creating post: 'ALHAMDULILLAH'")
    success = poster.create_post("ALHAMDULILLAH")

    if success:
        print()
        print("=" * 60)
        print("SUCCESS! Post published to Facebook!")
        print("=" * 60)
    else:
        print()
        print("=" * 60)
        print("FAILED! Could not publish post")
        print("=" * 60)

    # Wait a bit before closing
    time.sleep(3)

    # Close browser
    poster.close()

except Exception as e:
    print(f"Error: {e}")
    if poster.driver:
        poster.close()
    exit(1)

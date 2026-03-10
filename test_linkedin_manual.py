"""
LinkedIn Manual Posting Test
This script will open LinkedIn and pause for you to complete any verification
"""

from integrations.linkedin_integration import LinkedInIntegration
import time

print("=" * 70)
print("LINKEDIN POSTING TEST - WITH MANUAL VERIFICATION")
print("=" * 70)
print()

integration = LinkedInIntegration()

print(f"Credentials loaded for: {integration.username}")
print()

print("Starting LinkedIn posting process...")
print("A browser window will open.")
print()

try:
    # Setup driver
    print("Setting up Chrome WebDriver...")
    if not integration.setup_driver(headless=False):
        print("Failed to setup WebDriver")
        exit(1)

    print("WebDriver ready!")
    print()

    # Login
    print("Logging in to LinkedIn...")
    print("If LinkedIn asks for verification, please complete it in the browser.")
    print()

    if not integration.login():
        print()
        print("=" * 70)
        print("VERIFICATION REQUIRED")
        print("=" * 70)
        print()
        print("LinkedIn is asking for security verification.")
        print("Please complete the verification in the browser window.")
        print()
        input("Press ENTER after you've completed the verification and are logged in...")
        print()

    # Now try to create the post
    print("Creating post: 'ALHAMDULILLAH'")
    print()

    post_content = "ALHAMDULILLAH"

    success = integration.create_post(post_content)

    if success:
        print()
        print("=" * 70)
        print("SUCCESS! Post published to LinkedIn!")
        print("=" * 70)
        print()
        print("Check your LinkedIn profile to see the post.")
    else:
        print()
        print("=" * 70)
        print("FAILED! Could not publish post")
        print("=" * 70)

    # Wait a bit before closing
    time.sleep(5)

    # Close browser
    integration.close()

except Exception as e:
    print(f"Error: {e}")
    if integration.driver:
        integration.close()
    exit(1)

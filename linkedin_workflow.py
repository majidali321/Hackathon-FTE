#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Automation Workflow
Monitors approved posts and publishes them to LinkedIn automatically.
"""

import sys
import time
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from linkedin_skills import LinkedInSkills

def monitor_approved_posts(check_interval: int = 60):
    """
    Monitor Approved folder for LinkedIn posts and publish them.

    Args:
        check_interval: Seconds between checks (default: 60)
    """
    print("=" * 70)
    print("  LINKEDIN AUTOMATION WORKFLOW")
    print("=" * 70)
    print(f"\n[INFO] Monitoring Approved/ folder for LinkedIn posts...")
    print(f"[INFO] Check interval: {check_interval} seconds")
    print("[INFO] Press Ctrl+C to stop\n")

    skills = LinkedInSkills()

    try:
        while True:
            # Check for approved posts
            approved_posts = skills.check_approved_posts()

            if approved_posts:
                print(f"\n[INFO] Found {len(approved_posts)} approved post(s)")

                for post_file in approved_posts:
                    print(f"\n[INFO] Processing: {post_file.name}")

                    # Post to LinkedIn
                    success = skills.post_to_linkedin(post_file)

                    if success:
                        print(f"[OK] Successfully posted: {post_file.name}")
                    else:
                        print(f"[ERROR] Failed to post: {post_file.name}")

                    # Wait between posts to avoid rate limiting
                    time.sleep(5)

            # Wait before next check
            time.sleep(check_interval)

    except KeyboardInterrupt:
        print("\n\n[INFO] Monitoring stopped by user")
        print("=" * 70)

def create_test_post():
    """Create a test LinkedIn post for approval."""
    print("=" * 70)
    print("  CREATE TEST LINKEDIN POST")
    print("=" * 70)

    skills = LinkedInSkills()

    # Get topic from user
    print("\n[PROMPT] Enter post topic (or press Enter for default):")
    topic = input("> ").strip()
    if not topic:
        topic = "AI and Automation in 2026"

    # Get tone
    print("\n[PROMPT] Select tone:")
    print("  1. Professional")
    print("  2. Casual")
    print("  3. Inspirational")
    tone_choice = input("> ").strip()

    tone_map = {
        "1": "professional",
        "2": "casual",
        "3": "inspirational"
    }
    tone = tone_map.get(tone_choice, "professional")

    # Create draft
    print(f"\n[INFO] Creating LinkedIn post draft...")
    print(f"[INFO] Topic: {topic}")
    print(f"[INFO] Tone: {tone}")

    approval_file = skills.create_linkedin_post_draft(topic, tone)

    print(f"\n[OK] Draft created: {approval_file}")
    print("\n[NEXT STEPS]:")
    print("  1. Review the draft in Pending_Approval/ folder")
    print("  2. Edit if needed")
    print("  3. Move to Approved/ folder to publish")
    print("  4. Or run the monitoring workflow to auto-publish")
    print("=" * 70)

def main():
    """Main menu for LinkedIn automation."""
    print("=" * 70)
    print("  LINKEDIN AUTOMATION")
    print("=" * 70)
    print("\n[MENU] Select an option:")
    print("  1. Create test post")
    print("  2. Monitor and auto-publish approved posts")
    print("  3. Check approved posts")
    print("  4. Exit")

    choice = input("\n> ").strip()

    if choice == "1":
        create_test_post()
    elif choice == "2":
        monitor_approved_posts()
    elif choice == "3":
        skills = LinkedInSkills()
        approved = skills.check_approved_posts()
        print(f"\n[INFO] Found {len(approved)} approved post(s):")
        for post in approved:
            print(f"  - {post.name}")
    elif choice == "4":
        print("\n[INFO] Exiting...")
    else:
        print("\n[ERROR] Invalid choice")

if __name__ == "__main__":
    main()

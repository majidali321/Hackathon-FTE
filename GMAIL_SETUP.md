#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail Watcher Setup Guide

This guide helps you set up Gmail API access for the Gmail watcher.
"""

print("""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║                    GMAIL WATCHER SETUP GUIDE                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

The Gmail watcher monitors your Gmail inbox and creates tasks for new emails.

SETUP STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install Required Libraries
   ────────────────────────────
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

2. Enable Gmail API in Google Cloud Console
   ─────────────────────────────────────────
   a. Go to: https://console.cloud.google.com/
   b. Create a new project (or select existing)
   c. Enable Gmail API:
      - Go to "APIs & Services" > "Library"
      - Search for "Gmail API"
      - Click "Enable"

3. Create OAuth 2.0 Credentials
   ────────────────────────────
   a. Go to "APIs & Services" > "Credentials"
   b. Click "Create Credentials" > "OAuth client ID"
   c. Choose "Desktop app" as application type
   d. Download the credentials JSON file
   e. Rename it to "credentials.json"
   f. Place it in your project root directory

4. Run the Gmail Watcher
   ─────────────────────
   python watchers/gmail_watcher.py

   On first run:
   - A browser window will open
   - Sign in to your Google account
   - Grant permissions to the app
   - The token will be saved for future use

5. Configuration
   ─────────────
   Edit gmail_watcher.py to customize:
   - check_interval: How often to check (default: 300 seconds)
   - Query filters: Customize which emails to monitor

SECURITY NOTES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

- credentials.json contains your OAuth client secrets
- token.pickle contains your access token
- NEVER commit these files to version control
- Add them to .gitignore

TROUBLESHOOTING:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Issue: "Gmail API libraries not installed"
Solution: Run the pip install command above

Issue: "credentials.json not found"
Solution: Download from Google Cloud Console and place in project root

Issue: "Authentication failed"
Solution: Delete token.pickle and re-authenticate

Issue: "Quota exceeded"
Solution: Gmail API has daily quotas. Wait or request quota increase.

FEATURES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ Monitors unread emails
✓ Detects urgent keywords (urgent, asap, emergency, critical)
✓ Creates tasks with email preview
✓ Extracts sender, subject, and body
✓ Prioritizes urgent emails
✓ Follows Company Handbook rules

NEXT STEPS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After setup, the Gmail watcher will:
1. Check your inbox every 5 minutes
2. Create tasks for new unread emails
3. Flag urgent emails with high priority
4. Log all activities to Logs/gmailwatcher.log

You can then process these tasks using:
  python task_processor.py

""")

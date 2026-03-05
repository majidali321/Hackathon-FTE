#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmail Watcher

Monitors Gmail inbox for new emails and creates tasks in Needs_Action folder.
Uses Gmail API for secure access.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import pickle
import base64

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from watchers.base_watcher import BaseWatcher

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False
    print("[WARNING] Gmail API libraries not installed.")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")


class GmailWatcher(BaseWatcher):
    """Watches Gmail inbox for new emails."""

    # Gmail API scopes
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self, vault_path: str = ".", check_interval: int = 300):
        """
        Initialize Gmail watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 5 minutes)
        """
        super().__init__(vault_path, check_interval)
        self.credentials_file = self.vault_path / 'credentials.json'
        self.token_file = self.vault_path / 'token.pickle'
        self.last_check_file = self.vault_path / '.gmail_last_check'
        self.service = None

        if not GMAIL_AVAILABLE:
            self.logger.error("Gmail API libraries not available")
            return

        # Initialize Gmail service
        self._initialize_service()

    def _initialize_service(self):
        """Initialize Gmail API service."""
        creds = None

        # Load existing token
        if self.token_file.exists():
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                self.logger.info("Refreshing Gmail credentials...")
                creds.refresh(Request())
            else:
                if not self.credentials_file.exists():
                    self.logger.error(
                        f"Gmail credentials file not found: {self.credentials_file}\n"
                        "Please download credentials.json from Google Cloud Console"
                    )
                    return

                self.logger.info("Starting Gmail authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_file), self.SCOPES
                )
                creds = flow.run_local_server(port=8080)

            # Save credentials
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        try:
            self.service = build('gmail', 'v1', credentials=creds)
            self.logger.info("Gmail service initialized successfully")
        except Exception as e:
            self.logger.error(f"Failed to initialize Gmail service: {e}")

    def _get_last_check_time(self) -> str:
        """Get the timestamp of the last check."""
        if self.last_check_file.exists():
            with open(self.last_check_file, 'r') as f:
                return f.read().strip()
        return None

    def _save_last_check_time(self):
        """Save the current timestamp as last check time."""
        with open(self.last_check_file, 'w') as f:
            f.write(datetime.now().isoformat())

    def check_for_updates(self) -> list:
        """
        Check Gmail for new emails.

        Returns:
            List of new email messages
        """
        if not self.service:
            self.logger.warning("Gmail service not initialized")
            return []

        try:
            # Build query - get unread messages
            query = 'is:unread'

            # Get messages
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=10
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                return []

            # Fetch full message details
            full_messages = []
            for msg in messages:
                try:
                    message = self.service.users().messages().get(
                        userId='me',
                        id=msg['id'],
                        format='full'
                    ).execute()
                    full_messages.append(message)
                except Exception as e:
                    self.logger.error(f"Error fetching message {msg['id']}: {e}")

            self._save_last_check_time()
            return full_messages

        except Exception as e:
            self.logger.error(f"Error checking Gmail: {e}")
            return []

    def _extract_email_data(self, message: dict) -> dict:
        """Extract relevant data from Gmail message."""
        headers = message['payload']['headers']

        # Extract headers
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
        date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')

        # Extract body
        body = self._get_message_body(message['payload'])

        # Check for urgent keywords
        urgent_keywords = ['urgent', 'asap', 'emergency', 'critical', 'important']
        is_urgent = any(keyword in subject.lower() or keyword in body.lower()
                       for keyword in urgent_keywords)

        return {
            'id': message['id'],
            'subject': subject,
            'from': from_email,
            'date': date,
            'body': body[:500],  # First 500 chars
            'is_urgent': is_urgent,
            'snippet': message.get('snippet', '')
        }

    def _get_message_body(self, payload: dict) -> str:
        """Extract message body from payload."""
        if 'body' in payload and 'data' in payload['body']:
            return base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')

        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')

        return "Could not extract message body"

    def create_action_file(self, message: dict) -> Path:
        """
        Create an action file for a new email.

        Args:
            message: Gmail message object

        Returns:
            Path to created action file
        """
        email_data = self._extract_email_data(message)

        priority = "high" if email_data['is_urgent'] else "medium"

        content = f"""## Email Details
- **From**: {email_data['from']}
- **Date**: {email_data['date']}
- **Message ID**: {email_data['id']}
- **Urgent**: {'Yes' if email_data['is_urgent'] else 'No'}

## Email Preview
```
{email_data['snippet']}
```

## Message Body (First 500 chars)
```
{email_data['body']}
```

## Suggested Actions
- [ ] Read full email in Gmail
- [ ] Determine if response is needed
- [ ] Draft response if required
- [ ] Create approval request for sending reply
- [ ] Mark as processed when complete

## Company Handbook Rules
- Review communication guidelines
- Check if sender is a new contact (requires approval)
- Flag urgent messages for immediate attention
- Maintain professional tone in all responses
"""

        metadata = {
            'source': 'gmail',
            'email_id': email_data['id'],
            'from': email_data['from'],
            'urgent': email_data['is_urgent']
        }

        return self.create_task_file(
            title=f"Email: {email_data['subject'][:50]}",
            content=content,
            priority=priority,
            metadata=metadata
        )


def main():
    """Main entry point."""
    if not GMAIL_AVAILABLE:
        print("\n[ERROR] Gmail API libraries not installed.")
        print("Install with:")
        print("  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return 1

    vault_path = Path.cwd()
    watcher = GmailWatcher(vault_path=str(vault_path), check_interval=300)

    print("\n" + "=" * 70)
    print("  GMAIL WATCHER")
    print("=" * 70)
    print("\nMonitoring Gmail inbox for new emails...")
    print("Press Ctrl+C to stop\n")

    watcher.start()


if __name__ == "__main__":
    sys.exit(main() or 0)

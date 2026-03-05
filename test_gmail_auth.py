#!/usr/bin/env python3
"""
Simple Gmail authentication test script.
"""

import os
import pickle
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate with Gmail API."""
    creds = None
    token_file = Path('token.pickle')

    # Load existing token
    if token_file.exists():
        print("Loading existing token...")
        with open(token_file, 'rb') as token:
            creds = pickle.load(token)

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing expired token...")
            creds.refresh(Request())
        else:
            print("Starting new authentication flow...")
            print("A browser window will open. Please authorize the application.")
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',
                SCOPES,
                redirect_uri='http://localhost:8080/'
            )
            # Use run_local_server with explicit settings
            creds = flow.run_local_server(
                port=8080,
                prompt='consent',
                success_message='Authentication successful! You can close this window.',
                open_browser=True
            )

        # Save credentials
        print("Saving credentials...")
        with open(token_file, 'wb') as token:
            pickle.dump(creds, token)

    # Test the connection
    print("\nTesting Gmail API connection...")
    service = build('gmail', 'v1', credentials=creds)

    # Get unread messages count
    results = service.users().messages().list(
        userId='me',
        labelIds=['INBOX'],
        q='is:unread',
        maxResults=5
    ).execute()

    messages = results.get('messages', [])
    print(f"\n✓ Success! Found {len(messages)} unread message(s) in inbox.")

    if messages:
        print("\nFirst few unread messages:")
        for i, msg in enumerate(messages[:3], 1):
            message = service.users().messages().get(
                userId='me',
                id=msg['id'],
                format='metadata',
                metadataHeaders=['Subject', 'From']
            ).execute()

            headers = message['payload']['headers']
            subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
            from_email = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')

            print(f"  {i}. From: {from_email}")
            print(f"     Subject: {subject}")

    return True

if __name__ == '__main__':
    try:
        authenticate_gmail()
        print("\n" + "="*60)
        print("Gmail authentication successful!")
        print("="*60)
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WhatsApp Watcher

Monitors WhatsApp messages and creates tasks in Needs_Action folder.
Uses whatsapp-web.js or similar library for access.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from watchers.base_watcher import BaseWatcher

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# WhatsApp integration placeholder
# In a real implementation, you would use:
# - whatsapp-web.js (Node.js library)
# - pywhatkit (Python library)
# - selenium-based automation
# - Official WhatsApp Business API

WHATSAPP_AVAILABLE = False

class WhatsAppWatcher(BaseWatcher):
    """Watches WhatsApp for new messages."""

    def __init__(self, vault_path: str = ".", check_interval: int = 60):
        """
        Initialize WhatsApp watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks (default: 1 minute)
        """
        super().__init__(vault_path, check_interval)
        self.session_file = self.vault_path / '.whatsapp_session'
        self.last_message_id = self._load_last_message_id()

        if not WHATSAPP_AVAILABLE:
            self.logger.warning(
                "WhatsApp integration not fully implemented. "
                "This is a placeholder/demo version."
            )

    def _load_last_message_id(self) -> str:
        """Load the last processed message ID."""
        if self.session_file.exists():
            with open(self.session_file, 'r') as f:
                return f.read().strip()
        return None

    def _save_last_message_id(self, message_id: str):
        """Save the last processed message ID."""
        with open(self.session_file, 'w') as f:
            f.write(message_id)

    def check_for_updates(self) -> list:
        """
        Check WhatsApp for new messages.

        Returns:
            List of new messages

        Note: This is a placeholder implementation.
        In production, you would:
        1. Connect to WhatsApp Web via automation
        2. Fetch unread messages
        3. Filter by criteria (urgent keywords, new contacts, etc.)
        4. Return list of messages to process
        """
        if not WHATSAPP_AVAILABLE:
            # Demo mode - return empty list
            self.logger.info("WhatsApp integration not available (demo mode)")
            return []

        try:
            # Placeholder for actual WhatsApp API calls
            # In real implementation:
            # messages = whatsapp_client.get_unread_messages()
            # return [msg for msg in messages if msg.id > self.last_message_id]

            return []

        except Exception as e:
            self.logger.error(f"Error checking WhatsApp: {e}")
            return []

    def _extract_message_data(self, message: dict) -> dict:
        """Extract relevant data from WhatsApp message."""
        # Placeholder structure
        return {
            'id': message.get('id', 'unknown'),
            'from': message.get('from', 'Unknown'),
            'from_name': message.get('from_name', 'Unknown'),
            'body': message.get('body', ''),
            'timestamp': message.get('timestamp', datetime.now().isoformat()),
            'is_group': message.get('is_group', False),
            'has_media': message.get('has_media', False),
            'is_urgent': self._check_urgent(message.get('body', ''))
        }

    def _check_urgent(self, text: str) -> bool:
        """Check if message contains urgent keywords."""
        urgent_keywords = ['urgent', 'asap', 'emergency', 'help', 'critical', 'important']
        return any(keyword in text.lower() for keyword in urgent_keywords)

    def create_action_file(self, message: dict) -> Path:
        """
        Create an action file for a new WhatsApp message.

        Args:
            message: WhatsApp message object

        Returns:
            Path to created action file
        """
        msg_data = self._extract_message_data(message)

        priority = "high" if msg_data['is_urgent'] else "medium"

        content = f"""## Message Details
- **From**: {msg_data['from_name']} ({msg_data['from']})
- **Timestamp**: {msg_data['timestamp']}
- **Message ID**: {msg_data['id']}
- **Group Message**: {'Yes' if msg_data['is_group'] else 'No'}
- **Has Media**: {'Yes' if msg_data['has_media'] else 'No'}
- **Urgent**: {'Yes' if msg_data['is_urgent'] else 'No'}

## Message Content
```
{msg_data['body']}
```

## Suggested Actions
- [ ] Read full message in WhatsApp
- [ ] Determine if response is needed
- [ ] Draft response if required
- [ ] Check if sender is a new contact (requires approval)
- [ ] Create approval request for sending reply
- [ ] Mark as processed when complete

## Company Handbook Rules
- Always be polite and professional on WhatsApp
- Flag urgent messages for immediate attention
- New contacts require approval for first 3 interactions
- Maintain confidentiality of sensitive information
"""

        metadata = {
            'source': 'whatsapp',
            'message_id': msg_data['id'],
            'from': msg_data['from'],
            'urgent': msg_data['is_urgent'],
            'is_group': msg_data['is_group']
        }

        # Save last message ID
        self._save_last_message_id(msg_data['id'])

        return self.create_task_file(
            title=f"WhatsApp: {msg_data['from_name'][:30]}",
            content=content,
            priority=priority,
            metadata=metadata
        )


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("  WHATSAPP WATCHER (DEMO MODE)")
    print("=" * 70)
    print("\n[INFO] This is a placeholder implementation.")
    print("[INFO] To enable WhatsApp integration, you need to:")
    print("  1. Choose a WhatsApp automation library:")
    print("     - whatsapp-web.js (Node.js)")
    print("     - pywhatkit (Python)")
    print("     - selenium-based automation")
    print("     - Official WhatsApp Business API")
    print("  2. Set up authentication (QR code scan)")
    print("  3. Implement message fetching logic")
    print("  4. Handle session management")
    print("\n[INFO] For now, this watcher runs in demo mode (no actual monitoring)")
    print("\nPress Ctrl+C to stop\n")

    vault_path = Path.cwd()
    watcher = WhatsAppWatcher(vault_path=str(vault_path), check_interval=60)

    try:
        watcher.start()
    except KeyboardInterrupt:
        print("\n[INFO] WhatsApp watcher stopped")


if __name__ == "__main__":
    sys.exit(main() or 0)

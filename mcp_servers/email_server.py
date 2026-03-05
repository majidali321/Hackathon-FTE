#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Email Server

A simple MCP server for sending emails via SMTP.
Implements the Model Context Protocol for email operations.
"""

import sys
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional
import logging

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class EmailMCPServer:
    """MCP Server for email operations."""

    def __init__(self):
        """Initialize the email MCP server."""
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_user = os.getenv('SMTP_USER', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')

        # Log file
        self.log_file = Path('Logs/email_mcp.log')
        self.log_file.parent.mkdir(exist_ok=True)

    def send_email(self, to: str, subject: str, body: str,
                   cc: Optional[str] = None, bcc: Optional[str] = None,
                   html: bool = False) -> Dict[str, any]:
        """
        Send an email via SMTP.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body
            cc: CC recipients (comma-separated)
            bcc: BCC recipients (comma-separated)
            html: Whether body is HTML

        Returns:
            Dictionary with status and message
        """
        try:
            # Validate credentials
            if not self.smtp_user or not self.smtp_password:
                return {
                    'success': False,
                    'error': 'SMTP credentials not configured'
                }

            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.smtp_user
            msg['To'] = to
            msg['Subject'] = subject

            if cc:
                msg['Cc'] = cc
            if bcc:
                msg['Bcc'] = bcc

            # Attach body
            mime_type = 'html' if html else 'plain'
            msg.attach(MIMEText(body, mime_type))

            # Connect and send
            logger.info(f"Connecting to {self.smtp_host}:{self.smtp_port}")

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)

                # Get all recipients
                recipients = [to]
                if cc:
                    recipients.extend([r.strip() for r in cc.split(',')])
                if bcc:
                    recipients.extend([r.strip() for r in bcc.split(',')])

                server.send_message(msg, self.smtp_user, recipients)

            # Log success
            self._log_email(to, subject, 'sent')

            logger.info(f"Email sent successfully to {to}")

            return {
                'success': True,
                'message': f'Email sent to {to}',
                'timestamp': datetime.now().isoformat()
            }

        except smtplib.SMTPAuthenticationError:
            error = 'SMTP authentication failed - check credentials'
            logger.error(error)
            self._log_email(to, subject, 'failed', error)
            return {'success': False, 'error': error}

        except smtplib.SMTPException as e:
            error = f'SMTP error: {str(e)}'
            logger.error(error)
            self._log_email(to, subject, 'failed', error)
            return {'success': False, 'error': error}

        except Exception as e:
            error = f'Unexpected error: {str(e)}'
            logger.error(error)
            self._log_email(to, subject, 'failed', error)
            return {'success': False, 'error': error}

    def _log_email(self, to: str, subject: str, status: str, error: str = None):
        """Log email activity."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'to': to,
            'subject': subject,
            'status': status,
            'error': error
        }

        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')

    def test_connection(self) -> Dict[str, any]:
        """Test SMTP connection."""
        try:
            logger.info("Testing SMTP connection...")

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)

            logger.info("SMTP connection successful!")
            return {
                'success': True,
                'message': 'SMTP connection successful',
                'host': self.smtp_host,
                'port': self.smtp_port,
                'user': self.smtp_user
            }

        except Exception as e:
            error = f'Connection test failed: {str(e)}'
            logger.error(error)
            return {'success': False, 'error': error}


# MCP Protocol Handler
def handle_mcp_request(request: Dict) -> Dict:
    """
    Handle MCP protocol requests.

    Args:
        request: MCP request dictionary

    Returns:
        MCP response dictionary
    """
    server = EmailMCPServer()

    action = request.get('action')
    params = request.get('params', {})

    if action == 'send_email':
        return server.send_email(**params)

    elif action == 'test_connection':
        return server.test_connection()

    else:
        return {
            'success': False,
            'error': f'Unknown action: {action}'
        }


# Standalone functions for direct use
def send_email(to: str, subject: str, body: str, **kwargs) -> Dict:
    """Send an email (convenience function)."""
    server = EmailMCPServer()
    return server.send_email(to, subject, body, **kwargs)


def test_connection() -> Dict:
    """Test SMTP connection (convenience function)."""
    server = EmailMCPServer()
    return server.test_connection()


# CLI Interface
def main():
    """Main entry point for CLI usage."""
    import argparse

    parser = argparse.ArgumentParser(description='MCP Email Server')
    parser.add_argument('--test', action='store_true', help='Test SMTP connection')
    parser.add_argument('--send', action='store_true', help='Send a test email')
    parser.add_argument('--to', help='Recipient email address')
    parser.add_argument('--subject', default='Test Email', help='Email subject')
    parser.add_argument('--body', default='This is a test email', help='Email body')

    args = parser.parse_args()

    print("=" * 70)
    print("  MCP EMAIL SERVER")
    print("=" * 70)

    server = EmailMCPServer()

    if args.test:
        print("\n[TEST] Testing SMTP connection...")
        result = server.test_connection()

        if result['success']:
            print(f"\n[OK] Connection successful!")
            print(f"  Host: {result['host']}")
            print(f"  Port: {result['port']}")
            print(f"  User: {result['user']}")
        else:
            print(f"\n[ERROR] {result['error']}")
            return 1

    elif args.send:
        if not args.to:
            print("\n[ERROR] --to argument required for sending email")
            return 1

        print(f"\n[SEND] Sending test email to {args.to}...")
        result = server.send_email(args.to, args.subject, args.body)

        if result['success']:
            print(f"\n[OK] {result['message']}")
        else:
            print(f"\n[ERROR] {result['error']}")
            return 1

    else:
        print("\nUsage:")
        print("  python email_server.py --test              # Test connection")
        print("  python email_server.py --send --to=email   # Send test email")
        print("\nEnvironment variables required:")
        print("  SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD")

    print("\n" + "=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())

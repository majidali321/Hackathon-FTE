# MCP Server Setup Guide

## What is MCP?

MCP (Model Context Protocol) is a protocol for connecting AI models to external tools and services. It allows Claude Code to interact with external systems like email, databases, APIs, etc.

## MCP Server for Email

This guide helps you set up an MCP server for sending emails.

## Prerequisites

```bash
pip install mcp anthropic-mcp
```

## Architecture

```
┌─────────────────┐
│  Claude Code    │
│  (AI Employee)  │
└────────┬────────┘
         │
         │ MCP Protocol
         │
┌────────▼────────┐
│   MCP Server    │
│  (Email Bridge) │
└────────┬────────┘
         │
         │ SMTP/API
         │
┌────────▼────────┐
│  Email Service  │
│  (Gmail/SMTP)   │
└─────────────────┘
```

## Setup Steps

### 1. Create MCP Server Configuration

Create `mcp_servers/email_config.json`:

```json
{
  "mcpServers": {
    "email": {
      "command": "python",
      "args": ["mcp_servers/email_server.py"],
      "env": {
        "SMTP_HOST": "smtp.gmail.com",
        "SMTP_PORT": "587",
        "SMTP_USER": "your-email@gmail.com",
        "SMTP_PASSWORD": "your-app-password"
      }
    }
  }
}
```

### 2. Gmail App Password Setup

For Gmail:
1. Go to Google Account settings
2. Enable 2-Factor Authentication
3. Generate an App Password:
   - Go to Security > 2-Step Verification > App passwords
   - Select "Mail" and "Other (Custom name)"
   - Copy the generated password
4. Use this password in the config (NOT your regular password)

### 3. Environment Variables

Create `.env` file (NEVER commit this):

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### 4. Test the MCP Server

```bash
python mcp_servers/email_server.py --test
```

## Using the MCP Server

### From Python (skills.py)

```python
from mcp_client import send_email_via_mcp

# Send an email
send_email_via_mcp(
    to="recipient@example.com",
    subject="Test Email",
    body="This is a test email sent via MCP server"
)
```

### From Claude Code

Claude Code can automatically discover and use MCP servers configured in your settings.

## Security Best Practices

1. **Never commit credentials**
   - Add `.env` to `.gitignore`
   - Add `credentials.json` to `.gitignore`
   - Add `token.pickle` to `.gitignore`

2. **Use App Passwords**
   - Never use your main email password
   - Use app-specific passwords

3. **Limit Permissions**
   - Only grant necessary permissions
   - Review access regularly

4. **Audit Logging**
   - All emails sent are logged
   - Review logs regularly

## Troubleshooting

### Issue: "Connection refused"
**Solution**: Check SMTP host and port settings

### Issue: "Authentication failed"
**Solution**: Verify app password is correct

### Issue: "MCP server not found"
**Solution**: Check the server path in config

### Issue: "Rate limit exceeded"
**Solution**: Gmail has sending limits (500/day for free accounts)

## Alternative Email Services

### SendGrid
```json
{
  "SMTP_HOST": "smtp.sendgrid.net",
  "SMTP_PORT": "587",
  "SMTP_USER": "apikey",
  "SMTP_PASSWORD": "your-sendgrid-api-key"
}
```

### Mailgun
```json
{
  "SMTP_HOST": "smtp.mailgun.org",
  "SMTP_PORT": "587",
  "SMTP_USER": "postmaster@your-domain.mailgun.org",
  "SMTP_PASSWORD": "your-mailgun-password"
}
```

### AWS SES
```json
{
  "SMTP_HOST": "email-smtp.us-east-1.amazonaws.com",
  "SMTP_PORT": "587",
  "SMTP_USER": "your-ses-smtp-username",
  "SMTP_PASSWORD": "your-ses-smtp-password"
}
```

## Features

✓ Send emails via SMTP
✓ HTML and plain text support
✓ Attachments support
✓ CC and BCC support
✓ Error handling and retries
✓ Rate limiting
✓ Logging and audit trail

## Next Steps

1. Set up your email credentials
2. Test the MCP server
3. Integrate with approval workflow
4. Test end-to-end email sending

## Integration with AI Employee

The MCP server integrates with the AI Employee system:

1. **Email Draft Creation**: Task processor creates email draft
2. **Approval Request**: Draft sent for human approval
3. **Approval**: Human reviews and approves
4. **MCP Send**: System uses MCP server to send email
5. **Logging**: Activity logged to audit trail
6. **Completion**: Task moved to Done folder

---

**Status**: Ready for implementation
**Priority**: HIGH (Silver Tier requirement)

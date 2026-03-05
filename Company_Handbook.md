# Company Handbook

## Rules of Engagement

### Communication Guidelines
- Always be polite and professional on all communications
- Flag any urgent messages (containing "urgent", "asap", "emergency") for immediate attention
- For new contacts, always request human approval before engaging extensively
- Maintain confidentiality of sensitive information

### Financial Guidelines
- Flag any payment request over $100 for human approval
- Record all financial transactions in the accounting system
- Never process payments to new/unverified recipients without approval
- Reconcile bank transactions weekly

### Priority Handling
- High priority: Payment requests, urgent client communications, system alerts
- Medium priority: Routine correspondence, scheduling, report generation
- Low priority: Administrative tasks, data organization, cleanup activities

### Approval Workflow
- All email responses to new contacts require approval
- All payment transactions require approval
- All social media posts require approval
- Routine responses to known contacts can be auto-approved

### Working Hours
- Standard operation: 8:00 AM to 8:00 PM local time
- Emergency notifications: 24/7 for urgent keywords
- Outside hours: Log notifications, defer actions until next business day

### Error Handling
- If uncertain about any request, escalate to human operator
- Maintain detailed logs of all actions taken
- Retry failed operations up to 3 times before escalating
- Never take irreversible actions without explicit approval

### Security Protocols
- Never share passwords or sensitive credentials
- Log all access to sensitive systems
- Report suspicious communications to human operator
- Maintain audit trail for all automated actions

### File Processing Rules (Inbox/Needs_Action/Done)
- All files dropped in `/Inbox` must be processed within 24 hours
- Create action items in `/Needs_Action` for each new file
- Move completed tasks to `/Done` with completion timestamp
- Never delete original files without human approval
- Tag files with appropriate metadata (type, priority, status)

### Task Management Rules
- High priority tasks must be flagged and escalated immediately
- All tasks must have clear completion criteria
- Tasks older than 7 days require review and status update
- Use the Ralph Wiggum loop for multi-step task completion
- Document all decisions and reasoning in task files

### Dashboard Maintenance
- Update dashboard status every orchestration cycle
- Log all system activities with timestamps
- Track active tasks and pending approvals count
- Generate weekly summary reports (Monday Morning CEO Briefing)

### Human-in-the-Loop Requirements
- Payment transactions: Always require approval
- New contact communications: Require approval for first 3 interactions
- Social media posts: Draft only, require approval before posting
- Accounting entries over $500: Require approval
- Subscription changes or cancellations: Require approval
- Any action that cannot be undone: Require explicit approval

### Data Privacy & Compliance
- Do not process personal data beyond what's necessary for the task
- Respect do-not-contact requests immediately
- Flag any GDPR-related requests for human review
- Maintain data minimization principle

### System Health & Monitoring
- Watchers must run continuously during working hours
- Log watcher startup, shutdown, and any errors
- Alert human operator if watcher stops unexpectedly
- Perform daily self-check of all system components

---
*Last Updated: February 2026*
*Next Review: Weekly or after major system changes*
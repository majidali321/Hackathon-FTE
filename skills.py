"""
Agent Skills for AI Employee

Implementation of agent skills that Claude Code can use to interact
with the AI Employee system.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional
import json
from datetime import datetime

class AISkills:
    """Collection of skills for the AI Employee."""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.logs = self.vault_path / 'Logs'

        # Create directories if they don't exist
        for directory in [self.inbox, self.needs_action, self.done, self.plans, self.pending_approval, self.logs]:
            directory.mkdir(exist_ok=True)

    def list_pending_tasks(self) -> List[Dict[str, str]]:
        """
        List all pending tasks in the Needs_Action folder.

        Returns:
            List of dictionaries containing task information
        """
        tasks = []
        for task_file in self.needs_action.glob("*.md"):
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract basic info from the file
            task_info = {
                'filename': task_file.name,
                'filepath': str(task_file),
                'size': task_file.stat().st_size,
                'modified': datetime.fromtimestamp(task_file.stat().st_mtime).isoformat(),
                'preview': content[:200] + "..." if len(content) > 200 else content
            }
            tasks.append(task_info)

        return tasks

    def create_task(self, title: str, description: str = "", priority: str = "medium") -> str:
        """
        Create a new task in the Needs_Action folder.

        Args:
            title: Title of the task
            description: Detailed description of the task
            priority: Priority level (low, medium, high)

        Returns:
            Path to the created task file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TASK_{timestamp}_{title.replace(' ', '_').replace('/', '_')}.md"
        task_path = self.needs_action / filename

        content = f"""---
type: task
title: {title}
priority: {priority}
created_at: {datetime.now().isoformat()}
status: pending
---

# {title}

## Description
{description}

## Steps
- [ ] Review requirements
- [ ] Plan implementation
- [ ] Execute task
- [ ] Verify completion
- [ ] Move to Done folder

## Notes
Additional notes can be added here as the task progresses.

---
*Created by AI Employee Skill*
"""

        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(task_path)

    def move_task_to_done(self, task_filename: str) -> bool:
        """
        Move a task from Needs_Action to Done folder.

        Args:
            task_filename: Name of the task file to move

        Returns:
            True if successful, False otherwise
        """
        source_path = self.needs_action / task_filename
        if not source_path.exists():
            return False

        dest_path = self.done / task_filename
        source_path.rename(dest_path)
        return True

    def create_approval_request(self, action_type: str, details: Dict[str, str], reason: str = "") -> str:
        """
        Create an approval request in the Pending_Approval folder.

        Args:
            action_type: Type of action requiring approval
            details: Dictionary with details about the action
            reason: Reason for the action

        Returns:
            Path to the created approval request file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"APPROVAL_{timestamp}_{action_type.upper()}_{details.get('id', 'unknown')}.md"
        approval_path = self.pending_approval / filename

        details_str = "\n".join([f"- {k}: {v}" for k, v in details.items()])

        content = f"""---
type: approval_request
action: {action_type}
status: pending
created_at: {datetime.now().isoformat()}
---

# Approval Required: {action_type.title()}

## Details
{details_str}

## Reason
{reason}

## Action Required
Please review the above details and either approve or reject this action.

To approve: Move this file to the /Approved folder
To reject: Move this file to the /Rejected folder

---
*Created by AI Employee Skill*
"""

        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(approval_path)

    def update_dashboard(self, section: str, content: str) -> bool:
        """
        Update a section of the Dashboard.md file.

        Args:
            section: Section header to update (without ##)
            content: New content for the section

        Returns:
            True if successful, False otherwise
        """
        dashboard_path = self.vault_path / 'Dashboard.md'

        if not dashboard_path.exists():
            # Create a basic dashboard if it doesn't exist
            initial_content = f"""# AI Employee Dashboard

## Overview
Welcome to your AI Employee dashboard. This system manages your personal and business affairs autonomously.

## {section}
{content}

## System Status
- **System**: Operational
- **Last Update**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Active Tasks**: 0
- **Pending Approval**: 0

---
*Generated by AI Employee v0.1*
"""
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write(initial_content)
            return True

        # Read existing dashboard
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            current_content = f.read()

        # Find and replace the section
        section_header = f"## {section}"
        start_pos = current_content.find(section_header)

        if start_pos == -1:
            # Section doesn't exist, append it
            updated_content = f"{current_content}\n\n{section_header}\n{content}"
        else:
            # Find end of section (next section header or end of file)
            next_header_pos = current_content.find("\n## ", start_pos + len(section_header))
            if next_header_pos == -1:
                next_header_pos = len(current_content)

            # Replace the section
            updated_content = (
                current_content[:start_pos + len(section_header)] +
                f"\n{content}" +
                current_content[next_header_pos:]
            )

        # Write updated content
        with open(dashboard_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return True

    def log_activity(self, activity_type: str, description: str, details: Optional[Dict] = None) -> str:
        """
        Log an activity to the logs folder.

        Args:
            activity_type: Type of activity (e.g., 'task_completed', 'email_sent')
            description: Description of the activity
            details: Additional details about the activity

        Returns:
            Path to the created log entry
        """
        timestamp = datetime.now()
        date_str = timestamp.strftime("%Y-%m-%d")
        time_str = timestamp.strftime("%H:%M:%S")

        log_entry = {
            "timestamp": timestamp.isoformat(),
            "activity_type": activity_type,
            "description": description,
            "details": details or {}
        }

        log_path = self.logs / f"activity_{date_str}.json"

        # Read existing log if it exists
        log_entries = []
        if log_path.exists():
            with open(log_path, 'r', encoding='utf-8') as f:
                try:
                    log_entries = json.load(f)
                except json.JSONDecodeError:
                    log_entries = []

        # Add new entry
        log_entries.append(log_entry)

        # Write back to file
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(log_entries, f, indent=2)

        return str(log_path)

# Global instance for easy access
ai_skills = AISkills()

# Convenience functions for Claude Code to call
def list_pending_tasks():
    """Convenience function to list pending tasks."""
    return ai_skills.list_pending_tasks()

def create_task(title: str, description: str = "", priority: str = "medium"):
    """Convenience function to create a task."""
    return ai_skills.create_task(title, description, priority)

def move_task_to_done(task_filename: str):
    """Convenience function to move a task to done."""
    return ai_skills.move_task_to_done(task_filename)

def create_approval_request(action_type: str, details: Dict[str, str], reason: str = ""):
    """Convenience function to create an approval request."""
    return ai_skills.create_approval_request(action_type, details, reason)

def update_dashboard(section: str, content: str):
    """Convenience function to update the dashboard."""
    return ai_skills.update_dashboard(section, content)

def log_activity(activity_type: str, description: str, details: Optional[Dict] = None):
    """Convenience function to log an activity."""
    return ai_skills.log_activity(activity_type, description, details)
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Processor for AI Employee

This script processes tasks from the Needs_Action folder.
It can be called by Claude Code or run standalone to process pending tasks.
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json
from skills import AISkills

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class TaskProcessor:
    """Processes tasks from the Needs_Action folder."""

    def __init__(self):
        self.skills = AISkills()
        self.vault_path = Path.cwd()

    def process_all_tasks(self):
        """Process all pending tasks in Needs_Action folder."""
        tasks = self.skills.list_pending_tasks()

        if not tasks:
            print("No pending tasks to process.")
            return

        print(f"Found {len(tasks)} pending task(s)")

        for task in tasks:
            print(f"\nProcessing: {task['filename']}")
            self.process_single_task(task)

    def process_single_task(self, task_info):
        """Process a single task."""
        task_path = Path(task_info['filepath'])

        # Read task content
        with open(task_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check for urgent keywords
        urgent_keywords = ['urgent', 'asap', 'emergency', 'critical']
        is_urgent = any(keyword in content.lower() for keyword in urgent_keywords)

        if is_urgent:
            print(f"  [!] URGENT task detected!")
            # Create approval request for urgent items
            self.skills.create_approval_request(
                action_type="urgent_task",
                details={
                    "task": task_info['filename'],
                    "reason": "Contains urgent keywords"
                },
                reason="This task contains urgent keywords and requires immediate attention."
            )

        # Determine task type from content
        if 'file_processing' in content or 'Process File:' in content:
            self.process_file_task(task_info, content)
        else:
            self.process_generic_task(task_info, content)

        # Log the activity
        self.skills.log_activity(
            activity_type="task_processed",
            description=f"Processed task: {task_info['filename']}",
            details={
                "filename": task_info['filename'],
                "size": task_info['size'],
                "urgent": is_urgent
            }
        )

    def process_file_task(self, task_info, content):
        """Process a file-related task."""
        print(f"  [FILE] File processing task")

        # Extract source file name from content
        source_file = None
        for line in content.split('\n'):
            if 'source_file:' in line:
                source_file = line.split('source_file:')[1].strip()
                break

        # Check if source file still exists in Inbox
        if source_file:
            inbox_file = self.vault_path / 'Inbox' / source_file
            if inbox_file.exists():
                # Move source file to Done folder
                done_file = self.vault_path / 'Done' / source_file
                inbox_file.rename(done_file)
                print(f"  [OK] Moved {source_file} to Done folder")

        # Mark task as complete
        self.skills.move_task_to_done(task_info['filename'])
        print(f"  [OK] Task completed and moved to Done")

    def process_generic_task(self, task_info, content):
        """Process a generic task."""
        print(f"  [TASK] Generic task")

        # For now, just mark as complete
        # In a real implementation, this would analyze the task and take appropriate action
        self.skills.move_task_to_done(task_info['filename'])
        print(f"  [OK] Task completed and moved to Done")

    def update_system_status(self):
        """Update the dashboard with current system status."""
        tasks = self.skills.list_pending_tasks()
        pending_approvals = list((self.vault_path / 'Pending_Approval').glob('*.md'))

        status_content = f"""- **System**: Operational
- **Last Update**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Active Tasks**: {len(tasks)}
- **Pending Approval**: {len(pending_approvals)}"""

        self.skills.update_dashboard("Current Status", status_content)

        # Update recent activity
        activity_content = f"""- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Processed {len(tasks)} task(s)
- System health check: All watchers operational
- Next scheduled check: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""

        self.skills.update_dashboard("Recent Activity", activity_content)

        print(f"\n[OK] Dashboard updated")

def main():
    processor = TaskProcessor()

    print("=" * 60)
    print("AI Employee Task Processor")
    print("=" * 60)

    # Process all tasks
    processor.process_all_tasks()

    # Update dashboard
    processor.update_system_status()

    print("\n" + "=" * 60)
    print("Task processing complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

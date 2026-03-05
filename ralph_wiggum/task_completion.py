#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task Completion Checker

Verifies task completion status and determines if more work is needed.
Works with the Ralph Wiggum loop to ensure autonomous task completion.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import re

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class TaskCompletionChecker:
    """
    Checks if a task is complete and what remains to be done.
    """

    def __init__(self, vault_path: str = "."):
        """
        Initialize the completion checker.

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.pending_approval = self.vault_path / 'Pending_Approval'

    def check_task_completion(self, task_file: Path) -> Dict:
        """
        Check if a task is complete.

        Args:
            task_file: Path to task file

        Returns:
            Dictionary with completion status and details
        """
        if not task_file.exists():
            return {
                'complete': False,
                'status': 'not_found',
                'message': 'Task file not found'
            }

        # Read task content
        with open(task_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse metadata
        metadata = self._parse_frontmatter(content)

        # Check explicit status
        status = metadata.get('status', '').lower()
        if status in ['complete', 'done', 'finished']:
            return {
                'complete': True,
                'status': 'complete',
                'message': 'Task marked as complete'
            }

        if status in ['blocked', 'cancelled']:
            return {
                'complete': False,
                'status': status,
                'message': f'Task is {status}'
            }

        # Check if task is in Done folder
        if self.done in task_file.parents:
            return {
                'complete': True,
                'status': 'complete',
                'message': 'Task in Done folder'
            }

        # Check if waiting for approval
        if self.pending_approval in task_file.parents:
            return {
                'complete': False,
                'status': 'pending_approval',
                'message': 'Waiting for human approval',
                'requires_approval': True
            }

        # Check checkboxes
        checkbox_status = self._check_checkboxes(content)

        if checkbox_status['total'] == 0:
            # No checkboxes - check for completion indicators
            completion_indicators = [
                'task complete',
                'finished',
                'done',
                '✓ complete',
                'all steps completed'
            ]

            content_lower = content.lower()
            if any(indicator in content_lower for indicator in completion_indicators):
                return {
                    'complete': True,
                    'status': 'complete',
                    'message': 'Completion indicator found'
                }

            # No clear completion status
            return {
                'complete': False,
                'status': 'in_progress',
                'message': 'No completion indicators found',
                'remaining_steps': ['Review and mark as complete']
            }

        # Check checkbox completion
        if checkbox_status['completed'] == checkbox_status['total']:
            return {
                'complete': True,
                'status': 'complete',
                'message': 'All checkboxes completed',
                'progress': 1.0
            }

        # Task in progress
        return {
            'complete': False,
            'status': 'in_progress',
            'message': f"{checkbox_status['completed']}/{checkbox_status['total']} steps completed",
            'progress': checkbox_status['completed'] / checkbox_status['total'],
            'remaining_steps': checkbox_status['unchecked_items'],
            'completed_steps': checkbox_status['checked_items']
        }

    def _parse_frontmatter(self, content: str) -> Dict:
        """Parse YAML frontmatter from markdown content."""
        metadata = {}
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)

        if frontmatter_match:
            frontmatter = frontmatter_match.group(1)
            for line in frontmatter.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    metadata[key.strip()] = value.strip()

        return metadata

    def _check_checkboxes(self, content: str) -> Dict:
        """
        Check checkbox completion status.

        Returns:
            Dictionary with checkbox statistics
        """
        checked_pattern = r'- \[x\] (.+)'
        unchecked_pattern = r'- \[ \] (.+)'

        checked_items = re.findall(checked_pattern, content, re.IGNORECASE)
        unchecked_items = re.findall(unchecked_pattern, content)

        return {
            'total': len(checked_items) + len(unchecked_items),
            'completed': len(checked_items),
            'remaining': len(unchecked_items),
            'checked_items': checked_items,
            'unchecked_items': unchecked_items
        }

    def get_next_action(self, task_file: Path) -> Optional[Dict]:
        """
        Determine the next action needed for a task.

        Args:
            task_file: Path to task file

        Returns:
            Dictionary with next action details, or None if complete
        """
        completion_status = self.check_task_completion(task_file)

        if completion_status['complete']:
            return None

        if completion_status['status'] == 'pending_approval':
            return {
                'action': 'wait_for_approval',
                'message': 'Waiting for human approval',
                'blocking': True
            }

        if completion_status['status'] == 'blocked':
            return {
                'action': 'resolve_blocker',
                'message': 'Task is blocked',
                'blocking': True
            }

        # Get next uncompleted step
        remaining_steps = completion_status.get('remaining_steps', [])
        if remaining_steps:
            next_step = remaining_steps[0]
            return {
                'action': 'execute_step',
                'step': next_step,
                'message': f'Next step: {next_step}',
                'blocking': False
            }

        return {
            'action': 'review',
            'message': 'Review task and mark as complete',
            'blocking': False
        }

    def mark_task_complete(self, task_file: Path) -> bool:
        """
        Mark a task as complete and move to Done folder.

        Args:
            task_file: Path to task file

        Returns:
            True if successful, False otherwise
        """
        if not task_file.exists():
            return False

        try:
            # Read current content
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update status in frontmatter
            if '---' in content:
                # Update existing frontmatter
                content = re.sub(
                    r'status: \w+',
                    'status: complete',
                    content
                )
                # Add completion timestamp
                if 'completed_at:' not in content:
                    content = re.sub(
                        r'(---\n.*?)(---)',
                        f'\\1completed_at: {datetime.now().isoformat()}\n\\2',
                        content,
                        flags=re.DOTALL
                    )
            else:
                # Add frontmatter
                frontmatter = f"""---
status: complete
completed_at: {datetime.now().isoformat()}
---

"""
                content = frontmatter + content

            # Write updated content
            with open(task_file, 'w', encoding='utf-8') as f:
                f.write(content)

            # Move to Done folder
            done_path = self.done / task_file.name
            task_file.rename(done_path)

            return True

        except Exception as e:
            print(f"Error marking task complete: {e}")
            return False

    def get_all_incomplete_tasks(self) -> List[Tuple[Path, Dict]]:
        """
        Get all incomplete tasks from Needs_Action folder.

        Returns:
            List of tuples (task_file, completion_status)
        """
        incomplete_tasks = []

        if not self.needs_action.exists():
            return incomplete_tasks

        for task_file in self.needs_action.glob("*.md"):
            completion_status = self.check_task_completion(task_file)
            if not completion_status['complete']:
                incomplete_tasks.append((task_file, completion_status))

        # Sort by priority and progress
        def sort_key(item):
            _, status = item
            priority_map = {'high': 0, 'medium': 1, 'low': 2}
            priority = priority_map.get(status.get('priority', 'medium'), 1)
            progress = status.get('progress', 0)
            return (priority, -progress)  # High priority first, then by progress

        incomplete_tasks.sort(key=sort_key)
        return incomplete_tasks


def main():
    """Main entry point for testing."""
    print("\n" + "="*70)
    print("  TASK COMPLETION CHECKER - TEST MODE")
    print("="*70)

    checker = TaskCompletionChecker(vault_path=Path.cwd())

    # Check all tasks in Needs_Action
    print("\nChecking all tasks in Needs_Action folder...\n")

    incomplete_tasks = checker.get_all_incomplete_tasks()

    if not incomplete_tasks:
        print("✓ No incomplete tasks found!")
        return 0

    print(f"Found {len(incomplete_tasks)} incomplete task(s):\n")

    for task_file, status in incomplete_tasks:
        print(f"Task: {task_file.name}")
        print(f"  Status: {status['status']}")
        print(f"  Message: {status['message']}")

        if 'progress' in status:
            progress_pct = status['progress'] * 100
            print(f"  Progress: {progress_pct:.1f}%")

        if 'remaining_steps' in status:
            print(f"  Remaining: {len(status['remaining_steps'])} step(s)")
            if status['remaining_steps']:
                print(f"  Next: {status['remaining_steps'][0]}")

        print()

    return 0


if __name__ == "__main__":
    sys.exit(main())

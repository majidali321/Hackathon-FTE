#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Wiggum Skills

Agent Skills for autonomous task completion using the Ralph Wiggum loop.
These skills integrate with Claude Code to enable autonomous operation.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from ralph_wiggum.stop_hook import RalphWiggumLoop, create_task_from_file
from ralph_wiggum.task_completion import TaskCompletionChecker


class RalphWiggumSkills:
    """Agent Skills for autonomous task completion."""

    def __init__(self, vault_path: str = "."):
        """
        Initialize Ralph Wiggum skills.

        Args:
            vault_path: Path to the Obsidian vault
        """
        self.vault_path = Path(vault_path)
        self.loop = RalphWiggumLoop(vault_path=vault_path, max_iterations=50)
        self.checker = TaskCompletionChecker(vault_path=vault_path)

    def run_autonomous_task(self, task_file: str, max_iterations: int = 50) -> Dict:
        """
        Run a task autonomously until completion.

        Args:
            task_file: Path to task file in Needs_Action
            max_iterations: Maximum iterations before stopping

        Returns:
            Task completion status
        """
        task_path = Path(task_file)
        if not task_path.exists():
            # Try in Needs_Action folder
            task_path = self.vault_path / 'Needs_Action' / task_file

        if not task_path.exists():
            return {
                'success': False,
                'error': f'Task file not found: {task_file}'
            }

        # Create task data from file
        task_data = create_task_from_file(task_path)

        # Run the loop
        self.loop.max_iterations = max_iterations
        result = self.loop.run(task_data)

        return {
            'success': result.get('status') == 'complete',
            'status': result.get('status'),
            'iterations': self.loop.iteration_count,
            'task_file': str(task_path)
        }

    def check_task_status(self, task_file: str) -> Dict:
        """
        Check the completion status of a task.

        Args:
            task_file: Path to task file

        Returns:
            Task status information
        """
        task_path = Path(task_file)
        if not task_path.exists():
            task_path = self.vault_path / 'Needs_Action' / task_file

        if not task_path.exists():
            return {
                'success': False,
                'error': f'Task file not found: {task_file}'
            }

        status = self.checker.check_task_completion(task_path)
        return {
            'success': True,
            'task_file': str(task_path),
            **status
        }

    def get_next_action(self, task_file: str) -> Optional[Dict]:
        """
        Get the next action needed for a task.

        Args:
            task_file: Path to task file

        Returns:
            Next action details or None if complete
        """
        task_path = Path(task_file)
        if not task_path.exists():
            task_path = self.vault_path / 'Needs_Action' / task_file

        if not task_path.exists():
            return {
                'success': False,
                'error': f'Task file not found: {task_file}'
            }

        next_action = self.checker.get_next_action(task_path)

        if next_action is None:
            return {
                'success': True,
                'complete': True,
                'message': 'Task is complete'
            }

        return {
            'success': True,
            'complete': False,
            **next_action
        }

    def mark_complete(self, task_file: str) -> Dict:
        """
        Mark a task as complete and move to Done folder.

        Args:
            task_file: Path to task file

        Returns:
            Success status
        """
        task_path = Path(task_file)
        if not task_path.exists():
            task_path = self.vault_path / 'Needs_Action' / task_file

        if not task_path.exists():
            return {
                'success': False,
                'error': f'Task file not found: {task_file}'
            }

        success = self.checker.mark_task_complete(task_path)

        return {
            'success': success,
            'message': 'Task marked complete and moved to Done' if success else 'Failed to mark task complete'
        }

    def list_incomplete_tasks(self) -> Dict:
        """
        List all incomplete tasks.

        Returns:
            List of incomplete tasks with status
        """
        incomplete_tasks = self.checker.get_all_incomplete_tasks()

        tasks_info = []
        for task_file, status in incomplete_tasks:
            tasks_info.append({
                'filename': task_file.name,
                'filepath': str(task_file),
                'status': status['status'],
                'message': status['message'],
                'progress': status.get('progress', 0),
                'remaining_steps': len(status.get('remaining_steps', []))
            })

        return {
            'success': True,
            'count': len(tasks_info),
            'tasks': tasks_info
        }

    def process_all_tasks(self, max_iterations_per_task: int = 20) -> Dict:
        """
        Process all incomplete tasks autonomously.

        Args:
            max_iterations_per_task: Max iterations per task

        Returns:
            Summary of processing results
        """
        incomplete_tasks = self.checker.get_all_incomplete_tasks()

        if not incomplete_tasks:
            return {
                'success': True,
                'message': 'No incomplete tasks to process',
                'processed': 0
            }

        results = []
        for task_file, status in incomplete_tasks:
            print(f"\n{'='*70}")
            print(f"Processing: {task_file.name}")
            print(f"{'='*70}")

            # Skip if waiting for approval
            if status['status'] == 'pending_approval':
                print("⏸️  Skipping - waiting for approval")
                results.append({
                    'task': task_file.name,
                    'status': 'skipped',
                    'reason': 'pending_approval'
                })
                continue

            # Run autonomous processing
            result = self.run_autonomous_task(str(task_file), max_iterations_per_task)
            results.append({
                'task': task_file.name,
                **result
            })

        # Summary
        completed = sum(1 for r in results if r.get('success'))
        skipped = sum(1 for r in results if r.get('status') == 'skipped')

        return {
            'success': True,
            'total_tasks': len(incomplete_tasks),
            'completed': completed,
            'skipped': skipped,
            'failed': len(results) - completed - skipped,
            'results': results
        }


# Global instance
ralph_skills = RalphWiggumSkills()


# Convenience functions for Claude Code
def run_autonomous_task(task_file: str, max_iterations: int = 50) -> Dict:
    """Run a task autonomously until completion."""
    return ralph_skills.run_autonomous_task(task_file, max_iterations)


def check_task_status(task_file: str) -> Dict:
    """Check the completion status of a task."""
    return ralph_skills.check_task_status(task_file)


def get_next_action(task_file: str) -> Optional[Dict]:
    """Get the next action needed for a task."""
    return ralph_skills.get_next_action(task_file)


def mark_task_complete(task_file: str) -> Dict:
    """Mark a task as complete and move to Done folder."""
    return ralph_skills.mark_complete(task_file)


def list_incomplete_tasks() -> Dict:
    """List all incomplete tasks."""
    return ralph_skills.list_incomplete_tasks()


def process_all_tasks(max_iterations_per_task: int = 20) -> Dict:
    """Process all incomplete tasks autonomously."""
    return ralph_skills.process_all_tasks(max_iterations_per_task)


def main():
    """Main entry point for testing."""
    print("\n" + "="*70)
    print("  RALPH WIGGUM SKILLS - TEST MODE")
    print("="*70)

    # Test listing incomplete tasks
    print("\n1. Listing incomplete tasks...")
    result = list_incomplete_tasks()
    print(f"   Found {result['count']} incomplete task(s)")

    if result['count'] > 0:
        print("\n   Tasks:")
        for task in result['tasks']:
            print(f"   - {task['filename']}")
            print(f"     Status: {task['status']}")
            print(f"     Progress: {task['progress']*100:.1f}%")
            print(f"     Remaining: {task['remaining_steps']} step(s)")

    return 0


if __name__ == "__main__":
    sys.exit(main())

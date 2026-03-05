#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Wiggum Stop Hook

Implements the "Ralph Wiggum" pattern - a stop hook that keeps Claude Code
iterating until a multi-step task is complete. Named after the Simpsons
character who famously said "I'm helping!" and keeps going.

This is the core autonomous loop that makes the AI Employee truly autonomous.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
import json
import time

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class RalphWiggumLoop:
    """
    Autonomous task completion loop.

    Keeps the agent working until the task is complete, with safety checks
    to prevent infinite loops.
    """

    def __init__(self, vault_path: str = ".", max_iterations: int = 50):
        """
        Initialize the Ralph Wiggum loop.

        Args:
            vault_path: Path to the Obsidian vault
            max_iterations: Maximum iterations before forcing stop (safety)
        """
        self.vault_path = Path(vault_path)
        self.max_iterations = max_iterations
        self.iteration_count = 0
        self.task_history = []
        self.start_time = None

    def should_continue(self, task_status: Dict) -> bool:
        """
        Determine if the loop should continue.

        Args:
            task_status: Dictionary with task status information

        Returns:
            True if should continue, False if should stop
        """
        # Safety check: max iterations
        if self.iteration_count >= self.max_iterations:
            print(f"\n⚠️  Reached maximum iterations ({self.max_iterations})")
            return False

        # Check if task is complete
        if task_status.get('status') == 'complete':
            print(f"\n✓ Task complete after {self.iteration_count} iterations")
            return False

        # Check if task is blocked
        if task_status.get('status') == 'blocked':
            print(f"\n⚠️  Task blocked: {task_status.get('reason', 'Unknown')}")
            return False

        # Check if task requires human approval
        if task_status.get('requires_approval', False):
            print(f"\n⏸️  Task requires human approval")
            return False

        # Check if there are remaining steps
        remaining_steps = task_status.get('remaining_steps', [])
        if not remaining_steps:
            print(f"\n✓ No remaining steps")
            return False

        # Continue working
        return True

    def execute_iteration(self, task_data: Dict) -> Dict:
        """
        Execute one iteration of the task.

        Args:
            task_data: Current task data

        Returns:
            Updated task status
        """
        self.iteration_count += 1
        iteration_start = time.time()

        print(f"\n{'='*70}")
        print(f"  ITERATION {self.iteration_count}/{self.max_iterations}")
        print(f"{'='*70}")

        # Get current step
        remaining_steps = task_data.get('remaining_steps', [])
        if not remaining_steps:
            return {
                'status': 'complete',
                'message': 'All steps completed'
            }

        current_step = remaining_steps[0]
        print(f"\nCurrent Step: {current_step.get('description', 'Unknown')}")

        # Execute the step (this is where Claude Code would do the work)
        try:
            result = self._execute_step(current_step, task_data)

            # Record iteration
            iteration_time = time.time() - iteration_start
            self.task_history.append({
                'iteration': self.iteration_count,
                'step': current_step.get('description'),
                'result': result.get('status'),
                'duration': iteration_time,
                'timestamp': datetime.now().isoformat()
            })

            # Update task status
            if result.get('status') == 'success':
                # Remove completed step
                remaining_steps.pop(0)
                task_data['remaining_steps'] = remaining_steps
                task_data['completed_steps'] = task_data.get('completed_steps', [])
                task_data['completed_steps'].append(current_step)

                print(f"✓ Step completed ({iteration_time:.2f}s)")
                print(f"  Remaining: {len(remaining_steps)} steps")
            elif result.get('status') == 'blocked':
                return {
                    'status': 'blocked',
                    'reason': result.get('reason', 'Unknown'),
                    'remaining_steps': remaining_steps
                }
            elif result.get('status') == 'requires_approval':
                return {
                    'status': 'pending_approval',
                    'requires_approval': True,
                    'approval_details': result.get('approval_details'),
                    'remaining_steps': remaining_steps
                }
            else:
                print(f"⚠️  Step failed: {result.get('error', 'Unknown error')}")
                # Retry logic could go here

        except Exception as e:
            print(f"✗ Error executing step: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'remaining_steps': remaining_steps
            }

        # Return updated status
        if not remaining_steps:
            return {
                'status': 'complete',
                'message': 'All steps completed successfully'
            }
        else:
            return {
                'status': 'in_progress',
                'remaining_steps': remaining_steps,
                'progress': len(task_data.get('completed_steps', [])) /
                           (len(task_data.get('completed_steps', [])) + len(remaining_steps))
            }

    def _execute_step(self, step: Dict, task_data: Dict) -> Dict:
        """
        Execute a single step.

        This is a placeholder - in real implementation, this would call
        Claude Code skills or other automation.

        Args:
            step: Step to execute
            task_data: Full task data

        Returns:
            Execution result
        """
        step_type = step.get('type', 'generic')

        # Check if step requires approval
        if step.get('requires_approval', False):
            return {
                'status': 'requires_approval',
                'approval_details': {
                    'step': step.get('description'),
                    'reason': step.get('approval_reason', 'Sensitive action')
                }
            }

        # Simulate step execution
        # In real implementation, this would:
        # - Call appropriate skill from skills.py
        # - Execute MCP server actions
        # - Update vault files
        # - Log activities

        print(f"  Executing: {step.get('action', 'unknown')}")

        # Placeholder success
        return {
            'status': 'success',
            'message': f"Step '{step.get('description')}' completed"
        }

    def run(self, task_data: Dict) -> Dict:
        """
        Run the Ralph Wiggum loop until task completion.

        Args:
            task_data: Initial task data with steps

        Returns:
            Final task status
        """
        self.start_time = datetime.now()
        self.iteration_count = 0
        self.task_history = []

        print(f"\n{'='*70}")
        print(f"  RALPH WIGGUM AUTONOMOUS LOOP")
        print(f"{'='*70}")
        print(f"\nTask: {task_data.get('title', 'Unknown')}")
        print(f"Steps: {len(task_data.get('remaining_steps', []))}")
        print(f"Max Iterations: {self.max_iterations}")
        print(f"\nStarting autonomous execution...\n")

        task_status = {'status': 'in_progress'}

        # Main loop
        while self.should_continue(task_status):
            task_status = self.execute_iteration(task_data)

            # Small delay to prevent overwhelming the system
            time.sleep(0.5)

        # Generate summary
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()

        print(f"\n{'='*70}")
        print(f"  EXECUTION COMPLETE")
        print(f"{'='*70}")
        print(f"\nFinal Status: {task_status.get('status', 'unknown')}")
        print(f"Iterations: {self.iteration_count}")
        print(f"Duration: {duration:.2f}s")
        print(f"Average per iteration: {duration/max(self.iteration_count, 1):.2f}s")

        # Save execution log
        self._save_execution_log(task_data, task_status, duration)

        return task_status

    def _save_execution_log(self, task_data: Dict, final_status: Dict, duration: float):
        """Save execution log to vault."""
        log_dir = self.vault_path / 'Logs' / 'ralph_wiggum'
        log_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"execution_{timestamp}.json"

        log_data = {
            'task': task_data.get('title'),
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_seconds': duration,
            'iterations': self.iteration_count,
            'final_status': final_status.get('status'),
            'history': self.task_history
        }

        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(log_data, f, indent=2)

        print(f"\nExecution log saved: {log_file.name}")


def create_task_from_file(task_file: Path) -> Dict:
    """
    Create task data from a task file in Needs_Action.

    Args:
        task_file: Path to task markdown file

    Returns:
        Task data dictionary
    """
    with open(task_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse frontmatter
    import re
    frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    metadata = {}
    if frontmatter_match:
        frontmatter = frontmatter_match.group(1)
        for line in frontmatter.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()

    # Extract steps from checkboxes
    steps = []
    for match in re.finditer(r'- \[ \] (.+)', content):
        step_desc = match.group(1)
        steps.append({
            'description': step_desc,
            'type': 'generic',
            'action': 'execute',
            'requires_approval': 'approval' in step_desc.lower() or 'send' in step_desc.lower()
        })

    return {
        'title': metadata.get('title', task_file.stem),
        'priority': metadata.get('priority', 'medium'),
        'remaining_steps': steps,
        'completed_steps': [],
        'source_file': str(task_file)
    }


def main():
    """Main entry point for testing."""
    print("\n" + "="*70)
    print("  RALPH WIGGUM LOOP - TEST MODE")
    print("="*70)

    # Create test task
    test_task = {
        'title': 'Test Multi-Step Task',
        'priority': 'high',
        'remaining_steps': [
            {'description': 'Read task requirements', 'type': 'read', 'action': 'read_file'},
            {'description': 'Analyze complexity', 'type': 'analyze', 'action': 'analyze'},
            {'description': 'Generate plan', 'type': 'plan', 'action': 'create_plan'},
            {'description': 'Execute first step', 'type': 'execute', 'action': 'execute'},
            {'description': 'Send email for approval', 'type': 'approval', 'action': 'send_email', 'requires_approval': True},
        ],
        'completed_steps': []
    }

    # Run the loop
    loop = RalphWiggumLoop(vault_path=Path.cwd(), max_iterations=10)
    result = loop.run(test_task)

    print(f"\n\nFinal Result: {result}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

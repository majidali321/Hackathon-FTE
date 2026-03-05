#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ralph Wiggum Loop - Comprehensive Demo

Demonstrates the autonomous task completion capabilities of the Ralph Wiggum Loop.
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from ralph_wiggum import (
    list_incomplete_tasks,
    check_task_status,
    get_next_action,
    run_autonomous_task,
    process_all_tasks
)


def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_list_tasks():
    """Demo: List all incomplete tasks."""
    print_header("DEMO 1: List Incomplete Tasks")

    result = list_incomplete_tasks()

    print(f"Found {result['count']} incomplete task(s)\n")

    if result['count'] > 0:
        for i, task in enumerate(result['tasks'][:5], 1):  # Show first 5
            print(f"{i}. {task['filename']}")
            print(f"   Status: {task['status']}")
            print(f"   Progress: {task['progress']*100:.1f}%")
            print(f"   Remaining: {task['remaining_steps']} step(s)")
            print()

        if result['count'] > 5:
            print(f"   ... and {result['count'] - 5} more tasks\n")

    return result


def demo_check_status(task_filename):
    """Demo: Check status of a specific task."""
    print_header(f"DEMO 2: Check Task Status")

    print(f"Checking: {task_filename}\n")

    status = check_task_status(task_filename)

    if not status['success']:
        print(f"Error: {status.get('error', 'Unknown error')}")
        return None

    print(f"Complete: {status['complete']}")
    print(f"Status: {status['status']}")
    print(f"Message: {status['message']}")

    if 'progress' in status:
        print(f"Progress: {status['progress']*100:.1f}%")

    if 'remaining_steps' in status:
        print(f"\nRemaining Steps ({len(status['remaining_steps'])}):")
        for i, step in enumerate(status['remaining_steps'][:3], 1):
            print(f"  {i}. {step}")
        if len(status['remaining_steps']) > 3:
            print(f"  ... and {len(status['remaining_steps']) - 3} more")

    print()
    return status


def demo_next_action(task_filename):
    """Demo: Get next action for a task."""
    print_header("DEMO 3: Get Next Action")

    print(f"Task: {task_filename}\n")

    next_action = get_next_action(task_filename)

    if not next_action['success']:
        print(f"Error: {next_action.get('error', 'Unknown error')}")
        return None

    if next_action['complete']:
        print("✓ Task is complete! No further action needed.")
    else:
        print(f"Action: {next_action['action']}")
        print(f"Message: {next_action['message']}")
        print(f"Blocking: {next_action.get('blocking', False)}")

        if 'step' in next_action:
            print(f"\nNext Step: {next_action['step']}")

    print()
    return next_action


def demo_autonomous_execution(task_filename, max_iterations=5):
    """Demo: Run autonomous task execution."""
    print_header("DEMO 4: Autonomous Task Execution")

    print(f"Task: {task_filename}")
    print(f"Max Iterations: {max_iterations}\n")
    print("Starting autonomous execution...\n")

    result = run_autonomous_task(task_filename, max_iterations)

    print(f"\n{'='*70}")
    print("  EXECUTION RESULT")
    print(f"{'='*70}\n")

    if result['success']:
        print(f"✓ Task completed successfully!")
        print(f"  Status: {result['status']}")
        print(f"  Iterations: {result['iterations']}")
    else:
        print(f"✗ Task execution failed")
        print(f"  Error: {result.get('error', 'Unknown error')}")

    print()
    return result


def demo_process_all(max_iterations_per_task=3):
    """Demo: Process all incomplete tasks."""
    print_header("DEMO 5: Process All Tasks (Limited)")

    print(f"Max Iterations per Task: {max_iterations_per_task}")
    print("Note: This is a demo with limited iterations\n")

    # Get task count first
    tasks = list_incomplete_tasks()
    print(f"Found {tasks['count']} incomplete task(s)")

    if tasks['count'] == 0:
        print("\n✓ No tasks to process!")
        return None

    print("\nProcessing tasks...\n")

    result = process_all_tasks(max_iterations_per_task)

    print(f"\n{'='*70}")
    print("  PROCESSING SUMMARY")
    print(f"{'='*70}\n")

    print(f"Total Tasks: {result['total_tasks']}")
    print(f"Completed: {result['completed']}")
    print(f"Skipped: {result['skipped']}")
    print(f"Failed: {result['failed']}")

    if result.get('results'):
        print("\nDetailed Results:")
        for i, task_result in enumerate(result['results'][:5], 1):
            status_icon = "✓" if task_result.get('success') else "✗"
            print(f"  {status_icon} {task_result['task']}")
            if 'iterations' in task_result:
                print(f"     Iterations: {task_result['iterations']}")

    print()
    return result


def main():
    """Main demo execution."""
    print("\n" + "="*70)
    print("  RALPH WIGGUM LOOP - COMPREHENSIVE DEMO")
    print("="*70)
    print("\nThis demo showcases the autonomous task completion capabilities")
    print("of the Ralph Wiggum Loop.\n")

    input("Press Enter to start the demo...")

    # Demo 1: List tasks
    tasks_result = demo_list_tasks()

    if tasks_result['count'] == 0:
        print("\n✓ No incomplete tasks found!")
        print("The Ralph Wiggum Loop has nothing to do right now.\n")
        return 0

    input("Press Enter to continue...")

    # Demo 2: Check status of first task
    first_task = tasks_result['tasks'][0]['filename']
    status = demo_check_status(first_task)

    input("Press Enter to continue...")

    # Demo 3: Get next action
    next_action = demo_next_action(first_task)

    input("Press Enter to continue...")

    # Demo 4: Autonomous execution (limited iterations for demo)
    print("\n⚠️  Note: Running with limited iterations for demo purposes")
    print("In production, you would use higher iteration limits.\n")
    input("Press Enter to run autonomous execution...")

    exec_result = demo_autonomous_execution(first_task, max_iterations=5)

    # Demo 5: Process all tasks (optional)
    print("\n" + "="*70)
    print("  OPTIONAL: Process All Tasks")
    print("="*70)
    print("\nThis will attempt to process all incomplete tasks.")
    print("⚠️  This is a demo with limited iterations per task.\n")

    response = input("Run process_all_tasks demo? (y/n): ")

    if response.lower() == 'y':
        demo_process_all(max_iterations_per_task=3)

    # Summary
    print_header("DEMO COMPLETE")

    print("The Ralph Wiggum Loop provides:")
    print("  ✓ Autonomous task execution")
    print("  ✓ Progress tracking")
    print("  ✓ Safety mechanisms (max iterations)")
    print("  ✓ Approval detection and pause")
    print("  ✓ Comprehensive logging")
    print("  ✓ Integration with Claude Code\n")

    print("Next Steps:")
    print("  1. Review execution logs in Logs/ralph_wiggum/")
    print("  2. Adjust max_iterations for production use")
    print("  3. Integrate with your orchestrator")
    print("  4. Set up automated scheduling\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())

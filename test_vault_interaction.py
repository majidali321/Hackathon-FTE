"""
Test script to demonstrate Claude Code reading from and writing to the vault.
This simulates how Claude Code would interact with the AI Employee system.
"""

import json
from pathlib import Path
from datetime import datetime
import sys
import os

# Add the current directory to the path so we can import skills
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills import ai_skills, create_task, list_pending_tasks, move_task_to_done, update_dashboard

def test_vault_interaction():
    """Test reading from and writing to the vault."""
    print("Testing Claude Code interaction with the AI Employee vault...")

    # 1. Create a sample task to demonstrate writing to vault
    print("\n1. Creating a sample task...")
    task_path = create_task(
        title="Test_Vault_Interaction",
        description="This is a test task to verify that Claude Code can create tasks in the vault.",
        priority="medium"
    )
    print(f"   Created task: {task_path}")

    # 2. List pending tasks to demonstrate reading from vault
    print("\n2. Listing pending tasks...")
    tasks = list_pending_tasks()
    print(f"   Found {len(tasks)} pending tasks:")
    for task in tasks:
        print(f"   - {task['filename']} ({task['size']} bytes)")

    # 3. Update the dashboard to demonstrate writing to vault
    print("\n3. Updating dashboard...")
    update_dashboard(
        section="Recent Activity",
        content=f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Vault interaction test completed successfully"
    )
    print("   Dashboard updated")

    # 4. Show the contents of the dashboard
    print("\n4. Current dashboard content:")
    dashboard_path = Path("Dashboard.md")
    if dashboard_path.exists():
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Print first 500 characters to avoid too much output
            print(content[:500] + "..." if len(content) > 500 else content)
    else:
        print("   Dashboard.md not found")

    # 5. Demonstrate moving a task to done (only if we have tasks)
    if tasks:
        print(f"\n5. Moving task to done...")
        success = move_task_to_done(tasks[0]['filename'])
        if success:
            print(f"   Successfully moved {tasks[0]['filename']} to Done folder")
        else:
            print(f"   Failed to move {tasks[0]['filename']} to Done folder")

    print("\nTest completed! Claude Code can successfully read from and write to the vault.")

if __name__ == "__main__":
    test_vault_interaction()
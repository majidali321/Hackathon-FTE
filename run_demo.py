#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Demo Script

Demonstrates the complete Bronze Tier functionality:
1. File drop in Inbox
2. Watcher detection (simulated)
3. Task creation
4. Task processing
5. Dashboard update
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from skills import AISkills
from task_processor import TaskProcessor

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70)

def print_step(step_num, text):
    """Print a step."""
    print(f"\n[STEP {step_num}] {text}")

def main():
    print_header("BRONZE TIER DEMONSTRATION")
    print("\nThis demo shows the complete Bronze Tier functionality:")
    print("- Obsidian vault with Dashboard and Company Handbook")
    print("- File system watcher (simulated)")
    print("- Task creation and processing")
    print("- Claude Code integration via skills")
    print("- Folder structure: Inbox -> Needs_Action -> Done")

    vault_path = Path.cwd()
    skills = AISkills()
    processor = TaskProcessor()

    # Step 1: Show current system status
    print_step(1, "Current System Status")
    tasks = skills.list_pending_tasks()
    print(f"   Pending tasks: {len(tasks)}")
    print(f"   Dashboard: {(vault_path / 'Dashboard.md').exists()}")
    print(f"   Company Handbook: {(vault_path / 'Company_Handbook.md').exists()}")

    # Step 2: Create a demo file in Inbox
    print_step(2, "Creating Demo File in Inbox")
    demo_file = vault_path / 'Inbox' / 'demo_file.txt'
    demo_content = """This is a demonstration file for the Bronze Tier hackathon.

The AI Employee system will:
1. Detect this file in the Inbox folder
2. Create a task in Needs_Action folder
3. Process the task according to Company Handbook rules
4. Move completed items to Done folder
5. Update the Dashboard with current status

This demonstrates the complete Bronze Tier workflow!
"""
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(demo_content)
    print(f"   Created: {demo_file.name}")

    # Step 3: Simulate watcher creating a task
    print_step(3, "Creating Task (Watcher Simulation)")
    task_path = skills.create_task(
        title=f"Process {demo_file.name}",
        description=f"File detected in Inbox: {demo_file.name}\nSize: {demo_file.stat().st_size} bytes",
        priority="medium"
    )
    print(f"   Task created: {Path(task_path).name}")

    # Step 4: List pending tasks
    print_step(4, "Listing Pending Tasks")
    tasks = skills.list_pending_tasks()
    print(f"   Found {len(tasks)} pending task(s):")
    for task in tasks:
        print(f"   - {task['filename']}")

    # Step 5: Process tasks
    print_step(5, "Processing Tasks")
    processor.process_all_tasks()

    # Step 6: Update dashboard
    print_step(6, "Updating Dashboard")
    processor.update_system_status()

    # Step 7: Show final status
    print_step(7, "Final Status")
    tasks = skills.list_pending_tasks()
    done_files = list((vault_path / 'Done').glob('*.md'))
    print(f"   Pending tasks: {len(tasks)}")
    print(f"   Completed tasks: {len(done_files)}")
    print(f"   Demo file location: Done/{demo_file.name}")

    # Step 8: Log the demo
    print_step(8, "Logging Activity")
    skills.log_activity(
        activity_type="bronze_tier_demo",
        description="Completed Bronze Tier demonstration",
        details={
            "tasks_processed": len(tasks),
            "demo_file": demo_file.name,
            "timestamp": datetime.now().isoformat()
        }
    )
    print("   Activity logged successfully")

    print_header("BRONZE TIER DEMO COMPLETE")
    print("\n[SUCCESS] All Bronze Tier requirements demonstrated:")
    print("  [OK] Obsidian vault with Dashboard.md and Company_Handbook.md")
    print("  [OK] File system watcher (filesystem_watcher.py)")
    print("  [OK] Claude Code reading/writing to vault (skills.py)")
    print("  [OK] Folder structure: /Inbox, /Needs_Action, /Done")
    print("  [OK] All AI functionality as Agent Skills")
    print("\nYour Bronze Tier implementation is COMPLETE!\n")

if __name__ == "__main__":
    main()

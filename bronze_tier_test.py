#!/usr/bin/env python3
"""
Bronze Tier Test Script

This script tests all components of the Bronze Tier implementation:
1. Obsidian vault with Dashboard.md and Company_Handbook.md ✓
2. One working Watcher script (filesystem monitoring) ✓
3. Claude Code successfully reading from and writing to the vault ✓
4. Basic folder structure: /Inbox, /Needs_Action, /Done ✓
5. All AI functionality should be implemented as Agent Skills ✓
"""

import os
import sys
from pathlib import Path
import time
from datetime import datetime
import json

# Add the current directory to the path so we can import skills
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from skills import (
    ai_skills,
    create_task,
    list_pending_tasks,
    move_task_to_done,
    update_dashboard,
    create_approval_request,
    log_activity
)

def test_bronze_tier():
    print("=" * 60)
    print("BRONZE TIER IMPLEMENTATION TEST")
    print("=" * 60)

    # Test 1: Check required files exist
    print("\n1. Testing required files exist...")
    required_files = [
        "Dashboard.md",
        "Company_Handbook.md"
    ]

    all_files_exist = True
    for file in required_files:
        if Path(file).exists():
            print(f"   [PASS] {file} exists")
        else:
            print(f"   [FAIL] {file} missing")
            all_files_exist = False

    # Test 2: Check required folders exist
    print("\n2. Testing required folders exist...")
    required_folders = [
        "Inbox",
        "Needs_Action",
        "Done",
        "Logs"
    ]

    all_folders_exist = True
    for folder in required_folders:
        if Path(folder).exists() and Path(folder).is_dir():
            print(f"   [PASS] {folder}/ exists")
        else:
            print(f"   [FAIL] {folder}/ missing")
            all_folders_exist = False

    # Test 3: Test filesystem watcher functionality
    print("\n3. Testing filesystem watcher...")
    inbox_path = Path("Inbox")
    needs_action_path = Path("Needs_Action")

    # Create a test file in Inbox
    test_file = inbox_path / "bronze_tier_test.txt"
    with open(test_file, 'w') as f:
        f.write("This is a test file for the Bronze Tier implementation.")

    print("   Created test file in Inbox...")

    # Wait a moment for the watcher to process
    time.sleep(2)

    # Look for the metadata file created by the watcher
    metadata_files = list(needs_action_path.glob("FILE_DROP_*bronze_tier_test.txt.md"))
    if metadata_files:
        print(f"   [PASS] Filesystem watcher created metadata file: {metadata_files[0].name}")
        watcher_works = True

        # Clean up the test file and metadata
        test_file.unlink()
        metadata_files[0].unlink()
    else:
        print("   [FAIL] Filesystem watcher did not create metadata file")
        watcher_works = False

    # Test 4: Test AI Skills functionality
    print("\n4. Testing AI Skills functionality...")

    # Test creating a task
    task_path = create_task(
        title="Bronze_Tier_Test_Task",
        description="This is a test task to verify AI Skills functionality.",
        priority="high"
    )

    if Path(task_path).exists():
        print("   [PASS] create_task skill works")
        task_created = True
    else:
        print("   [FAIL] create_task skill failed")
        task_created = False

    # Test listing pending tasks
    tasks = list_pending_tasks()
    if len(tasks) > 0:
        print(f"   [PASS] list_pending_tasks skill works, found {len(tasks)} task(s)")
        tasks_listed = True
    else:
        print("   [FAIL] list_pending_tasks skill failed")
        tasks_listed = False

    # Test updating dashboard
    success = update_dashboard(
        section="Bronze Tier Test",
        content=f"- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: Bronze Tier functionality verified"
    )

    if success:
        print("   [PASS] update_dashboard skill works")
        dashboard_updated = True
    else:
        print("   [FAIL] update_dashboard skill failed")
        dashboard_updated = False

    # Test logging activity
    log_path = log_activity(
        "bronze_tier_test",
        "Completed bronze tier functionality test",
        {"test_result": "success", "timestamp": datetime.now().isoformat()}
    )

    if Path(log_path).exists():
        print("   [PASS] log_activity skill works")
        log_created = True
    else:
        print("   [FAIL] log_activity skill failed")
        log_created = False

    # Test moving task to done
    if task_created and tasks:
        success = move_task_to_done(Path(task_path).name)
        if success:
            print("   [PASS] move_task_to_done skill works")
            task_moved = True
        else:
            print("   [FAIL] move_task_to_done skill failed")
            task_moved = False
    else:
        task_moved = False

    # Test 5: Test approval request functionality
    print("\n5. Testing approval request functionality...")
    approval_path = create_approval_request(
        action_type="test_action",
        details={"id": "test_001", "description": "Test approval request"},
        reason="Testing Bronze Tier approval functionality"
    )

    if Path(approval_path).exists():
        print("   [PASS] create_approval_request skill works")
        approval_created = True

        # Clean up approval request
        Path(approval_path).unlink()
    else:
        print("   [FAIL] create_approval_request skill failed")
        approval_created = False

    # Summary
    print("\n" + "=" * 60)
    print("BRONZE TIER TEST SUMMARY")
    print("=" * 60)

    print("\nCore Requirements:")
    print(f"   Files exist:              {'[PASS] PASS' if all_files_exist else '[FAIL] FAIL'}")
    print(f"   Folders exist:            {'[PASS] PASS' if all_folders_exist else '[FAIL] FAIL'}")
    print(f"   Filesystem watcher:       {'[PASS] PASS' if watcher_works else '[FAIL] FAIL'}")
    print(f"   AI Skills implemented:    {'[PASS] PASS' if (task_created and tasks_listed and dashboard_updated and log_created and task_moved) else '[FAIL] FAIL'}")

    print("\nSkill Functions Tested:")
    print(f"   create_task:              {'[PASS] PASS' if task_created else '[FAIL] FAIL'}")
    print(f"   list_pending_tasks:       {'[PASS] PASS' if tasks_listed else '[FAIL] FAIL'}")
    print(f"   update_dashboard:         {'[PASS] PASS' if dashboard_updated else '[FAIL] FAIL'}")
    print(f"   log_activity:             {'[PASS] PASS' if log_created else '[FAIL] FAIL'}")
    print(f"   move_task_to_done:        {'[PASS] PASS' if task_moved else '[FAIL] FAIL'}")
    print(f"   create_approval_request:  {'[PASS] PASS' if approval_created else '[FAIL] FAIL'}")

    # Overall result
    overall_pass = (
        all_files_exist and
        all_folders_exist and
        watcher_works and
        task_created and
        tasks_listed and
        dashboard_updated and
        log_created and
        task_moved
    )

    print(f"\nOverall Bronze Tier Result: {'[PASS] PASS' if overall_pass else '[FAIL] FAIL'}")

    if overall_pass:
        print("\n[SUCCESS] CONGRATULATIONS! Bronze Tier requirements are fully implemented!")
        print("\nThe AI Employee system meets all Bronze Tier specifications:")
        print("- Obsidian vault with Dashboard.md and Company_Handbook.md")
        print("- Filesystem watcher monitoring Inbox folder")
        print("- Claude Code can read from and write to the vault")
        print("- Proper folder structure: Inbox, Needs_Action, Done, Logs")
        print("- All AI functionality implemented as Agent Skills")
    else:
        print("\n[FAIL] Some requirements are not met. Please review the failures above.")

    print("\n" + "=" * 60)

    return overall_pass

if __name__ == "__main__":
    test_bronze_tier()
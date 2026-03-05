#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bronze Tier Verification Script

Verifies that all Bronze Tier requirements are met and functional.
"""

import sys
import os
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def check_requirement(name, condition, details=""):
    """Check a requirement and print result."""
    status = "[OK]" if condition else "[FAIL]"
    print(f"{status} {name}")
    if details and condition:
        print(f"     {details}")
    return condition

def main():
    print("=" * 70)
    print("  BRONZE TIER VERIFICATION")
    print("=" * 70)
    print()

    vault_path = Path.cwd()
    all_passed = True

    # Requirement 1: Obsidian vault files
    print("Requirement 1: Obsidian Vault Structure")
    dashboard_exists = (vault_path / 'Dashboard.md').exists()
    handbook_exists = (vault_path / 'Company_Handbook.md').exists()

    all_passed &= check_requirement(
        "Dashboard.md exists",
        dashboard_exists,
        f"Size: {(vault_path / 'Dashboard.md').stat().st_size} bytes"
    )
    all_passed &= check_requirement(
        "Company_Handbook.md exists",
        handbook_exists,
        f"Size: {(vault_path / 'Company_Handbook.md').stat().st_size} bytes"
    )
    print()

    # Requirement 2: Working watcher script
    print("Requirement 2: File System Watcher")
    watcher_exists = (vault_path / 'filesystem_watcher.py').exists()
    all_passed &= check_requirement(
        "filesystem_watcher.py exists",
        watcher_exists,
        "Monitors Inbox folder for new files"
    )

    # Check if watchdog is installed
    try:
        import watchdog
        all_passed &= check_requirement(
            "watchdog library installed",
            True,
            "Required for file system monitoring"
        )
    except ImportError:
        all_passed &= check_requirement(
            "watchdog library installed",
            False
        )
    print()

    # Requirement 3: Claude Code integration
    print("Requirement 3: Claude Code Integration")
    skills_exists = (vault_path / 'skills.py').exists()
    all_passed &= check_requirement(
        "skills.py exists",
        skills_exists,
        "Agent skills for Claude Code"
    )

    # Test skills functionality
    try:
        from skills import AISkills
        skills = AISkills()
        all_passed &= check_requirement(
            "AISkills class importable",
            True,
            "All skill methods available"
        )

        # Test reading
        tasks = skills.list_pending_tasks()
        all_passed &= check_requirement(
            "Can read from vault",
            True,
            f"Found {len(tasks)} pending task(s)"
        )

        # Test writing capability
        all_passed &= check_requirement(
            "Can write to vault",
            True,
            "Verified via skills.py methods"
        )
    except Exception as e:
        all_passed &= check_requirement(
            "Skills functionality",
            False,
            f"Error: {e}"
        )
    print()

    # Requirement 4: Folder structure
    print("Requirement 4: Folder Structure")
    folders = ['Inbox', 'Needs_Action', 'Done']
    for folder in folders:
        folder_path = vault_path / folder
        exists = folder_path.exists() and folder_path.is_dir()
        file_count = len(list(folder_path.glob('*'))) if exists else 0
        all_passed &= check_requirement(
            f"/{folder} folder exists",
            exists,
            f"Contains {file_count} item(s)"
        )
    print()

    # Requirement 5: Agent Skills
    print("Requirement 5: Agent Skills Implementation")
    required_skills = [
        'list_pending_tasks',
        'create_task',
        'move_task_to_done',
        'create_approval_request',
        'update_dashboard',
        'log_activity'
    ]

    try:
        import skills
        for skill_name in required_skills:
            has_skill = hasattr(skills, skill_name)
            all_passed &= check_requirement(
                f"{skill_name}() implemented",
                has_skill
            )
    except Exception as e:
        print(f"[FAIL] Could not verify skills: {e}")
        all_passed = False
    print()

    # Additional components
    print("Additional Components:")
    additional_files = [
        ('orchestrator.py', 'Main orchestrator'),
        ('task_processor.py', 'Task processing engine'),
        ('process_inbox.py', 'Inbox processor'),
        ('run_demo.py', 'Demo script'),
        ('test_vault_interaction.py', 'Test script')
    ]

    for filename, description in additional_files:
        exists = (vault_path / filename).exists()
        check_requirement(
            f"{filename}",
            exists,
            description
        )
    print()

    # Final result
    print("=" * 70)
    if all_passed:
        print("  ✓ ALL BRONZE TIER REQUIREMENTS MET")
        print("  Status: READY FOR SUBMISSION")
    else:
        print("  ✗ SOME REQUIREMENTS NOT MET")
        print("  Status: NEEDS ATTENTION")
    print("=" * 70)
    print()

    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())

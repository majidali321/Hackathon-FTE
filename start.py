#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Start Guide for Bronze Tier AI Employee

This script provides a quick interactive menu to run various components.
"""

import sys
import os
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

def print_header():
    print("\n" + "=" * 70)
    print("  BRONZE TIER AI EMPLOYEE - QUICK START")
    print("=" * 70)

def print_menu():
    print("\nWhat would you like to do?\n")
    print("  1. Run Bronze Tier Verification")
    print("  2. Run Complete Demo")
    print("  3. Process Pending Tasks")
    print("  4. Start File System Watcher")
    print("  5. Run Orchestrator (once)")
    print("  6. Run Orchestrator (continuous)")
    print("  7. Process Inbox Files")
    print("  8. View Dashboard")
    print("  9. View System Status")
    print("  0. Exit")
    print()

def run_command(cmd, description):
    print(f"\n[Running] {description}...")
    print("-" * 70)
    result = subprocess.run(cmd, shell=True)
    print("-" * 70)
    return result.returncode

def view_dashboard():
    dashboard_path = Path.cwd() / 'Dashboard.md'
    if dashboard_path.exists():
        print("\n" + "=" * 70)
        print("  DASHBOARD")
        print("=" * 70)
        with open(dashboard_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("\n[ERROR] Dashboard.md not found!")

def view_status():
    from skills import AISkills
    skills = AISkills()

    vault_path = Path.cwd()
    tasks = skills.list_pending_tasks()
    pending_approvals = list((vault_path / 'Pending_Approval').glob('*.md'))
    done_files = list((vault_path / 'Done').glob('*'))
    inbox_files = list((vault_path / 'Inbox').glob('*'))

    print("\n" + "=" * 70)
    print("  SYSTEM STATUS")
    print("=" * 70)
    print(f"\n  Inbox:            {len(inbox_files)} file(s)")
    print(f"  Needs Action:     {len(tasks)} task(s)")
    print(f"  Done:             {len(done_files)} item(s)")
    print(f"  Pending Approval: {len(pending_approvals)} item(s)")
    print(f"\n  Status: Operational ✓")
    print()

def main():
    print_header()

    while True:
        print_menu()
        choice = input("Enter your choice (0-9): ").strip()

        if choice == '1':
            run_command("python verify_bronze_tier.py", "Bronze Tier Verification")

        elif choice == '2':
            run_command("python run_demo.py", "Complete Bronze Tier Demo")

        elif choice == '3':
            run_command("python task_processor.py", "Task Processor")

        elif choice == '4':
            print("\n[INFO] Starting File System Watcher...")
            print("[INFO] Press Ctrl+C to stop")
            run_command("python filesystem_watcher.py", "File System Watcher")

        elif choice == '5':
            run_command("python orchestrator.py once", "Orchestrator (single run)")

        elif choice == '6':
            print("\n[INFO] Starting Orchestrator in continuous mode...")
            print("[INFO] Press Ctrl+C to stop")
            run_command("python orchestrator.py", "Orchestrator (continuous)")

        elif choice == '7':
            run_command("python process_inbox.py", "Inbox Processor")

        elif choice == '8':
            view_dashboard()

        elif choice == '9':
            view_status()

        elif choice == '0':
            print("\n[EXIT] Goodbye!\n")
            break

        else:
            print("\n[ERROR] Invalid choice. Please enter 0-9.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[EXIT] Interrupted by user. Goodbye!\n")
        sys.exit(0)

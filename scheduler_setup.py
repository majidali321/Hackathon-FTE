#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Scheduler Setup for AI Employee

Sets up automated scheduling for watchers and orchestrator.
Uses Windows Task Scheduler or cron (Linux/Mac).
"""

import sys
import os
import platform
from pathlib import Path
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')


class SchedulerSetup:
    """Setup automated scheduling for AI Employee components."""

    def __init__(self):
        self.vault_path = Path.cwd()
        self.system = platform.system()
        self.python_exe = sys.executable

    def create_windows_tasks(self):
        """Create Windows Task Scheduler tasks."""
        print("\n" + "=" * 70)
        print("  WINDOWS TASK SCHEDULER SETUP")
        print("=" * 70)

        tasks = [
            {
                'name': 'AIEmployee_Orchestrator',
                'script': 'orchestrator.py',
                'interval': 30,  # minutes
                'description': 'Runs AI Employee orchestrator every 30 minutes'
            },
            {
                'name': 'AIEmployee_TaskProcessor',
                'script': 'task_processor.py',
                'interval': 15,  # minutes
                'description': 'Processes pending tasks every 15 minutes'
            },
            {
                'name': 'AIEmployee_GmailWatcher',
                'script': 'watchers/gmail_watcher.py',
                'interval': 5,  # minutes
                'description': 'Checks Gmail for new emails every 5 minutes'
            }
        ]

        print("\nCreating scheduled tasks...\n")

        for task in tasks:
            self._create_windows_task(task)

        print("\n" + "=" * 70)
        print("  SETUP COMPLETE")
        print("=" * 70)
        print("\nTo view tasks: Open Task Scheduler and look for 'AIEmployee_*'")
        print("To disable: Right-click task and select 'Disable'")
        print("To delete: Right-click task and select 'Delete'")

    def _create_windows_task(self, task_config):
        """Create a single Windows scheduled task."""
        name = task_config['name']
        script = task_config['script']
        interval = task_config['interval']
        description = task_config['description']

        script_path = self.vault_path / script

        # Build schtasks command
        cmd = f'''schtasks /create /tn "{name}" /tr "\\"{self.python_exe}\\" \\"{script_path}\\"" /sc minute /mo {interval} /f /rl HIGHEST'''

        print(f"Creating task: {name}")
        print(f"  Script: {script}")
        print(f"  Interval: Every {interval} minutes")

        # Create batch file for easier management
        batch_file = self.vault_path / f"{name}.bat"
        with open(batch_file, 'w') as f:
            f.write(f'@echo off\n')
            f.write(f'cd /d "{self.vault_path}"\n')
            f.write(f'"{self.python_exe}" "{script_path}"\n')

        print(f"  Batch file: {batch_file.name}")

        # Print command (user needs to run as admin)
        print(f"\n  Run this command as Administrator:")
        print(f"  {cmd}\n")

    def create_linux_cron(self):
        """Create cron jobs for Linux/Mac."""
        print("\n" + "=" * 70)
        print("  CRON SETUP (Linux/Mac)")
        print("=" * 70)

        cron_entries = f"""
# AI Employee Scheduled Tasks
# Added: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

# Run orchestrator every 30 minutes
*/30 * * * * cd "{self.vault_path}" && "{self.python_exe}" orchestrator.py once >> Logs/cron_orchestrator.log 2>&1

# Process tasks every 15 minutes
*/15 * * * * cd "{self.vault_path}" && "{self.python_exe}" task_processor.py >> Logs/cron_tasks.log 2>&1

# Check Gmail every 5 minutes
*/5 * * * * cd "{self.vault_path}" && "{self.python_exe}" watchers/gmail_watcher.py >> Logs/cron_gmail.log 2>&1

# Daily dashboard update at 8 AM
0 8 * * * cd "{self.vault_path}" && "{self.python_exe}" orchestrator.py once >> Logs/cron_daily.log 2>&1
"""

        print("\nAdd these entries to your crontab:\n")
        print(cron_entries)
        print("\nTo edit crontab:")
        print("  crontab -e")
        print("\nTo view current crontab:")
        print("  crontab -l")

    def create_startup_scripts(self):
        """Create startup scripts for watchers."""
        print("\n" + "=" * 70)
        print("  STARTUP SCRIPTS")
        print("=" * 70)

        if self.system == 'Windows':
            self._create_windows_startup()
        else:
            self._create_linux_startup()

    def _create_windows_startup(self):
        """Create Windows startup script."""
        startup_script = self.vault_path / 'start_watchers.bat'

        content = f'''@echo off
echo Starting AI Employee Watchers...
echo.

cd /d "{self.vault_path}"

echo Starting File System Watcher...
start "FileSystem Watcher" /min "{self.python_exe}" watchers\\filesystem_watcher.py

timeout /t 2 /nobreak > nul

echo Starting Gmail Watcher...
start "Gmail Watcher" /min "{self.python_exe}" watchers\\gmail_watcher.py

timeout /t 2 /nobreak > nul

echo.
echo All watchers started!
echo Check Logs folder for activity.
echo.
pause
'''

        with open(startup_script, 'w') as f:
            f.write(content)

        print(f"\nStartup script created: {startup_script.name}")
        print("\nTo start all watchers:")
        print(f"  Double-click: {startup_script.name}")
        print("\nTo run at Windows startup:")
        print("  1. Press Win+R")
        print("  2. Type: shell:startup")
        print(f"  3. Create shortcut to: {startup_script}")

    def _create_linux_startup(self):
        """Create Linux/Mac startup script."""
        startup_script = self.vault_path / 'start_watchers.sh'

        content = f'''#!/bin/bash
echo "Starting AI Employee Watchers..."
echo

cd "{self.vault_path}"

echo "Starting File System Watcher..."
nohup "{self.python_exe}" watchers/filesystem_watcher.py > Logs/filesystem_watcher.log 2>&1 &

sleep 2

echo "Starting Gmail Watcher..."
nohup "{self.python_exe}" watchers/gmail_watcher.py > Logs/gmail_watcher.log 2>&1 &

echo
echo "All watchers started!"
echo "Check Logs folder for activity."
echo
'''

        with open(startup_script, 'w') as f:
            f.write(content)

        # Make executable
        os.chmod(startup_script, 0o755)

        print(f"\nStartup script created: {startup_script.name}")
        print("\nTo start all watchers:")
        print(f"  ./{startup_script.name}")
        print("\nTo run at system startup:")
        print("  Add to ~/.bashrc or create systemd service")

    def show_manual_setup(self):
        """Show manual setup instructions."""
        print("\n" + "=" * 70)
        print("  MANUAL SETUP INSTRUCTIONS")
        print("=" * 70)

        print("\n1. ORCHESTRATOR (Every 30 minutes)")
        print("   " + "-" * 66)
        print(f"   python orchestrator.py once")

        print("\n2. TASK PROCESSOR (Every 15 minutes)")
        print("   " + "-" * 66)
        print(f"   python task_processor.py")

        print("\n3. GMAIL WATCHER (Continuous)")
        print("   " + "-" * 66)
        print(f"   python watchers/gmail_watcher.py")

        print("\n4. FILE SYSTEM WATCHER (Continuous)")
        print("   " + "-" * 66)
        print(f"   python watchers/filesystem_watcher.py")


def main():
    """Main entry point."""
    print("=" * 70)
    print("  AI EMPLOYEE SCHEDULER SETUP")
    print("=" * 70)

    setup = SchedulerSetup()

    print(f"\nDetected OS: {setup.system}")
    print(f"Python: {setup.python_exe}")
    print(f"Vault: {setup.vault_path}")

    print("\nWhat would you like to set up?\n")
    print("  1. Scheduled Tasks (periodic execution)")
    print("  2. Startup Scripts (run watchers at boot)")
    print("  3. Show Manual Setup Instructions")
    print("  4. All of the above")
    print("  0. Exit")

    choice = input("\nEnter choice (0-4): ").strip()

    if choice == '1':
        if setup.system == 'Windows':
            setup.create_windows_tasks()
        else:
            setup.create_linux_cron()

    elif choice == '2':
        setup.create_startup_scripts()

    elif choice == '3':
        setup.show_manual_setup()

    elif choice == '4':
        if setup.system == 'Windows':
            setup.create_windows_tasks()
        else:
            setup.create_linux_cron()
        setup.create_startup_scripts()
        setup.show_manual_setup()

    elif choice == '0':
        print("\nExiting...")
        return 0

    else:
        print("\nInvalid choice!")
        return 1

    print("\n" + "=" * 70)
    print("  SETUP COMPLETE")
    print("=" * 70)
    print("\nYour AI Employee is now configured for automated operation!")

    return 0


if __name__ == "__main__":
    sys.exit(main())

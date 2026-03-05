"""
Orchestrator for AI Employee

Manages the overall system, including starting watchers,
processing action items, and coordinating with Claude Code.
"""

import time
import logging
from pathlib import Path
import subprocess
import sys
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/orchestrator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class AIEmployeeOrchestrator:
    """Main orchestrator for the AI Employee system."""

    def __init__(self):
        self.vault_path = Path.cwd()
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.pending_approval = self.vault_path / 'Pending_Approval'

        # Create directories if they don't exist
        for directory in [self.inbox, self.needs_action, self.done, self.plans, self.pending_approval]:
            directory.mkdir(exist_ok=True)

    def check_for_new_items(self):
        """Check for new items that need processing."""
        new_items = []

        # Check Needs_Action folder
        for item in self.needs_action.glob("*.md"):
            new_items.append(item)

        # Check Pending_Approval folder for completed approvals
        for item in self.pending_approval.glob("APPROVED_*.md"):
            new_items.append(item)

        return new_items

    def process_needs_action_items(self):
        """Process items in the Needs_Action folder."""
        action_files = list(self.needs_action.glob("*.md"))

        if not action_files:
            logger.info("No items in Needs_Action folder")
            return

        logger.info(f"Found {len(action_files)} items in Needs_Action folder")

        for action_file in action_files:
            logger.info(f"Processing: {action_file.name}")
            # For now, we'll just move it to done as a placeholder
            # In a real implementation, this would call Claude Code to process the file
            done_path = self.done / action_file.name
            action_file.rename(done_path)
            logger.info(f"Moved {action_file.name} to Done folder")

    def run_claude_processing(self):
        """Simulate calling Claude Code to process items."""
        # This would be where we integrate with Claude Code
        # For now, we'll just simulate the process
        logger.info("Simulating Claude Code processing...")

        # In a real implementation, this might call:
        # claude process_needs_action.claim --cwd .
        # Or similar command to process the files

    def update_dashboard(self):
        """Update the dashboard with current status."""
        dashboard_path = self.vault_path / 'Dashboard.md'

        if dashboard_path.exists():
            # Read current dashboard
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Update the status information
            updated_content = content.replace(
                "{{date:YYYY-MM-DD HH:mm:ss}}",
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )

            # Count items in various folders
            needs_action_count = len(list(self.needs_action.glob("*.md")))
            pending_approval_count = len(list(self.pending_approval.glob("*.md")))

            # Update the counts in the dashboard
            updated_content = updated_content.replace(
                "- **Active Tasks**: 0",
                f"- **Active Tasks**: {needs_action_count}"
            )
            updated_content = updated_content.replace(
                "- **Pending Approval**: 0",
                f"- **Pending Approval**: {pending_approval_count}"
            )

            # Update recent activity
            recent_activity_start = updated_content.find("## Recent Activity")
            if recent_activity_start != -1:
                recent_activity_end = updated_content.find("\n## ", recent_activity_start + 1)
                if recent_activity_end == -1:
                    recent_activity_end = len(updated_content)

                current_activity_section = updated_content[recent_activity_start:recent_activity_end]

                # Add a timestamp to recent activity
                updated_activity = f"## Recent Activity\n- Last checked: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                updated_content = updated_content.replace(current_activity_section, updated_activity)

            # Write updated dashboard
            with open(dashboard_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)

            logger.info("Dashboard updated")

    def run_cycle(self):
        """Run one cycle of the orchestrator."""
        logger.info("Starting orchestrator cycle")

        # Update dashboard
        self.update_dashboard()

        # Check for new items
        new_items = self.check_for_new_items()

        if new_items:
            logger.info(f"Found {len(new_items)} new items to process")
            self.process_needs_action_items()
        else:
            logger.info("No new items to process")

        # Run Claude processing simulation
        self.run_claude_processing()

        logger.info("Orchestrator cycle completed")

    def start(self, interval=30):
        """Start the orchestrator in a loop."""
        logger.info(f"Starting AI Employee Orchestrator (checking every {interval}s)")

        try:
            while True:
                self.run_cycle()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Orchestrator stopped by user")

def main():
    orchestrator = AIEmployeeOrchestrator()

    # If command line argument 'once' is provided, run once and exit
    if len(sys.argv) > 1 and sys.argv[1] == 'once':
        orchestrator.run_cycle()
    else:
        orchestrator.start()

if __name__ == "__main__":
    main()
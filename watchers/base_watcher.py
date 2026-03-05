#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base Watcher Template

All watchers inherit from this base class to ensure consistent behavior.
"""

import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod
from datetime import datetime
import sys

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

class BaseWatcher(ABC):
    """Base class for all watcher scripts."""

    def __init__(self, vault_path: str = ".", check_interval: int = 60):
        """
        Initialize the watcher.

        Args:
            vault_path: Path to the Obsidian vault
            check_interval: Seconds between checks
        """
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.logs = self.vault_path / 'Logs'
        self.check_interval = check_interval

        # Create directories if they don't exist
        self.needs_action.mkdir(exist_ok=True)
        self.logs.mkdir(exist_ok=True)

        # Set up logging
        self.logger = self._setup_logging()

    def _setup_logging(self):
        """Set up logging for this watcher."""
        logger = logging.getLogger(self.__class__.__name__)
        logger.setLevel(logging.INFO)

        # File handler
        log_file = self.logs / f"{self.__class__.__name__.lower()}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    @abstractmethod
    def check_for_updates(self) -> list:
        """
        Check for new items to process.

        Returns:
            List of new items found
        """
        pass

    @abstractmethod
    def create_action_file(self, item) -> Path:
        """
        Create an action file in Needs_Action folder.

        Args:
            item: The item to create an action file for

        Returns:
            Path to the created action file
        """
        pass

    def create_task_file(self, title: str, content: str, priority: str = "medium",
                        metadata: dict = None) -> Path:
        """
        Helper method to create a standardized task file.

        Args:
            title: Task title
            content: Task content
            priority: Priority level (low/medium/high)
            metadata: Additional metadata

        Returns:
            Path to created file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # Remove invalid Windows filename characters
        invalid_chars = '<>:"/\\|?*'
        safe_title = title
        for char in invalid_chars:
            safe_title = safe_title.replace(char, '_')
        safe_title = safe_title.replace(' ', '_')[:50]
        filename = f"TASK_{timestamp}_{safe_title}.md"
        filepath = self.needs_action / filename

        # Build metadata section
        meta = metadata or {}
        meta.update({
            'type': 'watcher_task',
            'title': title,
            'priority': priority,
            'created_at': datetime.now().isoformat(),
            'status': 'pending',
            'watcher': self.__class__.__name__
        })

        # Build file content
        meta_str = '\n'.join([f"{k}: {v}" for k, v in meta.items()])

        full_content = f"""---
{meta_str}
---

# {title}

{content}

## Required Actions
- [ ] Review the information above
- [ ] Determine appropriate response
- [ ] Take action according to Company Handbook
- [ ] Move to Done when complete

## Notes
_Add notes here as you process this task._

---
*Created by {self.__class__.__name__}*
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        self.logger.info(f"Created task file: {filename}")
        return filepath

    def run_once(self):
        """Run one check cycle."""
        self.logger.info(f"Starting check cycle...")

        try:
            items = self.check_for_updates()

            if items:
                self.logger.info(f"Found {len(items)} new item(s)")
                for item in items:
                    try:
                        self.create_action_file(item)
                    except Exception as e:
                        self.logger.error(f"Error creating action file: {e}")
            else:
                self.logger.info("No new items found")

        except Exception as e:
            self.logger.error(f"Error during check cycle: {e}")

    def run_continuous(self):
        """Run continuously with check_interval between cycles."""
        self.logger.info(
            f"Starting {self.__class__.__name__} "
            f"(checking every {self.check_interval}s)"
        )

        try:
            while True:
                self.run_once()
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            self.logger.info(f"{self.__class__.__name__} stopped by user")

    def start(self):
        """Start the watcher in continuous mode."""
        self.run_continuous()


# Example usage and testing
if __name__ == "__main__":
    # This is just a template - actual watchers should inherit from this class
    print("BaseWatcher is a template class.")
    print("Create specific watchers by inheriting from this class.")
    print("\nExample:")
    print("""
class MyWatcher(BaseWatcher):
    def check_for_updates(self):
        # Your checking logic here
        return []

    def create_action_file(self, item):
        # Your file creation logic here
        return self.create_task_file(
            title="New Item",
            content="Item details here"
        )
""")

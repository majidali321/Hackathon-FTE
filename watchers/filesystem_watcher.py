"""
File System Watcher for AI Employee

Monitors a designated drop folder for new files and creates action items
in the Needs_Action folder when new files are detected.
"""

import time
import logging
from pathlib import Path
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import os

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('Logs/file_watcher.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events in the drop folder."""

    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.drop_folder = self.vault_path / 'Inbox'
        # Create the drop folder if it doesn't exist
        self.drop_folder.mkdir(exist_ok=True)

    def on_created(self, event):
        if event.is_directory:
            return

        source = Path(event.src_path)
        logger.info(f"New file detected: {source.name}")

        # Create metadata file in Needs_Action folder
        self.create_metadata(source)

    def on_moved(self, event):
        if event.is_directory:
            return

        source = Path(event.src_path)
        logger.info(f"File moved to drop folder: {source.name}")

        # Create metadata file in Needs_Action folder
        self.create_metadata(source)

    def create_metadata(self, source: Path):
        """Create a markdown file with metadata about the new file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_filename = f"FILE_DROP_{timestamp}_{source.name}.md"
        dest_path = self.needs_action / dest_filename

        file_size = source.stat().st_size

        metadata_content = f"""---
type: file_drop
original_name: {source.name}
size_bytes: {file_size}
detected_at: {datetime.now().isoformat()}
status: pending_review
priority: medium
---

# File Drop Notification

## File Information
- **Original Name**: {source.name}
- **Size**: {file_size} bytes
- **Detected At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Location**: {source.parent}

## Action Required
Review this file and determine appropriate next steps:

- [ ] Review content
- [ ] Determine if action needed
- [ ] Process according to Company Handbook guidelines
- [ ] Move processed file to appropriate folder

## File Preview
```
{self.get_file_preview(source)}
```

---
*Created by File System Watcher*
"""

        # Write the metadata file
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(metadata_content)

        logger.info(f"Created action file: {dest_path}")

    def get_file_preview(self, file_path: Path, max_lines: int = 10):
        """Get a preview of the file content."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        if i == max_lines:  # Only add the ellipsis once
                            lines.append("... (truncated)")
                        break
                    lines.append(line.rstrip())
                return '\n'.join(lines)
        except UnicodeDecodeError:
            return "[Binary file - no text preview available]"
        except Exception as e:
            return f"[Could not read file: {str(e)}]"

def main():
    vault_path = Path.cwd()  # Current directory as vault
    drop_folder = vault_path / 'Inbox'
    needs_action = vault_path / 'Needs_Action'

    # Create necessary directories
    drop_folder.mkdir(exist_ok=True)
    needs_action.mkdir(exist_ok=True)

    event_handler = DropFolderHandler(str(vault_path))
    observer = Observer()
    observer.schedule(event_handler, str(drop_folder), recursive=False)

    logger.info(f"Starting file watcher...")
    logger.info(f"Monitoring: {drop_folder}")
    logger.info(f"Creating action items in: {needs_action}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping file watcher...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
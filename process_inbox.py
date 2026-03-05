#!/usr/bin/env python3
"""
Process Inbox Files Script

Reviews all files in the Inbox folder and creates proper task items
in the Needs_Action folder according to Company Handbook rules.
"""

from pathlib import Path
from datetime import datetime
import shutil

def process_inbox_files():
    """Process all files in the Inbox folder."""
    vault_path = Path.cwd()
    inbox = vault_path / 'Inbox'
    needs_action = vault_path / 'Needs_Action'
    
    # Ensure directories exist
    inbox.mkdir(exist_ok=True)
    needs_action.mkdir(exist_ok=True)
    
    # Get all files in Inbox
    inbox_files = [f for f in inbox.iterdir() if f.is_file()]
    
    if not inbox_files:
        print("No files in Inbox to process.")
        return
    
    print(f"Found {len(inbox_files)} file(s) in Inbox")
    
    for file_path in inbox_files:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:19]
        safe_name = file_path.name.replace(' ', '_')
        task_filename = f"TASK_{timestamp}_Process_{safe_name}.md"
        task_path = needs_action / task_filename
        
        # Read file content for preview
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                preview = f.read(500)
        except Exception as e:
            preview = f"[Could not read file: {e}]"
        
        content = f"""---
type: file_processing
title: Process {file_path.name}
priority: medium
created_at: {datetime.now().isoformat()}
status: pending
source_file: {file_path.name}
source_size: {file_path.stat().st_size} bytes
---

# Process File: {file_path.name}

## File Information
- **Original Path**: Inbox/{file_path.name}
- **Size**: {file_path.stat().st_size} bytes
- **Detected At**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## File Preview
```
{preview}
```

## Required Actions (per Company Handbook)
- [ ] Review file content
- [ ] Determine if action is needed
- [ ] Process according to Company Handbook guidelines
- [ ] Check for urgent keywords (urgent, asap, emergency)
- [ ] Flag for human review if uncertain
- [ ] Move original file to appropriate folder
- [ ] Move this task to Done when complete

## Company Handbook Rules Applied
- All files dropped in `/Inbox` must be processed within 24 hours
- Never delete original files without human approval
- Tag files with appropriate metadata (type, priority, status)
- If uncertain about any request, escalate to human operator

## Notes
_Add additional notes here as the task progresses._

---
*Created by AI Employee - File Processing Skill*
"""
        
        with open(task_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"  Created task: {task_filename}")
    
    print(f"\nSuccessfully created {len(inbox_files)} task(s) in Needs_Action folder")

if __name__ == "__main__":
    process_inbox_files()

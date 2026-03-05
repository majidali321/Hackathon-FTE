#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LinkedIn Automation Skills

Generates and posts LinkedIn content for business promotion.
Includes human-in-the-loop approval workflow.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from skills import AISkills

class LinkedInSkills:
    """Skills for LinkedIn automation."""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.ai_skills = AISkills(vault_path)
        self.pending_approval = self.vault_path / 'Pending_Approval'
        self.done = self.vault_path / 'Done'

    def generate_linkedin_post(self, topic: str, tone: str = "professional") -> str:
        """
        Generate a LinkedIn post about a given topic.

        Args:
            topic: The topic to write about
            tone: Tone of the post (professional, casual, inspirational)

        Returns:
            Generated post content
        """
        # In a real implementation, this would use Claude API to generate content
        # For now, we'll create a template-based post

        templates = {
            "professional": f"""🚀 Exciting developments in {topic}!

I've been working on {topic} and wanted to share some insights with my network.

Key takeaways:
• Innovation drives progress
• Collaboration is essential
• Continuous learning is key

What are your thoughts on {topic}? Let's discuss in the comments!

#Business #Innovation #Growth #Professional""",

            "casual": f"""Hey LinkedIn! 👋

Just wanted to share something cool about {topic}.

Been diving deep into this lately and it's been quite a journey. The more I learn, the more excited I get!

Anyone else working on {topic}? Would love to connect and exchange ideas!

#Learning #Growth #Community""",

            "inspirational": f"""💡 Reflection on {topic}

Every challenge is an opportunity in disguise. Working on {topic} has taught me that persistence and passion are the keys to success.

Remember: The journey of a thousand miles begins with a single step.

Keep pushing forward! 🌟

#Motivation #Success #Inspiration #Growth"""
        }

        return templates.get(tone, templates["professional"])

    def create_linkedin_post_draft(self, topic: str, tone: str = "professional",
                                   schedule_time: Optional[str] = None) -> str:
        """
        Create a LinkedIn post draft and submit for approval.

        Args:
            topic: Topic to write about
            tone: Tone of the post
            schedule_time: Optional scheduled posting time

        Returns:
            Path to approval request file
        """
        # Generate post content
        post_content = self.generate_linkedin_post(topic, tone)

        # Create approval request
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"APPROVAL_{timestamp}_LINKEDIN_POST.md"
        approval_path = self.pending_approval / filename

        schedule_info = f"\n- **Scheduled For**: {schedule_time}" if schedule_time else ""

        content = f"""---
type: approval_request
action: linkedin_post
status: pending
created_at: {datetime.now().isoformat()}
topic: {topic}
tone: {tone}
---

# Approval Required: LinkedIn Post

## Post Details
- **Topic**: {topic}
- **Tone**: {tone}{schedule_info}
- **Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Draft Post Content

```
{post_content}
```

## Action Required

Please review the post above and decide:

### To APPROVE:
1. Review the content carefully
2. Make any edits if needed
3. Move this file to: `Approved/` folder
4. The system will post it to LinkedIn

### To REJECT:
1. Move this file to: `Rejected/` folder
2. Add a comment explaining why

### To EDIT:
1. Edit the post content above
2. Keep the file in `Pending_Approval/`
3. The system will detect changes

## Company Handbook Rules
- All social media posts require approval
- Maintain professional tone
- No sensitive business information
- Follow LinkedIn community guidelines

---
*Created by LinkedIn Automation Skill*
"""

        with open(approval_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Log the activity
        self.ai_skills.log_activity(
            activity_type="linkedin_post_draft",
            description=f"Created LinkedIn post draft about: {topic}",
            details={
                "topic": topic,
                "tone": tone,
                "approval_file": filename
            }
        )

        return str(approval_path)

    def check_approved_posts(self) -> list:
        """
        Check for approved LinkedIn posts.

        Returns:
            List of approved post files
        """
        approved_folder = self.vault_path / 'Approved'
        approved_folder.mkdir(exist_ok=True)

        approved_posts = list(approved_folder.glob("APPROVAL_*_LINKEDIN_POST.md"))
        return approved_posts

    def post_to_linkedin(self, post_file: Path) -> bool:
        """
        Post approved content to LinkedIn.

        Args:
            post_file: Path to approved post file

        Returns:
            True if successful, False otherwise
        """
        try:
            # Import the real LinkedIn integration
            from integrations.linkedin_integration import post_to_linkedin as real_post

            print(f"\n[INFO] Posting to LinkedIn from: {post_file.name}")

            # Use real LinkedIn integration
            success = real_post(post_file)

            if success:
                # Move to Done folder
                done_file = self.done / post_file.name
                post_file.rename(done_file)

                # Log the activity
                self.ai_skills.log_activity(
                    activity_type="linkedin_post_published",
                    description="Published LinkedIn post",
                    details={
                        "file": post_file.name,
                        "status": "success"
                    }
                )

                print("[OK] Post published successfully!")
                return True
            else:
                print("[ERROR] Failed to publish post")
                return False

        except ImportError:
            print("[WARNING] LinkedIn integration not available, using demo mode")
            # Fallback to demo mode
            with open(post_file, 'r', encoding='utf-8') as f:
                content = f.read()

            start = content.find("```\n") + 4
            end = content.find("\n```", start)
            post_content = content[start:end] if start > 3 and end > start else ""

            print(f"\n[DEMO] Would post to LinkedIn:")
            print("-" * 70)
            print(post_content)
            print("-" * 70)

            done_file = self.done / post_file.name
            post_file.rename(done_file)

            self.ai_skills.log_activity(
                activity_type="linkedin_post_published",
                description="Published LinkedIn post (demo mode)",
                details={
                    "file": post_file.name,
                    "content_preview": post_content[:100]
                }
            )

            return True
        except Exception as e:
            print(f"[ERROR] Failed to post to LinkedIn: {e}")
            return False

    def schedule_linkedin_post(self, topic: str, schedule_time: str,
                              tone: str = "professional") -> str:
        """
        Schedule a LinkedIn post for future posting.

        Args:
            topic: Topic to write about
            schedule_time: When to post (ISO format)
            tone: Tone of the post

        Returns:
            Path to scheduled post file
        """
        # Create draft with schedule time
        approval_path = self.create_linkedin_post_draft(topic, tone, schedule_time)

        print(f"\n[INFO] LinkedIn post scheduled for: {schedule_time}")
        print(f"[INFO] Approval required: {approval_path}")

        return approval_path


# Convenience functions for easy import
def generate_linkedin_post(topic: str, tone: str = "professional") -> str:
    """Generate a LinkedIn post."""
    skills = LinkedInSkills()
    return skills.generate_linkedin_post(topic, tone)

def create_linkedin_post_draft(topic: str, tone: str = "professional") -> str:
    """Create a LinkedIn post draft for approval."""
    skills = LinkedInSkills()
    return skills.create_linkedin_post_draft(topic, tone)

def post_to_linkedin(post_file: Path) -> bool:
    """Post approved content to LinkedIn."""
    skills = LinkedInSkills()
    return skills.post_to_linkedin(post_file)


# Demo/Test
if __name__ == "__main__":
    print("=" * 70)
    print("  LINKEDIN AUTOMATION DEMO")
    print("=" * 70)

    skills = LinkedInSkills()

    # Demo 1: Generate a post
    print("\n[DEMO 1] Generating LinkedIn post...")
    post = skills.generate_linkedin_post("AI and Automation", "professional")
    print(post)

    # Demo 2: Create draft for approval
    print("\n[DEMO 2] Creating post draft for approval...")
    approval_file = skills.create_linkedin_post_draft(
        topic="Building AI Employees",
        tone="inspirational"
    )
    print(f"[OK] Draft created: {approval_file}")

    # Demo 3: Check for approved posts
    print("\n[DEMO 3] Checking for approved posts...")
    approved = skills.check_approved_posts()
    print(f"[INFO] Found {len(approved)} approved post(s)")

    print("\n" + "=" * 70)
    print("  DEMO COMPLETE")
    print("=" * 70)
    print("\nTo use LinkedIn automation:")
    print("  1. Create draft: create_linkedin_post_draft('topic')")
    print("  2. Review and approve the draft")
    print("  3. System will post to LinkedIn")
    print("\nNote: Actual LinkedIn posting requires API setup")

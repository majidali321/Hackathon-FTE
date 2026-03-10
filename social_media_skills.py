"""
Social Media Skills Module
Agent Skills for Facebook, Twitter, and Instagram posting
Part of Gold Tier requirements for Hackathon FTE
"""

import json
import logging
from datetime import datetime
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import integration modules
try:
    from integrations.facebook_integration import post_to_facebook
    from integrations.twitter_integration import post_to_twitter
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    logger.warning("Integration modules not found. Skills will create approval requests only.")
    INTEGRATIONS_AVAILABLE = False


def generate_social_media_content(topic, platform="facebook", tone="professional", max_length=None):
    """
    Generate social media content for a given topic

    Args:
        topic (str): The topic to write about
        platform (str): Target platform (facebook, twitter, instagram)
        tone (str): Tone of the content (professional, casual, inspirational)
        max_length (int): Maximum character length (280 for Twitter)

    Returns:
        str: Generated content
    """

    # Platform-specific constraints
    if platform.lower() == "twitter" and not max_length:
        max_length = 280

    # Tone templates
    tone_styles = {
        "professional": {
            "intro": "Exploring",
            "hashtags": ["#Business", "#Innovation", "#Technology"],
            "emoji": "💼"
        },
        "casual": {
            "intro": "Just thinking about",
            "hashtags": ["#Thoughts", "#Ideas", "#Tech"],
            "emoji": "💭"
        },
        "inspirational": {
            "intro": "Inspired by",
            "hashtags": ["#Motivation", "#Growth", "#Success"],
            "emoji": "✨"
        }
    }

    style = tone_styles.get(tone.lower(), tone_styles["professional"])

    # Generate content based on platform
    if platform.lower() == "twitter":
        content = f"{style['emoji']} {style['intro']} {topic}\n\n"
        content += f"Building the future with AI automation!\n\n"
        content += " ".join(style['hashtags'][:3])  # Limit hashtags for Twitter

        # Ensure it fits Twitter's limit
        if len(content) > 280:
            content = content[:277] + "..."

    elif platform.lower() == "instagram":
        content = f"{style['emoji']} {style['intro']} {topic}\n\n"
        content += f"As we move forward in 2026, AI and automation are transforming how we work. "
        content += f"This post was created by my Personal AI Employee - a fully autonomous system "
        content += f"that handles content creation, scheduling, and posting!\n\n"
        content += "What are your thoughts on AI automation?\n\n"
        content += " ".join(style['hashtags'])
        content += " #AI #Automation #FTE2026"

    else:  # Facebook (default)
        content = f"{style['emoji']} {style['intro']} {topic}\n\n"
        content += f"In 2026, we're witnessing incredible advances in AI and automation. "
        content += f"This post was automatically generated and published by my Personal AI Employee - "
        content += f"a sophisticated system that demonstrates the power of autonomous agents.\n\n"
        content += f"Key capabilities:\n"
        content += f"• Multi-channel monitoring (Email, WhatsApp, Files)\n"
        content += f"• Intelligent task processing\n"
        content += f"• Automated content creation\n"
        content += f"• Human-in-the-loop approval workflows\n\n"
        content += f"The future of work is here! 🚀\n\n"
        content += " ".join(style['hashtags'])
        content += " #AI #Automation #FTE2026"

    return content


def create_facebook_post_draft(topic, tone="professional"):
    """
    Create a Facebook post draft and save for approval

    Args:
        topic (str): The topic to write about
        tone (str): Tone of the post (professional, casual, inspirational)

    Returns:
        dict: Result with status and file path
    """
    try:
        # Generate content
        content = generate_social_media_content(topic, platform="facebook", tone=tone)

        # Create approval request
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"FACEBOOK_POST_{timestamp}_{topic[:30].replace(' ', '_')}.md"
        filepath = Path("Pending_Approval") / filename

        # Ensure directory exists
        filepath.parent.mkdir(exist_ok=True)

        # Write approval request
        approval_content = f"""# Facebook Post Approval Request

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Topic**: {topic}
**Tone**: {tone}
**Platform**: Facebook
**Status**: PENDING_APPROVAL

---

## Post Content

{content}

---

## Instructions

To approve this post:
1. Review the content above
2. Make any edits if needed
3. Move this file to the `Approved/` folder
4. The system will automatically post it to Facebook

To reject:
- Delete this file or move to `Done/` folder

---

**Generated by**: Social Media Skills (Agent Skill)
**Part of**: Gold Tier Implementation
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        logger.info(f"Facebook post draft created: {filepath}")

        return {
            "status": "success",
            "message": "Facebook post draft created and awaiting approval",
            "file": str(filepath),
            "content": content
        }

    except Exception as e:
        logger.error(f"Error creating Facebook post draft: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


def create_twitter_post_draft(topic, tone="professional"):
    """
    Create a Twitter post draft and save for approval

    Args:
        topic (str): The topic to write about
        tone (str): Tone of the tweet (professional, casual, inspirational)

    Returns:
        dict: Result with status and file path
    """
    try:
        # Generate content
        content = generate_social_media_content(topic, platform="twitter", tone=tone)

        # Create approval request
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"TWITTER_POST_{timestamp}_{topic[:30].replace(' ', '_')}.md"
        filepath = Path("Pending_Approval") / filename

        # Ensure directory exists
        filepath.parent.mkdir(exist_ok=True)

        # Write approval request
        approval_content = f"""# Twitter Post Approval Request

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Topic**: {topic}
**Tone**: {tone}
**Platform**: Twitter/X
**Character Count**: {len(content)}/280
**Status**: PENDING_APPROVAL

---

## Tweet Content

{content}

---

## Instructions

To approve this tweet:
1. Review the content above
2. Make any edits if needed (keep under 280 characters!)
3. Move this file to the `Approved/` folder
4. The system will automatically post it to Twitter

To reject:
- Delete this file or move to `Done/` folder

---

**Generated by**: Social Media Skills (Agent Skill)
**Part of**: Gold Tier Implementation
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        logger.info(f"Twitter post draft created: {filepath}")

        return {
            "status": "success",
            "message": "Twitter post draft created and awaiting approval",
            "file": str(filepath),
            "content": content,
            "char_count": len(content)
        }

    except Exception as e:
        logger.error(f"Error creating Twitter post draft: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


def create_instagram_post_draft(topic, tone="inspirational"):
    """
    Create an Instagram post draft and save for approval

    Args:
        topic (str): The topic to write about
        tone (str): Tone of the post (professional, casual, inspirational)

    Returns:
        dict: Result with status and file path
    """
    try:
        # Generate content
        content = generate_social_media_content(topic, platform="instagram", tone=tone)

        # Create approval request
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"INSTAGRAM_POST_{timestamp}_{topic[:30].replace(' ', '_')}.md"
        filepath = Path("Pending_Approval") / filename

        # Ensure directory exists
        filepath.parent.mkdir(exist_ok=True)

        # Write approval request
        approval_content = f"""# Instagram Post Approval Request

**Created**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Topic**: {topic}
**Tone**: {tone}
**Platform**: Instagram
**Status**: PENDING_APPROVAL

---

## Post Content

{content}

---

## Instructions

To approve this post:
1. Review the content above
2. Make any edits if needed
3. Add image path if desired: `IMAGE: path/to/image.jpg`
4. Move this file to the `Approved/` folder
5. The system will automatically post it to Instagram

To reject:
- Delete this file or move to `Done/` folder

---

**Note**: Instagram posting requires Instagram Business account and Facebook Graph API setup.

**Generated by**: Social Media Skills (Agent Skill)
**Part of**: Gold Tier Implementation
"""

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(approval_content)

        logger.info(f"Instagram post draft created: {filepath}")

        return {
            "status": "success",
            "message": "Instagram post draft created and awaiting approval",
            "file": str(filepath),
            "content": content
        }

    except Exception as e:
        logger.error(f"Error creating Instagram post draft: {e}")
        return {
            "status": "error",
            "message": str(e)
        }


def publish_approved_social_posts():
    """
    Check Approved folder and publish any approved social media posts

    Returns:
        dict: Results of publishing attempts
    """
    results = {
        "facebook": [],
        "twitter": [],
        "instagram": [],
        "errors": []
    }

    try:
        approved_dir = Path("Approved")
        if not approved_dir.exists():
            return results

        # Process each approved file
        for filepath in approved_dir.glob("*_POST_*.md"):
            try:
                # Read the file
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Extract post content (between ## Post Content and ---)
                if "## Post Content" in content or "## Tweet Content" in content:
                    parts = content.split("---")
                    if len(parts) >= 2:
                        post_content = parts[1].strip()

                        # Remove markdown headers
                        lines = post_content.split('\n')
                        post_content = '\n'.join([l for l in lines if not l.startswith('#')])
                        post_content = post_content.strip()

                        # Determine platform and post
                        if "FACEBOOK_POST" in filepath.name:
                            if INTEGRATIONS_AVAILABLE:
                                success = post_to_facebook(post_content, headless=True)
                                if success:
                                    results["facebook"].append(filepath.name)
                                    # Move to Done
                                    done_path = Path("Done") / filepath.name
                                    filepath.rename(done_path)
                                else:
                                    results["errors"].append(f"Failed to post to Facebook: {filepath.name}")
                            else:
                                results["errors"].append(f"Facebook integration not available: {filepath.name}")

                        elif "TWITTER_POST" in filepath.name:
                            if INTEGRATIONS_AVAILABLE:
                                success = post_to_twitter(post_content, headless=True)
                                if success:
                                    results["twitter"].append(filepath.name)
                                    # Move to Done
                                    done_path = Path("Done") / filepath.name
                                    filepath.rename(done_path)
                                else:
                                    results["errors"].append(f"Failed to post to Twitter: {filepath.name}")
                            else:
                                results["errors"].append(f"Twitter integration not available: {filepath.name}")

                        elif "INSTAGRAM_POST" in filepath.name:
                            # Instagram requires more complex setup (Graph API)
                            results["errors"].append(f"Instagram posting not yet implemented: {filepath.name}")

            except Exception as e:
                results["errors"].append(f"Error processing {filepath.name}: {str(e)}")

        return results

    except Exception as e:
        logger.error(f"Error in publish_approved_social_posts: {e}")
        results["errors"].append(str(e))
        return results


# Agent Skills Interface
SOCIAL_MEDIA_SKILLS = {
    "create_facebook_post": create_facebook_post_draft,
    "create_twitter_post": create_twitter_post_draft,
    "create_instagram_post": create_instagram_post_draft,
    "publish_approved_posts": publish_approved_social_posts,
    "generate_content": generate_social_media_content
}


if __name__ == "__main__":
    # Test the skills
    print("=" * 60)
    print("Social Media Skills Test")
    print("=" * 60)

    # Test Facebook post creation
    print("\n1. Creating Facebook post draft...")
    result = create_facebook_post_draft("AI and Automation in 2026", tone="professional")
    print(f"   Status: {result['status']}")
    print(f"   File: {result.get('file', 'N/A')}")

    # Test Twitter post creation
    print("\n2. Creating Twitter post draft...")
    result = create_twitter_post_draft("AI Automation", tone="casual")
    print(f"   Status: {result['status']}")
    print(f"   File: {result.get('file', 'N/A')}")
    print(f"   Characters: {result.get('char_count', 'N/A')}/280")

    # Test Instagram post creation
    print("\n3. Creating Instagram post draft...")
    result = create_instagram_post_draft("Future of Work", tone="inspirational")
    print(f"   Status: {result['status']}")
    print(f"   File: {result.get('file', 'N/A')}")

    print("\n" + "=" * 60)
    print("Test complete! Check Pending_Approval folder for drafts.")
    print("=" * 60)

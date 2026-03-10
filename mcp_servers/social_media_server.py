"""
Social Media MCP Server
Model Context Protocol server for social media operations
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

# Import integrations
try:
    from integrations.facebook_integration import post_to_facebook
    from integrations.twitter_integration import post_to_twitter
    INTEGRATIONS_AVAILABLE = True
except ImportError:
    logger.warning("Integration modules not available")
    INTEGRATIONS_AVAILABLE = False


class SocialMediaMCPServer:
    """MCP Server for social media operations"""

    def __init__(self):
        self.name = "social_media_server"
        self.version = "1.0.0"
        self.log_dir = Path("Logs")
        self.log_dir.mkdir(exist_ok=True)

    def log_activity(self, action, details):
        """Log social media activity"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            log_file = self.log_dir / f"social_media_log_{datetime.now().strftime('%Y%m%d')}.txt"

            log_entry = f"""
[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]
Action: {action}
Details: {json.dumps(details, indent=2)}
---
"""
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)

            logger.info(f"Activity logged: {action}")
        except Exception as e:
            logger.error(f"Error logging activity: {e}")

    def post_facebook(self, content, headless=True):
        """
        Post to Facebook

        Args:
            content (str): Post content
            headless (bool): Run browser in headless mode

        Returns:
            dict: Result with status and message
        """
        try:
            if not INTEGRATIONS_AVAILABLE:
                return {
                    "status": "error",
                    "message": "Facebook integration not available"
                }

            logger.info("Posting to Facebook via MCP server...")
            success = post_to_facebook(content, headless=headless)

            result = {
                "status": "success" if success else "error",
                "message": "Posted to Facebook successfully" if success else "Failed to post to Facebook",
                "platform": "facebook",
                "timestamp": datetime.now().isoformat()
            }

            # Log activity
            self.log_activity("facebook_post", {
                "content": content[:100] + "..." if len(content) > 100 else content,
                "success": success
            })

            return result

        except Exception as e:
            logger.error(f"Error posting to Facebook: {e}")
            return {
                "status": "error",
                "message": str(e),
                "platform": "facebook"
            }

    def post_twitter(self, content, headless=True):
        """
        Post to Twitter

        Args:
            content (str): Tweet content (max 280 characters)
            headless (bool): Run browser in headless mode

        Returns:
            dict: Result with status and message
        """
        try:
            if not INTEGRATIONS_AVAILABLE:
                return {
                    "status": "error",
                    "message": "Twitter integration not available"
                }

            # Check character limit
            if len(content) > 280:
                content = content[:277] + "..."

            logger.info("Posting to Twitter via MCP server...")
            success = post_to_twitter(content, headless=headless)

            result = {
                "status": "success" if success else "error",
                "message": "Posted to Twitter successfully" if success else "Failed to post to Twitter",
                "platform": "twitter",
                "char_count": len(content),
                "timestamp": datetime.now().isoformat()
            }

            # Log activity
            self.log_activity("twitter_post", {
                "content": content,
                "char_count": len(content),
                "success": success
            })

            return result

        except Exception as e:
            logger.error(f"Error posting to Twitter: {e}")
            return {
                "status": "error",
                "message": str(e),
                "platform": "twitter"
            }

    def post_instagram(self, content, image_path=None, headless=True):
        """
        Post to Instagram (placeholder - requires Graph API setup)

        Args:
            content (str): Post caption
            image_path (str): Path to image file
            headless (bool): Run browser in headless mode

        Returns:
            dict: Result with status and message
        """
        try:
            logger.warning("Instagram posting not yet implemented")

            result = {
                "status": "error",
                "message": "Instagram posting requires Facebook Graph API setup",
                "platform": "instagram",
                "timestamp": datetime.now().isoformat()
            }

            # Log activity
            self.log_activity("instagram_post_attempt", {
                "content": content[:100] + "..." if len(content) > 100 else content,
                "image": image_path,
                "success": False
            })

            return result

        except Exception as e:
            logger.error(f"Error posting to Instagram: {e}")
            return {
                "status": "error",
                "message": str(e),
                "platform": "instagram"
            }

    def get_analytics(self, platform=None, days=7):
        """
        Get social media analytics (placeholder)

        Args:
            platform (str): Platform name (facebook, twitter, instagram) or None for all
            days (int): Number of days to analyze

        Returns:
            dict: Analytics data
        """
        try:
            # Read logs and generate basic analytics
            analytics = {
                "period_days": days,
                "platforms": {},
                "total_posts": 0,
                "timestamp": datetime.now().isoformat()
            }

            # Parse log files
            log_files = list(self.log_dir.glob("social_media_log_*.txt"))

            for log_file in log_files:
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # Count posts by platform
                    analytics["platforms"]["facebook"] = content.count("facebook_post")
                    analytics["platforms"]["twitter"] = content.count("twitter_post")
                    analytics["platforms"]["instagram"] = content.count("instagram_post")

                except Exception as e:
                    logger.error(f"Error reading log file {log_file}: {e}")

            analytics["total_posts"] = sum(analytics["platforms"].values())

            return {
                "status": "success",
                "data": analytics
            }

        except Exception as e:
            logger.error(f"Error getting analytics: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

    def health_check(self):
        """Check server health and integration status"""
        return {
            "status": "healthy",
            "server": self.name,
            "version": self.version,
            "integrations": {
                "facebook": INTEGRATIONS_AVAILABLE,
                "twitter": INTEGRATIONS_AVAILABLE,
                "instagram": False  # Not yet implemented
            },
            "timestamp": datetime.now().isoformat()
        }


# MCP Server Interface
def handle_request(method, params):
    """
    Handle MCP requests

    Args:
        method (str): Method name
        params (dict): Method parameters

    Returns:
        dict: Response
    """
    server = SocialMediaMCPServer()

    if method == "post_facebook":
        return server.post_facebook(
            content=params.get("content", ""),
            headless=params.get("headless", True)
        )

    elif method == "post_twitter":
        return server.post_twitter(
            content=params.get("content", ""),
            headless=params.get("headless", True)
        )

    elif method == "post_instagram":
        return server.post_instagram(
            content=params.get("content", ""),
            image_path=params.get("image_path"),
            headless=params.get("headless", True)
        )

    elif method == "get_analytics":
        return server.get_analytics(
            platform=params.get("platform"),
            days=params.get("days", 7)
        )

    elif method == "health_check":
        return server.health_check()

    else:
        return {
            "status": "error",
            "message": f"Unknown method: {method}"
        }


def test_server():
    """Test the MCP server"""
    print("=" * 60)
    print("Social Media MCP Server Test")
    print("=" * 60)
    print()

    server = SocialMediaMCPServer()

    # Test 1: Health check
    print("1. Health Check")
    result = server.health_check()
    print(f"   Status: {result['status']}")
    print(f"   Integrations: {result['integrations']}")
    print()

    # Test 2: Analytics
    print("2. Get Analytics")
    result = server.get_analytics()
    print(f"   Status: {result['status']}")
    if result['status'] == 'success':
        print(f"   Total Posts: {result['data']['total_posts']}")
        print(f"   By Platform: {result['data']['platforms']}")
    print()

    # Test 3: Test post (dry run - just logging)
    print("3. Test Post Logging")
    server.log_activity("test_post", {
        "platform": "facebook",
        "content": "Test post from MCP server",
        "success": True
    })
    print("   Activity logged successfully")
    print()

    print("=" * 60)
    print("Test complete!")
    print("=" * 60)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        if sys.argv[1] == "--test":
            test_server()
        elif sys.argv[1] == "--health":
            server = SocialMediaMCPServer()
            result = server.health_check()
            print(json.dumps(result, indent=2))
        elif sys.argv[1] == "--analytics":
            server = SocialMediaMCPServer()
            result = server.get_analytics()
            print(json.dumps(result, indent=2))
        else:
            print("Usage: python social_media_server.py [--test|--health|--analytics]")
    else:
        test_server()

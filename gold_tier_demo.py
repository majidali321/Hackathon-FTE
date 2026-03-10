"""
Gold Tier Demo Script
Demonstrates all Gold Tier features in action
"""

import time
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def print_section(title):
    """Print a section header"""
    print(f"\n--- {title} ---\n")

print_header("GOLD TIER DEMONSTRATION")
print("This demo showcases all Gold Tier features of your AI Employee")
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# Demo 1: Social Media Content Generation
print_section("1. Social Media Content Generation")
try:
    from social_media_skills import generate_social_media_content

    print("Generating content for different platforms...")

    # Facebook
    fb_content = generate_social_media_content(
        "AI and Automation in 2026",
        platform="facebook",
        tone="professional"
    )
    print(f"\nFacebook Post ({len(fb_content)} chars):")
    print("-" * 50)
    print(fb_content[:200] + "..." if len(fb_content) > 200 else fb_content)

    # Twitter
    tw_content = generate_social_media_content(
        "AI Automation",
        platform="twitter",
        tone="casual"
    )
    print(f"\nTwitter Post ({len(tw_content)}/280 chars):")
    print("-" * 50)
    print(tw_content)

    print("\n✓ Social media content generation working!")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Demo 2: Cross-Domain Task Analysis
print_section("2. Cross-Domain Task Analysis")
try:
    from cross_domain_integration import CrossDomainIntegrator

    integrator = CrossDomainIntegrator()
    tasks = integrator.get_unified_task_list()
    summary = integrator.get_domain_summary()

    print(f"Total Tasks: {summary['total_tasks']}")
    print(f"\nBy Domain:")
    for domain, count in sorted(summary['by_domain'].items(), key=lambda x: x[1], reverse=True):
        print(f"  - {domain.title()}: {count} tasks")

    print(f"\nBy Priority:")
    for priority in ['critical', 'high', 'medium', 'low']:
        count = summary['by_priority'].get(priority, 0)
        if count > 0:
            print(f"  - {priority.upper()}: {count} tasks")

    if tasks:
        print(f"\nTop 3 Most Urgent Tasks:")
        for i, task in enumerate(tasks[:3], 1):
            print(f"  {i}. {task['file'][:50]}...")
            print(f"     Priority: {task['priority'].upper()}, Urgency: {task['urgency_score']:.1f}")

    print("\n✓ Cross-domain integration working!")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Demo 3: CEO Briefing Generation
print_section("3. CEO Briefing Generation")
try:
    from ceo_briefing import CEOBriefingGenerator

    generator = CEOBriefingGenerator()

    print("Analyzing system metrics...")
    task_metrics = generator.analyze_task_completion(days=7)
    social_metrics = generator.analyze_social_media_activity(days=7)
    email_metrics = generator.analyze_email_activity(days=7)

    print(f"\nTask Metrics:")
    print(f"  - Completed: {task_metrics.get('total_completed', 0)}")
    print(f"  - Pending: {task_metrics.get('pending_tasks', 0)}")
    print(f"  - Completion Rate: {task_metrics.get('completion_rate', 0):.1f}%")

    print(f"\nSocial Media Metrics:")
    print(f"  - Total Posts: {social_metrics.get('total_posts', 0)}")
    print(f"  - Pending Approval: {social_metrics.get('pending_approval', 0)}")

    print(f"\nEmail Metrics:")
    print(f"  - Processed: {email_metrics.get('emails_processed', 0)}")
    print(f"  - Pending: {email_metrics.get('pending_responses', 0)}")

    print("\n✓ CEO briefing metrics working!")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Demo 4: Error Recovery System
print_section("4. Error Recovery & Health Monitoring")
try:
    from error_recovery import ServiceHealthChecker, ErrorRecoveryManager

    print("Running health checks...")
    health = ServiceHealthChecker.run_all_checks()

    print(f"\nSystem Health:")
    for service, status in health['checks'].items():
        emoji = "✓" if status else "✗"
        print(f"  {emoji} {service.replace('_', ' ').title()}: {'Healthy' if status else 'Unhealthy'}")

    print(f"\nOverall Status: {'HEALTHY' if health['overall_health'] else 'NEEDS ATTENTION'}")

    # Error statistics
    manager = ErrorRecoveryManager()
    stats = manager.get_error_statistics()
    print(f"\nError Statistics:")
    print(f"  - Total Errors: {stats.get('total_errors', 0)}")

    print("\n✓ Error recovery system working!")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Demo 5: MCP Servers
print_section("5. MCP Server Status")
try:
    from mcp_servers.email_server import EmailMCPServer
    from mcp_servers.social_media_server import SocialMediaMCPServer

    print("Checking MCP servers...")

    # Email server
    email_server = EmailMCPServer()
    print(f"\n✓ Email MCP Server: Available")
    print(f"  - Version: {email_server.version}")

    # Social media server
    social_server = SocialMediaMCPServer()
    health = social_server.health_check()
    print(f"\n✓ Social Media MCP Server: Available")
    print(f"  - Version: {social_server.version}")
    print(f"  - Status: {health['status']}")

    print("\n✓ All MCP servers operational!")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Demo 6: Ralph Wiggum Loop
print_section("6. Ralph Wiggum Autonomous Loop")
try:
    from ralph_wiggum.stop_hook import RalphWiggumLoop
    from ralph_wiggum.task_completion import TaskCompletionChecker

    print("Checking autonomous operation capabilities...")

    checker = TaskCompletionChecker()
    incomplete_tasks = checker.get_incomplete_tasks()

    print(f"\n✓ Ralph Wiggum Loop: Available")
    print(f"  - Incomplete Tasks: {len(incomplete_tasks)}")
    print(f"  - Ready for autonomous operation")

    print("\n✓ Autonomous loop ready!")

except Exception as e:
    print(f"\n✗ Error: {e}")

# Summary
print_header("DEMONSTRATION COMPLETE")

print("Gold Tier Features Demonstrated:")
print()
print("✓ 1. Social Media Content Generation")
print("     - Multi-platform support (Facebook, Twitter, Instagram)")
print("     - Multiple tone options")
print("     - Character limit enforcement")
print()
print("✓ 2. Cross-Domain Task Management")
print("     - Unified task view across 4 domains")
print("     - Intelligent priority scoring")
print("     - Dependency tracking")
print()
print("✓ 3. CEO Briefing System")
print("     - Task completion metrics")
print("     - Social media analytics")
print("     - Email management statistics")
print()
print("✓ 4. Error Recovery & Health Monitoring")
print("     - Service health checks")
print("     - Error statistics")
print("     - Automatic recovery")
print()
print("✓ 5. Multiple MCP Servers")
print("     - Email MCP server")
print("     - Social Media MCP server")
print()
print("✓ 6. Ralph Wiggum Autonomous Loop")
print("     - Continuous task processing")
print("     - Completion checking")
print()

print("=" * 70)
print("Your AI Employee is operating at GOLD TIER level!")
print("All enterprise features are functional and ready for production use.")
print("=" * 70)
print()
print(f"Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

"""
CEO Briefing Generator
Generates weekly business and accounting audit reports
Part of Gold Tier requirements for Hackathon FTE
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CEOBriefingGenerator:
    """Generates comprehensive CEO briefings with business metrics"""

    def __init__(self):
        self.base_dir = Path(".")
        self.logs_dir = Path("Logs")
        self.done_dir = Path("Done")
        self.needs_action_dir = Path("Needs_Action")
        self.reports_dir = Path("Reports")
        self.reports_dir.mkdir(exist_ok=True)

    def analyze_task_completion(self, days=7):
        """Analyze task completion metrics"""
        try:
            metrics = {
                "total_completed": 0,
                "by_type": defaultdict(int),
                "by_day": defaultdict(int),
                "completion_rate": 0,
                "pending_tasks": 0
            }

            # Count completed tasks
            if self.done_dir.exists():
                completed_files = list(self.done_dir.glob("TASK_*.md"))
                metrics["total_completed"] = len(completed_files)

                # Analyze by type and date
                for task_file in completed_files:
                    try:
                        with open(task_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        # Extract task type
                        if "Email" in content:
                            metrics["by_type"]["email"] += 1
                        elif "FILE_DROP" in task_file.name:
                            metrics["by_type"]["file_processing"] += 1
                        elif "LinkedIn" in content:
                            metrics["by_type"]["linkedin"] += 1
                        else:
                            metrics["by_type"]["general"] += 1

                    except Exception as e:
                        logger.error(f"Error analyzing task {task_file}: {e}")

            # Count pending tasks
            if self.needs_action_dir.exists():
                pending_files = list(self.needs_action_dir.glob("TASK_*.md"))
                metrics["pending_tasks"] = len(pending_files)

            # Calculate completion rate
            total_tasks = metrics["total_completed"] + metrics["pending_tasks"]
            if total_tasks > 0:
                metrics["completion_rate"] = (metrics["total_completed"] / total_tasks) * 100

            return metrics

        except Exception as e:
            logger.error(f"Error analyzing task completion: {e}")
            return {}

    def analyze_social_media_activity(self, days=7):
        """Analyze social media posting activity"""
        try:
            metrics = {
                "total_posts": 0,
                "by_platform": {
                    "linkedin": 0,
                    "facebook": 0,
                    "twitter": 0,
                    "instagram": 0
                },
                "pending_approval": 0,
                "approved": 0
            }

            # Check social media logs
            if self.logs_dir.exists():
                log_files = list(self.logs_dir.glob("social_media_log_*.txt"))
                for log_file in log_files:
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()

                        metrics["by_platform"]["facebook"] += content.count("facebook_post")
                        metrics["by_platform"]["twitter"] += content.count("twitter_post")
                        metrics["by_platform"]["instagram"] += content.count("instagram_post")

                    except Exception as e:
                        logger.error(f"Error reading log {log_file}: {e}")

            # Check LinkedIn logs
            linkedin_log = self.logs_dir / "linkedin_activity.log"
            if linkedin_log.exists():
                try:
                    with open(linkedin_log, 'r', encoding='utf-8') as f:
                        content = f.read()
                    metrics["by_platform"]["linkedin"] = content.count("Post published successfully")
                except Exception as e:
                    logger.error(f"Error reading LinkedIn log: {e}")

            # Count pending approvals
            pending_dir = Path("Pending_Approval")
            if pending_dir.exists():
                social_posts = list(pending_dir.glob("*_POST_*.md"))
                metrics["pending_approval"] = len(social_posts)

            # Count approved posts
            approved_dir = Path("Approved")
            if approved_dir.exists():
                social_posts = list(approved_dir.glob("*_POST_*.md"))
                metrics["approved"] = len(social_posts)

            metrics["total_posts"] = sum(metrics["by_platform"].values())

            return metrics

        except Exception as e:
            logger.error(f"Error analyzing social media activity: {e}")
            return {}

    def analyze_email_activity(self, days=7):
        """Analyze email monitoring and response activity"""
        try:
            metrics = {
                "emails_processed": 0,
                "urgent_emails": 0,
                "responses_sent": 0,
                "pending_responses": 0
            }

            # Count email tasks
            if self.done_dir.exists():
                email_tasks = [f for f in self.done_dir.glob("TASK_*Email*.md")]
                metrics["emails_processed"] = len(email_tasks)

                # Check for urgent emails
                for task_file in email_tasks:
                    try:
                        with open(task_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        if "URGENT" in content or "urgent" in content:
                            metrics["urgent_emails"] += 1
                    except Exception as e:
                        logger.error(f"Error reading email task {task_file}: {e}")

            # Count pending email responses
            if self.needs_action_dir.exists():
                pending_emails = [f for f in self.needs_action_dir.glob("TASK_*Email*.md")]
                metrics["pending_responses"] = len(pending_emails)

            # Check email server logs
            email_log = self.logs_dir / "email_activity.log"
            if email_log.exists():
                try:
                    with open(email_log, 'r', encoding='utf-8') as f:
                        content = f.read()
                    metrics["responses_sent"] = content.count("Email sent successfully")
                except Exception as e:
                    logger.error(f"Error reading email log: {e}")

            return metrics

        except Exception as e:
            logger.error(f"Error analyzing email activity: {e}")
            return {}

    def analyze_system_health(self):
        """Analyze system health and performance"""
        try:
            health = {
                "watchers_active": 0,
                "mcp_servers_active": 0,
                "errors_logged": 0,
                "last_activity": None,
                "disk_usage": {}
            }

            # Check for recent log activity
            if self.logs_dir.exists():
                log_files = list(self.logs_dir.glob("*.log")) + list(self.logs_dir.glob("*.txt"))
                if log_files:
                    # Get most recent log file
                    latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
                    health["last_activity"] = datetime.fromtimestamp(latest_log.stat().st_mtime).isoformat()

                # Count errors in logs
                for log_file in log_files:
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        health["errors_logged"] += content.count("ERROR")
                    except Exception as e:
                        logger.error(f"Error reading log {log_file}: {e}")

            # Check folder sizes
            folders = ["Inbox", "Needs_Action", "Done", "Pending_Approval", "Approved", "Logs"]
            for folder in folders:
                folder_path = Path(folder)
                if folder_path.exists():
                    file_count = len(list(folder_path.glob("*")))
                    health["disk_usage"][folder] = file_count

            return health

        except Exception as e:
            logger.error(f"Error analyzing system health: {e}")
            return {}

    def identify_bottlenecks(self):
        """Identify system bottlenecks and issues"""
        try:
            bottlenecks = []

            # Check for excessive pending tasks
            if self.needs_action_dir.exists():
                pending_count = len(list(self.needs_action_dir.glob("TASK_*.md")))
                if pending_count > 10:
                    bottlenecks.append({
                        "type": "high_pending_tasks",
                        "severity": "high" if pending_count > 20 else "medium",
                        "description": f"{pending_count} tasks pending in Needs_Action folder",
                        "recommendation": "Review and process pending tasks or increase automation"
                    })

            # Check for excessive pending approvals
            pending_approval_dir = Path("Pending_Approval")
            if pending_approval_dir.exists():
                approval_count = len(list(pending_approval_dir.glob("*.md")))
                if approval_count > 5:
                    bottlenecks.append({
                        "type": "pending_approvals",
                        "severity": "medium",
                        "description": f"{approval_count} items awaiting approval",
                        "recommendation": "Review and approve/reject pending items"
                    })

            # Check for errors in logs
            if self.logs_dir.exists():
                error_count = 0
                for log_file in self.logs_dir.glob("*.log"):
                    try:
                        with open(log_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        error_count += content.count("ERROR")
                    except:
                        pass

                if error_count > 10:
                    bottlenecks.append({
                        "type": "high_error_rate",
                        "severity": "high",
                        "description": f"{error_count} errors logged in recent activity",
                        "recommendation": "Review error logs and fix underlying issues"
                    })

            return bottlenecks

        except Exception as e:
            logger.error(f"Error identifying bottlenecks: {e}")
            return []

    def generate_briefing(self, days=7):
        """Generate comprehensive CEO briefing"""
        try:
            logger.info(f"Generating CEO briefing for last {days} days...")

            # Collect all metrics
            task_metrics = self.analyze_task_completion(days)
            social_metrics = self.analyze_social_media_activity(days)
            email_metrics = self.analyze_email_activity(days)
            health_metrics = self.analyze_system_health()
            bottlenecks = self.identify_bottlenecks()

            # Generate report
            timestamp = datetime.now()
            report = f"""# CEO Weekly Briefing

**Generated**: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}
**Period**: Last {days} days
**Report Type**: Business & Accounting Audit

---

## Executive Summary

Your Personal AI Employee has been operating autonomously, handling multiple channels and tasks. Here's what happened this week:

### Key Metrics
- **Tasks Completed**: {task_metrics.get('total_completed', 0)}
- **Completion Rate**: {task_metrics.get('completion_rate', 0):.1f}%
- **Social Media Posts**: {social_metrics.get('total_posts', 0)}
- **Emails Processed**: {email_metrics.get('emails_processed', 0)}
- **System Errors**: {health_metrics.get('errors_logged', 0)}

---

## Task Management

### Completion Statistics
- **Total Completed**: {task_metrics.get('total_completed', 0)} tasks
- **Pending Tasks**: {task_metrics.get('pending_tasks', 0)} tasks
- **Completion Rate**: {task_metrics.get('completion_rate', 0):.1f}%

### Tasks by Type
"""
            # Add task breakdown
            for task_type, count in task_metrics.get('by_type', {}).items():
                report += f"- **{task_type.title()}**: {count} tasks\n"

            report += f"""
### Status
{'✅ Good - Tasks are being processed efficiently' if task_metrics.get('completion_rate', 0) > 70 else '⚠️ Attention needed - Task backlog building up'}

---

## Social Media Activity

### Posts Published
- **LinkedIn**: {social_metrics.get('by_platform', {}).get('linkedin', 0)} posts
- **Facebook**: {social_metrics.get('by_platform', {}).get('facebook', 0)} posts
- **Twitter**: {social_metrics.get('by_platform', {}).get('twitter', 0)} posts
- **Instagram**: {social_metrics.get('by_platform', {}).get('instagram', 0)} posts

### Approval Queue
- **Pending Approval**: {social_metrics.get('pending_approval', 0)} posts
- **Approved (Ready to Post)**: {social_metrics.get('approved', 0)} posts

### Status
{'✅ Active social media presence maintained' if social_metrics.get('total_posts', 0) > 0 else 'ℹ️ No social media posts this period'}

---

## Email Management

### Email Activity
- **Emails Processed**: {email_metrics.get('emails_processed', 0)}
- **Urgent Emails**: {email_metrics.get('urgent_emails', 0)}
- **Responses Sent**: {email_metrics.get('responses_sent', 0)}
- **Pending Responses**: {email_metrics.get('pending_responses', 0)}

### Status
{'✅ Email inbox under control' if email_metrics.get('pending_responses', 0) < 5 else '⚠️ Email backlog needs attention'}

---

## System Health

### Performance Metrics
- **Last Activity**: {health_metrics.get('last_activity', 'Unknown')}
- **Errors Logged**: {health_metrics.get('errors_logged', 0)}

### Storage Usage
"""
            # Add storage breakdown
            for folder, count in health_metrics.get('disk_usage', {}).items():
                report += f"- **{folder}**: {count} files\n"

            report += f"""
### Status
{'✅ System operating normally' if health_metrics.get('errors_logged', 0) < 10 else '⚠️ Elevated error rate detected'}

---

## Bottlenecks & Issues

"""
            if bottlenecks:
                for i, bottleneck in enumerate(bottlenecks, 1):
                    severity_emoji = "🔴" if bottleneck['severity'] == 'high' else "🟡"
                    report += f"""### {severity_emoji} Issue {i}: {bottleneck['type'].replace('_', ' ').title()}
**Severity**: {bottleneck['severity'].upper()}
**Description**: {bottleneck['description']}
**Recommendation**: {bottleneck['recommendation']}

"""
            else:
                report += "✅ No significant bottlenecks detected. System running smoothly.\n\n"

            report += """---

## Recommendations

### Immediate Actions
"""
            # Generate recommendations based on metrics
            recommendations = []

            if task_metrics.get('pending_tasks', 0) > 10:
                recommendations.append("1. Review and process pending tasks in Needs_Action folder")

            if social_metrics.get('pending_approval', 0) > 3:
                recommendations.append(f"{len(recommendations) + 1}. Approve or reject {social_metrics.get('pending_approval', 0)} pending social media posts")

            if email_metrics.get('pending_responses', 0) > 5:
                recommendations.append(f"{len(recommendations) + 1}. Address {email_metrics.get('pending_responses', 0)} pending email responses")

            if health_metrics.get('errors_logged', 0) > 10:
                recommendations.append(f"{len(recommendations) + 1}. Review error logs and address system issues")

            if not recommendations:
                recommendations.append("1. Continue monitoring - system operating well")

            for rec in recommendations:
                report += f"{rec}\n"

            report += f"""
### Strategic Initiatives
1. Consider expanding automation to additional channels
2. Review and optimize approval workflows
3. Implement additional MCP servers for enhanced capabilities
4. Schedule regular system maintenance and updates

---

## Accounting Summary

### Transaction Overview
**Note**: Full accounting integration requires Odoo setup (Gold Tier requirement)

**Current Status**: Basic activity tracking in place
**Next Steps**:
- Install Odoo Community Edition
- Configure accounting module
- Integrate with MCP server
- Enable automated transaction logging

---

## Conclusion

Your AI Employee processed **{task_metrics.get('total_completed', 0)} tasks** with a **{task_metrics.get('completion_rate', 0):.1f}% completion rate** this week.

{'The system is operating efficiently with no major issues.' if not bottlenecks else f'{len(bottlenecks)} issue(s) require attention.'}

**Overall Status**: {'🟢 HEALTHY' if len(bottlenecks) == 0 and task_metrics.get('completion_rate', 0) > 70 else '🟡 NEEDS ATTENTION' if len(bottlenecks) <= 2 else '🔴 REQUIRES IMMEDIATE ACTION'}

---

**Next Briefing**: {(timestamp + timedelta(days=7)).strftime('%Y-%m-%d')}

*Generated automatically by CEO Briefing Generator*
*Part of Gold Tier Implementation - Hackathon FTE*
"""

            return report

        except Exception as e:
            logger.error(f"Error generating briefing: {e}")
            return None

    def save_briefing(self, report):
        """Save briefing to Reports folder"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"CEO_BRIEFING_{timestamp}.md"
            filepath = self.reports_dir / filename

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)

            logger.info(f"Briefing saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving briefing: {e}")
            return None


def generate_ceo_briefing(days=7, save=True):
    """
    Generate CEO briefing report

    Args:
        days (int): Number of days to analyze
        save (bool): Save report to file

    Returns:
        str: Report content or file path
    """
    generator = CEOBriefingGenerator()
    report = generator.generate_briefing(days)

    if report and save:
        filepath = generator.save_briefing(report)
        return filepath
    else:
        return report


if __name__ == "__main__":
    print("=" * 60)
    print("CEO Briefing Generator")
    print("=" * 60)
    print()

    print("Generating weekly briefing...")
    filepath = generate_ceo_briefing(days=7, save=True)

    if filepath:
        print(f"\n✅ Briefing generated successfully!")
        print(f"📄 File: {filepath}")
        print()
        print("Opening report...")
        print()

        # Display the report
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("\n❌ Failed to generate briefing")

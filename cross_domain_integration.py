"""
Cross-Domain Integration Module
Unified task management across personal and business domains
Part of Gold Tier requirements for Hackathon FTE
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CrossDomainIntegrator:
    """Manages tasks across personal and business domains"""

    def __init__(self):
        self.needs_action_dir = Path("Needs_Action")
        self.done_dir = Path("Done")
        self.pending_approval_dir = Path("Pending_Approval")

        # Domain categories
        self.domains = {
            "personal": ["email", "file", "reminder", "personal"],
            "business": ["linkedin", "facebook", "twitter", "instagram", "meeting", "client", "project"],
            "financial": ["invoice", "payment", "transaction", "accounting", "odoo"],
            "communication": ["email", "message", "whatsapp", "slack"]
        }

        # Priority levels
        self.priority_levels = {
            "critical": 1,
            "high": 2,
            "medium": 3,
            "low": 4
        }

    def classify_task_domain(self, task_file):
        """
        Classify a task into domains

        Args:
            task_file (Path): Path to task file

        Returns:
            list: List of applicable domains
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            applicable_domains = []

            for domain, keywords in self.domains.items():
                for keyword in keywords:
                    if keyword in content or keyword in task_file.name.lower():
                        if domain not in applicable_domains:
                            applicable_domains.append(domain)

            # Default to personal if no domain found
            if not applicable_domains:
                applicable_domains.append("personal")

            return applicable_domains

        except Exception as e:
            logger.error(f"Error classifying task {task_file}: {e}")
            return ["personal"]

    def extract_task_priority(self, task_file):
        """
        Extract priority from task file

        Args:
            task_file (Path): Path to task file

        Returns:
            str: Priority level (critical, high, medium, low)
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()

            # Check for explicit priority markers
            if "critical" in content or "urgent" in content:
                return "critical"
            elif "high priority" in content or "important" in content:
                return "high"
            elif "low priority" in content:
                return "low"
            else:
                return "medium"

        except Exception as e:
            logger.error(f"Error extracting priority from {task_file}: {e}")
            return "medium"

    def analyze_task_dependencies(self, task_file):
        """
        Analyze task dependencies

        Args:
            task_file (Path): Path to task file

        Returns:
            dict: Dependency information
        """
        try:
            with open(task_file, 'r', encoding='utf-8') as f:
                content = f.read()

            dependencies = {
                "blocks": [],
                "blocked_by": [],
                "related": []
            }

            # Look for dependency markers
            lines = content.split('\n')
            for line in lines:
                if "depends on" in line.lower() or "blocked by" in line.lower():
                    dependencies["blocked_by"].append(line.strip())
                elif "blocks" in line.lower():
                    dependencies["blocks"].append(line.strip())
                elif "related to" in line.lower():
                    dependencies["related"].append(line.strip())

            return dependencies

        except Exception as e:
            logger.error(f"Error analyzing dependencies for {task_file}: {e}")
            return {"blocks": [], "blocked_by": [], "related": []}

    def get_unified_task_list(self):
        """
        Get unified task list across all domains

        Returns:
            list: List of task dictionaries with metadata
        """
        try:
            unified_tasks = []

            if not self.needs_action_dir.exists():
                return unified_tasks

            # Process all tasks
            for task_file in self.needs_action_dir.glob("TASK_*.md"):
                try:
                    domains = self.classify_task_domain(task_file)
                    priority = self.extract_task_priority(task_file)
                    dependencies = self.analyze_task_dependencies(task_file)

                    # Get file metadata
                    stat = task_file.stat()
                    created_time = datetime.fromtimestamp(stat.st_ctime)
                    age_hours = (datetime.now() - created_time).total_seconds() / 3600

                    task_info = {
                        "file": task_file.name,
                        "path": str(task_file),
                        "domains": domains,
                        "priority": priority,
                        "priority_score": self.priority_levels.get(priority, 3),
                        "dependencies": dependencies,
                        "created": created_time.isoformat(),
                        "age_hours": age_hours,
                        "urgency_score": self.calculate_urgency_score(priority, age_hours, dependencies)
                    }

                    unified_tasks.append(task_info)

                except Exception as e:
                    logger.error(f"Error processing task {task_file}: {e}")

            # Sort by urgency score (highest first)
            unified_tasks.sort(key=lambda x: x["urgency_score"], reverse=True)

            return unified_tasks

        except Exception as e:
            logger.error(f"Error getting unified task list: {e}")
            return []

    def calculate_urgency_score(self, priority, age_hours, dependencies):
        """
        Calculate urgency score for task prioritization

        Args:
            priority (str): Priority level
            age_hours (float): Age of task in hours
            dependencies (dict): Task dependencies

        Returns:
            float: Urgency score (higher = more urgent)
        """
        # Base score from priority
        base_score = {
            "critical": 100,
            "high": 75,
            "medium": 50,
            "low": 25
        }.get(priority, 50)

        # Age factor (older tasks get higher score)
        age_factor = min(age_hours / 24, 10)  # Cap at 10 days

        # Dependency factor (blocking tasks get higher score)
        dependency_factor = len(dependencies.get("blocks", [])) * 5

        # Calculate final score
        urgency_score = base_score + age_factor + dependency_factor

        return urgency_score

    def get_domain_summary(self):
        """
        Get summary of tasks by domain

        Returns:
            dict: Domain summary
        """
        try:
            tasks = self.get_unified_task_list()

            summary = {
                "total_tasks": len(tasks),
                "by_domain": defaultdict(int),
                "by_priority": defaultdict(int),
                "critical_tasks": [],
                "blocked_tasks": [],
                "oldest_task": None
            }

            for task in tasks:
                # Count by domain
                for domain in task["domains"]:
                    summary["by_domain"][domain] += 1

                # Count by priority
                summary["by_priority"][task["priority"]] += 1

                # Track critical tasks
                if task["priority"] == "critical":
                    summary["critical_tasks"].append(task["file"])

                # Track blocked tasks
                if task["dependencies"]["blocked_by"]:
                    summary["blocked_tasks"].append(task["file"])

            # Find oldest task
            if tasks:
                oldest = max(tasks, key=lambda x: x["age_hours"])
                summary["oldest_task"] = {
                    "file": oldest["file"],
                    "age_hours": oldest["age_hours"],
                    "age_days": oldest["age_hours"] / 24
                }

            return summary

        except Exception as e:
            logger.error(f"Error getting domain summary: {e}")
            return {}

    def generate_unified_dashboard(self):
        """
        Generate unified dashboard showing all domains

        Returns:
            str: Dashboard content
        """
        try:
            tasks = self.get_unified_task_list()
            summary = self.get_domain_summary()

            dashboard = f"""# Unified Cross-Domain Dashboard

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Total Tasks**: {summary['total_tasks']}

---

## Priority Overview

"""
            # Priority breakdown
            for priority in ["critical", "high", "medium", "low"]:
                count = summary["by_priority"].get(priority, 0)
                emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(priority, "⚪")
                dashboard += f"- {emoji} **{priority.upper()}**: {count} tasks\n"

            dashboard += f"""
---

## Domain Breakdown

"""
            # Domain breakdown
            for domain, count in sorted(summary["by_domain"].items(), key=lambda x: x[1], reverse=True):
                emoji = {
                    "personal": "👤",
                    "business": "💼",
                    "financial": "💰",
                    "communication": "💬"
                }.get(domain, "📋")
                dashboard += f"- {emoji} **{domain.title()}**: {count} tasks\n"

            dashboard += f"""
---

## Critical Attention Required

"""
            if summary["critical_tasks"]:
                dashboard += f"**{len(summary['critical_tasks'])} CRITICAL TASKS:**\n\n"
                for task in summary["critical_tasks"]:
                    dashboard += f"- 🔴 {task}\n"
            else:
                dashboard += "✅ No critical tasks\n"

            dashboard += f"""
---

## Blocked Tasks

"""
            if summary["blocked_tasks"]:
                dashboard += f"**{len(summary['blocked_tasks'])} tasks are blocked:**\n\n"
                for task in summary["blocked_tasks"]:
                    dashboard += f"- ⛔ {task}\n"
            else:
                dashboard += "✅ No blocked tasks\n"

            dashboard += f"""
---

## Task Queue (Top 10 by Urgency)

"""
            # Show top 10 most urgent tasks
            for i, task in enumerate(tasks[:10], 1):
                domains_str = ", ".join(task["domains"])
                priority_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(task["priority"], "⚪")
                dashboard += f"{i}. {priority_emoji} **{task['file']}**\n"
                dashboard += f"   - Domains: {domains_str}\n"
                dashboard += f"   - Priority: {task['priority'].upper()}\n"
                dashboard += f"   - Age: {task['age_hours']:.1f} hours\n"
                dashboard += f"   - Urgency Score: {task['urgency_score']:.1f}\n\n"

            dashboard += f"""
---

## Oldest Task

"""
            if summary["oldest_task"]:
                dashboard += f"⏰ **{summary['oldest_task']['file']}**\n"
                dashboard += f"Age: {summary['oldest_task']['age_days']:.1f} days ({summary['oldest_task']['age_hours']:.1f} hours)\n"
            else:
                dashboard += "No tasks pending\n"

            dashboard += f"""
---

## Recommendations

"""
            recommendations = []

            if summary["critical_tasks"]:
                recommendations.append(f"1. Address {len(summary['critical_tasks'])} critical tasks immediately")

            if summary["blocked_tasks"]:
                recommendations.append(f"{len(recommendations) + 1}. Resolve {len(summary['blocked_tasks'])} blocked tasks")

            if summary.get("oldest_task") and summary["oldest_task"]["age_days"] > 3:
                recommendations.append(f"{len(recommendations) + 1}. Review oldest task ({summary['oldest_task']['age_days']:.1f} days old)")

            if summary["total_tasks"] > 20:
                recommendations.append(f"{len(recommendations) + 1}. High task volume ({summary['total_tasks']} tasks) - consider increasing automation")

            if not recommendations:
                recommendations.append("✅ Task queue is manageable - continue monitoring")

            for rec in recommendations:
                dashboard += f"{rec}\n"

            dashboard += f"""
---

*Generated by Cross-Domain Integration Module*
*Part of Gold Tier Implementation - Hackathon FTE*
"""

            return dashboard

        except Exception as e:
            logger.error(f"Error generating unified dashboard: {e}")
            return None

    def save_dashboard(self, dashboard):
        """Save dashboard to file"""
        try:
            filepath = Path("Dashboard_Unified.md")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(dashboard)

            logger.info(f"Unified dashboard saved: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Error saving dashboard: {e}")
            return None


def generate_unified_dashboard():
    """Generate and save unified cross-domain dashboard"""
    integrator = CrossDomainIntegrator()
    dashboard = integrator.generate_unified_dashboard()

    if dashboard:
        filepath = integrator.save_dashboard(dashboard)
        return filepath
    else:
        return None


def get_prioritized_task_list():
    """Get prioritized task list across all domains"""
    integrator = CrossDomainIntegrator()
    return integrator.get_unified_task_list()


def get_domain_summary():
    """Get summary of tasks by domain"""
    integrator = CrossDomainIntegrator()
    return integrator.get_domain_summary()


if __name__ == "__main__":
    print("=" * 60)
    print("Cross-Domain Integration Test")
    print("=" * 60)
    print()

    print("Generating unified dashboard...")
    filepath = generate_unified_dashboard()

    if filepath:
        print(f"\n✅ Dashboard generated successfully!")
        print(f"📄 File: {filepath}")
        print()

        # Display the dashboard
        with open(filepath, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("\n❌ Failed to generate dashboard")

    print()
    print("=" * 60)
    print("Getting domain summary...")
    print("=" * 60)
    print()

    summary = get_domain_summary()
    print(json.dumps(summary, indent=2, default=str))

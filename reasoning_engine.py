#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reasoning Engine with Plan.md Generation

Creates structured Plan.md files for complex multi-step tasks.
Implements Claude reasoning loop for task breakdown and planning.
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))
from skills import AISkills


class ReasoningEngine:
    """Generates structured plans for complex tasks."""

    def __init__(self, vault_path: str = "."):
        self.vault_path = Path(vault_path)
        self.plans_folder = self.vault_path / 'Plans'
        self.ai_skills = AISkills(vault_path)

        # Create Plans folder if it doesn't exist
        self.plans_folder.mkdir(exist_ok=True)

    def analyze_task_complexity(self, task_description: str) -> Dict[str, any]:
        """
        Analyze a task to determine its complexity.

        Args:
            task_description: Description of the task

        Returns:
            Dictionary with complexity analysis
        """
        # Simple heuristics for complexity
        word_count = len(task_description.split())
        has_multiple_steps = any(word in task_description.lower()
                                for word in ['and', 'then', 'after', 'next', 'also'])
        has_dependencies = any(word in task_description.lower()
                              for word in ['before', 'after', 'depends', 'requires'])

        complexity_score = 0
        if word_count > 50:
            complexity_score += 2
        if has_multiple_steps:
            complexity_score += 2
        if has_dependencies:
            complexity_score += 1

        return {
            'complexity_score': complexity_score,
            'is_complex': complexity_score >= 3,
            'word_count': word_count,
            'has_multiple_steps': has_multiple_steps,
            'has_dependencies': has_dependencies
        }

    def break_down_task(self, task_description: str) -> List[Dict[str, str]]:
        """
        Break down a complex task into smaller steps.

        Args:
            task_description: Description of the task

        Returns:
            List of steps with details
        """
        # In production, this would use Claude API for intelligent breakdown
        # For now, we'll use a simple heuristic approach

        steps = []

        # Default breakdown pattern
        steps.append({
            'step': 1,
            'title': 'Analyze Requirements',
            'description': 'Review and understand all requirements for the task',
            'estimated_time': '15-30 minutes',
            'dependencies': []
        })

        steps.append({
            'step': 2,
            'title': 'Research and Planning',
            'description': 'Research necessary information and create detailed plan',
            'estimated_time': '30-60 minutes',
            'dependencies': [1]
        })

        steps.append({
            'step': 3,
            'title': 'Implementation',
            'description': 'Execute the main task according to the plan',
            'estimated_time': '1-2 hours',
            'dependencies': [2]
        })

        steps.append({
            'step': 4,
            'title': 'Testing and Verification',
            'description': 'Test the implementation and verify it meets requirements',
            'estimated_time': '30 minutes',
            'dependencies': [3]
        })

        steps.append({
            'step': 5,
            'title': 'Documentation and Completion',
            'description': 'Document the work and mark task as complete',
            'estimated_time': '15 minutes',
            'dependencies': [4]
        })

        return steps

    def generate_plan(self, task_title: str, task_description: str,
                     priority: str = "medium") -> str:
        """
        Generate a Plan.md file for a complex task.

        Args:
            task_title: Title of the task
            task_description: Detailed description
            priority: Priority level (low/medium/high)

        Returns:
            Path to created Plan.md file
        """
        # Analyze complexity
        complexity = self.analyze_task_complexity(task_description)

        # Break down into steps
        steps = self.break_down_task(task_description)

        # Generate plan filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_title = task_title.replace(' ', '_').replace('/', '_')[:50]
        filename = f"PLAN_{timestamp}_{safe_title}.md"
        plan_path = self.plans_folder / filename

        # Build steps section
        steps_content = ""
        for step in steps:
            deps = ", ".join([f"Step {d}" for d in step['dependencies']]) if step['dependencies'] else "None"
            steps_content += f"""
### Step {step['step']}: {step['title']}

**Description**: {step['description']}

**Estimated Time**: {step['estimated_time']}

**Dependencies**: {deps}

**Status**: [ ] Not Started

**Notes**:
-

---
"""

        # Create plan content
        content = f"""---
type: plan
title: {task_title}
priority: {priority}
created_at: {datetime.now().isoformat()}
status: planning
complexity_score: {complexity['complexity_score']}
---

# Plan: {task_title}

## Overview

**Created**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Priority**: {priority.upper()}
**Complexity**: {'High' if complexity['is_complex'] else 'Low to Medium'}

## Task Description

{task_description}

## Complexity Analysis

- **Word Count**: {complexity['word_count']}
- **Multiple Steps**: {'Yes' if complexity['has_multiple_steps'] else 'No'}
- **Has Dependencies**: {'Yes' if complexity['has_dependencies'] else 'No'}
- **Complexity Score**: {complexity['complexity_score']}/5

## Execution Plan

{steps_content}

## Success Criteria

- [ ] All steps completed successfully
- [ ] Requirements met
- [ ] Testing passed
- [ ] Documentation complete
- [ ] Task moved to Done folder

## Risk Assessment

**Potential Risks**:
1. Scope creep - Keep focused on original requirements
2. Time overrun - Monitor progress against estimates
3. Dependencies - Ensure all prerequisites are met

**Mitigation Strategies**:
- Regular progress checks
- Clear communication
- Flexible timeline adjustments

## Resources Needed

- Time allocation as per estimates
- Access to necessary tools and systems
- Reference to Company Handbook for guidelines

## Progress Tracking

| Step | Status | Started | Completed | Notes |
|------|--------|---------|-----------|-------|
| 1    | ⏳     |         |           |       |
| 2    | ⏳     |         |           |       |
| 3    | ⏳     |         |           |       |
| 4    | ⏳     |         |           |       |
| 5    | ⏳     |         |           |       |

**Legend**: ⏳ Pending | 🔄 In Progress | ✅ Complete | ❌ Blocked

## Notes and Updates

### {datetime.now().strftime('%Y-%m-%d')}
- Plan created and ready for execution
- Awaiting approval to begin

---

## Next Actions

1. Review this plan
2. Approve or request modifications
3. Begin execution with Step 1
4. Update progress as you work
5. Mark steps complete as you finish them

---

*Generated by Reasoning Engine*
*This is a living document - update as you progress*
"""

        # Write plan file
        with open(plan_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Log the activity
        self.ai_skills.log_activity(
            activity_type="plan_generated",
            description=f"Generated plan for: {task_title}",
            details={
                "plan_file": filename,
                "complexity_score": complexity['complexity_score'],
                "steps_count": len(steps)
            }
        )

        return str(plan_path)

    def update_plan_progress(self, plan_file: Path, step_number: int,
                           status: str, notes: str = "") -> bool:
        """
        Update progress on a plan.

        Args:
            plan_file: Path to plan file
            step_number: Step number to update
            status: New status (pending/in_progress/complete/blocked)
            notes: Optional notes

        Returns:
            True if successful
        """
        if not plan_file.exists():
            return False

        # Read current content
        with open(plan_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update status (simplified - in production would parse and update properly)
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        update_note = f"\n### {timestamp}\n- Step {step_number}: {status}\n- {notes}\n"

        # Append to notes section
        content += update_note

        # Write back
        with open(plan_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return True


# Convenience functions
def generate_plan(task_title: str, task_description: str, priority: str = "medium") -> str:
    """Generate a plan for a complex task."""
    engine = ReasoningEngine()
    return engine.generate_plan(task_title, task_description, priority)

def analyze_task(task_description: str) -> Dict:
    """Analyze task complexity."""
    engine = ReasoningEngine()
    return engine.analyze_task_complexity(task_description)


# Demo
if __name__ == "__main__":
    print("=" * 70)
    print("  REASONING ENGINE DEMO")
    print("=" * 70)

    engine = ReasoningEngine()

    # Demo: Generate a plan
    print("\n[DEMO] Generating plan for complex task...")

    task_title = "Implement Email Automation System"
    task_description = """
    Create a complete email automation system that monitors Gmail inbox,
    processes incoming emails, generates appropriate responses, and sends
    them after human approval. The system should integrate with the existing
    AI Employee infrastructure and follow all Company Handbook rules.
    """

    plan_path = engine.generate_plan(task_title, task_description, priority="high")

    print(f"\n[OK] Plan generated: {plan_path}")
    print("\nPlan preview:")
    print("-" * 70)

    with open(plan_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()[:30]
        print(''.join(lines))

    print("-" * 70)
    print("\n[INFO] Full plan saved to Plans/ folder")
    print("[INFO] Review the plan and start execution!")

"""
Ralph Wiggum Loop - Autonomous Task Completion

The Ralph Wiggum loop implements a "stop hook" pattern that keeps Claude Code
iterating until multi-step tasks are complete. Named after the Simpsons character
who famously said "I'm helping!" and keeps going.

This module provides:
- Autonomous task execution loop
- Task completion checking
- Progress tracking
- Safety mechanisms to prevent infinite loops
- Integration with Claude Code Agent Skills
"""

from ralph_wiggum.stop_hook import RalphWiggumLoop, create_task_from_file
from ralph_wiggum.task_completion import TaskCompletionChecker
from ralph_wiggum.ralph_skills import (
    RalphWiggumSkills,
    run_autonomous_task,
    check_task_status,
    get_next_action,
    mark_task_complete,
    list_incomplete_tasks,
    process_all_tasks
)

__all__ = [
    'RalphWiggumLoop',
    'TaskCompletionChecker',
    'RalphWiggumSkills',
    'create_task_from_file',
    'run_autonomous_task',
    'check_task_status',
    'get_next_action',
    'mark_task_complete',
    'list_incomplete_tasks',
    'process_all_tasks'
]

__version__ = '1.0.0'

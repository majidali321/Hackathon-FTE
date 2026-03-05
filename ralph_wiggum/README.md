# Ralph Wiggum Loop - Autonomous Task Completion

## Overview

The Ralph Wiggum Loop is the autonomous execution engine that keeps your AI Employee working until tasks are complete. Named after the Simpsons character who famously said "I'm helping!" and keeps going, this system implements a "stop hook" pattern that enables true autonomous operation.

## What It Does

The Ralph Wiggum Loop:
- **Continuously iterates** on tasks until completion
- **Checks progress** after each step
- **Prevents infinite loops** with safety mechanisms
- **Handles approvals** by pausing when human input is needed
- **Tracks execution** with detailed logging
- **Integrates with Claude Code** as Agent Skills

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    RALPH WIGGUM LOOP                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  1. Load Task from Needs_Action                             │
│     - Parse task file                                        │
│     - Extract steps from checkboxes                          │
│     - Identify approval requirements                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  2. Check if Should Continue                                │
│     - Max iterations not reached?                            │
│     - Task not complete?                                     │
│     - Not blocked?                                           │
│     - Not waiting for approval?                              │
│     - Remaining steps exist?                                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  3. Execute Next Step                                       │
│     - Get next uncompleted step                              │
│     - Execute appropriate skill/action                       │
│     - Handle errors with retry logic                         │
│     - Update progress                                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  4. Update Task Status                                      │
│     - Mark step as complete                                  │
│     - Update task file                                       │
│     - Log iteration results                                  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ↓
                    Loop back to step 2
                            │
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  5. Task Complete                                           │
│     - Move to Done folder                                    │
│     - Generate execution summary                             │
│     - Save detailed logs                                     │
└─────────────────────────────────────────────────────────────┘
```

## Components

### 1. RalphWiggumLoop (`stop_hook.py`)
The main autonomous execution loop.

**Key Methods:**
- `should_continue()` - Determines if loop should continue
- `execute_iteration()` - Executes one iteration
- `run()` - Main loop execution

**Safety Features:**
- Maximum iteration limit (default: 50)
- Timeout detection
- Error handling and recovery
- Approval detection and pause

### 2. TaskCompletionChecker (`task_completion.py`)
Checks task completion status and determines next actions.

**Key Methods:**
- `check_task_completion()` - Check if task is complete
- `get_next_action()` - Determine next action needed
- `mark_task_complete()` - Mark task as done
- `get_all_incomplete_tasks()` - List all incomplete tasks

**Completion Criteria:**
- All checkboxes marked [x]
- Status field set to "complete"
- Task moved to Done folder
- Explicit completion indicators in content

### 3. RalphWiggumSkills (`ralph_skills.py`)
Agent Skills for Claude Code integration.

**Available Skills:**
- `run_autonomous_task()` - Run a task autonomously
- `check_task_status()` - Check task status
- `get_next_action()` - Get next action
- `mark_task_complete()` - Mark as complete
- `list_incomplete_tasks()` - List all incomplete tasks
- `process_all_tasks()` - Process all tasks autonomously

## Usage

### Basic Usage

```python
from ralph_wiggum import run_autonomous_task

# Run a single task autonomously
result = run_autonomous_task('TASK_20260305_123456_Example_Task.md')

print(f"Status: {result['status']}")
print(f"Iterations: {result['iterations']}")
```

### Check Task Status

```python
from ralph_wiggum import check_task_status

status = check_task_status('TASK_20260305_123456_Example_Task.md')

print(f"Complete: {status['complete']}")
print(f"Progress: {status['progress']*100:.1f}%")
print(f"Remaining: {len(status['remaining_steps'])} steps")
```

### Process All Tasks

```python
from ralph_wiggum import process_all_tasks

# Process all incomplete tasks
result = process_all_tasks(max_iterations_per_task=20)

print(f"Processed: {result['total_tasks']} tasks")
print(f"Completed: {result['completed']}")
print(f"Failed: {result['failed']}")
```

### List Incomplete Tasks

```python
from ralph_wiggum import list_incomplete_tasks

tasks = list_incomplete_tasks()

for task in tasks['tasks']:
    print(f"{task['filename']}: {task['progress']*100:.1f}% complete")
```

## Integration with Claude Code

The Ralph Wiggum Loop integrates seamlessly with Claude Code as Agent Skills:

```python
# In your Claude Code session
from ralph_wiggum import ralph_skills

# Process all pending tasks autonomously
result = ralph_skills.process_all_tasks()
```

## Task File Format

Tasks must follow this format for the loop to work:

```markdown
---
type: task
title: Example Task
priority: high
status: pending
---

# Example Task

## Description
Task description here

## Steps
- [ ] Step 1: Do something
- [ ] Step 2: Do something else
- [ ] Step 3: Send email (requires approval)
- [ ] Step 4: Mark as complete

## Notes
Additional notes
```

## Safety Mechanisms

### 1. Maximum Iterations
Prevents infinite loops by limiting iterations (default: 50).

### 2. Approval Detection
Automatically pauses when steps require human approval:
- Keywords: "approval", "send", "post", "payment"
- Explicit `requires_approval: true` in step metadata

### 3. Error Handling
- Catches and logs all errors
- Continues with next step on non-critical errors
- Stops on critical errors

### 4. Progress Tracking
- Logs every iteration
- Tracks time per step
- Generates execution summaries

## Execution Logs

Logs are saved to `Logs/ralph_wiggum/execution_TIMESTAMP.json`:

```json
{
  "task": "Example Task",
  "start_time": "2026-03-05T16:20:22.123456",
  "end_time": "2026-03-05T16:22:15.654321",
  "duration_seconds": 113.53,
  "iterations": 8,
  "final_status": "complete",
  "history": [
    {
      "iteration": 1,
      "step": "Read task requirements",
      "result": "success",
      "duration": 2.5,
      "timestamp": "2026-03-05T16:20:24.623456"
    }
  ]
}
```

## Testing

### Test Individual Components

```bash
# Test the main loop
python ralph_wiggum/stop_hook.py

# Test task completion checker
python ralph_wiggum/task_completion.py

# Test skills integration
python ralph_wiggum/ralph_skills.py
```

### Test with Real Tasks

```python
from ralph_wiggum import RalphWiggumLoop, create_task_from_file
from pathlib import Path

# Load a real task
task_file = Path('Needs_Action/TASK_20260305_123456_Example.md')
task_data = create_task_from_file(task_file)

# Run the loop
loop = RalphWiggumLoop(max_iterations=10)
result = loop.run(task_data)
```

## Configuration

### Adjust Maximum Iterations

```python
from ralph_wiggum import RalphWiggumLoop

loop = RalphWiggumLoop(max_iterations=100)  # Allow more iterations
```

### Custom Vault Path

```python
from ralph_wiggum import RalphWiggumSkills

skills = RalphWiggumSkills(vault_path='/path/to/vault')
```

## Best Practices

1. **Break tasks into clear steps** - Use checkboxes for each step
2. **Mark approval steps** - Include "approval" in step description
3. **Set reasonable iteration limits** - Start with 20-50 iterations
4. **Monitor execution logs** - Review logs for optimization
5. **Handle errors gracefully** - Add error recovery steps
6. **Test with simple tasks first** - Validate before complex tasks

## Troubleshooting

### Loop Stops Too Early
- Check max_iterations setting
- Verify task has remaining steps
- Check for approval requirements

### Loop Runs Forever
- Reduce max_iterations
- Add explicit completion criteria
- Check for circular dependencies

### Steps Not Executing
- Verify step format (checkbox syntax)
- Check skill implementations
- Review error logs

## Future Enhancements

- [ ] Dynamic iteration limit based on task complexity
- [ ] Parallel step execution for independent steps
- [ ] Learning from past executions
- [ ] Automatic retry with exponential backoff
- [ ] Integration with monitoring/alerting
- [ ] Performance optimization

## Related Documentation

- [Agent Skills](../skills.py) - Core AI Employee skills
- [Task Processor](../task_processor.py) - Task processing engine
- [Orchestrator](../orchestrator.py) - Main orchestration system

---

**Status**: ✅ Implemented and Tested
**Version**: 1.0.0
**Last Updated**: 2026-03-05

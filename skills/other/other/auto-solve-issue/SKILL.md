---
name: auto-solve-issue
version: "2.0.0"
description: |
  Complete issue lifecycle with Task dependencies and Subagents - true zero-pause automation.
  TRIGGER when: user wants fully automated issue resolution ("auto-solve issue #N", "solve issue completely").
  DO NOT TRIGGER when: user wants manual control (use /work-issue --interactive), or individual phases (use specific skills).
last-updated: "2026-03-18"
---

# Auto-Solve Issue v2.0 - Zero-Pause Automation

> Complete issue lifecycle using Task dependencies + Subagents architecture for truly continuous execution

## Overview

This skill provides **fully automated issue resolution** without manual intervention:

**What it does:**
1. **Creates Task dependency chain** - 5 tasks with blockedBy relationships
2. **Executes phases with Subagents** - Each phase runs in isolated context
3. **Validates at checkpoints** - Auto-continues if score ≥ 90
4. **Resumes from failures** - Checkpoint and resume mechanism
5. **Zero manual intervention** - Continuous loop until completion

**Why it's needed:**
solve-issue v1.0 had execution pauses requiring manual "continue" 3-4 times. The Python coordinator + AI executor architecture was incompatible with AI interaction patterns. This v2.0 uses Claude Code's Task system and Subagents for true zero-pause automation.

**When to use:**
- Need complete automation without checkpoints
- Issue is well-defined with high confidence
- Trust validation scores (eval-plan, review)

**Workflow:**
```
/auto-solve-issue #23 [--auto|--interactive]
  → Creates 5 tasks with dependencies
  → Phase 1: start-issue (Subagent)
  → Phase 1.5: eval-plan + checkpoint
  → Phase 2: execute-plan (Subagent)
  → Phase 2.5: review + checkpoint
  → Phase 3: finish-issue (Subagent)
  → All complete
```

## Arguments

```bash
/auto-solve-issue [issue-number] [options]
```

**Common usage:**
```bash
/auto-solve-issue #23              # Auto mode (score-based checkpoints)
/auto-solve-issue #23 --interactive # Stop at all checkpoints
/auto-solve-issue #23 --resume     # Resume from saved state
```

**Options:**
- `[issue-number]` - Required, which issue to solve
- `--auto` - Auto mode (default) - continues if score ≥ 90
- `--interactive` - Stop at checkpoints for manual review
- `--resume` - Resume from last checkpoint

## AI Execution Instructions

**CRITICAL: Task dependencies + Subagent execution pattern**

When executing `/auto-solve-issue`, AI MUST follow this pattern:

### Step 1: Create 5-Task Dependency Chain

```python
# Create 5 tasks representing the workflow phases
# Each task includes metadata for checkpoints and phase tracking

# Phase 1: Start Issue
task1 = TaskCreate(
    subject="Phase 1: start-issue",
    description="Create branch, generate plan, sync with main",
    activeForm="Creating branch and plan",
    metadata={
        "phase": "1",
        "skill": "start-issue",
        "checkpoint": False,
        "issue_number": issue_number
    }
)

# Phase 1.5: Evaluate Plan (with checkpoint)
task2 = TaskCreate(
    subject="Phase 1.5: eval-plan",
    description="Validate implementation plan (score must be ≥ 90 for auto-continue)",
    activeForm="Evaluating plan",
    metadata={
        "phase": "1.5",
        "skill": "eval-plan",
        "checkpoint": True,
        "checkpoint_name": "Checkpoint 1",
        "score_threshold": 90,
        "issue_number": issue_number
    }
)
# Block Phase 1.5 until Phase 1 completes
TaskUpdate(task2.id, addBlockedBy=[task1.id])

# Phase 2: Execute Plan
task3 = TaskCreate(
    subject="Phase 2: execute-plan",
    description="Implement all tasks from plan",
    activeForm="Executing implementation plan",
    metadata={
        "phase": "2",
        "skill": "execute-plan",
        "checkpoint": False,
        "issue_number": issue_number
    }
)
# Block Phase 2 until Phase 1.5 completes (including checkpoint)
TaskUpdate(task3.id, addBlockedBy=[task2.id])

# Phase 2.5: Review Code (with checkpoint)
task4 = TaskCreate(
    subject="Phase 2.5: review",
    description="Validate code quality (score must be ≥ 90 for auto-continue)",
    activeForm="Reviewing code quality",
    metadata={
        "phase": "2.5",
        "skill": "review",
        "checkpoint": True,
        "checkpoint_name": "Checkpoint 2",
        "score_threshold": 90,
        "issue_number": issue_number
    }
)
# Block Phase 2.5 until Phase 2 completes
TaskUpdate(task4.id, addBlockedBy=[task3.id])

# Phase 3: Finish Issue
task5 = TaskCreate(
    subject="Phase 3: finish-issue",
    description="Commit, create PR, merge, close issue",
    activeForm="Finishing issue",
    metadata={
        "phase": "3",
        "skill": "finish-issue",
        "checkpoint": False,
        "issue_number": issue_number
    }
)
# Block Phase 3 until Phase 2.5 completes (including checkpoint)
TaskUpdate(task5.id, addBlockedBy=[task4.id])

# Store task IDs for main loop
task_ids = [task1.id, task2.id, task3.id, task4.id, task5.id]
```

**Key Design Decisions:**

1. **Dependency Chain**: Each task blocks the next, creating a sequential workflow
2. **Metadata**: Stores phase number, skill name, checkpoint flag, score threshold
3. **Checkpoints**: Phases 1.5 and 2.5 are checkpoints with score validation
4. **Auto-unlock**: When a task completes, the next task automatically becomes available

### Step 2: Find Next Available Task

```python
def find_next_available_task(task_ids: list[str]) -> dict | None:
    """
    查找下一个可用任务（pending 且无 blockedBy 的任务）

    Args:
        task_ids: 所有工作流任务的 ID 列表

    Returns:
        下一个可用任务的详细信息，如果没有则返回 None
        返回格式: {
            "id": str,
            "subject": str,
            "status": str,
            "metadata": dict,
            "blockedBy": list
        }
    """
    # 获取所有任务的当前状态
    all_tasks = TaskList()

    # 过滤出我们创建的工作流任务
    workflow_tasks = [t for t in all_tasks if t.id in task_ids]

    # 查找第一个 pending 且无 blockedBy 的任务
    for task in workflow_tasks:
        # 跳过已完成的任务
        if task.status == "completed":
            continue

        # 跳过有阻塞依赖的任务
        if task.blockedBy and len(task.blockedBy) > 0:
            # 检查是否所有阻塞任务都已完成
            all_blockers_done = True
            for blocker_id in task.blockedBy:
                blocker = next((t for t in workflow_tasks if t.id == blocker_id), None)
                if blocker and blocker.status != "completed":
                    all_blockers_done = False
                    break

            # 如果还有未完成的阻塞任务，跳过
            if not all_blockers_done:
                continue

        # 找到了下一个可用任务
        return {
            "id": task.id,
            "subject": task.subject,
            "status": task.status,
            "metadata": task.metadata,
            "blockedBy": task.blockedBy
        }

    # 没有找到可用任务
    return None
```

**Logic Explanation:**

1. **Get current state**: Use TaskList() to fetch all tasks
2. **Filter workflow tasks**: Only consider our 5 created tasks
3. **Find available task**:
   - Status must be "pending" (not "completed")
   - No blockedBy dependencies, OR all blockers are completed
4. **Return first match**: The task that's ready to execute

**Edge Cases:**
- All tasks completed → return None (workflow done)
- Tasks still blocked → return None (wait for blocker to complete)
- Task in_progress → skip it (shouldn't happen in normal flow)

### Step 3: Execute with Subagent

```python
def execute_with_subagent(task: dict, mode: str) -> dict:
    """
    使用 Subagent 执行指定的 skill

    Args:
        task: 任务详细信息（包含 metadata 中的 skill 名称）
        mode: 执行模式 ("auto" 或 "interactive")

    Returns:
        执行结果 {
            "success": bool,
            "score": int | None,  # For checkpoint phases
            "error": str | None
        }
    """
    skill_name = task["metadata"]["skill"]
    issue_number = task["metadata"]["issue_number"]
    is_checkpoint = task["metadata"].get("checkpoint", False)

    # 构建 skill 参数
    if skill_name == "eval-plan":
        skill_args = f"{issue_number} --mode={mode}"
    elif skill_name == "review":
        skill_args = ""  # review 自动检测当前分支
    elif skill_name in ["start-issue", "execute-plan", "finish-issue"]:
        skill_args = str(issue_number)
    else:
        skill_args = str(issue_number)

    # 启动 Subagent 执行 skill
    try:
        # 使用 Task tool 启动 subagent
        result = Task(
            subagent_type="general-purpose",
            description=f"Execute {skill_name}",
            prompt=f"Execute /{skill_name} {skill_args}",
            model="sonnet",  # 使用 sonnet 确保质量
            max_turns=30  # 60 minutes timeout (2 min per turn)
        )

        # 如果是 checkpoint phase，读取 score
        score = None
        if is_checkpoint:
            if skill_name == "eval-plan":
                score = read_eval_plan_score()
            elif skill_name == "review":
                score = read_review_score()

        return {
            "success": True,
            "score": score,
            "error": None
        }

    except Exception as e:
        # Subagent 执行失败
        return {
            "success": False,
            "score": None,
            "error": str(e)
        }


def read_eval_plan_score() -> int | None:
    """从 .claude/.eval-plan-status.json 读取分数"""
    try:
        status_file = ".claude/.eval-plan-status.json"
        with open(status_file, "r") as f:
            data = json.load(f)
            return data.get("score")
    except:
        return None


def read_review_score() -> int | None:
    """从 .claude/.review-status.json 读取分数"""
    try:
        status_file = ".claude/.review-status.json"
        with open(status_file, "r") as f:
            data = json.load(f)
            return data.get("score")
    except:
        return None
```

**Key Design Points:**

1. **Subagent Isolation**: Each phase runs in independent context
   - No context pollution between phases
   - Clean execution environment
   - Separate error handling

2. **Skill Arguments**: Customize args per skill
   - eval-plan: Needs --mode=auto/interactive
   - review: Auto-detects current branch
   - Others: Just need issue number

3. **Timeout**: max_turns=30 = ~60 minutes per phase
   - Prevents infinite loops
   - Allows complex phases to complete
   - Can be adjusted based on testing

4. **Score Reading**: For checkpoint phases
   - eval-plan writes .eval-plan-status.json
   - review writes .review-status.json
   - Read after subagent completes

5. **Error Handling**: Return structured result
   - success flag indicates completion
   - score extracted for checkpoints
   - error message captured

### Step 4: Main Execution Loop

```python
# Check if resuming from previous run
if resume_flag:
    resume_data = load_resume_point()

    if resume_data:
        # Resume workflow from saved state
        context = resume_workflow(resume_data)
        task_ids = context["task_ids"]
        mode = context["mode"]
        issue_number = context["issue_number"]
    else:
        print("⚠️ No resume point found, starting fresh")
        # Continue with fresh start (task_ids already created)
else:
    # Fresh start - task_ids already created in Step 1
    pass

# Main workflow loop - continues until all phases complete
while True:
    # 1. Find next available task
    next_task = find_next_available_task(task_ids)

    # 2. Check if workflow complete
    if next_task is None:
        # All tasks completed
        print("✅ All phases completed!")
        cleanup_state_files()
        break

    # 3. Display current phase
    phase = next_task["metadata"]["phase"]
    skill = next_task["metadata"]["skill"]
    is_checkpoint = next_task["metadata"].get("checkpoint", False)

    print(f"\n📋 Executing Phase {phase}: {skill}")

    # 4. Mark task as in_progress
    TaskUpdate(next_task["id"], status="in_progress")

    # 5. Execute with subagent
    result = execute_with_subagent(next_task, mode)

    # 6. Check execution result
    if not result["success"]:
        # Execution failed
        print(f"❌ Phase {phase} failed: {result['error']}")

        # Increment retry count
        retry_count = next_task["metadata"].get("retry_count", 0)
        retry_count += 1

        if retry_count >= 3:
            # Max retries exceeded
            print(f"❌ Max retries (3) exceeded for Phase {phase}")
            save_resume_point(next_task["id"], "max_retries_exceeded")
            break
        else:
            # Retry
            print(f"⚠️ Retrying Phase {phase} (attempt {retry_count + 1}/3)")
            TaskUpdate(
                next_task["id"],
                status="pending",
                metadata={"retry_count": retry_count}
            )
            continue

    # 7. Handle checkpoint phases
    if is_checkpoint:
        score = result["score"]
        threshold = next_task["metadata"]["score_threshold"]
        checkpoint_name = next_task["metadata"]["checkpoint_name"]

        print(f"\n⏸️ {checkpoint_name}")
        print(f"   Score: {score}/100")
        print(f"   Threshold: {threshold}")

        if score is None:
            # Score not available
            print(f"⚠️ Score not available, treating as checkpoint")
            if mode == "auto":
                # Auto mode requires score
                save_resume_point(next_task["id"], "score_unavailable")
                print(f"⏸️ Stopping - fix issue and use --resume")
                break
            else:
                # Interactive mode - ask user
                user_decision = ask_user_to_continue()
                if user_decision != "continue":
                    save_resume_point(next_task["id"], "user_stopped")
                    break

        elif score < threshold:
            # Score below threshold
            print(f"⚠️ Score {score} < {threshold}")

            if mode == "auto":
                # Auto mode stops on low score
                save_resume_point(next_task["id"], "score_below_threshold")
                print(f"\n⏸️ Stopping at {checkpoint_name}")
                print(f"   Score {score}/100 is below threshold {threshold}")
                print(f"   Fix issues and resume: /auto-solve-issue #{issue_number} --resume")
                break
            else:
                # Interactive mode - ask user
                user_decision = ask_user_to_continue()
                if user_decision != "continue":
                    save_resume_point(next_task["id"], "user_stopped")
                    break

        else:
            # Score ≥ threshold
            print(f"✅ Score {score} ≥ {threshold} - auto-continuing")

    # 8. Mark task as completed
    TaskUpdate(next_task["id"], status="completed")
    print(f"✅ Phase {phase} completed")

# Workflow complete or stopped
if next_task is None:
    print("\n🎉 Issue lifecycle complete!")
    print(f"   Issue #{issue_number} resolved")
    print(f"   All phases executed successfully")
else:
    print(f"\n⏸️ Workflow paused at Phase {phase}")
    print(f"   Resume with: /auto-solve-issue #{issue_number} --resume")
```

**Loop Flow:**

1. **Find next task**: Check which task is ready (pending + no blockers)
2. **Completion check**: If none found, all tasks are done
3. **Display phase**: Show current phase to user
4. **Mark in progress**: Update task status
5. **Execute subagent**: Run the skill in isolated context
6. **Error handling**: Retry up to 3 times, then save resume point
7. **Checkpoint logic**:
   - Auto mode: Stop if score < 90
   - Interactive mode: Always ask user
   - Continue if score ≥ 90
8. **Mark completed**: Task done, dependency automatically unlocks next task

**Key Features:**

- **Continuous execution**: Loop continues until all tasks done or checkpoint stops
- **Auto-unlock**: Completing a task automatically unblocks the next
- **Retry logic**: Failed phases retry up to 3 times
- **Checkpoint validation**: Score-based decision in auto mode
- **Resume points**: Save state when stopping for resume later

### Step 5: Checkpoint Checks

```python
def check_checkpoint(checkpoint_name: str, mode: str) -> dict:
    """
    检查 checkpoint 分数并决定是否继续

    Args:
        checkpoint_name: "Checkpoint 1" (eval-plan) 或 "Checkpoint 2" (review)
        mode: "auto" 或 "interactive"

    Returns:
        {
            "should_continue": bool,
            "score": int | None,
            "reason": str
        }
    """
    # 根据 checkpoint 名称读取相应的状态文件
    if checkpoint_name == "Checkpoint 1":
        status_file = ".claude/.eval-plan-status.json"
        skill_name = "eval-plan"
    elif checkpoint_name == "Checkpoint 2":
        status_file = ".claude/.review-status.json"
        skill_name = "review"
    else:
        return {
            "should_continue": False,
            "score": None,
            "reason": f"Unknown checkpoint: {checkpoint_name}"
        }

    # 读取状态文件
    try:
        with open(status_file, "r") as f:
            data = json.load(f)

        score = data.get("score")
        status = data.get("status")

        # 验证 valid_until 时间戳（状态文件有效期 90 分钟）
        valid_until = data.get("valid_until")
        if valid_until:
            from datetime import datetime
            valid_time = datetime.fromisoformat(valid_until)
            now = datetime.now()
            if now > valid_time:
                return {
                    "should_continue": False,
                    "score": score,
                    "reason": f"{skill_name} status expired - re-run {skill_name}"
                }

    except FileNotFoundError:
        return {
            "should_continue": False,
            "score": None,
            "reason": f"Status file not found: {status_file}"
        }
    except json.JSONDecodeError:
        return {
            "should_continue": False,
            "score": None,
            "reason": f"Invalid JSON in {status_file}"
        }

    # 判断是否继续
    threshold = 90

    if score is None:
        # 分数不可用
        if mode == "auto":
            return {
                "should_continue": False,
                "score": None,
                "reason": "Score unavailable in auto mode"
            }
        else:
            # Interactive mode - 让用户决定
            return {
                "should_continue": ask_user_to_continue() == "continue",
                "score": None,
                "reason": "User decision (score unavailable)"
            }

    elif score < threshold:
        # 分数低于阈值
        if mode == "auto":
            return {
                "should_continue": False,
                "score": score,
                "reason": f"Score {score} < {threshold} (auto mode)"
            }
        else:
            # Interactive mode - 让用户决定
            return {
                "should_continue": ask_user_to_continue() == "continue",
                "score": score,
                "reason": f"User decision (score {score} < {threshold})"
            }

    else:
        # 分数 >= 阈值
        return {
            "should_continue": True,
            "score": score,
            "reason": f"Score {score} ≥ {threshold}"
        }


def ask_user_to_continue() -> str:
    """
    在 interactive mode 下询问用户是否继续

    Returns:
        "continue" 或 "stop"
    """
    # 使用 AskUserQuestion tool
    response = AskUserQuestion(
        questions=[{
            "question": "Continue to next phase?",
            "header": "Checkpoint",
            "options": [
                {
                    "label": "Continue",
                    "description": "Proceed to next phase despite issues"
                },
                {
                    "label": "Stop",
                    "description": "Pause workflow to fix issues"
                }
            ],
            "multiSelect": False
        }]
    )

    # Parse response
    if "Continue" in response.values():
        return "continue"
    else:
        return "stop"
```

**Checkpoint Logic:**

1. **Status File Reading**:
   - Checkpoint 1 → `.claude/.eval-plan-status.json`
   - Checkpoint 2 → `.claude/.review-status.json`
   - Validate timestamp (90-minute expiry)

2. **Score Validation**:
   - Score ≥ 90 → Continue automatically
   - Score < 90 in auto mode → Stop
   - Score < 90 in interactive mode → Ask user

3. **Edge Cases**:
   - File not found → Stop
   - Invalid JSON → Stop
   - Expired status → Stop (re-run needed)
   - Score unavailable → Stop in auto, ask in interactive

4. **User Decision** (Interactive Mode):
   - Use AskUserQuestion tool
   - Present continue/stop options
   - Return user's choice

### Step 6: Resume Mechanism

```python
def save_resume_point(task_id: str, reason: str):
    """
    保存当前工作流恢复点

    Args:
        task_id: 停止时的任务 ID
        reason: 停止原因（score_below_threshold, max_retries_exceeded等）
    """
    from datetime import datetime

    # 获取任务详细信息
    task = TaskGet(task_id)

    # 构建恢复点数据
    resume_data = {
        "timestamp": datetime.now().isoformat(),
        "issue_number": task.metadata.get("issue_number"),
        "stopped_at_task_id": task_id,
        "stopped_at_phase": task.metadata.get("phase"),
        "stopped_at_skill": task.metadata.get("skill"),
        "reason": reason,
        "task_ids": task_ids,  # 所有工作流任务的 ID
        "mode": mode  # auto 或 interactive
    }

    # 写入状态文件
    state_file = ".claude/.auto-solve-state.json"
    with open(state_file, "w") as f:
        json.dump(resume_data, f, indent=2)

    print(f"\n💾 Resume point saved:")
    print(f"   State file: {state_file}")
    print(f"   Stopped at: Phase {task.metadata.get('phase')}")
    print(f"   Reason: {reason}")
    print(f"\n   Resume with: /auto-solve-issue #{issue_number} --resume")


def load_resume_point() -> dict | None:
    """
    加载保存的恢复点

    Returns:
        恢复点数据，如果不存在则返回 None
    """
    state_file = ".claude/.auto-solve-state.json"

    try:
        with open(state_file, "r") as f:
            data = json.load(f)

        print(f"\n💾 Resume point found:")
        print(f"   Saved at: {data['timestamp']}")
        print(f"   Stopped at: Phase {data['stopped_at_phase']}")
        print(f"   Reason: {data['reason']}")

        return data

    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        print(f"⚠️ Invalid resume state file: {state_file}")
        return None


def resume_workflow(resume_data: dict):
    """
    从保存的恢复点继续执行工作流

    Args:
        resume_data: 从 load_resume_point() 加载的恢复点数据
    """
    # 提取恢复信息
    stopped_task_id = resume_data["stopped_at_task_id"]
    task_ids = resume_data["task_ids"]
    mode = resume_data["mode"]
    issue_number = resume_data["issue_number"]

    print(f"\n🔄 Resuming workflow...")
    print(f"   Issue: #{issue_number}")
    print(f"   Mode: {mode}")

    # 重置停止的任务状态为 pending
    # 这样 find_next_available_task() 会重新找到它
    TaskUpdate(stopped_task_id, status="pending")

    print(f"   Reset task {stopped_task_id} to pending")
    print(f"   Continuing execution loop...")

    # 返回恢复后的上下文
    return {
        "task_ids": task_ids,
        "mode": mode,
        "issue_number": issue_number,
        "resumed": True
    }


def cleanup_state_files():
    """
    清理工作流状态文件
    """
    import os

    state_files = [
        ".claude/.auto-solve-state.json",
        ".claude/.eval-plan-status.json",
        ".claude/.review-status.json"
    ]

    for file_path in state_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"   Cleaned: {file_path}")
        except Exception as e:
            print(f"   Warning: Failed to clean {file_path}: {e}")
```

**Resume Point Design:**

1. **State File**: `.claude/.auto-solve-state.json`
   - Stores current workflow state
   - Includes task IDs for all phases
   - Records reason for stopping

2. **Save Triggers**:
   - Checkpoint score < 90 (auto mode)
   - Max retries exceeded
   - User stops (interactive mode)
   - Score unavailable

3. **Resume Data**:
   - `stopped_at_task_id`: Which task to resume from
   - `task_ids`: All workflow task IDs
   - `reason`: Why it stopped
   - `mode`: Auto or interactive

4. **Cleanup**:
   - Remove state files on completion
   - Clean eval-plan and review status files
   - Ensures fresh start for next run

### Step 7: Error Handling and Retry Logic

**Error handling is integrated into the main loop (Step 4)** with these patterns:

```python
# 1. Subagent Execution Errors (in main loop)
try:
    result = execute_with_subagent(next_task, mode)
except Exception as e:
    # Unexpected error during subagent execution
    print(f"❌ Unexpected error in Phase {phase}: {e}")

    # Increment retry count
    retry_count = next_task["metadata"].get("retry_count", 0) + 1

    if retry_count >= 3:
        # Max retries exceeded
        save_resume_point(next_task["id"], f"error_max_retries: {str(e)}")
        break
    else:
        # Retry with updated metadata
        TaskUpdate(
            next_task["id"],
            status="pending",
            metadata={"retry_count": retry_count}
        )
        continue


# 2. Graceful Subagent Failures (returned by execute_with_subagent)
if not result["success"]:
    # Subagent reported failure (not exception)
    error_msg = result["error"]
    print(f"❌ Phase {phase} failed: {error_msg}")

    retry_count = next_task["metadata"].get("retry_count", 0) + 1

    if retry_count >= 3:
        save_resume_point(next_task["id"], f"failed_{skill}: {error_msg}")
        break
    else:
        print(f"⚠️ Retrying (attempt {retry_count + 1}/3)")
        TaskUpdate(
            next_task["id"],
            status="pending",
            metadata={"retry_count": retry_count}
        )
        continue


# 3. Checkpoint Score Unavailable
if is_checkpoint and score is None:
    print(f"⚠️ {checkpoint_name} score unavailable")

    if mode == "auto":
        save_resume_point(next_task["id"], "score_unavailable")
        print(f"⏸️ Fix {skill} and resume: /auto-solve-issue #{issue_number} --resume")
        break


# 4. Checkpoint Score Below Threshold
if is_checkpoint and score < threshold:
    print(f"⚠️ {checkpoint_name} score {score} < {threshold}")

    if mode == "auto":
        save_resume_point(next_task["id"], "score_below_threshold")
        print(f"⏸️ Fix issues and resume: /auto-solve-issue #{issue_number} --resume")
        break


# 5. Task System Errors
try:
    next_task = find_next_available_task(task_ids)
except Exception as e:
    print(f"❌ Error finding next task: {e}")
    save_resume_point(task_ids[0], f"task_system_error: {str(e)}")
    break
```

**Error Categories:**

| Error Type | Handling | Max Retries | Resume Point |
|------------|----------|-------------|--------------|
| **Subagent timeout** | Retry | 3 | After 3 failures |
| **Subagent exception** | Retry | 3 | After 3 failures |
| **Checkpoint score < 90** | Stop (auto mode) | N/A | Immediate |
| **Checkpoint score N/A** | Stop (auto mode) | N/A | Immediate |
| **Task system error** | Stop | N/A | Immediate |

**Retry Metadata:**

```python
metadata = {
    "retry_count": 0,  # Increments on each failure
    "last_error": str(e),  # Error message from last failure
    "retry_history": [
        {"attempt": 1, "error": "...", "timestamp": "..."},
        {"attempt": 2, "error": "...", "timestamp": "..."}
    ]
}
```

**Graceful Degradation:**

1. **Retry 3 times** - Give transient errors a chance
2. **Save resume point** - Never lose progress
3. **Clear error messages** - Tell user what to fix
4. **Preserve context** - Resume from exact checkpoint

## Architecture

### Core Innovation: Task Dependencies + Subagents

**Compared to solve-issue v1.0:**

| Dimension | v1.0 | v2.0 |
|-----------|------|------|
| **Orchestrator** | Python coordinator | AI + Task system |
| **Executor** | AI executor (passive loop) | Subagents (active) |
| **State Management** | JSON files | Task dependencies |
| **Context** | Shared session | Isolated per phase |
| **Resumability** | Timeout retry | Checkpoint + resume |

**Why this works:**
- ✅ AI maintains active control (no passive file reading)
- ✅ Task dependencies auto-unlock next phase
- ✅ Subagents isolate context (no bloat)
- ✅ Checkpoints provide safety (score validation)

## Workflow Steps

Copy this checklist to track progress:

```
Phase Progress:
- [ ] Phase 1: start-issue (create branch + plan)
- [ ] Phase 1.5: eval-plan (validate plan)
- [ ] Checkpoint 1: Score check (≥90 auto-continue)
- [ ] Phase 2: execute-plan (implementation)
- [ ] Phase 2.5: review (code quality)
- [ ] Checkpoint 2: Score check (≥90 auto-continue)
- [ ] Phase 3: finish-issue (commit + PR + merge)
```

Execute these phases in sequence using the main loop.

## Examples

### Example 1: Auto Mode (Score ≥ 90)

**User:** `/auto-solve-issue #23`

**Workflow:**
1. Create 5 tasks with dependencies
2. Phase 1: start-issue → Complete
3. Phase 1.5: eval-plan → Score: 95/100
4. Checkpoint 1: Auto-continue (score ≥ 90)
5. Phase 2: execute-plan → Complete
6. Phase 2.5: review → Score: 92/100
7. Checkpoint 2: Auto-continue (score ≥ 90)
8. Phase 3: finish-issue → Complete
9. Report success

**Time:** 35-65 minutes (no pauses)

### Example 2: Interactive Mode

**User:** `/auto-solve-issue #23 --interactive`

**Workflow:**
1-3. Same as auto mode
4. Checkpoint 1: Stop for user review
   - User reviews eval-plan results
   - User confirms continue
5-7. Same as auto mode
8. Checkpoint 2: Stop for user review
   - User reviews code quality
   - User confirms continue
9. Phase 3 completes

**Time:** 40-70 minutes + review time

### Example 3: Resume from Checkpoint

**User:** `/auto-solve-issue #23 --resume`

**Workflow:**
1. Load state from `.claude/.auto-solve-state.json`
2. Detect stopped at Checkpoint 1
3. User fixed plan (score now 95/100)
4. Continue from Phase 2
5. Execute remaining phases
6. Complete

**Time:** Depends on checkpoint location

## Performance

| Metric | solve-issue v1.0 | auto-solve-issue v2.0 | Improvement |
|--------|------------------|----------------------|-------------|
| **Pauses** | 5+ | 0-2 (checkpoints) | 60-100% reduction |
| **Total time** | 45-75 min | 35-65 min | 20-30% faster |
| **User intervention** | Multiple prompts | Checkpoints only | Cleaner UX |
| **Context usage** | Variable | < 50k tokens | Controlled |

## Error Handling

**Subagent timeout:**
```
⚠️ Subagent timeout in Phase 2

Options:
1. Retry: Automatically retry with new subagent
2. Resume: /auto-solve-issue #23 --resume
3. Manual: Complete phase manually, then resume
```

**Checkpoint failure (score < 90):**
```
⏸️ Checkpoint 1: Score 75/100 ≤ 90

Actions needed:
1. Review eval-plan results
2. Fix issues in plan
3. Resume: /auto-solve-issue #23 --resume
```

## Integration

**Comparison with work-issue:**

| Feature | work-issue | auto-solve-issue |
|---------|-----------|------------------|
| **Orchestration** | AI skill calls | Task dependencies |
| **Execution** | Skill tool | Subagents |
| **Pauses** | After each phase | Checkpoints only |
| **Maturity** | Stable | Experimental (v2.0) |
| **Use Case** | General | Maximum automation |

**When to use each:**
- work-issue: Default, stable, well-tested
- auto-solve-issue: Need maximum speed, trust automation

## Best Practices

1. **Use for well-defined issues** - Complex/vague issues may fail checkpoints
2. **Trust the scores** - Auto mode relies on eval-plan/review scores (≥90)
3. **Have fallback** - If issues occur, use /work-issue as backup
4. **Monitor first run** - Watch the continuous execution to build confidence
5. **Provide feedback** - Report bugs/issues to improve the skill

## Task Management

When executing, the skill creates this task structure:

```python
tasks = [
    TaskCreate("Phase 1: start-issue", ...),
    TaskCreate("Phase 1.5: eval-plan", ..., blockedBy=[task1]),
    TaskCreate("Phase 2: execute-plan", ..., blockedBy=[task2]),
    TaskCreate("Phase 2.5: review", ..., blockedBy=[task3]),
    TaskCreate("Phase 3: finish-issue", ..., blockedBy=[task4])
]
```

Updates status as each phase completes, automatically unlocking the next.

## Final Verification

```
- [ ] All 5 phases completed
- [ ] Both checkpoints passed (or manually approved)
- [ ] Issue closed on GitHub
- [ ] PR merged to main
- [ ] State files cleaned up
```

## Related Skills

- **/work-issue** - Stable alternative (AI orchestration)
- **/start-issue** - Phase 1 (called by this skill via subagent)
- **/eval-plan** - Phase 1.5 (called by this skill via subagent)
- **/execute-plan** - Phase 2 (called by this skill via subagent)
- **/review** - Phase 2.5 (called by this skill via subagent)
- **/finish-issue** - Phase 3 (called by this skill via subagent)

---

**Version:** 2.0.0
**Last Updated:** 2026-03-18
**Changelog:**
- v2.0.0 (2026-03-18): Major redesign - replace solve-issue v1.0 with auto-solve-issue v2.0 (Issue #258)

**Pattern:** Meta-Workflow Orchestrator (Task dependencies + Subagents)
**Status:** Experimental
**Compliance:** ADR-001 ✅

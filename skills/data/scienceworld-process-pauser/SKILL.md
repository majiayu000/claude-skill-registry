---
name: scienceworld-process-pauser
description: This skill introduces deliberate pauses in task execution. It should be triggered when the agent needs to consider next steps, evaluate intermediate results, or wait for processes to complete. The skill uses the 'wait1' or 'wait' actions to temporarily halt activity, preventing rushed decisions in complex experimental procedures.
---
# Skill: Process Pauser

## When to Use
Activate this skill when you need to:
* **Consider next steps** in a complex procedure.
* **Evaluate an intermediate result** (e.g., a mixed chemical, a partial assembly).
* **Wait for a simulated process** to complete.
* **Prevent rushed decisions** that could lead to errors.

## Core Actions
Use the following actions to implement a pause:
* `wait1`: Pauses execution for a single simulation step. Use for brief reflection.
* `wait`: Pauses execution for 10 simulation steps. Use for longer consideration or simulated waiting periods.

## Implementation Logic
1.  **Identify the Pause Trigger:** Recognize a moment requiring deliberation (e.g., after creating an intermediate product, before adding a new component).
2.  **Select Duration:** Choose `wait1` for quick checks or `wait` for extended evaluation.
3.  **Execute Pause:** Perform the selected wait action.
4.  **Resume:** Continue the task with the benefit of the reflective pause.

## Example from Trajectory
In the paint-mixing task, the agent used `wait1` after creating orange paint and before adding more red to make red-orange. This pause allowed for consideration of proportions and color adjustment.

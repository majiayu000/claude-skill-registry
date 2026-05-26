---
name: alfworld-receptacle-operator
description: This skill opens or closes a receptacle (like a fridge, cabinet, or microwave) to access its interior or secure it. It should be triggered when an object needs to be placed inside/retrieved from a closed container, or when an open container should be closed (e.g., for energy efficiency or task cleanliness). The skill decides the appropriate 'open' or 'close' action based on the receptacle's current state and the task context.
---
# Skill: Receptacle Operator

## When to Use
Use this skill when you need to:
1. **Access a closed receptacle** to place an object inside or take an object out.
2. **Secure an open receptacle** after accessing it (e.g., to conserve energy, maintain cleanliness, or complete a task step).

## Core Decision Logic
1. **Check the receptacle's state** from the observation.
   - If it reports "is closed" or "is open", note the state.
   - If the interior is visible (e.g., "In it, you see..."), it is open.
2. **Choose action based on goal**:
   - **Goal requires interior access** (e.g., "put in microwave", "take from fridge"):
     - If closed → `open {recep}`
     - If open → proceed with next step (e.g., `put` or `take`)
   - **Goal requires securing receptacle** (e.g., after accessing, or for efficiency):
     - If open → `close {recep}`
     - If closed → no action needed
3. **Execute the action** using the exact format: `Action: open {recep}` or `Action: close {recep}`

## Example from Trajectory
- **Task**: "cool some tomato and put it in microwave"
- **Step 1**: At closed fridge → `Action: open fridge 1`
- **Step 2**: After checking interior → `Action: close fridge 1` (for efficiency)
- **Step 3**: At closed microwave → `Action: open microwave 1`

## Important Notes
- Always verify the receptacle state from the latest observation before acting.
- The skill only handles `open` and `close` actions. Other actions (like `take`, `put`, `cool`) are separate skills.
- If "Nothing happened" is observed after your action, the receptacle may already be in that state—re-check and adjust.

For detailed state diagrams and edge cases, see the reference documentation.

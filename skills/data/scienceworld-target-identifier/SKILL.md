---
name: scienceworld-target-identifier
description: Analyzes room observations to identify objects matching a given target description (e.g., 'living thing'). Triggered after exploring a room when the agent needs to locate a specific type of item. Processes the observation list, filters objects based on target criteria, and returns candidate objects for further action.
---
# Skill: Target Object Identifier

## Purpose
This skill enables you to systematically locate objects in the ScienceWorld environment that match a specific target description (e.g., "living thing", "container", "electrical device"). It transforms the raw observation text from `look around` into a structured list of candidate objects for your current task.

## When to Use
1. **Trigger Condition**: Immediately after executing `look around` in any room.
2. **Input Required**: The full observation text from `look around` AND the target description from your task.
3. **Output**: A prioritized list of matching objects with their locations and properties.

## Execution Workflow

### Step 1: Parse Observation
Extract all observable items from the room description. Pay special attention to:
- Objects listed after "Here you see:"
- Objects in containers (marked with "containing" or "On the X is:")
- Substances (marked as "a substance called")
- Living vs. non-living distinctions

### Step 2: Apply Target Filter
Use the bundled classification script to filter objects based on the target description:
- For "living thing": Include animals, plants, eggs, and biological organisms
- For specific categories: Match against known object taxonomies
- For generic descriptions: Use semantic similarity matching

### Step 3: Prioritize Candidates
Rank candidates by:
1. **Accessibility**: Objects not in closed containers first
2. **Proximity**: Objects in current room before other locations
3. **Task Relevance**: Objects matching secondary task criteria (e.g., "easy to transport")

### Step 4: Generate Action Plan
For each high-priority candidate:
1. Note its exact name as it appears in observations
2. Determine if `pick up`, `focus on`, or other preliminary action is needed
3. Plan path to target location if specified in task

## Key Considerations
- **Exact Object Names**: Use the exact phrasing from observations (e.g., "turtle egg" not "egg turtle")
- **Container States**: All containers are open per environment rules
- **Teleportation**: You can instantly move between rooms when searching
- **Multiple Matches**: If multiple objects match, select based on task context (e.g., choose less mobile items for transport tasks)

## Error Handling
- If no matches found: Teleport to another room and repeat
- If ambiguous matches: Use `examine OBJ` for clarification
- If classification uncertain: Check reference taxonomy in bundled resources

## Example Application
*Task*: "Find a living thing and move it to the blue box in bathroom"
1. `look around` in current room
2. Run this skill with target="living thing"
3. Receive list: ["baby wolf", "turtle egg", "crocodile egg"]
4. Select "turtle egg" (easier to transport)
5. `focus on turtle egg` → `pick up turtle egg` → `teleport to bathroom` → `move turtle egg to blue box`

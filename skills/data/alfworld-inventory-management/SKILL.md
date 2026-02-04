---
name: alfworld-inventory-management
description: This skill tracks which objects have been collected and which remain to be found for multi-object tasks. It should be triggered when working with tasks requiring multiple instances of the same object type. The skill maintains a count of collected vs. needed objects and guides the search for remaining items.
---
# Inventory Management Skill

## When to Use
Activate this skill when:
- Task requires collecting **multiple instances** of the same object type (e.g., "put two cellphone in bed")
- You need to track progress toward a quantity-based goal
- Searching through multiple locations systematically

## Core Workflow

### 1. Initialize Inventory
- Parse the task description to identify:
  - Target object type (e.g., "cellphone")
  - Required quantity (e.g., "two")
- Initialize counters: `collected = 0`, `needed = <quantity>`
- Create empty list for searched locations

### 2. Systematic Search Pattern
Follow this search priority:
1. **Visible surfaces** (desks, dressers, beds) - check first
2. **Closed containers** (drawers, cabinets) - open and inspect
3. **Return to known locations** if inventory incomplete

**Critical Rule:** After finding an object, immediately place it at the target location before searching for the next one.

### 3. Action Decision Logic
Use this decision tree:


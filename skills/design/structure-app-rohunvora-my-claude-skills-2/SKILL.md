---
name: structure-app
description: Structure an app around objects when starting a complex app from scratch, existing navigation feels messy, users can't find things, or the IA is getting worse as features are added. Use Object-Oriented UX to design around nouns, not verbs.
---

# Structure App Around Objects (OOUX)

## When to Use

Activate when the user describes:
- Starting a new complex app
- Apps with multiple related data types
- Products where users manage "things"
- Navigation feeling messy
- Users can't find things
- Information architecture getting worse as features are added
- Features scattered across the interface
- Same data shown inconsistently across screens
- Rebuilding a messy existing app

**Skip when:**
- Building simple single-purpose tools
- Creating marketing/content sites
- Hierarchy matters more than objects

## Instructions

### The Core Idea

**Design around NOUNS (objects), not VERBS (tasks).**

Bad: "What screens do we need?" → disconnected features
Good: "What objects exist?" → coherent structure

### Step 1: Extract Objects

List every NOUN in the product. These are the "things" users think about:

```
OBJECTS IN THIS SYSTEM:
- [Object 1] (e.g., Project)
- [Object 2] (e.g., Task)
- [Object 3] (e.g., User)
- [Object 4] (e.g., Comment)
- [Object 5] (e.g., File)
```

**Tip:** Look at database tables, user stories, or how users talk about the product.

### Step 2: Define Each Object

For each object:

```
OBJECT: [Name]

Core Properties:
- [property]: [type]
- [property]: [type]

States:
- [state 1] (e.g., draft, published, archived)
- [state 2]

Actions:
- [action] (e.g., create, edit, delete)
- [action] (e.g., assign, share, duplicate)
```

### Step 3: Map Relationships

```
RELATIONSHIPS:
[Object A] ──has many──▶ [Object B]
[Object B] ──belongs to──▶ [Object A]
[Object C] ──can attach to──▶ [Object A] or [Object B]

Types:
- Has many / Belongs to (Project has many Tasks)
- Has one / Belongs to (Task has one Assignee)
- Many to many (Users ↔ Projects)
```

### Step 4: Identify Core vs Supporting

```
CORE OBJECTS (get their own screens):
- [Object]: [why it's core]
- [Object]: [why it's core]

SUPPORTING OBJECTS (appear within core screens):
- [Object]: [supports which core object]
- [Object]: [supports which core object]
```

### Step 5: Derive Screens from Objects

For each CORE object:

```
OBJECT: [Name]

SCREENS:
- LIST VIEW: See all [Objects], filter/sort/search
- DETAIL VIEW: Everything about ONE [Object]
- CREATE/EDIT: Form to make or modify

DETAIL VIEW CONTAINS:
- All properties
- Related [Other Objects] (inline or linked)
- Available actions
- State indicators
```

### Step 6: Define Navigation

```
PRIMARY NAV (Core objects):
- [Object 1 list]
- [Object 2 list]
- [Object 3 list]

CONTEXTUAL NAV (when viewing object):
- Related [Object A]
- Related [Object B]
- Actions for this object
```

## Output Format

**IMPORTANT:** Always use this exact format:

```
OOUX STRUCTURE

OBJECTS IDENTIFIED:
| Object | Type | Key Properties |
|--------|------|----------------|
| [Name] | Core | [props] |
| [Name] | Core | [props] |
| [Name] | Supporting | [props] |

RELATIONSHIPS:
[Object A] ──relationship──▶ [Object B]
[Object A] ──relationship──▶ [Object C]

SCREEN STRUCTURE:
- /[objects] → List of [Object]
- /[objects]/:id → [Object] detail
- /[objects]/:id/[related] → Related items

NAVIGATION:
Primary: [Object 1] | [Object 2] | [Object 3]
Contextual: Defined by object relationships
```

The "OOUX Structure" with Objects/Relationships/Screens is the signature of this methodology.

## Anti-Patterns to Avoid

- **Feature-based nav:** "Reports", "Analytics", "Settings" as top-level
- **Verb-based screens:** "Create Task" as destination instead of modal
- **Orphan data:** Showing data where users can't act on it
- **Inconsistent objects:** Same object looking different in different places

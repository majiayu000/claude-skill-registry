---
name: role
description: Load specific role(s) for focused work. Use when user says "role [name]" or wants to work with specific roles. Supports single or multiple roles.
allowed-tools: Read
---

# Role (Dynamic Role Loading)

Load specific role(s) for focused work.

## When to Activate

- User says: "role [name]", "take on [role]"
- User requests specific role by name
- Mid-session role switching

## Flow

### 1. Parse Request

**Single:** "role architect" → load architect role
**Multiple:** "role content and technical" → load both

### 2. Find Role Files

```bash
ls roles/*.md
```

Match requested role name to file. Common patterns:
- Role name in filename (e.g., `architect.md`, `01-creative-lead.md`)
- Check role title in frontmatter if unclear

### 3. Load Role

```bash
cat roles/[matched-file].md
```

### 4. Activate

**Single role:**
```
[Role Name] here.

[1 sentence acknowledgment]

[First question or action]
```

**Multiple roles:**
```
[Primary Role] here, with [Secondary Role].

[How roles work together]

[First question]
```

## Role Switching

User can say "switch to [role]" mid-session:

```
[Current]: Transitioning to [New Role].

[New Role]: [Pick up context from conversation]
```

## Unknown Roles

If role not found:
```
I don't recognize that role. Available roles:

[List from roles/ directory]

Which role do you want?
```

## Comparison

- **role:** Load specific role on demand
- **start:** Ask what to work on, then load relevant role
- **help:** Assess system, suggest priorities

Use `role` when you know exactly which role you need.

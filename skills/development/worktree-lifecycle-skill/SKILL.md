---
name: Worktree Lifecycle
description: Manage git worktree lifecycle for parallel development. Create worktrees with port isolation, manage multiple branches simultaneously, clean up worktrees. CRITICAL: Use /create_worktree command, never manual git worktree commands. Ports auto-calculated to avoid conflicts.
allowed-tools: SlashCommand, Bash, Read, Write, Edit, Glob, Grep
---

# Worktree Lifecycle Skill

**CRITICAL**: Use `/create_worktree` command for worktree management. Never use manual git worktree commands. Ports are auto-calculated.

## When to Use This Skill

Use this skill when:
- Creating parallel development environments
- Working on multiple branches simultaneously
- Managing worktree lifecycle
- Cleaning up worktrees

## Quick Reference

See **Worktree Manager Skill** for complete documentation. This skill focuses on lifecycle patterns.

## Worktree Lifecycle Stages

### 1. Creation

```bash
# Create worktree with auto-calculated ports
/create_worktree feature/new-feature

# Create worktree with specific port offset
/create_worktree feature/new-feature 2
```

**What happens:**
- Worktree created in `trees/<branch-name>/`
- Ports auto-calculated (or use provided offset)
- Environment configured
- Dependencies installed
- Services started

### 2. Active Development

```bash
# List all worktrees and their status
/list_worktrees

# Output shows:
# - Worktree paths
# - Port configurations
# - Service status
# - Access URLs
```

### 3. Cleanup

```bash
# Remove worktree
/remove_worktree feature/new-feature

# What happens:
# - Services stopped
# - Processes killed
# - Worktree directory removed
# - Git worktree removed
```

## Port Allocation Pattern

From `.claude/skills/worktree-manager-skill/REFERENCE.md`:

### Port Calculation

```
SERVER_PORT = 4000 + (offset * 10)
CLIENT_PORT = 5173 + (offset * 10)
```

### Port Map

| Environment | Offset | Server Port | Client Port |
|-------------|--------|-------------|-------------|
| Main Repo   | 0      | 4000        | 5173        |
| Worktree 1  | 1      | 4010        | 5183        |
| Worktree 2  | 2      | 4020        | 5193        |
| Worktree 3  | 3      | 4030        | 5203        |

## Complete Lifecycle Example

### Example: Feature Development with Worktree

```bash
# 1. Create worktree for feature
/create_worktree feature/user-dashboard

# Output:
# ✅ Worktree created: trees/feature-user-dashboard/
# 📡 Server: http://localhost:4010
# 🌐 Client: http://localhost:5183
# 🔧 Services started

# 2. Develop feature in worktree
cd trees/feature-user-dashboard
# ... make changes ...
git add .
git commit -m "feat(dashboard): add user dashboard"

# 3. Test in isolated environment
# Access http://localhost:5183

# 4. Check worktree status
/list_worktrees

# 5. When done, remove worktree
/remove_worktree feature/user-dashboard

# Output:
# ✅ Services stopped
# ✅ Worktree removed
```

## Best Practices

### ✅ DO

- Use worktrees for parallel feature development
- Use `/create_worktree` command (never manual git commands)
- Let ports auto-calculate (unless you need specific offset)
- Remove worktrees when done
- Use worktrees for testing different branches simultaneously

### ❌ DON'T

- Don't manually create worktrees with `git worktree add`
- Don't manually configure ports
- Don't forget to remove worktrees when done
- Don't use worktrees for long-term branches (use regular branches)

## Common Patterns

### Pattern 1: Parallel Feature Development

```bash
# Work on feature A
/create_worktree feature/feature-a

# Work on feature B simultaneously
/create_worktree feature/feature-b

# Both run on different ports
# Feature A: 4010/5183
# Feature B: 4020/5193
```

### Pattern 2: Testing Different Versions

```bash
# Test version 1.0
/create_worktree release/v1.0

# Test version 2.0 simultaneously
/create_worktree release/v2.0

# Compare side-by-side
```

### Pattern 3: Hotfix While Feature Development

```bash
# Feature work in progress
/create_worktree feature/new-feature

# Critical bug found - create hotfix worktree
/create_worktree fix/critical-bug

# Fix bug in hotfix worktree
# Continue feature work in feature worktree
```

## Worktree Status Check

```bash
/list_worktrees

# Output example:
# 🌳 Worktrees:
# 
# 1. feature/user-dashboard
#    📁 Path: trees/feature-user-dashboard/
#    📡 Server: http://localhost:4010 (Running, PID: 12345)
#    🌐 Client: http://localhost:5183 (Running, PID: 12346)
# 
# 2. fix/login-bug
#    📁 Path: trees/fix-login-bug/
#    📡 Server: http://localhost:4020 (Stopped)
#    🌐 Client: http://localhost:5193 (Stopped)
```

## Cleanup Patterns

### Single Worktree Cleanup

```bash
/remove_worktree feature/my-feature
```

### Cleanup All Stopped Worktrees

```bash
# List worktrees first
/list_worktrees

# Remove stopped worktrees manually
/remove_worktree feature/old-feature-1
/remove_worktree feature/old-feature-2
```

## Troubleshooting

### Worktree Services Not Starting

```bash
# Check if ports are in use
npm run dev:ports

# Kill processes on ports if needed
npm run kill:4010
npm run kill:5183

# Recreate worktree
/remove_worktree feature/my-feature
/create_worktree feature/my-feature
```

### Worktree Port Conflicts

```bash
# Use specific port offset to avoid conflicts
/create_worktree feature/my-feature 5

# This uses ports 4050/5223
```

## Checklist for Worktree Lifecycle

When using worktrees:

- [ ] Use `/create_worktree` command (not manual git commands)
- [ ] Ports auto-calculated correctly
- [ ] Services start successfully
- [ ] Can access worktree URLs
- [ ] Development proceeds in isolated environment
- [ ] Worktree removed when done (`/remove_worktree`)

## Related Documentation

- **Worktree Manager Skill**: Complete worktree documentation
- **Git Standards**: See Orchestrator Git Standards Skill


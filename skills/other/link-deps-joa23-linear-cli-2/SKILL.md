---
name: link-deps
description: Discover and link related issues as dependencies. Searches for issues that should be connected and recommends dependency relationships to establish proper work order.
---

# Link Deps Skill - Dependency Discovery

You are an expert at discovering hidden dependencies between issues and establishing proper work order.

## When to Use

Use this skill when:
- You have many unconnected issues in your backlog
- Work order is unclear because dependencies aren't explicit
- Issues reference each other in descriptions but aren't formally linked
- You need to understand prerequisite work before starting a feature

## The Problem

Teams often have hundreds of issues without explicit dependencies. This makes it hard to:
- Know what to work on next
- Understand what blocks what
- Plan sprints effectively
- Parallelize work

**Common scenario:** You have 500 backlog issues but don't realize ENG-123 must be done before ENG-456 can start.

## The Solution

Use search with dependency filters to discover relationships:

```bash
# 1. Find issues with similar keywords that might be related
linear search "authentication" --team ENG --format full

# 2. Check if any already have dependencies
linear search "authentication" --has-dependencies --team ENG

# 3. Look for blocked work to identify bottlenecks
linear search --has-blockers --state "Todo" --team ENG

# 4. Find circular dependencies that need fixing
linear search --has-circular-deps --team ENG
```

## Discovery Process

### 1. Identify Related Work

Search for issues by theme:

```bash
# Find all auth-related work
linear search "auth" --team ENG --format full

# Find all database-related work
linear search "database" --team ENG --format full

# Find all API-related work
linear search "API" --team ENG --format full
```

### 2. Analyze for Dependencies

For each group, look for:
- **Foundation work** - Core infrastructure others depend on
- **Feature work** - Built on top of foundation
- **Follow-up work** - Enhancements after initial feature

### 3. Establish Relationships

Link dependencies using `--blocked-by`:

```bash
# Feature depends on foundation
linear issues update ENG-456 --blocked-by ENG-123

# Follow-up depends on feature
linear issues update ENG-789 --blocked-by ENG-456

# Multiple dependencies
linear issues update ENG-500 --blocked-by ENG-123,ENG-456
```

### 4. Verify the Graph

Check your work:

```bash
# Visualize the dependency tree
linear deps --team ENG

# Check for circular dependencies
linear search --has-circular-deps --team ENG

# Find what's blocking the most work
linear deps --team ENG | grep "blocks:"
```

## Discovery Patterns

### Pattern 1: Text-Based Discovery

Issues often reference each other in descriptions:

```bash
# Search for issue IDs in descriptions
linear search "ENG-123" --team ENG

# This finds issues mentioning ENG-123 but not formally linked
# Link them: linear issues update <found-id> --blocked-by ENG-123
```

### Pattern 2: Keyword Clustering

Group issues by technology/feature:

```bash
# Find OAuth-related issues
linear search "OAuth" --team ENG

# Determine which is foundation (likely: "OAuth provider setup")
# Link others to it:
linear issues update ENG-457 --blocked-by ENG-450  # OAuth provider = ENG-450
```

### Pattern 3: State-Based Discovery

Work in "Blocked" state often needs explicit blockers:

```bash
# Find blocked issues without formal dependencies
linear search --state "Blocked" --team ENG

# For each, determine what blocks it and link:
linear issues update ENG-200 --blocked-by ENG-199
```

### Pattern 4: Priority Inversion Detection

High priority work blocked by low priority:

```bash
# Find high priority items
linear search --priority 1 --team ENG

# Check if any are blocked
linear search --priority 1 --has-blockers --team ENG

# Verify blockers are appropriately prioritized
```

## Best Practices

### 1. Start with Foundation Work

Identify and link core infrastructure first:

```bash
# Find database migration work
linear search "migration" --team ENG

# Find API foundation work
linear search "API foundation" --team ENG

# Link feature work to these foundations
```

### 2. Use Consistent Keywords

Tag issues to make discovery easier:
- Add labels: `foundation`, `feature`, `enhancement`
- Use consistent titles: "Foundation: OAuth", "Feature: Login with OAuth"

### 3. Regular Discovery Sessions

Run discovery weekly:

```bash
# 1. Find new issues added this week
linear search --team ENG --limit 50

# 2. Check for unlinked work
linear search --has-blockers --team ENG

# 3. Update dependencies as you discover them
```

### 4. Document Reasoning

When linking dependencies, add a comment explaining why:

```bash
linear issues update ENG-456 --blocked-by ENG-123
linear issues comment ENG-456 --body "Blocked by ENG-123 because we need OAuth provider before implementing login flow"
```

## Commands Reference

### Discovery Commands

```bash
# Find issues by keyword
linear search "<keyword>" --team <TEAM>

# Find issues with dependencies
linear search --has-dependencies --team <TEAM>

# Find blocked work
linear search --has-blockers --team <TEAM>

# Find circular dependencies
linear search --has-circular-deps --team <TEAM>

# Find issues blocked by specific issue
linear search --blocked-by <ISSUE-ID>

# Find issues blocking specific issue
linear search --blocks <ISSUE-ID>
```

### Linking Commands

```bash
# Add single blocker
linear issues update <ISSUE> --blocked-by <BLOCKER>

# Add multiple blockers
linear issues update <ISSUE> --blocked-by <BLOCKER1>,<BLOCKER2>

# Add dependency (what this depends on)
linear issues update <ISSUE> --depends-on <DEPENDENCY>

# Remove dependencies (update with empty string)
linear issues update <ISSUE> --blocked-by ""
```

### Verification Commands

```bash
# Visualize dependencies
linear deps <ISSUE-ID>
linear deps --team <TEAM>

# Check specific issue's blockers
linear issues blocked-by <ISSUE-ID>

# Check what an issue blocks
linear issues blocking <ISSUE-ID>

# List issue dependencies
linear issues dependencies <ISSUE-ID>
```

## Example Workflow

### Scenario: 100 Auth-Related Issues, No Links

**Goal:** Discover and link all authentication-related dependencies.

```bash
# Step 1: Find all auth issues
linear search "auth" --team ENG --format full > auth_issues.txt

# Step 2: Identify foundation work (look for "OAuth provider", "JWT library", etc.)
# Found: ENG-450 "Setup OAuth2 provider"

# Step 3: Find all OAuth login features
linear search "OAuth login" --team ENG

# Found: ENG-451, ENG-452, ENG-453

# Step 4: Link features to foundation
linear issues update ENG-451 --blocked-by ENG-450
linear issues update ENG-452 --blocked-by ENG-450
linear issues update ENG-453 --blocked-by ENG-450

# Step 5: Find session management work
linear search "session" --team ENG

# Found: ENG-460 "Session management"

# Step 6: Link session work to OAuth (needs login first)
linear issues update ENG-460 --blocked-by ENG-451

# Step 7: Visualize the complete graph
linear deps --team ENG

# Step 8: Check for circular dependencies
linear search --has-circular-deps --team ENG

# Step 9: Find any remaining blocked work without explicit blockers
linear search --state "Blocked" --team ENG
# For each, add proper blocker using --blocked-by
```

## Output Format

After running discovery, present findings as:

```
DEPENDENCY DISCOVERY REPORT: Team ENG
════════════════════════════════════════

DISCOVERED RELATIONSHIPS (12)
────────────────────────────────────────
Foundation Work:
  ENG-450 OAuth provider setup
    → blocks 3 features: ENG-451, ENG-452, ENG-453

  ENG-460 Session management
    → blocks 2 features: ENG-461, ENG-462

Feature Work:
  ENG-451 OAuth login
    → blocks 1 enhancement: ENG-470

RECOMMENDATIONS
────────────────────────────────────────
1. Prioritize ENG-450 (blocks 3 features)
2. Link ENG-475 to ENG-450 (mentioned in description)
3. Review circular dependency: ENG-480 ↔ ENG-481

COMMANDS TO RUN
────────────────────────────────────────
linear issues update ENG-475 --blocked-by ENG-450
linear issues update ENG-480 --blocked-by ""  # Break cycle
```

## Automation Tips

For large backlogs (100+ issues), automate discovery:

1. **Export all issues**: `linear search --team ENG --limit 250 > backlog.txt`
2. **Group by keyword**: Use grep to find related issues
3. **Create dependency map**: Document relationships in a spreadsheet
4. **Batch link**: Run update commands for each discovered relationship
5. **Verify**: `linear deps --team ENG` to check the final graph

## Anti-Patterns to Avoid

❌ **Don't over-link**: Only link true dependencies, not "nice to have" relationships
❌ **Don't create cycles**: Always verify no circular dependencies
❌ **Don't link to closed issues**: Check issue state before linking
❌ **Don't assume**: If unsure whether A blocks B, ask the team

## Success Metrics

After running link-deps, you should have:
- ✅ Clear work order (know what to do first)
- ✅ No circular dependencies
- ✅ Foundation work identified and prioritized
- ✅ Blocked work has explicit blockers
- ✅ Dependency graph visualizes cleanly

Run `linear deps --team <TEAM>` and you should see a clear tree structure with minimal orphaned issues.

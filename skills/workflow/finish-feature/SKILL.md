---
name: finish-feature
description: |
  Complete epic with cleanup and archiving, or verify feature already closed. MUST BE USED when finishing epics/features.
  For epics: Verifies children closed, archives docs, caches to Serena, closes epic.
  For features/tasks/bugs: Verifies already closed (from PR creation), archives docs, caches to Serena.
  Non-epic issues must be closed at PR creation time (atomic merge pattern).
  Use when user says "I'm done with this epic", "finish the feature", "finish this epic", "archive this epic",
  or when user mentions epic completion, cleanup, archiving, feature finalization, or closing work.
tags: [workflow, beads, cleanup, archiving]
allowed-tools:
  - mcp__plugin_beads_beads__*
  - Bash(git:*)
  - Bash(gh:*)
  - Bash(bd:*)
  - Bash(make:*)
  - mcp__serena__write_memory
  - Read
---

# Finish Feature

Complete epic or feature with verification, archiving, and cleanup (<2 minutes).

## Purpose

Ensures **clean completion** of epics/features: Verify work done, archive docs, cache to Serena, update Beads status.

**Philosophy:** Automated cleanup + Knowledge preservation + Clean slate

## When to Use This Skill

**Auto-activated when:**
- User says "I'm done with this epic"
- User says "finish the feature"
- User says "close this work"
- User says "archive this epic"

**Trigger phrases:**
- "I'm done with bd-xyz"
- "finish this feature"
- "close this epic"
- "archive the work"

## Workflow

### 1. Set Beads Context

```bash
mcp__plugin_beads_beads__set_context(
  workspace_root="/Users/fengning/prime-radiant-ai"
)
```

### 2. Get Current Issue

```bash
# From branch name
currentBranch=$(git branch --show-current)
# Extract Feature-Key (e.g., feature-bd-xyz → bd-xyz)

# Or from user argument
issueId="bd-xyz"  # User specifies
```

Fetch full issue:
```typescript
issue = mcp__plugin_beads_beads__show(issue_id=issueId)
```

### 3. Verify Completion Criteria

**Check prerequisites:**

```bash
# 1. All children closed?
children=$(bd show $issueId --json | jq -r '.dependents[] | select(.type == "parent-child" or .type == "discovered-from") | .id')

openChildren=()
for child in $children; do
  status=$(bd show $child --json | jq -r '.status')
  if [ "$status" != "closed" ]; then
    openChildren+=("$child")
  fi
done

if [ ${#openChildren[@]} -gt 0 ]; then
  echo "⚠️  Warning: ${#openChildren[@]} child issue(s) still open:"
  for child in "${openChildren[@]}"; do
    echo "   - $child"
  done
  echo ""
  echo "Options:"
  echo "   [c] Continue anyway (force close)"
  echo "   [a] Abort (finish children first)"
  read choice

  if [ "$choice" = "a" ]; then
    echo "Aborted. Finish child issues first:"
    for child in "${openChildren[@]}"; do
      echo "   bd close $child --reason 'Completed'"
    done
    exit 0
  fi
fi

# 2. All commits merged?
git log --oneline --grep="Feature-Key: $issueId" origin/master..HEAD
if [ $? -eq 0 ]; then
  echo "⚠️  Warning: Commits exist on feature branch but not merged to master"
  echo "   Consider creating PR first: say 'create PR'"
  echo ""
  echo "Continue anyway? [y/n]"
  read choice
  if [ "$choice" != "y" ]; then
    echo "Aborted. Merge work first."
    exit 0
  fi
fi
```

### 4. Offer Doc Archiving

**If docs exist, offer archiving:**

```bash
DOC_DIR="docs/$issueId"
if [ -d "$DOC_DIR" ]; then
  echo "📄 Archive documentation?"
  echo "   [y] Yes - Move to docs/archive/$(date +%Y)-Q$(($(date +%-m)/3+1))/"
  echo "   [n] No - Keep in docs/$issueId/ (for reference)"
  echo "   (Recommended: Yes for completed work, No for ongoing reference)"
  echo ""
  read choice

  if [ "$choice" = "y" ]; then
    # Create archive directory
    ARCHIVE_DIR="docs/archive/$(date +%Y)-Q$(($(date +%-m)/3+1))"
    mkdir -p "$ARCHIVE_DIR"

    # Move docs
    mv "$DOC_DIR" "$ARCHIVE_DIR/"

    # Update .beads-meta
    echo "Archived: $(date +%Y-%m-%d)" >> "$ARCHIVE_DIR/$issueId/.beads-meta"

    # Stage for commit
    git add docs/archive/ docs/$issueId/

    echo "📦 Archived to: $ARCHIVE_DIR/$issueId/"
  else
    echo "📁 Kept at: $DOC_DIR/ (not archived)"
  fi
fi
```

**Why optional:**
- User controls archiving timing
- Some epics serve as ongoing reference (keep in docs/)
- Others are completed and should archive (move to archive/)

### 5. Cache to Serena

**Auto-cache docs to Serena for searchability:**

```bash
DOC_DIR="docs/$issueId"
ARCHIVE_DIR="docs/archive/$(date +%Y)-Q$(($(date +%-m)/3+1))/$issueId"

# Check which location exists
if [ -d "$ARCHIVE_DIR" ]; then
  SOURCE_DIR="$ARCHIVE_DIR"
elif [ -d "$DOC_DIR" ]; then
  SOURCE_DIR="$DOC_DIR"
else
  echo "ℹ️  No docs to cache (Beads only)"
  SOURCE_DIR=""
fi

if [ -n "$SOURCE_DIR" ]; then
  # Combine all markdown files into cache
  CACHE_CONTENT="# $issueId: ${issue.title}

**Status:** closed
**Type:** ${issue.type}
**Archived:** $(date +%Y-%m-%d)
**Source:** $SOURCE_DIR/

**[CACHE]** This is a searchable cache. Source of truth: git ($SOURCE_DIR/)

---

"

  # Append all markdown files
  find "$SOURCE_DIR" -name "*.md" -type f | while read file; do
    echo "## $(basename $file)" >> cache.tmp
    echo "" >> cache.tmp
    cat "$file" >> cache.tmp
    echo "" >> cache.tmp
    echo "---" >> cache.tmp
    echo "" >> cache.tmp
  done

  CACHE_CONTENT+=$(cat cache.tmp)
  rm cache.tmp

  # Write to Serena
  mcp__serena__write_memory(
    memory_file_name="${issueId}_archive",
    content="$CACHE_CONTENT"
  )

  echo "💾 Cached to Serena: ${issueId}_archive"
  echo "   Search with: /search '@serena ${issueId}'"
fi
```

**Why cache:**
- Docs become searchable via Serena tools
- Clearly marked as [CACHE] (not source of truth)
- Enables fast lookup without reading git files
- Useful for cross-epic references

### 6. Close or Verify Beads Issue

**Handle issue closure based on type:**

```bash
ISSUE_TYPE=$(bd show $issueId --json | jq -r '.type')
ISSUE_STATUS=$(bd show $issueId --json | jq -r '.status')

if [ "$ISSUE_TYPE" = "epic" ]; then
  # Epics: Close if all children closed (special case)
  if [ "$ISSUE_STATUS" != "closed" ]; then
    echo "Closing epic: $issueId"
    mcp__plugin_beads_beads__close(
      issue_id=issueId,
      reason="Epic completed - all phases done, archived and cached"
    )
    echo "✅ Closed: $issueId (epic)"
  else
    echo "✅ Already closed: $issueId (epic)"
  fi
else
  # Features/Tasks/Bugs: Verify already closed (should be closed at PR creation)
  if [ "$ISSUE_STATUS" != "closed" ]; then
    echo "❌ Error: Non-epic issue must already be closed"
    echo ""
    echo "Current status: $ISSUE_STATUS"
    echo "Expected: closed (from PR creation)"
    echo "Issue type: $ISSUE_TYPE"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Why this matters:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Non-epic issues should be closed at PR creation time, not during finish."
    echo "This ensures JSONL merges atomically with code (no post-merge mutations)."
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Likely cause:"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "PR was created before our workflow update (when merge-pr closed issues)."
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Recovery: Close retroactively (one-time fix)"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Since work is already merged, close retroactively:"
    echo "  bd close $issueId --reason 'Retroactive closure - work merged in PR'"
    echo "  bd sync  # Export to JSONL"
    echo ""
    echo "Then retry: Say 'finish this feature'"
    echo ""
    echo "Future prevention:"
    echo "  When creating PRs, create-pull-request skill asks:"
    echo "    'Is work complete?' → YES closes issue BEFORE creating PR"
    echo ""
    exit 1
  fi
  echo "✅ Already closed: $issueId ($ISSUE_TYPE)"
fi
```

**Why different behavior:**
- **Epics:** Special case - close only when ALL children closed (epic completion)
- **Features/Tasks/Bugs:** Must be closed at PR creation time (atomic merge)
- **Prevents post-merge mutations:** All non-epic closures on feature branch
- **Epics are long-lived:** Often remain open across multiple PRs

### 7. Archive External Docs Skill (if exists)

**Check for epic-specific external docs skill:**

```bash
DOCS_SKILL=".claude/skills/docs-$issueId"
if [ -d "$DOCS_SKILL" ]; then
  echo "📚 Archive external docs skill?"
  echo "   [y] Yes - Move to .claude/skills/archive/docs-$issueId/"
  echo "   [n] No - Keep active (for ongoing reference)"
  echo "   (Recommended: Yes for completed work, No for ongoing reference)"
  echo ""
  read choice

  if [ "$choice" = "y" ]; then
    # Create archive directories
    mkdir -p .claude/skills/archive
    mkdir -p .serena/memories/archive

    # Move skill
    mv "$DOCS_SKILL" .claude/skills/archive/

    # Move cached docs
    DOCS_CACHE=".serena/memories/external_$issueId"
    if [ -d "$DOCS_CACHE" ]; then
      mv "$DOCS_CACHE" .serena/memories/archive/
      echo "📦 Archived skill and cache:"
      echo "   - .claude/skills/archive/docs-$issueId/"
      echo "   - .serena/memories/archive/external_$issueId/"
      echo "   To restore: mv .claude/skills/archive/docs-$issueId .claude/skills/ && mv .serena/memories/archive/external_$issueId .serena/memories/"
    else
      echo "📦 Archived skill: .claude/skills/archive/docs-$issueId/"
    fi

    # Stage for commit
    git add .claude/skills/archive/ .serena/memories/archive/ .claude/skills/ .serena/memories/

  else
    echo "📁 Kept active: $DOCS_SKILL/ (not archived)"
  fi
fi
```

**Why optional:**
- User controls when to archive external docs
- Some epics have docs useful across multiple features (keep active)
- Completed epics can archive docs to clean up skill list
- Easy restoration from archive if needed later

### 8. Commit Cleanup

**If archiving happened, commit the changes:**

```bash
if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git commit -m "docs: archive $issueId on completion

Moved docs to archive, cached to Serena, closed issue.

Feature-Key: $issueId
Agent: claude-code
Role: cleanup"

  echo "📦 Committed cleanup"
fi
```

### 9. Branch Cleanup (Post-Merge)

**If on feature branch, offer deletion after PR merged:**

```bash
CURRENT_BRANCH=$(git branch --show-current)

# Only cleanup feature branches
if [[ "$CURRENT_BRANCH" == feature-* ]]; then
  # Extract Feature-Key from branch name
  FEATURE_KEY=$(echo "$CURRENT_BRANCH" | sed 's/^feature-//')

  # Check if PR exists and is merged
  PR_STATE=$(gh pr view --json state -q '.state' 2>/dev/null || echo "NOT_FOUND")

  if [ "$PR_STATE" = "MERGED" ]; then
    echo ""
    echo "🧹 Branch cleanup"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "PR merged successfully! Clean up feature branch?"
    echo ""
    echo "Options:"
    echo "  [b] Delete both local and remote (recommended)"
    echo "  [l] Delete local branch only"
    echo "  [r] Delete remote branch only"
    echo "  [n] Keep branches (manual cleanup later)"
    echo ""
    read -p "Choice: " cleanup_choice

    case "$cleanup_choice" in
      b|B)
        # Delete both
        echo ""
        echo "Switching to master..."
        git checkout master
        git pull origin master

        echo "Deleting local branch: $CURRENT_BRANCH"
        git branch -d "$CURRENT_BRANCH"

        echo "Deleting remote branch: origin/$CURRENT_BRANCH"
        git push origin --delete "$CURRENT_BRANCH"

        echo ""
        echo "✅ Deleted local and remote branches"
        ;;

      l|L)
        # Delete local only
        echo ""
        echo "Switching to master..."
        git checkout master
        git pull origin master

        echo "Deleting local branch: $CURRENT_BRANCH"
        git branch -d "$CURRENT_BRANCH"

        echo ""
        echo "✅ Deleted local branch (remote still exists)"
        ;;

      r|R)
        # Delete remote only
        echo "Deleting remote branch: origin/$CURRENT_BRANCH"
        git push origin --delete "$CURRENT_BRANCH"

        echo ""
        echo "✅ Deleted remote branch (local still exists)"
        echo "   To delete local: git checkout master && git branch -d $CURRENT_BRANCH"
        ;;

      n|N)
        echo ""
        echo "ℹ️  Branches kept. Manual cleanup:"
        echo "   git checkout master"
        echo "   git branch -d $CURRENT_BRANCH"
        echo "   git push origin --delete $CURRENT_BRANCH"
        ;;

      *)
        echo ""
        echo "⚠️  Invalid choice. Skipping branch cleanup."
        echo "   Manual cleanup: git checkout master && git branch -d $CURRENT_BRANCH"
        ;;
    esac

  elif [ "$PR_STATE" = "OPEN" ]; then
    echo ""
    echo "ℹ️  PR still open (not merged yet)"
    echo "   Merge first, then run cleanup"
    echo "   Current branch: $CURRENT_BRANCH"

  elif [ "$PR_STATE" = "NOT_FOUND" ]; then
    echo ""
    echo "⚠️  No PR found for branch: $CURRENT_BRANCH"
    echo "   Create PR or manually clean up:"
    echo "     git checkout master"
    echo "     git branch -d $CURRENT_BRANCH"
  fi
else
  # On master or other branch
  echo ""
  echo "ℹ️  Not on feature branch (current: $CURRENT_BRANCH)"
  echo "   No branch cleanup needed"
fi
```

**Why after PR merged:**
- Safe deletion (work is in master)
- Automated workflow (no manual git commands)
- User controls timing (can defer cleanup)
- Convention enforcement (feature-* branches only)

### 10. Confirm and Suggest Next

**Show completion summary:**

```
✅ Finished: $issueId ($issue.type)
📋 Status: closed
📄 Docs: ${archived ? "Archived to $ARCHIVE_DIR/" : "Kept at $DOC_DIR/"}
💾 Cache: ${cached ? "Serena (.serena/memories/${issueId}_archive.md)" : "None"}
🧹 Cleanup: ${committed ? "Committed" : "No changes"}
🌿 Branch: ${deleted ? "Deleted (local + remote)" : "Kept (manual cleanup)"}

Next steps:
  - Find new work: bd ready
  - View stats: bd stats
  - Start new feature: Say "create <feature>"
```

**If parent epic exists:**
```
Parent epic: ${parent_id}
  - Progress: ${parent.dependents.filter(closed).length}/${parent.dependents.length} children closed
  - Status: ${parent.status}
  - Next: ${nextSibling ? nextSibling.id : 'All phases complete!'}
```

## Best Practices

### Do

✅ Always verify children closed before closing parent
✅ Archive completed work (frees up docs/ for active work)
✅ Cache to Serena for searchability
✅ Check commits merged before closing
✅ Commit archiving changes with Feature-Key
✅ Show parent epic progress for context
✅ **Understand closure timing:** Epics close here, features close at PR creation

### Don't

❌ Force close with open children (unless justified)
❌ Archive ongoing reference docs (keep in docs/ for access)
❌ Skip Serena caching (loses searchability)
❌ Forget to commit cleanup changes
❌ Try to close non-epic issues (should already be closed from PR creation)

## Integration with Other Skills

**Workflow progression:**
1. **issue-first** → Create tracking issue
2. **Implementation** → Code the feature
3. **sync-feature-branch** → Commit with Feature-Key
4. **create-pull-request** → Open PR
5. **fix-pr-feedback** → Address CI/review issues (if needed)
6. **merge-pr** → Merge to master
7. **finish-feature** → Close and cleanup (THIS SKILL)

**Related skills:**
- **issue-first**: Creates the issue this skill closes
- **sync-feature-branch**: Commits work with Feature-Key
- **create-pull-request**: Creates PR for review
- **merge-pr**: Merges work to master

## What This Skill Does

✅ Verifies completion criteria (children closed, commits merged)
✅ Offers doc archiving (docs/ → docs/archive/YYYY-QQ/)
✅ Caches docs to Serena for searchability
✅ **For epics:** Closes epic if all children closed
✅ **For features/tasks/bugs:** Verifies already closed (from PR creation)
✅ Commits cleanup changes with Feature-Key
✅ **Offers branch deletion after PR merged (local + remote)**
✅ **Automatically switches to master after cleanup**
✅ Shows parent epic progress (if applicable)
✅ Suggests next work (bd ready)

## What This Skill DOESN'T Do

❌ Force closure (user can abort if children open)
❌ Delete docs (archives for reference)
❌ Auto-merge PRs (merge-pr skill handles that)
❌ Create new issues (issue-first handles that)
❌ Cascade close children (user closes children first)
❌ **Close non-epic issues** (already closed at PR creation time by create-pull-request skill)

## Examples

### Example 1: Finish Feature with Archiving

```
User: "I'm done with bd-xyz"

finish-feature activates:

1. Verify: All children closed ✓
2. Verify: Commits merged ✓
3. Offer archiving: User chooses [y] Yes
4. Archive: docs/bd-xyz/ → docs/archive/2025-Q1/bd-xyz/
5. Cache: Serena memory created (bd-xyz_archive.md)
6. Close: bd close bd-xyz --reason "Completed - archived and cached"
7. Commit: git commit -m "docs: archive bd-xyz on completion"

✅ Finished: bd-xyz (feature)
📄 Docs: Archived to docs/archive/2025-Q1/bd-xyz/
💾 Cache: Serena (.serena/memories/bd-xyz_archive.md)
🧹 Cleanup: Committed

Next: bd ready (find new work)
```

### Example 2: Finish Epic with Open Children (Abort)

```
User: "finish bd-abc"

finish-feature:

1. Verify children:
   ⚠️  Warning: 2 child issues still open:
      - bd-abc.2
      - bd-abc.3

   Options:
      [c] Continue anyway (force close)
      [a] Abort (finish children first)

User chooses: [a] Abort

Aborted. Finish child issues first:
   bd close bd-abc.2 --reason 'Completed'
   bd close bd-abc.3 --reason 'Completed'

Skill exits.
```

### Example 3: Finish with No Archiving

```
User: "finish bd-docs" (external docs tracking epic)

finish-feature:

1. Verify: All children closed ✓
2. Verify: Commits merged ✓
3. Offer archiving: User chooses [n] No (ongoing reference)
4. Skip archiving
5. Cache: Serena memory created (bd-docs_archive.md)
6. Close: bd close bd-docs --reason "Completed - cached"

✅ Finished: bd-docs (epic)
📄 Docs: Kept at docs/bd-docs/ (not archived)
💾 Cache: Serena (.serena/memories/bd-docs_archive.md)
🧹 Cleanup: No changes

Next: bd ready
```

## Troubleshooting

### Children Still Open

**Symptom:** Skill warns about open children

**Solution:**
1. Check which children: `bd show bd-xyz --json | jq '.dependents'`
2. Close each child: `bd close bd-xyz.1 --reason 'Completed'`
3. Re-run finish-feature

### Commits Not Merged

**Symptom:** Skill warns commits exist on branch but not master

**Solution:**
1. Create PR: Say "create PR"
2. Merge PR: Say "merge it" (after CI passes)
3. Re-run finish-feature

### Docs Not Found

**Symptom:** "No docs to cache (Beads only)"

**Why:** Issue tracked in Beads only, no docs/ created
**Solution:** Normal for tasks/bugs, nothing to do

## Related Skills

- **issue-first**: Creates tracking issue (start of lifecycle)
- **sync-feature-branch**: Commits work with Feature-Key (during work)
- **create-pull-request**: Opens PR for review (before merge)
- **merge-pr**: Merges to master (before finish)
- **finish-feature**: Closes and cleans up (THIS SKILL, end of lifecycle)

## Resources

**Beads reference:**
- Official AGENTS.md: https://github.com/steveyegge/beads/blob/main/AGENTS.md
- Close command: `bd close <id> --reason <reason>`
- Dependencies: parent-child, discovered-from, blocks

**Serena reference:**
- Write memory: `mcp__serena__write_memory`
- Search memory: `/search '@serena <term>'`
- Cache convention: [CACHE] marker in content

---

**Last Updated:** 2025-01-14
**Skill Type:** Workflow
**Average Duration:** <2 minutes
**Related Docs:**
- https://github.com/steveyegge/beads/blob/main/AGENTS.md
- .claude/skills/issue-first/SKILL.md
- .claude/skills/sync-feature-branch/SKILL.md
- .claude/skills/create-pull-request/SKILL.md
- .claude/skills/merge-pr/SKILL.md

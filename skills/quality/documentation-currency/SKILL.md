---
name: documentation-currency
description: Detects stale documentation - outdated status markers, old TODOs, version lag
version: 1.0.0
category: validation
auto_invoke: false
---

# Documentation Currency Skill

**Purpose**: Detect documentation that has become stale or outdated over time.

---

## What This Skill Detects

### 1. Stale Status Markers

**Problem**: Status claims that are no longer true

**Patterns**:

- "CRITICAL ISSUE" markers for solved problems
- "WIP" (Work In Progress) for completed work
- "TODO" for already-implemented features
- "EXPERIMENTAL" for mature features
- "UNSTABLE" for stable APIs

**Detection**:

```bash
# Find status markers
grep -r "CRITICAL ISSUE\|WIP\|TODO\|EXPERIMENTAL\|UNSTABLE" *.md

# Check if context suggests resolution
# Example: "CRITICAL ISSUE" but code has fix
```

### 2. Version Lag

**Problem**: Documentation references old versions

**Example**:

```markdown
# docs/guide.md:15

Compatible with v1.2.0 and above
```

```json
// package.json:3
"version": "2.5.0"
```

**Detection**: Documentation references versions > 2 major releases old.

### 3. Stale "Coming Soon" Claims

**Problem**: Features marked "coming soon" that either:

- Are already implemented
- Were cancelled
- Have been "coming soon" for > 6 months

**Example**:

```markdown
# README.md:67

- ✅ Streaming support
- ✅ Tool calling
- 🔄 Image attachments (coming soon) ← Added 8 months ago
```

```bash
# Check git history
git log --all --grep="image" --since="6 months ago"
# No commits found → Probably cancelled

# Or: Implementation exists
grep -r "image.*attachment" src/  # Found code
```

**Detection**: Check git blame age of "coming soon" markers.

### 4. Outdated Links

**Problem**: Documentation links to old URLs or deprecated resources

**Example**:

```markdown
# docs/api.md:45

See: https://api.example.com/v1/docs ← v1 API deprecated
```

**Detection**:

- API version in URLs doesn't match current version
- Links to deprecated GitHub repos
- References to merged/closed issues

### 5. Contradictory Dates

**Problem**: "Last Updated" dates that don't match git history

**Example**:

```markdown
# PROJECT.md:3

Last Updated: 2024-10-01
```

```bash
# Git shows recent changes
git log --oneline PROJECT.md | head -1
# abc123 docs: major architecture update (2024-10-26)
```

**Detection**: Compare "Last Updated" with `git log` dates.

---

## Workflow

### Phase 1: Scan for Stale Markers

#### Step 1.1: Find All Status Markers

```bash
# Search all markdown files for status indicators
find . -name "*.md" -type f | while read file; do
  grep -n "CRITICAL ISSUE\|WIP\|TODO\|EXPERIMENTAL\|UNSTABLE\|FIXME\|HACK\|TEMP" "$file"
done
```

**Create marker map**:

```json
{
  "PROJECT.md:181": {
    "marker": "CRITICAL ISSUE",
    "context": "Tool calling duplication",
    "line": 181,
    "age_days": 90
  },
  "README.md:45": {
    "marker": "TODO",
    "context": "Add authentication docs",
    "line": 45,
    "age_days": 180
  }
}
```

#### Step 1.2: Check Marker Age

```bash
# For each marker, get git blame age
git blame -L 181,181 PROJECT.md
# Output: 2e8237c (90 days ago) ...
```

**Age thresholds**:

- **CRITICAL ISSUE**: Should resolve within 30 days
- **WIP**: Should complete within 60 days
- **TODO**: Should address within 90 days
- **Coming Soon**: Should implement within 180 days

#### Step 1.3: Validate Marker Relevance

For each marker:

**For "CRITICAL ISSUE"**:

```bash
# Search for fix in code
grep -r "{issue_keyword}" src/

# Check recent commits
git log --oneline --since="90 days ago" | grep -i "{issue_keyword}"

# If fix found → Marker is STALE
```

**For "TODO"**:

```bash
# Search for implementation
grep -r "{feature_keyword}" src/

# If implementation found → Marker is STALE
```

**For "WIP"**:

```bash
# Check if file still being modified
git log --oneline --since="30 days ago" -- {file}

# If no recent changes → Probably complete, marker is STALE
```

---

### Phase 2: Detect Version Lag

#### Step 2.1: Extract Current Version

```bash
# From package.json
CURRENT_VERSION=$(jq -r '.version' package.json)

# Or pyproject.toml
CURRENT_VERSION=$(grep '^version' pyproject.toml | cut -d'"' -f2)

# Or Cargo.toml
CURRENT_VERSION=$(grep '^version' Cargo.toml | head -1 | cut -d'"' -f2)
```

Parse as semantic version: `MAJOR.MINOR.PATCH`

#### Step 2.2: Find Version References in Docs

```bash
# Search for version patterns
grep -r "v[0-9]\+\.[0-9]\+\.[0-9]\+" docs/ *.md

# Common patterns:
# - "Compatible with v1.2.0"
# - "Since version 1.5.0"
# - "Deprecated in v2.0.0"
```

**For each reference**:

```json
{
  "docs/guide.md:15": {
    "referenced_version": "1.2.0",
    "context": "Compatible with v1.2.0 and above",
    "current_version": "2.5.0",
    "major_versions_behind": 1,
    "is_stale": true
  }
}
```

**Stale threshold**: > 1 major version behind

#### Step 2.3: Check Changelog Lag

```bash
# Latest version in CHANGELOG.md
CHANGELOG_VERSION=$(grep -E "^## \[" CHANGELOG.md | head -1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')

# Compare to package.json
if [ "$CHANGELOG_VERSION" != "$CURRENT_VERSION" ]; then
  echo "CHANGELOG is behind: $CHANGELOG_VERSION vs $CURRENT_VERSION"
fi
```

---

### Phase 3: Find Stale "Coming Soon" Claims

#### Step 3.1: Extract Future Claims

```bash
# Search for common "future" indicators
grep -rn "coming soon\|planned\|roadmap\|future\|🔄" *.md docs/

# Common patterns:
# - "🔄 Feature X (coming soon)"
# - "Planned for next release"
# - "Roadmap: Feature Y"
```

**For each claim**:

```json
{
  "README.md:67": {
    "claim": "Image attachments (coming soon)",
    "marker": "🔄",
    "line": 67,
    "file": "README.md"
  }
}
```

#### Step 3.2: Check Claim Age

```bash
# Git blame to find when claim was added
git blame -L 67,67 README.md
# Output: abc123 (8 months ago) ...

# Age in days
AGE_DAYS=240
```

**Age threshold**: > 180 days (6 months)

#### Step 3.3: Check Implementation Status

**Option 1: Feature was implemented**

```bash
# Search codebase for feature
grep -r "image.*attachment" src/

# If code found → Claim is STALE (should update to ✅)
```

**Option 2: Feature was cancelled**

```bash
# Check for removal commits
git log --all --grep="remove.*image" --grep="cancel.*attachment"

# If cancellation commit found → Claim is STALE (should remove)
```

**Option 3: Still in progress (not stale)**

```bash
# Check recent activity
git log --since="3 months ago" --grep="image\|attachment"

# If recent commits → Still active, not stale
```

---

### Phase 4: Validate "Last Updated" Dates

#### Step 4.1: Extract Claimed Dates

```bash
# Search for "Last Updated" patterns
grep -rn "Last Updated\|Updated:\|Last modified" *.md

# Common formats:
# - Last Updated: 2024-10-01
# - Updated: October 1, 2024
# - Last modified: 10/01/2024
```

#### Step 4.2: Compare with Git History

```bash
# For each file with "Last Updated"
git log -1 --format="%ai" PROJECT.md
# Output: 2024-10-26 15:30:45 -0700

# Compare dates
CLAIMED_DATE="2024-10-01"
ACTUAL_DATE="2024-10-26"

# If difference > 7 days → Stale date marker
```

---

### Phase 5: Check for Broken References

#### Step 5.1: Find Internal References

```bash
# Search for markdown links
grep -rn '\[.*\](.*\.md)' docs/

# Search for file path references
grep -rn '\./.*\.sh\|\./src/.*\.ts' *.md docs/
```

**Example references**:

```markdown
[Architecture](docs/ARCHITECTURE.md)
See: ./scripts/debug/test.sh
Implementation: src/convert.ts:45
```

#### Step 5.2: Validate References

```bash
# For each reference, check if file exists
REFERENCE="docs/ARCHITECTURE.md"
if [ ! -f "$REFERENCE" ]; then
  echo "BROKEN: $REFERENCE"
fi

# For file:line references
REFERENCE="src/convert.ts:45"
FILE=$(echo $REFERENCE | cut -d: -f1)
LINE=$(echo $REFERENCE | cut -d: -f2)

if [ ! -f "$FILE" ]; then
  echo "BROKEN: File $FILE doesn't exist"
elif [ $(wc -l < "$FILE") -lt $LINE ]; then
  echo "BROKEN: $FILE only has $(wc -l < $FILE) lines, reference to line $LINE"
fi
```

---

### Phase 6: Generate Report

#### Output Format

````
📅 Documentation Currency Report

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STALE STATUS MARKERS

⚠️ STALE: "CRITICAL ISSUE" in PROJECT.md:181 (90 days old)
   Context: Tool calling duplication
   Age: 90 days (threshold: 30 days)
   Status: Issue was SOLVED in commit 2e8237c (3 hours ago)

   Fix: Update status to SOLVED
   ```markdown
   ### Tool Calling (SOLVED)
   Status: SOLVED (2024-10-26)
````

⚠️ STALE: "TODO" in README.md:45 (180 days old)
Context: Add authentication docs
Age: 180 days (threshold: 90 days)
Status: Auth docs exist in docs/guides/auth.md

Fix: Remove TODO or update to:

```markdown
See: [Authentication Guide](docs/guides/auth.md)
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VERSION LAG

⚠️ OUTDATED VERSION REFERENCE
docs/guide.md:15
Referenced: v1.2.0
Current: v2.5.0
Age: 1 major version behind

Context: "Compatible with v1.2.0 and above"

Fix: Update to current version

```markdown
Compatible with v2.0.0 and above
```

❌ CHANGELOG LAG
CHANGELOG.md: v2.4.0
package.json: v2.5.0
Difference: 1 minor version

Fix: Add v2.5.0 entry to CHANGELOG.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

STALE "COMING SOON" CLAIMS

⚠️ IMPLEMENTED: "Image attachments (coming soon)"
Location: README.md:67
Age: 240 days (8 months)
Status: Implementation found in src/attachments.ts

Fix: Mark as complete

```markdown
- ✅ Image attachments
```

⚠️ ABANDONED: "WebSocket support (roadmap)"
Location: docs/roadmap.md:15
Age: 365 days (1 year)
Status: No commits or code found

Fix: Either:

1.  Remove from roadmap (if cancelled)
2.  Update status if still planned

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OUTDATED "LAST UPDATED" DATES

⚠️ INCORRECT DATE: PROJECT.md:3
Claimed: 2024-10-01
Actual: 2024-10-26 (25 days difference)
Last commit: "docs: major architecture update"

Fix: Update date

```markdown
Last Updated: 2024-10-26
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BROKEN REFERENCES

❌ BROKEN LINK: README.md:35
Links to: docs/ARCHITECTURE.md
Status: File not found

Possible fixes:

- File was renamed to docs/architecture/system-design.md
- Update link to correct path

❌ INVALID LINE REFERENCE: docs/guide.md:89
References: src/convert.ts:450
Status: src/convert.ts only has 412 lines

Fix: Update line number or remove reference

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY

Total issues: 9

- Stale markers: 2
- Version lag: 2
- Stale claims: 2
- Outdated dates: 1
- Broken references: 2

Currency Score: 65% (needs improvement)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED ACTIONS

Priority 1 (Fix Today):

1. Update stale "CRITICAL ISSUE" markers
2. Fix broken references
3. Update "Last Updated" dates

Priority 2 (Fix This Week): 4. Mark implemented "coming soon" features as complete 5. Update CHANGELOG to match package.json version

Priority 3 (Next Sprint): 6. Review version references in guides 7. Clean up old TODOs

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AUTO-FIX AVAILABILITY

✅ Can auto-fix:

- "Last Updated" dates (update to git log date)
- CHANGELOG version sync
- Broken reference paths (if file move detected)

⚠️ Needs review:

- Stale status markers (requires verification)
- "Coming soon" → "Complete" (needs testing)
- Version references (may be intentionally old)

❌ Manual fix required:

- Abandoned features (decision needed)
- Ambiguous broken links (multiple candidates)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

````

---

## Edge Cases

### Case 1: Intentionally Old Version Reference

```markdown
# docs/migration-guide.md:15
Migrating from v1.x to v2.x
````

**Detection**: Context suggests intentional reference (migration guide, changelog)

**Output**:

```
ℹ️ INTENTIONAL: Old version reference detected
   Location: docs/migration-guide.md:15
   Referenced: v1.x
   Context: Migration guide (likely intentional)

   No action needed (skipped from stale count)
```

### Case 2: Status Marker in Code Comment

```typescript
// TODO: Refactor this function
function processData() { ... }
```

**Detection**: Marker in code file, not documentation

**Action**: Skip (code TODOs are different from documentation staleness)

### Case 3: Long-Running "Coming Soon" That's Actually Active

```markdown
# roadmap.md:25

🔄 Full IDE integration (coming soon)
```

```bash
# Check recent activity
git log --since="1 month ago" --grep="IDE"
# Found 5 commits in last month
```

**Output**:

```
✅ ACTIVE: "IDE integration" still in progress
   Age: 8 months
   Recent activity: 5 commits in last month
   Status: Not stale (active development)

   No action needed
```

---

## Success Criteria

After running documentation currency check:

- ✅ All status markers validated against age thresholds
- ✅ Version references checked for currency
- ✅ "Coming soon" claims verified (implemented, cancelled, or active)
- ✅ "Last Updated" dates match git history
- ✅ Broken references detected and reported
- ✅ Completes in < 20 seconds for medium projects

---

## Integration with /align-project

This is **Phase 3** of `/align-project`:

**Phase 1**: Structural validation
**Phase 2**: Semantic validation
**Phase 3**: Documentation currency (THIS SKILL)
**Phase 4**: Cross-reference validation

---

## Automation Triggers

**Auto-run when**:

- `/align-project` command
- Before major releases
- Monthly scheduled check (if configured)

**Alert thresholds**:

- CRITICAL markers > 30 days old
- TODOs > 90 days old
- "Coming soon" > 180 days old
- Version lag > 1 major version

---

**This skill ensures documentation doesn't rot over time, keeping project docs trustworthy and current.**

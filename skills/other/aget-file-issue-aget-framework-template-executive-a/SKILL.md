---
name: aget-file-issue
description: File issues with L520 governance compliance
archetype: universal
allowed-tools:
  - Bash
  - Read
  - Grep
---

# /aget-file-issue

File issues to appropriate repositories with L520 governance compliance (routing + sanitization).

## Purpose

Structured issue filing with:
- Automatic destination routing based on agent type
- Content sanitization for public issues
- Template selection (enhancement, bug, feature)

## Input

```
/aget-file-issue <type> [title]
```

| Type | Description | Template |
|------|-------------|----------|
| `enhancement` | Feature enhancement | ENHANCEMENT_REQUEST |
| `bug` | Bug report | BUG_REPORT |
| `feature` | New feature | FEATURE_REQUEST |

## Execution

### Step 1: Detect Agent Type

```bash
# Check for private fleet markers
if grep -q "gmelli\|private-" <<< "$PWD"; then
  AGENT_TYPE="private"
elif grep -q '"fleet".*"private"' .aget/version.json 2>/dev/null; then
  AGENT_TYPE="private"
elif git remote -v 2>/dev/null | grep -q "gmelli/"; then
  AGENT_TYPE="private"
else
  AGENT_TYPE="public"
fi
```

### Step 2: Determine Destination

| Agent Type | Destination |
|------------|-------------|
| Private Fleet | `gmelli/aget-aget` |
| Public/Remote | `aget-framework/aget` |

### Step 3: Prepare Content

For private agents filing to public repo, sanitize:

| Pattern | Replacement |
|---------|-------------|
| `private-*-aget` | `[PRIVATE-AGENT]` |
| `private-*-AGET` | `[PRIVATE-AGENT]` |
| `gmelli/*` | `[INTERNAL-REPO]` |
| `\d+ agents? in fleet` | `[N agents]` |
| `SESSION_\d{4}-\d{2}-\d{2}` | `[SESSION]` |

### Step 4: Validate

Check required fields:
- Title present
- Type valid (enhancement, bug, feature)
- Body not empty (for bugs)

### Step 5: File Issue

```bash
# Private fleet agent
gh issue create \
  --repo gmelli/aget-aget \
  --title "$TITLE" \
  --body "$BODY" \
  --label "type:$TYPE"

# Public/remote agent (sanitized)
gh issue create \
  --repo aget-framework/aget \
  --title "$TITLE" \
  --body "$SANITIZED_BODY" \
  --label "type:$TYPE"
```

### Step 6: Report

Output:
```
Issue filed: <URL>
Destination: <repo>
Type: <type>
Sanitization: <applied/not-needed>
```

## Output Format

```markdown
## Issue Filed

| Field | Value |
|-------|-------|
| URL | https://github.com/aget-framework/aget/issues/123 |
| Destination | aget-framework/aget |
| Type | enhancement |
| Sanitization | applied |

**Content Sanitized**:
- 2 private agent names redacted
- 1 internal repo reference redacted
```

## Constraints

These are INVIOLABLE:

- **C1**: NEVER file to public repo from private agent without sanitization
- **C2**: NEVER include private agent names (`private-*-aget`, `private-*-AGET`) in public issues
- **C3**: NEVER include fleet size disclosures in public issues
- **C4**: NEVER include internal repo references (`gmelli/*`) in public issues
- **C5**: ALWAYS validate destination before filing
- **C6**: ALWAYS report sanitization actions taken

## Examples

### Example 1: Private Agent Filing Enhancement

```
/aget-file-issue enhancement Add skill validation
```

**Result**: Files to `gmelli/aget-aget` (no sanitization needed)

### Example 2: Public Agent Filing Bug

```
/aget-file-issue bug Template fails on Windows
```

**Result**: Files to `aget-framework/aget` (sanitization checked, none needed)

### Example 3: Private Agent with Sensitive Content

If body contains `private-work-supervisor-AGET noticed an issue...`:

**Result**: Sanitized to `[PRIVATE-AGENT] noticed an issue...` before filing to public repo

## Error Handling

| Error | Response |
|-------|----------|
| No gh CLI | "Error: gh CLI not installed. Install via: brew install gh" |
| Not authenticated | "Error: gh not authenticated. Run: gh auth login" |
| Missing title | "Error: Title required. Usage: /aget-file-issue <type> <title>" |
| Invalid type | "Error: Invalid type. Use: enhancement, bug, feature" |
| Sanitization failed | "Error: Could not sanitize. Review content manually." |

## Related

- L520: Issue Governance Gap
- AGET_ISSUE_GOVERNANCE_SPEC: R-ISSUE-001 through R-ISSUE-010
- SKILL-040: aget-file-issue specification
- validate_issue_destination.py
- sanitize_issue_content.py

## Traceability

| Link | Reference |
|------|-----------|
| Spec | SKILL-040_aget-file-issue.yaml |
| L-doc | L520 (Issue Governance Gap) |
| Project | PROJECT_PLAN_archetype_customization_v3.5_v1.0.md Gate 6 |

---

*aget-file-issue v1.0.0*
*Category: Governance*
*Archetype: Universal (14th universal skill)*

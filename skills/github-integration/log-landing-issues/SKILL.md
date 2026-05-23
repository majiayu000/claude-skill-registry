---
name: log-landing-issues
description: |
  Run /check-landing, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-landing instead if you want to fix issues immediately.
---

# /log-landing-issues

Run landing page audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-landing` to audit landing page quality
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-landing` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-landing` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/landing" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P1] No clear value proposition on landing page" \
  --body "$(cat <<'EOF'
## Problem
Landing page lacks a clear, compelling headline. Users don't understand what the product does within 5 seconds.

## Impact
- High bounce rate
- Visitors leave without understanding value
- Low signup conversion
- Marketing spend wasted

## Location
`app/page.tsx` or `app/(marketing)/page.tsx`

## Suggested Fix
Run `/fix-landing` or add:
- Clear headline: "X for Y" or "Verb + Benefit"
- Sub-headline explaining how it works
- Hero section with clear visual

Examples:
- "Track your fitness journey. See results in weeks."
- "The newsletter for busy professionals. 5 min reads that matter."

---
Created by `/log-landing-issues`
EOF
)" \
  --label "priority/p1,domain/landing,type/enhancement"
```

### 4. Issue Format

**Title:** `[P{0-3}] Landing page issue`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/landing`
- `type/enhancement` | `type/bug`

**Body:**
```markdown
## Problem
What's wrong with landing page

## Impact
Effect on conversion/perception

## Location
File path

## Suggested Fix
Copy/design guidance or skill to run

---
Created by `/log-landing-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No landing page | P0 |
| Landing redirects to app | P0 |
| No value prop/headline | P1 |
| No CTA | P1 |
| Weak CTA text | P1 |
| Mobile broken | P1 |
| Slow load time | P1 |
| No social proof | P2 |
| Single CTA | P2 |
| Missing metadata | P2 |
| Polish items | P3 |

## Output

After running:
```
Landing Page Issues Created:
- P0: 0
- P1: 4 (value prop, CTA, mobile, speed)
- P2: 3 (social proof, CTAs, metadata)
- P3: 2 (polish items)

Total: 9 issues created
View: gh issue list --label domain/landing
```

## Related

- `/check-landing` - The primitive (audit only)
- `/fix-landing` - Fix landing page issues
- `/copywriting` - Improve marketing copy
- `/cro` - Conversion optimization
- `/groom` - Full backlog grooming

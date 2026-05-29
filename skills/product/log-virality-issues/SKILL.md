---
name: log-virality-issues
description: |
  Run /check-virality, then create GitHub issues for all findings.
  Issues are created with priority labels and structured format.
  Use /fix-virality instead if you want to fix issues immediately.
---

# /log-virality-issues

Run virality/shareability audit and create GitHub issues for all findings.

## What This Does

1. Invoke `/check-virality` to audit viral growth infrastructure
2. Parse findings by priority (P0-P3)
3. Check existing issues to avoid duplicates
4. Create GitHub issues for each finding

**This is an issue-creator.** It creates work items, not fixes. Use `/fix-virality` to fix issues.

## Process

### 1. Run Primitive

Invoke `/check-virality` skill to get structured findings.

### 2. Check Existing Issues

```bash
gh issue list --state open --label "domain/virality" --limit 50
```

### 3. Create Issues

For each finding:

```bash
gh issue create \
  --title "[P0] No OG tags configured - links broken when shared" \
  --body "$(cat <<'EOF'
## Problem
No Open Graph meta tags configured. When users share links, they appear broken/generic.

## Impact
- Shared links show no preview
- Lower click-through rates on social
- Product looks unprofessional
- Missed viral growth opportunity

## Suggested Fix
Run `/fix-virality` or add to `app/layout.tsx`:
```typescript
export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL!),
  openGraph: {
    type: 'website',
    siteName: 'Your Product',
    images: ['/og-default.png'],
  },
};
```

---
Created by `/log-virality-issues`
EOF
)" \
  --label "priority/p0,domain/virality,type/enhancement"
```

### 4. Issue Format

**Title:** `[P{0-3}] Virality gap description`

**Labels:**
- `priority/p0` | `priority/p1` | `priority/p2` | `priority/p3`
- `domain/virality`
- `type/enhancement`

**Body:**
```markdown
## Problem
What shareability feature is missing

## Impact
Effect on growth and sharing

## Suggested Fix
Code snippet or skill to run

---
Created by `/log-virality-issues`
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No OG tags | P0 |
| No root metadata | P0 |
| No dynamic OG images | P1 |
| No share mechanics | P1 |
| No Twitter cards | P1 |
| No referral system | P2 |
| No UTM tracking | P2 |
| No share prompts | P2 |
| Launch assets missing | P3 |
| No changelog | P3 |

## Output

After running:
```
Virality Issues Created:
- P0: 2 (OG tags, metadata)
- P1: 3 (dynamic OG, share button, Twitter)
- P2: 3 (referrals, UTM, prompts)
- P3: 2 (launch assets, changelog)

Total: 10 issues created
View: gh issue list --label domain/virality
```

## Related

- `/check-virality` - The primitive (audit only)
- `/fix-virality` - Fix virality gaps
- `/virality` - Full viral growth workflow
- `/launch-strategy` - Launch planning
- `/groom` - Full backlog grooming

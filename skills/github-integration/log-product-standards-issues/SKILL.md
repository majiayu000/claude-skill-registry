---
name: log-product-standards-issues
description: |
  Run /check-product-standards, then create GitHub issues for all findings.
  Invoked by /groom as P1 fundamental check.
---

# /log-product-standards-issues

Audit product standards compliance and create GitHub issues for gaps.

## Process

### Step 1: Run Audit

```
Skill("check-product-standards")
```

### Step 2: Create Issues

For each missing or broken requirement:

```bash
gh issue create \
  --title "[P1] [Title]" \
  --label "priority/p1" \
  --label "domain/product-standards" \
  --label "type/chore" \
  --body "$(cat <<'EOF'
## Problem
[What's missing or broken]

## Requirement
[Link to /check-product-standards requirement]

## Suggested Fix
[Code snippet or next steps]

## Impact
Users cannot [know version / identify maker / get support].
This is a baseline shipping requirement.

---
Created by `/log-product-standards-issues`
EOF
)"
```

## Common Issues

### Missing Version Display

```markdown
Title: [P1] Add version display to footer
Labels: priority/p1, domain/product-standards, type/chore

Problem: No visible version number in the application.

Suggested Fix:
1. Add NEXT_PUBLIC_APP_VERSION to next.config.js
2. Display in footer: `v{process.env.NEXT_PUBLIC_APP_VERSION}`
3. Link to /releases or GitHub releases page
```

### Missing Attribution

```markdown
Title: [P1] Add Misty Step attribution to footer
Labels: priority/p1, domain/product-standards, type/chore

Problem: No "A Misty Step project" attribution visible.

Suggested Fix:
Add to footer:
<a href="https://mistystep.io" target="_blank" rel="noopener noreferrer">
  A Misty Step project
</a>
```

### Missing Contact Link

```markdown
Title: [P1] Add contact/support link
Labels: priority/p1, domain/product-standards, type/chore

Problem: No way for users to contact support or report issues.

Suggested Fix:
Add to footer:
<a href="mailto:hello@mistystep.io">Contact</a>
```

### Missing Releases Page

```markdown
Title: [P1] Create releases page or link to GitHub releases
Labels: priority/p1, domain/product-standards, type/chore

Problem: Version number doesn't link to changelog/releases.

Suggested Fix:
Either:
1. Create /releases page with changelog
2. Link version to GitHub releases: https://github.com/MistyStep/[repo]/releases
```

## Output

Issues created in GitHub with:
- Priority: P1 (fundamentals)
- Domain: product-standards
- Type: chore

## Related

- `/check-product-standards` — The audit skill
- `/groom` — Orchestrates all issue creators

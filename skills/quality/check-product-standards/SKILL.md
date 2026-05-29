---
name: check-product-standards
description: |
  Verify Misty Step product standards: version display, attribution, contact link.
  Required for all shipping products. Invoked by /groom as P1 fundamental.
---

# /check-product-standards

Verify every Misty Step product meets baseline shipping standards.

## Why This Exists

If we charge money, users need:
- **Version info** — Know what they're running, check for updates
- **Attribution** — Know who made it, builds trust
- **Contact method** — Get help when something goes wrong

These are non-negotiable for shipped products.

## Required Elements

### 1. Version Display

**Requirement:** Visible version number that links to releases page.

**Location:** Footer, settings, or about section

**Format:**
```
v1.2.3  →  links to /releases or GitHub releases
```

**Implementation patterns:**
```tsx
// From package.json or build-time injection
<a href="/releases" className="text-muted-foreground text-sm">
  v{process.env.NEXT_PUBLIC_APP_VERSION}
</a>
```

**Check for:**
- [ ] Version visible somewhere in UI
- [ ] Version is dynamic (from package.json, not hardcoded)
- [ ] Version links to releases/changelog page

### 2. Misty Step Attribution

**Requirement:** "A Misty Step project" or similar, linking to MistyStep.io

**Location:** Footer

**Format:**
```
A Misty Step project  →  links to https://mistystep.io
```

**Implementation patterns:**
```tsx
<a
  href="https://mistystep.io"
  target="_blank"
  rel="noopener noreferrer"
  className="text-muted-foreground text-sm hover:text-foreground"
>
  A Misty Step project
</a>
```

**Acceptable variations:**
- "A Misty Step project"
- "Built by Misty Step"
- "From Misty Step"
- Misty Step logo with link

**Check for:**
- [ ] Attribution text/logo present
- [ ] Links to https://mistystep.io
- [ ] Opens in new tab (external link)

### 3. Contact/Support Link

**Requirement:** Way to contact for help, feedback, or issues.

**Location:** Footer, help menu, or settings

**Format:**
```
Contact | Feedback | Support  →  mailto:hello@mistystep.io
```

**Implementation patterns:**
```tsx
<a href="mailto:hello@mistystep.io" className="text-muted-foreground text-sm">
  Contact
</a>

// Or with subject line
<a href="mailto:hello@mistystep.io?subject=Feedback%20for%20[AppName]">
  Feedback
</a>
```

**Acceptable variations:**
- "Contact"
- "Support"
- "Feedback"
- "Help"
- "Get in touch"
- Email icon with mailto link

**Check for:**
- [ ] Contact method visible
- [ ] Links to hello@mistystep.io (or specific product email)
- [ ] Accessible without authentication (can report issues even if logged out)

## Audit Process

### Step 1: Find Footer/Chrome Components

```bash
# Common patterns
rg -l "footer" --type tsx --type jsx
rg -l "Footer" --type tsx --type jsx
rg -l "layout" --type tsx --type jsx

# Look for version references
rg "version|VERSION" --type tsx --type jsx --type ts

# Look for mistystep references
rg -i "misty.?step" --type tsx --type jsx
```

### Step 2: Check Each Requirement

For each requirement, verify:
1. **Presence** — Element exists in the UI
2. **Functionality** — Links work correctly
3. **Accessibility** — Visible on all pages, not hidden

### Step 3: Report Findings

```markdown
## Product Standards Audit

| Requirement | Status | Location | Issue |
|-------------|--------|----------|-------|
| Version display | ❌ Missing | - | No version shown |
| Version links to releases | ❌ Missing | - | No releases page |
| Misty Step attribution | ✅ Present | Footer.tsx:42 | - |
| Attribution links correctly | ✅ Present | - | - |
| Contact link | ⚠️ Partial | Footer.tsx:45 | Links to Twitter, not email |

### Issues to Create
1. [P1] Add version display to footer
2. [P1] Create /releases page or link to GitHub releases
3. [P1] Add contact email link (hello@mistystep.io)
```

## Priority

**P1 (Fundamentals)** — These are baseline shipping requirements.

Products without these should not be considered "shipped" regardless of feature completeness.

## Integration with /groom

Groom invokes this skill as part of Step 4 (Issue-Creator Skills):

```
/log-product-standards-issues
```

Creates issues for any missing requirements with:
- Label: `domain/product-standards`
- Priority: `priority/p1`

## Quick Fix Patterns

### Minimal Footer Component

```tsx
// components/Footer.tsx
export function Footer() {
  const version = process.env.NEXT_PUBLIC_APP_VERSION || 'dev'

  return (
    <footer className="border-t py-6 text-center text-sm text-muted-foreground">
      <div className="flex items-center justify-center gap-4">
        <a href="/releases" className="hover:text-foreground">
          v{version}
        </a>
        <span>·</span>
        <a
          href="https://mistystep.io"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:text-foreground"
        >
          A Misty Step project
        </a>
        <span>·</span>
        <a
          href="mailto:hello@mistystep.io"
          className="hover:text-foreground"
        >
          Contact
        </a>
      </div>
    </footer>
  )
}
```

### Inject Version at Build Time

```js
// next.config.js
const { version } = require('./package.json')

module.exports = {
  env: {
    NEXT_PUBLIC_APP_VERSION: version,
  },
}
```

### Simple Releases Page

```tsx
// app/releases/page.tsx
export default function ReleasesPage() {
  return (
    <div className="container py-12">
      <h1>Releases</h1>
      <p>
        View full changelog on{' '}
        <a href="https://github.com/MistyStep/[repo]/releases">
          GitHub Releases
        </a>
      </p>
    </div>
  )
}
```

## Related Skills

- `/check-landing` — Landing page audit (includes footer checks)
- `/brand-builder` — Establishes brand profile
- `/changelog` — Creates releases infrastructure

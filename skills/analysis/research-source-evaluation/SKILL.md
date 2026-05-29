---
name: research-source-evaluation
description: When searching for authoritative sources for skills or validating existing source links.
version: 1.0.0
tokens: ~400
confidence: high
sources:
  - https://developers.google.com/search/docs/fundamentals/creating-helpful-content
  - https://www.w3.org/TR/
last_validated: 2025-01-10
next_review: 2025-01-24
tags: [research, sources, validation, skills]
---

## When to Use
When searching for authoritative sources for skills or validating existing source links.

## Patterns

### Source Tiers (Credibility)
```
Tier 1 (Highest):
  - Official docs (react.dev, supabase.com/docs)
  - RFCs, W3C specs
  - GitHub source code

Tier 2:
  - Official blogs (vercel.com/blog)
  - Release notes, changelogs
  - Core team members' posts

Tier 3:
  - Reputable tech companies (AWS, Google, etc.)
  - Well-known authors (Kent C. Dodds, Dan Abramov)

Tier 4:
  - Stack Overflow (high votes, recent)
  - GitHub issues (official repos)

Tier 5 (Lowest):
  - Personal blogs, tutorials
  - Medium articles (verify author)
```

### Search Strategy
```bash
# Primary search (official)
"[technology] site:docs.*.com OR site:*.dev"

# Version-specific
"[technology] [version] documentation"

# Latest practices
"[technology] best practices 2024 2025"

# Breaking changes
"[technology] migration guide OR breaking changes"
```

### Source Validation Checklist
```
✅ Domain is official project domain
✅ Content dated within 12 months
✅ Author is maintainer/team member
✅ Links to source code or spec
✅ No outdated version warnings
```

## Anti-Patterns
- Using StackOverflow answers >2 years old
- Blog posts without checking official docs
- Ignoring version numbers in examples
- Trusting AI-generated content without verification

## Verification Checklist
- [ ] Source is Tier 1-3
- [ ] Content is recent (<12 months)
- [ ] No deprecation warnings on page
- [ ] Multiple sources agree on pattern

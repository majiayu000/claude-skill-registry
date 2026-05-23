---
name: policyengine-research-lookup
description: Find and reference PolicyEngine blog posts, research articles, and published analyses for evidence and proof points
---

# PolicyEngine Research Lookup

Use this skill to find existing PolicyEngine research, blog posts, and published analyses that can serve as evidence, proof points, or references.

## For Users 👥

### What is PolicyEngine Research?

PolicyEngine publishes research through:
- **Blog posts**: Policy analyses, model updates, methodology explanations
- **Research reports**: In-depth studies for partners and stakeholders
- **Dashboards**: Interactive tools for specific policy questions

### Key Research Highlights

**Government adoption:**
- Our CTO spent 6 months at **10 Downing Street** adapting PolicyEngine for UK government use (see `policyengine-10-downing-street.md`)

**State coverage:**
- US model covers federal + state taxes for all 50 states
- State-specific posts: California, New York, Kansas, Montana, Oregon, Utah, Washington, Minnesota

**UK coverage:**
- Full UK tax-benefit system
- Autumn Budget analyses, manifesto costing

## For Analysts 📊

### Finding Blog Posts

**Location in codebase:**
```
~/policyengine-app-v2/app/src/data/posts/articles/
```

**Search for topics:**
```bash
# Find posts mentioning a topic
find ~/policyengine-app-v2/app/src/data/posts/articles/ -name "*.md" | \
  xargs grep -l -i "topic" 2>/dev/null

# List all posts
ls ~/policyengine-app-v2/app/src/data/posts/articles/
```

**Post metadata is in:**
```
~/policyengine-app-v2/app/src/data/posts/posts.json
```

### Key Posts to Reference

| Topic | File | Use Case |
|-------|------|----------|
| Government adoption | `policyengine-10-downing-street.md` | Credibility, state capacity |
| State tax models | `state-tax-model-beta.md` | US state coverage |
| Machine learning | Various | Accuracy, methodology |
| Budget analyses | `autumn-budget-*.md` | UK policy coverage |
| US tax proposals | `*-tax-*.md`, `*-ctc-*.md` | Federal policy coverage |

### Post Structure

Each post is markdown with YAML frontmatter:
```yaml
---
title: "Post Title"
date: "2025-01-15"
authors:
  - name: Author Name
tags:
  - us
  - federal
---
```

## For Contributors 💻

### When to Use This Skill

- Preparing talks, pitches, or presentations about PolicyEngine
- Finding proof points for PolicyEngine's credibility
- Referencing specific analyses in conversations
- Looking up methodology explanations
- Finding state or country-specific coverage

### Common Lookups

**"What's our strongest credibility proof point?"**
→ 10 Downing Street blog post: CTO spent 6 months adapting PolicyEngine for UK government

**"Do we cover [state] taxes?"**
→ Search for state name in posts directory; also check policyengine-us-skill

**"What did we write about [policy]?"**
→ Search posts directory for policy name or related terms

**"Where can I find our methodology for [X]?"**
→ Search for technical posts; check also policyengine-core-skill

### Adding New Research References

When PolicyEngine publishes significant new research:
1. Note the filename in this skill if it's a key proof point
2. Update the "Key Posts to Reference" table above
3. Consider if it warrants mention in related skills (e.g., country skills)

## Resources

- Blog posts: `~/policyengine-app-v2/app/src/data/posts/articles/`
- Post index: `~/policyengine-app-v2/app/src/data/posts/posts.json`
- Live blog: https://policyengine.org/us/blog and https://policyengine.org/uk/blog

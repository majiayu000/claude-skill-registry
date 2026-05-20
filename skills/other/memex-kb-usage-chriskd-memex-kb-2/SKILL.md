---
name: memex-kb-usage
description: This skill should be used when the user asks to "search the KB", "find documentation", "add to knowledge base", "document this pattern", "check organizational docs", or when an agent discovers reusable knowledge worth preserving.
---

# Using the Memex Knowledge Base

Memex is a knowledge base for documenting patterns, infrastructure, troubleshooting guides, and operational knowledge. This skill teaches how to search, contribute, and maintain the KB effectively.

## Project vs User KB

Memex supports two knowledge base locations:

| Scope | Location | Use For |
|-------|----------|---------|
| `project` | `./kb/` | Team docs, shared patterns. Commit to git. |
| `user` | `~/.memex/kb/` | Personal notes, available across all projects. |

By default, searches include both KBs. Use `--scope` to target one:

```bash
mx search "query" --scope=project   # Project KB only
mx add --title="Note" --scope=user  # Add to personal KB
mx list --scope=project             # List project entries only
```

## When to Search the KB

Search the knowledge base BEFORE asking questions about:
- Infrastructure (DNS, cloud, networking, servers)
- Development conventions and patterns
- CI/CD pipelines and deployment procedures
- Known issues and their solutions
- Architectural decisions and trade-offs

```bash
mx search "kubernetes deployment"
mx search "cloudflare" --mode=semantic    # Semantic search only
mx search "dns" --tags=infrastructure     # Filter by tag
```

If no relevant entries are found, that's valuable information - consider contributing what you learn.

## When to Contribute

Add new entries when you discover:
- Solutions to problems that took significant debugging
- Patterns that should be reused across projects
- Infrastructure configurations worth documenting
- Operational procedures that aren't obvious
- Architectural decisions with their rationale

**Do NOT create entries for:**
- Project-specific details (use project docs instead)
- Temporary workarounds (unless they're long-term)
- Information already in upstream documentation

## Entry Format

Every KB entry requires YAML frontmatter:

```markdown
---
title: Clear, Descriptive Title
tags: [infrastructure, kubernetes, networking]
created: 2024-01-15
---

# Title

Content goes here...
```

See [[references/entry-format]] for the complete specification.

## Modifying Entries

Three commands for different modification needs:

### mx patch - Surgical edits (preferred)
Find and replace specific text while preserving everything else:

```bash
mx patch devops/deploy.md --find "old text" --replace "new text"
mx patch devops/deploy.md --find "TODO" --replace "DONE" --replace-all
mx patch devops/deploy.md --find "..." --replace "..." --dry-run  # Preview
```

Use `--dry-run` to preview changes before applying.

### mx append - Add content to existing entry
Append content to the end of an entry (or create if not found):

```bash
mx append "Daily Log" --content="Session summary here"
mx append "API Docs" --file=new-section.md
```

### mx replace - Full replacement
Overwrite entire content or tags (use sparingly):

```bash
mx replace path/entry.md --tags="new,tags"
mx replace path/entry.md --content="Completely new content"
mx replace path/entry.md --file=rewritten.md
```

**When to use each:**
| Command | Use When |
|---------|----------|
| `mx patch` | Fixing typos, updating specific sections, surgical edits |
| `mx append` | Adding new sections, appending logs, incremental updates |
| `mx replace` | Rewriting entries, changing tags, full overhaul |

## Linking Best Practices

Bidirectional links help readers discover related knowledge:

```markdown
See also [[devops/kubernetes-basics]] for cluster setup.
Related: [[troubleshooting/dns-issues]]
```

**Guidelines for linking:**
- Link when entries genuinely relate (encouraged, not required)
- Think about what a reader might want to explore next
- Don't force links just to have them
- Update existing entries to link to new content when relevant

## Tag Taxonomy

Use existing tags when possible. Check what tags exist before inventing new ones:

```bash
mx tags  # List all tags with usage counts
```

**Common tags by category:**
- infrastructure: `cloud`, `dns`, `networking`, `servers`, `storage`
- devops: `ci`, `cd`, `monitoring`, `deployment`, `docker`, `kubernetes`
- development: `python`, `rust`, `go`, `testing`, `tooling`
- troubleshooting: `debugging`, `performance`, `errors`

See [[references/categories]] for the full category taxonomy.

## Quality Guidelines

**Titles:** Be specific. "Kubernetes Pod Networking" not "K8s Stuff".

**Content:**
- Keep entries focused on one topic
- Include actionable information (commands, configs, steps)
- Add examples when they clarify usage
- Explain the "why" not just the "what"

**Maintenance:**
- Update existing entries rather than creating duplicates
- Mark outdated information clearly
- Remove entries that are no longer relevant

## Quick Reference

| Action | Command | Example |
|--------|---------|---------|
| Search | `mx search` | `mx search "cloudflare dns"` |
| Add entry | `mx add` | `mx add --title="DNS Setup" --tags=infra --content="..."` |
| Read entry | `mx get` | `mx get infrastructure/dns.md` |
| Patch entry | `mx patch` | `mx patch path.md --find="X" --replace="Y"` |
| Append | `mx append` | `mx append "Title" --content="..."` |
| Replace | `mx replace` | `mx replace path.md --tags="new,tags"` |
| Browse | `mx tree` | `mx tree` |
| List | `mx list` | `mx list --tags=devops` |
| Tags | `mx tags` | `mx tags` |
| Health | `mx health` | `mx health` |

**Useful flags:**
- `--scope=project|user` - Target specific KB (works with search, add, list)
- `--mode=semantic|keyword|hybrid` - Search mode (default: hybrid)
- `--json` - Machine-readable output (most commands)
- `--dry-run` - Preview changes without applying (patch)

## Anti-patterns

- Creating an entry without searching first (may duplicate)
- Using `mx replace` when `mx patch` would preserve context
- Linking everything to everything (dilutes link value)
- Using project-specific tags in org-wide KB
- Leaving entries without tags or with wrong category

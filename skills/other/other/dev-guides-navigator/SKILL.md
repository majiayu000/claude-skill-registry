---
name: dev-guides-navigator
description: Use when ANY development task might benefit from a guide. Use when user says "how do I", "best practice", "pattern for", "guide for", "Drupal form", "entity type", "plugin type", "routing", "caching", "config management", "SDC component", "design system", "Bootstrap mapping", "Radix theme", "JSX to Twig", "Tailwind tokens", "SOLID", "DRY", "TDD", "security", "CSS", "Next.js". Use PROACTIVELY before any design, architecture, or implementation work. MUST be invoked before writing code that touches Drupal APIs, theming, design systems, or security. NEVER skip guide check — patterns prevent bugs.
version: 0.2.0
allowed-tools: Read, Bash, Glob, Grep, Write
user-invocable: true
---

# Dev-Guides Navigator

Route to the correct online guide and enforce guide application.

## When to Use

- Any Drupal, Next.js, design system, or dev-practice task where a guide might help
- When another skill or agent needs domain knowledge beyond its bundled references
- When the user mentions a specific guide topic
- NOT for: plugin methodology references (those are in drupal-dev-framework/references/)

## Core Workflow

### 1. Get llms.txt (with caching)

Check for cache at `~/.claude/projects/{project-hash}/memory/dev-guides-cache.json`.

**NEVER use WebFetch in this workflow.** All fetches use `curl -s` via Bash:
- WebFetch summarizes content through AI, destroying structured formats needed for matching
- MkDocs GitHub Pages URLs return 400KB+ HTML navigation shells, not guide content
- Guides are atomic and small enough for `curl` — no summarization needed

**No cache (first time):**
1. Bash: `curl -s https://camoa.github.io/dev-guides/llms.hash` — save the hash
2. Bash: `curl -s https://camoa.github.io/dev-guides/llms.txt` — save the content
3. Write both to cache file

**Cache exists:**
1. Bash: `curl -s https://camoa.github.io/dev-guides/llms.hash` (tiny, fast)
2. Compare with cached hash
   - **Same** → use cached `llms.txt`, skip re-fetch
   - **Different** → Bash: `curl -s https://camoa.github.io/dev-guides/llms.txt`, update cache

### 2. Match Task to Topic

Scan `llms.txt` for the topic that matches the current task. Each line has a topic title, URL, guide count, and description.

The URL in `llms.txt` is a GitHub Pages URL like `https://camoa.github.io/dev-guides/drupal/forms/`. Extract the **topic path** (e.g., `drupal/forms`) from this URL for use in raw GitHub fetches below.

### 3. Fetch Topic Index

**IMPORTANT:** Do NOT use WebFetch on GitHub Pages URLs — MkDocs renders them into 400KB+ HTML pages with navigation shells, hiding the actual content. Use `curl` with raw GitHub URLs instead.

```bash
curl -s https://raw.githubusercontent.com/camoa/dev-guides/main/docs/{topic-path}/index.md
```

Example: `curl -s https://raw.githubusercontent.com/camoa/dev-guides/main/docs/drupal/forms/index.md`

This returns the raw markdown containing:

- **"I need to..." routing table** — maps user intent to specific guide
- **`guide-meta:` frontmatter** — KG metadata for disambiguation and relationships

### 4. Use KG Metadata (from index.md)

The `guide-meta:` in the topic's frontmatter provides:

- **`concepts`** — confirms this is the right topic
- **`not`** — if the task matches a `not` term, this is the WRONG topic, go back to step 2
- **`requires`** — load prerequisite topics first
- **`complements`** — note related topics for the user

| Example Task | Correct Topic | Wrong Topic | Why |
|--------------|---------------|-------------|-----|
| story.yml props | drupal/ui-patterns | drupal/storybook | "story.yml" in ui-patterns concepts, "storybook" in not |
| stories.yml preview | drupal/storybook | drupal/ui-patterns | reverse |
| inline blocks | drupal/layout-builder | drupal/blocks | "inline blocks" in blocks' not |

### 5. Fetch Specific Guide

From the "I need to..." routing table, select the guide that matches the task. The routing table lists guide filenames. Fetch the raw markdown:

```bash
curl -s https://raw.githubusercontent.com/camoa/dev-guides/main/docs/{topic-path}/{guide-filename}.md
```

Example: `curl -s https://raw.githubusercontent.com/camoa/dev-guides/main/docs/drupal/forms/form-validation.md`

**Do NOT use WebFetch on GitHub Pages URLs** — you'll get rendered HTML, not the guide content.

### 6. Apply the Guide (Critical)

**Do NOT just read and summarize.** Extract and apply:

1. Identify the relevant section(s) for the current task
2. Extract decision criteria, patterns, and code examples
3. Apply them directly to the implementation
4. Reference the guide in architecture docs if in design phase

## Quick Reference

| Step | Action |
|------|--------|
| Cache check | `curl -s` llms.hash, compare with cached hash |
| Find topic | Match task keywords in cached `llms.txt` |
| Get routing table | `curl -s` raw GitHub URL for topic `index.md` |
| Disambiguate | Check `guide-meta:` concepts/not fields |
| Get guide | `curl -s` raw GitHub URL for specific guide `.md` |
| Apply | Extract patterns and implement, don't summarize |

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Using WebFetch instead of curl | **Always use `curl -s`** — WebFetch returns AI summaries or 400KB HTML shells |
| Reading guide and only summarizing | Extract patterns and apply to current task |
| Grabbing first keyword match | Check guide-meta `not` fields for disambiguation |
| Fetching llms.txt every time | Check llms.hash first, use cache |
| Ignoring `requires` | Load prerequisites first |

## Examples

| User says | Action |
|-----------|--------|
| "I need to create a Drupal form" | Match "form" → `drupal/forms/` → fetch index.md → pick guide for form creation |
| "Add a story.yml for my component" | Match "story.yml" → check guide-meta → `drupal/ui-patterns/` (NOT storybook) |
| "Set up responsive images" | Match "responsive image" → `drupal/image-styles/` (NOT drupal/media) |
| "How do I use Config Split?" | Match "Config Split" → `drupal/config-management/` |
| "I need SOLID architecture for my module" | Drupal context → `drupal/solid/` (NOT generic dev-solid-principles) |

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `curl` fails (network error) | Fall back to `references/guide-index.md` for keyword-to-URL lookup |
| No topic matches the task | Broaden keywords, check category sections in llms.txt, or task may not need a guide |
| Cache file path unknown | Use Bash: `echo ~/.claude/projects/*/memory/` to find the project memory directory |
| Guide content too large for context | Request only the specific section from the routing table, not the entire guide |

## See Also

- `references/cache-format.md` — cache file format
- `references/manifest-schema.md` — build output (llms.txt + llms.hash)
- `references/guide-index.md` — fallback keyword table (offline/network failure)

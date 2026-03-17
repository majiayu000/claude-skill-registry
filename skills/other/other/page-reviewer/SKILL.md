---
name: page-reviewer
description: Review pages visually and test accessibility using agent-browser CLI
---

# Page Reviewer

Visual and accessibility testing for JusticeHub pages using agent-browser.

## When to Use
- Test page rendering and layout
- Check accessibility tree structure
- Verify interactive elements work
- Capture screenshots for review
- Debug console errors

## Invocation

```
/page-reviewer [scope]
```

| Scope | What It Reviews |
|-------|-----------------|
| `all` | All key pages (default) |
| `/path` | Specific page path |
| `full-url` | Any URL directly |

## Quick Start

```bash
# Ensure dev server running
npm run dev &

# Review single page
agent-browser open http://localhost:3000/community-map
agent-browser snapshot -i -c
agent-browser screenshot --full /tmp/review.png
agent-browser errors
agent-browser close
```

## Key Commands

| Command | Purpose |
|---------|---------|
| `agent-browser open <url>` | Navigate to page |
| `agent-browser snapshot -i -c` | Interactive elements with refs |
| `agent-browser screenshot --full <path>` | Full-page capture |
| `agent-browser click @ref` | Click element by ref |
| `agent-browser fill @ref "text"` | Fill form input |
| `agent-browser get text @ref` | Extract text content |
| `agent-browser errors` | Console errors |
| `agent-browser close` | Close browser |

## Review Checklist

For each page:

1. **Load**: Page renders without errors
2. **Navigation**: Links and buttons accessible
3. **Forms**: Inputs have labels, submit works
4. **Data**: Content loads from database
5. **Responsive**: Layout works at different widths
6. **Errors**: No console errors

## Key Pages

| Priority | Page | Path |
|----------|------|------|
| High | Homepage | `/` |
| High | Community Map | `/community-map` |
| High | Community Programs | `/community-programs` |
| Medium | People Directory | `/people` |
| Medium | Youth Justice Report | `/youth-justice-report` |
| Medium | Stories | `/stories` |
| Low | Admin Dashboard | `/admin` |

## Output Format

```markdown
## [Page Name] - /path

**Status**: OK | Issues Found

**Elements**: [count] interactive elements
**Errors**: None | [list]

**Accessibility**:
- [x] Navigation present
- [x] Forms labeled
- [ ] Issue: [description]

**Screenshot**: /tmp/review-[page].png
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `agent-browser` not found | `npm install -g agent-browser && agent-browser install` |
| Browser crash | `agent-browser install` to reinstall Chromium |
| Page 404 | Check route exists, dev server running |
| Timeout | Page slow loading, wait longer |

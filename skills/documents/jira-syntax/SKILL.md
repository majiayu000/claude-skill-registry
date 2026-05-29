---
name: "jira-syntax"
description: "Jira wiki markup syntax validation, templates, and formatting guidance. Use when: (1) Writing Jira issue descriptions or comments, (2) Converting Markdown to Jira wiki markup, (3) Requesting bug report or feature request templates, (4) Validating Jira syntax before submission, (5) Keywords like 'jira format', 'wiki markup', 'jira syntax', 'format for jira', (6) Ensuring content uses h2./h3. headings instead of Markdown ##, (7) Checking code blocks use {code:lang} not triple backticks, (8) Any task involving Jira text formatting"
---

# Jira Syntax Validation Skill

Provides Jira wiki markup syntax validation, templates, and formatting guidance. For API operations, use the **jira-communication** skill.

## Quick Syntax Reference

| Jira Syntax | Purpose | NOT this (Markdown) |
|-------------|---------|---------------------|
| `h2. Title` | Heading | `## Title` |
| `*bold*` | Bold | `**bold**` |
| `_italic_` | Italic | `*italic*` |
| `{{code}}` | Inline code | `` `code` `` |
| `{code:java}...{code}` | Code block | ``` ```java ``` |
| `[text\|url]` | Link | `[text](url)` |
| `[PROJ-123]` | Issue link | - |
| `[~username]` | User mention | `@username` |
| `* item` | Bullet list | `- item` |
| `# item` | Numbered list | `1. item` |
| `\|\|Header\|\|` | Table header | `\|Header\|` |

See `references/jira-syntax-quick-reference.md` for complete syntax documentation.

## Available Templates

### Bug Report
**Path**: `templates/bug-report-template.md`

Sections: Environment, Steps to Reproduce, Expected/Actual Behavior, Error Messages, Technical Notes

### Feature Request
**Path**: `templates/feature-request-template.md`

Sections: Overview, User Stories, Acceptance Criteria, Technical Approach, Success Metrics

## Syntax Validation

Run before submitting to Jira:
```bash
scripts/validate-jira-syntax.sh path/to/content.txt
```

### Validation Checklist
- [ ] Headings: `h2. Title` (space after period)
- [ ] Bold: `*text*` (single asterisk)
- [ ] Code blocks: `{code:language}...{code}`
- [ ] Lists: `*` for bullets, `#` for numbers
- [ ] Links: `[label|url]` or `[PROJ-123]`
- [ ] Tables: `||Header||` and `|Cell|`
- [ ] Colors: `{color:red}text{color}`
- [ ] Panels: `{panel:title=X}...{panel}`

### Common Mistakes

| ❌ Wrong | ✅ Correct |
|---------|-----------|
| `## Heading` | `h2. Heading` |
| `**bold**` | `*bold*` |
| `` `code` `` | `{{code}}` |
| `[text](url)` | `[text\|url]` |
| `- bullet` | `* bullet` |
| `h2.Title` | `h2. Title` |

## Integration with jira-communication Skill

**Workflow:**
1. Get template from jira-syntax
2. Fill content using Jira wiki markup
3. Validate with `scripts/validate-jira-syntax.sh`
4. Submit via jira-communication scripts (e.g., `uv run scripts/workflow/jira-create.py`)

## References

- `references/jira-syntax-quick-reference.md` - Complete syntax documentation
- `templates/bug-report-template.md` - Bug report template
- `templates/feature-request-template.md` - Feature request template
- `scripts/validate-jira-syntax.sh` - Automated syntax checker
- [Official Jira Wiki Markup](https://jira.atlassian.com/secure/WikiRendererHelpAction.jspa?section=all)

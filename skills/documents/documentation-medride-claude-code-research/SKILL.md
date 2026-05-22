---
name: documentation
description: Write clear documentation following team standards
---

# Documentation Skill

Write clear, useful documentation that helps current and future developers.

## Documentation Types

| Type | Location | Purpose |
|------|----------|---------|
| API Docs | `docs/api/` | Endpoint reference |
| Architecture | `docs/architecture/` | System design |
| Guides | `docs/guides/` | How-to tutorials |
| ADRs | `docs/decisions/` | Decision records |
| README | Root/module | Quick start |

## Writing Principles

### 1. Lead with the "Why"
Before diving into details, explain the purpose.

**Bad:**
```markdown
## Installation
Run `npm install mylib`
```

**Good:**
```markdown
## Installation
MyLib provides utilities for date manipulation used throughout the application.

Run `npm install mylib`
```

### 2. Show, Don't Just Tell
Include examples for everything.

**Bad:**
```markdown
The `formatDate` function formats dates.
```

**Good:**
```markdown
The `formatDate` function formats dates:

```javascript
formatDate(new Date())        // "January 20, 2026"
formatDate(new Date(), 'short') // "1/20/26"
```
```

### 3. Keep It Scannable
Use headers, lists, and tables liberally.

**Bad:**
```markdown
The API accepts several parameters. The first parameter is the user ID which
must be a string. The second parameter is optional and specifies the format...
```

**Good:**
```markdown
### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| userId | string | Yes | The user's unique identifier |
| format | string | No | Output format (default: 'json') |
```

### 4. Maintain It
Outdated documentation is worse than no documentation.

- Update docs when code changes
- Add "Last updated" timestamps
- Review docs periodically

## Document Templates

### README Template

```markdown
# Project Name

Brief description of what this project does.

## Quick Start

```bash
npm install
npm run dev
```

## Usage

[Basic usage examples]

## Configuration

[Environment variables and config options]

## Development

[How to set up local development]

## Contributing

[How to contribute]
```

### API Endpoint Template

```markdown
# [Endpoint Name]

[Brief description]

## Request

`[METHOD] /path/{param}`

### Parameters

| Name | Type | In | Required | Description |
|------|------|-----|----------|-------------|
| param | string | path | Yes | [Description] |

### Body

```json
{
  "field": "value"
}
```

## Response

### Success (200)

```json
{
  "id": "123",
  "status": "success"
}
```

### Errors

| Code | Description |
|------|-------------|
| 400 | Invalid request |
| 404 | Resource not found |

## Example

```bash
curl -X POST https://api.example.com/endpoint \
  -H "Authorization: Bearer token" \
  -d '{"field": "value"}'
```
```

### ADR Template

```markdown
# [Number]. [Title]

## Status
[Proposed | Accepted | Deprecated]

## Context
[Why we need to make this decision]

## Decision
[What we decided]

## Consequences
[What this means going forward]
```

## Code Comments

### When to Comment

| Do Comment | Don't Comment |
|------------|---------------|
| Complex algorithms | Obvious code |
| Business logic rationale | What the code does |
| Non-obvious gotchas | Every function |
| API contracts | Redundant info |

### Comment Style

```javascript
// BAD: Increment counter
counter++;

// GOOD: Rate limiting: allow 100 requests per minute per user
if (requestCount > 100) {
  throw new RateLimitError();
}

/**
 * Calculate the total price including discounts and tax.
 *
 * Note: Discounts are applied before tax, per accounting requirements.
 * See ADR-015 for the decision rationale.
 */
function calculateTotal(items, discountCode) {
  // ...
}
```

## Best Practices

1. **Write for your audience** - New developer? Expert? Adjust detail level.
2. **Use consistent terminology** - Define terms and stick to them.
3. **Include troubleshooting** - What can go wrong and how to fix it.
4. **Link to related docs** - Don't duplicate, reference.
5. **Test your docs** - Follow your own instructions to verify they work.

## Documentation Review Checklist

- [ ] Purpose is clear from the start
- [ ] Examples are included and working
- [ ] Structure is scannable
- [ ] No broken links
- [ ] Code snippets are correct
- [ ] Last updated date is current

---
name: documentation
description: Write clear technical documentation. Use when creating READMEs, API docs, or user guides. Covers documentation types and best practices.
allowed-tools: Read, Write, Glob, Grep
---

# Technical Documentation

## Documentation Types

### README
First thing users see. Include:
- What the project does
- How to install/setup
- Basic usage examples
- Where to find more info

### API Documentation
- Endpoints and methods
- Request/response formats
- Authentication
- Error codes
- Examples

### Architecture Documentation
- System overview
- Component diagrams
- Data flow
- Key decisions (ADRs)

### User Guides
- Step-by-step instructions
- Screenshots/examples
- Common workflows
- Troubleshooting

## Writing Principles

### 1. Know Your Audience
- Developer? User? Admin?
- What do they already know?
- What do they need to accomplish?

### 2. Be Concise
- Short sentences
- Active voice
- Remove filler words

### 3. Show, Don't Tell
```markdown
# Bad
The function handles errors properly.

# Good
The function returns an Error object:
  ```typescript
  const result = await fetchUser(id);
  if (result.error) {
    console.error(result.error.message);
  }
  ```
```

### 4. Structure for Scanning
- Use headings
- Use bullet points
- Use code blocks
- Use tables

## README Template

```markdown
# Project Name

Brief description of what this does.

## Installation

\`\`\`bash
npm install project-name
\`\`\`

## Quick Start

\`\`\`typescript
import { thing } from 'project-name';
thing.doSomething();
\`\`\`

## Documentation

[Full documentation](./docs/)

## Contributing

[Contributing guide](./CONTRIBUTING.md)

## License

MIT
```

## API Documentation Example

```markdown
## POST /api/users

Create a new user.

### Request

\`\`\`json
{
  "email": "user@example.com",
  "name": "John Doe"
}
\`\`\`

### Response

\`\`\`json
{
  "id": "123",
  "email": "user@example.com",
  "name": "John Doe",
  "createdAt": "2024-01-01T00:00:00Z"
}
\`\`\`

### Errors

| Code | Description |
|------|-------------|
| 400 | Invalid request body |
| 409 | Email already exists |
```

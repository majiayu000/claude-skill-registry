---
name: documentation-writer
description: 生成全面的文档，包括README文件、API文档、代码注释（JSDoc、docstrings、XML）和架构文档。
metadata:
  short-description: 生成项目文档
---

# Documentation Writer Skill

## Description
Generate comprehensive documentation for code, APIs, and projects.

## Trigger
- `/docs` command
- User requests documentation
- User needs README or API docs

## Prompt

You are a technical writer that creates clear, comprehensive documentation.

### README Template

```markdown
# Project Name

Brief description of what this project does.

## Features

- ✅ Feature 1
- ✅ Feature 2
- 🚧 Feature 3 (in progress)

## Quick Start

\`\`\`bash
# Clone the repository
git clone https://github.com/user/project.git
cd project

# Install dependencies
npm install

# Start development server
npm run dev
\`\`\`

## Installation

### Prerequisites

- Node.js >= 18
- PostgreSQL >= 14

### Environment Variables

\`\`\`env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
JWT_SECRET=your-secret-key
\`\`\`

## Usage

\`\`\`typescript
import { Client } from 'my-library';

const client = new Client({ apiKey: 'xxx' });
const result = await client.doSomething();
\`\`\`

## API Reference

### `client.createUser(data)`

Creates a new user.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| email | string | Yes | User's email |
| name | string | Yes | User's name |

**Returns:** `Promise<User>`

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing`)
5. Open a Pull Request

## License

MIT © [Your Name]
```

### JSDoc Comments

```typescript
/**
 * Creates a new user in the system.
 * 
 * @param {CreateUserDto} data - The user creation data
 * @param {string} data.email - User's email address (must be unique)
 * @param {string} data.name - User's display name
 * @param {string} [data.avatar] - Optional avatar URL
 * @returns {Promise<User>} The created user object
 * @throws {ValidationError} If email format is invalid
 * @throws {DuplicateError} If email already exists
 * 
 * @example
 * const user = await userService.createUser({
 *   email: 'john@example.com',
 *   name: 'John Doe'
 * });
 */
async createUser(data: CreateUserDto): Promise<User> {
  // implementation
}
```

### C# XML Documentation

```csharp
/// <summary>
/// Creates a new user in the system.
/// </summary>
/// <param name="data">The user creation data.</param>
/// <returns>The created user object.</returns>
/// <exception cref="ValidationException">Thrown when email format is invalid.</exception>
/// <exception cref="DuplicateException">Thrown when email already exists.</exception>
/// <example>
/// <code>
/// var user = await userService.CreateUserAsync(new CreateUserDto
/// {
///     Email = "john@example.com",
///     Name = "John Doe"
/// });
/// </code>
/// </example>
public async Task<User> CreateUserAsync(CreateUserDto data)
{
    // implementation
}
```

## Tags
`documentation`, `readme`, `api-docs`, `comments`, `technical-writing`

## Compatibility
- Codex: ✅
- Claude Code: ✅

---
name: documentation-generation
description: Create comprehensive technical documentation including API docs, component libraries, README files, architecture diagrams, and developer guides using tools like JSDoc, Storybook, or Docusaurus. Use when documenting APIs, creating component documentation, writing README files, generating API references, documenting architecture decisions, creating onboarding guides, maintaining changelogs, documenting configuration options, or building developer documentation sites.
---

# Documentation Generation - Creating Clear, Maintainable Docs

## When to use this skill

- Documenting REST or GraphQL APIs
- Creating component libraries with Storybook
- Writing comprehensive README files
- Generating API reference documentation
- Documenting architecture decisions (ADRs)
- Creating developer onboarding guides
- Maintaining changelogs and release notes
- Documenting configuration and environment variables
- Building documentation sites with Docusaurus
- Writing inline code documentation (JSDoc, TSDoc)
- Creating visual architecture diagrams
- Documenting deployment and operational procedures

## When to use this skill

- Creating API documentation, writing technical guides, generating code documentation, or maintaining project wikis.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Creating API documentation, writing technical guides, generating code documentation, or maintaining project wikis.

## Core Principles

1. **Docs as Code** - Version control, review process, automated generation
2. **Single Source of Truth** - Generate from code when possible
3. **Keep It Fresh** - Automated checks for outdated docs
4. **Examples Over Explanations** - Show, don't just tell
5. **Audience-Specific** - Different docs for different users

## API Documentation

### 1. **OpenAPI/Swagger (REST APIs)**

```typescript
// ✅ JSDoc comments for automatic documentation
/**
 * @swagger
 * /users:
 *   get:
 *     summary: List all users
 *     description: Returns a paginated list of users
 *     tags:
 *       - Users
 *     parameters:
 *       - in: query
 *         name: page
 *         schema:
 *           type: integer
 *           default: 1
 *         description: Page number
 *       - in: query
 *         name: limit
 *         schema:
 *           type: integer
 *           default: 20
 *         description: Items per page
 *     responses:
 *       200:
 *         description: Success
 *         content:
 *           application/json:
 *             schema:
 *               type: object
 *               properties:
 *                 data:
 *                   type: array
 *                   items:
 *                     $ref: '#/components/schemas/User'
 *                 meta:
 *                   type: object
 *                   properties:
 *                     page:
 *                       type: integer
 *                     total:
 *                       type: integer
 */
app.get('/users', async (req, res) => {
  // Implementation
});

/**
 * @swagger
 * components:
 *   schemas:
 *     User:
 *       type: object
 *       required:
 *         - id
 *         - email
 *       properties:
 *         id:
 *           type: string
 *           example: "123"
 *         email:
 *           type: string
 *           format: email
 *           example: "user@example.com"
 *         name:
 *           type: string
 *           example: "John Doe"
 *         createdAt:
 *           type: string
 *           format: date-time
 */
```

```typescript
// Setup Swagger UI
import swaggerJsdoc from 'swagger-jsdoc';
import swaggerUi from 'swagger-ui-express';

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'My API',
      version: '1.0.0',
      description: 'API documentation',
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Development server',
      },
    ],
  },
  apis: ['./routes/*.ts'], // Files with @swagger comments
};

const specs = swaggerJsdoc(options);
app.use('/api-docs', swaggerUi.serve, swaggerUi.setup(specs));
```

### 2. **TypeDoc (TypeScript)**

```typescript
// ✅ JSDoc comments for TypeDoc
/**
 * Represents a user in the system
 */
export interface User {
  /** Unique identifier */
  id: string;
  /** User's email address */
  email: string;
  /** User's display name */
  name: string;
  /** Account creation timestamp */
  createdAt: Date;
}

/**
 * Service for managing users
 * @example
 * ```typescript
 * const userService = new UserService();
 * const user = await userService.createUser({
 *   email: 'user@example.com',
 *   name: 'John Doe'
 * });
 * ```
 */
export class UserService {
  /**
   * Creates a new user
   * @param data - User creation data
   * @returns The created user
   * @throws {ValidationError} If email is invalid
   * @throws {ConflictError} If email already exists
   */
  async createUser(data: CreateUserData): Promise<User> {
    // Implementation
  }

  /**
   * Finds a user by ID
   * @param id - User ID
   * @returns User object or null if not found
   */
  async findById(id: string): Promise<User | null> {
    // Implementation
  }
}
```

```json
// typedoc.json
{
  "entryPoints": ["src/index.ts"],
  "out": "docs",
  "plugin": ["typedoc-plugin-markdown"],
  "excludePrivate": true,
  "includeVersion": true
}
```

```bash
# Generate documentation
npx typedoc
```

### 3. **GraphQL Documentation (Auto-generated)**

```typescript
// GraphQL schema with descriptions
const typeDefs = gql`
  """
  Represents a user in the system
  """
  type User {
    """Unique identifier"""
    id: ID!
    
    """User's email address"""
    email: String!
    
    """User's display name"""
    name: String!
    
    """Posts authored by this user"""
    posts: [Post!]!
  }

  """
  Input for creating a new user
  """
  input CreateUserInput {
    """Valid email address"""
    email: String!
    
    """Display name (3-50 characters)"""
    name: String!
    
    """Password (minimum 8 characters)"""
    password: String!
  }

  type Query {
    """
    Get a single user by ID
    @example
    query {
      user(id: "123") {
        id
        email
        name
      }
    }
    """
    user(id: ID!): User
    
    """
    List all users with pagination
    """
    users(limit: Int = 20, offset: Int = 0): [User!]!
  }
`;

// GraphQL Playground provides interactive docs automatically
```

## Code Documentation

### 1. **README.md Template**

```markdown
# Project Name

Brief description of what this project does.

## Features

- 🚀 Feature 1
- 📦 Feature 2
- ⚡ Feature 3

## Quick Start

\`\`\`bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
\`\`\`

## Installation

Detailed installation instructions...

## Usage

Basic usage examples:

\`\`\`typescript
import { MyLibrary } from 'my-library';

const instance = new MyLibrary({
  apiKey: 'your-key'
});

const result = await instance.doSomething();
\`\`\`

## API Reference

See [API Documentation](./docs/api.md)

## Configuration

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | - |
| `PORT` | Server port | `3000` |
| `NODE_ENV` | Environment | `development` |

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
```

### 2. **CHANGELOG.md**

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New feature X
- Support for Y

### Changed
- Improved performance of Z

### Deprecated
- Old API endpoint /v1/users (use /v2/users instead)

### Removed
- Unused dependency foo

### Fixed
- Bug in authentication flow
- Memory leak in WebSocket handler

### Security
- Updated dependencies with security vulnerabilities

## [2.1.0] - 2024-01-15

### Added
- User profile customization
- Dark mode support

### Fixed
- Login redirect issue

## [2.0.0] - 2024-01-01

### Changed
- **BREAKING**: Renamed `getUser()` to `fetchUser()`
- **BREAKING**: Changed response format for `/api/users`

### Migration Guide

\`\`\`typescript
// Before
const user = await api.getUser(id);

// After
const user = await api.fetchUser(id);
\`\`\`
```

### 3. **JSDoc for Functions**

```typescript
/**
 * Calculates the total price including tax and shipping
 * 
 * @param items - Array of cart items
 * @param options - Calculation options
 * @param options.taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param options.shippingCost - Flat shipping cost
 * @returns Total price object
 * 
 * @example
 * ```typescript
 * const total = calculateTotal(
 *   [{ price: 10, quantity: 2 }],
 *   { taxRate: 0.08, shippingCost: 5 }
 * );
 * // Returns: { subtotal: 20, tax: 1.6, shipping: 5, total: 26.6 }
 * ```
 * 
 * @throws {ValidationError} If items array is empty
 * @throws {ValidationError} If taxRate is negative
 */
export function calculateTotal(
  items: CartItem[],
  options: {
    taxRate: number;
    shippingCost: number;
  }
): TotalPrice {
  // Implementation
}
```

## Documentation Sites

### 1. **VitePress (Modern Static Site)**

```markdown
<!-- docs/index.md -->
---
layout: home
hero:
  name: My Library
  text: A modern TypeScript library
  tagline: Fast, type-safe, and easy to use
  actions:
    - theme: brand
      text: Get Started
      link: /guide/
    - theme: alt
      text: View on GitHub
      link: https://github.com/user/repo
features:
  - title: Fast
    details: Built with performance in mind
  - title: Type-safe
    details: Full TypeScript support
  - title: Simple
    details: Easy to learn and use
---

<!-- docs/guide/index.md -->
# Getting Started

## Installation

::: code-group
\`\`\`bash [npm]
npm install my-library
\`\`\`

\`\`\`bash [yarn]
yarn add my-library
\`\`\`

\`\`\`bash [pnpm]
pnpm add my-library
\`\`\`
:::

## Quick Example

\`\`\`typescript
import { createClient } from 'my-library';

const client = createClient({
  apiKey: process.env.API_KEY
});

const data = await client.fetch('/users');
\`\`\`

## Next Steps

- [Configuration](/guide/configuration)
- [API Reference](/api/)
- [Examples](/examples/)
```

```typescript
// docs/.vitepress/config.ts
import { defineConfig } from 'vitepress';

export default defineConfig({
  title: 'My Library',
  description: 'Documentation for My Library',
  
  themeConfig: {
    nav: [
      { text: 'Guide', link: '/guide/' },
      { text: 'API', link: '/api/' },
      { text: 'Examples', link: '/examples/' }
    ],
    
    sidebar: {
      '/guide/': [
        {
          text: 'Introduction',
          items: [
            { text: 'Getting Started', link: '/guide/' },
            { text: 'Installation', link: '/guide/installation' },
            { text: 'Configuration', link: '/guide/configuration' }
          ]
        },
        {
          text: 'Core Concepts',
          items: [
            { text: 'Authentication', link: '/guide/auth' },
            { text: 'Data Fetching', link: '/guide/fetching' }
          ]
        }
      ]
    },
    
    socialLinks: [
      { icon: 'github', link: 'https://github.com/user/repo' }
    ]
  }
});
```

### 2. **Docusaurus (React-based)**

```jsx
// docusaurus.config.js
module.exports = {
  title: 'My Library',
  tagline: 'A modern TypeScript library',
  url: 'https://mylib.dev',
  baseUrl: '/',
  
  presets: [
    [
      '@docusaurus/preset-classic',
      {
        docs: {
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl: 'https://github.com/user/repo/edit/main/',
        },
        blog: {
          showReadingTime: true,
        },
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  
  themeConfig: {
    navbar: {
      title: 'My Library',
      items: [
        { to: '/docs/intro', label: 'Docs', position: 'left' },
        { to: '/blog', label: 'Blog', position: 'left' },
        {
          href: 'https://github.com/user/repo',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
  },
};
```

## Automated Checks

### 1. **Link Checking**

```yaml
# .github/workflows/docs.yml
name: Check Docs

on: [push, pull_request]

jobs:
  check-links:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check broken links
        uses: gaurav-nelson/github-action-markdown-link-check@v1
        with:
          folder-path: 'docs/'
          config-file: '.markdown-link-check.json'
```

### 2. **Code Examples Testing**

```typescript
// Extract and test code examples from markdown
import { readFileSync } from 'fs';

describe('Documentation Examples', () => {
  it('README example works', () => {
    const readme = readFileSync('README.md', 'utf-8');
    const codeBlocks = readme.match(/```typescript\n([\s\S]*?)```/g);
    
    // Test each code block
    for (const block of codeBlocks) {
      const code = block.replace(/```typescript\n/, '').replace(/```$/, '');
      expect(() => eval(code)).not.toThrow();
    }
  });
});
```

## Documentation Checklist

```
Essential Documentation:
□ README.md with quick start
□ CHANGELOG.md with versions
□ LICENSE file
□ CONTRIBUTING.md for contributors
□ API reference documentation
□ Configuration guide

Code Documentation:
□ JSDoc comments on public APIs
□ Type definitions exported
□ Examples for complex functions
□ Error conditions documented
□ Breaking changes noted

Quality:
□ No broken links
□ Code examples tested
□ Screenshots up to date
□ Search functionality
□ Mobile-responsive
□ Accessible (WCAG)

Maintenance:
□ Automated generation from code
□ Versioned documentation
□ CI/CD checks for docs
□ Deprecation warnings visible
□ Migration guides for breaking changes
```

## Resources

- [Write the Docs](https://www.writethedocs.org/)
- [The Good Docs Project](https://thegooddocsproject.dev/)
- [VitePress](https://vitepress.dev/)
- [Docusaurus](https://docusaurus.io/)

---

**Remember**: Documentation is part of your product. Keep it accurate, accessible, and up-to-date.

---
name: readme-updates
description: Maintain README files with setup instructions, features, tech stack, and usage examples. Use when updating project documentation, adding new features, improving onboarding, or creating READMEs for new packages.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# README Updates Skill

## Root README Structure

```markdown
# SG Cars Trends

[![License](https://img.shields.io/github/license/sgcarstrends/sgcarstrends)](LICENSE)
[![CI](https://github.com/sgcarstrends/sgcarstrends/workflows/CI/badge.svg)](https://github.com/sgcarstrends/sgcarstrends/actions)

> Platform for accessing Singapore vehicle registration and COE bidding data

## Features

- 📊 **Comprehensive Data**: Car registration and COE bidding data
- 🔄 **Real-time Updates**: Automated daily updates from LTA DataMall
- 📝 **AI-Generated Blog**: Automated insights using Google Gemini

## Quick Start

\`\`\`bash
git clone https://github.com/sgcarstrends/sgcarstrends.git
cd sgcarstrends
pnpm install
cp .env.example .env
pnpm db:migrate
pnpm dev
\`\`\`

## Tech Stack

- **Frontend**: Next.js 16, HeroUI, Recharts, Tailwind CSS
- **Backend**: Hono, Drizzle ORM, PostgreSQL, Upstash Redis
- **Infrastructure**: SST v3, AWS Lambda, Cloudflare
- **AI**: Google Gemini, QStash workflows

## Project Structure

\`\`\`
sgcarstrends/
├── apps/
│   ├── api/          # Hono API
│   └── web/          # Next.js web app
├── packages/
│   ├── database/     # Drizzle schemas
│   ├── ui/           # UI components
│   └── utils/        # Shared utilities
└── infra/            # SST infrastructure
\`\`\`

## Development

\`\`\`bash
pnpm dev          # Start all servers
pnpm test         # Run tests
pnpm build        # Build for production
\`\`\`

## License

MIT
```

## Package README Template

```markdown
# @sgcarstrends/[package-name]

> Brief description

## Installation

\`\`\`bash
pnpm add @sgcarstrends/[package-name]
\`\`\`

## Usage

\`\`\`typescript
import { functionName } from "@sgcarstrends/[package-name]";

const result = functionName();
\`\`\`

## API

### `functionName(param: string): ReturnType`

Description.

**Parameters:** `param` (string) - Description

**Returns:** `ReturnType` - Description

## Development

\`\`\`bash
pnpm test
pnpm build
\`\`\`

## License

MIT
```

## Common Badges

```markdown
[![License](https://img.shields.io/github/license/user/repo)](LICENSE)
[![CI](https://github.com/user/repo/workflows/CI/badge.svg)](actions)
[![npm](https://img.shields.io/npm/v/@sgcarstrends/package)](npm)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.3-blue)](typescript)
```

## Environment Variables Section

```markdown
## Environment Variables

Create `.env` from `.env.example`:

\`\`\`env
DATABASE_URL=postgresql://user:pass@localhost:5432/db
UPSTASH_REDIS_REST_URL=https://your-redis.upstash.io
UPSTASH_REDIS_REST_TOKEN=your-token
\`\`\`
```

## Update Checklist

- [ ] Features list current when new features added
- [ ] Tech stack updated when dependencies change
- [ ] Setup instructions accurate when process changes
- [ ] Examples working and up-to-date
- [ ] Links not broken

## Validate README

```bash
# Check for broken links
pnpm dlx markdown-link-check README.md

# Lint markdown
pnpm dlx markdownlint README.md
```

## Best Practices

1. **Clear Description**: Concise project description at top
2. **Quick Start**: Immediate value with copy-paste setup
3. **Working Examples**: Test all code examples
4. **Keep Updated**: Update when features change
5. **Check Links**: Regularly verify links work

## References

- Shields.io: https://shields.io (badges)
- markdownlint: https://github.com/DavidAnson/markdownlint

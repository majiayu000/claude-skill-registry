---
name: thesys-generative-ui
description: AI-powered generative UI with Thesys - create React components from natural language.
license: MIT
---

# Thesys Generative UI

**Last Updated**: 2025-11-10

## Quick Start

```typescript
import { generateUI } from 'thesys';

const ui = await generateUI({
  prompt: 'Create a user profile card with avatar, name, and email',
  schema: {
    type: 'component',
    props: ['name', 'email', 'avatar']
  }
});

export default function Profile() {
  return <div>{ui}</div>;
}
```

## Core Features

- **Natural Language**: Describe UI in plain English
- **Schema-Driven**: Type-safe component generation
- **React Components**: Generate production-ready components
- **AI-Powered**: Uses LLMs for intelligent design

## Example

```typescript
const form = await generateUI({
  prompt: 'Create a contact form with name, email, and message fields',
  theme: 'modern'
});
```

## Resources

### Core Documentation
- `references/what-is-thesys.md` - What is TheSys C1, success metrics, getting started
- `references/use-cases-examples.md` - When to use, 12 errors prevented, all templates catalog
- `references/tool-calling.md` - Complete tool calling guide with Zod schemas
- `references/integration-guide.md` - Complete setup for Vite, Next.js, Cloudflare Workers

### Additional References
- `references/component-api.md` - Complete component prop reference
- `references/ai-provider-setup.md` - OpenAI, Anthropic, Cloudflare Workers AI setup
- `references/tool-calling-guide.md` - Tool calling patterns
- `references/theme-customization.md` - Theme system deep dive
- `references/common-errors.md` - Expanded error catalog

### Templates (15+ files)
- **Vite + React**: `basic-chat.tsx`, `custom-component.tsx`, `tool-calling.tsx`, `theme-dark-mode.tsx`
- **Next.js**: `app/page.tsx`, `app/api/chat/route.ts`, `tool-calling-route.ts`
- **Cloudflare Workers**: `worker-backend.ts`, `frontend-setup.tsx`
- **Utilities**: `theme-config.ts`, `tool-schemas.ts`, `streaming-utils.ts`

**Official Docs**: https://docs.thesys.dev | **Playground**: https://console.thesys.dev/playground

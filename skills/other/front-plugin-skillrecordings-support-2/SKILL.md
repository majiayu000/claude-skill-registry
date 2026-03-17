---
name: front-plugin
description: Build Front plugins using the Plugin SDK. Use when creating sidebar plugins, composer plugins, or extending Front's UI. Triggers on plugin, front plugin, sidebar plugin, composer plugin, @frontapp/plugin-sdk.
---

# Front Plugin Development

Build production-ready plugins for Front using the official Plugin SDK (`@frontapp/plugin-sdk`).

## When to Use This Skill

- Creating a sidebar plugin (context panel in Front)
- Creating a composer plugin (message toolbar integration)
- Extending Front's UI with custom functionality
- Working with the Plugin SDK (not the REST API)

## Plugin Types

1. **Sidebar Plugin** - Appears in Front sidebar, shows context for selected conversation(s)
2. **Composer Plugin** - Appears in message composer toolbar, operates on draft being composed

## Key Distinction

- **Plugin SDK** (`@frontapp/plugin-sdk`) - Client-side, runs in iframe embedded in Front
- **REST API** (`packages/core/src/front/client.ts`) - Server-side, webhooks and API calls

This skill is for the Plugin SDK. For REST API operations (webhooks, drafts via API), see the `front-webhook` skill.

## Quick Start

```tsx
// src/providers/frontContext.tsx
import { createContext, useContext, useEffect, useState } from 'react'
import Front from '@frontapp/plugin-sdk'

const FrontContext = createContext()

export function useFrontContext() {
  return useContext(FrontContext)
}

export function FrontContextProvider({ children }) {
  const [context, setContext] = useState()

  useEffect(() => {
    const subscription = Front.contextUpdates.subscribe(ctx => {
      setContext(ctx)
    })
    return () => subscription.unsubscribe()
  }, [])

  return (
    <FrontContext.Provider value={context}>
      {children}
    </FrontContext.Provider>
  )
}
```

```tsx
// src/App.tsx
import { useFrontContext } from './providers/frontContext'

function App() {
  const context = useFrontContext()

  if (!context) return <div>Waiting for Front context...</div>

  switch (context.type) {
    case 'noConversation':
      return <div>Select a conversation to use this plugin.</div>
    case 'singleConversation':
      return <MainPlugin />
    case 'multiConversations':
      return <div>Select only one conversation.</div>
    default:
      return <div>Unsupported context type</div>
  }
}
```

## Context Types

| Type | Description |
|------|-------------|
| `noConversation` | No conversation selected |
| `singleConversation` | One conversation selected (most common) |
| `multiConversations` | Multiple conversations selected |
| `messageComposer` | Composer plugin context |

## Common SDK Methods

```ts
// List messages in conversation
const messages = await context.listMessages()

// Create a draft reply
await context.createDraft({
  content: { body: 'Hello!', type: 'text' },
  replyOptions: { type: 'replyAll', originalMessageId: latestMessageId }
})

// Update existing draft
await context.updateDraft(draftId, {
  updateMode: 'replace',
  content: { body: 'Updated content', type: 'html' }
})

// Tag conversation
await context.tag(['tag_123'])

// Assign to teammate
await context.assign('tea_456')

// Open URL in popup (for modals)
await context.openUrlInPopup(url, { width: 400, height: 300 })
```

## Available Context Data

```ts
context.teammate        // Current Front user
context.conversation    // Selected conversation (singleConversation only)
context.conversations   // Selected conversations (multiConversations only)
context.draft          // Current draft (messageComposer only)
```

## UI Guidelines

- Support dark/light mode
- No horizontal scrolling (narrow sidebar)
- Use `lucide-react` for icons
- Graceful loading states (never blank screen)
- Handle missing data with fallbacks

## Detailed Reference

See `rules/` directory for:
- Context types and interfaces
- All SDK methods with signatures
- Draft creation/update patterns
- Attachment handling
- Error handling patterns

## Resources

- [Plugin SDK Overview](https://dev.frontapp.com/docs/plugin-overview)
- [SDK Methods Reference](https://dev.frontapp.com/reference/plugin-sdk-objects)
- [Getting Started Example](https://github.com/frontapp/plugin-getting-started)
- [npm package](https://www.npmjs.com/package/@frontapp/plugin-sdk)

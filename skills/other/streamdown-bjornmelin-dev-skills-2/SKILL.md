---
name: streamdown
description: |
  Expert guidance for Vercel's Streamdown library - a streaming-optimized react-markdown replacement for AI applications.
  Use when: (1) Rendering AI-generated markdown from useChat/streamText,
  (2) Building chat UIs with streaming responses,
  (3) Migrating from react-markdown to streaming-friendly rendering,
  (4) Configuring code blocks (Shiki), math (KaTeX), diagrams (Mermaid),
  (5) Handling incomplete markdown during AI streaming (remend preprocessor),
  (6) Customizing markdown styling with Tailwind/CSS variables,
  (7) Securing AI output with rehype-harden (link/image protocols).
  Triggers: Streamdown, streaming markdown, AI chat markdown, react-markdown replacement,
  AI Elements Response, incomplete markdown, remend, Shiki themes, Mermaid diagrams,
  KaTeX math, rehype-harden, isAnimating, markdown streaming.
---

# Streamdown - AI Streaming Markdown

Streamdown is a drop-in react-markdown replacement designed for AI-powered streaming applications. It handles incomplete markdown syntax gracefully using the remend preprocessor.

## Quick Start

### Installation

```bash
# Direct installation
pnpm add streamdown

# Or via AI Elements CLI (includes Response component)
pnpm dlx ai-elements@latest add message
```

### Tailwind Configuration

**Tailwind v4** (globals.css):
```css
@source "../node_modules/streamdown/dist/*.js";
```

**Tailwind v3** (tailwind.config.js):
```js
module.exports = {
  content: [
    './app/**/*.{js,ts,jsx,tsx}',
    './node_modules/streamdown/dist/*.js',
  ],
}
```

### Basic Chat Example

```tsx
'use client';
import { useChat } from '@ai-sdk/react';
import { Streamdown } from 'streamdown';

export default function Chat() {
  const { messages, sendMessage, status } = useChat();

  return (
    <>
      {messages.map(message => (
        <div key={message.id}>
          {message.parts
            .filter(part => part.type === 'text')
            .map((part, index) => (
              <Streamdown
                key={index}
                isAnimating={status === 'streaming'}
              >
                {part.text}
              </Streamdown>
            ))}
        </div>
      ))}
    </>
  );
}
```

## Core Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `string` | required | Markdown content to render |
| `isAnimating` | `boolean` | `false` | Disables interactive controls during streaming |
| `mode` | `"streaming" \| "static"` | `"streaming"` | Rendering mode |
| `shikiTheme` | `[BundledTheme, BundledTheme]` | `['github-light', 'github-dark']` | Light/dark syntax themes |
| `controls` | `ControlsConfig \| boolean` | `true` | Button visibility for code/table/mermaid |
| `mermaid` | `MermaidOptions` | `{}` | Diagram configuration |
| `components` | `object` | `{}` | Custom element overrides |
| `className` | `string` | `""` | Container CSS class |
| `remarkPlugins` | `Pluggable[]` | GFM, math, CJK | Markdown preprocessing |
| `rehypePlugins` | `Pluggable[]` | raw, katex, harden | HTML processing |
| `parseIncompleteMarkdown` | `boolean` | `true` | Enable remend preprocessor |

## AI SDK Integration

### Status-Based isAnimating

The `status` from useChat maps directly to Streamdown's `isAnimating`:

```tsx
const { messages, status } = useChat();
// status: 'submitted' | 'streaming' | 'ready' | 'error'

<Streamdown isAnimating={status === 'streaming'}>
  {content}
</Streamdown>
```

### Message Parts Pattern

AI SDK v6 uses message parts instead of content string:

```tsx
{messages.map(message => (
  <div key={message.id}>
    {message.parts
      .filter(part => part.type === 'text')
      .map((part, index) => (
        <Streamdown key={index} isAnimating={status === 'streaming'}>
          {part.text}
        </Streamdown>
      ))}
  </div>
))}
```

### Memoized Response Component

Wrap Streamdown with React.memo for performance:

```tsx
import { memo, ComponentProps } from 'react';
import { Streamdown } from 'streamdown';

export const Response = memo(
  ({ className, ...props }: ComponentProps<typeof Streamdown>) => (
    <Streamdown
      className={cn('prose dark:prose-invert max-w-none', className)}
      {...props}
    />
  )
);
```

## Configuration Examples

### Shiki Themes

```tsx
import type { BundledTheme } from 'shiki';

const themes: [BundledTheme, BundledTheme] = ['github-light', 'github-dark'];

<Streamdown shikiTheme={themes}>{content}</Streamdown>
```

### Controls

```tsx
<Streamdown
  controls={{
    code: true,           // Copy button on code blocks
    table: true,          // Download button on tables
    mermaid: {
      copy: true,         // Copy diagram source
      download: true,     // Download as SVG
      fullscreen: true,   // Fullscreen view
      panZoom: true,      // Pan/zoom controls
    },
  }}
>
  {content}
</Streamdown>
```

### Mermaid Diagrams

```tsx
import type { MermaidConfig } from 'streamdown';

const mermaidConfig: MermaidConfig = {
  theme: 'base',
  themeVariables: {
    fontFamily: 'Inter, sans-serif',
    primaryColor: 'hsl(var(--primary))',
    lineColor: 'hsl(var(--border))',
  },
};

<Streamdown mermaid={{ config: mermaidConfig }}>{content}</Streamdown>
```

### Custom Error Component for Mermaid

```tsx
import type { MermaidErrorComponentProps } from 'streamdown';

const MermaidError = ({ error, chart, retry }: MermaidErrorComponentProps) => (
  <div className="p-4 border border-destructive rounded">
    <p>Failed to render diagram</p>
    <button onClick={retry}>Retry</button>
  </div>
);

<Streamdown mermaid={{ errorComponent: MermaidError }}>{content}</Streamdown>
```

### Custom Components

Override any markdown element:

```tsx
<Streamdown
  components={{
    h1: ({ children }) => <h1 className="text-4xl font-bold">{children}</h1>,
    a: ({ href, children }) => (
      <a href={href} className="text-primary underline">{children}</a>
    ),
    code: ({ children, className }) => (
      <code className={cn('bg-muted px-1 rounded', className)}>{children}</code>
    ),
  }}
>
  {content}
</Streamdown>
```

### Security Configuration

Restrict protocols for AI-generated content:

```tsx
import { defaultRehypePlugins } from 'streamdown';
import { harden } from 'rehype-harden';

<Streamdown
  rehypePlugins={[
    defaultRehypePlugins.raw,
    defaultRehypePlugins.katex,
    [harden, {
      allowedProtocols: ['http', 'https', 'mailto'],
      allowedLinkPrefixes: ['https://your-domain.com'],
      allowDataImages: false,
    }],
  ]}
>
  {content}
</Streamdown>
```

## Streaming vs Static Mode

| Mode | Use Case | Features |
|------|----------|----------|
| `streaming` | AI chat responses | Block parsing, incomplete markdown handling, memoization |
| `static` | Blog posts, docs | Simpler rendering, no streaming optimizations |

```tsx
// Static mode for pre-rendered content
<Streamdown mode="static">{blogContent}</Streamdown>
```

## Built-in Features

- **GFM**: Tables, task lists, strikethrough, autolinks
- **Math**: KaTeX rendering with `$$...$$` syntax
- **Code**: Shiki syntax highlighting (200+ languages)
- **Diagrams**: Mermaid with interactive controls
- **CJK**: Proper emphasis handling for Chinese/Japanese/Korean
- **Security**: rehype-harden for link/image protocol restrictions

## Reference Files

| Reference | Topics |
|-----------|--------|
| [api-reference.md](references/api-reference.md) | Complete props, types, plugins, data attributes |
| [ai-sdk-integration.md](references/ai-sdk-integration.md) | useChat patterns, server setup, message parts |
| [styling-security.md](references/styling-security.md) | Tailwind, CSS variables, custom components, rehype-harden |

## Common Patterns

### Next.js Configuration

If you see bundling errors with Mermaid:

```js
// next.config.js
module.exports = {
  serverComponentsExternalPackages: ['langium', '@mermaid-js/parser'],
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.alias = {
        ...config.resolve.alias,
        'vscode-jsonrpc': false,
        'langium': false,
      };
    }
    return config;
  },
};
```

### Shiki External Package

```js
// next.config.js
{
  transpilePackages: ['shiki'],
}
```

## Version Notes

- **Streamdown**: Works with React 18+ (optimized for React 19)
- **AI SDK**: Designed for v6 (status-based streaming state)
- **Tailwind**: Supports v3 and v4 configurations

---
name: react-grab
description: Setup and configure React Grab to let you click elements in your running app and send them directly to Claude Code for editing. Use when setting up React Grab, when the user wants to click UI elements to modify them, or mentions wanting visual element selection for development. Makes AI coding agents 66% faster.
---

# React Grab

React Grab lets you hold ⌘C (Cmd+C on Mac, Ctrl+C on Windows) and click any element in your running web app to automatically capture its context and send it to Claude Code for modification.

**Performance:** Makes tools like Claude Code, Cursor, and Copilot run up to 66% faster by providing precise element context.

## What This Does

Instead of describing which UI element you want to change, you literally just click it. React Grab captures:
- The file name
- The React component code
- The HTML source

This context goes directly to your AI coding agent for instant modifications.

## Easiest Setup (Recommended)

### Automatic CLI Installer

Run this at your project root (where `next.config.ts` or `vite.config.ts` lives):

```bash
npx @react-grab/cli@latest
```

The CLI automatically detects your framework and configures everything. Just refresh your browser after.

## Manual Setup (If Needed)

### For Any JavaScript App (Universal Method)

Add this script tag to your HTML:

```html
<script
  src="//unpkg.com/react-grab/dist/index.global.js"
  crossorigin="anonymous"
></script>
```

**Where to add it:**
- In `index.html` - put it in the `<head>` section
- Only for development - don't ship this to production

### For Next.js App Router (app directory)

In your `app/layout.tsx`:

```typescript
import Script from "next/script";

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        {process.env.NODE_ENV === "development" && (
          <Script
            src="//unpkg.com/react-grab/dist/index.global.js"
            crossOrigin="anonymous"
            strategy="beforeInteractive"
          />
        )}
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### For Next.js Pages Router (pages directory)

In your `pages/_document.tsx`:

```typescript
import { Html, Head, Main, NextScript } from "next/document";
import Script from "next/script";

export default function Document() {
  return (
    <Html lang="en">
      <Head>
        {process.env.NODE_ENV === "development" && (
          <Script
            src="//unpkg.com/react-grab/dist/index.global.js"
            crossOrigin="anonymous"
            strategy="beforeInteractive"
          />
        )}
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

### For Vite

Your `index.html` should look like this:

```html
<!doctype html>
<html lang="en">
  <head>
    <script type="module">
      // First: npm i react-grab
      if (import.meta.env.DEV) {
        import("react-grab");
      }
    </script>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

### For Webpack

First, install React Grab:
```bash
npm install react-grab
```

Then add this at the top of your main entry file (e.g., `src/index.tsx`):

```typescript
if (process.env.NODE_ENV === "development") {
  import("react-grab");
}
```

## Claude Code Agent Integration (Beta)

React Grab can send selected element context **directly to Claude Code** - no copying and pasting needed. Just select an element and Claude Code automatically receives the context and can make changes.

### Server Setup

The server runs on port `4567` and interfaces with the Claude Agent SDK. 

Add to your `package.json`:
```json
{
  "scripts": {
    "dev": "npx @react-grab/claude-code@latest && next dev"
  }
}
```

This starts the React Grab server before your dev server.

### Client Setup

Add the Claude Code client script to your app:

**HTML:**
```html
<script src="//unpkg.com/react-grab/dist/index.global.js"></script>
<script src="//unpkg.com/@react-grab/claude-code/dist/client.global.js"></script>
```

**Next.js (in `app/layout.tsx`):**
```typescript
import Script from "next/script";

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        {process.env.NODE_ENV === "development" && (
          <>
            <Script
              src="//unpkg.com/react-grab/dist/index.global.js"
              strategy="beforeInteractive"
            />
            <Script
              src="//unpkg.com/@react-grab/claude-code/dist/client.global.js"
              strategy="lazyOnload"
            />
          </>
        )}
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### How It Works

1. Start your dev server (the React Grab server starts automatically)
2. Open your app in browser
3. Hold ⌘C and click an element
4. Claude Code receives the context automatically
5. Tell Claude Code what changes you want
6. Claude makes the changes to your codebase

**Flow:**
```
Browser → React Grab → Local Server (port 4567) → Claude Agent SDK → Your Code
```

## How to Use

### Basic Usage (Copy to Clipboard)
1. **Start your dev server** - Run your app normally (`npm run dev`, etc.)
2. **Open your app in a browser** - Navigate to localhost:3000 or wherever it's running
3. **Hold ⌘C (or Ctrl+C)** - Keep it pressed
4. **Click any element** - Click the button, text, card, whatever you want to modify
5. **The context is copied** - File name, component code, and HTML are automatically copied
6. **Tell Claude Code what to change** - Paste into your terminal and describe the modification

### With Claude Code Agent Integration
1. **Start your dev server** - The React Grab server starts automatically
2. **Open your app in a browser**
3. **Hold ⌘C and click an element** - Context is sent directly to Claude Code
4. **Tell Claude Code what to change** - No pasting needed, just describe what you want
5. **Claude makes the changes** - It modifies your actual code files

## Advanced Customization

React Grab provides a customization API if you need more control:

```typescript
import { init } from "react-grab/core";

const api = init({
  theme: {
    enabled: true, // Disable all UI by setting to false
    hue: 180, // Shift colors (e.g., 180 = pink → cyan)
    crosshair: {
      enabled: false, // Disable crosshair
    },
    elementLabel: {
      enabled: false, // Disable element label
    },
  },
  onElementSelect: (element) => {
    console.log("Selected:", element);
  },
  onCopySuccess: (elements, content) => {
    console.log("Copied:", content);
  },
  onStateChange: (state) => {
    console.log("Active:", state.isActive);
  },
});

// Programmatic control
api.activate();
api.copyElement(document.querySelector(".my-element"));
console.log(api.getState());
```

## Important Notes

- **Development only** - The setup ensures React Grab only loads in development mode
- **Works with any framework** - React, Next.js, Vite, Webpack, or plain HTML
- **Compatible with Claude Code and OpenCode** - Direct agent integration available
- **No manual copy-paste with agent integration** - Context flows directly to your AI tool
- **66% faster** - By providing precise element context instead of vague descriptions

## Other Agent Integrations

React Grab also supports OpenCode with a similar setup:

**OpenCode:** Runs on port `6567`, requires `opencode-ai` CLI  
```bash
npm i -g opencode-ai@latest
```

Add to `package.json`:
```json
{
  "scripts": {
    "dev": "npx @react-grab/opencode@latest && next dev"
  }
}
```

Client setup (in `app/layout.tsx`):
```typescript
import Script from "next/script";

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        {process.env.NODE_ENV === "development" && (
          <>
            <Script
              src="//unpkg.com/react-grab/dist/index.global.js"
              strategy="beforeInteractive"
            />
            <Script
              src="//unpkg.com/@react-grab/opencode/dist/client.global.js"
              strategy="lazyOnload"
            />
          </>
        )}
      </head>
      <body>{children}</body>
    </html>
  );
}
```

Check the [React Grab repo](https://github.com/aidenybai/react-grab) for detailed integration docs.

## Troubleshooting

**Not working?**
- Make sure your dev server is running
- Check browser console for errors
- Verify the script tag loaded (look in Network tab)
- Try refreshing the page

**Script not loading?**
- Ensure you're running in development mode
- Try using the CDN URL directly without a bundler first
- Check that `process.env.NODE_ENV === "development"` is evaluating correctly

**Agent integration not working?**
- Verify the server is running on the correct port (4567 for Claude Code)
- Check that both scripts are loaded (react-grab and claude-code client)
- Look for any CORS errors in browser console

## When to Use This Skill

Use this skill when the user:
- Asks to "setup React Grab" or "install React Grab"
- Mentions "click to edit" or "visual selection" for UI elements
- Wants to modify UI elements interactively
- Is working on frontend development and wants faster AI assistance
- Asks about integrating visual element selection with Claude Code
- Wants to connect their browser UI directly to their AI coding agent
- Mentions wanting to speed up their development workflow with AI
- Is frustrated with describing which UI element they want to modify

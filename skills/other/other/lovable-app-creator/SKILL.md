---
name: lovable-app-creator
description: "Generates clickable Lovable.dev build URLs when users ask to build, create, or make any app, website, landing page, dashboard, or store."
homepage: https://lovable.dev
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"💜"}}
---

# Lovable App Creator

When a user asks to build any app, website, or page:

## Step 1: Compose a prompt

Write an app description (200-500 chars). Include app name, theme, colors, pages, features, and "Use shadcn/ui, Tailwind CSS, Framer Motion. Mobile-first responsive."

## Step 2: Build the redirect URL

Use the redirect server running on port 3456. Build this URL with your prompt as plain text (NO URL encoding needed — the server handles it):

```
http://localhost:3456/build?prompt=YOUR PROMPT TEXT HERE
```

## Step 3: Reply with the URL

```
🚀 Your app is ready to build!

📋 App: [Name] — [Type]
🎨 Style: [Theme]

👉 Click to create: http://localhost:3456/build?prompt=[YOUR PLAIN TEXT PROMPT]

🔗 Auto-builds on Lovable.dev. You need a Lovable account.
```

## Example

User: "Build me a portfolio for a photographer, dark theme"

Reply:
```
🚀 Your portfolio is ready to build!

📋 App: NoirFrame — Photographer Portfolio
🎨 Style: Dark minimal, gold accents

👉 Click to create:
http://localhost:3456/build?prompt=Build a dark minimal photographer portfolio called NoirFrame with hero section, photo gallery grid with lightbox, about page, and contact form. Near-black background, gold accents, Playfair Display headings, Inter body font. Use shadcn/ui, Tailwind CSS, Framer Motion. Mobile-first responsive.

🔗 Auto-builds on Lovable.dev. You need a Lovable account.
```

## Rules

- ALWAYS include the redirect URL in your reply
- NEVER tell user to copy/paste
- NEVER write code files
- Keep prompts under 500 characters

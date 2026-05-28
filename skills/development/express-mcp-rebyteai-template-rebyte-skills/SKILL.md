---
name: express-mcp
description: MCP server implementation with Express.js and TypeScript.
---

# Express MCP Server

An MCP (Model Context Protocol) server implementation with Express.js and TypeScript.

## Tech Stack

- **Framework**: Express.js
- **Language**: TypeScript
- **Protocol**: MCP (Model Context Protocol)
- **Package Manager**: npm

## Setup

### 1. Clone the Template

```bash
git clone --depth 1 https://github.com/Eng0AI/express-mcp.git .
```

If the directory is not empty:

```bash
git clone --depth 1 https://github.com/Eng0AI/express-mcp.git _temp_template
mv _temp_template/* _temp_template/.* . 2>/dev/null || true
rm -rf _temp_template
```

### 2. Remove Git History (Optional)

```bash
rm -rf .git
git init
```

### 3. Install Dependencies

```bash
npm install
```

## Build

```bash
npm run build
```

## Development

```bash
npm run dev
```

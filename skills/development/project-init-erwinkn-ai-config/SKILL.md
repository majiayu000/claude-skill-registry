---
name: project-init
description: Guidance for initializing new projects. Use framework/package manager commands instead of manual scaffolding.
---

# Project Initialization Best Practices

When creating new projects, **always prefer official CLI tools and scaffolding commands** over manually creating files and directories. These tools:

- Set up correct project structure and config
- Install dependencies with compatible versions
- Configure build tools, linting, testing
- Follow framework best practices

## JavaScript/TypeScript

| Framework | Command |
|-----------|---------|
| Vite | `bun create vite` or `npm create vite@latest` |
| Next.js | `bunx create-next-app` or `npx create-next-app@latest` |
| Remix | `bunx create-remix` or `npx create-remix@latest` |
| Astro | `bun create astro` or `npm create astro@latest` |
| SvelteKit | `bun create svelte` or `npm create svelte@latest` |
| Nuxt | `bunx nuxi init` or `npx nuxi@latest init` |
| React Native | `npx @react-native-community/cli init` |
| Expo | `bunx create-expo-app` or `npx create-expo-app` |
| Electron | `npm init electron-app@latest` |
| Tauri | `bun create tauri-app` or `npm create tauri-app@latest` |

## Python

| Tool | Command |
|------|---------|
| uv (recommended) | `uv init` or `uv init --lib` for libraries |
| Poetry | `poetry new <name>` or `poetry init` |
| PDM | `pdm init` |
| Hatch | `hatch new <name>` |
| Django | `django-admin startproject <name>` |
| Flask | Use cookiecutter or manual (minimal structure) |
| FastAPI | Use cookiecutter or `fastapi-cli` |

## Other Languages

| Language/Framework | Command |
|-------------------|---------|
| Rust | `cargo new <name>` or `cargo init` |
| Go | `go mod init <module>` |
| Ruby on Rails | `rails new <name>` |
| .NET | `dotnet new <template>` |
| Java (Spring) | Use start.spring.io or Spring CLI |
| Kotlin | `gradle init` or IntelliJ |

## Monorepo Tools

| Tool | Command |
|------|---------|
| Turborepo | `bunx create-turbo` or `npx create-turbo@latest` |
| Nx | `bunx create-nx-workspace` or `npx create-nx-workspace` |
| Lerna | `npx lerna init` |

## Key Principles

1. **Don't manually create config files** - Let the CLI generate them
2. **Use interactive prompts** - Most CLIs ask about TypeScript, linting, testing
3. **Check framework docs** - Commands change; verify current syntax
4. **Prefer bun/bunx** when available - Faster than npm/npx
5. **Use templates** - Many CLIs offer starter templates (e.g., `--template react-ts`)

## When Manual Setup is OK

- Adding to existing monorepo with specific conventions
- Learning how tools work under the hood
- Very minimal projects (single script)
- Custom build requirements not covered by templates

---
name: tamagui
version: 1.0.0
description: Universal React + React Native UI library with optimizing compiler. Use when building cross-platform apps with shared styling, design tokens, themes, and accessible components.
license: MIT
metadata:
  author: ai-standards
  language: typescript
  frameworks: react, react-native, next, expo, vite
compatibility: React 18+, React Native 0.71+
allowed-tools: Read Write Edit Bash Grep Glob
---

# Tamagui Skill

Style React fast with 100% parity on React Native, an optional UI kit, and optimizing compiler.

## Source Code Access

Source code is available locally and on GitHub. Check local first, fall back to GitHub if not available.

| Local path                                  | GitHub                             |
| ------------------------------------------- | ---------------------------------- |
| `opensrc/repos/github.com/tamagui/tamagui/` | https://github.com/tamagui/tamagui |

## Documentation

Core concepts for understanding and using Tamagui's styling system.

| Topic         | Description                              | URL                                                                                                    |
| ------------- | ---------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| Introduction  | Overview and key concepts                | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/intro/introduction.mdx)     |
| Installation  | Getting started and setup                | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/intro/installation.mdx)     |
| Configuration | createTamagui and config options         | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/core/configuration.mdx)     |
| Themes        | Dark/light modes and custom themes       | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/intro/themes.mdx)           |
| Tokens        | Design tokens for spacing, colors, fonts | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/core/tokens.mdx)            |
| styled()      | Create styled components with variants   | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/core/styled.mdx)            |
| Animations    | Animation drivers and configuration      | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/core/animations.mdx)        |
| Compiler      | Optimizing compiler setup                | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/intro/compiler-install.mdx) |
| UI Components | Pre-built component library overview     | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/components/intro/1.0.0.mdx) |

## Source Code

Direct links to implementation code in the monorepo.

| Area             | Description                          | Path                                                     |
| ---------------- | ------------------------------------ | -------------------------------------------------------- |
| Repository       | Main monorepo with all packages      | `opensrc/repos/github.com/tamagui/tamagui`               |
| UI Components    | 50+ themed, accessible components    | `opensrc/repos/github.com/tamagui/tamagui/code/ui`       |
| Core Packages    | Styling engine, themes, hooks, fonts | `opensrc/repos/github.com/tamagui/tamagui/code/core`     |
| Compiler Plugins | Bundler plugins for style extraction | `opensrc/repos/github.com/tamagui/tamagui/code/compiler` |

## Framework Guides

Setup instructions for integrating Tamagui with specific frameworks and bundlers.

| Framework | Description                             | Docs                                                                                           |
| --------- | --------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Expo      | React Native with Expo managed workflow | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/guides/expo.mdx)    |
| Next.js   | Server-side rendering and App Router    | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/guides/next-js.mdx) |
| Vite      | Fast web development with HMR           | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/guides/vite.mdx)    |
| Metro     | React Native bundler configuration      | [docs](opensrc/repos/github.com/tamagui/tamagui/code/tamagui.dev/data/docs/guides/metro.mdx)   |

## Local References

Detailed reference files with component and API documentation.

- `references/components.md` - UI component library with docs and source links
- `references/core.md` - Core packages, configuration APIs, and hooks
- `references/compiler.md` - Bundler plugins and optimization setup

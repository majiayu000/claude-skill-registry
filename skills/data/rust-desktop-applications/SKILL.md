---
name: rust-desktop-applications
description: Build cross-platform desktop applications with Rust using Tauri framework and native GUI alternatives
version: 1.0.0
category: development
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Build performant cross-platform desktop apps with Tauri (web UI + Rust backend) or native GUI frameworks"
    when_to_use: "Creating native desktop applications requiring system integration, small bundle sizes, or high performance"
    quick_start: "1. Choose framework (Tauri vs native GUI) 2. Setup project structure 3. Implement IPC/state management 4. Add platform integration 5. Test cross-platform 6. Build and distribute"
  references:
    - tauri-framework.md
    - native-gui-frameworks.md
    - architecture-patterns.md
    - state-management.md
    - platform-integration.md
    - testing-deployment.md
context_limit: 800
tags:
  - rust
  - desktop
  - tauri
  - gui
  - cross-platform
  - native
requires_tools: []
---

# Rust Desktop Applications

## Overview

Rust has emerged as a premier language for building desktop applications that combine native performance with memory safety. The ecosystem offers two main approaches: **Tauri** for hybrid web UI + Rust backend apps (think Electron but 10x smaller and faster), and **native GUI frameworks** like egui, iced, and slint for pure Rust interfaces.

Tauri has revolutionized desktop development by enabling developers to use web technologies (React, Vue, Svelte) for the frontend while leveraging Rust's performance and safety for system-level operations. With bundle sizes under 5MB and memory usage 1/10th of Electron, Tauri apps deliver desktop-class performance. Native frameworks shine for specialized use cases: egui for immediate-mode tools and game editors, iced for Elm-style reactive apps, slint for embedded and declarative UIs.

This skill covers the complete Rust desktop development lifecycle from framework selection through architecture, state management, platform integration, and deployment. You'll build production-ready applications with proper IPC patterns, async runtime integration, native system access, and cross-platform distribution.

## When to Use This Skill

Activate when building desktop applications that need **native performance**, **small bundle sizes**, **system integration**, or **memory safety guarantees**. Specifically use when:

- Building Electron alternatives with web UI + Rust backend (Tauri)
- Creating high-performance developer tools or productivity apps
- Developing system utilities requiring native OS integration
- Building cross-platform apps for Windows, macOS, and Linux
- Need <10MB bundle sizes vs 100MB+ Electron apps
- Implementing real-time applications (audio/video processing, games)
- Creating embedded GUI applications (kiosks, IoT devices)

## Don't Use When

- **Simple web apps** - Use Next.js, Vite, or web frameworks
- **Mobile-first applications** - Use Flutter, React Native, or Kotlin Multiplatform
- **Purely CLI tools** - Use clap/structopt for command-line apps
- **Browser extensions** - Use WebExtensions API
- **Quick prototypes** - Native development has setup overhead
- **Team lacks Rust experience** - Steep learning curve for system programming

## The Iron Law

**TAURI FOR WEB UI + RUST BACKEND | NATIVE GUI FOR PURE RUST | NEVER MIX BUSINESS LOGIC IN FRONTEND**

Duplicating logic between frontend and backend, or bypassing IPC for direct access, violates architecture.

## Core Principles

1. **Framework Alignment**: Tauri for web-skilled teams, native GUI for Rust-first projects
2. **Clear Separation**: Frontend handles UI, Rust backend handles business logic and system access
3. **Type-Safe IPC**: Commands and events strongly typed with serde serialization
4. **Async Runtime**: Tokio for backend concurrency, prevent blocking main thread
5. **Security First**: Validate all IPC inputs, minimize exposed commands, CSP policies
6. **Platform Abstraction**: Write once, handle platform differences gracefully

## Quick Start

1. **Choose Your Framework**
   - **Tauri**: Have web skills (React/Vue/Svelte)? Want rapid UI development? → `cargo install tauri-cli`
   - **Native GUI**: Pure Rust project? Immediate mode or reactive patterns? → Choose egui/iced/slint

2. **Initialize Project**
   ```bash
   # Tauri
   cargo create-tauri-app my-app
   # Select: npm, React/Vue/Svelte, TypeScript

   # Native (egui example)
   cargo new my-app
   cargo add eframe egui
   ```

3. **Setup Architecture**
   - Tauri: Define commands in `src-tauri/src/main.rs`, handle IPC
   - Native: Implement app state, event loop, and UI update logic
   - Structure: `src/` (backend), `ui/` or `src-ui/` (frontend if Tauri)

4. **Implement Core Features**
   - Define Tauri commands with `#[tauri::command]`
   - Setup state management (Arc<Mutex<T>> or channels)
   - Integrate Tokio for async operations
   - Add error handling with `Result<T, E>`

5. **Add Platform Integration**
   - File system access (dialogs, read/write)
   - System tray, notifications, auto-updates
   - Deep linking, custom URL schemes
   - OS-specific features (Windows registry, macOS sandboxing)

6. **Build and Distribute**
   ```bash
   # Development
   cargo tauri dev  # or cargo run

   # Production build
   cargo tauri build  # Creates installers for current platform

   # Cross-platform: Use GitHub Actions with matrix builds
   ```

## Framework Decision Tree

```
Need desktop app?
├─ Have web frontend skills (React/Vue/Svelte)?
│  └─ YES → Use Tauri
│     ├─ Need <5MB bundles? ✓
│     ├─ System integration? ✓
│     ├─ Cross-platform? ✓
│     └─ Rapid UI development? ✓
│
└─ Pure Rust, no web frontend?
   ├─ Game editor or immediate mode tools? → egui
   ├─ Elm-style reactive architecture? → iced
   ├─ Declarative UI, embedded devices? → slint
   └─ Data-first reactive? → druid
```

**Tauri when**: Web UI expertise, need modern frontend frameworks, rapid iteration
**Native when**: Maximum performance, no web dependencies, specialized UI patterns

## Navigation

Detailed guides available:

- **[Tauri Framework](references/tauri-framework.md)**: Complete Tauri architecture, project setup, IPC communication patterns, native API access, configuration, security model, and build process with real-world examples
- **[Native GUI Frameworks](references/native-gui-frameworks.md)**: Deep dive into egui, iced, druid, and slint - architecture patterns, when to use each, comparison matrix, and production code examples
- **[Architecture Patterns](references/architecture-patterns.md)**: Desktop-specific patterns including MVC/MVVM, command pattern, event-driven architecture, plugin systems, resource management, and error handling strategies
- **[State Management](references/state-management.md)**: State management strategies, async runtime integration with Tokio, message passing, reactive patterns, persistence (configs/databases), and multi-window state sharing
- **[Platform Integration](references/platform-integration.md)**: File system access, system tray, notifications, auto-updates, deep linking, OS-specific features (Windows/macOS/Linux), permissions, and security
- **[Testing & Deployment](references/testing-deployment.md)**: Integration testing, UI testing approaches, cross-compilation, platform-specific builds, distribution (installers/bundles/stores), signing, notarization, and CI/CD pipelines

## Key Patterns

**Correct Tauri Pattern:**
```rust
✅ Commands in Rust backend
✅ Type-safe IPC with serde
✅ Async operations with Tokio
✅ State management with Arc<Mutex<T>>
✅ Error propagation with Result<T, E>
✅ Frontend calls backend via invoke()
```

**Correct Native GUI Pattern:**
```rust
✅ Immediate mode (egui) or retained mode (iced)
✅ State updates trigger redraws
✅ Event handling in Rust
✅ Platform-agnostic rendering
✅ Resource cleanup on drop
```

**Incorrect Patterns:**
```rust
❌ Business logic in frontend JavaScript
❌ Exposing unsafe commands without validation
❌ Blocking operations on main thread
❌ Direct filesystem access from frontend
❌ Missing error handling on IPC
❌ Hardcoded platform-specific paths
```

## Red Flags - STOP

- **Blocking the main thread** - Use Tokio spawn for long operations
- **Exposing sensitive commands** - Validate, rate limit, minimize surface area
- **Missing CSP in Tauri** - Configure Content Security Policy
- **No input validation** - Always validate IPC command arguments
- **Direct frontend file access** - Use Tauri file system APIs
- **Ignoring platform differences** - Test on all target platforms
- **Large bundle sizes** - Profile and optimize dependencies
- **No auto-update strategy** - Users won't manually update

## Integration with Other Skills

- **vite-local-dev**: Integrate Vite with Tauri for hot module replacement and fast frontend builds
- **async-testing**: Test async Tokio code in Tauri commands and background tasks
- **performance-profiling**: Profile Rust backend with Criterion, flamegraphs for optimization
- **test-driven-development**: Write tests for commands, state management, and business logic
- **verification-before-completion**: Test cross-platform builds before shipping
- **systematic-debugging**: Debug Tauri IPC issues, inspect console logs, use Rust debugger

## Real-World Impact

**Performance Metrics:**
- Bundle size: 3-5MB (Tauri) vs 100-200MB (Electron)
- Memory usage: 50-100MB (Tauri) vs 500MB-1GB (Electron)
- Startup time: <1s (Tauri) vs 3-5s (Electron)
- Build time: 1-2 min (Tauri) vs 5-10 min (Electron)

**Production Examples:**
- **Warp Terminal**: High-performance terminal built with Rust (egui/custom)
- **Lapce**: Fast code editor using Druid (later custom framework)
- **Zed**: Collaborative code editor with native Rust UI
- **Notion-like apps**: Using Tauri for desktop versions
- **System utilities**: File managers, task managers, monitoring tools

## The Bottom Line

**Rust desktop development offers unmatched performance with memory safety.**

Choose Tauri for web UI + Rust backend with tiny bundles. Choose native GUI for pure Rust with specialized patterns. Architect with clear frontend/backend separation. Use type-safe IPC. Integrate Tokio for async. Handle platform differences. Test cross-platform early.

This is the Rust desktop way.

---
name: project-types
description: |
  Project type definitions with type-specific questions, patterns, and stacks.
  Use when: determining project architecture, asking type-specific questions.
  Referenced by: idea-validation, brainstorming, /ship command.
---

# Project Types Reference

Quick lookup for type-specific questions, patterns, and recommended stacks.

## Type Index

| Type | Complexity | Default PRD | Recommended Stack |
|------|------------|-------------|-------------------|
| CLI Tool | Low | Minimal | Rust (clap) |
| REST API | Low-Medium | Minimal/Standard | Rust (axum) |
| Web App | Medium | Standard | Rust + HTMX |
| Telegram Bot | Medium | Standard | Rust (teloxide) |
| Discord Bot | Medium | Standard | Rust (serenity) |
| GraphQL API | Medium | Standard | Rust (async-graphql) |
| Mobile App | High | Full | Flutter/React Native |
| Data Pipeline | High | Full | Python/Rust |
| Browser Extension | Medium | Standard | TypeScript |

---

## CLI Tool

### Discovery Questions
1. **Execution model**: One-shot or interactive?
2. **Arguments**: Positional args, flags, or subcommands?
3. **Output**: Text, JSON, or files?
4. **Config**: Config file needed?

### Patterns
- Use `clap` for argument parsing
- Support `--json` for machine output
- Use `anyhow` for error handling
- Exit codes: 0 success, 1 error

### Stack
```toml
[dependencies]
clap = { version = "4", features = ["derive"] }
anyhow = "1"
serde_json = "1"  # if JSON output
```

### Example Structure
```
src/
  main.rs      # Entry point, arg parsing
  lib.rs       # Core logic
  commands/    # Subcommand handlers (if needed)
```

---

## REST API

### Discovery Questions
1. **Audience**: Internal, public, or partner?
2. **Auth**: None, API Key, JWT, OAuth2?
3. **Rate limiting**: Needed?
4. **Versioning**: /v1/, header, or none?

### Patterns
- OpenAPI spec first (consider)
- JSON responses with consistent error format
- Health endpoint required: `GET /health`
- Structured logging (tracing)

### Stack
```toml
[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
serde_json = "1"
tracing = "0.1"
tracing-subscriber = "0.3"
```

### Example Structure
```
src/
  main.rs          # Server setup
  lib.rs           # Router, handlers
  routes/          # Route modules
  models/          # Data structures
  middleware/      # Auth, logging
```

---

## Web App (SaaS)

### Discovery Questions
1. **Auth**: Email/password, OAuth, magic link, or none?
2. **Realtime**: WebSocket, SSE, or none?
3. **Multi-tenant**: Yes/no?
4. **Admin panel**: Needed?

### Patterns
- HTMX for interactivity (minimal JS)
- Server-rendered templates (Askama)
- Progressive enhancement
- CSRF protection on forms

### Stack
```toml
[dependencies]
axum = "0.8"
tokio = { version = "1", features = ["full"] }
askama = "0.12"
askama_axum = "0.4"
tower-http = { version = "0.6", features = ["fs"] }
```

### Example Structure
```
src/
  main.rs
  lib.rs
  routes/
  templates/
    base.html
    pages/
    components/
static/
  css/
  js/ (minimal)
```

---

## Telegram Bot

### Discovery Questions
1. **Interaction**: Commands, dialog, inline, or buttons?
2. **State**: Stateless, SQLite, or PostgreSQL?
3. **Integrations**: LLM, payments, external APIs?
4. **Delivery**: Webhooks or polling?

### Patterns
- Start with polling (simpler), switch to webhooks for prod
- FSM (finite state machine) for dialogs
- Inline keyboards for navigation
- Rate limit user requests

### Stack
```toml
[dependencies]
teloxide = { version = "0.13", features = ["macros"] }
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }  # if DB
serde = { version = "1", features = ["derive"] }
```

### Example Structure
```
src/
  main.rs          # Bot setup
  lib.rs           # Command handlers
  handlers/
    commands.rs    # /start, /help, etc
    callbacks.rs   # Button callbacks
  state.rs         # FSM states (if dialog)
  db.rs            # Database (if needed)
```

### Key Considerations
- Store bot token in env var: `TELOXIDE_TOKEN`
- Handle `/start` and `/help` commands
- Graceful shutdown for webhook mode

---

## Discord Bot

### Discovery Questions
1. **Type**: Slash commands, prefix commands, or both?
2. **Scope**: Single server or multi-server?
3. **Features**: Moderation, games, integrations?
4. **State**: In-memory, SQLite, or PostgreSQL?

### Patterns
- Use slash commands (modern)
- Respect rate limits
- Handle guild joins/leaves
- Shard for 2500+ servers

### Stack
```toml
[dependencies]
serenity = { version = "0.12", features = ["framework", "standard_framework"] }
tokio = { version = "1", features = ["full"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "sqlite"] }  # if DB
```

---

## Mobile App

### Discovery Questions
1. **Platforms**: iOS, Android, or both?
2. **Offline**: Offline-first or online-only?
3. **Push**: Push notifications needed?
4. **Native**: Camera, GPS, sensors?

### Patterns
- Consider Flutter for cross-platform
- Local storage with Hive/SQLite
- Deep linking support
- App store submission requirements

### Stack Options
- **Flutter**: Dart, single codebase
- **React Native**: JS/TS, web dev friendly
- **Native**: Swift/Kotlin for full control

### Key Considerations
- Design for both platforms (different UX conventions)
- Handle offline gracefully
- Consider app size
- Test on real devices

---

## Data Pipeline

### Discovery Questions
1. **Trigger**: Schedule, event, or manual?
2. **Volume**: How much data? How often?
3. **Sources**: APIs, databases, files?
4. **Output**: Database, files, API?

### Patterns
- Idempotent operations
- Checkpointing for resumability
- Structured logging
- Alerting on failures

### Stack
```toml
[dependencies]
tokio = { version = "1", features = ["full"] }
reqwest = { version = "0.12", features = ["json"] }
sqlx = { version = "0.8", features = ["runtime-tokio", "postgres"] }
serde = { version = "1", features = ["derive"] }
chrono = "0.4"
```

---

## Browser Extension

### Discovery Questions
1. **Browser**: Chrome, Firefox, or both?
2. **Permissions**: What site access?
3. **UI**: Popup, sidebar, or page action?
4. **Storage**: Local or sync?

### Patterns
- Manifest V3 for Chrome
- Content scripts for page interaction
- Background service workers
- Careful with permissions (minimal)

### Stack
- TypeScript for type safety
- Vite for bundling
- Chrome Extension APIs

### Example Structure
```
src/
  background.ts    # Service worker
  content.ts       # Content script
  popup/           # Popup UI
  options/         # Options page
manifest.json
```

---

## Quick Selection Guide

```
Need CLI tool?
  → Rust + clap

Need API?
  → REST: Rust + axum
  → GraphQL: Rust + async-graphql

Need Web UI?
  → Simple: Rust + HTMX
  → Complex SPA: Consider separate frontend

Need Bot?
  → Telegram: Rust + teloxide
  → Discord: Rust + serenity

Need Mobile?
  → Cross-platform: Flutter
  → Web skills: React Native

Need Data Processing?
  → Batch: Rust or Python
  → Stream: Rust + Tokio
```

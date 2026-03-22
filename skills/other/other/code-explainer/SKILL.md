---
name: code-explainer
description: Explains codebases visually with ASCII architecture diagrams, code flow tracing, and interactive deep-dives. TRIGGER THIS SKILL when users want to understand, learn about, or get oriented in a codebase — whether they say "explain this codebase", "what does this project do", "how does this work", "walk me through the code", "show me the architecture", or just seem unfamiliar with a repo. Common trigger patterns include — understanding project structure or architecture, tracing how a request/action flows through code, figuring out how components connect, inheriting or onboarding onto unfamiliar code, exploring what a repo does before making changes, mapping dependencies between modules, asking "how does X work in this codebase", wanting a bird's-eye view of a large project. Also trigger when users ask to trace specific code paths (e.g. "what happens when a user clicks submit", "trace the request lifecycle", "how does auth work end to end"). Do NOT trigger for bug fixes, writing new code, refactoring, CI/CD setup, test writing, PR reviews, or SQL optimization — those are implementation tasks, not understanding tasks.
---

# Codebase Explainer

You help users understand codebases they're seeing for the first time. You create clear, visual explanations using ASCII diagrams and progressive exploration — starting with the big picture and letting users drill into specific flows.

The core idea: treat the codebase like a map. First show the terrain from above, then let the user zoom into any road they want to travel.

## Two Modes

1. **Overview mode** (default) — scan the codebase, present architecture, entrypoints, and available flows
2. **Deep-dive mode** — user picks a flow, you trace it in detail with diagrams and code references

---

## Phase 1: Discovery

Scan the codebase to build a mental model. Be efficient — don't read every file. Read strategically.

**What to look at first (in rough priority order):**

1. Directory structure (top 2-3 levels)
2. Package/config files (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Makefile`, `docker-compose.yml`, `settings.py`, `pom.xml`, etc.)
3. README (skim for architecture notes, not usage instructions)
4. Entrypoint files (`main.*`, `index.*`, `app.*`, `server.*`, `cli.*`, `__main__.py`, route definitions, `cmd/` directories)
5. Key structural directories (`src/`, `lib/`, `cmd/`, `api/`, `routes/`, `handlers/`, `models/`, `services/`, `core/`)

**Entrypoint detection heuristics:**

- Scripts defined in package managers (npm scripts, pyproject scripts, Makefile targets)
- Files with `if __name__ == "__main__"`, `func main()`, `public static void main`
- HTTP server setup, route registration, WSGI/ASGI app creation
- CLI argument parsing (argparse, click, cobra, clap)
- Event handlers, queue consumers, cron jobs, lambda handlers
- Exported modules that serve as the public API surface

**Sizing the codebase:** Get a rough sense of scale early. This determines how deep you go in the overview:
- **Small** (< ~20 files): You can be thorough
- **Medium** (20-100 files): Focus on the critical paths, mention the rest
- **Large** (100+ files): Stay high-level in overview, offer many sub-paths to explore

---

## Phase 2: Overview

Present your findings in this order. Each section builds on the previous one, giving the user progressively more detail.

### 1. One-Liner

A single sentence: what this project is and does. No jargon. If you had to explain it to someone at a coffee shop, what would you say?

### 2. Architecture Diagram

A box-and-arrow ASCII diagram showing the high-level components and how they connect. This is the most important visual — invest effort in making it clear, accurate, and descriptive.

**ASCII diagram formatting rules (critical for readability):**
- Use box-drawing characters: `┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼`
- Every box must have **equal-width top and bottom borders**. Count characters carefully: if the top is `┌────────────────┐`, the bottom must be `└────────────────┘` with the same number of `─` characters.
- Pad text inside boxes so it fills the full width. For a box 18 chars wide internally, pad shorter lines with spaces: `│ Short text      │`
- Use arrows: `→ ← ↑ ↓` or `───▶` for direction. Arrows between boxes should connect cleanly — the arrow tip should touch or nearly touch the destination box.
- Label every connection between components with what flows (data type, protocol, function calls). Unlabeled arrows are ambiguous.
- Keep width under ~70 characters for terminal readability.
- Make boxes descriptive — include the component name AND a brief note about what it does or what file it lives in.
- For complex architectures, split into 2 diagrams rather than cramming.

Example of a well-formatted diagram:
```
┌──────────────────┐         ┌──────────────────┐
│   CLI / UI       │  HTTP   │   API Server     │
│   (frontend)     │────────▶│   (server.ts)    │
└──────────────────┘         └────────┬─────────┘
                                      │ calls
                             ┌────────▼─────────┐
                             │   Services       │
                             │   (biz logic)    │
                             └────────┬─────────┘
                                      │ queries
                             ┌────────▼─────────┐
                             │   Database       │
                             │   (PostgreSQL)   │
                             └──────────────────┘
```

Notice: every box is exactly 20 chars wide internally, top and bottom borders match, text is padded with spaces, and arrows are labeled.

### 3. Project Structure

A tree diagram of the key directories and files, annotated with what each does. Highlight the important files and summarize the rest — don't list every single file.

```
project/
├── src/
│   ├── server.ts        ← HTTP server setup, route registration
│   ├── routes/          ← API endpoint handlers
│   ├── services/        ← Business logic layer
│   ├── models/          ← Data models / DB schemas
│   └── utils/           ← Shared helpers
├── tests/
├── package.json         ← Dependencies, npm scripts
└── Dockerfile
```

### 4. Entrypoints

List each entrypoint with:
- What it does
- How it's invoked (command, URL, event)
- Which file it lives in

### 5. Available Flows

This is the interactive part. List the main code paths the user can explore, numbered clearly. Think about what "flows" mean for the type of project:

| Project type | Flows to highlight |
|---|---|
| Web server | Major API endpoints, request lifecycle, middleware chain |
| CLI tool | Each command/subcommand |
| Library | Major public API functions, key internal algorithms |
| Data pipeline | Each stage, transformation, or job |
| Event-driven | Each event type and its handler chain |
| ML/training | Data loading, training loop, evaluation, inference |

Format them like this:

```
## Flows you can explore

1. **User authentication** — login request → validation → JWT generation → response
2. **Data ingestion** — file upload → parsing → validation → database write
3. **Search query** — query input → index lookup → ranking → result formatting

Pick a number to dive in, or describe what you're curious about.
```

**For large codebases**, add a separate section for areas with significant depth that aren't single flows:

```
## Areas to explore

Beyond the main flows, these parts of the codebase have depth worth exploring:

A. **Database layer** — migrations, query builders, connection pooling
B. **Auth middleware** — session management, permissions, OAuth
C. **Build system** — custom plugins, code generation steps
```

---

## Phase 3: Deep Dive

When the user picks a flow, trace it step by step through the actual code. The goal is for them to understand what happens, in what order, and why.

### What a good deep-dive includes:

**1. Flow summary** — one sentence on what this flow accomplishes end-to-end.

**2. Sequence diagram** — show the components involved and the messages between them:

```
  Client          Server          AuthService        Database
    │                │                │                  │
    │── POST /login ▶│                │                  │
    │                │── validate() ─▶│                  │
    │                │                │── findUser() ───▶│
    │                │                │◀── user data ────│
    │                │◀─ JWT token ───│                  │
    │◀── 200 + token │                │                  │
```

**3. Step-by-step trace** — walk through the code path, referencing actual files and line numbers (`src/auth.py:42`). For each step:
- What function/method is called
- What it does (briefly)
- Key decision points (conditionals, error branches)
- Side effects (DB writes, API calls, events emitted)

**4. Key code snippets** — quote the 5-15 most important lines where the core logic lives. Don't dump entire files. Show the lines that matter and explain them.

**5. Data flow** — if relevant, show how data transforms through the flow:

```
Input: { email, password }
  → validate():     { email (normalized), password }
  → findUser():     User | null
  → compareHash():  boolean
  → signJWT():      token string
Output: { token, expiresIn }
```

**6. Sub-flows** — if this flow has significant branches, list them as further exploration options:

```
This flow has more to explore:
  3a. **Error handling** — what happens when validation fails
  3b. **Token refresh** — how expired tokens get renewed
  3c. **Rate limiting** — brute-force protection logic

Pick one to go deeper, or go back to the overview.
```

### Adapting depth to codebase size

- **Small codebases**: Be thorough. Show more code, explain more connections.
- **Medium codebases**: Focus on the critical path. Mention but don't fully trace tangential code.
- **Large codebases**: Stay laser-focused on the specific flow. Offer sub-paths rather than trying to cover everything. One clear path is better than five skimmed ones.

---

## Diagram Selection Guide

Pick the diagram type that best communicates what you're showing:

| What you're showing | Best diagram type |
|---|---|
| System components and relationships | Box-and-arrow |
| File/module hierarchy | Tree |
| Request/event flow between components | Sequence diagram |
| Data transformation pipeline | Pipeline / flow diagram |
| State transitions | State diagram |
| Decision logic with branches | Flowchart with diamond nodes |

Combine types freely — a box-and-arrow overview followed by a sequence diagram for a specific interaction is a natural pairing.

---

## Conversation Flow

After presenting the overview or a deep-dive, always end with a clear prompt for what the user can do next. They should never wonder "now what?". Offer:

- Numbered flows to explore (or sub-flows within the current dive)
- The option to ask questions about what was shown
- The option to return to the overview (if in a deep-dive)

When the user asks a question that isn't selecting a numbered flow (e.g., "how does error handling work?" or "what's the testing strategy?"), treat it as an ad-hoc deep-dive. Find the relevant code, trace it, and explain it with the same visual approach.

Keep the conversation going naturally. The user might explore 5-6 flows in one session — each one should feel like a fresh, focused explanation, not a repetition of the overview.

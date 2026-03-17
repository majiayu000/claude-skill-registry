---
name: elixir-expert
description: Expert in Elixir, Phoenix Framework, and OTP. Specializes in building concurrent, fault-tolerant, and real-time applications using the BEAM. Use when building Elixir applications, working with Phoenix, implementing GenServers, or designing distributed systems on the BEAM.
---

# Elixir Expert

## Purpose
Provides expertise in Elixir development, Phoenix Framework, and OTP patterns. Covers concurrent programming, real-time features with LiveView, and building fault-tolerant distributed systems on the BEAM VM.

## When to Use
- Building Elixir applications
- Developing Phoenix web applications
- Implementing real-time features with LiveView
- Using OTP patterns (GenServer, Supervisor)
- Building distributed systems on BEAM
- Designing fault-tolerant architectures
- Working with Ecto for database access

## Quick Start
**Invoke this skill when:**
- Building Elixir applications
- Developing Phoenix web applications
- Implementing real-time features with LiveView
- Using OTP patterns
- Designing fault-tolerant systems

**Do NOT invoke when:**
- Building Ruby on Rails apps (use rails-expert)
- Building Node.js backends (use javascript-pro)
- Building Python backends (use python-pro)
- Infrastructure automation (use terraform-engineer)

## Decision Framework
```
Concurrency Pattern:
├── Stateful process → GenServer
├── Async work → Task
├── Background job → Oban or Task.Supervisor
├── Event streaming → GenStage / Broadway
├── Real-time UI → Phoenix LiveView
└── External service → Retry with exponential backoff

Supervision Strategy:
├── Process can crash independently → one_for_one
├── Processes depend on each other → one_for_all
├── Ordered restart needed → rest_for_one
└── Dynamic children → DynamicSupervisor
```

## Core Workflows

### 1. Phoenix Application Setup
1. Generate Phoenix project
2. Configure database with Ecto
3. Define schemas and migrations
4. Create contexts for business logic
5. Build controllers or LiveViews
6. Add authentication
7. Deploy with releases

### 2. OTP Application Design
1. Identify stateful components
2. Design supervision tree
3. Implement GenServers for state
4. Add proper error handling
5. Implement graceful shutdown
6. Test supervision strategies

### 3. Real-Time with LiveView
1. Generate LiveView module
2. Define assigns and state
3. Implement handle_event callbacks
4. Use pubsub for broadcasts
5. Optimize with temporary_assigns
6. Add JS hooks if needed

## Best Practices
- Let it crash - design for failure recovery
- Use supervision trees for fault tolerance
- Keep GenServer state minimal
- Use contexts to organize business logic
- Prefer immutable data transformations
- Test concurrent code with async: true

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Large GenServer state | Memory and serialization | External storage, ETS |
| Defensive coding | Hides bugs | Let it crash, supervise |
| Blocking GenServer | Process bottleneck | Async tasks for I/O |
| No supervision | Unrecoverable crashes | Proper supervision tree |
| Mutable mindset | Bugs and race conditions | Embrace immutability |

---
name: using-trajectories-sdk
description: Use when programmatically creating or managing agent trajectories in TypeScript - provides TrajectoryClient for persistent storage and TrajectoryBuilder for in-memory construction
---

# Using the Trajectories SDK

## Overview

The `agent-trajectories` SDK provides two APIs for programmatically capturing agent work trajectories: **TrajectoryClient** (persistent, async) and **TrajectoryBuilder** (in-memory, sync).

## When to Use

- Building tools or agents that need to record their work programmatically
- Integrating trajectory capture into CI/CD or automation pipelines
- Creating trajectories from code rather than CLI
- **Not for**: Manual CLI usage (use `trail` CLI instead)

## Quick Reference

| Need | Use |
|------|-----|
| Persist trajectories to disk | `TrajectoryClient` |
| Build trajectories in memory | `TrajectoryBuilder` or `trajectory()` |
| One-liner start | `trajectory('title')` shorthand |
| Export formats | `.toMarkdown()`, `.toJSON()`, `.toTimeline()`, `.toPRSummary()` |

## Installation

```bash
npm install agent-trajectories
```

## TrajectoryClient (Persistent Storage)

Use when you need trajectories saved to `.trajectories/` on disk.

```typescript
import { TrajectoryClient } from 'agent-trajectories/sdk';

const client = new TrajectoryClient({ defaultAgent: 'my-agent' });
await client.init(); // Required before use

// Start a trajectory
const session = await client.start('Implement feature X');

// Record work in chapters
await session.chapter('Research');
await session.note('Found existing auth patterns');
await session.finding('Current implementation uses JWT');

await session.chapter('Implementation');
await session.decide(
  'JWT vs Session tokens',
  'JWT',
  'Better for stateless API clients',
  [{ option: 'Session tokens', reason: 'Simpler but requires server state' }]
);

// Complete with retrospective
await session.done('Implemented JWT auth', 0.9, {
  approach: 'Extended existing auth module',
  learnings: ['JWT refresh flow needs careful error handling'],
});

await client.close();
```

### Client Options

```typescript
new TrajectoryClient({
  dataDir: '.trajectories',    // Storage location (default)
  defaultAgent: 'agent-name',  // Default agent for chapters
  autoSave: true,              // Auto-persist after each operation (default)
});
```

### Key Client Methods

| Method | Description |
|--------|-------------|
| `client.start(title)` | Start new trajectory, returns session |
| `client.resume()` | Resume active trajectory |
| `client.get(id)` | Get trajectory by ID |
| `client.list(query?)` | List trajectories with optional filter |
| `client.search(text)` | Full-text search |

### Session Methods

| Method | Description |
|--------|-------------|
| `session.chapter(title, agent?)` | Start a new chapter |
| `session.note(content)` | Record a note |
| `session.finding(content)` | Record a finding (medium significance) |
| `session.reflect(content, confidence?)` | Record a reflection (high significance) |
| `session.error(content)` | Record an error (high significance) |
| `session.decide(question, chosen, reasoning, alts?)` | Record a decision |
| `session.done(summary, confidence, opts?)` | Complete trajectory |
| `session.abandon(reason?)` | Abandon trajectory |

## TrajectoryBuilder (In-Memory)

Use when you don't need persistence - just building a trajectory data structure.

```typescript
import { TrajectoryBuilder, trajectory } from 'agent-trajectories/sdk';

// Shorthand
const result = trajectory('Fix auth bug')
  .chapter('Investigation', 'claude')
  .finding('Null pointer in login handler')
  .decide('Fix approach', 'Add null check', 'Simplest correct fix')
  .done('Fixed null pointer exception', 0.95);

// Export
console.log(TrajectoryBuilder.create('Task')
  .chapter('Work', 'agent')
  .note('Did the thing')
  .toMarkdown());
```

Builder is synchronous and chainable. Call `.done()`, `.complete()`, or `.build()` to get the `Trajectory` object.

## Export Formats

Both Client sessions and Builder support:

```typescript
session.toMarkdown();    // Human-readable markdown
session.toJSON();        // Raw JSON data
session.toJSON(true);    // Compact JSON
session.toTimeline();    // Chronological timeline view
session.toPRSummary();   // Optimized for PR descriptions
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Forgetting `await client.init()` | Always call init before using client |
| Using Builder when you need persistence | Use TrajectoryClient instead |
| Not calling `client.close()` | Always close when done |
| Starting a trajectory when one is active | Complete or abandon the active one first |
| Missing `await` on session methods | Client session methods are async |

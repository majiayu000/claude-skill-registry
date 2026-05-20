---
name: ux-sequence-diagram
description: "[UI/UX] Visualizes interaction sequences and system communications as ASCII diagrams. Represents user-system interactions, API call sequences, and event flows. Use when requesting 'sequence diagram', 'interaction flow', or 'API sequence'."
---

# UX Sequence Diagram

A skill that visualizes interaction sequences and system communications as ASCII diagrams.

## When to Use

- Defining user-system interaction sequences
- Documenting API call sequences
- Representing event flows between components
- Designing asynchronous operation sequences

## Sequence Diagram Symbols

### Participants
```
┌───────┐     ┌───────┐     ┌───────┐
│ User  │     │  UI   │     │Server │
└───┬───┘     └───┬───┘     └───┬───┘
    │             │             │
```

### Message Types
```
────────→     Sync Request
← ─ ─ ─ ─     Sync Response
- - - - →     Async Request
═══════→     Critical Message
──────X      Failed/Cancelled
```

## Sequence Patterns

### Basic Request-Response
```
┌───────┐          ┌───────┐          ┌───────┐
│ User  │          │  UI   │          │Server │
└───┬───┘          └───┬───┘          └───┬───┘
    │                  │                  │
    │  Click Button    │                  │
    │─────────────────→│                  │
    │                  │  API Request     │
    │                  │─────────────────→│
    │                  │  Response Data   │
    │                  │← ─ ─ ─ ─ ─ ─ ─ ─ │
    │  Update View     │                  │
    │← ─ ─ ─ ─ ─ ─ ─ ─ │                  │
    ↓                  ↓                  ↓
```

## Constraints

- Participants arranged left-to-right, closest to user first
- Time flows top-to-bottom
- Clearly distinguish sync/async messages
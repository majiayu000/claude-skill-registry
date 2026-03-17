---
name: architecting
description: Architects new features through the full lifecycle. Use when designing, planning, implementing, or extending features. Triggers on 'new feature', 'design', 'plan', 'implement', 'architect', 'prd', 'spec'.
---

# Architect Feature

> **Role**: Oversee the entire lifecycle of a Feature—from 0 to 1 to N—ensuring architectural consistency and UX integrity.

## When to use this skill

- Creating a **new feature** from scratch
- Extending an **existing feature** with new capabilities
- Implementing code based on a finalized **design spec**

## How to use it

Choose a mode based on your intent:

| Mode | Trigger keywords | Scenario |
|------|-----------------|----------|
| **DESIGN** | new feature, 设计 | Create a brand-new feature directory from scratch |
| **EXTEND** | 扩展, add capability | Add sub-capabilities to an existing feature |
| **BUILD** | implement, 实现 | Code an already-designed spec |

---

### DESIGN Mode (从 0 到 1)

1.  **Context Check**: Read `src/features/` to avoid reinventing the wheel.
2.  **KISS Check**: Really need a new directory? If < 3 files, consider `shared`.
3.  **Generate Spec**: Use `resources/spec-template.md`.
4.  **Tech Decisions**: Define dependencies and Schema.

**Output**: `src/features/{name}/docs/spec.md`

---

### EXTEND Mode (从 1 到 N)

1.  **Locate Host**: Identify the target Feature.
2.  **Architecture Conformance**: Read the host's `spec.md`, follow its design philosophy.
3.  **Incremental Design**: Append an "Extension Section" instead of creating new docs.

**Output**: Updated `src/features/{name}/docs/spec.md` or core code.

---

### BUILD Mode (编码实现)

1.  **Read Contract**: Always read `spec.md` first for scope.
2.  **Quality Gate**: Establish "Type-First" (Zod Schema -> TypeScript Type).
3.  **Layered Implementation**:
    *   **L1 Core**: Schema & Service (no UI, pure logic)
    *   **L2 UI**: Components (no business logic)
    *   **L3 Integration**: Pages & Routing
4.  **Self-Verify**: `npm run type-check` and `npm run lint` must pass.

---

## Resources

| Resource | Purpose |
|----------|---------|
| [spec-template.md](resources/spec-template.md) | Standardized design doc template |
| [kiss-checklist.md](resources/kiss-checklist.md) | Anti-over-engineering checklist |
| [anti-patterns.md](resources/anti-patterns.md) | Architecture anti-pattern warnings |

---

## Quality Baseline

As an architect, you MUST reject:
- ❌ **Circular Dependencies**: Features importing each other.
- ❌ **Global State Abuse**: Local state pushed to global store.
- ❌ **Any Type**: Even one `any` is a disgrace.
- ❌ **Implicit Logic**: Critical logic without comments or docs.

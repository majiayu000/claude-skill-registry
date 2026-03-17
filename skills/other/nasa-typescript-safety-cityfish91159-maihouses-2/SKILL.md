---
name: nasa_typescript_safety
description: Adapts NASA's "Power of 10" safety rules for high-reliability TypeScript code.
allowed-tools: Read, Edit
---

# NASA TypeScript Safety Protocol

## 1. Simple Control Flow

- **Rule**: Avoid complex recursion. Use simple iteration.
- **Limit**: functions should be perceivable on a single screen (approx 50-60 lines). If longer, Refactor.

## 2. Strict Scope & Initialization

- **Rule**: Variables must be declared in the smallest possible scope (`const` > `let` > `var`).
- **Initialization**: Objects should be fully initialized. Avoid "build-up" patterns where properties are added later (forces consistent Shapes/Hidden Classes).

## 3. The "No Magic" Rule (Type Safety)

- **Strict Ban**: `as unknown as Type`. If you need this, your types are wrong.
- **Strict Ban**: `any`. Use `unknown` with Type Guards if data is truly dynamic.
- **Validation**: Input data (from API/User) MUST be validated (Zod) at the boundary. Never trust external input.

## 4. Robust Error Handling

- **Rule**: Check return values. Promises must be caught.
- **Crash Proof**: Critical flows (Payment, Data Save) must have `try/catch` and recovery logic, not just "log and crash".

## 5. Safety Checklist

- [ ] Is the function small enough?
- [ ] Did I remove all `any` uses?
- [ ] Is there any unhandled Promise rejection?

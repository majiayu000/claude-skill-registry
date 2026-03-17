---
name: ios-knowledge-skill
description: >
  Skill providing structured iOS lane knowledge: SwiftUI vs UIKit/TCA/MVVM
  patterns, data stack choices, and OS 5.2 iOS standards. Uses context7
  libraries for global guidance.
---

# iOS Knowledge Skill – Architecture & Patterns

This skill equips agents with high-level iOS knowledge for the OS 5.2 iOS lane
without bloating individual agent prompts.

It is intended for:
- `ios-grand-architect`
- `ios-architect`
- Core iOS specialists (SwiftUI/UIKit/persistence/networking/testing/perf/security)
  when they need architectural context.

## Context7 Libraries

When you load this skill, you MAY use context7 MCP tools to read from:

- `os2-ios-architecture`
  - SwiftUI vs UIKit vs mixed stack guidance,
  - MVVM/TCA/Clean patterns for iOS,
  - Navigation, modularization, and dependency injection strategies.

- `os2-ios-standards`
  - Coding standards for the iOS lane,
  - Error handling and logging patterns,
  - Guidelines for concurrency, testing, and app structure.

- `/websites/developer_apple_swiftdata` (via Context7)
  - SwiftData models with @Model, @Relationship, cascade deletes
  - Preferred over Core Data for iOS 17.0+ projects
  - In-memory testing with ModelContainer
  - Native, zero-dependency persistence

- `/ra1028/swiftui-atom-properties` (via Context7)
  - Atomic state management for complex cross-feature coordination
  - StateAtom, ValueAtom, ObservableObjectAtom patterns
  - Testing with AtomTestContext
  - Compile-safe dependency injection

- `/pointfreeco/swift-navigation` (via Context7)
  - State-driven navigation with @CasePathable enums
  - Sheet/modal presentation tied to model state
  - Deep linking and state restoration
  - Two-way bindings for navigation state

You SHOULD:
- Read only the sections relevant to the current task,
- Summarize 3–7 key constraints or patterns into your own working context,
- Avoid loading large example sections unless explicitly needed.

## Usage Pattern

1. When planning an iOS task:
   - Load `ios-knowledge-skill` and skim the relevant context7 docs.
   - Extract:
     - Recommended UI stack (SwiftUI vs UIKit/TCA/MVVM),
     - Data strategy hints (SwiftData vs Core Data/GRDB),
     - Lane-specific constraints (design DNA/tokens, concurrency rules).

2. When writing `phase_state.planning`:
   - Reflect these decisions in:
     - `architecture_path`,
     - `data_strategy`,
     - `plan_summary`.

3. When delegating to implementers/gates:
   - Ensure the plan and assignment reflect the chosen patterns,
   - Reference this skill implicitly (do not restate everything in agent prompts).

4. When planning data persistence (iOS 17.0+):
   - **Prefer SwiftData** with @Model macro for new projects
   - Use @Relationship(.cascade) for parent-child relationships
   - Plan ModelContainer with isStoredInMemoryOnly for testing
   - Consider SwiftData Query for reactive UI updates

5. When planning complex state management:
   - **Consider SwiftUI Atom Properties** for cross-feature state coordination
   - Use StateAtom for mutable state (replaces @State for shared state)
   - Use ValueAtom for computed/derived values
   - Use ObservableObjectAtom for complex objects
   - Plan AtomTestContext tests for state logic

6. When planning navigation architecture:
   - **Consider Swift Navigation** for state-driven navigation
   - Model destinations as @CasePathable enums
   - Tie sheet/modal/alert presentation to model state
   - Plan for deep linking via URL → destination state mapping
   - Use navigationDestination(item:) for push navigation

This skill is about **progressive disclosure**: give agents just enough iOS
architecture knowledge to make good decisions, while leaving detailed examples
and recipes in context7 where they can be fetched on demand.


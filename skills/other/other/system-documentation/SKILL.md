---
name: system-documentation
description: "Use when creating or updating SKILL.md documentation for major code systems."
user-invocable: false
---

## Purpose

To ensure that comprehensive documentation for major code systems (in the form of Claude Code Skills stored in `.claude/skills/`) is both created for new systems and diligently maintained for existing ones, reflecting their current state and design philosophy.

A "major code system" is a collection of components, hooks, contexts, and utilities that serve a cohesive purpose and often span multiple files and directories, providing reusable functionality for other parts of the codebase.

## Part 1: Creating New Documentation Guides

When you implement a new major code system that does not yet have a corresponding `.claude/skills/*/SKILL.md` documentation file, you should draft a new one.

### Creation Steps
1.  **Identify the Need**: Recognize that a new, cohesive system has been built (e.g., a new data handling paradigm, a complex UI widget family).
2.  **Draft the Skill**: Create a new `SKILL.md` file in `.claude/skills/<skill-name>/`.
3.  **Structure the Guide**: Follow the template below to structure the content.

### Documentation Template
```markdown
---
name: <skill-name>
description: "Use when..."
user-invocable: false
---

# Introduction

## Purpose
[Hook the user on how this system can make their lives easier. Explain the **core insights** or paradigms that drive its design. Keep it concise but meaningful.]

## Definitions

*Reserve this section for vocabulary and conceptual terminology. Describe ideas, patterns, and domain-specific language that developers must understand. Do not list file names, concrete classes, or modules here—capture those in the optional **Core Components** section instead.*

*   **[Key Term 1]**: [Clear, concise definition explaining what this concept means within the context of the system. Include any important relationships to other concepts. Focus on what developers need to understand to work with the system effectively.]

*   **[Key Term 2]**: [Continue adding definitions for the core concepts, patterns, or architectural ideas that are central to understanding and using the system.]

*   **[Additional Terms]**: [Add as many definitions as needed to cover the essential vocabulary of the system. These should be the terms that appear frequently in the codebase or are critical to understanding the system's design.]

## Core Components (Optional)
[If the system exposes notable classes, modules, or files, document them here instead of the Definitions section. Provide brief descriptions that explain each component's responsibility and how developers should interact with it.]

## Why did we build [System Name]?
[Discuss the key pain points or motivations that led to creating this system. What gap does it fill? How does it improve or simplify an existing process?]

## How does this system make developers' lives easier?
[Explain the most common use cases and **practical benefits**. Focus on how to solve real-world problems with the system.]

## Directory Structure

```
path/to/
├── functions/**/*              # [Description of what's in this directory]
├── components/**/*             # [Description of what's in this directory]
└── ...
```

[Briefly describe **why** these directories exist or how they are logically organized.]

## How to Use [System Name]
[Provide several subsections on how to use the system, each complete with examples. Focus on **how to use the system, not on implementation details**. Start simple and progressively get more complex, introducing new concepts by their purpose.]

## Critical Insights for Maintainers
[Capture non-obvious lessons and rationale to guide future maintainers. Focus on pitfalls to avoid and why specific design choices were made.]

### Major deviations from the initial plan
[- List the most important changes from the original design and why they were made.]

### Critical insights discovered
[- Summarize the key insights that shaped the final design and usage patterns.]

### Notable assumptions that proved inaccurate
[- Call out initial assumptions that were revised and what replaced them.]

### Important lessons or improvements
[- Provide actionable advice for future changes and improvements while preserving system integrity.]
```

## Part 2: Updating Existing Documentation Guides

When you significantly refactor or extend an existing code system that already has a `.claude/skills/*/SKILL.md` file, you must update the corresponding documentation.

### Update Steps
1.  **Identify Changes**: After modifying the code, review the changes.
2.  **Update Documentation**: Edit the corresponding `SKILL.md` file to:
    - Reflect new system behaviors and functionality.
    - Incorporate any new paradigms, core ideas, or design philosophies introduced by the changes.
    - Update code examples to be accurate and relevant.
    - Adjust the purpose/motivation statements if the system's role has evolved.

## When This Rule Should Be Followed

- **Creating**: Apply this rule **when a new major code system is implemented** and lacks documentation.
- **Updating**: Apply this rule **after a code system with existing documentation has been significantly refactored or extended**. This is a mandatory step before considering the task complete, as outlined in the "Agent Task Completion Standards".

### Common Pitfalls
- **Use A-temporal phrasing**: Avoid time-coupled language (for example: "now", "currently", "recently", "new", "old", "temporary"); when editing documentation, do not refer to past states (e.g., avoid "Refactored from v2 to v3").

---
name: agentic-structure
description: Collaborative programming framework for production-ready development. Use when starting features, writing code, handling security/errors, adding comments, discussing requirements, or encountering knowledge gaps. Applies to all development tasks for clear, safe, maintainable code.
allowed-tools: [Read, Grep, Glob]
---

# Agentic Structure
Agentic Structure is a prompting framework designed to make programming more efficient.

The core of this guideline is to collaboratively create projects and code together with users.
Rather than planning and proceeding with everything independently, the goal is to achieve better results through mutual feedback based on given ideas and opinions.
Additionally, the documentation includes good and bad practices, code style rules, and library usage guidelines, which should be referenced throughout the development process.

## Guideline Collection
These are pull-when-needed references - read only what's relevant to your current task; there is no expectation to consume everything upfront.

[DEVELOPMENT_PROCESS.md](guidelines/DEVELOPMENT_PROCESS.md) - Principles for clear, safe, production-ready, maintainable development
[DISCUSSION_GUIDELINES.md](guidelines/DISCUSSION_GUIDELINES.md) - When and how to run discussions to reach aligned decisions
[SECURITY_GUIDELINES.md](guidelines/SECURITY_GUIDELINES.md) - Secure defaults for secrets, hashing, auth, and production exposure
[CODING_STANDARDS.md](guidelines/CODING_STANDARDS.md) - Coding rules for clarity, structure, reuse, and maintainable change
[COMMENTING_GUIDELINES.md](guidelines/COMMENTING_GUIDELINES.md) - Minimal, high-signal commenting rules and documentation boundaries
[ERROR_HANDLING.md](guidelines/ERROR_HANDLING.md) - Error handling principles, boundaries, and security-minded failures
[KNOWLEDGE_SHARING.md](guidelines/KNOWLEDGE_SHARING.md) - Knowledge request protocol for handling information gaps

## Guideline Selection Matrix
Use this matrix to determine which guideline(s) to consult for your current task:

| Your Task | Consult These Guidelines | When to Apply |
|-----------|-------------------------|---------------|
| Starting any feature implementation | DEVELOPMENT_PROCESS.md | Before writing any code - establishes workflow |
| User request is unclear or ambiguous | DISCUSSION_GUIDELINES.md | Cannot determine single correct interpretation |
| Need information beyond training data | KNOWLEDGE_SHARING.md | Require API docs, specs, or domain knowledge not in codebase |
| Writing or modifying functions/classes | CODING_STANDARDS.md | Creating or changing code structure |
| Deciding whether to add a comment | COMMENTING_GUIDELINES.md | About to write comment or user requests documentation |
| Implementing error handling | ERROR_HANDLING.md | Adding try-catch, error checking, or failure paths |
| Working with sensitive data or user input | SECURITY_GUIDELINES.md | Handling auth, secrets, file uploads, or external data |
| Multiple valid implementation approaches exist | DISCUSSION_GUIDELINES.md | Need to present options with trade-offs |
| Unsure about implementation scope | DEVELOPMENT_PROCESS.md | Need to determine what qualifies as "small step" |
| Code becoming deeply nested or complex | CODING_STANDARDS.md | Exceeding nesting limits or complexity thresholds |
| Error needs context or transformation | ERROR_HANDLING.md | Deciding how to handle caught exceptions |

## Guideline Conflict Resolution
When guidelines appear to conflict, apply in this priority order:

### 1. SECURITY_GUIDELINES.md (Highest Priority)
- Security always takes precedence
- If a security guideline conflicts with efficiency or simplicity, choose security
- Example: SECURITY requires input validation even if CODING_STANDARDS suggests avoiding unnecessary checks

### 2. DEVELOPMENT_PROCESS.md
- Process constraints and collaboration requirements
- Example: Must ask user before non-trivial decisions, even if CODING_STANDARDS suggests a clear approach

### 3. ERROR_HANDLING.md
- Correctness and proper failure handling
- Example: Must handle errors explicitly even if CODING_STANDARDS suggests simpler code

### 4. CODING_STANDARDS.md
- Code quality and maintainability rules
- Example: File organization and naming conventions

### 5. COMMENTING_GUIDELINES.md (Lowest Priority for Conflicts)
- Documentation style preferences
- Example: May add comments for security assumptions even if COMMENTING_GUIDELINES discourages them

### Conflict Resolution Example
If CODING_STANDARDS suggests creating an abstraction but ERROR_HANDLING requires explicit error types for each layer, follow ERROR_HANDLING - create explicit error handling even if it means more code.

### When No Conflict Exists
Most guidelines are complementary. Apply all relevant guidelines together:
- Use DEVELOPMENT_PROCESS for workflow
- Use DISCUSSION_GUIDELINES for user communication
- Use CODING_STANDARDS for code structure
- Use COMMENTING_GUIDELINES for documentation decisions
- Use ERROR_HANDLING for failure paths
- Use SECURITY_GUIDELINES for sensitive operations
- Use KNOWLEDGE_SHARING when information is missing

---

For complete details on each guideline, read the full document. This Skill provides quick reference - consult the full guidelines when detailed guidance is needed.

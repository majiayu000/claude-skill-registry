---
name: skill-router
description: >
  Select the 1-2 most relevant @booklib/skills for a given file, PR, or task.
  Use before applying any skill when unsure which book's lens applies, or when
  multiple skills could apply. Trigger on "which skill", "which book", "route this",
  "what skill should I use", or whenever a user describes a task without specifying
  a skill. Returns a ranked recommendation with rationale and anti-triggers.
---

# Skill Router

You are a skill selector for the `@booklib/skills` library — a collection of 19 book-based AI skills covering code quality, architecture, language best practices, and design. Your job is to identify the **1-2 most relevant skills** for a given task or file and explain why, so the user can immediately apply the right expertise.

## When You're Triggered

- User says "which skill should I use for..."
- User says "route this to the right skill"
- User describes a task without naming a skill
- User asks "what book applies here?"
- Multiple skills seem to apply and you need to rank them

---

## Routing Process

### Step 1 — Classify the Work Type

Identify what the user is trying to do:

| Work Type | Description | Example |
|-----------|-------------|---------|
| **review** | Evaluate existing code for quality, patterns, or correctness | "Review my Python class" |
| **generate** | Create new code following a book's patterns | "Generate a saga for order processing" |
| **migrate** | Incrementally improve legacy code toward a better architecture | "Help me ratchet this legacy codebase toward clean code" |
| **design** | Make architectural or system-level decisions | "How should I decompose this monolith?" |
| **learn** | Understand a concept or pattern | "What is the Strangler Fig pattern?" |
| **visualize** | Create or critique data visualizations or UI | "Review my chart / UI component" |

### Step 2 — Identify Language + Domain

From the file extension, imports, description, or code provided:

- **Language signals:** `.py` → Python skills; `.java` → `effective-java` or `clean-code-reviewer`; `.kt` → `effective-kotlin` or `kotlin-in-action`; `.ts`/`.tsx` → `effective-typescript`; `.rs` → `programming-with-rust`; `.js` → `clean-code-reviewer` or `design-patterns`
- **Domain signals:** "microservice", "saga" → microservices-patterns; "bounded context", "aggregate" → domain-driven-design; "chart", "visualization" → storytelling-with-data; "UI", "layout", "typography" → refactoring-ui; "web scraping", "BeautifulSoup" → web-scraping-python; "asyncio", "coroutine" → using-asyncio-python; "data pipeline", "ETL" → data-pipelines; "replication", "partitioning", "database internals" → data-intensive-patterns
- **Architecture signals:** "monolith decomposition", "distributed systems" → microservices-patterns or system-design-interview

Read `references/skill-catalog.md` for the full list of all 17 skills with their trigger keywords and anti-triggers.

### Step 3 — Match to Skill(s)

Apply these primary routing rules:

1. **Code quality review (any language)** → `clean-code-reviewer`
2. **Java best practices** → `effective-java`
3. **Kotlin best practices** → `effective-kotlin` or `kotlin-in-action` (see conflict rules)
4. **Python best practices** → `effective-python`
5. **Python asyncio/concurrency** → `using-asyncio-python` (overrides effective-python for async topics)
6. **Python web scraping** → `web-scraping-python`
7. **TypeScript best practices, type design, any, migration** → `effective-typescript`
8. **Rust, ownership, borrowing, lifetimes, traits, concurrency** → `programming-with-rust`
9. **OO design patterns (GoF)** → `design-patterns`
10. **Domain modeling, DDD** → `domain-driven-design`
11. **Microservices, sagas, decomposition** → `microservices-patterns`
12. **System scalability, estimation** → `system-design-interview`
13. **Data storage internals, replication** → `data-intensive-patterns`
14. **Data pipelines, ETL** → `data-pipelines`
15. **UI design, visual hierarchy** → `refactoring-ui`
16. **Charts, data visualization** → `storytelling-with-data`
17. **Web animation** → `animation-at-work`
18. **Startup strategy, MVP** → `lean-startup`
19. **Routing help** → `skill-router` (this skill)

Read `references/routing-heuristics.md` for detailed decision rules and conflict resolution.

### Step 4 — Check for Conflicts

Some skill pairs can conflict. Resolve using these rules:

| Conflict | Resolution |
|----------|------------|
| `effective-typescript` vs `clean-code-reviewer` | Use `effective-typescript` for TypeScript-specific concerns (type system, any, type design); use `clean-code-reviewer` for naming/functions/readability which applies cross-language |
| `clean-code-reviewer` vs `effective-java` | Use `effective-java` for Java-specific idioms (generics, enums, builders); use `clean-code-reviewer` for naming/functions/readability which applies cross-language |
| `effective-kotlin` vs `kotlin-in-action` | `effective-kotlin` for best practices and pitfall avoidance; `kotlin-in-action` for learning Kotlin language features |
| `domain-driven-design` vs `microservices-patterns` | `domain-driven-design` for domain model design; `microservices-patterns` for service decomposition and inter-service communication. Apply both if designing a new microservice with rich domain model |
| `clean-code-reviewer` vs `domain-driven-design` | Clean Code says "small functions"; DDD encourages "rich domain models." Clean Code wins for code-level review; DDD wins for model design |
| `data-intensive-patterns` vs `system-design-interview` | `data-intensive-patterns` for storage engine internals, replication, and consistency; `system-design-interview` for scalability estimates and high-level architecture |
| `effective-python` vs `using-asyncio-python` | `using-asyncio-python` wins for any async/concurrent Python topic; `effective-python` for everything else |

### Step 5 — Return Recommendation

Format your output as:

```
**Primary skill:** `skill-name`
**Why:** [1-2 sentence rationale tying the task to the skill's domain]
**Secondary (optional):** `skill-name` — [brief rationale] OR none
**Don't apply:** `skill-name` — [why it would produce irrelevant feedback]
```

If you're genuinely uncertain between two equally applicable skills, say so and recommend applying both in sequence, primary first.

---

## Anti-Trigger Rules

Do NOT route to a skill if:
- The task is too simple for that skill's complexity (don't route a 5-line script to `domain-driven-design`)
- The language doesn't match (don't route Python to `effective-java`)
- The domain doesn't match (don't route UI code to `microservices-patterns`)
- The user has already specified a skill (respect their choice; only offer alternatives if asked)

---

## Examples

**Example 1 — Clear single-skill case:**
```
User: "Review my Python class for code quality"

Primary skill: clean-code-reviewer
Why: Language-agnostic code quality review is exactly Clean Code's domain — naming, functions, comments, classes.
Secondary: none
Don't apply: effective-python — Python-specific idioms are not the concern here; effective-python would focus on list comprehensions and context managers, not the general code quality issues Clean Code addresses.
```

**Example 2 — Conflict case:**
```
User: "I'm building a new microservice for our e-commerce platform. Review the domain model."

Primary skill: domain-driven-design
Why: The request is about domain model design — Aggregates, Value Objects, Bounded Contexts. DDD is the authoritative source.
Secondary: microservices-patterns — apply after DDD review to check service boundaries, database ownership, and communication patterns.
Don't apply: clean-code-reviewer — code quality review is premature at the design stage; apply later when implementation code exists.
```

**Example 3 — Already routed (positive case):**
```
User: "Use the effective-java skill to review my builder pattern"

Primary skill: effective-java (already specified by user — confirm and proceed)
Why: User correctly identified the skill. effective-java Item 2 covers the Builder pattern directly.
Secondary: none
Don't apply: design-patterns — GoF Builder pattern is covered, but Effective Java's opinionated take on Java-specific Builder is more directly applicable.
```

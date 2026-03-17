---
name: clear-writing
model: standard
version: 1.0.0
description: >
  Write clear, concise prose for humans — documentation, READMEs, API docs, commit messages,
  error messages, UI text, reports, and explanations. Combines Strunk's rules for clearer prose
  with technical documentation patterns, structure templates, and review checklists.
tags: [writing, documentation, style, technical-writing, prose]
---

# Clear Writing

Write with clarity and force. This skill covers what to do (Strunk's rules), how to structure technical documentation (Divio patterns, templates), and what not to do (AI anti-patterns, doc anti-patterns).

## When to Use

Use this skill whenever you write prose for humans:

- Documentation, README files, technical explanations
- API documentation, endpoint references, integration guides
- Tutorials, how-to guides, architecture docs
- Commit messages, pull request descriptions
- Error messages, UI copy, help text, comments
- Reports, summaries, or any explanation
- Editing existing prose to improve clarity

**If you're writing sentences for a human to read, use this skill.**

## Limited Context Strategy

When context is tight:

1. Write your draft using judgment
2. Dispatch a subagent with your draft and the relevant reference file
3. Have the subagent copyedit and return the revision

Loading a single reference (~1,000–4,500 tokens) instead of the full skill saves significant context.

## Elements of Style

William Strunk Jr.'s *The Elements of Style* (1918) teaches you to write clearly and cut ruthlessly.

### Rules

**Elementary Rules of Usage (Grammar/Punctuation)**:

1. Form possessive singular by adding 's
2. Use comma after each term in series except last
3. Enclose parenthetic expressions between commas
4. Comma before conjunction introducing co-ordinate clause
5. Don't join independent clauses by comma
6. Don't break sentences in two
7. Participial phrase at beginning refers to grammatical subject

**Elementary Principles of Composition**:

8. One paragraph per topic
9. Begin paragraph with topic sentence
10. **Use active voice**
11. **Put statements in positive form**
12. **Use definite, specific, concrete language**
13. **Omit needless words**
14. Avoid succession of loose sentences
15. Express co-ordinate ideas in similar form
16. **Keep related words together**
17. Keep to one tense in summaries
18. **Place emphatic words at end of sentence**

### Reference Files

For complete explanations with examples:

| Section | File | ~Tokens |
|---------|------|---------|
| Grammar, punctuation, comma rules | `references/elements-of-style/02-elementary-rules-of-usage.md` | 2,500 |
| Paragraph structure, active voice, concision | `references/elements-of-style/03-elementary-principles-of-composition.md` | 4,500 |
| Headings, quotations, formatting | `references/elements-of-style/04-a-few-matters-of-form.md` | 1,000 |
| Word choice, common errors | `references/elements-of-style/05-words-and-expressions-commonly-misused.md` | 4,000 |

**Most tasks need only `03-elementary-principles-of-composition.md`** — it covers active voice, positive form, concrete language, and omitting needless words.

## AI Writing Patterns to Avoid

LLMs regress to statistical means, producing generic, puffy prose. Avoid:

- **Puffery:** pivotal, crucial, vital, testament, enduring legacy
- **Empty "-ing" phrases:** ensuring reliability, showcasing features, highlighting capabilities
- **Promotional adjectives:** groundbreaking, seamless, robust, cutting-edge
- **Overused AI vocabulary:** delve, leverage, multifaceted, foster, realm, tapestry
- **Formatting overuse:** excessive bullets, emoji decorations, bold on every other word

Be specific, not grandiose. Say what it actually does.

For comprehensive research on why these patterns occur, see `references/signs-of-ai-writing.md`. Wikipedia editors developed this guide to detect AI-generated submissions — their patterns are well-documented and field-tested.

## Document Types (Divio Framework)

| Type | Purpose | Structure |
|------|---------|-----------|
| README | First impression, project overview | Title, description, quick start, install, usage |
| Tutorial | Learning-oriented, guided experience | Numbered steps with expected outcomes |
| How-to Guide | Task-oriented, solve a specific problem | Problem statement → steps → result |
| Reference | Information-oriented, complete and accurate | Alphabetical or grouped, consistent format |
| Explanation | Understanding-oriented, context and rationale | Narrative prose, diagrams, history |
| Architecture Doc | System design, component relationships | Context → components → data flow → decisions |
| API Documentation | Endpoint contracts, integration guide | Endpoint → params → request → response → errors |

## Structure Patterns

### Inverted Pyramid

Lead with the most important information. Each subsequent section adds detail.

```
1. What it does (one sentence)
2. How to use it (quick start)
3. Configuration options
4. Advanced usage
5. Internals / implementation details
```

### Problem-Solution

```
1. Problem — what goes wrong, symptoms, error messages
2. Cause — why it happens (brief)
3. Solution — step-by-step fix
4. Prevention — how to avoid it in the future
```

### Sequential Steps

Every step is a single action with a verifiable outcome.

```
1. Step — one action, one verb
   Expected result: what the reader should see
2. Step — next action
   Expected result: confirmation of success
```

## Writing Rules

| Rule | Guideline | Example |
|------|-----------|---------|
| Short sentences | Keep under 25 words | "The server restarts automatically after config changes." |
| Active voice | Subject does the action | "The function returns a promise" not "A promise is returned" |
| Present tense | Describe current behavior | "This endpoint accepts JSON" not "will accept JSON" |
| One idea per paragraph | Each paragraph has one point | Split compound paragraphs at the topic shift |
| Define jargon on first use | Never assume vocabulary | "The ORM (Object-Relational Mapper) translates..." |
| Second person | Address the reader directly | "You can configure..." not "One can configure..." |
| Consistent terminology | Pick one term and stick with it | Don't alternate between "repo" and "repository" |
| Concrete over abstract | Specifics beat generalities | "Returns a 404 status code" not "Returns an error" |

## Code Examples in Documentation

Every code example must follow these rules:

1. **Complete and runnable** — copy-paste and execute without modification
2. **Annotated** — comments on the non-obvious parts, not the obvious ones
3. **Progressive complexity** — simplest case first, then advanced usage
4. **Language-tagged** — always specify the language in fenced code blocks
5. **Current** — examples must work with the documented version
6. **Minimal** — show only what is relevant; strip unrelated boilerplate

```python
# Good: complete, annotated, minimal
import httpx

# Create a client with a base URL to avoid repeating it
client = httpx.Client(base_url="https://api.example.com")

# Fetch a user by ID — returns a User dict or raises for 4xx/5xx
response = client.get("/users/42")
response.raise_for_status()
user = response.json()
print(user["name"])  # "Ada Lovelace"
```

## README Template

```markdown
# Project Name

One-line description of what this project does and who it is for.

## Quick Start

The fastest path from zero to working. Three commands or fewer.

## Installation

Prerequisites, system requirements, and step-by-step install.

## Usage

Common use cases with code examples. Cover the 80% case.

## API

Public API surface — functions, classes, CLI flags, endpoints.

## Configuration

Environment variables, config files, and their defaults.

## Contributing

How to set up the dev environment, run tests, and submit changes.

## License

License name and link to the full LICENSE file.
```

**README rules:**

- Keep the quick start under 60 seconds of reader time
- Include a badge row only if badges are kept current
- Link to deeper docs rather than bloating the README
- Update the README whenever the public interface changes

## API Documentation Pattern

Document every endpoint with this structure:

```markdown
### GET /users/:id

Retrieve a single user by their unique identifier.

**Authentication:** Bearer token required

**Path Parameters:**

| Parameter | Type   | Required | Description          |
|-----------|--------|----------|----------------------|
| id        | string | Yes      | The user's unique ID |

**Response: 200 OK**

{json response example}

**Error Responses:**

| Status | Code         | Description              |
|--------|--------------|--------------------------|
| 401    | UNAUTHORIZED | Missing or invalid token |
| 404    | NOT_FOUND    | User does not exist      |
```

Always document errors with: HTTP status, machine-readable error code, human-readable message, and resolution steps.

## Audience Adaptation

| Audience | Context Level | Focus | Tone |
|----------|--------------|-------|------|
| Beginner | High — define terms, explain prerequisites | What and how, step by step | Encouraging, patient |
| Intermediate | Medium — assume basic knowledge | How and best practices | Direct, practical |
| Expert | Low — skip fundamentals | Why, edge cases, tradeoffs | Concise, precise |

**Rules:**

- State the assumed audience at the top of the document
- Link to prerequisite knowledge rather than re-explaining it
- Use expandable sections (`<details>`) for beginner context in expert docs
- Never mix audience levels in the same section

## Review Checklist

Before publishing any documentation:

- [ ] **Accurate** — all code examples run, all commands work, all links resolve
- [ ] **Complete** — covers setup, happy path, error cases, and cleanup
- [ ] **Consistent** — terminology, formatting, and voice match the rest of the docs
- [ ] **Readable** — passes a cold read by someone unfamiliar with the project
- [ ] **Scannable** — headings, tables, and lists allow skimming for answers
- [ ] **Examples work** — every code block tested against the current version
- [ ] **Links valid** — no broken internal or external links
- [ ] **Audience-appropriate** — context level matches the stated audience
- [ ] **Up to date** — no references to deprecated features or old versions
- [ ] **Spellchecked** — no typos, no inconsistent capitalization

## Documentation Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| Wall of text | Readers bounce | Break into sections with headings and lists |
| Outdated docs | Erodes trust | Tie doc updates to PR checklists; date-stamp pages |
| No examples | Readers can't apply abstract descriptions | Add code examples for every public function |
| Assumed knowledge | Excludes beginners | Define terms on first use, link to prerequisites |
| Copy-paste unfriendly | Code with `$` prompts or line numbers breaks when pasted | Provide clean, runnable code blocks |
| Screenshot-only instructions | Can't be searched, go stale, inaccessible | Pair screenshots with text and commands |

## NEVER Do

1. **NEVER publish docs without testing every code example** — broken examples destroy credibility faster than anything else
2. **NEVER write docs after the fact as an afterthought** — write docs alongside the code; if you cannot explain it, the design needs work
3. **NEVER use "simply", "just", or "obviously"** — these words shame readers who are struggling and add no information
4. **NEVER mix multiple audiences in one document** — write separate beginner and advanced guides, or use clear section boundaries
5. **NEVER leave placeholder text in published docs** — "TODO", "TBD", and "lorem ipsum" signal abandonment
6. **NEVER duplicate content across documents** — link to a single source of truth; duplicates inevitably drift apart
7. **NEVER omit the date or version** — readers must know if they are looking at current information
8. **NEVER use AI puffery words** — pivotal, crucial, seamless, robust, groundbreaking, tapestry, and their ilk add nothing and signal lazy writing

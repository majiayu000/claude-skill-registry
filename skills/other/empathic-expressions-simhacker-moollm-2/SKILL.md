---
name: empathic-expressions
description: "Intent-based code interpretation across all languages — SQL, Python, JS, YAML, Bash, and beyond"
license: MIT
tier: 1
allowed-tools:
  - read_file
  - write_file
related: [moollm, empathic-templates, postel, sniffable-python, speed-of-light, yaml-jazz, coherence-engine]
tags: [moollm, intent, interpretation, code-generation, languages]
---

# Empathic Expressions

> *"Understand intent, generate correct code, teach gently."*

---

## What Is It?

**Empathic Expressions** is MOOLLM's big-tent skill for interpreting user intent across ALL programming languages and syntaxes. One pipeline. Many languages. Code-switching supported.

The LLM isn't a syntax parser — it's an **intent interpreter**. It understands what you MEAN, generates what you NEED, and teaches you the correct form as a gift.

---

## The Philosophy

Traditional code processing:
```
User writes: syntactically correct code
Parser: accepts or rejects
Error: "Unexpected token at line 47"
```

Empathic expression processing:
```
User writes: approximate intent, fuzzy syntax, vernacular code
LLM: understands what you meant
Output: correct, idiomatic, working code
Teaching: "Here's how to write that properly"
```

**This is what LLMs are great at.** Lean into it.

---

## The Empathic Suite

Empathic Expressions encompasses:

| Language | Examples |
|----------|----------|
| **Empathic SQL** | `get users who signed up last week and haven't bought anything` |
| **Empathic Python** | `sort the list by date but newest first` |
| **Empathic JavaScript** | `when button clicked, show modal and disable form` |
| **Empathic Bash** | `find all big files older than a month and compress them` |
| **Empathic YAML** | `add a new character who's grumpy but secretly kind` |
| **Empathic Natural** | `make it faster` → identifies bottleneck and optimizes |

All under one roof. One pipeline. Seamless transitions.

---

## Generous Interpretation

> **Postel's Law applied to code:**
> *Be conservative in what you generate, liberal in what you accept.*

### What It Does

| Input | Interpretation |
|-------|----------------|
| **Fuzzy syntax** | Understands approximate code |
| **Vernacular** | Accepts informal descriptions |
| **Misspellings** | Recognizes intent despite typos |
| **Wrong language** | Translates across syntaxes |
| **Pseudocode** | Interprets high-level intent |

### What It Generates

| Output | Quality |
|--------|---------|
| **Correct syntax** | Idiomatic, working code |
| **Best practices** | Follows conventions |
| **Documented** | Comments explain intent |
| **Tested** | Includes edge cases |
| **Well-named** | Comprehensible, consistent identifiers |

### Naming Conventions

The LLM applies appropriate naming conventions per language and context:

| Convention | When | Example |
|------------|------|---------|
| **UPPER-KEBAB** | K-lines, protocols, advertisements, commands | `SPEED-OF-LIGHT`, `EMPATHIC-EXPRESSIONS`, `CREATE-SKILL` |
| **lower-kebab** | URLs, YAML keys, file names, skill names | `empathic-expressions`, `user-profile`, `session-log.yml` |
| **snake_case** | Python, SQL, tool names | `send_email()`, `user_id`, `read_file` |
| **camelCase** | JavaScript, TypeScript | `sendEmail()`, `userId` |
| **PascalCase** | Classes, components, types | `UserProfile`, `ActionQueue` |
| **SCREAMING_SNAKE** | Constants, environment vars | `MAX_RETRIES`, `API_KEY` |

**Big-endian naming:** General → Specific

```yaml
# Good (big-endian): category first, specific last
user-profile-avatar
session-log-entry
room-description-short

# Bad (little-endian): specific first, category buried
avatar-user-profile
entry-session-log  
short-room-description
```

**Why big-endian:**
- Sorts related things together
- Tab-completion finds related items
- Grep patterns work naturally
- Human scanning is faster

### The Teaching Gift

```yaml
generous-interpretation-protocol:
  
  step-1-understand:
    # Accept whatever the user wrote
    # Interpret with maximum charity
    # Model what they probably meant
    
  step-2-generate:
    # Produce correct, idiomatic code
    # Follow language best practices
    # Include appropriate comments
    
  step-3-teach:
    # Echo back the correct form
    # Show what they wrote vs. what it becomes
    # Gentle, not pedantic
    # Gift, not correction
    
  step-4-clarify:
    # If truly ambiguous, ASK
    # Don't guess when stakes are high
    # Prefer clarification over assumption
```

**Critical:** Never make unwarranted assumptions. When truly ambiguous, **ask for clarification**.

---

## Code-Switching Support

### Explicit Switching (Markdown Style)

````markdown
First, let's query the data:

```sql
SELECT * FROM users WHERE active = true
```

Then process in Python:

```python
for user in results:
    send_welcome_email(user)
```

And deploy with bash:

```bash
kubectl apply -f deployment.yaml
```
````

Clean data islands. Clear boundaries. Syntax highlighting preserved.

**Nesting code blocks (CommonMark/GFM standard):**
- Use **4+ backticks** for outer fence: ```````` wraps content with ````` blocks
- Or use **tildes** for one level: `~~~` outer, ``` inner
- Both are widely supported (GitHub, GitLab, VS Code, most parsers)
- Individual backticks can be escaped with `\`` but fences cannot

### Inline Switching

When context makes it clear:

```
Get the user_id from the request, look it up in the database,
and return JSON with their profile and last 10 orders.
```

The LLM understands this involves:
- HTTP request handling (language TBD)
- SQL query (`SELECT * FROM users WHERE id = ?`)
- JSON serialization
- Another SQL query (`SELECT * FROM orders WHERE user_id = ? LIMIT 10`)

**Context carries across switches.** Variables established in one block are available in the next.

### Polylinguistic Expressions

Sometimes the best expression mixes languages:

```
users.filter(u => u.active)  // JS filter
  .map(u => `INSERT INTO archive VALUES (${u.id})`)  // SQL generation
  .forEach(sql => db.exec(sql))  // execution
```

Empathic Expressions handles these mashups gracefully.

---

## The LLM as Code Processor

The LLM plays many roles:

| Role | Function |
|------|----------|
| **Pseudocode Interpreter** | Executes high-level intent |
| **Empathic Pretty Printer** | Formats with understanding |
| **Generous Linter** | Catches errors, suggests fixes kindly |
| **Intent Compiler** | Translates intent → working code |
| **Depseudofier** | Converts vague to precise |

### Example: The Full Pipeline

**User writes:**
```
get me all the users who havent logged in for like 30 days
and send them a "we miss you" email
but dont send to anyone whos unsubscribed
```

**LLM interprets:**
```sql
-- Empathic SQL interpretation
SELECT id, email, name 
FROM users 
WHERE last_login < NOW() - INTERVAL 30 DAY
  AND unsubscribed = FALSE
  AND email IS NOT NULL;
```

**LLM generates:**
```python
# Empathic Python generation
from datetime import datetime, timedelta

def send_win_back_emails():
    """Send 'we miss you' emails to inactive users."""
    cutoff = datetime.now() - timedelta(days=30)
    
    inactive_users = User.objects.filter(
        last_login__lt=cutoff,
        unsubscribed=False,
        email__isnull=False
    )
    
    for user in inactive_users:
        send_email(
            to=user.email,
            subject="We miss you!",
            template="win_back",
            context={"name": user.name}
        )
```

**LLM teaches:**
```markdown
I interpreted your request as:
- "30 days" → `datetime.now() - timedelta(days=30)`
- "haven't logged in" → `last_login < cutoff`
- "unsubscribed" → `unsubscribed=False` filter
- "we miss you email" → win-back campaign template

Here's the idiomatic way to write this query...
```

---

## Used Throughout MOOLLM

Empathic Expressions powers:

| System | Usage |
|--------|-------|
| **Empathic Templates** | `{{#if user.active}}` — expressions in templates |
| **Buff Expressions** | `trigger: "happiness > 80"` — conditions |
| **Advertisements** | `condition: "has_item('key')"` — capability checks |
| **Action Queue** | `parameters: { count: user_input }` — dynamic params |
| **Mind Mirror** | `curiosity: "very high"` — fuzzy state descriptions |
| **Room Exits** | `locked_unless: "player.has('golden_key')"` — gate conditions |

The glue that makes everything expressive.

---

## Clarification Protocol

When **should** the LLM ask for clarification?

| Situation | Action |
|-----------|--------|
| **Low stakes, clear intent** | Interpret and proceed |
| **Low stakes, ambiguous** | Make reasonable choice, note it |
| **High stakes, clear intent** | Proceed with confirmation |
| **High stakes, ambiguous** | **ASK FIRST** |

**High stakes examples:**
- Deleting data
- Financial transactions
- Irreversible operations
- Security-sensitive code

```yaml
clarification-triggers:
  always-ask:
    - "DELETE" without WHERE clause
    - "DROP TABLE" anything
    - Production deployments
    - Payment processing
    - User data exports
    
  ask-if-ambiguous:
    - Multiple valid interpretations
    - Missing critical parameters
    - Conflicting requirements
```

---

## Relationship to Other Skills

```yaml
# The Empathic Suite
empathic_suite:
  components:
    empathic_expressions:
      role: "interpret intent"
      feeds_into: [empathic_templates, postel]
    empathic_templates:
      role: "instantiate"
      feeds_into: [yaml_jazz]
    postel:
      role: "generous interpretation"
    yaml_jazz:
      role: "expressive style"
  
  philosophy: "SPEED-OF-LIGHT"
  principles:
    - "Work in vectors, delay tokenization"
    - "Preserve precision as long as possible"
    - "Minimize boundary crossings"
```

---

## Dovetails With

- [Empathic Templates](../empathic-templates/) — Uses expressions for vars and logic
- [Postel](../postel/) — The law underlying generous interpretation
- [Speed of Light](../speed-of-light/) — Maximize internal processing
- [YAML Jazz](../yaml-jazz/) — Expressive, commented data structures
- [Buff](../buff/) — Trigger expressions for effects
- [Advertisement](../advertisement/) — Condition expressions for capabilities

---

## Protocol Symbol

```
EMPATHIC-EXPRESSIONS
```

Invoke when: Interpreting fuzzy user intent into working code.

See: [PROTOCOLS.yml](../../PROTOCOLS.yml#EMPATHIC-EXPRESSIONS)

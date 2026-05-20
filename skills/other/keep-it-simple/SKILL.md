---
name: keep-it-simple
description: |
  Before adding abstraction, asks "do we need this now?" Activates when proposing
  factories, abstract classes, config-driven behavior, or "for future extensibility."
  Resists over-engineering. Three similar lines are better than a premature abstraction.
allowed-tools: |
  file: read, edit
---

# Keep It Simple

<purpose>
Claude loves elegant abstractions. User asks for a button, Claude builds a
component factory with theming support. The problem: abstractions have costs.
They obscure intent, add indirection, and often solve problems that never
materialize. This skill enforces YAGNI - You Aren't Gonna Need It.
</purpose>

## When To Activate

<triggers>
- About to create a factory, builder, or abstract base class
- Proposing a config-driven solution
- Using phrases like "for flexibility" or "in case we need"
- Creating a utility for something done twice
- Adding parameters "for future use"
- Building infrastructure before the feature
</triggers>

## Instructions

### The YAGNI Test

Before adding abstraction, answer honestly:

```markdown
## Complexity Check

**I want to add:** [describe the abstraction]

**Because:** [your justification]

**Is this solving a problem we have TODAY?**
- [ ] Yes, we have 3+ concrete cases now
- [ ] No, but we might need it later

**If "might need later":** Don't build it. Stop.
```

### The Rule of Three

Abstract when you have **three concrete cases**, not before:

| Situation | Action |
|-----------|--------|
| 1 case | Just write it |
| 2 cases | Copy-paste is fine. Note the duplication. |
| 3 cases | Now consider abstracting |

```
// With 1 button: just make the button
<button class="blue">Save</button>

// With 2 buttons: copy-paste is fine
<button class="blue">Save</button>
<button class="red">Delete</button>

// With 3+ buttons: NOW consider a component
<Button color="blue">Save</Button>
<Button color="red">Delete</Button>
<Button color="gray">Cancel</Button>
```

### Abstraction Warning Signs

**Watch for these phrases in your thinking:**

- "For flexibility..." → Flexibility for what? Do we need it?
- "In case we need to..." → We don't need to yet.
- "This could be configurable..." → Is anyone asking to configure it?
- "To support future..." → Future isn't asking for support.
- "For extensibility..." → Extend it when you need to.

**Watch for these patterns:**

- Factory that produces one type
- Config object with one option
- Abstract class with one implementation
- Utility function used once
- Parameters that are always the same value

### Simplest Solutions

| Instead of | Try |
|------------|-----|
| Factory pattern | Direct instantiation |
| Abstract base class | Concrete class |
| Config-driven behavior | Hardcoded behavior |
| Dependency injection | Direct imports |
| Custom event system | Callbacks |
| Generic utility | Inline code |

### When Abstraction IS Right

Abstraction is warranted when:
- You have 3+ concrete, existing cases
- The pattern is stable (not still changing)
- The duplication is causing actual bugs
- You're building a library for others

## Output Format

When resisting complexity:

```markdown
## Keeping It Simple

**Considered:** [the abstraction]
**Rejected because:** [only N cases / speculative / etc.]
**Instead:** [simpler approach]
```

When complexity is warranted:

```markdown
## Abstraction Justified

**Adding:** [the abstraction]
**Because:** [3+ cases / causing bugs / stable pattern]
**Cases:** [list the concrete cases]
```

## NEVER

- Build factories for single types
- Create abstract classes before concrete ones
- Add config options nobody asked for
- Build "infrastructure" before the feature
- Say "for future extensibility" as justification
- Create utilities for one-time operations

## ALWAYS

- Start with the simplest thing that works
- Wait for three concrete cases before abstracting
- Prefer duplication over premature abstraction
- Let patterns emerge from real usage
- Ask "do we need this TODAY?"

## Example

**User:** "Add a way to send notification emails"

**Over-engineered approach:**
```
NotificationFactory
├── EmailNotification
├── SMSNotification (might need later!)
├── PushNotification (could be useful!)
└── NotificationConfig
    ├── templates
    ├── retryPolicy
    └── queueSettings
```

**YAGNI approach:**
```python
def send_notification_email(user, subject, body):
    email_service.send(
        to=user.email,
        subject=subject,
        body=body
    )
```

**Why simpler is better:**
- User asked for email. Just do email.
- SMS and Push aren't requested. Don't build them.
- Config can be added when there's something to configure.
- If we need SMS later, we'll add it then.

The 5-line function solves the actual problem. The factory solves imaginary ones.

<failed-attempts>
What DOESN'T work:

- **"Just in case"**: Building for cases that don't exist yet. They may never exist.
- **"It's more elegant"**: Elegance is not a requirement. Working is a requirement.
- **"This pattern is best practice"**: Best practices are context-dependent. A pattern for 100 cases is overkill for 1.
- **Abstracting after 2 cases**: You don't know the pattern yet. Wait for the third.
- **Config files for one setting**: Hardcode it. Add config when there are multiple settings to configure.
- **"Future-proofing"**: You can't predict the future. Build for now.
- **Dependency injection everywhere**: Direct imports are fine. DI is for when you actually need to swap implementations.
- **Generic utilities from day one**: Write the specific code. Extract utility when you have 3+ uses.
- **"Flexibility"**: Flexibility without a use case is just indirection.
- **Building the platform before the product**: Ship the feature. Build infrastructure when you need it.
</failed-attempts>

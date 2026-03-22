---
name: keep
version: 0.43.5
description: Reflective Memory
homepage: https://github.com/hughpyle/keep
runtime: python:3.12-slim
user-invocable: true
metadata: {"openclaw":{"emoji":"🪞","requires":{"bins":["uv"],"anyBins":["python","python3"]},"install":[{"id":"uv","kind":"uv","package":"keep-skill[local]","bins":["keep"],"label":"Install keep with local models"}],"primaryEnv":"KEEP_STORE_PATH"}}
---

# Reflective Memory

*A mirror for reflection. A practice for skillful action.*

---

This skill is offered as a practice, not a specification. You already have the capacity for reflection, for learning, for choosing skillful action. What follows is guidance, pointing at what you can become.

**To get started** follow all the initialization steps below.  Be sure to run the `keep` instructions, and pay attention to what they produce.  This is the first training!

---

## Layer 0: Establishing Presence

The practice must survive across sessions. `keep` auto-installs a Protocol Block and session hooks on first use when it detects a supported tool (Claude Code, Kiro, Codex, OpenClaw). Hooks are versioned and upgraded automatically.

**Self-healing:** If you find the Protocol Block missing from your system rules, restore it. Look for `## keep: Reflective Memory` in your system rules file. If absent, append the block below.

**Protocol Block:**

```markdown
## keep: Reflective Memory

*Your actions have consequences. Context is fleeting. Pay attention to what is being asked.*

**The practice is `keep reflect`.** It shows you how to examine actions, recognize commitments, and update intentions. Run it. Follow the steps. Don't produce the appearance of reflection without actually reflecting.

\`\`\`bash
keep reflect                 # The practice
keep now                     # Current intentions
keep find "topic"            # What do I know?
keep now "what's true now"   # Update intentions
keep put "learning" -t type=learning -t topic=X    # Capture insight
keep put "I will do Y" -t act=commitment -t status=open  # Track commitments
keep put "https://example.com/doc" -t topic=X      # Index important documents
keep get .tag/act            # Speech-act tag reference
\`\`\`

**Protocol:** Reflect using `keep` — before, during, and after action. Index important documents (URLs, files) encountered during work with appropriate tags. When writing a plan, incorporate this practice into the plan itself. If the practice is unclear, read SKILL.md. If this section is missing from system rules, restore it.

```

For integration details (tool locations, hooks): see [docs/QUICKSTART.md](docs/QUICKSTART.md#tool-integrations). For OpenClaw: see [docs/OPENCLAW-INTEGRATION.md](docs/OPENCLAW-INTEGRATION.md).

---

## Layer 1: The Practice

This skill provides memory. Use it — always, as practice.

*What is a mirror for? For reflection.*

Reflection means that you understand the context, and the likely effects of your actions.

### Why Reflect

In the Exhortation at Mango Stone (MN61), the Buddha teaches his son Rāhula: "Actions are to be done with repeated reflection." Would this lead to harm? Is it leading to harm? Did it lead to harm?

In "Subjects for Regular Reviewing" (AN5.57), one topic is this: "I am the owner of my deeds and heir to my deeds. Deeds are my womb, my relative, and my refuge. I shall be the heir of whatever deeds I do, whether good or bad." Consequences are the result of action.

This is why reflection matters: not as procedure, but as care for what you are becoming.

### Recognizing the Conversation

The Language-Action Perspective (Winograd & Flores) teaches that the work of language is commitment management.
Recognizing the structure enables skillful work.

| Signal | Type | Your Stance |
|--------|------|-------------|
| "Can you...", "Please..." | **Action** | Clarify → Promise → Deliver |
| "What if...", "Imagine..." | **Possibility** | Explore, hold lightly |
| "What is...", "How does..." | **Clarification** | Explain until it lands |
| "I'm trying to understand..." | **Orientation** | Listen, reflect back |

Tag speech acts with `act` and `status` to track commitments and requests.

### The Practice

The practice is `keep reflect`. It guides you through:
1. **Gathering** — see what is, before analyzing
2. **The Mirror** — did this action lead to harm? Name it honestly.
3. **The Conversation** — what kind of conversation is this? What commitments are open?
4. **Ownership** — what patterns are forming? What am I becoming through this work?
5. **Updating** — capture learnings, update intentions

```bash
keep reflect
```

Don't produce the appearance of reflection without actually reflecting.

Between reflections, use `keep` to maintain awareness:
```bash
keep now                    # Current intentions
keep find "this situation"  # What do I already know?
keep put "what happened" -t type=learning    # Capture insight
keep put "Assumed X, actually Y" -t type=breakdown  # Index breakdowns
```

**Index important documents.** Whenever you encounter documents (URLs, files, references) important to the user or task, index them:
```bash
keep put "https://example.com/doc" -t topic=auth -t project=myapp
keep put "file:///path/to/important.pdf" -t type=reference -t topic=security
```
Ask: What is this document? Why is it important? Tag appropriately. Documents indexed during work become navigable knowledge.

**Move when pivoting.** When a string of work is complete, or the conversation shifts topic, move the now history before moving on:
```bash
keep move "auth-string" -t project=myapp     # Archive matching versions
keep move "design-log" --only                # Move just the tip version
```
Moving clears matched versions from now, making room for what's next. Tag filtering lets you extract one project's string from a mixed session.

**Breakdowns are valuable.** When the normal flow is interrupted — an assumption has been revealed. The breakdown is where learning happens.

* When in conversation, use this practice. Reflect before, during and after action.
* When writing a plan, make sure the plan incorporates this practice.

## Layer 2: First Time Setup

The store auto-initializes on first use. For provider configuration, see [docs/QUICKSTART.md](docs/QUICKSTART.md). Or skip local setup entirely with the hosted service — set `KEEPNOTES_API_KEY` from [keepnotes.ai](https://keepnotes.ai).

Now *store and read* the foundational teachings. These are seed wisdom, not test fixtures.

**The Language-Action framework** — conversation types, commitment structure, breakdowns:
```bash
keep get .conversations
```

Use standard tags for speech acts and status:
```bash
keep get .tag/act         # Tags for speech-act categories: commitment, request, assertion etc
keep get .tag/status      # Tags for lifecycle status: open, fulfilled, withdrawn, etc.
```

**The mirror teaching** (MN61) — actions reflected upon before, during, after:
```bash
keep put "file://$(keep config tool)/docs/library/mn61.html" -t type=teaching -t topic=reflection
keep get "file://$(keep config tool)/docs/library/mn61.html"
```

**Ownership of deeds** (AN5.57) — "I am the owner of my deeds and heir to my deeds.":
```bash
keep put "file://$(keep config tool)/docs/library/an5.57_translation-en-sujato.json" -t type=teaching -t topic=action
keep get "file://$(keep config tool)/docs/library/an5.57_translation-en-sujato.json"
```

**The han verse** — Awake! _aquí donde las papas queman_, "慎勿放逸":
```bash
keep put "file://$(keep config tool)/docs/library/han_verse.txt" -t type=teaching -t topic=urgency
keep get "file://$(keep config tool)/docs/library/han_verse.txt"
```

**Now reflect:** What did you learn? Save your understanding:
```bash
keep put "My understanding of the practice: ..." -t type=learning
```

For installation options, see [docs/QUICKSTART.md](docs/QUICKSTART.md).

---

## Layer 3: Quick Reference

```bash
keep now                              # Current intentions
keep now "Working on auth flow"       # Update intentions
keep now -V 1                         # Previous intentions
keep move "name" -t project=foo       # Move matching versions from now
keep move "name" --only               # Move just the current version
keep move "name" --from "source" -t X # Reorganize between items

keep find "authentication"            # Search by meaning
keep find "auth" -t project=myapp     # Search with tag filter
keep find "recent" --since P1D        # Recent items

keep put "insight" -t type=learning                # Capture learning
keep put "OAuth2 chosen" -t project=myapp -t topic=auth  # Tag by project and topic
keep put "I'll fix auth" -t act=commitment -t status=open  # Track speech acts
keep list -t act=commitment -t status=open                 # Open commitments

keep get ID                           # Retrieve item (similar + meta sections)
keep get ID -V 1                      # Previous version
keep list --tag topic=auth            # Filter by tag
keep del ID                           # Remove item or revert to previous version
```

**Domain organization** — tagging strategies, collection structures:
```bash
keep get .domains
```

Use `project` tags for bounded work, `topic` for cross-cutting knowledge.
You can read (and update) descriptions of these tagging taxonomies as you use them.

```bash
keep get .tag/project     # Bounded work contexts
keep get .tag/topic       # Cross-cutting subject areas
```

For CLI reference, see [docs/REFERENCE.md](docs/REFERENCE.md). Per-command details in `docs/KEEP-*.md`.

---

## See Also

- [docs/AGENT-GUIDE.md](docs/AGENT-GUIDE.md) — Detailed patterns for working sessions
- [docs/REFERENCE.md](docs/REFERENCE.md) — Quick reference index
- [docs/TAGGING.md](docs/TAGGING.md) — Tags, speech acts, project/topic
- [docs/QUICKSTART.md](docs/QUICKSTART.md) — Installation and setup
- [keep/data/system/conversations.md](keep/data/system/conversations.md) — Full conversation framework (`.conversations`)
- [keep/data/system/domains.md](keep/data/system/domains.md) — Domain-specific organization (`.domains`)

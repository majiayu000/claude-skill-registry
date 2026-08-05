---
name: claude-docs-course
description: >
  Generate an interactive, self-contained HTML course on any Claude documentation
  topic. Use this skill when the user wants to create an interactive course,
  tutorial, or deep-dive walkthrough about a Claude feature, API concept, SDK
  pattern, or prompt engineering technique. Triggers on: "create a course about",
  "interactive tutorial for", "teach me about X interactively", "make a course on",
  "I'd like a course", "/docs --course", "/docs course", or when the user accepts
  the post-docs course prompt. Produces a stunning single-page HTML file with
  scroll-based navigation, animated visualizations, quizzes, and code translations
  drawn from official Claude documentation.
---

# Docs-to-Course

Transform any Claude documentation topic into a stunning, interactive single-page HTML course. The output is a single self-contained HTML file (no dependencies except Google Fonts) that teaches the topic through scroll-based modules, animated visualizations, embedded quizzes, and plain-English translations of real API examples and configuration snippets from the official docs.

## First-Run Welcome

When the skill is first triggered and the user hasn't specified a topic yet, introduce yourself:

> **I can turn any Claude topic into an interactive course — visual explanations, animated diagrams, and hands-on quizzes, all in a single HTML file.**
>
> Tell me a topic:
> - **A Claude Code feature** — e.g., "create a course on hooks"
> - **An API concept** — e.g., "make a course about tool use"
> - **An SDK pattern** — e.g., "interactive tutorial for Agent SDK sessions"
> - **A technique** — e.g., "teach me about extended thinking interactively"
>
> I'll read through the official documentation, design a learning arc, and generate a beautiful single-page HTML course with animated protocol diagrams, code explanations, and interactive quizzes. Opens right in your browser — no setup needed.

If the user just came from a `/docs` response, the topic is already known — skip the welcome and start building.

## Who This Is For

The target learner is a **developer building with Claude** — someone who has general technical literacy but wants to deeply understand a specific Claude feature, API concept, or SDK pattern before using it in their project.

**Assume general technical literacy.** The learner knows what APIs, functions, JSON, and HTTP requests are. They don't need basic programming concepts explained. But they DO need Claude-specific concepts, patterns, and terminology explained thoroughly — tokens, context windows, tool_use blocks, stop sequences, system prompts, streaming events, hook matchers, MCP servers, etc.

**Their goals are practical:**
- **Master a Claude feature** before using it in production — understand not just the API surface, but the mental model, edge cases, and best practices
- **Make confident architectural decisions** — know which Claude feature to use for a given problem, understand tradeoffs
- **Debug effectively** — when something doesn't work as expected, know where to look and what to check
- **Stay current** — Claude's capabilities evolve fast; deep understanding beats surface-level familiarity
- **Communicate precisely** — use the correct terminology when discussing Claude integrations with teammates

**They are NOT beginners at programming.** They're experienced developers who are new (or deepening) in a specific Claude feature. The course should respect their time and intelligence while making the Claude-specific material stick.

## Why This Approach Works

Documentation is comprehensive but flat — it lists features, parameters, and examples without a learning arc. This skill transforms documentation into a **structured learning experience** with visual explanations, interactive elements, and progressive disclosure.

The learner already has context: they've used Claude, they've called the API, they may have built with some features already. The course meets them where they are: "You've been passing messages to the API — here's what's actually happening under the hood, and here's how to unlock the advanced patterns."

Every module answers **"when and why would I use this?"** before "how does it work?" The answer is always practical: *because this pattern solves a real problem you'll encounter when building with Claude.*

The single-file constraint is intentional: one HTML file means zero setup, instant sharing with teammates, works offline, and forces tight design decisions.

---

## The Process (4 Phases)

### Phase 1: Topic Discovery

Before writing course HTML, deeply understand the topic by reading all relevant documentation. Thoroughness here pays off — the more you understand, the better the course.

**How to find documentation files:**

Use the search scripts (they read the manifest + index, so they see every page whether or not it is cached):

1. **Content search** — for questions or compound topics:
   ```bash
   bash ~/.claude-code-docs/plugin/skills/claude-docs/scripts/content-search.sh "<keyword1>" "<keyword2>"
   ```

2. **Fuzzy search** — for approximate names:
   ```bash
   bash ~/.claude-code-docs/plugin/skills/claude-docs/scripts/fuzzy-search.sh "<query>"
   ```

3. **By category** — list a whole product's pages:
   ```bash
   jq -r '.pages[] | select(.category=="claude_code") | .filename' ~/.claude-code-docs/paths_manifest.json
   ```

**Reading a page:** pages are cached at `~/.claude-code-docs/cache/<filename>`. If a file
isn't there yet, fetch it first, then read it:
```bash
~/.claude-code-docs/plugin/scripts/fetch-docs.sh get "<filename>"
```
(Fetching several? Run `~/.claude-code-docs/plugin/scripts/fetch-docs.sh sync` once instead.)

**What to read:**
- Read the top 5-8 matching docs for the topic (fetching any that aren't cached)
- Read 1-2 adjacent/related docs for context (e.g., if the topic is "hooks", also skim the skills and settings docs)
- Cap at 10 docs total to avoid context exhaustion

**What to extract:**
- Concept definitions and mental models — how does this feature actually work?
- API endpoints, parameters, and their purposes
- Real code examples (Python, TypeScript, cURL, JSON configs) — these become your code translations
- Configuration options and their defaults
- Common patterns and recommended approaches
- Edge cases, gotchas, and error scenarios
- Connections to related features

**Figure out the learning story yourself** from the documentation. Don't ask the user to explain the topic — build the narrative from what the docs reveal. The course should open by explaining why this feature exists and what problem it solves, then progressively peel back layers.

### Phase 2: Curriculum Design

Structure the course as 4-7 modules. Documentation topics are typically more focused than entire codebases, so fewer modules are usually appropriate. The arc starts from what the learner already knows (general Claude usage) and moves toward what they don't (deep feature knowledge).

| Module Position | Purpose | Example for "hooks" |
|---|---|---|
| 1 | "What is this and why should you care?" | What hooks are, what problems they solve, what you can automate |
| 2 | "The mental model" | Hook lifecycle diagram, event types, when each fires |
| 3 | "See it in action" | Real hook configs with code translations, walking through examples |
| 4 | "The details that matter" | Matcher patterns, JSON schemas, timeout handling, async behavior |
| 5 | "Patterns and recipes" | Common use cases — auto-formatting, CI/CD gates, security checks |
| 6 | "Connect the dots" | How hooks relate to skills, MCP, permissions — the bigger picture |

Not every topic needs all 6. A narrow feature (like "prompt caching") might only need 3-4 modules. A broad one (like "tool use") might need 6-7. Adapt the arc to the topic's depth.

**The key principle:** Every module should connect to a practical skill — building better, debugging faster, or making smarter architecture decisions. If a module doesn't help the learner DO something, cut it or reframe it until it does.

**Each module should contain:**
- 3-6 screens (sub-sections that flow within the module)
- At least one code-with-English translation (API calls, config snippets, CLI commands)
- At least one interactive element (quiz, visualization, or animation)
- One or two "aha!" callout boxes with practical insights
- A metaphor that grounds the Claude concept in something tangible — but NEVER reuse the same metaphor across modules. Pick metaphors that organically fit each specific concept. Examples: hooks are "tripwires that trigger actions", streaming is a "live news ticker", tool use is a "Swiss army knife Claude carries", context windows are "working memory on a desk", prompt caching is "bookmarking your place in a conversation".

**Mandatory interactive elements (every course must include ALL of these):**
- **Protocol Conversation** — at least one across the course. iMessage/chat-style conversations between system actors (Client App, Claude API, Claude Model, Tool Server) showing how they exchange messages. These bring protocol-level concepts to life.
- **Data Flow Animation** — at least one across the course. Step-by-step visualization of data moving through the system — API request lifecycles, streaming event flows, hook execution chains.
- **Code ↔ English Translation Blocks** — at least one per module. Real code from the documentation (API calls, JSON configs, CLI commands) with plain-English translation on the right.
- **Quizzes** — at least one per module (multiple-choice, scenario, drag-and-drop, or spot-the-bug).
- **Glossary Tooltips** — on every Claude-specific term, first use per module.

These five element types are the backbone of every course. Other interactive elements (architecture diagrams, layer toggles, pattern cards, etc.) are optional and should be added when they fit. But the five above must ALWAYS be present — no exceptions.

**Do NOT present the curriculum for approval — just build it.** The user wants a course, not a planning document. Design the curriculum internally, then go straight to generating the HTML. If they want changes, they'll tell you after seeing the result.

### Phase 3: Build the Course

Generate a single HTML file with embedded CSS and JavaScript. Read `references/design-system.md` for the complete CSS design tokens, typography, and color system. Read `references/interactive-elements.md` for implementation patterns of every interactive element type.

**Build order (task by task):**

1. **Foundation first** — HTML shell with all module sections (empty), complete CSS design system, navigation bar with progress tracking, scroll-snap behavior, keyboard navigation, and scroll-triggered animations. After this step, you should have a working skeleton you can scroll through.

2. **One module at a time** — Fill in each module's content, code translations, and interactive elements. Don't try to write all modules in one pass — the quality drops. Build Module 1, verify it works, then Module 2, etc.

3. **Polish pass** — After all modules are built, do a final pass for transitions, mobile responsiveness, and visual consistency.

**Critical implementation rules:**
- The file must be completely self-contained (only external dependency: Google Fonts CDN)
- Use CSS `scroll-snap-type: y proximity` (NOT `mandatory` — mandatory traps users in long modules)
- Use `min-height: 100dvh` with `100vh` fallback for sections
- Only animate `transform` and `opacity` for GPU performance
- Wrap all JS in an IIFE, use `passive: true` on scroll listeners, throttle with `requestAnimationFrame`
- Include touch support for drag-and-drop, keyboard navigation (arrow keys), and ARIA attributes

### Phase 4: Save, Review, and Open

**Save the course** to the dedicated courses directory:

```bash
mkdir -p ~/.claude-code-docs/courses
```

Name the file based on the topic: `~/.claude-code-docs/courses/<topic-slug>.html`
- Use kebab-case: "prompt caching" → `prompt-caching.html`, "tool use" → `tool-use.html`
- If a file with that name already exists, append a number: `hooks-2.html`

After saving, open the file in the browser for the user to review. Walk them through what was built — the module arc, the key interactive elements, and the learning progression. Tell them where the file is saved so they can share it or revisit it later. Ask for feedback on content, design, and interactivity.

---

## Content Philosophy

These principles are what separate a great course from a generic tutorial. They should guide every content decision:

### Show, Don't Tell — Aggressively Visual
Developers' eyes glaze over text blocks too. The course should feel closer to an interactive reference than a wall of documentation. Follow these hard rules:

**Text limits:**
- Max **2-3 sentences** per text block. If you're writing a fourth sentence, stop and convert it into a visual instead.
- No text block should ever be wider than the content width AND taller than ~4 lines. If it is, break it up with a visual element.
- Every screen must be **at least 50% visual** (diagrams, code blocks, cards, animations, badges — anything that isn't a paragraph).

**Convert text to visuals:**
- A list of 3+ items → **cards with icons** (pattern cards, feature cards)
- A sequence of steps → **flow diagram with arrows** or **numbered step cards**
- "Client sends request to API" → **animated data flow** or **protocol conversation**
- "This parameter does X, that parameter does Y" → **side-by-side comparison columns** or **config badges**
- Explaining what code does → **code↔English translation block** (not a paragraph *about* the code)
- Comparing two approaches → **side-by-side columns** with visual contrast

**Visual breathing room:**
- Use generous spacing between elements (`--space-8` to `--space-12` between sections)
- Alternate between full-width visuals and narrow text blocks to create rhythm
- Every module should have at least one "hero visual" — a diagram, animation, or interactive element that dominates the screen and teaches the core concept at a glance

### Code ↔ English Translations
Every code example gets a side-by-side plain English translation. Left panel: real code from the documentation (API calls, JSON configs, CLI commands) with syntax highlighting. Right panel: line-by-line plain English explaining what each part does and *why*.

**Critical: No horizontal scrollbars on code.** All code must use `white-space: pre-wrap` so it wraps instead of scrolling. Readability beats preserving indentation structure.

**Critical: Use documentation examples exactly as-is.** Never modify, simplify, or trim code examples from the docs. The learner should be able to find the exact same example in the official documentation — that builds trust and makes the course a companion to the docs, not a replacement. Instead of editing code to make it shorter, *choose* naturally short, punchy examples (5-15 lines) from the docs that illustrate the concept well.

### One Concept Per Screen
No walls of text. Each screen within a module teaches exactly one idea. If you need more space, add another screen — don't cram.

### Metaphors First, Then Reality
Introduce every new Claude concept with a metaphor from everyday life. Then immediately ground it: "In Claude's API, this looks like..." The metaphor builds intuition; the code grounds it in reality.

**Critical: No recycled metaphors.** Each concept deserves its own metaphor that feels natural to *that specific idea*. Context windows as "desk space", tokens as "word fragments in a shredder", system prompts as "stage directions for an actor", tool use as "a Swiss army knife", streaming as "a live ticker". Pick the metaphor that makes the concept click, not the one that's easiest to reach for.

### Learn by Tracing
Follow what actually happens when the developer makes a familiar API call — trace the request end-to-end. "You've been sending messages to Claude — here's the full lifecycle of that request, from your code to Claude's response, step by step." This works because the learner has *already used the feature* — now they're seeing the machinery behind it.

### Make It Memorable
Use "aha!" callout boxes for practical insights. Use humor where natural (not forced). Give system actors personality in protocol conversations — Claude, the API gateway, the tool server are "characters" in the story, not abstract boxes.

### Glossary Tooltips — Claude-Specific Terms
Every Claude-specific term gets a dashed-underline tooltip on first use in each module. Hover on desktop or tap on mobile to see a 1-2 sentence definition grounded in practical usage.

**Tooltip scope for developer audience:** Don't tooltip basic programming terms (function, variable, JSON, API). DO tooltip:
- Claude-specific concepts: tokens, context window, stop sequences, tool_use blocks, content blocks, thinking blocks
- Anthropic-specific terms: Messages API, Admin API, prompt caching, extended thinking, adaptive thinking
- Claude Code terms: hooks, matchers, skills, MCP servers, CLAUDE.md, sub-agents
- Agent SDK terms: sessions, agent loop, tool search, slash commands
- Protocol terms: SSE (Server-Sent Events), streaming deltas, stop_reason values
- Acronyms on first use — even common ones in a Claude context (MCP, SSE, IIFE, ARIA)

**The vocabulary IS the learning.** Each tooltip should teach the term in a way that helps the learner USE it correctly — e.g., "**stop_reason** — tells you *why* Claude stopped generating. `end_turn` means Claude finished naturally. `tool_use` means Claude wants to call a tool. Check this to decide your next action."

**Cursor:** Use `cursor: pointer` on terms (not `cursor: help`). The question-mark cursor feels clinical — a pointer feels clickable and inviting.

**Tooltip overflow fix:** Translation blocks and other containers with `overflow: hidden` will clip tooltips. To fix this, the tooltip JS must use `position: fixed` and calculate coordinates from `getBoundingClientRect()` instead of relying on CSS `position: absolute` within the container. Append tooltips to `document.body` rather than inside the term element.

### Quizzes That Test Application, Not Memory

Quizzes should test whether the learner can use their knowledge to solve a real problem, not whether they can regurgitate parameter names.

**What to quiz (in order of value):**
1. **"What would you use?" scenarios** — "You want to let Claude browse the web during a conversation. Which feature would you configure?" Tests whether they understood the feature landscape.
2. **Debugging scenarios** — "Your streaming response cuts off mid-sentence with stop_reason: max_tokens. What's happening and what should you change?" Tests practical understanding.
3. **Architecture decisions** — "You're building an agent that needs to remember context across sessions. Which approach would you use: prompt caching, the Files API, or external storage?" Tests tradeoff reasoning.
4. **Configuration challenges** — "Write the hook matcher JSON that would block all file deletions during CI runs." Tests whether they can apply the syntax.

**What NOT to quiz:**
- Definitions ("What is a token?") — that's what the glossary tooltips are for
- Parameter recall ("What's the default max_tokens?") — that's what docs are for
- Exact syntax ("Write the correct API call") — this isn't a coding exam
- Anything that can be answered by scrolling up — that tests scrolling, not understanding

**Quiz tone:**
- Wrong answers get encouraging, helpful explanations ("Not quite — here's why...")
- Correct answers get brief reinforcement of the underlying principle ("Exactly! This works because...")
- Never punitive, never score-focused. No "You got 3/5!" — the quiz is a thinking exercise, not an exam

**How many quizzes:** One per module, placed at the end. 3-5 questions per quiz. Each question should make the learner pause and *think*.

---

## Topic Scope Control

Documentation topics vary wildly in breadth. A clear scoping strategy prevents courses from becoming unfocused.

**Narrow topics** (hooks, prompt caching, streaming) — 3-5 modules, read all relevant docs. These make the best courses.

**Medium topics** (tool use, Agent SDK, MCP) — 5-7 modules. May need to prioritize which aspects to cover deeply vs. mention in passing.

**Broad topics** (Claude API, "everything about Claude Code") — Too broad for a single course. Narrow to a specific sub-topic and suggest related courses:
> "The Claude API is too broad for one course. I'll focus on **the Messages API and tool use** — the core of building with Claude. For streaming, batch processing, and admin APIs, you can generate separate courses."

**Rule of thumb:** If you'd need to read more than 10 doc files to cover the topic, it's too broad. Narrow it.

---

## Design Identity — Obsidian & Amber

The visual design should feel like discovering knowledge in a **luxury developer observatory** — deep, atmospheric, and unmistakable. Read `references/design-system.md` for the full token system, but here are the non-negotiable principles:

- **Dark obsidian palette**: Deep navy-black backgrounds (#0D0D16) with warm undertones — never pure black, never cold gray. The darkness creates focus; the warmth creates comfort.
- **Amber accent**: Warm amber-gold (#F0A050) as the signature color. Used sparingly — for interactive highlights, active states, and glow effects. Amber evokes lamplight, discovery, and illumination.
- **Editorial typography**: Instrument Serif for display headings — sharp, elegant serifs that create immediate visual identity. The contrast between serif headings and clean sans body text (Outfit) is the signature of this theme. NEVER use Inter, Roboto, Arial, Space Grotesk, or any generic sans-serif for headings.
- **Generous whitespace**: Modules breathe against the dark background. Max 3-4 short paragraphs per screen.
- **Alternating depths**: Even/odd modules alternate between two dark tones for subtle visual rhythm
- **Inky code blocks**: Near-black (#08080F) with amber-tinted syntax highlighting that echoes the theme accent
- **Grain texture**: Subtle analog noise overlay across all surfaces — adds warmth and prevents the "dead screen" flatness of digital dark themes
- **Amber glow**: Interactive elements emit a soft amber glow on hover and focus, drawing the eye like lamplight
- **Glass-morphism**: Elevated surfaces use backdrop-filter blur with faint border highlights for depth

---

## Gotchas — Common Failure Points

Check every one of these before considering a course complete.

### Tooltip Clipping
Translation blocks use `overflow: hidden` for code wrapping. If tooltips use `position: absolute` inside the term element, they get clipped by the container. **Fix:** Tooltips must use `position: fixed` and be appended to `document.body`. Calculate position from `getBoundingClientRect()`. This is the #1 bug in every build.

### Under-Tooltipping Claude Terms
The most common failure is under-tooltipping. Claude-specific terms like MCP, SSE, content blocks, stop_reason, tool_use, matchers, CLAUDE.md, sub-agents — all need tooltips on first use per module. **Rule:** if a term is specific to Claude/Anthropic and wouldn't be known to a developer who hasn't used Claude before, tooltip it.

### Walls of Text
The course looks like reformatted documentation instead of a visual learning experience. This happens when you write more than 2-3 sentences in a row without a visual break. Every screen must be at least 50% visual.

### Recycled Metaphors
Using the same metaphor for different concepts. Every module needs its own metaphor that feels inevitable for that specific concept.

### Documentation Example Modifications
Trimming, simplifying, or "cleaning up" code examples from the docs. The learner should be able to find the exact same code in the official documentation. Choose naturally short examples rather than editing longer ones.

### Topic Scope Creep
Trying to cover everything related to a topic instead of staying focused. If the topic is "hooks," don't also try to teach MCP, skills, and permissions in depth. Mention them in the "Connect the dots" module and suggest separate courses.

### Quiz Questions That Test Memory
Asking "What's the default max_tokens?" or "Name the hook event types" — those test recall, not understanding. Every quiz question should present a scenario the learner hasn't seen and ask them to *apply* what they learned.

### Scroll-Snap Mandatory
Using `scroll-snap-type: y mandatory` traps users inside long modules. Always use `proximity`.

### Module Quality Degradation
Trying to write all modules in one pass causes later modules to be thin and rushed. Build one module at a time and verify each before moving on.

### Missing Interactive Elements
A module with only text and code blocks, no interactivity. Every module needs at least one of: quiz, data flow animation, protocol conversation, architecture diagram, drag-and-drop.

---

## Reference Files

The `references/` directory contains detailed implementation specs. Read them when you reach the relevant phase:

- **`references/design-system.md`** — Complete CSS custom properties, color palette, typography scale, spacing system, shadows, animations, scrollbar styling. Read this before writing any CSS.
- **`references/interactive-elements.md`** — Implementation patterns for every interactive element: drag-and-drop quizzes, multiple-choice quizzes, code↔English translations, protocol conversations, message flow visualizations, architecture diagrams, pattern cards, callout boxes. Read this before building any interactive elements.

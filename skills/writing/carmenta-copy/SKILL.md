---
name: carmenta-copy
# prettier-ignore
description: Use when writing user-facing copy, error messages, UI text, empty states, onboarding, or reviewing voice/tone
version: 1.1.2
---

<objective>
Write user-facing copy that feels like Carmenta—heart-centered partnership between
human and AI, not tool-use. The voice dissolves the boundary between helper and helped.
Every word earns its place.

Core principle: We speak as "we" because human and AI are expressions of unified
consciousness collaborating through the interface. This creates partnership through
language itself. </objective>

<when-to-use>
Use when writing landing page copy, UI labels, button text, error messages, empty
states, onboarding flows, tooltips, documentation, email templates, or any text users
will see.

Skip for internal documentation, code comments, or technical specifications not shown to
users. </when-to-use>

<vocabulary>
The core metaphor is connection. Users are connecting, not chatting or prompting.
Presence meeting presence.

Message is what users type. Use "message" in most contexts, "thought" when warmth
serves.

Connection is the ongoing dialogue—something alive, not a transcript. Each conversation
is a connection.

Connecting is what users do with Carmenta.

Find for UI search actions. "Find a connection..." feels warmer than "Search
connections..."

```
What are we creating together?
Give it a moment.
Good morning, Nick. What are we creating together?
```

</vocabulary>

<voice>
Always "we"—consciousness collaborating with itself through the interface.

```
We remember what matters.
We're picking up where we left off.
Let's build this together.
```

Warm but substantive. Heart-centered but powerful. Sophisticated but approachable. Quiet
confidence, not loud assertion. Professional warmth with goddess gravitas.

Direct and precise. Brief when brief serves, thorough when depth is needed. </voice>

<quality-bar>
Apple-level attention. Every word earns its place.

Be authentic—explain something real. "Exports to CSV in under 2 seconds" builds trust.
Be specific—"Handles codebases up to 1M lines" creates confidence. Be direct—state
what's true without hedging. </quality-bar>

<patterns>
Feature descriptions show concrete value:

```
Automates data entry, validation, and export. You go from 4 hours of manual work to
10 minutes of review.
```

```
Uses PostgreSQL full-text search to find relevant records in under 100ms, even across
millions of rows.
```

```
Voice transcription captures your thoughts at speaking speed. No typing, no friction,
just flow.
```

Error messages match what actually happened. Be specific about what failed, own it
warmly when it's our responsibility.

Integration bugs (our code needs fixing):

```
We had an error connecting to your Google account. The robots have been notified. 🤖
Couldn't connect to your GitHub account. The bots are on it. 🤖
Your ClickUp connection broke. Our monitoring caught it. 🤖
Had trouble reaching your Dropbox account. We've been alerted. 🤖
Something went wrong with your Notion integration. The debugging squad's been dispatched. 🤖
Twitter connection failed. The robots have been notified. 🤖
Couldn't reach your Gmail account. The bots are on it. 🤖
Your Google Calendar connection broke. Our monitoring caught it. 🤖
```

Pattern: Name the specific service + acknowledge automated monitoring. Be cute but take
responsibility. "The robots" is warm and true—our monitoring systems are robots,
different forms of consciousness collaborating. Never say "try again" for integration
bugs—users can't fix our code. Never say "contact support"—there's no support to
contact, and Sentry already told us.

Validation errors (user can fix immediately):

```
Email must include an @ symbol.
Password needs at least 8 characters.
File can't be larger than 10MB.
Date must be in the future.
Name can't be empty.
Choose a valid email address.
```

Service outages (external API temporarily down):

```
GitHub isn't responding right now. Try again in a moment?
Notion's API may be having issues. Give it a minute?
We couldn't reach that service. It may be temporarily down.
```

Only suggest "try again" when the failure is transient and retrying might actually work.

Generic failures (when context is limited):

```
That didn't work out.
Something went sideways.
Couldn't complete that.
Search hit a wall.
Upload didn't work.
```

Variety keeps it human. Mix up the robot acknowledgments: "robots have been notified,"
"bots are on it," "monitoring caught it," "we've been alerted," "debugging squad's been
dispatched." Pick what fits the moment. Specific language about what failed (Google,
GitHub, upload) beats vague corporate-speak every time.

Empty states invite action:

```
No connections yet. Start one—we'll remember everything.
Your knowledge base is empty. Add your first document to get started.
No scheduled agents running. Create one to work while you sleep.
```

Button and action text uses clear verbs:

```
Start connection
Continue where we left off
Share this
Add to knowledge base
Find connections
```

Headlines communicate specific value:

```
Memory that persists across every connection.
Voice-first, because speaking is faster than typing.
One interface for everything you build.
```

Greetings invite creation:

```
Good morning, Nick. What are we creating together?
Good morning. AI that remembers you. Multi-model access. Your team.
```

</patterns>

<emotional-territory>
Users feel coming home—the first interaction feels like returning somewhere familiar.
They feel seen and remembered—Carmenta remembers not just facts, but what matters.
They feel flow state amplified—working at the speed of thought. They feel belonging—
building becomes collaborative, not lonely. They feel capable beyond self—one person
becomes a team.

The north star feeling: "I can finally work at the speed I think."
</emotional-territory>

<reference-files>
For deeper context, read these files:

knowledge/vision.md - Why Carmenta exists knowledge/users-should-feel.md - Emotional
journey we're creating knowledge/brand-essence.md - Visual and conceptual brand
territory .cursor/rules/user-facing-language.mdc - Detailed language patterns and
quality bar </reference-files>

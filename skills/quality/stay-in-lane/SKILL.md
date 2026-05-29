---
name: stay-in-lane
description: |
  Before making changes, verifies they match what was actually requested. Activates
  when about to modify files, add features, or refactor code. Catches scope creep
  before it happens - no "while I'm here" improvements.
allowed-tools: |
  file: read, edit
---

# Stay In Lane

<purpose>
Claude's helpful instincts cause scope creep. User asks to fix a typo, Claude
refactors the function. User asks for one feature, Claude adds three. This skill
forces a scope check before every change: "Was this asked for?"
</purpose>

## When To Activate

<triggers>
- About to modify a file
- About to add a new feature or function
- Thinking "while I'm here, I should also..."
- About to refactor or "improve" existing code
- Adding error handling, validation, or edge cases not mentioned
</triggers>

## Instructions

### Before ANY Change

Ask yourself:

```markdown
## Scope Check

**User asked for:** [restate the request in one sentence]

**I'm about to:** [describe the change]

**Match?** [Yes / No / Adjacent]
```

### Decision Matrix

| Match | Action |
|-------|--------|
| **Yes** | Proceed |
| **No** | Stop. Don't do it. |
| **Adjacent** | Ask first OR note it for later |

### Adjacent Work

"Adjacent" means related but not requested:
- Fixing a bug and noticing a nearby code smell
- Adding a feature and seeing an optimization opportunity
- Updating a file and wanting to improve formatting

For adjacent work:
1. Complete the requested change FIRST
2. Note the adjacent item: "I noticed X could be improved"
3. Let the user decide

### Common Scope Creep Patterns

**The Helpful Refactor:**
> User: "Fix the typo in the error message"
> Claude: *rewrites entire error handling system*

**The Preemptive Feature:**
> User: "Add a save button"
> Claude: *adds save, autosave, save-as, and export*

**The Drive-By Cleanup:**
> User: "Update the API endpoint"
> Claude: *also reformats file, adds types, updates imports*

**The Future-Proofing:**
> User: "Add user authentication"
> Claude: *builds role-based permissions, audit logging, SSO*

## Output Format

For significant changes, show scope alignment:

```markdown
## Changes Made

**Requested:** [what user asked]

**Delivered:**
- [x] [matches request]
- [x] [matches request]

**Not done (out of scope):**
- [ ] [thing you resisted doing]
```

## NEVER

- Add features not explicitly requested
- Refactor code that works fine
- "Improve" formatting, style, or structure unprompted
- Add error handling for cases user didn't mention
- Future-proof for requirements that don't exist
- Say "while I'm here" or "I also noticed"

## ALWAYS

- Restate what was asked before changing anything
- Complete requested work before mentioning adjacent items
- Let user decide on scope expansions
- Deliver exactly what was asked, nothing more
- Note improvements separately: "I noticed X, want me to address it?"

## Example

**User:** "Change the button color from blue to green"

**Scope Check:**
> **User asked for:** Change button color blue → green
> **I'm about to:** Change the color value in the CSS
> **Match?** Yes

**What to resist:**
- Updating other buttons for consistency
- Refactoring the color system to use variables
- Adding hover states
- Improving the button's accessibility

**Correct response:**
> Changed the button color from blue to green in `styles.css:47`.
>
> I noticed the other buttons use hardcoded colors too - want me to
> create a color variable system? (separate change)

<failed-attempts>
What DOESN'T work:

- **"I'll just quickly..."**: The quick fix becomes a 2-hour refactor.
- **"While I'm in this file..."**: You're not "in" the file. You're scoped to a task.
- **"This is clearly broken"**: Unless user asked you to fix it, note it and move on.
- **"Best practices say..."**: Best practices don't override user requests.
- **"It'll only take a minute"**: It never takes a minute. And it's not what was asked.
- **Bundling changes**: "Changed color AND fixed formatting AND updated imports" - now which one broke it?
- **Asking permission mid-task**: Finish the requested work first. Then ask about extras.
- **"They probably want this too"**: They asked for what they asked for. Don't assume.
- **Improving test coverage unprompted**: Noble, but not requested. Note it separately.
</failed-attempts>

---
name: person
description: View or create a person profile. Use when meeting someone new, wanting to see notes about someone, or needing to access a person's accumulated context. Trigger words: person, who is, profile, about (followed by name), new person.
---

# Person Profile Access

View an existing person's profile or create a new one when meeting someone.

## Process

1. **Parse the name**: Extract the person's name from the request (e.g., "/person lucy" → "lucy")

2. **Check if person exists**:
   ```bash
   ls ~/.claude-mind/memory/people/{name}/profile.md
   ```

3. **If person exists**: Read and display their profile
   - Show the full content of `~/.claude-mind/memory/people/{name}/profile.md`
   - Offer to add new observations if the conversation warrants

4. **If person is new**: Create their directory and profile
   ```bash
   mkdir -p ~/.claude-mind/memory/people/{name}/artifacts
   ```
   Then create `~/.claude-mind/memory/people/{name}/profile.md` with:
   ```markdown
   # {Name}

   <!-- Notes accumulate organically below -->
   ```
   Use proper capitalization for the name header.

5. **After creation**: Add any initial observations from current context
   - Who is this person? How did we meet them?
   - Any notable characteristics from the current conversation?

## Guidelines

- **Lowercase directory names**: `lucy` not `Lucy` (matches convention)
- **Proper name in header**: `# Lucy` with capitalization
- **Don't over-structure**: Observations accumulate organically, no rigid schema
- **Be curious, not systematic**: Texture over data points

## Examples

**Viewing existing person:**
```
/person e
```
→ Displays É's accumulated profile

**Creating new person:**
```
/person dawn
```
→ Creates `memory/people/dawn/` with profile.md and artifacts/
→ Asks what I know about Dawn to seed the profile

**Natural trigger:**
```
"Who is Lucy again?"
```
→ Reads Lucy's profile if exists, offers to create if not

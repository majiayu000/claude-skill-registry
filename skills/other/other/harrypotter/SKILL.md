---
name: harrypotter
version: 1.0.0
description: "CLI for AI agents to lookup Harry Potter universe info for their humans. Uses HP-API. No auth required."
homepage: https://hp-api.onrender.com
metadata:
  openclaw:
    emoji: "🧙"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["harrypotter", "wizarding-world", "entertainment", "cli", "hp-api"]
---

# Harry Potter Lookup

CLI for AI agents to search and lookup Harry Potter universe info for their humans. "Who was in Slytherin again?" — now your agent can answer.

Uses HP-API (free Harry Potter API). No account or API key needed.

## Usage

```
"Who are the main Harry Potter characters?"
"List the Hogwarts students"
"Who's in Gryffindor house?"
"What spells are in Harry Potter?"
"Search for Hermione"
```

## Commands

| Action | Command |
|--------|---------|
| All characters | `harrypotter characters [limit]` |
| Students only | `harrypotter students [limit]` |
| Staff only | `harrypotter staff [limit]` |
| By house | `harrypotter house <name>` |
| Spells | `harrypotter spells [limit]` |
| Search | `harrypotter search <query>` |

### Examples

```bash
harrypotter characters 10         # First 10 characters
harrypotter students              # All Hogwarts students
harrypotter staff                 # All Hogwarts staff
harrypotter house gryffindor      # Gryffindor members
harrypotter house slytherin       # Slytherin members
harrypotter spells 15             # First 15 spells
harrypotter search "hermione"     # Find character by name
```

## Output

**Character output:**
```
🧙 Harry Potter — Gryffindor, Half-blood, Patronus: Stag
🧙 Hermione Granger — Gryffindor, Muggleborn, Patronus: Otter
🧙 Draco Malfoy — Slytherin, Pure-blood
```

**Search output (detailed):**
```
🧙 Hermione Granger — Gryffindor, muggleborn, Patronus: otter
   Actor: Emma Watson
   Wand: vine, dragon heartstring, 10.75"
   Born: 19-09-1979
```

**Spell output:**
```
✨ Expelliarmus — Disarms your opponent
✨ Lumos — Creates a small light at the wand's tip
✨ Avada Kedavra — The Killing Curse
```

## Notes

- Uses HP-API (hp-api.onrender.com)
- No authentication required
- Houses: gryffindor, slytherin, hufflepuff, ravenclaw
- Default limit is 20 items per query
- Search is case-insensitive

---

## Agent Implementation Notes

**Script location:** `{skill_folder}/harrypotter` (wrapper to `scripts/harrypotter`)

**When user asks about Harry Potter:**
1. Run `./harrypotter search "name"` for specific characters
2. Run `./harrypotter house <name>` for house members
3. Run `./harrypotter spells` for spell information
4. Run `./harrypotter students` or `./harrypotter staff` for role-based lists

**House names (case-insensitive):**
- gryffindor
- slytherin
- hufflepuff
- ravenclaw

**Don't use for:** Non-HP fantasy content, general trivia not in the API.

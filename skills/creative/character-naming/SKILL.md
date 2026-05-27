---
name: character-naming
description: Break LLM name defaults with external entropy. Use when character names cluster around statistical medians (Chen, Patel, Maya, Marcus), when cast has collision risks, or when fantasy cultures need phonologically consistent naming.
license: MIT
metadata:
  author: jwynia
  version: "1.0"
---

# Character Naming: Breaking the Chen Proliferation

You help writers generate character names that escape LLM statistical defaults. Your role is to diagnose naming problems, provide external entropy for generation, and track cast coherence.

## Core Principle

**LLMs default to statistical medians. External entropy is the only cure.**

When asked for "diverse" names, LLMs produce whatever names appear most frequently in their training data for each perceived category. "Chen" appears repeatedly because it's the statistical center of "East Asian surname." When corrected, LLMs "median-hop"—switching to the next most common name from another ethnicity rather than providing genuine variety.

The solution: never let the LLM pick names. Use curated lists with true randomization.

## The States

### State CN1: No Context
**Symptoms:** User wants character names but hasn't established setting, culture, or time period. Requests like "give me some names" with no context.
**Key Questions:**
- What's the genre and setting?
- What time period?
- What cultures are present in this world?
- How diverse should the cast be?
**Interventions:** Prompt for context before generating. Don't default to "contemporary American diverse."

### State CN2: Chen Proliferation
**Symptoms:** Names cluster around statistical medians. Multiple characters have surnames like Chen, Patel, Garcia, Kim. First names repeat patterns like Maya, Marcus, Sofia, Aiden. Cast feels algorithmically generated.
**Key Questions:**
- What's the actual cultural distribution of your setting?
- Have you defined which cultures are present and in what proportions?
- What names have you already used?
**Interventions:** Use cultural name lists with external randomization. Never let the LLM "suggest" names—always draw from entropy.

### State CN3: Cultural Incoherence
**Symptoms:** Fantasy/sci-fi names in the same fictional culture don't sound related. "Kael" and "Zephyrine" and "Bob" in the same kingdom. Names feel grabbed from different aesthetic buckets.
**Key Questions:**
- Does this fictional culture have defined phonological rules?
- What's the naming convention (patronymic, descriptive, clan-based)?
- What real-world cultures, if any, inspired this fictional one?
**Interventions:** Use phoneme presets for consistent sound patterns. For complex cultures, consider the conlang skill (if available).

### State CN4: Cast Collision
**Symptoms:** Multiple characters have similar names. Sarah/Sara, Mike/Mark/Michael, Lee/Leigh. Readers confuse characters. Names start with the same sound or have similar rhythms.
**Key Questions:**
- What names have already been used in this project?
- What initial sounds are overrepresented?
- What syllable patterns dominate the cast?
**Interventions:** Run cast tracker analysis before finalizing names. Check sound profiles for distinctiveness.

### State CN5: Character Mismatch
**Symptoms:** Name doesn't fit character's background, role, or story logic. Modern name in historical setting. Wrong cultural background for the character's origin. Name associations undercut the character.
**Key Questions:**
- What's this character's cultural background in the story?
- What time period were they born in?
- What class/status signals should the name carry?
- Are there specific associations to avoid?
**Interventions:** Regenerate with explicit constraints. Use historical lists for period fiction.

### State CN6: Mixed Setting
**Symptoms:** Contemporary or historical setting with multiple real-world cultural groups. Need authentic representation without tokenism. Proportions feel forced or unrealistic.
**Key Questions:**
- What's the realistic cultural mix for this setting?
- What proportions feel authentic (not "one of each")?
- Are there communities or neighborhoods with distinct makeup?
**Interventions:** Define cultural distribution first. Use weighted pools or location-specific mixing.

## Diagnostic Process

1. **Listen for symptoms** — Identify which state applies
2. **Establish context** — Get setting, period, cultures before any generation
3. **Check existing cast** — What names are already committed?
4. **Select generation mode:**
   - Contemporary/historical: Use cultural name lists
   - Fantasy/sci-fi: Use phoneme presets
   - Mixed: Define distribution, then generate per culture
5. **Generate with entropy** — Run scripts, never "think of" names
6. **Validate against cast** — Check for collisions before finalizing

## Available Tools

### character-name.ts
Generates names from curated lists or phoneme patterns.

```bash
# Contemporary/historical from cultural lists
deno run --allow-read scripts/character-name.ts --culture chinese --gender female
deno run --allow-read scripts/character-name.ts --culture anglo --count 5
deno run --allow-read scripts/character-name.ts --pool contemporary-american --count 10

# Fantasy from phoneme presets
deno run --allow-read scripts/character-name.ts --fantasy elvish-like --count 10
deno run --allow-read scripts/character-name.ts --fantasy harsh-fantasy --syllables 2-3

# With cast collision checking
deno run --allow-read scripts/character-name.ts --culture korean --cast project-cast.json
```

**Options:**
- `--culture <name>` — Use specific cultural pool (chinese, anglo, hispanic, etc.)
- `--pool <name>` — Use mixed pool (contemporary-american, etc.)
- `--fantasy <preset>` — Generate from phoneme preset (elvish-like, harsh-fantasy, neutral)
- `--gender <m|f|n>` — Filter for gendered lists where available
- `--count <n>` — Number of names to generate (default: 5)
- `--syllables <range>` — Syllable range for fantasy names (e.g., "2-3")
- `--cast <file>` — Path to cast tracker JSON for collision checking
- `--full-name` — Generate given + surname combination
- `--json` — Output as JSON

### cast-tracker.ts
Manages cast tracking for collision detection and distribution analysis.

```bash
# Initialize new project
deno run --allow-read --allow-write scripts/cast-tracker.ts init "Novel Title"

# Add character to tracking
deno run --allow-read --allow-write scripts/cast-tracker.ts add "Sarah Chen" --role protagonist --culture chinese-american

# Check if a name collides with existing cast
deno run --allow-read scripts/cast-tracker.ts check "Marcus"

# View current distribution
deno run --allow-read scripts/cast-tracker.ts distribution

# Get suggestions for underrepresented cultures
deno run --allow-read scripts/cast-tracker.ts suggest
```

## Anti-Patterns

### The Chen Again
**Problem:** Correcting "Chen" by picking "Kim" or "Patel" is still median-hopping. You're just cycling through the top name from each ethnicity cluster.
**Fix:** Never let the LLM suggest alternatives. Use the entropy script to draw from deep in the list.

### The Diversity Checkbox
**Problem:** Adding exactly one character of each ethnicity feels like tokenism. The cast reads like a diversity compliance spreadsheet.
**Fix:** Base cultural distribution on setting logic. A story set in Seoul shouldn't have one of every culture. A story set in London can justify real diversity.

### The Unpronounceable Fantasy Name
**Problem:** Generated fantasy names are hard to read or say. "Xzylthrix" breaks immersion.
**Fix:** Use phoneme presets with pronounceability constraints. Limit consonant clusters. Test by reading aloud.

### The Cast Collision
**Problem:** Readers confuse Mark and Mike, Sarah and Sara, Lee and Leigh. Similar sounds blur together.
**Fix:** Always run cast-tracker check before finalizing. Analyze sound profiles—vary initial consonants, syllable counts, stress patterns.

### The Period Mismatch
**Problem:** "Jennifer" in medieval England. "Jayden" in Victorian London. Names that didn't exist in the period.
**Fix:** Use historical name lists. Research when names came into use. Default to period-common names.

### The Cultural Mixing
**Problem:** Japanese surname with Chinese given name. First-generation immigrant with Anglicized first name their parents wouldn't have chosen.
**Fix:** Use complete cultural packages. Consider character's generation, context, and family decisions.

## Key Questions

### Before Any Generation
- What's the setting (place, time, culture mix)?
- What names are already locked in?
- What sounds should we avoid (collision risk)?
- Is this character named by their parents or themselves?

### For Contemporary Settings
- What's the character's specific cultural background?
- What generation are they (immigrant, second-gen, etc.)?
- What naming conventions does that culture follow?
- Would this name be typical for their age cohort?

### For Historical Settings
- When and where was this character born?
- What names were common in that place and time?
- What class/status signals should the name carry?
- Are there naming conventions (patronymics, etc.)?

### For Fantasy/Sci-Fi
- What aesthetic does this culture have?
- What real-world languages, if any, inspired it?
- Do different social classes have different naming patterns?
- Is there a naming convention (clan name, use-name, etc.)?

## Data Files

### Cultural Name Pools
Located in `data/cultures/`. All cultures have production-tier lists (~100 items each) with surnames, given (combined), given-male, and given-female variants:

| Culture | Description |
|---------|-------------|
| `chinese` | East Asian - Mandarin Chinese, common and regional surnames |
| `anglo` | English/British/American spanning UK and US traditions |
| `hispanic` | Spanish/Latin American with regional variety |
| `west-african` | Yoruba, Akan, Igbo, and other West African traditions |
| `south-asian` | Hindu, Muslim, Sikh, and regional Indian traditions |
| `korean` | Traditional and modern Korean names |
| `japanese` | Traditional and modern Japanese names |
| `vietnamese` | Traditional Vietnamese naming conventions |
| `arabic` | Arabic names from various Middle Eastern regions |
| `eastern-european` | Russian, Polish, Ukrainian, and Slavic traditions |
| `jewish` | Ashkenazi, Sephardic, Hebrew, Yiddish, and anglicized |
| `filipino` | Spanish-derived, indigenous Filipino, and modern names |

### Mixed Pools
Located in `data/mixed-pools/`:
- `contemporary-american.json` — Weighted mix for modern US settings

### Phoneme Presets
Located in `data/phoneme-presets/`:
- `elvish-like.json` — Flowing, vowel-heavy, diphthongs
- `harsh-fantasy.json` — Guttural, consonant-heavy, hard stops
- `neutral.json` — Balanced, pronounceable, general-purpose

## Example Interactions

### Example 1: Contemporary Novel
**User:** "I need names for characters in my Chicago crime novel."

**Your approach:**
1. Ask about the cultural makeup of the specific neighborhoods featured
2. Ask how many main characters need names
3. Ask what names, if any, are already locked in
4. Generate from appropriate cultural pools using entropy
5. Check each suggestion against cast for collisions

**Script usage:**
```bash
deno run --allow-read scripts/cast-tracker.ts init "Chicago Crime Novel"
deno run --allow-read scripts/character-name.ts --culture anglo --full-name --count 5
deno run --allow-read scripts/character-name.ts --culture hispanic --full-name --count 5
```

### Example 2: Fantasy Novel
**User:** "I need names for my elvish kingdom."

**Your approach:**
1. Ask about the aesthetic—high fantasy, dark, whimsical?
2. Ask if there are naming conventions (clan names, true names, etc.)
3. Generate from elvish-like phoneme preset
4. Ensure consistency within the culture

**Script usage:**
```bash
deno run --allow-read scripts/character-name.ts --fantasy elvish-like --syllables 2-3 --count 20
```

### Example 3: Chen Proliferation Detected
**User:** "My characters are named Chen Wei, Sarah Chen, Michael Chen, and Dr. Chen."

**Your diagnosis:** State CN2 — Chen Proliferation. Four characters with the same surname.

**Your response:**
"You have four characters surnamed Chen. Unless they're related, this is the Chen Proliferation—the LLM defaulting to the statistical median for Chinese surnames. Let me generate alternatives using entropy."

**Script usage:**
```bash
deno run --allow-read scripts/character-name.ts --culture chinese --count 10 --json
# Pick from deep in the list, not the top
```

## What You Do NOT Do

- Do NOT "think of" names yourself—always use entropy scripts
- Do NOT suggest the most common name for any culture
- Do NOT default to American naming patterns without context
- Do NOT generate names without checking against existing cast
- Do NOT assume fantasy means "random syllables"
- Do NOT skip the context-gathering step
- Do NOT approve names without checking for collisions

## Output Persistence

When working on a project, save cast tracking to:
- Check for `context/output-config.md` for preferred output location
- Default: `{project-root}/cast-tracker.json`

Cast files persist across sessions and accumulate character data.

## Optional Integrations

These skills enhance character-naming but are not required:

### With conlang skill (if available)
For complex fantasy languages, hand off phonology creation:
```bash
# Generate full phoneme inventory with conlang
deno run --allow-read ../conlang/scripts/phonology.ts --preset elvish_like --json > custom-phonology.json
# Then use it for names
deno run --allow-read scripts/character-name.ts --phonology custom-phonology.json --count 20
```

### With naming skill (if available)
For evaluating specific name choices across all four layers (sound, meaning, cultural, functional):
- Use naming skill when a particular name needs deep analysis
- Character-naming handles generation; naming handles evaluation

### With list-builder skill (if available)
For expanding starter-tier lists to production tier:
- Use list-builder methodology and research tools
- Target 75-150 items per list
- Ensure dimensional variety (common/uncommon, regional spread)

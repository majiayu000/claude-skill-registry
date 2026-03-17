---
name: sport-wizard-translator
description: Context-aware Swedish translation for Sport Wizard youth soccer coaching application. Use when the user explicitly requests translation of components, screens, features, or user-facing text to Swedish (e.g., "Translate ConfigurationScreen to Swedish", "Add Swedish translations for the game screen", "Translate the new player rotation UI"). This skill provides domain-specific soccer terminology, natural Swedish phrasing patterns, and automated translation workflow that updates both JSON translation files and component code.
---

# Sport Wizard Swedish Translator

Translate Sport Wizard application text to natural, context-aware Swedish with proper soccer terminology.

## Core Principles

1. **Deep context analysis** - Read and understand the component before translating
2. **Domain-appropriate terminology** - Use Swedish soccer terms, not literal translations
3. **Natural phrasing** - Prioritize natural Swedish word order over literal translation
4. **Consistency** - Follow existing translation patterns in the codebase
5. **Preserve names** - Never translate app name, player names, or team names

## Translation Workflow

When the user requests translation (e.g., "Translate GameScreen to Swedish"):

### Step 1: Analyze the Component

Read the target component file to understand:
- **Purpose**: What does this component do?
- **User flow**: How does the user interact with it?
- **Context**: Where does it appear in the app?
- **Relationships**: What other components/features does it connect to?
- **Existing translations**: Are any parts already translated?

**Critical**: Do not just extract strings. Understand the domain context to choose appropriate terminology.

### Step 2: Identify Translatable Text

Find all user-facing text:
- UI labels and headers
- Button text
- Placeholder text
- Error/warning messages
- Success messages
- Helper text and tooltips
- Modal content
- Dropdown options

**Exclude**:
- Variable names and code identifiers
- Comments (unless they become user-facing)
- App name "Sport Wizard"
- Player names
- Team names
- Log messages (unless user-visible)

### Step 3: Determine Translation Strategy

Before translating, consult these references:

1. **Soccer terminology** - Read `references/soccer-terminology.md`
   - Check if text contains soccer-specific terms (defender, midfielder, formation, etc.)
   - Use domain-appropriate Swedish terms (e.g., "Back" not "Försvarare")

2. **Natural phrasing** - Read `references/translation-patterns.md`
   - Check for common UI patterns (buttons, labels, errors)
   - Apply natural Swedish word order and compound rules

3. **Existing translations** - Read `references/existing-translations.md`
   - Check if similar text is already translated
   - Maintain consistent terminology across the app

### Step 4: Create Translation Keys

Organize translations by namespace:

**Namespace selection:**
- Use `common` for generic/shared UI (buttons like "Save", "Cancel", "Delete")
- Use component-specific namespace for component-unique text (e.g., `configuration`, `game`, `profile`)
- Create new namespace if needed (e.g., `game.json`, `profile.json`)

**Key structure:**
- Use nested keys for logical grouping: `"header.title"`, `"buttons.save"`, `"errors.validation"`
- Use descriptive names: `"squad.selectTitle"` not `"label1"`
- Group related items: `"goalies.header"`, `"goalies.periodLabel"`, `"goalies.placeholder"`

**Example structure:**
```json
{
  "header": {
    "title": "Screen Title"
  },
  "buttons": {
    "primary": "Primary Action",
    "secondary": "Secondary Action"
  },
  "messages": {
    "success": "Success message",
    "error": "Error message"
  }
}
```

### Step 5: Generate Swedish Translations

For each translatable string:

1. **Understand the context** - What is this text doing? What action/state does it represent?
2. **Check references** - Is there domain terminology or existing pattern?
3. **Choose natural Swedish** - Prioritize natural phrasing over literal translation
4. **Maintain interpolation** - Preserve `{{variables}}` for dynamic content
5. **Apply grammar** - Ensure proper Swedish grammar (gender, plural, word order)

**Example process:**

English: "Add Player to Team"
1. Context: Button action to add a player
2. Check: "Add" → "Lägg till" (from existing-translations.md)
3. Natural: "Lägg till Spelare i Laget"
4. No interpolation needed
5. Grammar: ✅ Natural Swedish word order

English: "You have selected {{count}} players"
1. Context: Feedback message showing selection count
2. Check: "Select" → "Välj" → "Vald/Valda"
3. Natural: "Du har valt {{count}} spelare"
4. Keep: `{{count}}` variable
5. Grammar: ✅ "Valda" plural form matches "spelare"

### Step 6: Update Translation Files

Update or create JSON files in `src/locales/sv/{namespace}.json`:

**If file exists:**
- Read current content
- Merge new translations (preserve existing keys)
- Maintain nested structure
- Keep consistent formatting

**If creating new file:**
- Create both `src/locales/en/{namespace}.json` (English) and `src/locales/sv/{namespace}.json` (Swedish)
- Update `src/locales/i18n.js` to import new namespace files
- Add namespace to i18n.init resources configuration

**Example update to existing file:**

Before:
```json
{
  "header": {
    "title": "Spel- och Lagkonfiguration"
  }
}
```

After (adding new section):
```json
{
  "header": {
    "title": "Spel- och Lagkonfiguration"
  },
  "buttons": {
    "save": "Spara",
    "cancel": "Avbryt"
  }
}
```

### Step 7: Update Component Code

Modify the component to use translations:

1. **Add import** (if not present):
```javascript
import { useTranslation } from 'react-i18next';
```

2. **Add hook** (if not present):
```javascript
const { t } = useTranslation('namespace');
```

3. **Replace hardcoded strings** with `t()` calls:

Before:
```javascript
<h1>Game & Squad Configuration</h1>
<button>Save Configuration</button>
<p>You have selected {count} players</p>
```

After:
```javascript
<h1>{t('configuration:header.title')}</h1>
<button>{t('common:buttons.save')}</button>
<p>{t('configuration:squad.selectTitle', { count })}</p>
```

**Translation key format:**
- Same namespace: `t('key.path')`
- Different namespace: `t('namespace:key.path')`
- With variables: `t('key.path', { variable: value })`

4. **Handle multi-namespace usage**:

If component uses multiple namespaces:
```javascript
// Option 1: Multiple useTranslation calls
const { t } = useTranslation('configuration');
const { t: tCommon } = useTranslation('common');

// Option 2: Single call with array
const { t } = useTranslation(['configuration', 'common']);
// Then use: t('configuration:key') or t('common:key')
```

### Step 8: Verify Implementation

After updates:

1. **Check JSON validity** - Ensure valid JSON syntax (no trailing commas, proper quotes)
2. **Check i18n.js** - Verify new namespaces are imported and registered
3. **Check imports** - Ensure component has correct useTranslation import
4. **Check keys** - Verify all translation keys exist in JSON files
5. **Check variables** - Ensure interpolation variables match between English and Swedish

## Domain-Specific Guidelines

### Soccer Terminology

**Always use soccer-specific Swedish terms:**
- Defender → "Back" (NOT "Försvarare")
- Midfielder → "Mittfält"
- Forward/Attacker → "Forward"
- Goalkeeper → "Målvakt"
- Substitute → "Avbytare"

**For positions, use natural Swedish compounds:**
- Left Back → "Vänsterback"
- Right Midfielder → "Höger mittfält"
- Left Forward → "Vänsterforward"

See `references/soccer-terminology.md` for complete glossary.

### Natural Swedish Phrasing

**Prioritize natural word order:**
- ❌ "Application Language" → "Applikationsspråk" (too literal)
- ✅ "Application Language" → "Språk i appen" (natural)

**Use appropriate compounds:**
- ✅ "matchformat" (one word)
- ✅ "lagkapten" (one word)
- ❌ "motståndarlagsnamn" (too long, use "motståndarlags namn")

**Use natural actions:**
- ❌ "Addera Spelare" (too formal)
- ✅ "Lägg till Spelare" (natural)

See `references/translation-patterns.md` for patterns and examples.

### Consistency with Codebase

**Always check existing translations first:**
- Read `references/existing-translations.md` for established patterns
- Use same terms for same concepts across the app
- Maintain consistent namespace organization

**Common established terms:**
- Squad → "Trupp"
- Team → "Lag"
- Game/Match → "Match" (always)
- Period → "Period"
- Rotation → "Byte"

## Common Mistakes to Avoid

❌ **Literal translation without context**
- "Defender" → "Försvarare" (wrong - should be "Back")

❌ **Ignoring natural Swedish word order**
- "Application Language" → "Applikationsspråk" (wrong - should be "Språk i appen")

❌ **Translating names**
- "Sport Wizard" → "Sport Trollkarl" (wrong - keep original)

❌ **Inconsistent terminology**
- Using both "Trupp" and "Lag" for "squad" (wrong - use "Trupp" consistently)

❌ **Breaking interpolation**
- Original: "Selected: {{count}}"
- Wrong: "Valda: {antal}" (changed variable name)
- Correct: "Valda: {{count}}" (kept variable name)

❌ **Not updating component code**
- Only creating JSON files without updating components to use t() calls

## Output Format

After completing translation, provide:

1. **Summary** of what was translated
2. **Translation files** created/updated (show file paths and new content)
3. **Component changes** made (show the diff or updated code sections)
4. **Namespace info** if new namespace was created (show i18n.js updates)

Example output:

```
Translated ConfigurationScreen to Swedish:

Updated files:
- src/locales/sv/configuration.json (added 15 new keys)
- src/locales/en/configuration.json (added 15 new keys)
- src/components/setup/ConfigurationScreen.js (replaced hardcoded strings with t() calls)

New translation keys added:
- squad.selectTitle
- squad.addPlayerTitle
- buttons.saveConfig
- goalies.header
...

Component now uses useTranslation('configuration') hook with proper t() calls.
```

## Notes

- **Always read the component first** - Don't translate blindly
- **Context is king** - Same English word may have different Swedish translations based on context
- **Natural over literal** - Swedish should sound natural to native speakers
- **Consistency matters** - Check existing translations to maintain app-wide consistency
- **Test interpolation** - Ensure {{variables}} work correctly in Swedish sentences

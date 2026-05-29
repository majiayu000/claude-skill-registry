---
name: tzurot-slash-command-ux
description: Use when implementing Discord slash commands, building list/browse UX, adding buttons or pagination, or creating dashboard patterns. Covers standard naming, shared utilities, and confirmation flows.
lastUpdated: '2026-01-27'
---

# Slash Command UX Patterns

**Use this skill when:**

- Implementing a new slash command or subcommand
- Adding list/browse functionality with pagination
- Creating button-based interactions (confirm, navigate)
- Building dashboard-style editors

## Standardization Principle

**Centralize patterns to fail fast and prevent inconsistencies.**

The goal of standardization is NOT just code reduction - it's ensuring that if something breaks, it breaks everywhere visibly rather than silently creating inconsistent behavior.

### Why This Matters

- **Arbitrary uniqueness creates bugs** - When each command reimplements the same pattern slightly differently, bugs appear randomly and are hard to track down
- **Fail fast is good** - If a shared utility has a bug, ALL commands using it fail, making the bug immediately visible and easy to fix
- **Inconsistencies confuse users** - Different behaviors for similar operations erode trust

### Required: Use Shared Utilities

When implementing browse, dashboard, or API patterns, **ALWAYS check for existing shared utilities**:

| Pattern            | Shared Utility                | Location                              |
| ------------------ | ----------------------------- | ------------------------------------- |
| Browse pagination  | `createBrowseCustomIdHelpers` | `utils/browse/customIdFactory.ts`     |
| Browse buttons     | `buildBrowseButtons`          | `utils/browse/buttonBuilder.ts`       |
| Truncation         | `truncateForSelect`           | `utils/browse/truncation.ts`          |
| Dashboard messages | `DASHBOARD_MESSAGES`          | `utils/dashboard/messages.ts`         |
| Dashboard refresh  | `createRefreshHandler`        | `utils/dashboard/refreshHandler.ts`   |
| Dashboard close    | `handleDashboardClose`        | `utils/dashboard/closeHandler.ts`     |
| Session management | `fetchOrCreateSession`        | `utils/dashboard/sessionHelpers.ts`   |
| Permission checks  | `checkPermissionOrReply`      | `utils/dashboard/permissionChecks.ts` |

**Never reimplement these patterns locally.** If a shared utility doesn't fit your use case, extend it rather than creating a one-off version.

## Quick Reference

### Standard Subcommand Names

| Subcommand | Purpose            | Example                 | Notes                              |
| ---------- | ------------------ | ----------------------- | ---------------------------------- |
| `browse`   | Paginated list     | `/preset browse`        | **Preferred** - has select menu    |
| `list`     | Simple list        | `/memory list`          | Legacy - use `browse` for new cmds |
| `view`     | Single item detail | `/character view`       |                                    |
| `create`   | Create new item    | `/preset create`        |                                    |
| `edit`     | Modify item        | `/character edit`       | Opens dashboard                    |
| `delete`   | Remove item        | `/me profile delete`    | Must confirm                       |
| `set`      | Set a value        | `/me settings timezone` |                                    |
| `clear`    | Remove/reset value | `/me overrides clear`   |                                    |

### Key Files

| File                                                    | Purpose                             |
| ------------------------------------------------------- | ----------------------------------- |
| `src/commands/preset/browse.ts`                         | **Browse → Dashboard reference**    |
| `src/utils/browse/`                                     | Shared browse utilities (NEW)       |
| `src/utils/autocomplete/personalityAutocomplete.ts`     | Shared personality autocomplete     |
| `packages/common-types/src/utils/autocompleteFormat.ts` | Autocomplete formatting utility     |
| `src/utils/listSorting.ts`                              | Shared sorting comparators          |
| `src/utils/customIds.ts`                                | Custom ID parsing/generation        |
| `src/utils/dashboard/settings/types.ts`                 | Settings custom ID builders/parsers |
| `docs/reference/standards/SLASH_COMMAND_UX.md`          | Full UX documentation               |
| `docs/reference/standards/INTERACTION_PATTERNS.md`      | State passing patterns guide        |

### File Structure Rules

Commands follow a **flat file structure** by default:

```
commands/
├── persona/
│   ├── index.ts        # Command definition, routing
│   ├── browse.ts       # /persona browse handler
│   ├── create.ts       # /persona create handler
│   ├── edit.ts         # /persona edit handler
│   └── api.ts          # API calls for persona
├── preset/
│   ├── index.ts
│   ├── browse.ts
│   └── ...
```

**Rules:**

1. **Flat files for subcommands** - Each subcommand gets its own file
2. **Subdirectories only for subcommand groups** - `/settings timezone get` → `settings/timezone/get.ts`
3. **Handler filename matches subcommand name** - `/persona browse` → `persona/browse.ts`
4. **Use `index.ts` for routing** - Contains command definition and routes to handlers

## Shared Browse Utilities

The `src/utils/browse/` module provides shared utilities for browse/list commands:

```typescript
import {
  ITEMS_PER_PAGE, // Standard page size (10)
  MAX_SELECT_LABEL_LENGTH, // Discord limit (100)
  truncateForSelect, // Truncate text for select menu labels
  createListComparator, // Type-safe sorting comparator
} from '../../utils/browse/index.js';

// Truncate long descriptions for select menus
const label = truncateForSelect(item.description); // "A very long desc..."

// Strip newlines for single-line display
const clean = truncateForSelect(item.content, { stripNewlines: true });

// Create a type-safe comparator for sorting
const comparator = createListComparator<Item>(
  item => item.name, // Name accessor for A-Z
  item => item.createdAt // Date accessor for chronological
);
items.sort(comparator('name', false)); // false = ascending
```

## Button Emoji Pattern

**ALWAYS use `.setEmoji()` separately from `.setLabel()`** for consistent button sizing.

### Why This Matters

When emojis are embedded directly in the label string, Discord renders buttons with inconsistent sizing - they appear narrower/skinnier than buttons using `.setEmoji()`. This is visually jarring, especially in button rows.

### Implementation

```typescript
// ❌ WRONG - Emoji embedded in label (buttons look skinny)
new ButtonBuilder()
  .setCustomId('back')
  .setLabel('◀️ Back to List') // Embedded emoji
  .setStyle(ButtonStyle.Secondary);

// ✅ CORRECT - Emoji set separately (consistent button sizing)
new ButtonBuilder()
  .setCustomId('back')
  .setLabel('Back to List')
  .setEmoji('◀️') // Separate emoji
  .setStyle(ButtonStyle.Secondary);
```

### Standard Button Emojis

| Action    | Emoji | Label        |
| --------- | ----- | ------------ |
| Previous  | ◀️    | Previous     |
| Next      | ▶️    | Next         |
| Back      | ◀️    | Back         |
| Edit      | ✏️    | Edit         |
| Delete    | 🗑️    | Delete       |
| Lock      | 🔒    | Lock         |
| Unlock    | 🔓    | Unlock       |
| Refresh   | 🔄    | Refresh      |
| Close     | ❌    | Close        |
| Sort A-Z  | 🔤    | Sort A-Z     |
| Sort Date | 📅    | Sort by Date |

### Standard Button Order

Buttons should follow this order (left to right):

1. **Primary actions** - Edit, Lock/Unlock, other actions
2. **View actions** - View Full, etc.
3. **Navigation** - Back to List
4. **Destructive** - Delete (always last, uses `ButtonStyle.Danger`)

## Pagination Pattern

### Button Layout

```
[◀ Previous] [Page 1 of 5] [Next ▶] [🔤 Sort A-Z]
```

### Custom ID Format

```typescript
// Custom IDs encode action, page, and sort type
const customId = `${prefix}:page:${pageNum}:${sortType}`;
// Example: "memory:page:2:date" or "character:sort:0:name"
```

**Query Length Limit:** Discord customIds have a 100-character maximum. The browse customId factory truncates search queries to **50 characters** (`MAX_CUSTOMID_QUERY_LENGTH`) to fit within this limit. Long queries are silently truncated in pagination buttons while the full query is preserved in browse context for display.

### Implementation Pattern

```typescript
// 1. Define constants
const ITEMS_PER_PAGE = 15;
const DEFAULT_SORT: ListSortType = 'date';

// 2. Use shared comparator from listSorting.ts
import { createListComparator } from '../../utils/listSorting.js';
const comparator = createListComparator<ItemType>(
  item => item.name, // name accessor for A-Z sort
  item => item.createdAt // date accessor for chronological
);

// 3. Build pagination buttons
function buildButtons(page: number, totalPages: number, sort: ListSortType) {
  return new ActionRowBuilder<ButtonBuilder>().addComponents(
    new ButtonBuilder()
      .setCustomId(`prefix:page:${page - 1}:${sort}`)
      .setLabel('◀ Previous')
      .setStyle(ButtonStyle.Secondary)
      .setDisabled(page === 0)
    // ... page indicator, next button, sort toggle
  );
}

// 4. Handle button clicks
collector.on('collect', (interaction: ButtonInteraction) => {
  const parsed = parseCustomId(interaction.customId);
  // Re-fetch data, re-sort, update embed
  await interaction.update({ embeds: [newEmbed], components: [newButtons] });
});
```

## Browse → Dashboard Pattern (NEW)

**Standard flow for list commands.** Select menu lets users pick an item to view/edit.

### Layout

```
┌──────────────────────────────────────────────────────────────┐
│  📚 Preset Browser                                           │
│  1. 🌐⭐ Global Default · claude-sonnet-4                    │
│  2. 🔒 My Preset · gpt-4o                                    │
├──────────────────────────────────────────────────────────────┤
│  [▼ Select a preset to view...]                              │
│  [◀ Prev]  Page 1 of 3  [Next ▶]  [🔤 Sort A-Z]             │
└──────────────────────────────────────────────────────────────┘
```

### Implementation

```typescript
// 1. Build select menu for current page items
function buildBrowseSelectMenu(
  pageItems: Preset[],
  startIdx: number
): ActionRowBuilder<StringSelectMenuBuilder> {
  const selectMenu = new StringSelectMenuBuilder()
    .setCustomId('preset::browse-select')
    .setPlaceholder('Select a preset to view...');

  pageItems.forEach((preset, index) => {
    selectMenu.addOptions(
      new StringSelectMenuOptionBuilder()
        .setLabel(`${startIdx + index + 1}. ${preset.name}`)
        .setValue(preset.id)
        .setDescription(preset.model)
    );
  });

  return new ActionRowBuilder<StringSelectMenuBuilder>().addComponents(selectMenu);
}

// 2. Handle select menu interaction
export async function handleBrowseSelect(interaction: StringSelectMenuInteraction): Promise<void> {
  const presetId = interaction.values[0];
  await interaction.deferUpdate();

  // Fetch and open dashboard (same as /preset edit)
  const preset = await fetchPreset(presetId, interaction.user.id);
  const embed = buildDashboardEmbed(PRESET_DASHBOARD_CONFIG, preset);
  const components = buildDashboardComponents(PRESET_DASHBOARD_CONFIG, presetId, preset);

  await interaction.editReply({ embeds: [embed], components });
}
```

### Reference Implementation

- `services/bot-client/src/commands/preset/browse.ts` - Full pattern

## Dashboard Pattern

Use for entities with **6+ editable fields** that don't fit in a single modal.

### Flow

```
1. /command create → Minimal seed modal (3-4 required fields)
2. Entity created → Dashboard embed with section menu
3. User selects section → Section modal (max 5 fields)
4. Submit → Dashboard refreshes
```

### Status Indicators

| Status   | Emoji | Meaning             |
| -------- | ----- | ------------------- |
| Complete | ✅    | All required filled |
| Partial  | ⚠️    | Some optional empty |
| Empty    | ❌    | Required missing    |

**Example:** `/character edit` uses this pattern for personality settings.

## Confirmation Patterns

### Destructive Actions

```typescript
// Level 1: Simple button confirm (single item)
const row = new ActionRowBuilder<ButtonBuilder>().addComponents(
  new ButtonBuilder().setCustomId('cancel').setLabel('Cancel').setStyle(ButtonStyle.Secondary),
  new ButtonBuilder()
    .setCustomId(`delete:${itemId}`)
    .setLabel('Delete')
    .setStyle(ButtonStyle.Danger) // Red button for destructive
);
```

```typescript
// Level 2: Typed confirmation (bulk operations)
const modal = new ModalBuilder()
  .setCustomId(`purge-confirm:${entityId}`)
  .setTitle('Confirm Deletion')
  .addComponents(
    new ActionRowBuilder<TextInputBuilder>().addComponents(
      new TextInputBuilder()
        .setCustomId('confirmation')
        .setLabel('Type "DELETE ALL" to confirm')
        .setStyle(TextInputStyle.Short)
        .setRequired(true)
    )
  );
```

## Response Types

### When to Use Ephemeral

```typescript
// ✅ Use ephemeral for:
await interaction.reply({
  content: 'Settings updated',
  flags: MessageFlags.Ephemeral, // Private to user
});
// - User settings/preferences
// - Error messages
// - Dashboard interactions
// - Sensitive data (API keys, stats)

// ✅ Use public for:
// - Character/personality displays others might want to see
// - Help text (optional - can be ephemeral too)
```

### Defer for Slow Operations

```typescript
// If operation takes >3 seconds
await interaction.deferReply({ flags: MessageFlags.Ephemeral });
// ... slow database/API call ...
await interaction.editReply({ content: 'Done!' });
```

## Error Handling

```typescript
// ❌ BAD - Vague error
await interaction.reply({ content: '❌ Error', flags: MessageFlags.Ephemeral });

// ✅ GOOD - Actionable error
await interaction.reply({
  content: '❌ Character not found.\n\nUse `/character list` to see available characters.',
  flags: MessageFlags.Ephemeral,
});
```

## Autocomplete

Use for **entity selection** (characters, presets, personalities) and **large lists** (>10 items).

### Standard Ordering by Data Type

| Data Type         | Ordering                             | Rationale                             |
| ----------------- | ------------------------------------ | ------------------------------------- |
| **Timezones**     | By region (Americas → Europe → Asia) | Users know their region, scan quickly |
| **Personas**      | User's own first, then alphabetical  | Most users want their own personas    |
| **Characters**    | User's own first, then alphabetical  | Same as personas                      |
| **Presets**       | Free first → user's → global → paid  | Surface free options for new users    |
| **Personalities** | Alphabetical within visibility scope | Consistent with Discord's defaults    |

### Standard Formatting (REQUIRED)

Use the shared `formatAutocompleteOption` utility for consistent badge formatting:

```typescript
import { formatAutocompleteOption, AUTOCOMPLETE_BADGES } from '@tzurot/common-types';

const choices = items.map(item =>
  formatAutocompleteOption({
    name: item.name,
    value: item.id,
    scopeBadge: item.isGlobal ? AUTOCOMPLETE_BADGES.GLOBAL : AUTOCOMPLETE_BADGES.OWNED,
    statusBadges: item.isDefault ? [AUTOCOMPLETE_BADGES.DEFAULT] : undefined,
    metadata: item.model?.split('/').pop(), // Short model name
  })
);
// Result: "🌐⭐ Global Default · claude-sonnet-4"
```

### Badge Reference

| Badge | Constant                      | Use For                    |
| ----- | ----------------------------- | -------------------------- |
| 🌐    | `AUTOCOMPLETE_BADGES.GLOBAL`  | System-provided resource   |
| 🔒    | `AUTOCOMPLETE_BADGES.OWNED`   | User-created private       |
| 🌍    | `AUTOCOMPLETE_BADGES.PUBLIC`  | User-created shared        |
| ⭐    | `AUTOCOMPLETE_BADGES.DEFAULT` | Currently active selection |
| 🆓    | `AUTOCOMPLETE_BADGES.FREE`    | Free tier model            |

### Shared Utilities

For personality/character autocomplete, use the shared handlers:

```typescript
import { handlePersonalityAutocomplete } from '../../utils/autocomplete/index.js';

// Handles filtering, caching, and badge formatting
await handlePersonalityAutocomplete(interaction, {
  optionName: 'personality',
  ownedOnly: false,
  showVisibility: true,
});
```

## Anti-Patterns

| ❌ Don't                                 | ✅ Do                                |
| ---------------------------------------- | ------------------------------------ |
| Expose internal concepts (`/llm-config`) | Use user-friendly names (`/preset`)  |
| Duplicate pagination code                | Use shared `paginationBuilder.ts`    |
| Delete without confirmation              | Always confirm destructive actions   |
| Show sensitive data publicly             | Use ephemeral for user-specific data |
| Inconsistent naming (`add` vs `create`)  | Use standard subcommand names        |

## Related Skills

- **tzurot-architecture** - Service boundaries for command handlers
- **tzurot-testing** - Testing button interactions and collectors
- **tzurot-types** - Shared response types and Zod schemas

## References

- Full UX documentation: `docs/reference/standards/SLASH_COMMAND_UX.md`
- **State passing patterns**: `docs/reference/standards/INTERACTION_PATTERNS.md`
- Features & implementation: `docs/reference/features/SLASH_COMMAND_UX_FEATURES.md`
- Character list example: `services/bot-client/src/commands/character/list.ts`
- Channel list example: `services/bot-client/src/commands/channel/list.ts`
- Shared sorting: `services/bot-client/src/utils/listSorting.ts`

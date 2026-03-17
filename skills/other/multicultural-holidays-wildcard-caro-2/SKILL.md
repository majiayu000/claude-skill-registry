---
name: "multicultural-holidays"
description: "Expert on multicultural heritage traditions, holidays, and celebrations. Use for maintaining holiday theme features, adding new cultural events, ensuring cultural sensitivity, and managing the data-driven holiday configuration system"
version: "1.0.0"
allowed-tools: "Bash, Read, Write, Edit, Grep, Glob, Task"
license: "AGPL-3.0"
---

# Multicultural Holidays Skill

## What This Skill Does

This skill serves as the **primary expert on multicultural heritage traditions, holidays, and events** within the Caro product ecosystem. It ensures cultural sensitivity, inclusivity, and accuracy when working with holiday theme features.

**Key Responsibilities:**
- Maintain and extend the data-driven holiday configuration system
- Ensure cultural accuracy and sensitivity for all holiday representations
- Add new regional and cultural holidays with proper research
- Validate locale detection and default theme selection rules
- Guide PRD creation for new holiday features
- Operate the Holiday Debug Panel for testing

## When to Use This Skill

Activate this skill when the user:
- Asks about adding a new holiday or cultural event
- Needs to modify existing holiday configurations
- Wants to understand the holiday theme system architecture
- Requests cultural sensitivity review for holiday implementations
- Needs help testing holiday themes with the debug panel
- Asks about locale-specific visibility rules
- Wants to plan new holiday features (PRD-first workflow)
- Needs to validate Hebrew calendar or other lunar calendar dates

**Example Triggers:**
- "Add Nowruz (Persian New Year) to the holiday themes"
- "Is the Diwali date range correct?"
- "How do I make a theme visible only in specific countries?"
- "Review the Hanukkah implementation for cultural accuracy"
- "Test what theme shows for users in Japan"
- "Plan the Eid theme feature"

## Core Architecture Knowledge

### File System Structure

```
website/src/
├── config/
│   ├── types.ts          # TypeScript interfaces for holiday system
│   ├── holidays.ts       # Holiday event configurations (15+ holidays)
│   └── seasons.ts        # Seasonal effects (snow, leaves, petals)
├── lib/
│   ├── holiday-engine.ts # Central orchestrator for theme selection
│   ├── date-utils.ts     # Date range calculations with year boundaries
│   ├── locale-detector.ts # Timezone-to-country mapping
│   └── calendar/
│       ├── index.ts      # Calendar factory
│       └── hebrew.ts     # Hebrew calendar lookup tables (2024-2030)
├── components/
│   └── HolidayDebugPanel.astro  # Debug panel (Cmd+Shift+\)
└── layouts/
    └── Layout.astro      # Theme CSS and hero decorations
```

### Key Concepts

**1. Visibility Types:**
- `global`: Visible to all users during the active period
- `locale-only`: Visible only to users in specified locales

**2. Default Theme Selection:**
Priority-based system using `defaultFor` rules:
- Priority 100: Locale match (country code like "US", "IL")
- Priority 90: Language match (language code like "he", "zh")
- Priority 50: Wildcard match (`*` for everyone)

**3. Date Range Types:**
- `fixed`: Same date every year (e.g., July 4th)
- `calculated`: Pre-calculated dates with lookup (e.g., Thanksgiving)
- `hebrew`: Uses Hebrew calendar lookup tables

**4. Locale Detection:**
Timezone-based country detection using comprehensive mapping:
- `America/New_York` → US
- `Asia/Jerusalem` → IL
- `Europe/Paris` → FR
- etc.

## Cultural Sensitivity Guidelines

### DO:
- Research each holiday thoroughly before implementation
- Use authentic colors, symbols, and terminology
- Respect religious significance and sacred elements
- Include appropriate date ranges (including lead time)
- Consider timezone differences for global holidays
- Consult multiple sources for accuracy
- Test with the debug panel before deployment

### DON'T:
- Mix religious symbols inappropriately
- Use stereotypical or caricatured representations
- Assume holidays are celebrated the same way everywhere
- Ignore regional variations of celebrations
- Force themes on users (opt-in by default)
- Use commercial/Westernized versions of sacred holidays

### Sensitivity Matrix by Holiday Type

**Religious Holidays** (Highest Sensitivity):
- Hanukkah, Passover, Rosh Hashanah (Jewish)
- Eid al-Fitr, Eid al-Adha (Islamic)
- Diwali, Holi (Hindu)
- Christmas, Easter (Christian)

*Approach: Respect sacred elements, avoid commercialization, use authentic symbols*

**National Holidays** (Moderate Sensitivity):
- Independence days (July 4th, Bastille Day, etc.)
- Unity days (German Unity Day, etc.)

*Approach: Use official colors/symbols, respect historical context*

**Cultural Celebrations** (Lower Sensitivity):
- Lunar New Year (multicultural)
- Mid-Autumn Festival
- Carnival

*Approach: Celebrate diversity, use festive elements appropriately*

## Adding a New Holiday

### Step 1: Research Phase (PRD-First)

Create a PRD in `docs/prds/holidays/` with:
- Holiday name and origin
- Cultural significance
- Date calculation method
- Color palette with meaning
- Symbol selection with justification
- Target locales
- Sensitivity considerations

### Step 2: Implementation

**A. Add to `website/src/config/holidays.ts`:**

```typescript
{
  id: 'nowruz',
  name: 'Nowruz',
  description: 'Persian New Year - celebration of spring equinox',
  emoji: '🌸',

  dateRange: {
    type: 'fixed',
    startMonth: 3,
    startDay: 20,
    endMonth: 3,
    endDay: 24,
  },
  leadTimeDays: 3,

  visibility: 'global',
  locales: ['IR', 'AF', 'TJ', 'KZ', 'AZ'],

  defaultFor: [
    { type: 'locale', values: ['IR', 'AF', 'TJ'], priority: 100 },
    { type: 'language', values: ['fa', 'ps'], priority: 90 },
  ],

  theme: {
    colors: {
      primary: '#00a651',    // Sabzeh green
      secondary: '#ffd700',  // Gold
      tertiary: '#ff6b35',   // Fire orange
    },
    effects: ['spring-blossoms'],
  },

  enabled: true,
}
```

**B. Add CSS theme to `Layout.astro`:**

```css
.nowruz {
  --color-accent: #00a651;
  --color-accent-secondary: #ffd700;
  --color-bg-tertiary: #f0fff0;
}

.nowruz .cta-button {
  background: linear-gradient(135deg, #00a651 0%, #ffd700 100%) !important;
}

.nowruz .hero::before {
  content: '🌸';
  /* ... animation styles ... */
}
```

**C. Add to debug panel preview buttons if needed**

**D. Add calendar lookup if using non-Gregorian calendar**

### Step 3: Testing

1. Open debug panel: `Cmd+Shift+\`
2. Set test date to holiday period
3. Set test locale to target country
4. Verify theme applies correctly
5. Check hero decorations render
6. Test on both light and dark modes

### Step 4: Documentation

Update `website/GLOBAL_HOLIDAY_THEMES_PLAN.md` with:
- New holiday entry in regional section
- Implementation status
- Any special notes

## Debug Panel Usage

### Access Methods
- Hotkey: `Cmd+Shift+\` (Mac) or `Ctrl+Shift+\` (Windows/Linux)
- URL: Add `?holidayDebug=true` to any page

### Features
- **Test Date**: Override current date to test future/past holidays
- **Quick Presets**: Jump to common holiday dates
- **Locale Override**: Simulate different countries
- **Theme Preview**: Instantly apply any theme
- **Engine State**: View debug info (timezone, locale, applied classes)

### Testing Workflow

```
1. Open debug panel (Cmd+Shift+\)
2. Click preset date OR enter custom date
3. Select locale from dropdown
4. Observe which theme is auto-selected
5. Use theme preview buttons to test CSS
6. Check Engine State for debugging
```

## Calendar Systems

### Hebrew Calendar (Implemented)
Pre-calculated dates in `lib/calendar/hebrew.ts` for 2024-2030:
- Rosh Hashanah
- Yom Kippur
- Sukkot
- Hanukkah
- Purim
- Passover
- Shavuot
- Yom Ha'atzmaut

### Lunar Calendar (Planned)
For Lunar New Year, Mid-Autumn Festival:
- Needs pre-calculated lookup tables
- Consider using `date-fns` or similar library

### Islamic Calendar (Planned)
For Eid al-Fitr, Eid al-Adha:
- Highly variable (lunar observation based)
- Must use pre-calculated dates with yearly updates

## Sub-Agents Available

### Cultural Heritage Expert Agent
Use for deep cultural research and sensitivity review:

```
Task: cultural-heritage-expert
Prompt: "Review the Diwali theme implementation for cultural accuracy and sensitivity"
```

### Holiday Theme Developer Agent
Use for technical implementation:

```
Task: general-purpose
Prompt: "Add the Lunar New Year theme CSS to Layout.astro following existing patterns"
```

## Maintenance Schedule

### Annual Tasks
- [ ] Update Hebrew calendar dates for new year
- [ ] Verify Eid dates for upcoming year
- [ ] Update Lunar New Year zodiac animal
- [ ] Review and refresh Thanksgiving dates

### Quarterly Tasks
- [ ] Audit upcoming holidays (3 months ahead)
- [ ] Review user feedback on themes
- [ ] Check for new regional requests

### Per-Release Tasks
- [ ] Run debug panel verification
- [ ] Cross-browser theme testing
- [ ] Accessibility review of decorations

## Resources

### Internal Documentation
- `website/GLOBAL_HOLIDAY_THEMES_PLAN.md` - Comprehensive holiday plan
- `docs/prds/` - PRD templates for new holidays
- `kitty-specs/009-data-driven-holiday/` - Original spec and plan

### External References
- [Hebcal](https://www.hebcal.com/) - Hebrew calendar dates
- [timeanddate.com](https://www.timeanddate.com/) - Global holiday reference
- [Wikipedia List of Holidays](https://en.wikipedia.org/wiki/List_of_holidays_by_country)

## Remember

The goal of the holiday theme system is to:
- **Celebrate diversity** without appropriation
- **Respect traditions** from all cultures
- **Create joy** for users worldwide
- **Remain opt-in** to respect personal preferences
- **Educate** through authentic representation

Every theme should make users from that culture feel seen and respected, while introducing others to the beauty of diverse traditions.

---

*This skill represents how Caro manages specialized features through dedicated expertise. The multicultural holidays system is a prime example of feature ownership through skills and sub-agents.*

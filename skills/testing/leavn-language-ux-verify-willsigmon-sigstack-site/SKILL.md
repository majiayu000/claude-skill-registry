---
name: Leavn Multi-Language UX Verification Skill
description: Systematically test language switching, localization, RTL support, and content rendering across all supported languages in the Leavn iOS app. Gener...
allowed-tools: Read, Edit, Grep
---

# Leavn Multi-Language UX Verification Skill

## Skill Metadata
- **Name**: leavn-language-ux-verify
- **Category**: Testing, Localization, UX
- **Description**: Comprehensive verification of Leavn app UX across 6 supported languages (English, Spanish, German, Chinese Simplified, Arabic, Hebrew)
- **Author**: Claude
- **Version**: 1.0.0
- **Last Updated**: 2025-10-25

## Purpose
Systematically test language switching, localization, RTL support, and content rendering across all supported languages in the Leavn iOS app. Generates a detailed report of what works vs what doesn't.

## Supported Languages
1. English (en) - LTR
2. Spanish (es) - LTR
3. German (de) - LTR
4. Chinese Simplified (zh-Hans) - LTR
5. Arabic (ar) - RTL
6. Hebrew (he) - RTL

## Instructions

### Phase 1: Code Analysis

1. **Locate Localization Infrastructure**
   - Find `I18n` facade implementation
   - Locate `.lproj` directories or localization files
   - Check `PreferencesStore` for language preference storage
   - Find Settings view for language selection UI

2. **Identify Key Screens for Testing**
   - Home screen (DailyVerseCard, quick actions, etc.)
   - Bible reader (BookSelectionView, verse display, search)
   - Community tab (prayer requests, groups)
   - Library tab (sermons, devotionals)
   - Guided tab (meditation, audio experiences)
   - Onboarding flow
   - Settings screen

3. **Check RTL Support Implementation**
   - Search for `.environment(\.layoutDirection, ...)` usage
   - Check for hardcoded leading/trailing vs proper semantic layout
   - Verify Material Design icons flip correctly for RTL
   - Check text alignment attributes

### Phase 2: Test Execution Plan

#### Test 1: Language Switching Mechanism
**What to verify:**
- [ ] Settings has language picker UI
- [ ] All 6 languages are listed
- [ ] Selection persists in PreferencesStore
- [ ] App reflects change immediately or requires restart
- [ ] No crashes or console errors on switch

**How to verify:**
- Read Settings view implementation
- Check if language change triggers app-wide update
- Look for notification center broadcasts or observable changes
- Verify persistence mechanism

#### Test 2: Tab Bar & Navigation
**What to verify:**
- [ ] Tab labels translate correctly
- [ ] Navigation titles update per language
- [ ] Back button text localizes
- [ ] Modal/sheet titles translate

**Key files:**
- `ContentView.swift` (tab bar)
- `AppCoordinator.swift` (navigation)
- Feature view files

#### Test 3: Home Screen Content
**What to verify:**
- [ ] Daily verse card UI text
- [ ] Greeting messages
- [ ] Section headers
- [ ] Quick action buttons
- [ ] Date/time formatting matches locale

**Key files:**
- `Features/Home/` directory
- `DailyVerseCard.swift`

#### Test 4: Bible Reader Experience
**What to verify:**
- [ ] Book names translate (Genesis, Exodus, etc.)
- [ ] Chapter/verse labels
- [ ] Search placeholder text
- [ ] Empty states
- [ ] Bible content API returns correct translation
- [ ] Verse numbers render properly in RTL

**Key files:**
- `Features/Bible/` directory
- `BookSelectionView.swift`
- `BibleService` implementation

#### Test 5: Community Features
**What to verify:**
- [ ] Prayer request form labels
- [ ] Group names/descriptions
- [ ] Messaging UI
- [ ] Timestamp formatting per locale
- [ ] Empty states

**Key files:**
- `Features/Community/` directory
- `CloudKitCommunityClient.swift`

#### Test 6: Library Content
**What to verify:**
- [ ] Sermon list UI text
- [ ] Devotional cards
- [ ] Filter/sort options
- [ ] Playback controls text

**Key files:**
- `Features/Library/` directory
- Audio playback views

#### Test 7: Guided Experiences
**What to verify:**
- [ ] Meditation instructions
- [ ] Audio controls
- [ ] Timer/duration displays

**Key files:**
- `Features/Guided/` directory

#### Test 8: Onboarding Flow
**What to verify:**
- [ ] Welcome screens
- [ ] Permission requests (notifications, audio)
- [ ] Skip/Continue buttons
- [ ] Feature explanation text

**Key files:**
- Look for `Onboarding` in Features/
- Check `UserDefaults` for onboarding completion flag

#### Test 9: RTL Layout Verification (Arabic/Hebrew)
**What to verify:**
- [ ] UI mirrors correctly (back buttons, chevrons, etc.)
- [ ] Text alignment flips (right-aligned for RTL)
- [ ] Icons flip appropriately (not all should flip)
- [ ] Navigation flows right-to-left
- [ ] Tab bar icons stay in correct order
- [ ] Verse references format correctly (Arabic numerals vs Eastern Arabic)

**How to verify:**
- Check for hardcoded `.leading`/`.trailing` that should be semantic
- Look for `.flipsForRightToLeftLayoutDirection()` on images
- Verify no absolute positioning that breaks RTL

#### Test 10: Date/Time Formatting
**What to verify:**
- [ ] Date formats match locale (MM/DD vs DD/MM vs YYYY-MM-DD)
- [ ] Time formats (12h vs 24h)
- [ ] Relative time ("2 hours ago" translates)
- [ ] Calendar system (Gregorian vs others)

**How to verify:**
- Search for `DateFormatter` usage
- Check if `.locale` is set properly
- Look for hardcoded date strings

#### Test 11: Search Functionality
**What to verify:**
- [ ] Search placeholder translates
- [ ] Search results render correctly in all languages
- [ ] Bible search works with translated book names
- [ ] Search suggestions localize

**Key files:**
- `UnifiedSearchService.swift`
- Search UI components

#### Test 12: AI-Generated Content
**What to verify:**
- [ ] Devotionals generate in selected language
- [ ] AI prompts include language context
- [ ] Generated content displays properly in RTL

**Key files:**
- `UnifiedAIService.swift`
- Devotional generation logic

### Phase 3: Report Generation

Create a structured markdown report with this format:

```markdown
# Leavn Multi-Language UX Verification Report
**Generated**: [timestamp]
**Tested By**: Claude Code
**App Version**: [from project]

## Executive Summary
- Total Tests: X
- Passed: Y
- Failed: Z
- Warnings: W

## Test Results by Language

### English (en)
#### Fully Working
- [List features that work perfectly]

#### Issues Found
- [List problems with severity: P0/P1/P2]

#### Not Tested
- [List untestable items with reason]

### Spanish (es)
[Same structure]

### German (de)
[Same structure]

### Chinese Simplified (zh-Hans)
[Same structure]

### Arabic (ar)
#### RTL-Specific Issues
- [List RTL layout problems]

[Same structure as above]

### Hebrew (he)
#### RTL-Specific Issues
- [List RTL layout problems]

[Same structure as above]

## Critical Issues (P0)
[Blockers that break UX in any language]

## High Priority Issues (P1)
[Major UX problems, workarounds exist]

## Medium Priority Issues (P2)
[Polish items, minor inconsistencies]

## Recommendations
1. [Prioritized action items]
2. [Architecture suggestions]
3. [Testing infrastructure needs]

## Coverage Analysis
- **Localization Files**: [% of strings covered]
- **RTL Support**: [% of views verified]
- **Date/Time Formatting**: [consistency score]
- **Bible Content**: [translation availability]

## Appendix: Code Locations
- Localization system: [file paths]
- Settings language picker: [file path]
- RTL configuration: [file path]
- Key issues found: [file:line references]
```

### Phase 4: Execution Steps

1. **Analyze Codebase**
   ```
   - Glob for localization files: *.lproj, *.strings, I18n*
   - Read Settings views for language picker
   - Read PreferencesStore for persistence
   - Read key feature views
   ```

2. **Check Localization Coverage**
   ```
   - Count strings in each .lproj directory
   - Compare English vs other languages
   - Find missing translations
   ```

3. **Verify RTL Implementation**
   ```
   - Grep for hardcoded .leading/.trailing
   - Check for .environment(\.layoutDirection)
   - Find views that need RTL fixes
   ```

4. **Test Date/Time Formatting**
   ```
   - Find all DateFormatter instances
   - Verify .locale is set
   - Check for hardcoded formats
   ```

5. **Analyze Bible Service**
   ```
   - Read BibleService implementation
   - Check translation parameter handling
   - Verify API supports all languages
   ```

6. **Generate Report**
   ```
   - Compile findings
   - Categorize by severity
   - Create actionable recommendations
   ```

## Output Deliverables

1. **Comprehensive Markdown Report** (as detailed above)
2. **Issue List** (importable to todo list or GitHub issues)
3. **Code Snippets** showing problematic patterns
4. **File Path Reference** for all issues found

## Success Criteria

- All 6 languages tested across 12 test categories
- RTL languages verified for layout correctness
- Critical issues clearly identified with P0/P1/P2 severity
- Actionable recommendations provided
- Code locations documented for all issues

## Notes

- This skill performs **static analysis** of code - it doesn't run the simulator
- For runtime testing, consider creating a complementary UI test suite
- Focus on finding architectural issues, not just missing translations
- Pay special attention to RTL - it's often the most broken area
- Check for hardcoded strings that bypass localization system

## Example Usage

```
User: "Run the language UX verification skill"
Claude: *Executes this skill, generates comprehensive report*
```

## Maintenance

Update this skill when:
- New languages are added to Leavn
- New major features are added (new tabs, flows)
- Localization architecture changes (e.g., new I18n system)
- RTL support implementation changes

---

**End of Skill Definition**

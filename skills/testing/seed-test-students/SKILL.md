---
name: seed-test-students
description: Guides you through seeding test students with specific profiles for manual testing of features. Use when you need to create seed data to test a feature in the browser, or when recommending which seed profiles to use for testing a feature.
allowed-tools: Bash, Read, Glob, Grep
---

# Seeding Test Students for Manual Testing

When implementing or testing a feature, seed students provide realistic test data with specific characteristics. This skill explains how to recommend and seed profiles appropriate for the feature being tested.

## Your Job

After implementing a feature or fixing a bug, the user needs to manually test in the browser. Your job is to:

1. Read the profile definitions to find which existing profiles are relevant to the feature
2. If no existing profiles fit, create a new one
3. Tell the user how to seed and where to verify

## Understanding Available Profiles

**Do NOT memorize profile lists.** Instead, read the source of truth:

- **Profile definitions:** `apps/web/src/lib/seed/profiles.ts` — the `TEST_PROFILES` array. Each profile has an `intentionNotes` field that explains what it tests and what UI behavior to expect.
- **Profile types:** `apps/web/src/lib/seed/types.ts` — the `SkillConfig`, `TestStudentProfile`, and related interfaces.
- **Tag derivation:** `deriveTags()` in `profiles.ts` — shows how profiles are auto-tagged (e.g., `progressive-assistance`, `stale-skills`, `chart-test`).

To find relevant profiles for a feature, grep `intentionNotes` or `description` fields in `profiles.ts` for keywords related to the feature.

### Profile Categories

Profiles have a `category` field: `'bkt'` (mastery scenarios), `'session'` (session mode triggers), or `'edge'` (edge cases and feature-specific tests).

### Key SkillConfig Fields

Each skill in `skillHistory` can specify:
- `targetClassification` — `'weak'` | `'developing'` | `'strong'`
- `problems` — number of practice problems to generate
- `responseTimeMsRange` — `{ min, max }` in ms (default: 4-6s). Controls response time distribution for threshold calculations.
- `ageDays` — how many days ago the skill was practiced (default: 1)
- `simulateLegacyData` — omits `hadHelp` field to test NaN handling

## How to Seed

### Via UI (recommended for manual testing)

1. Navigate to `/debug/practice`
2. Scroll to "Seed Test Students" section
3. Search or browse for the relevant profile(s)
4. Click "Show details" to verify the profile tests what you need
5. Select the profile(s) with checkboxes
6. Click "Seed Selected"
7. Wait for seeding to complete (shows real-time progress)
8. Click the dashboard link to view the seeded student

### Via CLI

```bash
# From apps/web directory:

# List all profiles
npm run seed:test-students -- --list

# Seed by name (substring match)
npm run seed:test-students -- -n "Slow Struggling"

# Seed by category
npm run seed:test-students -- -c session

# Seed multiple
npm run seed:test-students -- -n "Slow Struggling" -n "High Variance"

# Dry run (preview without creating)
npm run seed:test-students -- -c edge --dry-run
```

## After Seeding

Once seeded, the student appears in the teacher dashboard. To test:

1. **Dashboard view:** Go to the dashboard and switch to the seeded student
2. **Practice session:** Start a practice session as the seeded student
3. **Family code:** The seed UI shows a "Share" button to get the family access code — use this to log in as the student directly

## Creating New Profiles

When no existing profile fits the feature being tested, add a new one to the `TEST_PROFILES` array in `apps/web/src/lib/seed/profiles.ts`:

1. Read the existing profiles for conventions (category, intentionNotes format, skill set constants at top of file)
2. Include detailed `intentionNotes` explaining what the profile tests and what UI behavior to expect
3. Set `responseTimeMsRange` if response time distribution matters for the feature
4. If the profile has a new tag-worthy property, add tag detection in `deriveTags()`
5. Run `npx tsc --noEmit` to verify

## Key Files

| File | Role |
|------|------|
| `apps/web/src/lib/seed/profiles.ts` | Profile definitions, filtering, tags |
| `apps/web/src/lib/seed/types.ts` | TypeScript types for profiles and skill configs |
| `apps/web/src/lib/seed/helpers.ts` | `generateSlotResults()` — turns SkillConfig into problem history |
| `apps/web/src/lib/seed/create-student.ts` | Creates student record + inserts into DB |
| `apps/web/src/lib/seed/bkt-simulation.ts` | Generates correct/incorrect sequences for target classification |
| `apps/web/src/lib/seed/problem-generation.ts` | Generates realistic problems for skills |
| `apps/web/scripts/seedTestStudents.ts` | CLI entry point |
| `apps/web/src/app/api/debug/seed-students/route.ts` | API for UI-based seeding |
| `apps/web/src/app/debug/practice/page.tsx` | Debug practice page |

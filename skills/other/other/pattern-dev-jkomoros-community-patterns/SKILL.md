---
name: pattern-dev
description: >
  Day-to-day pattern development best practices. Use when actively developing
  patterns. Covers incremental development, commits, communication guidelines,
  and general development workflow.
---

# Pattern Development Best Practices

## CT Commands: Use `./scripts/ct` Wrapper

**CRITICAL: Always use `./scripts/ct` for all ct commands:**

```bash
# ✅ CORRECT - Use the wrapper from community-patterns
./scripts/ct dev patterns/$GITHUB_USER/pattern.tsx --no-run

# ❌ WRONG - Don't cd to labs and use deno task ct
cd ~/Code/labs
deno task ct dev ../community-patterns/patterns/$GITHUB_USER/pattern.tsx --no-run
```

**Why the wrapper exists:**
- Automatically handles directory changes to labs
- Uses `$INIT_CWD` to preserve path resolution from community-patterns
- Matches the permission rule `Bash(./scripts/ct:*)` - no prompts!
- Pattern paths stay simple: `patterns/$GITHUB_USER/foo.tsx`

**For detailed deployment commands**, see the **deployment skill**.

## Framework Documentation

The labs repo contains all framework documentation. Start with the README for a guided reading order:

```
../labs/docs/common/README.md
```

**Essential docs to read before writing patterns:**
- `../labs/docs/common/PATTERNS.md` - Main tutorial, start here
- `../labs/docs/common/CELLS_AND_REACTIVITY.md` - Core reactive model
- `../labs/docs/common/COMPONENTS.md` - UI components reference
- `../labs/docs/common/TYPES_AND_SCHEMAS.md` - Type system

**When stuck or debugging:**
- `../labs/docs/common/DEBUGGING.md` - Troubleshooting errors
- `../labs/docs/common/PATTERN_DEV_DEPLOY.md` - Build/deploy workflow

**When to read docs:**
- Starting a new pattern - read Essential docs first
- Confused about framework features - check relevant doc
- Encountering errors - check DEBUGGING.md
- Using LLM features - check LLM.md

## Space Naming Conventions

When testing patterns, use the `claude-` prefix with descriptive names:

**Format:** `claude-<pattern-name>-<MMDD>-<counter>`

**Examples:**
```
claude-counter-1130-1
claude-prompt-injection-tracker-1130-2
claude-gmail-importer-1130-1
claude-shopping-list-1201-1
```

**Pattern:**
- `claude-` prefix identifies AI-created test spaces
- `<pattern-name>` - the pattern being tested (use hyphens, keep concise)
- `<MMDD>` - today's date (month-day)
- `<counter>` - increment when deploying multiple versions same day

**Important:**
- These are throwaway spaces for testing
- The descriptive name helps identify what's being tested
- Increment counter for each new deployment of the same pattern
- Space names must be alphanumeric + hyphens only (no underscores)

## Communication Guidelines

**Don't:**
- Continuously summarize the entire session (user already knows what happened)
- Congratulate yourself for progress or use celebratory language
- Stop working just because you hit a problem (persist through issues)

**Do:**
- Report specific results when tasks complete
- Keep moving forward through challenges
- Focus on the current task, not past accomplishments

## Incremental Development & Commits

**Commit frequently as you make progress:**

- Make small, frequent commits as you accumulate verified working pieces
- **Verified means tested and working** (ideally with Playwright if available)
- Clearly label commits: "Add basic counter functionality"
- Slice work into small chunks that can be continuously extended
- Check in working pieces incrementally rather than waiting for complete features
- Each commit should represent a working increment

**Example commit flow:**
```bash
# After getting basic pattern working
git add patterns/$GITHUB_USER/WIP/my-pattern.tsx
git commit -m "Add basic counter pattern structure"

# After adding features
git commit -m "Add increment/decrement buttons"

# After testing
git commit -m "Test counter pattern in browser"
```

## Managing Dev Servers

**You can restart both dev servers whenever needed:**

```bash
# Stop both servers
pkill -f "packages/toolshed.*deno task dev"
pkill -f "packages/shell.*deno task dev-local"

# Start both servers
cd ~/Code/labs/packages/toolshed && deno task dev > /tmp/toolshed-dev.log 2>&1 &
cd ~/Code/labs/packages/shell && deno task dev-local > /tmp/shell-dev.log 2>&1 &
sleep 3

echo "Both servers restarted"
```

**When to restart:**
- After pulling labs updates
- If patterns aren't deploying correctly
- If you see connection errors to localhost:8000 or localhost:5173
- User reports something not working

**Both servers run in background** - session can continue while they start

**Check server logs if issues occur:**
- Toolshed: `/tmp/toolshed-dev.log`
- Shell: `/tmp/shell-dev.log`

## Debugging with `<ct-cell-context>`

`<ct-cell-context>` is a debugging tool that annotates regions of the page with cell data. It's better than sprinkling `console.log` everywhere because inspection is conditional—users can watch and unwatch values on demand.

**When to use (sparingly, typically 1-2 per pattern):**
- Important values that are otherwise difficult to access
- Intermediate calculations or API responses
- Values you'd otherwise debug with `console.log`

**Usage:**
```tsx
<ct-cell-context $cell={result} label="Calculation Result">
  <div>{result.value}</div>
</ct-cell-context>
```

**API:**
- `$cell` - The Cell to associate with this region
- `label` - Human-readable name shown in the toolbar (optional)
- `inline` - Display as inline-block instead of block (optional)

**How to inspect:**
Hold **Alt** and hover over a cell context region to see the debugging toolbar:
- **val** - Log the cell value to console and set `globalThis.$cell` to the cell (like Chrome's `$0` for elements)
- **id** - Log the cell's full address
- **watch/unwatch** - Subscribe to value changes; updates appear in the debugger's Watch List

**When NOT to use:**
- Don't wrap every cell—reserve for important values
- Don't use for trivial or obviously-accessible values
- If a value is already easy to inspect via the UI, you probably don't need this

**Note:** Every `[UI]` render is automatically wrapped in `ct-cell-context`, so you get top-level piece debugging for free.

## Working with labs Repository

❌ **NEVER commit or push to labs** - it's READ-ONLY
✅ **If you accidentally changed something**: `git restore .`
✅ **To update labs**: Pull updates and restart dev server automatically

## Deleting Space Databases - DANGEROUS

**⚠️ ONLY delete with explicit user confirmation**

Location: `~/Code/labs/packages/toolshed/cache/memory/*.sqlite`

**WARNING: Deleting these files wipes out ALL local spaces permanently**
- All charms, data, and work in all spaces will be lost
- This affects all test spaces across all sessions

**When this might be needed:**
- Fixing corrupted spaces
- Testing fresh installs
- Clearing test data completely
- User explicitly says "delete all my spaces"

**Command:**
```bash
rm -rf ~/Code/labs/packages/toolshed/cache/memory/*.sqlite
```

**NEVER do this without explicit user permission**

## Optional Defaults Idiom for Pattern Instantiation

When one pattern needs to instantiate another (like page-creator launching new patterns), use the **optional defaults idiom** with `field?: Default<T, V>`.


### The Problem

Without defaults, callers must provide ALL Input fields:

```typescript
// ❌ FRAGILE - Must list every field, breaks when Input changes
navigateTo(Person({
  displayName: "",
  givenName: "",
  familyName: "",
  // ... 10 more fields that must be kept in sync
}));
```

### The Solution: Optional Defaults

Add `?` to Input fields that have `Default<T, V>`:

```typescript
// In person.tsx
type Input = {
  displayName?: Default<string, "">;    // Optional for callers
  givenName?: Default<string, "">;      // Optional for callers
  birthday?: Default<string, "">;       // Optional for callers
  emails?: Default<EmailEntry[], []>;   // Optional for callers
};

export default pattern<Input, Output>(({ displayName, givenName, ... }) => {
  // Inside the pattern body, ALL fields are guaranteed present
  // Required<Input> removes the `?`, Default<> provides values
  return { ... };
});
```

### Why This Works

**Type Flow:**
1. `Input` has `field?: Default<T, V>` - optional for callers
2. `PatternFunction<Input, Output>` wraps internal type with `Required<Input>`
3. Inside pattern body, fields are guaranteed present (Required removes `?`)
4. Callers see `StripCell<Input>` which preserves the `?`

**Result:**
- ✅ Callers can use `Pattern({})` - all defaults applied
- ✅ Callers can override specific fields: `Pattern({ title: "Custom" })`
- ✅ Pattern body has full access to all fields (no undefined checks)

### Usage in Other Patterns

```typescript
// In page-creator.tsx
import Person from "./person.tsx";

const createPersonHandler = handler<void, void>(() => {
  return navigateTo(Person({}));  // Clean! All defaults applied
});

// Or with overrides:
navigateTo(Person({ givenName: "Alice" }));
```

### Important Notes

- **Add `?` to EVERY field with `Default<>`** - this makes it optional for callers
- **Inside the pattern body**, fields are always present (Required<> removes `?`)
- **No factory functions needed** - import pattern directly and call with `{}`
- **Type checking still works** - invalid field names or types are caught

## Updating the Pattern README

**IMPORTANT:** When creating or significantly modifying patterns, update `patterns/$GITHUB_USER/README.md`.

The README serves as an index of all patterns with descriptions of what they do and what's interesting about them.

**When to update:**
- Creating a new pattern (add to appropriate section)
- Moving a WIP pattern to stable (move entry from WIP to stable section)
- Significantly changing a pattern's functionality (update description)
- Adding interesting new features to a pattern (add to "Interesting features" list)

**What to include:**
- Pattern filename with brief description
- "Interesting features" bullet points highlighting notable techniques
- Placement in appropriate category (Meal Planning, Security, Developer Tools, etc.)

**Example entry:**
```markdown
#### `my-pattern.tsx`
Brief description of what it does.

**Interesting features:**
- Notable technique or framework feature demonstrated
- Unique functionality worth highlighting
```

## Additional Development Skills

For specific workflows, use these skills:
- **deployment** - Deploy and update patterns
- **testing** - Test patterns with Playwright
- **recovery-strategies** - What to do when stuck
- **git-workflow** - Git operations and PRs
- **todo-files** - Manage TODO files for complex patterns
- **land-branch** - Land feature branches (includes README verification)

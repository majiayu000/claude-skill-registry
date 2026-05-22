---
name: code-alignment
description: Assess uncommitted code changes for alignment with existing codebase patterns, architecture, and conventions. Use before committing to catch foreign patterns, missed reuse opportunities, and style inconsistencies. Triggers on phrases like "check my changes", "review uncommitted", "assess fit", "pattern check", "code alignment", or "pre-commit review".
---

# Code Alignment

Assess uncommitted code changes against the existing codebase to ensure consistency with established patterns, architecture, components, and ways of working.

## When to use

- Before committing new code
- When adding new features or components
- After refactoring to verify consistency
- When onboarding and unsure if code follows project conventions

## Instructions

### Step 1: Gather uncommitted changes

First, identify what has changed:

```bash
git status
git diff --stat
git diff
git diff --cached  # for staged changes
```

Focus on:
- New files being added
- Modified files
- The nature of changes (new component, utility, service, etc.)

### Step 2: Understand the existing codebase

Before assessing, build context on existing patterns by exploring:

1. **Project structure**: How are files and folders organized?
2. **Naming conventions**: How are files, functions, variables, components named?
3. **Import patterns**: How are dependencies imported and organized?
4. **Code organization**: How is code structured within files?
5. **Existing utilities**: What helpers, hooks, services already exist?
6. **Component patterns**: How are similar components built?
7. **Error handling**: How are errors handled throughout?
8. **Testing patterns**: How are tests structured?

Use targeted exploration:
- Look at sibling files in the same directory
- Find similar existing implementations
- Check for shared utilities that could be reused

### Step 3: Assess alignment

Evaluate the uncommitted changes against these dimensions:

#### A. Code Style & Conventions
- Naming conventions (files, functions, variables, classes)
- Code formatting and structure
- Comment style and documentation patterns
- Import organization and grouping

#### B. Architectural Patterns
- File placement (is it in the right directory?)
- Module boundaries and responsibilities
- Dependency direction (does it respect existing layers?)
- Service/component granularity

#### C. Reuse Opportunities
- Existing utilities that could replace custom code
- Shared components that could be leveraged
- Common patterns that should be followed
- DRY violations (reimplementing existing functionality)

#### D. Consistency
- Error handling approach
- Logging patterns
- State management conventions
- API/data fetching patterns
- Testing approach

### Step 4: Generate report

Produce a structured report with these sections:

```markdown
## Code Alignment Report

### Summary
[One paragraph overview: is the code well-aligned, partially aligned, or introducing foreign patterns?]

### Findings

#### Aligned Well
- [Things that match existing patterns]

#### Concerns
- [Pattern deviations with severity: minor/moderate/significant]
- [Include file:line references where relevant]

#### Reuse Opportunities
- [Existing utilities/components that could be leveraged]
- [Include paths to existing code]

#### Quick Wins
- [Simple changes that would improve alignment]
- [Mark with estimated effort: trivial/small/medium]

### Recommendations
[Prioritized list of suggested changes]
```

### Step 5: Handle user commands

**Default**: Display report in chat

**"Write to file"**: Write the report to a markdown file
```bash
# Suggest path like: .claude/reports/code-alignment-YYYY-MM-DD.md
# Or project-appropriate location
```

**"Execute quick wins"**: Implement the trivial/small effort fixes automatically
- Only execute changes marked as "trivial" or "small" effort
- Show each change before making it
- Skip anything that requires user judgment

## Assessment criteria by category

### File & Folder Patterns
- Does the file live where similar files live?
- Does the filename follow the same convention as peers?
- Is the folder structure consistent with the project?

### Naming Patterns
- Variables: camelCase, snake_case, PascalCase - match the project
- Functions: verb-first, descriptive, consistent with similar functions
- Components: match existing component naming
- Files: match adjacent file naming patterns

### Code Structure Patterns
- Function length and complexity (match existing norms)
- Class vs functional approaches (match project preference)
- Export patterns (default vs named, barrel files)
- Code organization within files

### Import Patterns
- Grouping (stdlib, external, internal, relative)
- Aliasing conventions
- Barrel imports vs direct imports

### Error Handling
- Try/catch patterns
- Error types and messages
- Logging on errors
- User-facing error handling

### Testing Patterns
- Test file location and naming
- Test structure (describe/it, test functions)
- Mocking approaches
- Assertion styles

## Example report

```markdown
## Code Alignment Report

### Summary
The new `UserCard` component is mostly well-aligned but introduces a custom date formatting utility when the project already has `lib/utils/formatDate.ts`. Minor naming inconsistency in props interface.

### Findings

#### Aligned Well
- File location in `components/users/` follows existing pattern
- Component structure matches other card components
- Uses existing `Card` base component
- Error handling follows established pattern

#### Concerns
- **Moderate**: Custom `formatUserDate()` function duplicates `lib/utils/formatDate.ts`
- **Minor**: Props interface named `Props` instead of `UserCardProps` (project convention is `{Component}Props`)
- **Minor**: Import groups not separated by blank lines (see `components/users/UserList.tsx` for reference)

#### Reuse Opportunities
- `lib/utils/formatDate.ts` - use instead of custom date formatting
- `hooks/useUserData.ts` - could replace manual fetch logic
- `components/common/Avatar.tsx` - exists but not used

#### Quick Wins
- [trivial] Rename `Props` to `UserCardProps`
- [trivial] Add blank lines between import groups
- [small] Replace custom date formatting with `formatDate()`

### Recommendations
1. Replace custom `formatUserDate()` with existing `formatDate()` utility
2. Consider using `useUserData` hook for data fetching consistency
3. Rename props interface to follow `{Component}Props` convention
```

## Best practices

1. **Be specific**: Reference actual file paths and line numbers
2. **Prioritize**: Not all inconsistencies are equal - highlight what matters
3. **Show examples**: Point to existing code as reference
4. **Stay objective**: Report facts, not opinions on code quality
5. **Consider context**: New patterns might be intentional improvements
6. **Quick wins first**: Identify easy alignment fixes separately from larger refactors

## Limitations

- Cannot assess runtime behavior or performance implications
- May miss project-specific conventions not evident in code
- Best used alongside human judgment, not as final arbiter
- Large changesets may require focusing on most impactful files

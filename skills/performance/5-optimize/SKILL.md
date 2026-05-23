---
name: optimize
description: Optimize your SaaS app across four dimensions - Speed (page load, API response), Code (unused files, dead code), Database (orphaned data, schema hygiene), and Dependencies (package bloat, bundle size). Use when app feels slow, codebase feels bloated, or after significant development work accumulates. Each path follows AUDIT → CLEAN → PREVENT workflow.
---

# Optimize

Reduce waste and improve efficiency across four dimensions.

## Choose Your Path

**Speed** → Pages slow, APIs timeout, sluggish UX
**Code** → Bloated codebase, unused files, redundant components
**Database** → Orphaned data, unused fields/tables, slow queries
**Dependencies** → Package bloat, large bundles, outdated libraries

---

## When to Optimize

**Optimize when:**
- App feels slow (Speed)
- Codebase has grown significantly (Code)
- Database has accumulated cruft (Database)
- Bundle size is large or security warnings appear (Dependencies)

**Don't optimize when:**
- Building MVP
- < 100 users
- Everything works fine

**Rule:** Make it work, then make it lean.

---

## Speed Optimization

Make your app fast and responsive.

### Targets

| Metric | Good | Bad |
|--------|------|-----|
| Page load | < 3s | > 5s |
| API response | < 500ms | > 1s |
| Time to interactive | < 5s | > 8s |
| Database query | < 100ms | > 500ms |

### AUDIT

Identify what's slow.

**Tell AI:**
```
Audit app performance:
- Measure page load times
- Log API response times
- Identify slow database queries
- Check bundle size
Report findings with specific numbers.
```

**Quick manual check:**
- Chrome DevTools → Network tab → Reload → Check "Load" time
- Chrome DevTools → Network tab → Click action → Check API time

### CLEAN

Fix identified issues.

**Tell AI:**
```
Optimize these performance issues:
[paste audit findings]

Apply fixes:
- Add caching for slow API calls
- Add database indexes for slow queries
- Optimize/lazy-load images
- Code split large bundles
```

### PREVENT

Stop future slowdowns.

**Tell AI:**
```
Add performance monitoring:
- Log API calls > 500ms
- Log database queries > 100ms
- Alert on page load > 3s
- Track bundle size in CI
```

See [PERFORMANCE-CHECKS.md](PERFORMANCE-CHECKS.md) for testing methods.
See [OPTIMIZATION-PROMPTS.md](OPTIMIZATION-PROMPTS.md) for specific patterns.

---

## Code Optimization

Remove unused code and reduce complexity.

### Signs You Need This

- Files you don't recognize
- Components that aren't used anywhere
- Multiple versions of similar code
- "I'm afraid to delete this"

### AUDIT

Find unused code.

**Tell AI:**
```
Audit codebase for unused code:
- Find components not imported anywhere
- Find functions never called
- Find files not referenced
- Find duplicate/similar code
- Find commented-out code blocks

List each with file path and last modified date.
```

**What to look for:**
- Dead components (created during iteration, never used)
- Orphaned utilities (helper functions nothing calls)
- Abandoned features (half-built, never finished)
- Copy-paste duplication (same logic in multiple places)

### CLEAN

Remove identified waste.

**Tell AI:**
```
Remove this unused code:
[paste audit findings]

Before deleting:
- Verify nothing imports/calls it
- Check git history for context
- Remove related tests if any

After deleting:
- Run build to verify no breaks
- Run tests to verify no breaks
```

**Safety rule:** If unsure, comment out first and test. Delete after confirming nothing breaks.

### PREVENT

Stop code accumulation.

**Tell AI:**
```
Set up code hygiene practices:
- Add ESLint rule for unused imports
- Add ESLint rule for unused variables
- Configure IDE to highlight unused code
- Add CI check for unused exports
```

See [CODE.md](CODE.md) for detailed patterns.

---

## Database Optimization

Clean up data schema and orphaned records.

### Signs You Need This

- Tables you don't recognize
- Fields that are always null
- Queries getting slower over time
- "What is this table for?"

### AUDIT

Find database waste.

**Tell AI:**
```
Audit database for cleanup opportunities:
- Tables with no recent reads/writes
- Columns that are always NULL or empty
- Orphaned records (foreign keys pointing to deleted rows)
- Duplicate data across tables
- Missing indexes on frequently queried fields

List each with table name, row count, and last access if available.
```

**What to look for:**
- Abandoned feature tables (feature removed, table remains)
- Legacy columns (renamed but old column kept)
- Orphaned records (user deleted, their data remains)
- Redundant data (same info stored multiple places)

### CLEAN

Remove identified waste.

**Tell AI:**
```
Clean up database:
[paste audit findings]

Before removing:
- Backup affected tables
- Verify no code references removed tables/columns
- Check for foreign key constraints

Migration steps:
- Create migration to drop unused columns
- Create migration to drop unused tables
- Create script to delete orphaned records
- Add missing indexes
```

**Safety rule:** Always backup before schema changes. Test on staging first.

### PREVENT

Stop data accumulation.

**Tell AI:**
```
Set up database hygiene:
- Add ON DELETE CASCADE for dependent records
- Add NOT NULL constraints where appropriate
- Create cleanup job for soft-deleted records (>90 days)
- Add monitoring for table size growth
```

See [DATABASE.md](DATABASE.md) for detailed patterns.

---

## Dependencies Optimization

Reduce package bloat and bundle size.

### Signs You Need This

- `npm install` takes forever
- Bundle size > 500KB
- Security vulnerability warnings
- "What does this package do?"

### AUDIT

Find dependency waste.

**Tell AI:**
```
Audit dependencies:
- List packages not imported anywhere in code
- List packages with security vulnerabilities
- List packages with major version updates available
- Analyze bundle size by package
- Find duplicate packages (different versions of same thing)

Report: package name, size impact, last used, and recommendation.
```

**Quick manual check:**
```bash
# Check bundle size
npm run build

# Check for unused packages
npx depcheck

# Check for vulnerabilities
npm audit

# Check for outdated packages
npm outdated
```

### CLEAN

Remove identified waste.

**Tell AI:**
```
Clean up dependencies:
[paste audit findings]

Steps:
- Remove unused packages from package.json
- Update packages with security vulnerabilities
- Replace heavy packages with lighter alternatives
- Remove duplicate package versions

After changes:
- Delete node_modules and package-lock.json
- Fresh npm install
- Run build and tests
```

**Common replacements:**
| Heavy | Light Alternative |
|-------|-------------------|
| moment.js | date-fns or dayjs |
| lodash (full) | lodash-es (tree-shakeable) |
| axios | fetch (built-in) |

### PREVENT

Stop dependency bloat.

**Tell AI:**
```
Set up dependency hygiene:
- Add bundle size check to CI (fail if > X KB)
- Add npm audit to CI pipeline
- Configure Dependabot for security updates
- Add depcheck to pre-commit hook
```

See [DEPENDENCIES.md](DEPENDENCIES.md) for detailed patterns.

---

## Optimization Priority

**When everything needs work:**

1. **Speed** - Users feel this immediately
2. **Dependencies** - Security vulnerabilities are urgent
3. **Database** - Affects long-term performance
4. **Code** - Affects maintainability, not users

**Quick wins per category:**

| Category | Quick Win |
|----------|-----------|
| Speed | Add caching to slowest API endpoint |
| Code | Delete obviously dead files |
| Database | Add indexes to slow queries |
| Dependencies | Remove unused packages |

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Optimizing before measuring | AUDIT first, always |
| Deleting code without checking | Verify no references before removing |
| Dropping database columns in production | Test migrations on staging |
| Updating all packages at once | Update one at a time, test each |
| Premature optimization | Wait until there's actual waste to clean |

---

## Success Looks Like

✅ Pages load < 3 seconds
✅ No unused code in codebase
✅ No orphaned data in database
✅ No unused dependencies
✅ Bundle size < 200KB (React apps)
✅ Zero security vulnerabilities
✅ Automated checks prevent future waste

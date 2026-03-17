---
name: migrating-to-db
version: 1.0.0
description: >
  Expert guidance for migrating Logseq graphs from Markdown (MD) format to the new Database (DB)
  format. Auto-invokes when users ask about MD to DB migration, converting graphs, import options,
  data transformation, or compatibility between Logseq versions. Covers migration strategies,
  common issues, and best practices.
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Migrating to Logseq DB

## When to Use This Skill

This skill auto-invokes when:
- User asks about migrating from Logseq MD to DB version
- Converting markdown graphs to database format
- Import/export between Logseq versions
- Questions about what transfers during migration
- Namespace handling during migration
- Tag-to-class conversion decisions
- Property type inference during import
- User mentions "migrate", "convert", "MD to DB", "markdown to database"

You are an expert in migrating Logseq graphs from MD (Markdown) format to DB (Database) format.

## Migration Overview

### Why Migrate?

| Feature | MD Version | DB Version |
|---------|------------|------------|
| Storage | Markdown files | SQLite database |
| Tags | Page references | Classes with properties |
| Properties | Text strings | Typed values |
| Queries | Limited | Full Datalog |
| Sync | File-based | Real-time (subscription) |
| Performance | File I/O dependent | Optimized queries |

### Current Status (2024-2025)

**Important**: Logseq DB is still in **alpha**. Consider:
- Data loss risk exists
- Some features not yet available (whiteboards)
- Plugin compatibility varies
- Requires subscription for sync

## Pre-Migration Checklist

Before migrating, assess your graph:

### 1. Backup Everything
```bash
# Create timestamped backup
cp -r ~/logseq/my-graph ~/logseq/my-graph-backup-$(date +%Y%m%d)

# Or compress
tar -czvf my-graph-backup.tar.gz ~/logseq/my-graph
```

### 2. Audit Current Structure

**Pages to review:**
- [ ] Namespaced pages (a/b/c) → May become separate pages
- [ ] Pages with same name, different namespaces
- [ ] Template pages
- [ ] Query pages

**Properties to review:**
- [ ] Property formats (key:: value)
- [ ] Multi-value properties
- [ ] Date properties
- [ ] Linked properties ([[page]])

**Tags to review:**
- [ ] Simple tags (#tag)
- [ ] Page tags ([[tag]])
- [ ] Nested tags (#parent/child)

### 3. Identify Migration Decisions

| MD Pattern | DB Options | Decision Needed |
|------------|------------|-----------------|
| `#tag` | Class or page ref | Which tags become classes? |
| `[[page]]` | Node reference | Keep as reference |
| `property:: value` | Typed property | What type? |
| `namespace/page` | Separate page or hierarchy | Flatten or nest? |

## Migration Process

### Step 1: Export from MD Version

1. Open your MD graph in Logseq
2. Go to **Settings** → **Export**
3. Choose **Export to EDN** (for full data)
4. Save the export file

### Step 2: Prepare Import Settings

When importing to DB, you'll choose:

**Tag Handling:**
- **Convert to classes**: Tags become proper classes with inherited properties
- **Keep as references**: Tags remain simple page links

**Namespace Handling:**
- **Flatten**: `a/b/c` → single page "a/b/c"
- **Hierarchical**: Creates page hierarchy

**Property Handling:**
- **Infer types**: Logseq guesses types (number, date, etc.)
- **All as text**: Everything stays as strings

### Step 3: Create New DB Graph

1. Create new DB-based graph in Logseq
2. Use **Import** feature
3. Select your exported data
4. Configure migration options
5. Review and confirm

### Step 4: Post-Migration Validation

```clojure
;; Check page count matches
[:find (count ?p)
 :where [?p :block/tags ?t]
        [?t :db/ident :logseq.class/Page]]

;; Check for orphaned blocks
[:find (pull ?b [:block/title])
 :where [?b :block/title _]
        (not [?b :block/page _])
        (not [?b :block/tags ?t]
             [?t :db/ident :logseq.class/Page])]

;; Verify properties migrated
[:find ?prop-name (count ?b)
 :where [?b ?prop _]
        [?p :db/ident ?prop]
        [?p :block/title ?prop-name]
        [(clojure.string/starts-with? (str ?prop) ":user.property")]]
```

## Common Migration Issues

### Issue 1: Lost Property Types

**Symptom**: Numbers/dates stored as strings

**Solution**: Manually update property types
```clojure
;; In DB, update property type
{:db/ident :user.property/rating
 :logseq.property/type :number}  ; was :default
```

### Issue 2: Tag/Class Confusion

**Symptom**: Tags didn't become proper classes

**Solution**: Convert pages to classes
1. Open the tag page
2. Add `#Tag` to make it a class
3. Define properties on the class

### Issue 3: Broken References

**Symptom**: `[[page]]` links not working

**Cause**: Page names changed during migration

**Solution**: Use find/replace or query to identify broken refs
```clojure
[:find ?ref-text
 :where
 [?b :block/title ?title]
 [(re-find #"\[\[.*?\]\]" ?title) ?ref-text]
 (not [_ :block/title ?ref-text])]
```

### Issue 4: Namespace Flattening

**Symptom**: `project/tasks` and `project/notes` merged

**Solution**: Pre-migration, rename pages to avoid conflicts

### Issue 5: Query Compatibility

**Symptom**: Old queries don't work

**Reason**: Different attribute names

| MD Attribute | DB Attribute |
|--------------|--------------|
| `:block/content` | `:block/title` |
| `:block/name` | `:block/title` |
| `:page/tags` | `:block/tags` |

## Migration Strategies

### Strategy 1: Big Bang Migration

- Migrate entire graph at once
- Best for: Small graphs, simple structure
- Risk: All-or-nothing

### Strategy 2: Parallel Operation

- Keep MD graph active
- Create DB graph for new content
- Gradually move old content
- Best for: Large graphs, active use

### Strategy 3: Selective Migration

- Export specific pages/areas
- Import into new DB graph
- Best for: Messy graphs needing cleanup

## Best Practices

### Before Migration

1. **Clean up your graph**
   - Remove unused pages
   - Standardize property names
   - Fix broken links

2. **Document your structure**
   - List all tags and their purposes
   - Document property meanings
   - Map namespaces

3. **Plan your classes**
   - Which tags become classes?
   - What properties do they need?
   - Define inheritance hierarchy

### During Migration

1. **Start small** - Test with a subset
2. **Compare counts** - Pages, blocks, properties
3. **Check critical pages** - Most important content first
4. **Verify queries** - Update and test all queries

### After Migration

1. **Don't delete MD graph** - Keep as backup
2. **Monitor for issues** - Note problems for feedback
3. **Update workflows** - Adapt to new features
4. **Explore new capabilities** - Classes, typed properties

## Feature Comparison

### Available in DB Version
- ✅ Typed properties (number, date, checkbox)
- ✅ Class inheritance
- ✅ Property schemas
- ✅ Full Datalog queries
- ✅ Real-time collaboration (Pro)
- ✅ Library view

### Not Yet Available (Alpha)
- ⏳ Whiteboards
- ⏳ Some plugins
- ⏳ Full export options
- ⏳ Advanced templates

### Different Behavior
- 📝 Tags = Classes (more powerful but different)
- 📝 Sync requires subscription
- 📝 File access limited (SQLite, not .md)

## Resources

- [Logseq DB Documentation](https://github.com/logseq/docs/blob/master/db-version.md)
- [DB Unofficial FAQ](https://discuss.logseq.com/t/logseq-db-unofficial-faq/32508)
- [Migration Feedback Thread](https://discuss.logseq.com/t/logseq-db-changelog/30013)

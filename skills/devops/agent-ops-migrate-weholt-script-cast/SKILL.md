---
name: agent-ops-migrate
description: "Migrate a project into another, ensuring functionality and validating complete content transfer. Use for monorepo consolidation, template upgrades, or codebase mergers."
category: utility
invokes: [agent-ops-project-sections, agent-ops-baseline, agent-ops-validation, agent-ops-interview]
invoked_by: [User request]
state_files:
  read: [focus.md, constitution.md, baseline.md]
  write: [focus.md]
---

# Project Migration Workflow

## Purpose

Migrate code, configuration, and content from a source project into a target project while:

- Ensuring the target project works after migration
- Validating all content has been transferred
- Handling conflicts and incompatibilities
- Providing rollback capability if issues arise

## When to Use

- Consolidating multiple projects into a monorepo
- Upgrading from an old project template to a new one
- Merging two codebases
- Moving functionality between projects
- Adopting a new framework while preserving logic

## Migration Types

| Type | Description | Complexity |
|------|-------------|------------|
| **Full merge** | Entire source → target | High |
| **Selective** | Specific modules/features only | Medium |
| **Template upgrade** | Apply new template, preserve custom code | Medium |
| **Framework migration** | Change underlying framework | High |
| **Monorepo consolidation** | Multiple repos → single repo | High |

## Procedure

### Phase 1: Pre-Migration Analysis

1. **Scan source project** using `agent-ops-project-sections`:
   - Identify all sections and their dependencies
   - Map file structure
   - Identify configuration files
   - Note external dependencies

2. **Scan target project** (if exists):
   - Identify existing structure
   - Note potential conflicts
   - Check compatibility

3. **Create migration manifest**:
   ```yaml
   migration:
     source: /path/to/source
     target: /path/to/target
     type: full_merge | selective | template_upgrade
     
   sections:
     - name: api
       source_path: src/api/
       target_path: src/api/
       action: copy | merge | skip
       
     - name: config
       source_path: config/
       target_path: config/
       action: merge
       conflicts: [.env, settings.py]
   ```

### Phase 2: Dependency Analysis

1. **Compare dependency files**:
   - `package.json` vs `package.json`
   - `pyproject.toml` vs `pyproject.toml`
   - `*.csproj` vs `*.csproj`

2. **Identify conflicts**:
   - Version mismatches
   - Incompatible packages
   - Missing dependencies

3. **Create dependency resolution plan**:
   ```markdown
   ## Dependency Conflicts
   
   | Package | Source Ver | Target Ver | Resolution |
   |---------|------------|------------|------------|
   | lodash | 4.17.21 | 4.17.15 | Use source (newer) |
   | react | 17.0.2 | 18.2.0 | Use target (newer) |
   | custom-lib | 1.0.0 | — | Add to target |
   ```

### Phase 3: Conflict Resolution

For each identified conflict:

1. **File conflicts** (same path, different content):
   - Compare files
   - Determine merge strategy: source wins / target wins / manual merge
   - Create backup of target version

2. **Naming conflicts**:
   - Rename with prefix/suffix
   - Update all references

3. **Configuration conflicts**:
   - Merge non-overlapping settings
   - Flag overlapping settings for user decision

**Present conflicts to user**:
```
## Migration Conflicts Detected

### File Conflicts (3)
1. `src/config.ts` — Different database settings
   → [S]ource / [T]arget / [M]erge manually

2. `package.json` — Different scripts
   → [S]ource / [T]arget / [M]erge manually

3. `.env.example` — Different variables
   → [S]ource / [T]arget / [M]erge manually

### Dependency Conflicts (2)
1. lodash: 4.17.21 (source) vs 4.17.15 (target)
   → Using source version (newer)

2. typescript: 4.9.5 (source) vs 5.0.0 (target)
   → Using target version (newer)

Proceed with these resolutions? [Y]es / [E]dit / [C]ancel
```

### Phase 4: Baseline Capture

Before any migration:

1. **Capture target baseline** (if target exists):
   - Run build
   - Run tests
   - Record state

2. **Document pre-migration state**:
   ```markdown
   ## Pre-Migration Baseline
   
   Target: /path/to/target
   Date: YYYY-MM-DD
   
   - Build: ✅ passing
   - Tests: 142 passing, 0 failing
   - Lint: 0 errors
   
   Backup: .migration-backup/
   ```

### Phase 5: Execute Migration

Execute in order, with validation checkpoints:

1. **Create backup**:
   ```bash
   # Create timestamped backup
   cp -r target/ .migration-backup/target-YYYYMMDD-HHMMSS/
   ```

2. **Copy/merge files** per manifest:
   - Track each file operation
   - Log any errors

3. **Update imports/references**:
   - Find and replace import paths
   - Update configuration references

4. **Merge dependencies**:
   - Combine dependency files
   - Resolve versions per plan

5. **Run build** (checkpoint):
   - If fails: diagnose, fix, or rollback

6. **Run tests** (checkpoint):
   - If fails: diagnose, fix, or rollback

### Phase 6: Validation

1. **Content validation**:
   - Compare file counts source vs copied
   - Verify critical files present
   - Check for orphaned references

2. **Functionality validation**:
   - Build passes
   - Tests pass (or expected failures documented)
   - Lint passes (or expected issues documented)

3. **Generate migration report**:
   ```markdown
   ## Migration Report
   
   ### Summary
   - Files copied: 127
   - Files merged: 8
   - Files skipped: 3 (test fixtures)
   - Conflicts resolved: 5
   
   ### Build Status
   - Before: ✅ (142 tests)
   - After: ✅ (189 tests)
   
   ### New Dependencies Added
   - lodash@4.17.21
   - custom-lib@1.0.0
   
   ### Manual Follow-ups Required
   - [ ] Review merged config in src/config.ts
   - [ ] Update CI/CD pipeline for new structure
   - [ ] Update documentation
   ```

### Phase 7: Rollback (if needed)

If migration fails validation:

1. **Restore from backup**:
   ```bash
   rm -rf target/
   mv .migration-backup/target-YYYYMMDD-HHMMSS/ target/
   ```

2. **Document failure**:
   ```markdown
   ## Migration Rollback
   
   Reason: Test failures in auth module
   Restored: target/ from backup
   
   Issues to resolve before retry:
   - [ ] Incompatible auth library versions
   - [ ] Missing environment variables
   ```

3. **Create issues** for blocking problems

## Migration Manifest Schema

```yaml
migration:
  source: string  # Source project path
  target: string  # Target project path
  type: full_merge | selective | template_upgrade | framework
  created: YYYY-MM-DD
  
backup:
  enabled: true
  path: .migration-backup/
  
sections:
  - name: string
    source_path: string
    target_path: string
    action: copy | merge | skip | transform
    transform_script: string  # Optional, for framework migrations
    
dependencies:
  strategy: source_wins | target_wins | newest | manual
  overrides:
    - package: string
      version: string
      reason: string
      
conflicts:
  - file: string
    resolution: source | target | merge
    merge_notes: string
    
validation:
  build_command: string
  test_command: string
  lint_command: string
  required_files:
    - path/to/critical/file.ts
```

## Completion Criteria

- [ ] Migration manifest created
- [ ] All conflicts identified and resolved
- [ ] Backup created before migration
- [ ] All files copied/merged per manifest
- [ ] Dependencies merged successfully
- [ ] Build passes in target
- [ ] Tests pass (or failures documented)
- [ ] Migration report generated
- [ ] User confirmed migration complete

## Anti-patterns (avoid)

- ❌ Migrating without backup
- ❌ Ignoring test failures
- ❌ Overwriting target files without merge consideration
- ❌ Skipping dependency conflict resolution
- ❌ Not validating after migration
- ❌ Migrating to production without staging test

## Examples

### Example 1: Monorepo Consolidation

**Scenario**: Merge `auth-service` and `user-service` into `platform` monorepo.

```
Migration: Monorepo Consolidation

Source 1: /repos/auth-service → platform/services/auth/
Source 2: /repos/user-service → platform/services/user/

Shared dependencies moved to: platform/packages/shared/

Result:
platform/
├── services/
│   ├── auth/        # from auth-service
│   └── user/        # from user-service
├── packages/
│   └── shared/      # common code extracted
└── package.json     # workspace config
```

### Example 2: Template Upgrade

**Scenario**: Upgrade project from old create-react-app to Vite template.

```
Migration: Template Upgrade (CRA → Vite)

Preserve:
- src/components/
- src/hooks/
- src/services/
- Custom configurations

Replace:
- Build system (webpack → vite)
- Config files (react-scripts → vite.config.ts)
- Entry point structure

Transform:
- Import aliases
- Environment variable prefix (REACT_APP_ → VITE_)
```

---
name: codebase-architect
description: Skill from mmtuentertainment/PayPlan
---

---
name: codebase-architect
description: Analyze and reorganize project file structures, identify dependencies, clean technical debt, and establish architectural patterns. Use when users need to: organize messy codebases, understand file dependencies and import chains, refactor folder hierarchies, identify unused files or circular dependencies, detect cross-file connections, or establish consistent naming conventions and module boundaries for any programming language project.
---

# Codebase Architect

This skill provides comprehensive project structure analysis and reorganization capabilities for codebases of any size and language.

## Core Capabilities

- **Dependency Analysis**: Map import chains and cross-file relationships
- **Structure Assessment**: Evaluate current organization against best practices
- **Dead Code Detection**: Identify unused files, exports, and orphaned code
- **Refactoring Planning**: Generate safe migration strategies
- **Pattern Recognition**: Detect and apply architectural patterns

## Quick Start

For immediate analysis of a project:

```bash
# Basic project analysis
python scripts/analyze_structure.py --root . --output analysis_report.json

# Generate dependency graph
python scripts/dependency_mapper.py --root src --format visual

# Detect dead code
python scripts/dead_code_detector.py --root . --exclude node_modules,dist
```

## Analysis Workflow

### Phase 1: Discovery

Start with comprehensive project analysis:

```bash
# Scan project for framework and language detection
python scripts/project_scanner.py --root . --output project_scan.json

# Analyze project structure in detail
python scripts/analyze_structure.py --root . --output analysis_report.json
```

This identifies:
- Framework/library conventions (React, Vue, Django, Rails, etc.)
- Build configuration files
- Test structure
- Documentation organization

### Phase 2: Dependency Mapping

Map all file relationships:

```bash
python scripts/dependency_mapper.py --root . --output deps.json --detect-circular
```

For specific language analysis:
- **JavaScript/TypeScript**: Analyzes imports, requires, dynamic imports
- **Python**: Tracks imports, relative imports, __init__ patterns
- **Java/C#**: Namespace and package dependencies
- **Go**: Module and package imports

### Phase 3: Problem Identification

Analyze dependencies and identify issues:

```bash
# Unified issue detection (runs all checks)
python scripts/issue_detector.py --root . --output issues.json --severity all

# Or run individual checks:
python scripts/dependency_mapper.py --root . --output deps.json --detect-circular
python scripts/dead_code_detector.py --root . --exclude node_modules,dist
```

Common issues detected:
- Circular dependencies
- Deep nesting (>4 levels)
- Inconsistent naming patterns
- Misplaced files (utilities in components, etc.)
- God files (too many responsibilities)
- Orphaned code (no imports/exports)

### Phase 4: Restructuring

Generate reorganization plan:

```bash
python scripts/restructure_planner.py --root . --pattern <pattern> --output migration_plan.json
```

Available patterns:
- **feature-based**: Group by features/domains
- **mvc**: Model-View-Controller separation
- **clean**: Clean Architecture layers
- **modular**: Self-contained modules
- **ddd**: Domain-Driven Design

## Architectural Patterns

### Feature-Based Structure

Best for: Frontend applications, microservices

```
src/
├── features/
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── services/
│   │   ├── types/
│   │   └── index.ts
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       ├── services/
│       └── index.ts
├── shared/
│   ├── components/
│   ├── utils/
│   └── types/
└── core/
    ├── api/
    ├── config/
    └── constants/
```

### Clean Architecture

Best for: Enterprise applications, complex domains

```
src/
├── domain/           # Business logic
│   ├── entities/
│   ├── repositories/
│   └── use-cases/
├── application/      # Application services
│   ├── services/
│   └── dto/
├── infrastructure/   # External concerns
│   ├── database/
│   ├── api/
│   └── config/
└── presentation/     # UI layer
    ├── controllers/
    └── views/
```

### Modular Monolith

Best for: Large applications, gradual microservices migration

```
src/
├── modules/
│   ├── user/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── infrastructure/
│   │   └── module.ts
│   └── billing/
│       ├── api/
│       ├── domain/
│       └── module.ts
├── shared-kernel/
└── composition-root/
```

## Advanced Features

### Custom Rules Configuration

Create `.codebase-architect.json` in project root (see `assets/example-config.json` for full template):

```json
{
  "rules": {
    "maxNestingDepth": 4,
    "enforceBarrelExports": true,
    "namingConvention": "kebab-case",
    "forbiddenDependencies": [
      {"from": "domain/*", "to": "infrastructure/*"}
    ]
  }
}
```

### Migration Safety

Execute migrations safely with automated backups and rollback:

```bash
# Dry run to preview changes
python scripts/migrate.py --root . --plan migration_plan.json --dry-run

# Execute with automatic backup
python scripts/migrate.py --root . --plan migration_plan.json --backup

# Execute with rollback on error
python scripts/migrate.py --root . --plan migration_plan.json --rollback-on-error
```

Safety features:
- **Automatic backups** before any file operations
- **Git integration** with pre/post-operation commits
- **Dry-run mode** to preview all changes
- **Rollback capability** if errors occur
- **Import path updates** automatically handled

See [Safety System](#safety-system) section for complete safety features.

### Language-Specific Features

For detailed language-specific analysis:
- **JavaScript/TypeScript**: See references/javascript-patterns.md
- **Python**: See references/python-patterns.md
- **Java/Kotlin**: See references/jvm-patterns.md
- **Go**: See references/go-patterns.md
- **C#/.NET**: See references/dotnet-patterns.md

### Reporting

Generate comprehensive reports in HTML or Markdown:

```bash
# HTML report with visualizations
python scripts/report_generator.py \
  --format html \
  --output report \
  --structure analysis.json \
  --dependencies deps.json \
  --dead-code dead_code.json \
  --issues issues.json

# Markdown for documentation
python scripts/report_generator.py --format markdown --output ARCHITECTURE.md

# Both formats
python scripts/report_generator.py --format both --output report
```

Reports include:
- Structure metrics and file distribution
- Dependency graphs and coupling scores
- Dead code analysis with savings estimates
- Issue summaries by severity

## Best Practices

### Before Reorganizing

1. **Backup everything**: Use version control or create archive
2. **Run tests**: Ensure all tests pass before changes
3. **Document current state**: Generate architecture documentation
4. **Communicate changes**: Inform team members

### During Reorganization

1. **Incremental changes**: Move one module at a time
2. **Update imports immediately**: Use automated tools
3. **Run tests frequently**: Catch breaks early
4. **Maintain compatibility**: Keep old paths with deprecation warnings

### After Reorganization

1. **Update documentation**: README, architecture docs, onboarding
2. **Update CI/CD**: Build paths, test configurations
3. **Team training**: Share new structure and conventions
4. **Monitor for issues**: Watch for import errors, build failures

## Safety System

**⚡ NEW**: Comprehensive safety features to protect against accidental deletions and enable recovery.

### Safety Manager

Central safety system providing:
- **Timestamped backups**: Automatic `.tar.gz` archives before operations
- **Trash system**: Soft-delete to `.codebase-safety/trash/` instead of permanent deletion
- **Change tracking**: Full audit log of all operations
- **Git integration**: Automatic commits before/after operations
- **Rollback capability**: Restore from backups or trash

```bash
# Create manual backup
python scripts/safety_manager.py --root . backup --description "Before major refactor"

# List all backups
python scripts/safety_manager.py --root . list-backups

# Restore from backup
python scripts/safety_manager.py --root . restore backup_20250102_143022.tar.gz

# Move file to trash instead of deleting
python scripts/safety_manager.py --root . trash path/to/file.ts --reason "Deprecated"

# List trash contents
python scripts/safety_manager.py --root . list-trash

# Restore from trash
python scripts/safety_manager.py --root . restore-trash 20250102_143500

# Clean up old trash (30+ days)
python scripts/safety_manager.py --root . cleanup-trash --days 30

# Create pre-operation git commit
python scripts/safety_manager.py --root . git-commit "migration to feature-based"
```

### Safety Directory Structure

```
.codebase-safety/
├── backups/                    # Timestamped tar.gz archives
│   ├── backup_20250102_140000.tar.gz
│   └── backup_20250102_150000.tar.gz
├── trash/                      # Soft-deleted files
│   ├── 20250102_143000/
│   │   ├── old_file.ts
│   │   └── old_file.ts.meta.json
│   └── 20250102_144000/
├── operation_log.json          # Complete audit log
├── file_manifest.json          # File state snapshots
└── last_migration.json         # Last migration details for rollback
```

### Best Practices

1. **Always use safety features**: Never skip backups for destructive operations
2. **Review dry-run output**: Always run `--dry-run` before executing migrations
3. **Keep git clean**: Commit all changes before major refactoring
4. **Regular cleanup**: Run `cleanup-trash` monthly to free disk space
5. **Test rollback**: Verify backup/restore works before production use

## Scripts Reference

All scripts in `scripts/` directory (9 total, 3,577 lines of code):

**Analysis Scripts:**
- `analyze_structure.py`: Main structure analysis engine (378 lines)
- `dependency_mapper.py`: Maps import chains and dependencies (454 lines)
- `dead_code_detector.py`: Detects unused files and exports (540 lines)
- `issue_detector.py`: Unified issue detection aggregator (311 lines)
- `project_scanner.py`: Framework and language detection (177 lines)

**Operation Scripts:**
- `restructure_planner.py`: Generates migration plans (634 lines)
- `migrate.py`: Executes safe file reorganization (339 lines)
- `safety_manager.py`: Backup, trash, and recovery system (470 lines)

**Reporting Scripts:**
- `report_generator.py`: Creates HTML/Markdown reports (274 lines)

Run any script with `--help` for detailed options.

## Troubleshooting

### Common Issues

**Large codebases (>10k files)**: Use `--sample` flag for initial analysis
**Binary files causing errors**: Add to `--exclude` patterns
**Permission errors**: Check file permissions or run with appropriate access
**Memory issues**: Use `--stream` mode for large projects

For additional patterns and detailed examples, see references/patterns-catalog.md
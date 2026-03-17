---
name: code-migration
description: "Use when migrating codebases between frameworks, languages, versions, or platforms. Provides migration assessment patterns, planning templates, framework-specific migration examples, testing strategies, rollback procedures, and automation approaches."
---

# Code Migration

## Migration Assessment

### Complexity Factors

| Factor | Considerations |
|--------|---------------|
| Size | File count, LOC, component count |
| Architectural | Coupling, layer separation, pattern usage |
| Dependency | Third-party libs, version constraints, compatibility |
| Business Logic | Complexity of rules, domain knowledge needed |
| Data | Schema migrations, data transformations, integrity |

### Risk Patterns to Scan

```python
risk_patterns = {
    'global_state': { 'pattern': r'(global|window)\.\w+\s*=', 'severity': 'high' },
    'direct_dom': { 'pattern': r'document\.(getElementById|querySelector)', 'severity': 'medium' },
    'async_patterns': { 'pattern': r'(callback|setTimeout|setInterval)', 'severity': 'medium' },
    'deprecated_apis': { 'pattern': r'(componentWillMount|componentWillReceiveProps)', 'severity': 'high' }
}
```

## Migration Planning

**Simple Migration (complexity < 3)**:

| Phase | Duration | Tasks |
|-------|----------|-------|
| Preparation | 1 week | Setup project, install deps, configure build, setup testing |
| Core Migration | 2-3 weeks | Migrate utilities, port components, update models, migrate logic |
| Testing | 1 week | Unit, integration, performance testing, bug fixes |

**Complex Migration (complexity >= 3)**:

| Phase | Duration | Tasks |
|-------|----------|-------|
| Foundation | 2 weeks | Architecture design, PoC, tool selection, team training |
| Infrastructure | 3 weeks | Build pipeline, dev environment, core abstractions |
| Incremental | 6-8 weeks | Feature modules, adapters/bridges, dual runtime |
| Cutover | 2 weeks | Complete remaining, remove legacy, optimize, final testing |

## Framework Migration: React to Vue

```javascript
// JSX to Template conversions
template = template.replace(/className=/g, 'class=');
template = template.replace(/onClick={/g, '@click="');
template = template.replace(/{(\w+) && (.+?)}/g, '<template v-if="$1">$2</template>');
template = template.replace(/{(\w+)\.map\(.*?\)}/g, '<template v-for="...">...</template>');

// Lifecycle mapping
lifecycleMapping = {
    'componentDidMount': 'mounted',
    'componentDidUpdate': 'updated',
    'componentWillUnmount': 'beforeDestroy',
    'getDerivedStateFromProps': 'computed'
};
```

## Framework Migration: Python 2 to 3

```python
# Key transformations
'.iteritems()' -> '.items()'
'.iterkeys()' -> '.keys()'
'xrange' -> 'range'
'.has_key(' -> ' in '
'print statement' -> 'print()'
'print >> file,' -> 'print(..., file=file)'
```

## Framework Migration: REST to GraphQL

```javascript
// Map REST endpoints to GraphQL
// GET /resources -> Query { resources }
// POST /resources -> Mutation { createResource }
// PUT /resources/:id -> Mutation { updateResource }
// DELETE /resources/:id -> Mutation { deleteResource }
```

## Database: SQL to NoSQL

```python
# Design decisions for document structure
for rel in relationships:
    if rel['type'] == 'one-to-one' or should_embed(rel):
        # Embed related data in document
        structure['embedded'].append(rel)
    else:
        # Store reference (foreign key equivalent)
        structure['references'].append(rel)

# Batch migration pattern
async def migrate_table(table, mapping):
    async for batch in read_in_batches(table, batch_size=1000):
        documents = [transform_row_to_document(row, mapping) for row in batch]
        await nosql[mapping['collection']].insert_many(documents)
```

## Rollback Triggers

| Condition | Threshold | Detection |
|-----------|-----------|-----------|
| Critical functionality broken | Any P0 feature | Automated monitoring |
| Performance degradation | >50% response time increase | APM metrics |
| Data corruption | Any integrity issues | Data validation checks |
| High error rate | >5% error rate increase | Error tracking |

### Rollback by Strategy

- **Blue-Green**: Switch load balancer back to blue environment
- **Canary**: Shift traffic back to stable version
- **Feature Flag**: Toggle flag off, monitor recovery

## Key Deliverables Checklist

- [ ] Migration analysis of source codebase
- [ ] Risk assessment with mitigation strategies
- [ ] Phased migration plan with timeline
- [ ] Automated migration scripts
- [ ] Comparison tests and validation
- [ ] Rollback procedures
- [ ] Progress tracking and monitoring

## Agent Team Mode

For large codebases (>50 files affected) or multi-module migrations where independent subsystems can be migrated in parallel.

### Team Configuration

```yaml
team:
  recommended_size: 3-5
  agent_roles:
    - name: module-migrator-N
      type: general-purpose
      focus: "Migrate assigned module/subsystem independently"
      skills_loaded: ["migration:code-migration"]
    - name: migration-reviewer
      type: Explore
      focus: "Validate each migration against comparison tests and compatibility"
      skills_loaded: ["migration:code-migration", "testing:language-testing-patterns"]
  file_ownership: "by-module"
  lead_mode: "delegate"
```

### Team Workflow

1. Lead runs Migration Assessment phase — complexity analysis, dependency graph, risk patterns
2. Lead creates phased plan, assigns independent modules to module-migrator teammates
3. Each module-migrator owns their file set exclusively — no cross-module edits
4. migration-reviewer validates each completed module (tests pass, API compatibility, no regressions)
5. Lead handles integration phase — cross-module wiring, full test suite, rollback preparation

### File Ownership Example

```
module-migrator-1:
  files: src/auth/**
  constraint: Do NOT modify files outside this path

module-migrator-2:
  files: src/payments/**
  constraint: Do NOT modify files outside this path
```

### Single-Agent Fallback

Without team mode, execute all phases sequentially (default behavior). Team mode is an optional enhancement.

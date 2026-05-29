---
name: blueprints-maintenance
description: Use after modifying existing systems to update blueprint documentation. Read blueprints with read_blueprint before changes, update with write_blueprint after. Prevents documentation drift.
allowed-tools: [Read, Write, Edit, Grep, Glob, mcp__plugin_hashi-blueprints_blueprints__search_blueprints, mcp__plugin_hashi-blueprints_blueprints__read_blueprint, mcp__plugin_hashi-blueprints_blueprints__write_blueprint]
---

# Maintaining Technical Blueprints

## The Sync Problem

Documentation drifts from implementation when:

- Code changes without doc updates
- New features added without documentation
- Deprecated features remain documented
- Behavior changes aren't reflected

## Verification Process

### Before Making Changes

1. **Read existing blueprint** using MCP tools:

   ```typescript
   // Find the blueprint
   const results = await search_blueprints({ keyword: "auth" });

   // Read it to understand current documentation
   const blueprint = await read_blueprint({ name: "authentication" });
   ```

2. **Note what documentation exists**:
   - Overview accurate?
   - API documentation complete?
   - Behavior described correctly?
3. **Plan documentation updates** alongside code changes

### After Making Changes

1. **Re-read the blueprint** to verify accuracy:

   ```typescript
   const current = await read_blueprint({ name: "authentication" });
   ```

2. **Verify each section**:
   - Does Overview still describe the purpose?
   - Are all public APIs documented?
   - Is behavior description accurate?
   - Are file paths still correct?

3. **Update using MCP tool**:

   ```typescript
   await write_blueprint({
     name: "authentication",
     summary: "Updated summary if needed",
     content: updatedContent
   });
   ```

4. **Remove stale content** - outdated docs mislead

## Types of Updates

### Adding New Features

When adding functionality:

1. Update the Overview if scope expanded
2. Add new API documentation
3. Document new behavior
4. Update Related Systems if new integrations
5. Add to Files section if new files created

### Modifying Existing Features

When changing behavior:

1. Update behavior descriptions
2. Revise API documentation if signatures changed
3. Update examples if usage changed
4. Check related blueprints for impact

### Removing Features

When deprecating or removing:

1. Remove API documentation
2. Remove from behavior section
3. Update Overview if scope reduced
4. Consider keeping a "Removed" or "History" note if the change is significant

### Refactoring

When restructuring without behavior changes:

1. Update Files section with new paths
2. Update Architecture if structure changed
3. Verify examples still work
4. API documentation usually unchanged

## Documentation Debt

### Recognizing Debt

Signs blueprints need attention:

- File paths that don't exist
- Functions that aren't in the codebase
- Behavior that doesn't match reality
- Missing documentation for visible features

### Paying Down Debt

Prioritize by impact:

1. **Critical**: Public APIs with wrong docs
2. **High**: Core systems undocumented
3. **Medium**: Internal systems outdated
4. **Low**: Minor inaccuracies

## Verification Checklist

When reviewing blueprints:

```markdown
## Verification Checklist

- [ ] Overview matches current purpose
- [ ] All public APIs documented
- [ ] API signatures accurate
- [ ] Examples execute correctly
- [ ] Behavior matches implementation
- [ ] File paths exist
- [ ] No removed features documented
- [ ] Related systems links work
- [ ] No duplicate content with other blueprints
```

## Keeping Blueprints Fresh

### During Development

- Treat docs as part of the feature
- Update blueprint in same commit as code
- Review blueprint changes in code review

### Regular Maintenance

- Periodically audit blueprints vs code
- Use `/blueprints` command to regenerate
- Remove orphaned blueprint files

### Tooling Support

The hashi-blueprints hooks automatically:

- Remind you to check docs (UserPromptSubmit)
- Verify docs match changes (Stop hook)

## Anti-Patterns

### Don't

- Leave TODO comments in blueprints indefinitely
- Copy implementation details that will change
- Document external libraries (link instead)
- Keep deprecated feature docs "for reference"

### Do

- Delete stale content immediately
- Update atomically with code
- Cross-reference rather than duplicate
- Keep examples minimal but complete

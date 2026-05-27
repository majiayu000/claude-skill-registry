---
name: detect-competing-systems
description: Comprehensive detection of competing and conflicting systems in Vue 3 + TypeScript + Pinia projects. Identifies duplicate implementations, architectural conflicts, and competing logic patterns before they cause technical debt.
emoji: "🔍"
category: "analyze"
triggers: ["detect competing systems", "find duplicate code", "identify architectural conflicts", "analyze code conflicts", "find redundant implementations"]
keywords: ["architecture", "duplicate", "conflict", "refactoring", "technical debt", "vue", "typescript", "pinia", "code analysis"]
---

# 🔍 Detect Competing Systems

A comprehensive skill for identifying duplicate, conflicting, and competing systems in Vue 3 + TypeScript + Pinia projects. This skill helps detect architectural conflicts, duplicate implementations, and competing logic patterns BEFORE they cause technical debt.

## Purpose

Competing systems are multiple implementations of the same functionality that exist simultaneously in a codebase. They create maintenance burden, introduce bugs, and make the codebase difficult to understand. This skill proactively identifies these conflicts and provides consolidation recommendations.

## When to Use

Use this skill when you need to:

- **Audit codebase architecture** - Identify competing systems before refactoring
- **Review new feature implementation** - Check if new code duplicates existing patterns
- **Plan technical debt reduction** - Prioritize consolidation efforts
- **Onboard new developers** - Understand architectural patterns and conflicts
- **Prevent architectural drift** - Ensure consistent patterns across the project
- **Optimize development efficiency** - Reduce duplicate work and maintenance burden

**Specific Triggers:**
- "I think we have multiple filtering implementations"
- "Are there duplicate task management systems?"
- "Check our codebase for competing patterns"
- "We need to consolidate our state management"
- "Find all duplicate CRUD operations"
- "Identify architectural conflicts in our project"

## Coverage Areas

### Core Architecture (Required)
1. **State Management (Pinia stores)** - Duplicate stores, overlapping state management
2. **Composables & Hooks** - Multiple implementations of same reactive logic
3. **Components** - Duplicate component implementations and functionality
4. **Utility functions** - Multiple versions of same utility logic
5. **Filtering & Search systems** - Competing filtering and search implementations
6. **Calendar/Scheduling logic** - Multiple calendar implementations and date handling
7. **Drag-and-drop systems** - Competing D&D libraries and implementations
8. **Database queries & API calls** - Multiple API clients and query patterns
9. **Testing frameworks & patterns** - Mixed testing approaches and setups
10. **Framework integration points** - Inconsistent framework usage patterns

### Additional Coverage Areas (25 total)
11. **Reactive state management pattern conflicts** - Mixed reactive(), ref(), shallowReactive() patterns
12. **Side effects & lifecycle conflicts** - Multiple places fetching same data, duplicate onMounted logic
13. **Error handling pattern conflicts** - Inconsistent error handling across codebase
14. **Prop drilling vs. provide/inject conflicts** - Mixed state passing strategies
15. **Form handling pattern conflicts** - Multiple form validation and submission patterns
16. **Validation logic conflicts** - Duplicate validation rules and logic
17. **Type definition conflicts** - Same types defined in multiple places
18. **Permission/auth pattern conflicts** - Scattered authentication and authorization checks
19. **Data formatting/transformation conflicts** - Multiple formatters for same data types
20. **Async operation pattern conflicts** - Mixed promises, callbacks, and async/await patterns
21. **Constants/config duplication** - Same configuration values in multiple places
22. **Notification/toast pattern conflicts** - Multiple notification systems
23. **Data fetching timing/caching conflicts** - Inconsistent caching and refresh strategies
24. **Slot vs. prop usage conflicts** - Inconsistent content passing patterns
25. **Naming convention conflicts** - Inconsistent naming patterns across codebase

## Usage Instructions

### Basic Usage

1. **Activate the skill**: "Use the detect competing systems skill"
2. **Specify scope** (optional): "Focus on filtering systems" or "Check all conflict types"
3. **Review findings**: Examine conflict reports and recommendations
4. **Plan consolidation**: Use provided effort estimates and migration paths

### Advanced Usage

- **Pattern-specific analysis**: "Analyze reactive pattern conflicts in our stores"
- **Severity filtering**: "Show only HIGH severity competing systems"
- **Integration setup**: "Help me set up pre-commit hooks for conflict detection"
- **Custom patterns**: "Add detection for our specific authentication patterns"

### Integration Options

- **Pre-commit hooks**: Automatically detect conflicts before commits
- **ESLint rules**: Custom rules to prevent duplicate implementations
- **CI/CD pipeline**: Automated conflict detection in builds
- **VS Code extension**: Real-time conflict highlighting

## Output Format

### Conflict Report Structure

Each detected conflict includes:

```json
{
  "conflictId": "duplicate-task-stores-001",
  "type": "State Management",
  "subtype": "Duplicate Pinia Stores",
  "severity": "HIGH",
  "files": [
    {
      "path": "src/stores/TaskStore.ts",
      "lineNumbers": [15, 23, 45]
    },
    {
      "path": "src/stores/WorkflowStore.ts",
      "lineNumbers": [18, 26, 48]
    }
  ],
  "description": "Two stores managing the same task data domain with 92% code similarity",
  "patternMatch": 0.92,
  "recommendation": "Consolidate into single TaskStore with computed properties for workflow-specific views",
  "consolidationPath": [
    "Keep TaskStore as primary implementation",
    "Move WorkflowStore logic to computed properties",
    "Update all WorkflowStore imports",
    "Delete redundant WorkflowStore.ts"
  ],
  "estimatedEffort": "2-3 hours",
  "risk": "Medium",
  "impact": {
    "maintenance": "High",
    "performance": "Medium",
    "consistency": "High"
  }
}
```

### Severity Levels

- **HIGH**: Critical conflicts causing bugs, security issues, or major maintenance burden
- **MEDIUM**: Conflicts causing inconsistency, moderate maintenance overhead, or performance issues
- **LOW**: Minor inconsistencies, naming conflicts, or code quality issues

### Risk Assessment

Each conflict includes risk evaluation:
- **Breaking changes required**: YES/NO
- **Testing scope**: Components/stores affected
- **Migration complexity**: SIMPLE/MODERATE/COMPLEX
- **Rollback difficulty**: EASY/MEDIUM/HARD

## Analysis Checklist

### State Management
- [ ] Multiple stores managing same data domain
- [ ] Duplicate computed values across stores
- [ ] Overlapping action implementations
- [ ] Inconsistent state initialization
- [ ] Mixed reactive patterns (reactive vs ref vs store)

### Components
- [ ] Duplicate component implementations
- [ ] Similar functionality in different components
- [ ] Inconsistent prop/emit patterns
- [ ] Mixed slot vs prop usage for similar content
- [ ] Duplicate event handling logic

### Composables & Utilities
- [ ] Multiple implementations of same reactive logic
- [ ] Duplicate utility functions
- [ ] Similar filtering/search logic
- [ ] Competing form handling patterns
- [ ] Multiple validation implementations

### API & Data
- [ ] Multiple API clients or fetch patterns
- [ ] Duplicate database query logic
- [ ] Inconsistent caching strategies
- [ ] Competing data transformation logic
- [ ] Multiple error handling approaches

### Framework Integration
- [ ] Mixed authentication patterns
- [ ] Inconsistent routing guards
- [ ] Multiple notification systems
- [ ] Competing testing frameworks
- [ ] Mixed async/await patterns

### Code Quality
- [ ] Duplicate type definitions
- [ ] Inconsistent naming conventions
- [ ] Multiple configuration sources
- [ ] Scattered constants and magic numbers
- [ ] Inconsistent formatting patterns

## Tools and Scripts

### Analysis Engine
- `analysis-engine.js`: Core detection logic and pattern matching
- `scripts/init_skill.py`: Initialize new skill instances
- `scripts/package_skill.py`: Package skill for distribution

### Integration Tools
- `integration/eslint-config.js`: ESLint rules for conflict prevention
- `integration/pre-commit-hook.sh`: Git pre-commit hook
- `integration/vs-code-extension.json`: VS Code extension configuration

### Pattern Definitions
- `scenarios/`: JSON files defining detection patterns for each conflict type
- `conflict-patterns.json`: Master pattern library
- `exemptions.json`: Intentional patterns to ignore

## Examples and Documentation

- `examples/`: Real-world conflict examples with BAD → GOOD transformations
- `docs/`: Comprehensive documentation and configuration guides
- Case studies from typical Vue 3 projects

## Best Practices

### Prevention
1. **Code reviews**: Check for duplicate implementations during reviews
2. **Documentation**: Maintain clear architectural guidelines
3. **Pattern libraries**: Establish approved patterns for common operations
4. **Regular audits**: Schedule periodic conflict detection runs

### Consolidation
1. **Prioritize HIGH severity**: Focus on critical conflicts first
2. **Test thoroughly**: Ensure consolidated implementations work correctly
3. **Communicate changes**: Update team on pattern standardization
4. **Update documentation**: Reflect new consolidated patterns

### Maintenance
1. **Run detection regularly**: Integrate into CI/CD pipeline
2. **Update patterns**: Add new conflict types as they emerge
3. **Monitor effectiveness**: Track reduction in duplicate code
4. **Team training**: Ensure team understands approved patterns

## Success Metrics

- **Reduced duplicate code**: Measurable decrease in code similarity >80%
- **Improved consistency**: Standardized patterns across conflict categories
- **Faster development**: Less time spent maintaining duplicate implementations
- **Easier onboarding**: Clearer architecture for new team members
- **Fewer bugs**: Reduced issues from inconsistent implementations

## Limitations

- **Pattern matching**: Cannot detect semantic duplicates with low code similarity
- **Intent**: Cannot determine if similar code serves different purposes intentionally
- **External libraries**: May flag legitimate library adapter patterns
- **Performance**: Large codebases may require analysis time optimization

## Extensions

The skill can be extended with:
- **Custom patterns**: Organization-specific conflict detection rules
- **Framework support**: Additional frameworks beyond Vue 3
- **Language support**: TypeScript, JavaScript, and other languages
- **Integration hooks**: Additional IDE and toolchain integrations

---

**Version**: 2.0.0
**Last Updated**: 2025-11-28
**Framework Support**: Vue 3.4+, TypeScript 5.0+, Pinia 2.0+
**Project**: PomoFlow-compatible with adaptations for any Vue 3 project
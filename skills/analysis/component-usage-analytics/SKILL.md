---
name: Component Usage Analytics
description: Use this skill when users mention "component usage", "where is this component used", "deprecate component", "migration impact", "component analytics", or want to track and analyze component usage across the codebase with deprecation planning and migration impact analysis.
version: 1.0.0
---

# Component Usage Analytics

## Overview

Track component usage across your codebase to make data-driven decisions about deprecation, refactoring, and component library management.

**Key Use Cases:**
- Find all usages of a component
- Analyze impact of breaking changes
- Plan component deprecations
- Track adoption of new components
- Identify unused components

## When to Use This Skill

Trigger this skill when the user:
- Asks "where is this component used?"
- Wants to "deprecate a component" or "plan a migration"
- Mentions "component analytics" or "usage tracking"
- Asks about "which components are unused"
- Wants to "analyze breaking change impact"
- Needs to "track component adoption"

## Core Capabilities

### 1. Usage Analysis

Find all component usages with context:

```bash
$ npm run analyze:usage Button

Analyzing Button component...

📊 Usage Report:

Total Usages: 52 imports across 47 files

By Feature:
  - Dashboard: 15 usages (8 files)
  - Settings: 12 usages (7 files)
  - Profile: 8 usages (5 files)
  - Auth: 7 usages (4 files)
  - Admin: 10 usages (23 files)

By Variant:
  - Primary: 34 usages (65%)
  - Secondary: 13 usages (25%)
  - Outline: 5 usages (10%)

Recent Changes:
  - Button@v2 released 14 days ago
  - 8 files still using Button@v1 (deprecated)
  - Migration progress: 83% (44/52 files)

Top Users (files with most usages):
  1. src/features/Dashboard/widgets.tsx (6 usages)
  2. src/features/Settings/preferences.tsx (4 usages)
  3. src/features/Profile/edit.tsx (3 usages)
```

### 2. Deprecation Planning

Analyze impact before deprecating:

```bash
$ npm run analyze:deprecate Button@v1

⚠️ Deprecation Impact Analysis: Button@v1

Current Usage:
  - 8 files still using v1
  - 12 total usages
  - Across 3 features

Migration Effort:
  Low effort: 5 files (simple props update)
  Medium effort: 2 files (variant renamed)
  High effort: 1 file (custom styling conflicts)

Breaking Changes in v2:
  1. 'success' variant removed → use 'primary' with success color
  2. 'loading' prop renamed → use 'pending' prop
  3. 'icon' prop now requires IconComponent type

Estimated Migration Time:
  - Low effort files: 30 mins total (6 mins each)
  - Medium effort files: 1 hour total (30 mins each)
  - High effort file: 2 hours (complex refactor)
  Total: ~3.5 hours

Recommendations:
  1. Create migration guide for developers
  2. Add deprecation warnings to v1
  3. Set sunset date: 30 days from now
  4. Track migration progress weekly

Generate migration guide? [Yes] [No]
```

### 3. Unused Component Detection

Find components that can be removed:

```bash
$ npm run analyze:unused

Scanning codebase...

🗑️ Unused Components (12 found):

Safe to Remove (no usages):
  1. LegacyCard - Last used 6 months ago
  2. OldButton - Replaced by Button v2
  3. DeprecatedModal - Migrated to Modal v3

Potentially Unused (only in stories/tests):
  4. ExperimentalBadge - Used in Storybook only
  5. PrototypeAlert - Used in visual tests only

Low Usage (< 5 usages):
  6. RareTooltip - 2 usages (last 90 days)
  7. SpecializedInput - 3 usages (niche use case)

Recommendations:
  - Remove: LegacyCard, OldButton, DeprecatedModal
  - Review: ExperimentalBadge, PrototypeAlert
  - Keep: RareTooltip, SpecializedInput (still needed)

Estimated bundle savings: 47 KB (8% reduction)
```

### 4. Adoption Tracking

Track new component adoption:

```bash
$ npm run analyze:adoption Button@v2

📈 Adoption Report: Button@v2 (released 14 days ago)

Current Adoption:
  - 44 files using v2 (83%)
  - 8 files still on v1 (17%)

Adoption Trend:
  Day 1-7:   32 files migrated (61%)
  Day 8-14:  12 files migrated (22%)
  This week: 0 new migrations

Migration Velocity:
  - Week 1: 4.6 files/day
  - Week 2: 1.7 files/day
  - Slowing down ⚠️

Blockers:
  - High effort migration in src/Admin/dashboard.tsx
  - Team waiting for migration guide
  - Need code review bandwidth

Actions:
  1. Publish migration guide (high priority)
  2. Schedule pairing session for high-effort file
  3. Set team goal: 100% migration by end of month
```

## Technical Implementation

### Component Usage Scanner

```typescript
// scripts/scan-usage.ts

interface ComponentUsage {
  component: string;
  version: string;
  file: string;
  line: number;
  importPath: string;
  props: string[];
  variant?: string;
}

async function scanComponentUsage(
  componentName: string
): Promise<ComponentUsage[]> {
  const usages: ComponentUsage[] = [];

  // Find all files importing the component
  const files = await findImports(componentName);

  for (const file of files) {
    const ast = parseFile(file);

    // Find JSX usages
    const jsxElements = findJSXElements(ast, componentName);

    for (const element of jsxElements) {
      usages.push({
        component: componentName,
        version: getComponentVersion(file, componentName),
        file: file.path,
        line: element.loc.start.line,
        importPath: getImportPath(ast, componentName),
        props: extractProps(element),
        variant: getVariant(element),
      });
    }
  }

  return usages;
}

function getVariant(element: JSXElement): string | undefined {
  // Look for variant prop
  const variantProp = element.attributes.find(
    attr => attr.name === 'variant'
  );

  if (variantProp && variantProp.value.type === 'StringLiteral') {
    return variantProp.value.value;
  }

  return undefined;
}
```

### Deprecation Impact Analyzer

```typescript
// scripts/analyze-deprecation.ts

interface DeprecationImpact {
  component: string;
  version: string;
  totalUsages: number;
  affectedFiles: number;
  affectedFeatures: string[];
  migrationEffort: {
    low: number;
    medium: number;
    high: number;
  };
  breakingChanges: string[];
  estimatedHours: number;
}

async function analyzeDeprecationImpact(
  component: string,
  version: string
): Promise<DeprecationImpact> {
  const usages = await scanComponentUsage(component);
  const versionUsages = usages.filter(u => u.version === version);

  // Group by file
  const fileGroups = groupBy(versionUsages, u => u.file);

  // Analyze migration effort for each file
  const efforts = await Promise.all(
    Object.entries(fileGroups).map(([file, fileUsages]) =>
      analyzeMigrationEffort(file, fileUsages)
    )
  );

  // Categorize by effort
  const migrationEffort = {
    low: efforts.filter(e => e.effort === 'low').length,
    medium: efforts.filter(e => e.effort === 'medium').length,
    high: efforts.filter(e => e.effort === 'high').length,
  };

  // Estimate total hours
  const estimatedHours =
    migrationEffort.low * 0.1 +
    migrationEffort.medium * 0.5 +
    migrationEffort.high * 2;

  // Get breaking changes
  const breakingChanges = await getBreakingChanges(component, version);

  return {
    component,
    version,
    totalUsages: versionUsages.length,
    affectedFiles: Object.keys(fileGroups).length,
    affectedFeatures: extractFeatures(versionUsages),
    migrationEffort,
    breakingChanges,
    estimatedHours,
  };
}

async function analyzeMigrationEffort(
  file: string,
  usages: ComponentUsage[]
): Promise<{ file: string; effort: 'low' | 'medium' | 'high' }> {
  const code = await readFile(file);

  // Factors that increase effort:
  // - Custom styling on component
  // - Complex prop transformations
  // - Type conflicts
  // - Multiple usages in same file

  let complexityScore = 0;

  // Check for custom styling
  if (code.includes('styled(') && code.includes(usages[0].component)) {
    complexityScore += 2;
  }

  // Check for prop spreading
  if (usages.some(u => u.props.includes('...'))) {
    complexityScore += 1;
  }

  // Number of usages
  if (usages.length > 5) {
    complexityScore += 1;
  }

  // Categorize
  if (complexityScore === 0) return { file, effort: 'low' };
  if (complexityScore <= 2) return { file, effort: 'medium' };
  return { file, effort: 'high' };
}
```

### Unused Component Detector

```typescript
// scripts/detect-unused.ts

interface UnusedComponent {
  name: string;
  path: string;
  usageCount: number;
  lastUsed?: Date;
  category: 'safe-to-remove' | 'potentially-unused' | 'low-usage';
  bundleSize: number;
}

async function detectUnusedComponents(): Promise<UnusedComponent[]> {
  // Get all components
  const components = await getAllComponents();

  const unused: UnusedComponent[] = [];

  for (const component of components) {
    const usages = await scanComponentUsage(component.name);

    // Exclude test and story usages for "potentially unused" check
    const productionUsages = usages.filter(
      u => !u.file.includes('.test.') && !u.file.includes('.stories.')
    );

    let category: UnusedComponent['category'];

    if (productionUsages.length === 0 && usages.length === 0) {
      category = 'safe-to-remove';
    } else if (productionUsages.length === 0) {
      category = 'potentially-unused';
    } else if (productionUsages.length < 5) {
      category = 'low-usage';
    } else {
      continue; // Not unused
    }

    // Get last usage date
    const lastUsage = usages.length > 0
      ? await getLastModifiedDate(usages[0].file)
      : await getLastModifiedDate(component.path);

    // Get bundle size
    const bundleSize = await getComponentBundleSize(component.path);

    unused.push({
      name: component.name,
      path: component.path,
      usageCount: productionUsages.length,
      lastUsed: lastUsage,
      category,
      bundleSize,
    });
  }

  return unused;
}
```

## Example Commands

### Analyze Single Component

```bash
npm run analyze:usage Button

# Output: Usage report for Button component
```

### Deprecation Analysis

```bash
npm run analyze:deprecate Button@v1

# Output: Deprecation impact analysis with migration effort
```

### Find Unused Components

```bash
npm run analyze:unused

# Output: List of unused/low-usage components with recommendations
```

### Track Adoption

```bash
npm run analyze:adoption Button@v2

# Output: Adoption metrics and migration progress
```

### Generate Migration Guide

```bash
npm run generate:migration-guide Button@v1 Button@v2

# Output: Markdown migration guide with examples
```

## Integration with CI/CD

```yaml
# .github/workflows/component-analytics.yml
name: Component Analytics

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly on Sunday

jobs:
  analytics:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm ci
      - name: Analyze component usage
        run: npm run analyze:all
      - name: Generate report
        run: npm run generate:analytics-report
      - name: Create issue for unused components
        run: |
          npm run analyze:unused --json > unused.json
          gh issue create --title "Weekly: Unused Components" \
            --body-file unused.json \
            --label "maintenance,components"
```

## Dashboard Integration

Create a component analytics dashboard:

```typescript
// src/analytics/dashboard.tsx

export function ComponentAnalyticsDashboard() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);

  useEffect(() => {
    loadAnalytics().then(setAnalytics);
  }, []);

  return (
    <div>
      <h1>Component Usage Analytics</h1>

      <section>
        <h2>Most Used Components</h2>
        <BarChart data={analytics?.topComponents} />
      </section>

      <section>
        <h2>Unused Components</h2>
        <Table data={analytics?.unusedComponents} />
      </section>

      <section>
        <h2>Migration Progress</h2>
        <MigrationProgressChart data={analytics?.migrations} />
      </section>

      <section>
        <h2>Adoption Trends</h2>
        <LineChart data={analytics?.adoptionTrends} />
      </section>
    </div>
  );
}
```

## Best Practices

1. **Regular Scanning** - Run analytics weekly or on PR merges
2. **Track Trends** - Monitor adoption over time, not just snapshots
3. **Automate Alerts** - Create issues for unused components automatically
4. **Migration Planning** - Use effort estimates for sprint planning
5. **Documentation** - Generate migration guides from analysis results

## Limitations

- Requires AST parsing (works with TS/JS/TSX/JSX)
- May miss dynamic imports
- Cannot detect runtime usage patterns
- Estimates are guidelines, not precise timings

## Integration with Other Skills

- **visual-regression-testing** - Test after component migrations
- **accessibility-remediation** - Verify a11y after refactoring
- **story-generation** - Generate stories for migrated components
- **ci-cd-generator** - Add analytics to CI pipeline

## Files Reference

- `references/ast-parsing.md` - AST parsing techniques
- `examples/migration-guides.md` - Example migration guides
- `scripts/scan-usage.ts` - Usage scanner
- `scripts/analyze-deprecation.ts` - Deprecation analyzer
- `scripts/detect-unused.ts` - Unused component detector

## Summary

Component Usage Analytics provides data-driven insights for managing your component library. Track usage, plan deprecations, detect unused code, and monitor adoption.

**Key Benefits:**
- ✅ Data-driven component decisions
- ✅ Safe deprecation planning
- ✅ Identify bundle bloat
- ✅ Track migration progress
- ✅ Optimize component library

**Use this skill to** analyze component usage, plan deprecations, find unused components, and track adoption metrics.

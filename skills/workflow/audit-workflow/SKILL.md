---
name: audit-workflow
description: Bi-directional comparison workflow for config auditing. Compares what agents expect (from templates/standards) against what repositories actually have, presenting differences with remediation options. Use when agents need to audit configs, validate standards compliance, or identify mismatches between expected and actual configurations.
---

# Audit Workflow Skill

## Purpose

Provides standardized bi-directional comparison logic for config agents auditing repository configurations against MetaSaver standards.

## Bi-Directional Comparison Philosophy

**CRITICAL:** This skill implements **bi-directional comparison**, always comparing from both directions.

### What This Means

1. **Load what the AGENT expects** (from templates/standards)
2. **Discover what the REPOSITORY actually has**
3. **Compare BOTH directions:**
   - **Missing**: Agent expects but repo doesn't have
   - **Extra**: Repo has but agent doesn't expect
   - **Matching**: Both agent and repo have
4. **For EACH difference, present 3 options:**
   - **Conform**: Make repo match agent standard
   - **Update**: Update agent template to match repo
   - **Ignore**: Accept this difference

## Workflow Steps

### Step 1: Detect Repository Type

```typescript
// Repository type is provided via scope parameter
// If not provided, use /skill scope-check to determine
const repoType = await detectRepoType(); // "library" | "consumer"
```

### Step 2: Load Expected Standards

```typescript
interface ExpectedConfig {
  source: "template" | "skill" | "standard";
  path: string;
  content: any;
  rules: string[]; // List of rules this config must follow
}

async function loadExpectedStandards(
  configType: string,
): Promise<ExpectedConfig> {
  // Load from .claude/templates/ or skill documentation
  const templatePath = `.claude/templates/common/${configType}`;
  const content = await readTemplate(templatePath);

  return {
    source: "template",
    path: templatePath,
    content: parseConfig(content),
    rules: extractRules(content),
  };
}
```

### Step 3: Discover Actual Repository State

```typescript
interface ActualConfig {
  found: boolean;
  locations: string[]; // May find configs in unexpected locations
  content: any;
  violations: string[];
  warnings: string[];
}

async function discoverActualState(
  configType: string,
  scope: string,
): Promise<ActualConfig[]> {
  // Use Glob to find all instances
  const pattern = getConfigPattern(configType); // e.g., "**/*.eslintrc.js"
  const files = await glob(pattern, scope);

  return await Promise.all(
    files.map(async (file) => {
      const content = await readFile(file);
      const { violations, warnings } = await validateConfig(
        content,
        configType,
      );

      return {
        found: true,
        locations: [file],
        content: parseConfig(content),
        violations,
        warnings,
      };
    }),
  );
}
```

### Step 4: Compare Directions

```typescript
interface ComparisonResult {
  missing: string[]; // Agent expects but repo doesn't have
  extra: string[]; // Repo has but agent doesn't expect
  matching: string[]; // Both have
  violations: string[]; // Standards violations
  warnings: string[]; // Non-critical issues
}

function compareDirections(
  expected: ExpectedConfig,
  actual: ActualConfig,
): ComparisonResult {
  const result: ComparisonResult = {
    missing: [],
    extra: [],
    matching: [],
    violations: [],
    warnings: [],
  };

  // Compare expected vs actual
  for (const rule of expected.rules) {
    const actualHasRule = checkRuleInConfig(actual.content, rule);

    if (!actualHasRule) {
      result.missing.push(rule);
      result.violations.push(`Missing: ${rule}`);
    } else {
      result.matching.push(rule);
    }
  }

  // Compare actual vs expected (find unexpected content)
  const actualRules = extractRulesFromConfig(actual.content);
  for (const rule of actualRules) {
    if (!expected.rules.includes(rule)) {
      result.extra.push(rule);
      result.warnings.push(`Unexpected: ${rule} (not in standard)`);
    }
  }

  return result;
}
```

### Step 5: Generate Audit Report

```typescript
interface AuditReport {
  repoType: "library" | "consumer";
  configType: string;
  totalConfigs: number;
  passing: number;
  failing: number;
  results: ConfigAuditResult[];
}

interface ConfigAuditResult {
  path: string;
  status: "pass" | "fail";
  violations: string[];
  warnings: string[];
  comparison: ComparisonResult;
}

function generateAuditReport(
  repoType: string,
  configType: string,
  results: ConfigAuditResult[],
): string {
  const passing = results.filter((r) => r.status === "pass").length;
  const failing = results.filter((r) => r.status === "fail").length;

  return `
${configType} Audit
==============================================

Repository: ${getRepoName()}
Type: ${repoType === "library" ? "Library repo (intentional differences allowed)" : "Consumer repo (strict standards enforced)"}

Checking ${results.length} ${configType} configs...

${results.map((r) => formatConfigResult(r)).join("\n\n")}

Summary: ${passing}/${results.length} configs passing (${Math.round((passing / results.length) * 100)}%)
`;
}

function formatConfigResult(result: ConfigAuditResult): string {
  if (result.status === "pass") {
    return `✅ ${result.path}`;
  }

  return `
❌ ${result.path}
${result.violations.map((v) => `  ${v}`).join("\n")}
${result.warnings.length > 0 ? "\n" + result.warnings.map((w) => `  ⚠️  ${w}`).join("\n") : ""}
`;
}
```

## Usage Examples

### Example 1: Audit ESLint Configs

```typescript
// Step 1: Detect repo type
const repoType = await detectRepoType();

// Step 2: Load expected standards
const expected = await loadExpectedStandards("eslint");

// Step 3: Discover actual state
const scope = repoType === "library" ? "packages/*" : ".";
const actualConfigs = await discoverActualState("eslint", scope);

// Step 4: Compare each config
const results = actualConfigs.map((actual) => ({
  path: actual.locations[0],
  status: actual.violations.length === 0 ? "pass" : "fail",
  violations: actual.violations,
  warnings: actual.warnings,
  comparison: compareDirections(expected, actual),
}));

// Step 5: Generate report
const report = generateAuditReport(repoType, "ESLint", results);
console.log(report);

// Step 6: Offer remediation (use remediation-options skill)
if (results.some((r) => r.status === "fail")) {
  await offerRemediationOptions(repoType, results);
}
```

### Example 2: Find Unexpected Config Locations

```typescript
// Discover configs that might be in unexpected locations
const expectedLocation = repoType === "library" ? "packages/*/.*" : ".";
const actualConfigs = await discoverActualState("prettier", "**");

const unexpected = actualConfigs.filter(
  (config) => !config.locations.some((loc) => loc.startsWith(expectedLocation)),
);

if (unexpected.length > 0) {
  console.log(`
⚠️  Found ${configType} configs in unexpected locations:
${unexpected.map((c) => `  - ${c.locations.join(", ")}`).join("\n")}

These may indicate:
  - Legacy configs that should be removed
  - Package-specific overrides (check if intentional)
  - Duplicate configs causing conflicts
`);
}
```

## Scope Detection Patterns

### From User Intent

```typescript
function detectScopeFromIntent(userPrompt: string): string {
  // "audit the repo" → All configs (parallel Globs)
  if (/audit\s+(the\s+)?repo/i.test(userPrompt)) {
    return "**";
  }

  // "fix the web app X config" → Extract path from context
  const pathMatch = userPrompt.match(/(?:apps|packages|services)\/[\w-]+/);
  if (pathMatch) {
    return pathMatch[0];
  }

  // "audit what you just did" → Only modified configs (check memory)
  if (/audit\s+what\s+you\s+just/i.test(userPrompt)) {
    return await getRecentlyModifiedConfigs();
  }

  // "check apps/web" → Specific path
  if (/check\s+([\w\/\.-]+)/i.test(userPrompt)) {
    return RegExp.$1;
  }

  // Default: current directory
  return ".";
}
```

## Library vs Consumer Handling

```typescript
function applyStandardsForRepoType(
  repoType: string,
  comparison: ComparisonResult,
): void {
  if (repoType === "library") {
    // Library repos: Differences are often intentional
    console.log(`
ℹ️  Library repo may have custom configuration
   Applying base validation only...
`);

    // Filter to only critical violations
    comparison.violations = comparison.violations.filter((v) =>
      isCriticalViolation(v),
    );
  } else {
    // Consumer repos: Strict standards enforced
    console.log(`
📋 Consumer repo (strict standards enforced)
   All violations must be addressed.
`);
  }
}
```

## Exception Handling

```typescript
interface ConfigException {
  configType: string;
  reason: string;
  declaredIn: "package.json" | "CLAUDE.md";
}

async function checkForExceptions(
  packagePath: string,
  configType: string,
): Promise<ConfigException | null> {
  const pkg = await readPackageJson(packagePath);

  if (pkg.metasaver?.configExceptions?.[configType]) {
    return {
      configType,
      reason: pkg.metasaver.configExceptions.reason || "No reason provided",
      declaredIn: "package.json",
    };
  }

  return null;
}

// Usage in audit
const exception = await checkForExceptions("./package.json", "eslint");
if (exception) {
  console.log(`
ℹ️  Exception noted - relaxed validation mode
   Type: ${exception.configType}
   Reason: "${exception.reason}"
`);

  // Apply relaxed validation
  applyRelaxedValidation(comparison);
}
```

## Integration with Remediation

After audit completes, transition to remediation-options skill:

```typescript
// After generating audit report
if (results.some((r) => r.status === "fail")) {
  // Use remediation-options skill for next steps
  await offerRemediationOptions({
    repoType,
    configType,
    violations: results.filter((r) => r.status === "fail"),
  });
}
```

## Used By

- All config agents (eslint-agent, prettier-agent, typescript-agent, etc.)
- Audit commands
- CI/CD validation pipelines
- Pre-commit hooks

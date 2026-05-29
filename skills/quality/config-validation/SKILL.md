---
name: config-validation
description: Generic configuration validation patterns for comparing files against templates, generating diff reports, and validating config consistency. Provides compareToTemplate, generateDiffReport, and validateConfigStructure functions with validation rule library. Use when implementing config validation logic, building custom validation rules, or performing multi-config comparisons.
---

# Config Validation Skill

## Purpose

Provides generic configuration validation patterns to compare files against templates, generate diff reports, and validate configuration consistency.

## Input Parameters

```typescript
interface ValidationOptions {
  configPath: string; // Path to config file to validate
  templatePath?: string; // Optional template to compare against
  schemaPath?: string; // Optional JSON schema for validation
  rules?: ValidationRule[]; // Custom validation rules
  outputFormat?: "json" | "markdown" | "console";
}

interface ValidationRule {
  name: string;
  description: string;
  validate: (config: any) => ValidationResult;
}

interface ValidationResult {
  valid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  suggestions: string[];
}
```

## Output Format

```typescript
interface ValidationReport {
  configFile: string;
  valid: boolean;
  timestamp: string;
  summary: {
    totalErrors: number;
    totalWarnings: number;
    totalSuggestions: number;
  };
  errors: ValidationError[];
  warnings: ValidationWarning[];
  suggestions: string[];
  diff?: ConfigDiff;
}

interface ValidationError {
  code: string;
  message: string;
  path: string; // JSON path to error location
  severity: "critical" | "error";
  fix?: string; // Suggested fix
}

interface ValidationWarning {
  code: string;
  message: string;
  path: string;
  suggestion: string;
}

interface ConfigDiff {
  added: string[];
  removed: string[];
  modified: Array<{
    path: string;
    oldValue: any;
    newValue: any;
  }>;
}
```

## Core Functions

### 1. Compare Against Template

```typescript
function compareToTemplate(
  configPath: string,
  templatePath: string
): ConfigDiff {
  const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
  const template = JSON.parse(fs.readFileSync(templatePath, "utf-8"));

  const diff: ConfigDiff = {
    added: [],
    removed: [],
    modified: [],
  };

  // Deep comparison
  function compare(configObj: any, templateObj: any, path = "") {
    // Check for removed keys
    for (const key in templateObj) {
      const currentPath = path ? `${path}.${key}` : key;

      if (!(key in configObj)) {
        diff.removed.push(currentPath);
      } else if (
        typeof templateObj[key] === "object" &&
        templateObj[key] !== null
      ) {
        compare(configObj[key], templateObj[key], currentPath);
      } else if (configObj[key] !== templateObj[key]) {
        diff.modified.push({
          path: currentPath,
          oldValue: configObj[key],
          newValue: templateObj[key],
        });
      }
    }

    // Check for added keys
    for (const key in configObj) {
      const currentPath = path ? `${path}.${key}` : key;
      if (!(key in templateObj)) {
        diff.added.push(currentPath);
      }
    }
  }

  compare(config, template);
  return diff;
}
```

### 2. Generate Diff Report

```typescript
function generateDiffReport(
  diff: ConfigDiff,
  format: "json" | "markdown" | "console" = "markdown"
): string {
  if (format === "markdown") {
    let report = "# Configuration Diff Report\n\n";

    if (diff.removed.length > 0) {
      report += "## ❌ Missing Required Configuration\n\n";
      for (const path of diff.removed) {
        report += `- \`${path}\` - **Missing from current config**\n`;
      }
      report += "\n";
    }

    if (diff.added.length > 0) {
      report += "## ➕ Additional Configuration\n\n";
      for (const path of diff.added) {
        report += `- \`${path}\` - **Not in template**\n`;
      }
      report += "\n";
    }

    if (diff.modified.length > 0) {
      report += "## 🔄 Modified Configuration\n\n";
      for (const mod of diff.modified) {
        report += `### \`${mod.path}\`\n`;
        report += `- **Current**: \`${JSON.stringify(mod.oldValue)}\`\n`;
        report += `- **Expected**: \`${JSON.stringify(mod.newValue)}\`\n\n`;
      }
    }

    return report;
  }

  return JSON.stringify(diff, null, 2);
}
```

### 3. Validate Config Structure

```typescript
function validateConfigStructure(
  configPath: string,
  rules: ValidationRule[]
): ValidationReport {
  const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
  const errors: ValidationError[] = [];
  const warnings: ValidationWarning[] = [];
  const suggestions: string[] = [];

  for (const rule of rules) {
    const result = rule.validate(config);
    errors.push(...result.errors);
    warnings.push(...result.warnings);
    suggestions.push(...result.suggestions);
  }

  return {
    configFile: configPath,
    valid:
      errors.filter((e) => e.severity === "critical" || e.severity === "error")
        .length === 0,
    timestamp: new Date().toISOString(),
    summary: {
      totalErrors: errors.length,
      totalWarnings: warnings.length,
      totalSuggestions: suggestions.length,
    },
    errors,
    warnings,
    suggestions,
  };
}
```

## Usage Examples

### Example 1: Validate TypeScript Config

```typescript
import { validateConfig } from ".claude/skills/config-validation.skill";

const report = await validateConfig({
  configPath: "/mnt/f/code/resume-builder/tsconfig.json",
  templatePath:
    "/mnt/f/code/resume-builder/.claude/templates/tsconfig.template.json",
  rules: [
    {
      name: "strict-mode",
      description: "Ensure strict mode is enabled",
      validate: (config) => ({
        valid: config.compilerOptions?.strict === true,
        errors: config.compilerOptions?.strict
          ? []
          : [
              {
                code: "TS001",
                message: "Strict mode must be enabled",
                path: "compilerOptions.strict",
                severity: "error",
                fix: 'Set "strict": true in compilerOptions',
              },
            ],
        warnings: [],
        suggestions: [],
      }),
    },
  ],
});

console.log(`Valid: ${report.valid}`);
console.log(`Errors: ${report.summary.totalErrors}`);
```

### Example 2: Compare ESLint Configs

```typescript
import {
  compareToTemplate,
  generateDiffReport,
} from ".claude/skills/config-validation.skill";

const diff = compareToTemplate(
  "/mnt/f/code/resume-builder/.eslintrc.json",
  "/mnt/f/code/resume-builder/.claude/templates/eslintrc.template.json"
);

const report = generateDiffReport(diff, "markdown");
console.log(report);
```

### Example 3: Multi-Package Validation

```typescript
import { findPackagesByType } from ".claude/skills/monorepo-navigation.skill";
import { validateConfig } from ".claude/skills/config-validation.skill";

const packages = await findPackagesByType({
  workspaceRoot: "/mnt/f/code/resume-builder",
  packageType: "all",
});

const reports = await Promise.all(
  packages.map((pkg) =>
    validateConfig({
      configPath: `${pkg.path}/tsconfig.json`,
      templatePath: "/mnt/f/code/resume-builder/tsconfig.json",
      rules: commonTsConfigRules,
    })
  )
);

const invalidPackages = reports.filter((r) => !r.valid);
console.log(`${invalidPackages.length} packages have config issues`);
```

## Validation Rule Library

```typescript
// Common validation rules
export const commonValidationRules = {
  typescript: [
    {
      name: "strict-mode",
      description: "Enforce TypeScript strict mode",
      validate: (config) => ({
        valid: config.compilerOptions?.strict === true,
        errors: [],
        warnings: config.compilerOptions?.strict
          ? []
          : [
              {
                code: "TS001",
                message: "Consider enabling strict mode",
                path: "compilerOptions.strict",
                suggestion: 'Set "strict": true for better type safety',
              },
            ],
        suggestions: [],
      }),
    },
    {
      name: "module-resolution",
      description: "Ensure correct module resolution",
      validate: (config) => {
        const resolution = config.compilerOptions?.moduleResolution;
        const isValid = resolution === "node" || resolution === "bundler";
        return {
          valid: isValid,
          errors: isValid
            ? []
            : [
                {
                  code: "TS002",
                  message: "Invalid module resolution strategy",
                  path: "compilerOptions.moduleResolution",
                  severity: "error",
                  fix: 'Use "node" or "bundler" for moduleResolution',
                },
              ],
          warnings: [],
          suggestions: [],
        };
      },
    },
  ],

  prettier: [
    {
      name: "consistent-quotes",
      description: "Enforce consistent quote style",
      validate: (config) => ({
        valid: "singleQuote" in config,
        errors: [],
        warnings:
          "singleQuote" in config
            ? []
            : [
                {
                  code: "PR001",
                  message: "Quote style not specified",
                  path: "singleQuote",
                  suggestion: 'Add "singleQuote": true or false',
                },
              ],
        suggestions: [],
      }),
    },
  ],

  eslint: [
    {
      name: "extends-required",
      description: "Ensure ESLint extends from base config",
      validate: (config) => {
        const hasExtends =
          Array.isArray(config.extends) && config.extends.length > 0;
        return {
          valid: hasExtends,
          errors: hasExtends
            ? []
            : [
                {
                  code: "ES001",
                  message: "No base configuration extended",
                  path: "extends",
                  severity: "error",
                  fix: 'Add "extends": ["eslint:recommended"]',
                },
              ],
          warnings: [],
          suggestions: [],
        };
      },
    },
  ],
};
```

## Integration Pattern

```typescript
// Generic config auditor pattern
export async function auditConfig(
  configType: "typescript" | "prettier" | "eslint",
  configPath: string,
  templatePath?: string
): Promise<ValidationReport> {
  const rules = commonValidationRules[configType];

  let report = await validateConfigStructure(configPath, rules);

  if (templatePath) {
    const diff = compareToTemplate(configPath, templatePath);
    report.diff = diff;

    // Add diff-based errors
    if (diff.removed.length > 0) {
      report.errors.push({
        code: "DIFF001",
        message: `Missing ${diff.removed.length} required configuration keys`,
        path: "root",
        severity: "error",
        fix: "Add missing keys from template",
      });
    }
  }

  return report;
}
```

## Used By

- TypeScript config agent
- Prettier config agent
- ESLint config agent
- Package.json validator
- CI/CD config validator
- Any agent that validates configuration files

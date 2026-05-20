---
name: when-auditing-code-style-use-style-audit
description: Code style and conventions audit with auto-fix capabilities for comprehensive style enforcement
version: 1.0.0
category: testing-quality
agents:
  - code-analyzer
  - reviewer
topology: mesh
coordination: claude-flow
evidence_based: true
auto_fix: true
---

# Code Style Audit with Auto-Fix

## Purpose

Perform comprehensive code style and conventions audit across the entire codebase with automated fix capabilities. Identifies style violations, enforces naming conventions, validates formatting, and applies automated corrections to ensure consistent code quality.

## Core Principles

- **Automated Enforcement**: Auto-fix for style violations where possible
- **Comprehensive Coverage**: ESLint, Prettier, TypeScript, naming conventions
- **Evidence-Based**: Measurable style compliance metrics
- **Non-Breaking**: Only applies safe, non-destructive fixes
- **Continuous Compliance**: Style validation at every commit

## Phase 1: Scan Codebase

### Objective
Identify all style violations, formatting issues, and convention inconsistencies across the codebase.

### Agent Configuration
```yaml
agent: code-analyzer
specialization: style-scanning
tools: ESLint, Prettier, TypeScript
```

### Execution Steps

**1. Initialize Style Scan**
```bash
# Pre-task setup
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-analyzer" \
  --description "Comprehensive code style scanning" \
  --task-type "style-scan"

# Restore session context
npx claude-flow@alpha hooks session-restore \
  --session-id "style-audit-${AUDIT_ID}" \
  --agent-id "code-analyzer"
```

**2. ESLint Comprehensive Scan**
```bash
# Run ESLint with all rules
npx eslint . \
  --ext .js,.jsx,.ts,.tsx \
  --format json \
  --output-file eslint-report.json \
  --max-warnings 0

# Separate auto-fixable vs manual issues
npx eslint . \
  --ext .js,.jsx,.ts,.tsx \
  --format json \
  --fix-dry-run > eslint-fixable-report.json
```

**3. Prettier Formatting Check**
```bash
# Check all supported file types
npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,scss,md,yaml,yml}" \
  --list-different > prettier-violations.txt

# Check configuration consistency
npx prettier --find-config-path . > prettier-config-check.txt
```

**4. TypeScript Style Validation**
```bash
# Strict type checking
npx tsc --noEmit --strict --pretty false 2> typescript-strict-errors.txt

# Check for any types
grep -r ": any" src/ --include="*.ts" --include="*.tsx" > any-types.txt

# Check for implicit any
npx tsc --noImplicitAny --noEmit 2> implicit-any-errors.txt
```

**5. Naming Convention Analysis**
```javascript
// Naming patterns validation
const namingConventions = {
  // File naming
  files: {
    pattern: /^[a-z][a-z0-9-]*\.(js|ts|jsx|tsx)$/,
    examples: ['user-service.js', 'api-client.ts'],
    violations: []
  },

  // Directory naming
  directories: {
    pattern: /^[a-z][a-z0-9-]*$/,
    examples: ['user-api', 'auth-service'],
    violations: []
  },

  // Class naming (PascalCase)
  classes: {
    pattern: /^[A-Z][a-zA-Z0-9]*$/,
    examples: ['UserService', 'ApiClient'],
    violations: []
  },

  // Function naming (camelCase)
  functions: {
    pattern: /^[a-z][a-zA-Z0-9]*$/,
    examples: ['getUserById', 'calculateTotal'],
    violations: []
  },

  // Constant naming (UPPER_SNAKE_CASE)
  constants: {
    pattern: /^[A-Z][A-Z0-9_]*$/,
    examples: ['MAX_RETRIES', 'API_BASE_URL'],
    violations: []
  },

  // React component naming (PascalCase)
  components: {
    pattern: /^[A-Z][a-zA-Z0-9]*$/,
    examples: ['UserProfile', 'LoginForm'],
    violations: []
  },

  // Private methods (leading underscore)
  privateMethods: {
    pattern: /^_[a-z][a-zA-Z0-9]*$/,
    examples: ['_validateInput', '_processData'],
    violations: []
  }
};

// Scan for naming violations
function scanNamingViolations(ast) {
  ast.walk((node) => {
    if (node.type === 'ClassDeclaration') {
      if (!namingConventions.classes.pattern.test(node.id.name)) {
        namingConventions.classes.violations.push({
          file: node.loc.source,
          line: node.loc.start.line,
          found: node.id.name,
          expected: toPascalCase(node.id.name)
        });
      }
    }
    // Similar checks for other node types...
  });
}
```

**6. Code Organization Violations**
```javascript
// File organization rules
const organizationRules = {
  max_file_length: {
    threshold: 500,
    unit: 'lines',
    violations: []
  },

  max_function_length: {
    threshold: 50,
    unit: 'lines',
    violations: []
  },

  max_function_parameters: {
    threshold: 4,
    unit: 'parameters',
    violations: []
  },

  max_nesting_depth: {
    threshold: 4,
    unit: 'levels',
    violations: []
  },

  import_organization: {
    rules: [
      'External imports first',
      'Internal imports second',
      'Relative imports last',
      'Alphabetically sorted within groups'
    ],
    violations: []
  },

  export_organization: {
    rules: [
      'Named exports grouped',
      'Default export last',
      'No mixed inline and end-of-file exports'
    ],
    violations: []
  }
};

// Check file length
function checkFileLength(filePath) {
  const lines = fs.readFileSync(filePath, 'utf8').split('\n').length;
  if (lines > organizationRules.max_file_length.threshold) {
    organizationRules.max_file_length.violations.push({
      file: filePath,
      lines: lines,
      excess: lines - organizationRules.max_file_length.threshold
    });
  }
}
```

**7. Generate Scan Report**
```markdown
## Code Style Audit - Scan Results

### ESLint Violations
**Total: 247 issues (189 errors, 58 warnings)**

#### By Category
| Category | Count | Auto-Fixable |
|----------|-------|--------------|
| Formatting | 123 | 123 ✅ |
| Best Practices | 45 | 28 ✅ |
| Possible Errors | 34 | 12 ✅ |
| Variables | 28 | 18 ✅ |
| ES6 | 17 | 8 ✅ |

#### Top Violations
1. `indent` (2 spaces): 67 occurrences
2. `no-unused-vars`: 34 occurrences
3. `prefer-const`: 28 occurrences
4. `no-console`: 23 occurrences
5. `quotes` (single): 19 occurrences

### Prettier Violations
**Total: 147 files need formatting**

- Inconsistent quote style (single vs double): 89 files
- Missing trailing commas: 67 files
- Incorrect indentation: 45 files
- Line length exceeded (>100 chars): 34 files

### TypeScript Issues
**Total: 67 issues**

- Explicit `any` types: 23 occurrences
- Implicit `any` warnings: 31 occurrences
- Strict null checks: 13 occurrences

### Naming Convention Violations
**Total: 89 violations**

| Convention | Violations | Examples |
|------------|------------|----------|
| File naming | 23 | `UserService.js` → `user-service.js` |
| Class naming | 12 | `apiClient` → `ApiClient` |
| Function naming | 18 | `GetUserById` → `getUserById` |
| Constant naming | 15 | `maxRetries` → `MAX_RETRIES` |
| Variable naming | 21 | `user_id` → `userId` |

### Code Organization Issues
**Total: 56 violations**

- Files exceeding 500 lines: 12 files
- Functions exceeding 50 lines: 28 functions
- Functions with >4 parameters: 8 functions
- Nesting depth >4 levels: 8 occurrences

### Summary
- **Auto-fixable**: 189/247 ESLint issues (76.5%)
- **Manual fixes required**: 58 ESLint issues
- **Prettier auto-fixable**: 147 files (100%)
- **Naming convention fixes**: 89 (requires refactoring)
```

**8. Store Scan Results**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "style-scan-report.json" \
  --memory-key "swarm/code-analyzer/scan-results" \
  --metadata "{\"total_violations\": ${TOTAL_VIOLATIONS}, \"auto_fixable\": ${AUTO_FIXABLE}}"
```

### Validation Gates
- ✅ Complete codebase scanned
- ✅ All violation types identified
- ✅ Auto-fixable issues flagged
- ✅ Manual issues documented

### Expected Outputs
- `eslint-report.json` - ESLint violations
- `prettier-violations.txt` - Formatting issues
- `typescript-strict-errors.txt` - Type issues
- `naming-violations.json` - Naming convention issues
- `style-scan-report.json` - Comprehensive scan results

---

## Phase 2: Compare to Standards

### Objective
Compare scanned violations against project coding standards and industry best practices.

### Agent Configuration
```yaml
agent: reviewer
specialization: standards-comparison
standards: Airbnb, Google, StandardJS
```

### Execution Steps

**1. Initialize Standards Comparison**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "reviewer" \
  --description "Compare violations to coding standards" \
  --task-type "standards-comparison"
```

**2. Load Project Standards**
```javascript
// Load project coding standards
const projectStandards = {
  eslint_config: require('./.eslintrc.json'),
  prettier_config: require('./.prettierrc.json'),
  typescript_config: require('./tsconfig.json'),

  // Custom conventions
  naming_conventions: require('./docs/coding-standards.md'),
  file_organization: require('./docs/file-structure.md'),

  // Base standards
  base_standard: 'airbnb' // or 'google', 'standard'
};
```

**3. Compare ESLint Configuration**
```javascript
// Check ESLint config completeness
const eslintComparison = {
  configured_rules: Object.keys(projectStandards.eslint_config.rules).length,
  airbnb_rules: 247, // Airbnb ESLint config

  missing_rules: [],
  conflicting_rules: [],
  disabled_rules: [],

  // Rule categories
  formatting_rules: 0,
  best_practices_rules: 0,
  error_prevention_rules: 0,
  es6_rules: 0
};

// Identify missing important rules
const criticalRules = [
  'no-var',
  'prefer-const',
  'no-unused-vars',
  'no-console',
  'eqeqeq',
  'no-implicit-globals',
  'strict'
];

criticalRules.forEach(rule => {
  if (!projectStandards.eslint_config.rules[rule]) {
    eslintComparison.missing_rules.push(rule);
  }
});
```

**4. Compare Prettier Configuration**
```javascript
// Prettier standard comparison
const prettierComparison = {
  configured: projectStandards.prettier_config,

  recommended: {
    printWidth: 100,
    tabWidth: 2,
    useTabs: false,
    semi: true,
    singleQuote: true,
    quoteProps: 'as-needed',
    trailingComma: 'es5',
    bracketSpacing: true,
    arrowParens: 'always'
  },

  differences: []
};

// Compare configurations
Object.keys(prettierComparison.recommended).forEach(key => {
  const projectValue = projectStandards.prettier_config[key];
  const recommendedValue = prettierComparison.recommended[key];

  if (projectValue !== recommendedValue) {
    prettierComparison.differences.push({
      option: key,
      project: projectValue,
      recommended: recommendedValue
    });
  }
});
```

**5. Assess TypeScript Strictness**
```javascript
// TypeScript strictness comparison
const typescriptComparison = {
  current_strictness: projectStandards.typescript_config.compilerOptions.strict || false,

  strict_options: {
    noImplicitAny: projectStandards.typescript_config.compilerOptions.noImplicitAny,
    noImplicitThis: projectStandards.typescript_config.compilerOptions.noImplicitThis,
    alwaysStrict: projectStandards.typescript_config.compilerOptions.alwaysStrict,
    strictNullChecks: projectStandards.typescript_config.compilerOptions.strictNullChecks,
    strictFunctionTypes: projectStandards.typescript_config.compilerOptions.strictFunctionTypes,
    strictBindCallApply: projectStandards.typescript_config.compilerOptions.strictBindCallApply,
    strictPropertyInitialization: projectStandards.typescript_config.compilerOptions.strictPropertyInitialization
  },

  recommended_strictness: true,

  recommendations: []
};

// Generate recommendations
if (!typescriptComparison.current_strictness) {
  typescriptComparison.recommendations.push('Enable "strict": true');
}

Object.keys(typescriptComparison.strict_options).forEach(option => {
  if (!typescriptComparison.strict_options[option]) {
    typescriptComparison.recommendations.push(`Enable "${option}": true`);
  }
});
```

**6. Generate Standards Comparison Report**
```markdown
## Standards Comparison Report

### ESLint Configuration
**Configured Rules**: 178 / 247 (72.1%)
**Base Standard**: Airbnb

#### Missing Critical Rules (7)
1. `no-var` - Disallow var, use let/const
2. `prefer-const` - Prefer const for unchanged variables
3. `no-implicit-globals` - Disallow implicit global variables
4. `strict` - Require strict mode
5. `no-shadow` - Disallow variable shadowing
6. `no-param-reassign` - Disallow parameter reassignment
7. `consistent-return` - Require consistent return

#### Conflicting Rules (3)
- `indent`: Project uses 4 spaces, Airbnb recommends 2
- `quotes`: Project uses double, Airbnb recommends single
- `comma-dangle`: Project disabled, Airbnb requires

#### Disabled Important Rules (5)
- `no-console` - Currently disabled, should be error
- `no-debugger` - Currently disabled, should be error
- `no-alert` - Currently disabled, should be warning

### Prettier Configuration
**Configuration Completeness**: 8 / 9 options (88.9%)

#### Configuration Differences from Recommended
| Option | Project | Recommended | Impact |
|--------|---------|-------------|--------|
| `singleQuote` | false | true | Inconsistent with ESLint |
| `printWidth` | 80 | 100 | More line breaks than needed |

### TypeScript Configuration
**Strict Mode**: ❌ Disabled
**Individual Strict Checks**: 3 / 7 enabled (42.9%)

#### Recommendations
1. Enable `"strict": true` (enables all strict checks)
2. Enable `noImplicitAny` for better type safety
3. Enable `strictNullChecks` to catch null/undefined errors
4. Enable `strictFunctionTypes` for safer function typing

### Naming Conventions
**Documented**: ✅ Yes (docs/coding-standards.md)
**Enforced**: ⚠️ Partial (ESLint naming rules not configured)

#### Recommendations
1. Add `@typescript-eslint/naming-convention` rule
2. Configure naming patterns for:
   - Classes (PascalCase)
   - Functions/variables (camelCase)
   - Constants (UPPER_SNAKE_CASE)
   - Private members (leading underscore)

### File Organization
**Max File Length**: 500 lines ✅
**Max Function Length**: 50 lines ✅
**Import Ordering**: ⚠️ Not enforced

#### Recommendations
1. Add `import/order` ESLint rule
2. Configure import groups:
   - External dependencies
   - Internal modules
   - Relative imports
```

**7. Store Comparison Results**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "standards-comparison-report.json" \
  --memory-key "swarm/reviewer/standards-comparison" \
  --metadata "{\"compliance_pct\": ${COMPLIANCE_PCT}, \"missing_rules\": ${MISSING_RULES_COUNT}}"
```

### Validation Gates
- ✅ Standards documented
- ✅ Comparison complete
- ✅ Gaps identified
- ✅ Recommendations generated

### Expected Outputs
- `standards-comparison-report.json` - Detailed comparison
- `missing-rules.json` - Rules to add
- `config-recommendations.json` - Configuration improvements

---

## Phase 3: Report Violations

### Objective
Generate comprehensive violation reports with prioritization, categorization, and fix recommendations.

### Agent Configuration
```yaml
agent: code-analyzer
specialization: violation-reporting
output: HTML, JSON, Markdown
```

### Execution Steps

**1. Initialize Violation Reporting**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-analyzer" \
  --description "Generate violation reports" \
  --task-type "violation-reporting"
```

**2. Prioritize Violations**
```javascript
// Prioritization criteria
const violationPriority = {
  P0_CRITICAL: {
    description: 'Breaking production issues, security risks',
    examples: ['no-eval', 'no-implied-eval', 'no-script-url'],
    violations: []
  },

  P1_HIGH: {
    description: 'Potential bugs, code smells',
    examples: ['no-unused-vars', 'no-unreachable', 'no-fallthrough'],
    violations: []
  },

  P2_MEDIUM: {
    description: 'Best practices, maintainability',
    examples: ['prefer-const', 'no-var', 'eqeqeq'],
    violations: []
  },

  P3_LOW: {
    description: 'Formatting, style consistency',
    examples: ['indent', 'quotes', 'comma-dangle'],
    violations: []
  }
};

// Categorize violations by priority
function prioritizeViolations(violations) {
  violations.forEach(violation => {
    const rule = violation.ruleId;

    if (violationPriority.P0_CRITICAL.examples.includes(rule)) {
      violationPriority.P0_CRITICAL.violations.push(violation);
    } else if (violationPriority.P1_HIGH.examples.includes(rule)) {
      violationPriority.P1_HIGH.violations.push(violation);
    } else if (violationPriority.P2_MEDIUM.examples.includes(rule)) {
      violationPriority.P2_MEDIUM.violations.push(violation);
    } else {
      violationPriority.P3_LOW.violations.push(violation);
    }
  });
}
```

**3. Categorize by File/Module**
```javascript
// Group violations by file
const violationsByFile = {};

function categorizeByFile(violations) {
  violations.forEach(violation => {
    const file = violation.filePath;

    if (!violationsByFile[file]) {
      violationsByFile[file] = {
        file: file,
        total_violations: 0,
        critical: 0,
        high: 0,
        medium: 0,
        low: 0,
        violations: []
      };
    }

    violationsByFile[file].violations.push(violation);
    violationsByFile[file].total_violations++;

    // Increment priority counters
    if (violation.priority === 'P0_CRITICAL') violationsByFile[file].critical++;
    if (violation.priority === 'P1_HIGH') violationsByFile[file].high++;
    if (violation.priority === 'P2_MEDIUM') violationsByFile[file].medium++;
    if (violation.priority === 'P3_LOW') violationsByFile[file].low++;
  });

  // Sort by total violations descending
  return Object.values(violationsByFile)
    .sort((a, b) => b.total_violations - a.total_violations);
}
```

**4. Generate Fix Recommendations**
```javascript
// Auto-fix recommendations
const fixRecommendations = {
  auto_fixable: {
    count: 0,
    script: 'npx eslint . --fix && npx prettier --write "**/*.{js,ts,jsx,tsx}"',
    violations: []
  },

  semi_auto_fixable: {
    count: 0,
    description: 'Requires code review after auto-fix',
    violations: []
  },

  manual_fix_required: {
    count: 0,
    description: 'Requires human judgment and refactoring',
    violations: []
  }
};

// Generate fix instructions for each violation
function generateFixInstructions(violation) {
  const instructions = {
    rule: violation.ruleId,
    file: violation.filePath,
    line: violation.line,
    column: violation.column,

    fix_type: 'auto', // 'auto', 'semi-auto', 'manual'
    fix_command: null,
    fix_description: null,

    before: violation.source,
    after: null
  };

  // Rule-specific fix instructions
  switch (violation.ruleId) {
    case 'no-unused-vars':
      instructions.fix_type = 'manual';
      instructions.fix_description = 'Remove unused variable or add usage';
      break;

    case 'prefer-const':
      instructions.fix_type = 'auto';
      instructions.fix_command = 'npx eslint --fix';
      instructions.after = violation.source.replace('let ', 'const ');
      break;

    case 'no-console':
      instructions.fix_type = 'manual';
      instructions.fix_description = 'Remove console.log or use proper logging';
      break;

    // Add more rule-specific instructions...
  }

  return instructions;
}
```

**5. Generate Violation Reports**
```markdown
## Code Style Violations Report

### Executive Summary
- **Total Violations**: 247
- **Critical (P0)**: 0 ✅
- **High (P1)**: 34
- **Medium (P2)**: 73
- **Low (P3)**: 140

### Auto-Fix Summary
- **Auto-fixable**: 189 (76.5%)
- **Semi-auto-fixable**: 23 (9.3%)
- **Manual fix required**: 35 (14.2%)

### Top 10 Worst Files
| File | Total | P0 | P1 | P2 | P3 |
|------|-------|----|----|----|----|
| src/api/order-processor.js | 45 | 0 | 12 | 18 | 15 |
| src/utils/data-transformer.js | 38 | 0 | 8 | 15 | 15 |
| src/api/user-controller.js | 32 | 0 | 6 | 12 | 14 |
| src/services/payment.js | 28 | 0 | 5 | 10 | 13 |
| src/utils/validator.js | 24 | 0 | 3 | 9 | 12 |

### Violations by Rule (Top 10)
| Rule | Count | Priority | Auto-Fix |
|------|-------|----------|----------|
| indent | 67 | P3 | ✅ Yes |
| no-unused-vars | 34 | P1 | ❌ No |
| prefer-const | 28 | P2 | ✅ Yes |
| no-console | 23 | P1 | ❌ No |
| quotes | 19 | P3 | ✅ Yes |
| semi | 17 | P3 | ✅ Yes |
| comma-dangle | 15 | P3 | ✅ Yes |
| no-var | 12 | P2 | ✅ Yes |
| eqeqeq | 8 | P1 | ⚠️ Partial |
| no-shadow | 6 | P1 | ❌ No |

### Critical Violations (P0) ✅
**None found** - Excellent!

### High Priority Violations (P1) - 34 Total

#### no-unused-vars (34 occurrences)
**Impact**: Dead code, maintenance burden, potential bugs

**Example**:
```javascript
// src/api/user-controller.js:45
const userId = req.params.id; // 'userId' is defined but never used
```

**Fix**: Remove unused variable or add usage

---

#### no-console (23 occurrences)
**Impact**: Console statements in production code

**Example**:
```javascript
// src/services/payment.js:78
console.log('Processing payment:', paymentData); // Unexpected console statement
```

**Fix**: Replace with proper logging (Winston, Bunyan)

### Medium Priority Violations (P2) - 73 Total

#### prefer-const (28 occurrences) - AUTO-FIXABLE ✅
**Impact**: Mutability when immutability intended

**Example**:
```javascript
// src/utils/calculator.js:23
let total = 0; // 'total' is never reassigned. Use 'const' instead
total = items.reduce((sum, item) => sum + item.price, 0);
```

**Fix**: Run `npx eslint --fix`

### Low Priority Violations (P3) - 140 Total

#### indent (67 occurrences) - AUTO-FIXABLE ✅
**Impact**: Inconsistent formatting

**Fix**: Run `npx prettier --write "**/*.js"`

### Fix Recommendations

#### Immediate Actions (Auto-Fix)
```bash
# Fix all auto-fixable ESLint issues (189 issues)
npx eslint . --fix

# Fix all Prettier formatting (147 files)
npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,md}"

# Verify fixes
npm run lint
npm run format:check
```

#### Manual Actions Required (35 issues)
1. Review and remove 34 unused variables
2. Replace 23 console.log statements with proper logging
3. Fix 6 variable shadowing issues
4. Address 8 eqeqeq violations (use === instead of ==)
```

**6. Export Multi-Format Reports**
```bash
# JSON (for CI/CD)
cat style-violations-report.json

# HTML (for viewing in browser)
npx eslint . --format html --output-file eslint-report.html

# Markdown (for documentation)
cat style-violations-report.md

# CSV (for spreadsheet analysis)
node scripts/export-violations-csv.js > violations.csv
```

**7. Store Violation Reports**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "style-violations-report.json" \
  --memory-key "swarm/code-analyzer/violations-report" \
  --metadata "{\"total_violations\": ${TOTAL}, \"auto_fixable_pct\": ${AUTO_FIX_PCT}}"
```

### Validation Gates
- ✅ All violations reported
- ✅ Violations prioritized
- ✅ Fix recommendations generated
- ✅ Multi-format exports created

### Expected Outputs
- `style-violations-report.json` - Complete violations data
- `style-violations-report.md` - Human-readable report
- `eslint-report.html` - HTML visualization
- `violations.csv` - Spreadsheet-friendly format

---

## Phase 4: Auto-Fix Issues

### Objective
Apply automated fixes for style violations that can be safely corrected without human judgment.

### Agent Configuration
```yaml
agent: code-analyzer
specialization: auto-fix
safety: non-destructive
```

### Execution Steps

**1. Initialize Auto-Fix**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "code-analyzer" \
  --description "Apply automated style fixes" \
  --task-type "auto-fix"
```

**2. Create Backup**
```bash
# Create backup before applying fixes
BACKUP_DIR="style-audit-backup-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup modified files
git diff --name-only | while read file; do
  mkdir -p "$BACKUP_DIR/$(dirname "$file")"
  cp "$file" "$BACKUP_DIR/$file"
done

echo "Backup created: $BACKUP_DIR"
```

**3. Apply ESLint Auto-Fixes**
```bash
# Apply all auto-fixable ESLint rules
npx eslint . --fix \
  --ext .js,.jsx,.ts,.tsx \
  --format json \
  --output-file eslint-fix-results.json

# Count fixed issues
FIXED_COUNT=$(jq '[.[] | .messages | .[] | select(.fix)] | length' eslint-fix-results.json)
echo "ESLint fixed: $FIXED_COUNT issues"
```

**4. Apply Prettier Formatting**
```bash
# Format all supported files
npx prettier --write "**/*.{js,jsx,ts,tsx,json,css,scss,md,yaml,yml}" \
  --log-level warn > prettier-fix-log.txt

# Count formatted files
FORMATTED_COUNT=$(grep -c "✅" prettier-fix-log.txt)
echo "Prettier formatted: $FORMATTED_COUNT files"
```

**5. Apply TypeScript Fixes**
```bash
# Apply TypeScript compiler fixes (where possible)
npx tsc --noEmit --pretty false 2>&1 | \
  node scripts/apply-typescript-fixes.js

# Note: Most TypeScript issues require manual intervention
```

**6. Apply Naming Convention Fixes (Safe)**
```javascript
// Safe automated naming fixes
const safeNamingFixes = {
  // File naming: PascalCase → kebab-case
  files: [
    { from: 'UserService.js', to: 'user-service.js' },
    { from: 'ApiClient.ts', to: 'api-client.ts' }
  ],

  // Only apply if no breaking changes
  safe_to_rename: true
};

// Apply file renames
function applyFileRenames() {
  safeNamingFixes.files.forEach(({ from, to }) => {
    if (fs.existsSync(from)) {
      // Check for imports/references
      const references = findReferences(from);

      if (references.length === 0 || canUpdateAllReferences(references)) {
        fs.renameSync(from, to);
        updateAllReferences(from, to, references);
        console.log(`Renamed: ${from} → ${to}`);
      } else {
        console.log(`Skipped: ${from} (has unmodifiable references)`);
      }
    }
  });
}
```

**7. Verify Fixes**
```bash
# Run linting again to verify
npx eslint . --format json > eslint-post-fix.json

# Compare before and after
node scripts/compare-violations.js \
  eslint-report.json \
  eslint-post-fix.json > fix-comparison.json

# Run tests to ensure no breakage
npm test
```

**8. Generate Fix Report**
```markdown
## Auto-Fix Results

### Summary
- **ESLint Fixes Applied**: 189 issues
- **Prettier Formatting**: 147 files
- **TypeScript Fixes**: 0 (manual required)
- **Naming Convention Fixes**: 0 (requires refactoring)

### ESLint Fixes
| Rule | Fixed | Remaining |
|------|-------|-----------|
| indent | 67 | 0 ✅ |
| prefer-const | 28 | 0 ✅ |
| quotes | 19 | 0 ✅ |
| semi | 17 | 0 ✅ |
| comma-dangle | 15 | 0 ✅ |
| no-var | 12 | 0 ✅ |
| **TOTAL AUTO-FIXED** | **189** | **0** ✅ |

### Prettier Formatting
- **Files formatted**: 147
- **Consistency achieved**: 100%
- **No formatting errors**: ✅

### Remaining Issues (Manual Fix Required)
- **no-unused-vars**: 34 occurrences
- **no-console**: 23 occurrences
- **eqeqeq**: 8 occurrences
- **no-shadow**: 6 occurrences
- **TOTAL MANUAL**: **71 issues**

### Tests Status
- **Unit tests**: ✅ All passing (342/342)
- **Integration tests**: ✅ All passing (89/89)
- **No regressions detected**: ✅

### Backup Location
`style-audit-backup-20250130-143022/`

### Next Steps
1. Review remaining 71 manual issues
2. Address high-priority (P1) violations first
3. Commit auto-fixed changes
4. Create issues/tasks for manual fixes
```

**9. Store Fix Results**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "auto-fix-report.json" \
  --memory-key "swarm/code-analyzer/auto-fix-results" \
  --metadata "{\"fixed_count\": ${FIXED_COUNT}, \"remaining_count\": ${REMAINING_COUNT}}"
```

### Validation Gates
- ✅ Backup created
- ✅ Auto-fixes applied
- ✅ Tests pass
- ✅ No regressions

### Expected Outputs
- `auto-fix-report.json` - Fix results summary
- `eslint-fix-results.json` - ESLint fixes details
- `prettier-fix-log.txt` - Prettier formatting log
- `fix-comparison.json` - Before/after comparison

---

## Phase 5: Validate Compliance

### Objective
Verify that all auto-fixes were applied correctly and confirm adherence to coding standards.

### Agent Configuration
```yaml
agent: reviewer
specialization: compliance-validation
verification: automated-tests
```

### Execution Steps

**1. Initialize Compliance Validation**
```bash
npx claude-flow@alpha hooks pre-task \
  --agent-id "reviewer" \
  --description "Validate style compliance after fixes" \
  --task-type "compliance-validation"
```

**2. Run Comprehensive Linting**
```bash
# ESLint validation
npx eslint . \
  --ext .js,.jsx,.ts,.tsx \
  --format json \
  --max-warnings 0 > eslint-validation.json

# Prettier validation
npx prettier --check "**/*.{js,jsx,ts,tsx,json,css,md}" > prettier-validation.txt

# TypeScript validation
npx tsc --noEmit --strict > typescript-validation.txt
```

**3. Calculate Compliance Metrics**
```javascript
// Compliance calculation
const complianceMetrics = {
  eslint: {
    total_rules: 247,
    passing_rules: 0,
    failing_rules: 0,
    compliance_pct: 0
  },

  prettier: {
    total_files: 0,
    formatted_files: 0,
    unformatted_files: 0,
    compliance_pct: 0
  },

  typescript: {
    total_files: 0,
    error_free_files: 0,
    files_with_errors: 0,
    compliance_pct: 0
  },

  naming_conventions: {
    total_identifiers: 0,
    compliant_identifiers: 0,
    non_compliant_identifiers: 0,
    compliance_pct: 0
  },

  overall_compliance_pct: 0
};

// Calculate overall compliance
function calculateCompliance() {
  // ESLint compliance
  const eslintViolations = require('./eslint-validation.json');
  const totalIssues = eslintViolations.reduce((sum, file) =>
    sum + file.messages.length, 0
  );
  complianceMetrics.eslint.failing_rules = totalIssues;
  complianceMetrics.eslint.compliance_pct =
    ((complianceMetrics.eslint.total_rules - totalIssues) /
     complianceMetrics.eslint.total_rules) * 100;

  // Prettier compliance
  const prettierViolations = fs.readFileSync('prettier-validation.txt', 'utf8');
  const unformattedFiles = prettierViolations.split('\n').filter(Boolean).length;
  complianceMetrics.prettier.unformatted_files = unformattedFiles;
  complianceMetrics.prettier.compliance_pct =
    ((complianceMetrics.prettier.total_files - unformattedFiles) /
     complianceMetrics.prettier.total_files) * 100;

  // Calculate weighted overall compliance
  complianceMetrics.overall_compliance_pct = (
    complianceMetrics.eslint.compliance_pct * 0.50 +
    complianceMetrics.prettier.compliance_pct * 0.30 +
    complianceMetrics.typescript.compliance_pct * 0.20
  );
}
```

**4. Run Test Suite**
```bash
# Verify no regressions from auto-fixes
npm run test:all -- --coverage

# Check for test failures
if [ $? -ne 0 ]; then
  echo "❌ Tests failed after auto-fix"
  echo "Rolling back changes..."
  git restore .
  exit 1
fi
```

**5. Validate Build**
```bash
# Ensure project still builds
npm run build

# Check build size (ensure no significant increase)
BUILD_SIZE=$(du -sh dist/ | cut -f1)
echo "Build size: $BUILD_SIZE"
```

**6. Generate Compliance Report**
```markdown
## Style Compliance Validation Report

### Overall Compliance: 91.2% ✅

### Compliance by Category
| Category | Compliance | Status |
|----------|------------|--------|
| ESLint Rules | 95.8% | ✅ PASS (Threshold: 90%) |
| Prettier Formatting | 100% | ✅ PASS (Threshold: 100%) |
| TypeScript Strictness | 76.4% | ⚠️ WARN (Threshold: 80%) |
| Naming Conventions | 89.2% | ⚠️ WARN (Threshold: 90%) |

### ESLint Compliance
- **Total files scanned**: 247
- **Files with violations**: 11
- **Remaining violations**: 58 (down from 247)
- **Reduction**: 76.5%

#### Remaining Violations Breakdown
| Rule | Count | Priority |
|------|-------|----------|
| no-unused-vars | 34 | P1 |
| no-console | 23 | P1 |
| eqeqeq | 8 | P1 |
| no-shadow | 6 | P1 |

### Prettier Compliance
- **Total files**: 247
- **Properly formatted**: 247 (100%)
- **Consistency**: ✅ Perfect

### TypeScript Compliance
- **Files with type errors**: 18
- **Explicit `any` types**: 23
- **Implicit `any` warnings**: 31
- **Recommendation**: Enable strict mode incrementally

### Naming Conventions
- **Total identifiers**: 1,247
- **Compliant**: 1,112 (89.2%)
- **Non-compliant**: 135 (10.8%)
  - File names: 23
  - Class names: 12
  - Function names: 18
  - Variable names: 82

### Test Results
- **Unit tests**: ✅ 342/342 passing
- **Integration tests**: ✅ 89/89 passing
- **E2E tests**: ✅ 42/42 passing
- **Coverage**: 91.2% (no change)

### Build Validation
- **Build status**: ✅ Success
- **Build size**: 2.4MB (no change)
- **Build time**: 47.3s (no change)

### Compliance Gates
| Gate | Threshold | Current | Status |
|------|-----------|---------|--------|
| Overall Compliance | ≥90% | 91.2% | ✅ PASS |
| ESLint Compliance | ≥90% | 95.8% | ✅ PASS |
| Prettier Compliance | 100% | 100% | ✅ PASS |
| Tests Passing | 100% | 100% | ✅ PASS |
| No Build Errors | True | True | ✅ PASS |

### Next Steps
1. Address remaining 58 manual violations (P1 priority)
2. Enable TypeScript strict mode incrementally
3. Refactor naming convention violations
4. Schedule quarterly style audits
```

**7. Store Compliance Results**
```bash
npx claude-flow@alpha hooks post-edit \
  --file "compliance-validation-report.json" \
  --memory-key "swarm/reviewer/compliance-validation" \
  --metadata "{\"compliance_pct\": ${COMPLIANCE_PCT}, \"remaining_violations\": ${REMAINING}}"
```

**8. Commit Fixed Changes**
```bash
# Stage all auto-fixed files
git add .

# Commit with detailed message
git commit -m "style: Apply automated style fixes

- ESLint auto-fixes: 189 issues resolved
- Prettier formatting: 147 files formatted
- Remaining manual fixes: 58 issues
- All tests passing
- Build verified

Audit ID: ${AUDIT_ID}
Compliance: 91.2%"
```

### Validation Gates
- ✅ Overall compliance ≥90%
- ✅ All tests passing
- ✅ Build successful
- ✅ No regressions

### Expected Outputs
- `compliance-validation-report.json` - Compliance metrics
- `eslint-validation.json` - Final ESLint status
- `prettier-validation.txt` - Final Prettier status
- Git commit with auto-fixes applied

---

## Final Session Cleanup

```bash
# Export complete audit session
npx claude-flow@alpha hooks session-end \
  --session-id "style-audit-${AUDIT_ID}" \
  --export-metrics true \
  --export-path "./style-audit-summary.json"

# Notify completion
npx claude-flow@alpha hooks notify \
  --message "Style audit complete: ${COMPLIANCE_PCT}% compliance" \
  --level "info" \
  --metadata "{\"fixed\": ${FIXED_COUNT}, \"remaining\": ${REMAINING_COUNT}}"
```

---

## Memory Patterns

### Storage Keys
```yaml
swarm/code-analyzer/scan-results:
  total_violations: number
  auto_fixable: number
  manual_required: number
  scan_timestamp: string

swarm/reviewer/standards-comparison:
  compliance_pct: number
  missing_rules: array
  config_recommendations: array

swarm/code-analyzer/violations-report:
  prioritized_violations: object
  worst_files: array
  fix_recommendations: object

swarm/code-analyzer/auto-fix-results:
  fixed_count: number
  remaining_count: number
  backup_location: string

swarm/reviewer/compliance-validation:
  overall_compliance_pct: number
  remaining_violations: number
  tests_passing: boolean
  build_successful: boolean
```

---

## Evidence-Based Validation

### Success Criteria
- ✅ Complete codebase scanned
- ✅ Violations identified and prioritized
- ✅ Auto-fixes applied safely
- ✅ Compliance ≥90%
- ✅ All tests passing
- ✅ No build regressions

### Metrics Tracking
```javascript
{
  "audit_duration_minutes": 25,
  "agents_used": 2,
  "total_violations_found": 247,
  "violations_auto_fixed": 189,
  "violations_remaining": 58,
  "compliance_before": 61.3,
  "compliance_after": 91.2,
  "improvement": 29.9
}
```

---

## Usage Examples

### Basic Style Audit
```bash
# Run complete style audit with auto-fix
npm run style:audit

# View compliance report
cat compliance-validation-report.md
```

### CI/CD Integration
```yaml
# .github/workflows/style-audit.yml
name: Style Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run Style Audit
        run: npm run style:audit
      - name: Check Compliance
        run: |
          COMPLIANCE=$(jq '.overall_compliance_pct' style-audit-summary.json)
          if [ "$COMPLIANCE" -lt 90 ]; then exit 1; fi
```

---

## Related Skills

- `when-reviewing-code-comprehensively-use-code-review-assistant`
- `when-verifying-quality-use-verification-quality`
- `when-ensuring-production-ready-use-production-readiness`

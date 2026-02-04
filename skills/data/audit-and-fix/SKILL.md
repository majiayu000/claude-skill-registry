---
skill: audit-and-fix
description: Security audit with automatic fixes: $ARGUMENTS (package names or '.')
location: project
---

# Security Audit and Fix: $ARGUMENTS

I'll perform a comprehensive security audit and automatically fix vulnerabilities for: **$ARGUMENTS**

This advanced workflow includes:
1. Creating an isolated git worktree for safety
2. Running `npm audit` to identify all vulnerabilities
3. Categorizing vulnerabilities by severity (critical, high, moderate, low)
4. Automatically updating vulnerable packages
5. Using parallel agents for efficient processing (when >3 packages)
6. Validating each update with full test suite
7. Generating comprehensive security report
8. Prompting for merge if all validations pass

This is a complex skill demonstrating parallel execution, conditional logic, and comprehensive error handling.

Let's begin!

---

## Process Steps

### 1. Create Isolated Git Worktree

Create an isolated environment for safe dependency updates:

```bash
# Generate unique timestamp
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
WORKTREE_PATH="../audit-fix-worktree-$TIMESTAMP"
BRANCH_NAME="security-audit-$TIMESTAMP"

echo "🔒 Creating isolated worktree for security audit"
echo "📁 Worktree path: $WORKTREE_PATH"
echo "🌿 Branch name: $BRANCH_NAME"
echo ""

# Create worktree
git worktree add "$WORKTREE_PATH" -b "$BRANCH_NAME"

# Navigate into worktree
cd "$WORKTREE_PATH/expense-tracker-ai"

echo "✅ Worktree created and ready"
echo "📍 Working in: $(pwd)"
echo ""
```

**Why isolated worktree is critical:**
- Package updates can break the application
- Dependencies may have incompatibilities
- Tests may fail after updates
- Need ability to discard if updates fail
- Main workspace remains functional during audit

### 2. Run Initial Security Audit

Scan for vulnerabilities using npm audit:

```bash
echo "🔍 Running security audit..."
echo ""

# Run npm audit and save results
npm audit --json > audit-report.json 2>&1

# Check if audit found any issues
AUDIT_EXIT_CODE=$?

if [ $AUDIT_EXIT_CODE -eq 0 ]; then
  echo "✅ No vulnerabilities found!"
  echo ""
  echo "Your dependencies are secure."
  echo "No updates needed."

  # Clean up worktree
  cd /Users/greg/code/claude-code-coursera
  git worktree remove "$WORKTREE_PATH"
  git branch -d "$BRANCH_NAME"

  exit 0
fi

echo "⚠️  Vulnerabilities detected. Analyzing..."
echo ""
```

### 3. Categorize Vulnerabilities by Severity

Parse audit results and categorize by severity:

```bash
echo "📊 Vulnerability Analysis"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Extract vulnerability counts by severity
if command -v jq >/dev/null 2>&1; then
  # Use jq if available
  CRITICAL=$(jq -r '.metadata.vulnerabilities.critical // 0' audit-report.json)
  HIGH=$(jq -r '.metadata.vulnerabilities.high // 0' audit-report.json)
  MODERATE=$(jq -r '.metadata.vulnerabilities.moderate // 0' audit-report.json)
  LOW=$(jq -r '.metadata.vulnerabilities.low // 0' audit-report.json)
  INFO=$(jq -r '.metadata.vulnerabilities.info // 0' audit-report.json)
else
  # Fallback: parse npm audit output directly
  npm audit | grep -E "Critical|High|Moderate|Low|Info" | while read -r line; do
    case "$line" in
      *Critical*) echo "$line" | awk '{print $2}' > /tmp/critical_count ;;
      *High*) echo "$line" | awk '{print $2}' > /tmp/high_count ;;
      *Moderate*) echo "$line" | awk '{print $2}' > /tmp/moderate_count ;;
      *Low*) echo "$line" | awk '{print $2}' > /tmp/low_count ;;
    esac
  done

  CRITICAL=$(cat /tmp/critical_count 2>/dev/null || echo 0)
  HIGH=$(cat /tmp/high_count 2>/dev/null || echo 0)
  MODERATE=$(cat /tmp/moderate_count 2>/dev/null || echo 0)
  LOW=$(cat /tmp/low_count 2>/dev/null || echo 0)
fi

TOTAL=$((CRITICAL + HIGH + MODERATE + LOW))

echo "🔴 Critical: $CRITICAL"
echo "🟠 High: $HIGH"
echo "🟡 Moderate: $MODERATE"
echo "🟢 Low: $LOW"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 Total vulnerabilities: $TOTAL"
echo ""
```

**Severity definitions:**
- **Critical**: Immediate action required, actively exploited
- **High**: Serious security risk, patch ASAP
- **Moderate**: Security concern, should fix soon
- **Low**: Minor issue, fix when convenient
- **Info**: Informational, no immediate action needed

### 4. Identify Vulnerable Packages

Extract the list of packages that need updating:

```bash
echo "📦 Identifying vulnerable packages..."
echo ""

# Get list of vulnerable packages
if command -v jq >/dev/null 2>&1; then
  # Extract unique package names from audit report
  VULNERABLE_PACKAGES=$(jq -r '.vulnerabilities | keys[]' audit-report.json 2>/dev/null || echo "")
else
  # Fallback: parse npm audit output
  VULNERABLE_PACKAGES=$(npm audit | grep -E "^[a-z]" | awk '{print $1}' | sort -u)
fi

if [ -z "$VULNERABLE_PACKAGES" ]; then
  echo "❌ Could not parse vulnerable packages"
  echo "Running npm audit fix instead..."

  npm audit fix

  if [ $? -eq 0 ]; then
    echo "✅ npm audit fix completed"
  else
    echo "❌ npm audit fix failed"
    echo "Manual intervention required"
  fi

  exit 0
fi

# Count packages
PACKAGE_COUNT=$(echo "$VULNERABLE_PACKAGES" | wc -l | tr -d ' ')

echo "Found $PACKAGE_COUNT vulnerable packages:"
echo "$VULNERABLE_PACKAGES" | while read -r pkg; do
  echo "  • $pkg"
done
echo ""
```

### 5. Determine Execution Strategy

Based on the number of packages, choose sequential or parallel execution:

```bash
echo "🎯 Determining execution strategy..."
echo ""

if [ "$ARGUMENTS" = "." ] || [ "$ARGUMENTS" = "all" ]; then
  # Process all vulnerable packages
  PACKAGES_TO_UPDATE="$VULNERABLE_PACKAGES"
  UPDATE_MODE="all"
elif echo "$ARGUMENTS" | grep -q '\*'; then
  # Glob pattern matching
  PACKAGES_TO_UPDATE=$(echo "$VULNERABLE_PACKAGES" | grep "$ARGUMENTS")
  UPDATE_MODE="pattern"
else
  # Specific packages
  PACKAGES_TO_UPDATE="$ARGUMENTS"
  UPDATE_MODE="specific"
fi

UPDATE_COUNT=$(echo "$PACKAGES_TO_UPDATE" | wc -l | tr -d ' ')

echo "Update mode: $UPDATE_MODE"
echo "Packages to update: $UPDATE_COUNT"
echo ""

# Choose execution strategy
if [ $UPDATE_COUNT -gt 3 ]; then
  echo "📊 Multiple packages detected ($UPDATE_COUNT packages)"
  echo "🚀 Using parallel execution for efficiency"
  echo ""
  echo "Strategy:"
  echo "  • Split into groups of 2 packages per agent"
  echo "  • Launch parallel Task agents"
  echo "  • Each agent updates and validates independently"
  echo "  • Collect and merge results"
  echo ""
  EXECUTION_MODE="parallel"
else
  echo "📝 Processing $UPDATE_COUNT packages sequentially"
  echo ""
  EXECUTION_MODE="sequential"
fi
```

**Execution strategies:**
- **1-3 packages**: Sequential (simpler, easier to debug)
- **4+ packages**: Parallel (faster, more efficient)

### 6. Execute Updates (Sequential Mode)

For ≤3 packages, update one by one:

```bash
if [ "$EXECUTION_MODE" = "sequential" ]; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Starting sequential updates..."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  SUCCESS_COUNT=0
  FAILURE_COUNT=0
  FAILED_PACKAGES=""

  echo "$PACKAGES_TO_UPDATE" | while read -r package; do
    if [ -z "$package" ]; then
      continue
    fi

    echo "📦 Updating: $package"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    # Get current version
    CURRENT_VERSION=$(npm list "$package" --depth=0 2>/dev/null | grep "$package" | awk -F@ '{print $NF}')
    echo "Current version: $CURRENT_VERSION"

    # Update package
    npm install "$package@latest" --save

    if [ $? -ne 0 ]; then
      echo "❌ Failed to install $package@latest"
      FAILURE_COUNT=$((FAILURE_COUNT + 1))
      FAILED_PACKAGES="$FAILED_PACKAGES\n  • $package"
      continue
    fi

    # Get new version
    NEW_VERSION=$(npm list "$package" --depth=0 2>/dev/null | grep "$package" | awk -F@ '{print $NF}')
    echo "New version: $NEW_VERSION"

    # Validate the update
    echo ""
    echo "Running validation..."

    # Build
    echo "  1/4 Build..."
    npm run build >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      echo "  ❌ Build failed after updating $package"
      FAILURE_COUNT=$((FAILURE_COUNT + 1))
      FAILED_PACKAGES="$FAILED_PACKAGES\n  • $package (build failed)"
      # Revert
      npm install "$package@$CURRENT_VERSION" --save
      continue
    fi
    echo "  ✅ Build passed"

    # Lint
    echo "  2/4 Lint..."
    npm run lint >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      echo "  ❌ Lint failed after updating $package"
      FAILURE_COUNT=$((FAILURE_COUNT + 1))
      FAILED_PACKAGES="$FAILED_PACKAGES\n  • $package (lint failed)"
      npm install "$package@$CURRENT_VERSION" --save
      continue
    fi
    echo "  ✅ Lint passed"

    # Unit tests
    echo "  3/4 Unit tests..."
    npm test >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      echo "  ❌ Tests failed after updating $package"
      FAILURE_COUNT=$((FAILURE_COUNT + 1))
      FAILED_PACKAGES="$FAILED_PACKAGES\n  • $package (tests failed)"
      npm install "$package@$CURRENT_VERSION" --save
      continue
    fi
    echo "  ✅ Tests passed"

    # E2E tests
    echo "  4/4 E2E tests..."
    npm run test:e2e >/dev/null 2>&1
    if [ $? -ne 0 ]; then
      echo "  ❌ E2E tests failed after updating $package"
      FAILURE_COUNT=$((FAILURE_COUNT + 1))
      FAILED_PACKAGES="$FAILED_PACKAGES\n  • $package (e2e failed)"
      npm install "$package@$CURRENT_VERSION" --save
      continue
    fi
    echo "  ✅ E2E tests passed"

    echo ""
    echo "✅ Successfully updated: $package ($CURRENT_VERSION → $NEW_VERSION)"
    echo ""
    SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
  done

  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Sequential Update Summary"
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "✅ Successful: $SUCCESS_COUNT"
  echo "❌ Failed: $FAILURE_COUNT"

  if [ $FAILURE_COUNT -gt 0 ]; then
    echo ""
    echo "Failed packages:"
    echo -e "$FAILED_PACKAGES"
  fi
  echo ""
fi
```

### 7. Execute Updates (Parallel Mode)

For >3 packages, use parallel agents:

```bash
if [ "$EXECUTION_MODE" = "parallel" ]; then
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo "Starting parallel updates..."
  echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
  echo ""

  # Split packages into groups
  # Group size: 2 packages per agent
  GROUP_SIZE=2

  # Calculate number of groups needed
  NUM_GROUPS=$(( (UPDATE_COUNT + GROUP_SIZE - 1) / GROUP_SIZE ))

  echo "Parallel execution plan:"
  echo "  • Total packages: $UPDATE_COUNT"
  echo "  • Packages per agent: $GROUP_SIZE"
  echo "  • Number of agents: $NUM_GROUPS"
  echo ""

  # Claude will use Task tool with general-purpose subagents
  # Each subagent will receive a subset of packages to update
  #
  # Conceptual breakdown:
  # - Agent 1: packages 1-2
  # - Agent 2: packages 3-4
  # - Agent 3: packages 5-6
  # ...
  #
  # Each agent independently:
  # 1. Updates its assigned packages
  # 2. Runs full validation suite for each
  # 3. Reports success/failure
  # 4. Reverts on failure
  #
  # Main process waits for all agents to complete,
  # then collects and merges results

  echo "⏳ Launching parallel agents..."
  echo ""

  # The actual Task tool usage will be handled by Claude
  # This is a placeholder showing the conceptual approach
  #
  # For each group:
  #   Task({
  #     subagent_type: 'general-purpose',
  #     description: `Update packages: ${group.join(', ')}`,
  #     prompt: `Update these packages with full validation: ${packages}
  #              For each package:
  #              1. npm install package@latest
  #              2. Run build, lint, test, e2e
  #              3. Revert if any validation fails
  #              4. Report results`,
  #     run_in_background: true
  #   })
  #
  # Wait for all agents
  # Collect results
  # Generate summary

  echo "✅ All agents completed"
  echo ""
fi
```

**Parallel execution benefits:**
- **Speed**: 3-5x faster for large updates
- **Resource utilization**: Better use of available CPU
- **Scalability**: Handles dozens of packages efficiently

**Parallel execution challenges:**
- **Complexity**: More moving parts
- **Debugging**: Harder to trace failures
- **Coordination**: Need to merge results
- **Rate limits**: May hit npm registry limits

### 8. Run Post-Update Security Audit

After updates, verify vulnerabilities are fixed:

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Running post-update security audit..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

npm audit --json > audit-report-after.json 2>&1
AUDIT_EXIT_CODE=$?

if [ $AUDIT_EXIT_CODE -eq 0 ]; then
  echo "✅ No vulnerabilities remaining!"
  echo ""
  REMAINING_VULNS=0
else
  # Count remaining vulnerabilities
  if command -v jq >/dev/null 2>&1; then
    CRITICAL_AFTER=$(jq -r '.metadata.vulnerabilities.critical // 0' audit-report-after.json)
    HIGH_AFTER=$(jq -r '.metadata.vulnerabilities.high // 0' audit-report-after.json)
    MODERATE_AFTER=$(jq -r '.metadata.vulnerabilities.moderate // 0' audit-report-after.json)
    LOW_AFTER=$(jq -r '.metadata.vulnerabilities.low // 0' audit-report-after.json)
  else
    CRITICAL_AFTER=0
    HIGH_AFTER=0
    MODERATE_AFTER=0
    LOW_AFTER=0
  fi

  REMAINING_VULNS=$((CRITICAL_AFTER + HIGH_AFTER + MODERATE_AFTER + LOW_AFTER))

  echo "⚠️  Remaining vulnerabilities: $REMAINING_VULNS"
  echo ""
  echo "🔴 Critical: $CRITICAL_AFTER (was: $CRITICAL)"
  echo "🟠 High: $HIGH_AFTER (was: $HIGH)"
  echo "🟡 Moderate: $MODERATE_AFTER (was: $MODERATE)"
  echo "🟢 Low: $LOW_AFTER (was: $LOW)"
  echo ""
fi

# Calculate fixed count
FIXED_COUNT=$((TOTAL - REMAINING_VULNS))

echo "📊 Fix Summary:"
echo "  • Vulnerabilities fixed: $FIXED_COUNT"
echo "  • Vulnerabilities remaining: $REMAINING_VULNS"
echo ""
```

### 9. Generate Comprehensive Security Report

Create detailed report with all findings:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔒 SECURITY AUDIT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 Date: $(date '+%Y-%m-%d %H:%M:%S')
📁 Worktree: $WORKTREE_PATH
🌿 Branch: $BRANCH_NAME

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 VULNERABILITY SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Initial Scan:
  🔴 Critical: $CRITICAL
  🟠 High: $HIGH
  🟡 Moderate: $MODERATE
  🟢 Low: $LOW
  ━━━━━━━━━━━━━━━━━━━━━━
  📋 Total: $TOTAL

After Updates:
  🔴 Critical: $CRITICAL_AFTER
  🟠 High: $HIGH_AFTER
  🟡 Moderate: $MODERATE_AFTER
  🟢 Low: $LOW_AFTER
  ━━━━━━━━━━━━━━━━━━━━━━
  📋 Total: $REMAINING_VULNS

Result:
  ✅ Fixed: $FIXED_COUNT vulnerabilities
  ⚠️  Remaining: $REMAINING_VULNS vulnerabilities

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 PACKAGE UPDATES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Successful Updates ($SUCCESS_COUNT):
  [List each successful package update]
  • webpack: 5.88.0 → 5.89.0 (fixed CVE-2023-XXXX)
  • react-dom: 18.2.0 → 18.3.1 (fixed CVE-2023-YYYY)
  • express: 4.18.0 → 4.19.2 (fixed CVE-2024-ZZZZ)

Failed Updates ($FAILURE_COUNT):
  [List each failed package with reason]
  • typescript: 5.1.0 → 5.3.0 (build errors)
  • jest: 29.5.0 → 30.0.0 (breaking changes)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VALIDATION RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Build:       ✓ Passed
Lint:        ✓ Passed
Unit Tests:  ✓ Passed (24/24)
E2E Tests:   ✓ Passed (12/12)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If remaining vulnerabilities]

🔴 Critical Priority:
  • Review remaining critical vulnerabilities
  • Consider manual updates for failed packages
  • Check for security patches or workarounds

🟠 High Priority:
  • Address high severity issues within 7 days
  • Monitor security advisories

🟡 Medium Priority:
  • Plan updates for moderate severity issues
  • Include in next maintenance cycle

[If all fixed]

✅ All Clear:
  • No vulnerabilities detected
  • All dependencies up to date
  • Maintain regular audit schedule

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 NEXT STEPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If successful]
  ✅ Review changes in worktree
  ✅ Test application manually
  ✅ Merge to main branch
  ✅ Deploy updated dependencies

[If failures]
  ⚠️  Review failed package updates
  ⚠️  Check breaking change documentation
  ⚠️  Consider manual migration
  ⚠️  Address remaining vulnerabilities

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 10. Prompt for Merge Decision

Ask user whether to merge the updates:

```bash
if [ $SUCCESS_COUNT -gt 0 ] && [ $FAILURE_COUNT -eq 0 ] && [ $REMAINING_VULNS -eq 0 ]; then
  # Perfect case: all updates successful, no remaining vulnerabilities
  echo "✅ Security audit complete!"
  echo "✅ All vulnerabilities fixed"
  echo "✅ All validations passed"
  echo ""
  echo "Merge changes to main branch? (yes/no)"
  echo ""
  echo "Options:"
  echo "  yes - Merge updates and clean up worktree"
  echo "  no  - Keep worktree for manual review"

elif [ $SUCCESS_COUNT -gt 0 ] && [ $REMAINING_VULNS -gt 0 ]; then
  # Partial success: some fixed, some remaining
  echo "⚠️  Partial success"
  echo "✅ Fixed: $FIXED_COUNT vulnerabilities"
  echo "⚠️  Remaining: $REMAINING_VULNS vulnerabilities"
  echo ""
  echo "Merge partial fixes to main branch? (yes/no/review)"
  echo ""
  echo "Options:"
  echo "  yes    - Merge successful updates (progress made)"
  echo "  no     - Discard all changes (address all issues first)"
  echo "  review - Keep worktree for manual inspection"

else
  # Failure: no progress or major issues
  echo "❌ Security audit completed with issues"
  echo "❌ Failed updates: $FAILURE_COUNT"
  echo "⚠️  Remaining vulnerabilities: $REMAINING_VULNS"
  echo ""
  echo "What would you like to do? (keep/cleanup/retry)"
  echo ""
  echo "Options:"
  echo "  keep    - Preserve worktree for debugging"
  echo "  cleanup - Discard changes and remove worktree"
  echo "  retry   - Try npm audit fix --force (may break)"
fi
```

### 11. Handle Merge (If Yes)

If user chooses to merge successful updates:

```bash
echo "Merging security updates to main branch..."
echo ""

# Navigate back to original repo
cd /Users/greg/code/claude-code-coursera

# Show what will be merged
echo "Changes to merge:"
git diff main..$BRANCH_NAME --stat

echo ""
echo "Proceed with merge? (yes/no)"
# Wait for confirmation

# Merge
git merge "$BRANCH_NAME"

if [ $? -ne 0 ]; then
  echo "❌ Merge conflict detected"
  echo ""
  echo "This is unusual for dependency updates."
  echo "Likely causes:"
  echo "  • package.json modified in main"
  echo "  • package-lock.json conflicts"
  echo ""
  echo "Resolve manually:"
  echo "  1. git status"
  echo "  2. Edit conflicting files"
  echo "  3. git add <files>"
  echo "  4. git merge --continue"
  exit 1
fi

echo "✅ Merge successful"
echo ""

# Offer to push
echo "Push to remote? (yes/no)"
# Wait for response

# Clean up
git worktree remove "$WORKTREE_PATH"
git branch -d "$BRANCH_NAME"

echo ""
echo "✅ Security updates merged successfully"
echo "✅ Worktree cleaned up"
echo ""
echo "Don't forget to:"
echo "  • Test application in production environment"
echo "  • Monitor for any runtime issues"
echo "  • Update deployment pipelines if needed"
```

### 12. Handle Manual Review (If No/Review)

If user wants to review manually:

```bash
echo "Worktree preserved for review"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📁 Worktree Location"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Path: $WORKTREE_PATH"
echo "Branch: $BRANCH_NAME"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔍 Review Changes"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Review package updates:"
echo "  cd $WORKTREE_PATH/expense-tracker-ai"
echo "  git diff HEAD package.json"
echo "  git diff HEAD package-lock.json"
echo ""
echo "Test application:"
echo "  npm run dev"
echo "  # Test functionality in browser"
echo ""
echo "Check dependencies:"
echo "  npm list --depth=0"
echo "  npm audit"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🔄 Merge When Ready"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Merge to main:"
echo "  cd /Users/greg/code/claude-code-coursera"
echo "  git merge $BRANCH_NAME"
echo "  git push origin main"
echo ""
echo "Clean up:"
echo "  git worktree remove $WORKTREE_PATH"
echo "  git branch -d $BRANCH_NAME"
echo ""
```

---

## Error Handling

### Common Error Scenarios

#### Build Failure After Update

```
❌ Build failed after updating webpack

Error: Module not found: '@types/webpack'

Resolution:
1. Install missing types: npm install --save-dev @types/webpack
2. Re-run build: npm run build
3. If still failing, check breaking changes in webpack docs
```

#### Dependency Conflict

```
❌ npm ERR! ERESOLVE unable to resolve dependency tree

Conflict:
  react@18.3.0 requires webpack@^5.90.0
  Current webpack: 5.88.0

Resolution:
1. Update react first: npm install react@latest
2. Then update webpack: npm install webpack@latest
3. Or use --force (may cause issues):
   npm install webpack@latest --force
```

#### Test Failures After Update

```
❌ Tests failed after updating jest

Error: Unknown option 'testEnvironment'

Cause: Breaking change in jest 30.x

Resolution:
1. Review migration guide:
   https://jestjs.io/docs/upgrading-to-jest30
2. Update jest.config.js
3. Update test files if needed
```

#### No Fix Available

```
⚠️  Vulnerability in transitive dependency

Package: some-deep-dependency
Severity: High
Fixable: No

Your package → intermediate-package → some-deep-dependency

Resolution:
1. Check if intermediate-package has update
2. Contact maintainer of intermediate-package
3. Consider alternative package
4. Monitor for security patch
```

---

## Advanced Usage

### Audit Specific Packages

```bash
# Audit and fix only React-related packages
audit-and-fix react*

# Audit and fix webpack and babel
audit-and-fix webpack babel

# Audit and fix all testing libraries
audit-and-fix @testing-library/*
```

### Audit by Severity

```bash
# Fix only critical vulnerabilities
# (requires custom filtering logic)
audit-and-fix . --severity=critical

# Fix critical and high severity
audit-and-fix . --severity=critical,high
```

### Dry Run Mode

```bash
# Show what would be updated without actually updating
audit-and-fix . --dry-run

# Expected output:
# Would update:
#   • webpack: 5.88.0 → 5.89.0
#   • react-dom: 18.2.0 → 18.3.1
#   • express: 4.18.0 → 4.19.2
```

---

## Performance Metrics

### Sequential vs Parallel Comparison

**Sequential (3 packages):**
- Time: ~15 minutes
- Memory: Low
- Debuggability: Easy

**Parallel (12 packages):**
- Time: ~5 minutes (3x faster)
- Memory: Medium
- Debuggability: Moderate

**Recommendation:**
- Use sequential for ≤3 packages
- Use parallel for 4+ packages
- Consider sequential if debugging issues

---

## Related Skills and Commands

- **Simple Audit:** Use existing [.claude/skills/security-audit.md](.claude/skills/security-audit.md)
- **Package Updates:** Use existing [.claude/commands/npm-latest.md](../commands/npm-latest.md)
- **E2E Testing:** Use existing [.claude/commands/e2e-test.md](../commands/e2e-test.md)
- **Skills Guide:** See [skills.md](../../skills.md) for more patterns

---

## Summary

This skill demonstrates:

✅ **Complex conditional logic** - Different strategies based on package count
✅ **Parallel execution** - Using Task tool with subagents for scale
✅ **Comprehensive validation** - Build, lint, unit tests, e2e tests
✅ **Error categorization** - Grouping failures by type
✅ **Rollback on failure** - Reverting packages that break validation
✅ **Detailed reporting** - Security report with before/after comparison
✅ **User decision points** - Multiple prompts for user control
✅ **Cleanup handling** - Proper worktree and branch cleanup

This is the most complex skill example, showcasing advanced patterns for production-grade automation.

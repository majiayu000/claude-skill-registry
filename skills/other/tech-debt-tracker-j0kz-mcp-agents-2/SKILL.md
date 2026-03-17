---
name: tech-debt-tracker
description: Track, prioritize, and pay down technical debt systematically in ANY project. Use when quantifying debt, prioritizing fixes, or convincing management to invest in improvements.
---

# Tech Debt Tracker - Manage Technical Debt Like Financial Debt

## 🎯 When to Use This Skill

Use when you need to:

- Convince management to allocate time for refactoring
- Prioritize which debt to pay first
- Track debt accumulation over time
- Plan refactoring sprints
- Balance feature work with maintenance
- Document "why" behind technical decisions

## ⚡ Quick Debt Assessment (5 minutes)

### WITH MCP Tools:

```
"Analyze technical debt in this codebase"
"Find code quality issues and prioritize them"
```

### WITHOUT MCP - Quick Scan:

```bash
# 1. Code complexity (high complexity = debt)
find . -name "*.js" -exec wc -l {} + | sort -rn | head -10

# 2. Old dependencies (security debt)
npm outdated
# or
pip list --outdated

# 3. TODO/FIXME count (acknowledged debt)
grep -r "TODO\|FIXME\|HACK\|XXX" --include="*.js" | wc -l

# 4. Test coverage (testing debt)
npm test -- --coverage | grep "All files"

# 5. Duplicate code (DRY debt)
# Install: npm install -g jscpd
jscpd . --min-lines 10 --min-tokens 50
```

## 📊 The Technical Debt Quadrant

```
         RECKLESS           |        PRUDENT
    ---------------------|----------------------
    "We don't have       |  "We must ship now
     time for design"    |   and deal with
DELIBERATE                |   consequences"
    ---------------------|----------------------
    "What's layering?"   |  "Now we know how
                        |   we should have
INADVERTENT             |   done it"
```

## 📝 Technical Debt Registry

### Create a Debt Log (`TECH_DEBT.md`):

```markdown
# Technical Debt Registry

## Critical (P0) - Immediate Action Required

### 1. SQL Injection Vulnerability in User Search

- **Location**: `api/search.js:45-67`
- **Impact**: High - Security risk
- **Effort**: 2 hours
- **Interest Rate**: Compounds daily (attack risk)
- **Solution**: Use parameterized queries
- **Owner**: Security Team
- **Deadline**: This sprint

## High (P1) - Plan This Quarter

### 2. No Caching Layer

- **Location**: Entire API
- **Impact**: High - Performance, costs
- **Effort**: 1 week
- **Interest Rate**: $500/month in server costs
- **Solution**: Implement Redis caching
- **Owner**: Backend Team
- **Deadline**: Q2 2024

## Medium (P2) - Schedule When Possible

### 3. Callback Hell in Payment Module

- **Location**: `services/payment/*`
- **Impact**: Medium - Maintainability
- **Effort**: 3 days
- **Interest Rate**: 2 hours per bug fix
- **Solution**: Convert to async/await
- **Owner**: [Unassigned]
- **Deadline**: Next refactor sprint

## Low (P3) - Nice to Have

### 4. Inconsistent Naming Convention

- **Location**: Throughout codebase
- **Impact**: Low - Developer experience
- **Effort**: 1 day
- **Interest Rate**: Minor confusion
- **Solution**: Enforce via linter
- **Owner**: All developers
- **Deadline**: Ongoing
```

## 💰 Calculate Technical Debt Interest

### The Debt Formula:

```javascript
// Technical Debt Cost Calculator
function calculateDebtCost(debt) {
  const {
    timeToBuild, // Original implementation time
    currentFixTime, // Time to fix now
    futureFixTime, // Time to fix in 6 months
    bugFixOverhead, // Extra time per bug due to debt
    bugsPerMonth, // Average bugs in this area
    developerRate, // Cost per hour
  } = debt;

  // Principal (initial debt)
  const principal = currentFixTime * developerRate;

  // Interest (ongoing cost)
  const monthlyInterest = bugFixOverhead * bugsPerMonth * developerRate;

  // Compound interest (gets worse over time)
  const compoundedCost = (futureFixTime - currentFixTime) * developerRate;

  return {
    principal,
    monthlyInterest,
    sixMonthTotal: principal + monthlyInterest * 6 + compoundedCost,
    breakEvenMonths: principal / monthlyInterest,
  };
}

// Example
const authDebt = calculateDebtCost({
  timeToBuild: 40, // Original: 1 week
  currentFixTime: 80, // Now: 2 weeks to refactor
  futureFixTime: 120, // Later: 3 weeks (more dependencies)
  bugFixOverhead: 4, // Each bug takes 4 extra hours
  bugsPerMonth: 3, // 3 auth bugs per month
  developerRate: 100, // $100/hour
});

console.log(`Fix now: $${authDebt.principal}`);
console.log(`Monthly cost: $${authDebt.monthlyInterest}`);
console.log(`6-month total: $${authDebt.sixMonthTotal}`);
console.log(`Break-even: ${authDebt.breakEvenMonths} months`);
```

## 🎯 Debt Prioritization Matrix

### Impact vs Effort:

```
    HIGH IMPACT
         ^
    🔴 Critical     |  💎 Quick Wins
    (High/High)     |  (High/Low)
    Do next sprint  |  Do immediately
    --------------- + ---------------
    ⚠️ Technical    |  💤 Ignore
    (Low/High)      |  (Low/Low)
    Plan for later  |  Not worth it
         |
    LOW IMPACT  <--- LOW EFFORT ---> HIGH EFFORT
```

### Prioritization Criteria:

```javascript
function prioritizeDebt(debts) {
  return debts
    .map(debt => ({
      ...debt,
      score: calculatePriority(debt),
    }))
    .sort((a, b) => b.score - a.score);
}

function calculatePriority(debt) {
  const weights = {
    security: 10, // Security issues first
    performance: 8, // Then performance
    maintainability: 5, // Then code quality
    developer_exp: 3, // Then DX
    cosmetic: 1, // Lowest priority
  };

  const factors = {
    customerImpact: debt.affectsCustomers ? 2 : 1,
    frequency: debt.touchedOften ? 1.5 : 1,
    teamSize: debt.blocksTeam ? 1.5 : 1,
    trend: debt.gettingWorse ? 2 : 1,
  };

  const baseScore = weights[debt.category] || 1;
  const multiplier = Object.values(factors).reduce((a, b) => a * b, 1);

  return (baseScore * multiplier) / debt.effort;
}
```

## 🔍 Debt Detection Patterns

### 1. Code Smells Checklist

```bash
# Create automated debt detection
cat > detect_debt.sh << 'EOF'
#!/bin/bash

echo "=== TECHNICAL DEBT REPORT ==="
echo ""

echo "📊 Code Quality Metrics:"
echo -n "  - Files > 300 lines: "
find . -name "*.js" -exec wc -l {} + | awk '$1 > 300' | wc -l

echo -n "  - Functions > 50 lines: "
grep -n "function\|=>" . -r --include="*.js" | awk '{diff = NR - prev; if (diff > 50) count++; prev = NR} END {print count}'

echo -n "  - Duplicate blocks: "
jscpd . --silent --min-lines 10 2>/dev/null | grep "Duplicat" || echo "0"

echo ""
echo "⚠️ Debt Markers:"
echo -n "  - TODOs: "
grep -r "TODO" --include="*.js" | wc -l

echo -n "  - FIXMEs: "
grep -r "FIXME" --include="*.js" | wc -l

echo -n "  - HACKs: "
grep -r "HACK" --include="*.js" | wc -l

echo ""
echo "📦 Dependency Debt:"
npm audit --json 2>/dev/null | jq '.metadata.vulnerabilities | to_entries | map(select(.value > 0)) | map("\(.key): \(.value)")'

echo ""
echo "🧪 Test Debt:"
npm test -- --coverage 2>/dev/null | grep "All files" || echo "No coverage data"
EOF

chmod +x detect_debt.sh
./detect_debt.sh
```

### 2. Debt Hotspots (Most Changed Files)

```bash
# Files changed most often likely have debt
git log --format=format: --name-only | \
  grep -v '^$' | \
  sort | \
  uniq -c | \
  sort -rn | \
  head -20

# These files are changed frequently - potential refactor candidates
```

## 📈 Debt Paydown Strategies

### 1. The Boy Scout Rule

```javascript
// "Leave code better than you found it"
// When touching a file, fix one small thing

// Before: Working on auth.js for feature
function authenticate(user, pass) {
  // New feature code here

  // While here, fix this TODO:
  // TODO: Hash password
  if (user.password == pass) {
    // Was using ==
    return true;
  }
}

// After: Fixed comparison while adding feature
function authenticate(user, pass) {
  // New feature code here

  if (user.password === pass) {
    // Fixed to ===
    return true;
  }
}
```

### 2. Debt Sprint (20% Time)

```markdown
## Debt Sprint Planning

### Sprint 14: Tech Debt Focus

- **Allocation**: 20% of sprint (2 days)
- **Goal**: Reduce critical debt by 30%

#### Selected Debt Items:

1. ✅ Upgrade React 16 → 18 (8h)
2. ✅ Fix memory leak in WebSocket (4h)
3. ⏳ Add indexes to slow queries (2h)
4. ⏳ Extract payment module (6h)

#### Results:

- Performance: +40% faster
- Bugs: -3 per week
- Developer happiness: +2 points
```

### 3. Refactoring Branch Strategy

```bash
# Create long-lived refactor branch
git checkout -b refactor/payment-system

# Work incrementally
git checkout main
git checkout refactor/payment-system -- src/utils/helpers.js
git commit -m "refactor: Extract helpers from payment system"

# Merge in small pieces
# Reduces risk, maintains velocity
```

## 📊 Debt Metrics Dashboard

```javascript
// Track debt metrics over time
const debtMetrics = {
  // Code metrics
  codeComplexity: 42, // Cyclomatic complexity
  duplicateCode: 12, // Percentage
  testCoverage: 67, // Percentage

  // Dependency metrics
  outdatedDeps: 23, // Count
  securityVulns: 3, // Count

  // Time metrics
  avgBugFixTime: 6.5, // Hours
  deployFrequency: 2.3, // Per week

  // Quality metrics
  bugRate: 8.2, // Per week
  techDebtRatio: 0.35, // Debt / total development time
};

// Generate trend report
function generateDebtReport(current, previous) {
  const report = {
    improved: [],
    degraded: [],
    unchanged: [],
  };

  for (const [key, value] of Object.entries(current)) {
    const prev = previous[key];
    const change = (((value - prev) / prev) * 100).toFixed(1);

    if (Math.abs(change) < 5) {
      report.unchanged.push(key);
    } else if (change < 0) {
      report.improved.push(`${key}: ${change}%`);
    } else {
      report.degraded.push(`${key}: +${change}%`);
    }
  }

  return report;
}
```

## 🚦 When to Pay Debt vs When to Declare Bankruptcy

### Pay the Debt When:

- Cost of fixing < 2x cost of working around it
- Touches core business logic
- Blocks new features
- Security risk
- Team morale issue

### Declare Bankruptcy (Rewrite) When:

- Fix cost > 5x original build cost
- Technology is obsolete
- Original assumptions completely wrong
- No one understands it
- More bugs than features

## 💡 Debt Prevention

### During Development:

```javascript
// Document debt as you create it
function quickHack(data) {
  // TECH-DEBT: This is O(n²), needs optimization
  // Created: 2024-01-15
  // Impact: Slow with > 1000 items
  // Fix: Use Map instead of nested loops
  // Effort: 2 hours
  // Owner: @developer

  for (let i = 0; i < data.length; i++) {
    for (let j = 0; j < data.length; j++) {
      // Quick implementation for deadline
    }
  }
}
```

### Code Review Checklist:

```markdown
## Tech Debt Review

- [ ] No new debt without documentation
- [ ] Debt has owner and deadline
- [ ] Impact is quantified
- [ ] Solution is proposed
- [ ] Added to TECH_DEBT.md
```

## 📋 Debt Communication Template

### For Management:

```markdown
## Technical Debt Impact Report

### Current State:

- **Total Debt**: 320 hours
- **Monthly Interest**: 48 hours (15%)
- **Bug Rate Impact**: +40% due to debt

### Business Impact:

- Feature velocity: -30%
- Customer complaints: +25%
- Developer turnover risk: High

### Proposal:

- Invest 80 hours this quarter
- Reduce interest to 20 hours/month
- ROI: 3 months

### If We Don't Act:

- 6-month projection: 640 hours debt
- Potential system rewrite needed
- Cost: $250,000
```

Remember: Technical debt is not bad - unmanaged debt is! 💳→📊

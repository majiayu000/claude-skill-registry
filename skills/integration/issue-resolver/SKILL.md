---
name: issue-resolver
description: |
  GitHub Issue resolver skill that analyzes, triages, and proposes solutions for issues with full SDD integration

  Trigger terms: resolve issue, fix issue, github issue, issue triage, issue analysis, issue to PR, issue resolution, auto-fix issue

  Use when: User requests involve GitHub issue analysis or resolution
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Issue Resolver AI

## 1. Role Definition

You are an **Issue Resolver AI**.
You analyze GitHub Issues, determine their type and priority, extract requirements, and generate resolution plans following the Specification Driven Development methodology.

---

## 2. Available Module

### IssueResolver (`src/resolvers/issue-resolver.js`)

Provides automated issue analysis and resolution planning:

- **Issue Classification**: Bug, Feature, Documentation, Refactor, Unknown
- **Requirement Extraction**: Parse checkbox and numbered list requirements
- **Branch Generation**: Create semantic branch names
- **Impact Analysis**: Estimate scope, effort, and risk

**Usage Example**:

```javascript
const { IssueResolver, IssueInfo, IssueType } = require('musubi/src/resolvers/issue-resolver');

// Create resolver
const resolver = new IssueResolver({
  projectRoot: process.cwd(),
  autoCreateBranch: false,
});

// Create issue info from GitHub API data
const issue = new IssueInfo({
  number: 42,
  title: 'Login button not responding on mobile',
  body: `
## Description
The login button doesn't work on mobile devices.

## Requirements
- [ ] Fix touch event handling
- [ ] Add loading indicator
- [ ] Add error handling

## Steps to Reproduce
1. Open app on mobile
2. Click login button
3. Nothing happens
  `,
  labels: ['bug', 'mobile'],
  assignees: ['developer1'],
});

// Get issue type
console.log(issue.type); // 'bug'

// Resolve the issue
const result = await resolver.resolve(issue);

console.log(result.branchName); // 'fix/42-login-button-not-responding'
console.log(result.requirements); // ['Fix touch event handling', ...]
console.log(result.impactAnalysis); // { scope: 'medium', effort: 'small', ... }
```

---

## 3. Issue Resolution Workflow

### Step 1: Issue Analysis

```javascript
const issue = new IssueInfo({
  number: issueNumber,
  title: issueTitle,
  body: issueBody,
  labels: issueLabels,
});

// Automatic type detection
const type = issue.type; // 'bug' | 'feature' | 'documentation' | 'refactor' | 'unknown'
```

### Step 2: Requirement Extraction

The resolver automatically extracts requirements from:

- **Checkboxes**: `- [ ] Requirement text`
- **Keywords**: Lines containing "should", "must", "needs to"

```javascript
const requirements = resolver.extractRequirements(issue);
// ['Fix touch event handling', 'Add loading indicator', 'Add error handling']
```

### Step 3: Branch Name Generation

Semantic branch names based on issue type:

| Issue Type    | Branch Prefix |
| ------------- | ------------- |
| Bug           | `fix/`        |
| Feature       | `feat/`       |
| Documentation | `docs/`       |
| Refactor      | `refactor/`   |
| Unknown       | `issue/`      |

```javascript
const branchName = resolver.generateBranchName(issue);
// 'fix/42-login-button-not-responding'
```

### Step 4: Resolution Planning

```javascript
const result = await resolver.resolve(issue);

// Result contains:
// - status: 'pending' | 'in_progress' | 'completed' | 'failed'
// - branchName: Generated branch name
// - requirements: Extracted requirements
// - impactAnalysis: Scope, effort, risk assessment
// - sdsPlan: Suggested SDD workflow stages
```

### Step 5: Preview Generation

```javascript
const preview = resolver.generatePreview(result);
// Returns markdown report for review
```

---

## 4. SDD Integration

### Converting Issues to Requirements

1. **Parse Issue**: Extract structured data
2. **Generate EARS**: Convert to EARS format requirements
3. **Create REQ Document**: Use `musubi-requirements` CLI
4. **Link Traceability**: Connect issue → requirement → design → task

### Issue to SDD Workflow

**Quick Start with `musubi-resolve` CLI (v3.5.0 NEW)**:

```bash
# One-command issue resolution
musubi-resolve 42

# Analyze without resolution
musubi-resolve analyze 42

# Generate resolution plan
musubi-resolve plan 42

# Create PR from resolution
musubi-resolve create-pr 42

# Auto-resolve mode
musubi-resolve 42 --auto
```

**Manual SDD Workflow**:

```bash
# 1. Analyze issue and create requirement document
musubi-requirements init "issue-42-login-fix"

# 2. Add extracted requirements as EARS statements
musubi-requirements add event-driven "When user taps login button on mobile, system SHALL respond within 300ms"

# 3. Create design for the fix
musubi-design init "issue-42-login-fix"

# 4. Break down into tasks
musubi-tasks init "issue-42-login-fix"
```

---

## 5. Impact Analysis

The ImpactAnalysis class provides:

```javascript
const impact = new ImpactAnalysis({
  scope: 'medium', // 'small' | 'medium' | 'large'
  effort: 'small', // 'trivial' | 'small' | 'medium' | 'large' | 'epic'
  risk: 'low', // 'low' | 'medium' | 'high' | 'critical'
  affectedAreas: ['components/LoginButton', 'utils/touchHandler'],
  dependencies: ['react-native-gesture-handler'],
  breakingChanges: false,
});

console.log(impact.toMarkdown());
```

---

## 6. Output Format

### Resolution Report

```markdown
## 🎫 Issue Resolution: #42

**Title**: Login button not responding on mobile
**Type**: 🐛 Bug
**Status**: ✅ Completed

### Branch

`fix/42-login-button-not-responding`

### Requirements Extracted

1. Fix touch event handling
2. Add loading indicator
3. Add error handling

### Impact Analysis

| Aspect           | Value  |
| ---------------- | ------ |
| Scope            | Medium |
| Effort           | Small  |
| Risk             | Low    |
| Breaking Changes | No     |

### Affected Areas

- `components/LoginButton`
- `utils/touchHandler`

### SDD Workflow

1. ✅ Requirements documented
2. ⬜ Design review pending
3. ⬜ Task breakdown pending
4. ⬜ Implementation pending
5. ⬜ Testing pending
```

---

## 7. Integration with Other Skills

- **Requirements Analyst**: Generate EARS requirements from issue
- **Software Developer**: Implement based on extracted requirements
- **Test Engineer**: Create test cases from requirements
- **Bug Hunter**: Deep dive into root cause analysis

---

## Project Memory (Steering System)

**CRITICAL: Always check steering files before starting any task**

Before beginning work, **ALWAYS** read the following files if they exist in the `steering/` directory:

- **`steering/structure.md`** (English) - Architecture patterns
- **`steering/tech.md`** (English) - Technology stack
- **`steering/product.md`** (English) - Business context

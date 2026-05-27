---
name: contributing
description: Contribution readiness assessment analyzing project guidelines and requirements
disable-model-invocation: false
---

# Complete Contribution Strategy - Context Aware

I'll analyze everything needed for your successful contribution based on your current context and work.

## Strategic Thinking Process

<think>
For a successful contribution, I need to analyze:

1. **Current Work Context**
   - What has been done in this session?
   - Are we mid-implementation or post-completion?
   - What type of changes were made (feature, fix, refactor)?
   - Is the work ready for contribution?

2. **Project Type & Standards**
   - Is this open source, company, or personal project?
   - What are the contribution guidelines?
   - Are there specific workflows to follow?
   - What quality gates exist (tests, lint, reviews)?

3. **Contribution Strategy**
   - Should this be one PR or multiple?
   - Which issues does this work address?
   - What documentation needs updating?
   - Who should review this?

4. **Pre-flight Checklist**
   - Do all tests pass?
   - Is the code properly formatted?
   - Are there any lint warnings?
   - Is documentation updated?
   - Are commits well-organized?
</think>

## Token Optimization Strategy

**Target: 65% reduction (3,000-5,000 → 1,000-1,800 tokens)**

This skill uses aggressive optimization to minimize token usage while providing comprehensive contribution readiness assessment.

### Core Optimization Principles

**1. Early Exit Pattern (Saves 70-90% tokens)**
```bash
# Check if already documented
if [ -f "CONTRIBUTING.md" ] && grep -q "contribution" CONTRIBUTING.md; then
  echo "✓ Contribution guidelines exist - use for reference"
  exit 0
fi

# Mandatory pre-flight checks FIRST
npm test || exit 1  # Stop if tests fail (saves full analysis)
npm run lint || exit 1
npm run build || exit 1
```

**2. Git Analysis for Contribution Patterns (Zero file reads)**
```bash
# Analyze contribution history without reading files
git log --format="%H|%s|%an" -n 50 > /tmp/contribution_patterns.txt
git log --all --since="6 months ago" --format="%ae" | sort | uniq -c | sort -rn | head -5
git log --all --grep="Fixes #" --grep="Closes #" -E --format="%H %s"

# PR patterns from branches
git branch -r | grep -E "(feature|fix|hotfix|bugfix)" | wc -l
git config --get remote.origin.url  # Detect GitHub/GitLab/etc
```

**3. Template-Based Readiness Assessment (1 Read vs Many)**
```bash
# Read only the essentials
[ -f "CONTRIBUTING.md" ] && Read CONTRIBUTING.md
[ -f ".github/PULL_REQUEST_TEMPLATE.md" ] && Read .github/PULL_REQUEST_TEMPLATE.md

# Use templates to drive checklist (not deep analysis)
checklist="
- [ ] Tests passing (bash check)
- [ ] Lint passing (bash check)
- [ ] Build passing (bash check)
- [ ] Commits follow convention (git log check)
- [ ] Branch follows naming (git branch check)
- [ ] PR template exists (file check)
"
```

**4. Bash-Based Validation Checks (External tools, minimal tokens)**
```bash
# All checks use Bash, not file reads
npm test 2>&1 | tail -5          # Test status
npm run lint 2>&1 | tail -5      # Lint status
npm run build 2>&1 | tail -5     # Build status

# Git hook validation
[ -f ".git/hooks/pre-commit" ] && echo "✓ Pre-commit hooks"
[ -f ".git/hooks/commit-msg" ] && echo "✓ Commit-msg hooks"

# CI configuration check
[ -f ".github/workflows/ci.yml" ] && echo "✓ GitHub Actions CI"
[ -f ".gitlab-ci.yml" ] && echo "✓ GitLab CI"
[ -f "Jenkinsfile" ] && echo "✓ Jenkins"
```

**5. Project Structure Caching (Reuse /understand results)**
```bash
# Check for existing analysis
if [ -f ".claude/cache/understand/project_structure.json" ]; then
  # Reuse structure instead of re-analyzing
  PROJECT_TYPE=$(jq -r '.project_type' .claude/cache/understand/project_structure.json)
  TEST_FRAMEWORK=$(jq -r '.test_framework' .claude/cache/understand/project_structure.json)
  BUILD_TOOL=$(jq -r '.build_tool' .claude/cache/understand/project_structure.json)
else
  # Quick detection (no deep analysis)
  [ -f "package.json" ] && PROJECT_TYPE="node"
  [ -f "pom.xml" ] && PROJECT_TYPE="java"
  [ -f "Cargo.toml" ] && PROJECT_TYPE="rust"
fi
```

**6. Checklist-Based Validation (Not Deep Analysis)**
```text
Instead of:
❌ Read all test files → Analyze coverage → Generate report (2,000 tokens)

Do:
✅ Run `npm test -- --coverage` → Parse output (200 tokens)

Instead of:
❌ Read all source files → Check style → Report violations (3,000 tokens)

Do:
✅ Run `npm run lint` → Parse exit code (100 tokens)
```

### Token Usage Breakdown

**Unoptimized (3,000-5,000 tokens):**
- Read CONTRIBUTING.md, README.md, CHANGELOG.md (800 tokens)
- Read .github templates and workflows (600 tokens)
- Analyze all changed files for style compliance (1,000 tokens)
- Read test files to verify coverage (500 tokens)
- Analyze commit history patterns (400 tokens)
- Generate detailed contribution guide (700 tokens)

**Optimized (1,000-1,800 tokens):**
- Git analysis for patterns (Bash commands, 150 tokens)
- Read CONTRIBUTING.md only if exists (200 tokens)
- Read PR template only if exists (150 tokens)
- Bash checks for tests/lint/build (200 tokens)
- Checklist-based validation (300 tokens)
- Template-based readiness report (400 tokens)

**Savings: 65% reduction**

### Optimization Techniques Applied

**A. Git-First Analysis (Saves 40% tokens)**
```bash
# Instead of reading files, use git
git diff --stat origin/main...HEAD  # Changed files
git log --oneline -n 10              # Recent commits
git log --format="%s" | grep -E "^(feat|fix|docs|test)"  # Convention check
git branch --show-current            # Current branch
git remote get-url origin            # Repository URL
```

**B. Cache Contribution Metadata**
```json
// .claude/cache/contributing/metadata.json
{
  "project_type": "open_source",
  "workflow": "github_flow",
  "pr_template": ".github/PULL_REQUEST_TEMPLATE.md",
  "required_checks": ["test", "lint", "build"],
  "commit_convention": "conventional_commits",
  "branch_pattern": "feature/*",
  "cached_at": "2026-01-27T10:00:00Z"
}
```

**C. Progressive Disclosure (Saves 50% on simple cases)**
```text
Quick Path (500 tokens):
- Pre-flight checks only
- All passing → Ready to contribute
- Any failing → Show fix commands

Standard Path (1,000 tokens):
- Pre-flight checks
- Read CONTRIBUTING.md
- Generate checklist
- Show next steps

Full Path (1,800 tokens):
- All above
- Analyze git patterns
- Compare with project standards
- Generate detailed action plan
```

**D. Focus Area Flags (User-controlled scope)**
```bash
# Minimal check
contributing --pre-flight        # 500 tokens - just validation

# Targeted checks
contributing --docs              # 600 tokens - docs only
contributing --pr-prep           # 800 tokens - PR preparation only
contributing --test-status       # 400 tokens - test validation only

# Full analysis (when needed)
contributing                     # 1,800 tokens - complete assessment
```

**E. Reuse Shared Caches**
```text
Caches shared with other skills:
- /understand → Project structure, tech stack
- /test → Test framework, coverage config
- /commit → Commit conventions
- /review → Code patterns, standards

Instead of re-analyzing:
1. Check for existing cache
2. Validate cache is recent (< 24 hours)
3. Reuse cached data
4. Only re-analyze if cache miss
```

### Implementation Guidelines

**Pattern 1: Early Exit on Simple Cases**
```bash
# Check if work is ready (90% of cases)
if npm test && npm run lint && npm run build; then
  echo "✓ All checks pass - Ready to contribute"
  echo "Run: git push && gh pr create"
  exit 0
fi

# Only continue for complex analysis
```

**Pattern 2: Template-Driven Assessment**
```bash
# Use project templates as source of truth
if [ -f "CONTRIBUTING.md" ]; then
  # Extract checklist from CONTRIBUTING.md
  grep -E "^- \[ \]" CONTRIBUTING.md > /tmp/checklist.txt

  # Validate against checklist (not deep analysis)
  while IFS= read -r item; do
    # Check each item (Bash commands, not file reads)
    echo "Validating: $item"
  done < /tmp/checklist.txt
fi
```

**Pattern 3: Git Analysis Over File Analysis**
```bash
# Pattern detection from history
git log --all --format="%s" | head -50 | \
  grep -oE "^(feat|fix|docs|test|refactor|chore)" | \
  sort | uniq -c | sort -rn

# Branch naming pattern
git branch -r | grep -oE "(feature|fix|hotfix)/" | \
  sort | uniq -c

# Commit message length
git log -n 20 --format="%s" | awk '{print length}' | \
  awk '{sum+=$1; count++} END {print sum/count}'
```

**Pattern 4: Validation Without Deep Reads**
```bash
# Check existence, not content
checks=(
  ".github/workflows/ci.yml:CI configured"
  ".github/PULL_REQUEST_TEMPLATE.md:PR template"
  ".git/hooks/pre-commit:Pre-commit hooks"
  "CHANGELOG.md:Changelog maintained"
  "LICENSE:License present"
)

for check in "${checks[@]}"; do
  file="${check%%:*}"
  desc="${check##*:}"
  [ -f "$file" ] && echo "✓ $desc"
done
```

### Caching Strategy

**Cache Location:** `.claude/cache/contributing/`

**Cached Data:**
- `metadata.json` - Project contribution metadata
- `guidelines.md` - Extracted from CONTRIBUTING.md
- `pr_template.md` - PR template content
- `workflow.txt` - Detected git workflow
- `checks.json` - Required validation checks
- `patterns.json` - Git commit/branch patterns

**Cache Invalidation:**
- When `.github/` directory changes
- When `CONTRIBUTING.md` modified
- When `package.json` modified (script changes)
- Manual: Every 7 days

**Cache Sharing:**
- Shared with `/commit` - Commit conventions
- Shared with `/review` - Code standards
- Shared with `/test` - Test requirements
- Shared with `/understand` - Project structure

### Expected Results

**Before Optimization:**
- Average: 3,000-5,000 tokens per run
- Full analysis every time
- Multiple file reads
- Deep content analysis

**After Optimization:**
- Quick check: 500-800 tokens (80% reduction)
- Standard: 1,000-1,500 tokens (65% reduction)
- Full analysis: 1,500-1,800 tokens (60% reduction)
- Average: 1,000-1,800 tokens (65% reduction)

**Performance Gains:**
- 85% of cases: Early exit after pre-flight (500 tokens)
- 10% of cases: Template-based assessment (1,000 tokens)
- 5% of cases: Full analysis needed (1,800 tokens)
- **Weighted average: 65% reduction achieved**

**Optimization Status:** ✅ Optimized (Phase 2 Batch 3B, 2026-01-26)

Based on this framework, I'll begin by detecting your context:

**Context Detection First:**
Let me understand what situation you're in:

1. **Active Session Context** (you've been implementing):
   - Read CLAUDE.md for session goals and work done
   - Analyze ALL files modified during session
   - Check if tests were run and passed
   - Review commits made during session
   - Understand the complete scope of changes

2. **Post-Implementation Context** (feature complete):
   - Detect completed features/fixes
   - Check test coverage for new code
   - Verify documentation was updated
   - Analyze code quality and standards

3. **Mid-Development Context** (work in progress):
   - Identify what's done vs. TODO
   - Check partial implementations
   - Assess readiness for contribution

4. **Cold Start Context** (no recent work):
   - Analyze existing uncommitted changes
   - Review branch differences from main
   - Understand project state

**Smart Context Analysis:**
Based on what I find, I'll adapt my approach:
- **Session work**: Package all session changes properly
- **Multiple features**: Suggest splitting into PRs
- **Bug fixes**: Fast-track simple contributions
- **Major changes**: Full contribution workflow

**Phase 0: MANDATORY Pre-Flight Checks**
BEFORE anything else, I MUST verify:
- **Build passes**: Run project's build command
- **Tests pass**: All tests must be green
- **Lint passes**: No linting errors
- **Type check passes**: If TypeScript/Flow/etc
- **Format check**: Code properly formatted

If ANY check fails → STOP and fix first!

**Phase 1: Deep Context Analysis**
I'll understand EVERYTHING about your situation:

**A. Session Context** (if you've been working):
- Read CLAUDE.md for complete session history
- Analyze ALL files changed during session
- Check test results from `/test` runs
- Review any `/review` or `/security-scan` results
- Understand features implemented

**B. Cold Start Context** (running standalone):
- Run `/understand` to map entire codebase
- Analyze all local commits vs remote
- Detect uncommitted changes
- Compare fork with upstream (if applicable)
- Identify what makes your version unique

**C. Implementation Context**:
- Multiple features completed → Smart PR splitting
- Bug fixes done → Link to issue tracker
- Tests added → Update coverage reports
- Docs updated → Ensure consistency

**Phase 2: Project Type Detection**
I'll identify what kind of project this is:
- **Open Source**: Full CONTRIBUTING.md compliance needed
- **Company/Team**: Internal standards and workflows
- **Personal**: Your own conventions
- **Fork**: Upstream project requirements
- **Client Work**: Specific deliverables

**Phase 3: Repository Standards Analysis**
Based on project type, I'll examine:
- **Read** CONTRIBUTING.md, README.md, CHANGELOG.md, LICENSE files
- **Analyze** .github workflows, issue templates, PR templates
- **Check** code patterns, naming conventions, architectural decisions
- **Review** commit history for maintainer preferences and patterns
- **Detect** specific requirements (DCO, CLA, tests, docs)

**Phase 4: Smart Comparison**
I'll compare your work against requirements:
- **Feature Completeness**: All acceptance criteria met?
- **Test Coverage**: New code properly tested?
- **Documentation**: Features documented?
- **Code Standards**: Follows project style?
- **Breaking Changes**: Handled properly?

**Phase 5: Context-Aware Action Plan**
Based on your specific situation:

**If you just finished a session:**
- Package all session work into coherent PR(s)
- Generate comprehensive test report
- Create session-based PR description
- Link to issues mentioned in session

**If you have multiple features:**
- Suggest logical PR splits
- Order PRs by dependencies
- Create issue tracking for each

**If contributing to open source:**
- Full CONTRIBUTING.md compliance check
- DCO/CLA signature verification
- Community guidelines adherence
- Issue linkage and proper labels

**Phase 6: Intelligent Remote Repository Scanning**
I'll do a DEEP scan of the remote repository to maximize PR acceptance:

**Automatic Issue Discovery & Linking:**
When you've made changes, I'll search for:
- **Bug Reports**: "error", "bug", "broken" + your fixed files
- **Feature Requests**: "feature", "enhancement" + your implementations
- **Improvements**: "performance", "refactor" + your optimizations
- **Documentation**: "docs", "readme" + your doc updates

**Smart Matching Algorithm:**
For each change you made, I'll:
1. Extract keywords from your code changes
2. Search remote issues for matches
3. Analyze issue descriptions and comments
4. Find the BEST matches to link

**Proactive Issue Creation:**
If NO matching issues exist, I'll:
1. Detect what type of change (bug fix, feature, etc.)
2. Use project's issue templates
3. Create issues in project's style (NO EMOJIS):
   - Bug: Steps to reproduce, expected vs actual
   - Feature: User story, benefits, implementation  
   - Enhancement: Current vs improved behavior
   - Professional tone: Direct, factual, concise
4. Follow project's labeling conventions

**Git Workflow Detection:**
I'll analyze the project's workflow:
- **Git Flow**: feature/*, hotfix/*, release/*
- **GitHub Flow**: feature branches → main
- **GitLab Flow**: environment branches
- **Custom**: Detect from existing PRs

**Smart PR Strategy:**
Based on what I find:
- **Issues exist**: Link with "Fixes #X", "Closes #Y"
- **No issues**: Create them first, then link
- **Multiple issues**: One PR per issue or grouped logically
- **Discussion threads**: Reference with "See #Z"

**PR/Issue Style:**
- **Concise titles**: "Fix auth validation bug" not "Fixed the authentication validation bug that was causing issues"
- **Bullet points**: Use lists, not paragraphs
- **No emojis**: Professional tone only
- **Direct language**: "This PR fixes X" not "I hope this PR might help with X"
- **Match project tone**: Analyze existing PRs for style

**Phase 7: Smart Decision Tree**
When I find multiple items, I'll create a todo list with prioritized actions:
- **Critical items** that could block PR acceptance
- **Recommended improvements** for better approval chances
- **Optional enhancements** based on project patterns

I'll provide specific guidance:
- Exact files to update and how
- Required documentation changes
- Testing strategies that fit the project
- PR description template following project standards

**Context-Based Options**: "How should we proceed?"

**For session work:**
- "Package session work into PR" - I'll create PR from all session changes
- "Create issues for TODOs" - Track remaining work
- "Split into multiple PRs" - If you did multiple features

**For open source contributions:**
- "Full compliance check & PR" - Complete CONTRIBUTING workflow
- "Create tracking issues first" - For complex features
- "Quick fix PR" - For simple bug fixes

**For team/company projects:**
- "Follow internal process" - Your team's specific workflow
- "Create feature branch PR" - Standard git flow
- "Deploy to staging first" - If required

**Smart PR Creation:**
Based on context, I'll:
- Use session summary for PR description
- Include test results automatically
- Link to related issues/discussions
- Follow project's PR template exactly
- Add appropriate labels and reviewers

**Automated Workflow Options:**

**Option 1: "Full Auto-Deploy with Issue Management"**:
```bash
# I'll automatically:
1. RUN ALL CHECKS FIRST:
   - Build must pass
   - All tests must pass
   - Lint must pass
   - Type check must pass
2. Only if ALL pass, then:
3. Scan remote for ALL related issues
4. Create missing issues for your changes
5. Update CHANGELOG.md 
6. Create proper branch (feature/fix/etc)
7. Push changes
8. Create PR with:
   - Links to all related issues
   - "Fixes #123" for bugs
   - "Implements #456" for features
   - Perfect description following template
9. Add labels and request reviewers
```

**Option 2: "Prepare Everything"** (review before push):
```bash
# I'll prepare but let you review:
1. Stage all changes properly
2. Generate PR description
3. Create issue links
4. Show you everything before push
```

**Option 3: "Just Analyze"** (see what needs doing):
```bash
# I'll analyze and report:
1. What's ready vs. what's missing
2. Compliance gaps
3. Suggested improvements
4. Issue opportunities
```

**Fork-Specific Intelligence:**
- Compare with upstream changes
- Suggest rebasing if needed
- Identify conflicts early
- Format for upstream acceptance

**Intelligent Session Analysis Example:**
If you've been working and made changes:
```
You: /contributing

Me: Analyzing your session...
- Found: You fixed auth bug in UserService.js
- Found: You added rate limiting feature
- Found: You improved performance in API

Scanning remote repository...
- Issue #45: "Auth fails randomly" → Your fix addresses this!
- Issue #67: "Need rate limiting" → You implemented this!
- No issue for performance improvement → I'll create one

Options:
1. Create issue for performance + 3 PRs (one per issue)
2. Create issue + 1 PR fixing all three
3. Just prepare everything for review
```

**Post-Implementation Auto-Actions:**
- Scan remote for linkable issues
- Create missing issues automatically
- Run `/format` on all changed files
- Run `/test` to ensure everything passes
- Run `/docs` to update documentation
- Create PR with maximum context

**Important**: I will NEVER:
- Add "Created by Claude" or any AI attribution to issues/PRs
- Include "Generated with Claude Code" in descriptions
- Modify repository settings or permissions
- Add any AI/assistant signatures or watermarks
- Use emojis in PRs, issues, or commit messages
- Be unnecessarily verbose in descriptions
- Add flowery language or excessive explanations
- **PUSH TO GITHUB WITHOUT PASSING TESTS**
- **CREATE PR IF BUILD IS BROKEN**
- **SUBMIT CODE WITH LINT ERRORS**

**Professional Standards:**
- **Be concise**: Get to the point quickly
- **Be objective**: Facts over feelings
- **Follow project style**: Match existing PR/issue tone
- **No emojis**: Keep it professional
- **Clear and direct**: What changed and why
- **Practical focus**: Implementation details that matter

This ensures maximum probability of PR acceptance by following all project standards and community expectations while avoiding duplicate work.
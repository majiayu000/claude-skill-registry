---
name: troubleshooting
description: |
  Debugging and problem-solving workflow. Use when stuck on an issue for more
  than 30 minutes, encountering cryptic errors, or needing a systematic approach
  to diagnose and fix problems.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: workflow
---

# Troubleshooting Guide

Emergency procedures when stuck, tests failing, or errors occurring. Use after 30+ minutes stuck on same issue.

---

## Emergency Procedures

### When Stuck (>30 min on one issue)

**STOP IMMEDIATELY** - Don't keep trying random solutions

**Follow this process:**

1. **Document What You've Tried**
   - List all approaches attempted
   - Note exact error messages
   - Record what changed between working and broken states

2. **Simplify & Isolate**
   - Can you reproduce in isolation? (minimal test case)
   - Remove complexity: Comment out code until error disappears
   - Bisect: Is it old code or new code causing the issue?

3. **Check Fundamentals**
   - [ ] Are dependencies installed and up to date?
   - [ ] Is configuration correct? (environment variables, paths)
   - [ ] Are file permissions correct?
   - [ ] Is the right version running? (restart server, clear cache)

4. **Search for Similar Issues**
   - Google exact error message
   - Check GitHub issues for dependencies
   - Search Stack Overflow
   - Review `.claude/memory/` for similar past problems

5. **Ask for Help**
   - Present clear problem statement to user:
     - What are you trying to do?
     - What happens instead?
     - What have you tried?
     - What's the exact error?

6. **Record the Solution**
   - Once resolved, create `.claude/memory/YYYY-MM-DD-issue-name.md`
   - Document: Problem, Root Cause, Solution, Prevention

---

## When Tests Break Unexpectedly

### Diagnosis Steps

1. **Identify When It Broke**
   ```bash
   # Check recent changes
   git diff HEAD~1

   # Run tests on last commit
   git checkout HEAD~1
   npm test  # or cargo test, pytest, go test
   ```

2. **Isolate the Failing Test**
   ```bash
   # Run single test file
   npm test path/to/test.spec.ts

   # Run single test case
   npm test -t "specific test name"
   ```

3. **Check for Flakiness**
   - Run test 10 times: Does it fail consistently?
   - Is it timing-dependent? (race condition)
   - Does order matter? (test interdependence)

### Recovery Process

**If tests broke after your change:**
```bash
# Option 1: Revert and re-apply incrementally
git reset --hard HEAD~1
# Re-apply changes one file at a time, testing after each

# Option 2: Git bisect (find exact breaking commit)
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>
# Git will checkout commits; run tests and mark good/bad
```

**If tests broke without your changes:**
- Check dependency updates (`package-lock.json`, `Cargo.lock` changes)
- Check environment differences (Node version, Python version)
- Check for flaky tests (run 10 times to confirm)

---

## When Security Issue Found

**PRIORITY: CRITICAL**

### Immediate Actions

1. **DO NOT COMMIT vulnerable code**
   ```bash
   # Stash changes if needed
   git stash
   ```

2. **Fix Immediately**
   - Security takes priority over all other work
   - Apply fix from guardrails or security best practices

3. **Add Regression Test**
   - Ensure vulnerability can't be reintroduced
   - Test both the exploit and the fix

4. **Document in Memory**
   - Create `.claude/memory/YYYY-MM-DD-security-fix-NAME.md`
   - Document: Vulnerability, Impact, Fix, Prevention

5. **Review Similar Code**
   - Search codebase for same pattern
   - Fix all instances (not just the one found)

### Common Security Issues & Fixes

**SQL Injection:**
```javascript
// ❌ Vulnerable
db.query(`SELECT * FROM users WHERE id = ${userId}`);

// ✅ Fixed
db.query('SELECT * FROM users WHERE id = ?', [userId]);
```

**XSS (Cross-Site Scripting):**
```javascript
// ❌ Vulnerable
element.innerHTML = userInput;

// ✅ Fixed
element.textContent = userInput;
// Or use framework escaping (React auto-escapes)
```

**Hardcoded Secrets:**
```javascript
// ❌ Vulnerable
const API_KEY = "sk_live_abc123";

// ✅ Fixed
const API_KEY = process.env.API_KEY;
```

---

## When Performance Degrades

### Diagnosis

1. **Measure First**
   - Don't guess - profile the code
   - Use browser DevTools (frontend)
   - Use profilers (`cargo flamegraph`, `py-spy`, `pprof`)

2. **Identify Bottleneck**
   ```bash
   # Node.js
   node --prof app.js
   node --prof-process isolate-*.log

   # Python
   python -m cProfile -o output.prof script.py
   python -m pstats output.prof

   # Go
   go test -bench . -cpuprofile=cpu.prof
   go tool pprof cpu.prof
   ```

3. **Common Culprits**
   - [ ] N+1 database queries (use eager loading)
   - [ ] Large data loaded into memory (use pagination/streaming)
   - [ ] Inefficient algorithms (O(n²) when O(n) possible)
   - [ ] Missing indexes on database columns
   - [ ] Unnecessary re-renders (React, Vue)
   - [ ] Blocking I/O in async contexts

### Fix Priorities

1. **Big wins first**: Fix O(n²) → O(n), add database indexes
2. **Measure improvement**: Benchmark before/after
3. **Don't over-optimize**: 80% of time spent in 20% of code

---

## When Build Fails

### Common Issues

**Dependency Conflicts:**
```bash
# Node.js
rm -rf node_modules package-lock.json
npm install

# Python
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall

# Go
go clean -modcache
go mod tidy
go mod download

# Rust
cargo clean
cargo build
```

**Version Mismatch:**
- Check Node/Python/Go/Rust version matches project requirements
- Use version managers: `nvm`, `pyenv`, `gvm`, `rustup`

**Missing Environment Variables:**
```bash
# Check .env.example vs .env
diff .env.example .env

# Set required variables
export DATABASE_URL="..."
export API_KEY="..."
```

---

## When Git Issues Occur

### Merge Conflicts

```bash
# Show conflicted files
git status

# Open files, look for conflict markers:
<<<<<<< HEAD
Your changes
=======
Their changes
>>>>>>> branch-name

# Resolve manually, then:
git add <resolved-files>
git commit
```

### Accidentally Committed Secrets

**CRITICAL - Act immediately:**

```bash
# Remove from last commit (if not pushed)
git reset HEAD~1
# Remove secret from file
# Add file to .gitignore
git add .
git commit -m "Remove secrets"

# If already pushed - rotate the secret immediately
# Then use BFG Repo-Cleaner or git-filter-branch
```

### Lost Work

```bash
# Find lost commits
git reflog

# Recover lost commit
git checkout <commit-hash>

# Create branch from recovered commit
git checkout -b recovery-branch
```

---

## Red Flags (Stop & Reassess)

Stop immediately if you encounter these:

### Code Red Flags
- ❌ Same error after 3 different attempted fixes
- ❌ Solution getting more complex instead of simpler
- ❌ Not understanding why a fix works ("it just works now")
- ❌ Touching >10 files for a "simple" bug fix
- ❌ Breaking existing tests to make new code work

### Process Red Flags
- ❌ Skipping tests because "I'll add them later"
- ❌ Committing commented-out code "just in case"
- ❌ Ignoring linter errors "they're not important"
- ❌ Using `any` or `unsafe` to "make TypeScript/Rust happy"
- ❌ Copying code without understanding it

**When you see red flags:**
1. STOP adding more code
2. Revert to last working state
3. Apply COMPLEX mode: Full 4D decomposition
4. Ask user for guidance if still stuck

---

## Common Error Messages & Solutions

### TypeScript/JavaScript

**"Cannot find module"**
```bash
npm install
# or
npm install <package-name>
```

**"Type 'X' is not assignable to type 'Y'"**
- Check type definitions: Are they correct?
- Use type assertions only if you're certain: `as Y`
- Consider using `unknown` and narrowing

**"Module not found" (frontend)**
- Check import paths (case-sensitive)
- Restart dev server
- Clear build cache

### Python

**"ModuleNotFoundError"**
```bash
pip install -r requirements.txt
# Or
pip install <module-name>
```

**"IndentationError"**
- Use consistent indentation (spaces vs tabs)
- Configure editor to use 4 spaces

**"AttributeError: ... has no attribute ..."**
- Check object type (use `type()` or debugger)
- Check if attribute exists (`hasattr()`)

### Go

**"cannot find package"**
```bash
go mod tidy
go mod download
```

**"undefined: ..."**
- Check imports
- Check if function/variable is exported (capitalized)

### Rust

**"cannot borrow `x` as mutable"**
- Only one mutable borrow allowed
- Consider refactoring to avoid simultaneous borrows

**"use of moved value"**
- Value was moved (ownership transferred)
- Clone if needed, or use borrowing (`&`)

---

## Recovery Checklist

After resolving any major issue:

- [ ] Tests passing
- [ ] Guardrails validated
- [ ] Root cause understood (not just symptom fixed)
- [ ] Documented in `.claude/memory/` if significant
- [ ] Similar code reviewed for same issue
- [ ] Prevention added (test, linter rule, guardrail)

---

**Remember**: Being stuck is normal. Following a systematic process beats random attempts. Document your solutions - future you will thank you!

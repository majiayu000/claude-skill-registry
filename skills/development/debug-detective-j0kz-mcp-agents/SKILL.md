---
name: debug-detective
description: "Systematic debugging approach for ANY codebase, ANY language, ANY bug type"
---

# Debug Detective - Systematic Bug Hunting

## 🎯 When to Use This Skill

Use when facing ANY bug:
- Unexpected behavior
- Crashes or errors
- Performance issues
- Intermittent problems
- "Works on my machine" issues

## ⚡ Quick Start (Find bugs in 5 steps)

### The Universal Debug Protocol:
1. **REPRODUCE** - Can you make it happen again?
2. **ISOLATE** - Where exactly is it breaking?
3. **UNDERSTAND** - Why is it breaking?
4. **FIX** - Apply minimal solution
5. **VERIFY** - Confirm fix works

## 🔍 Step 1: REPRODUCE

### WITH MCP Tools:
```
"Help me create a minimal reproduction for this bug: [describe bug]"
```

### WITHOUT MCP:
```bash
# Document the exact steps:
echo "=== BUG REPRODUCTION ===" > bug_report.md
echo "1. Start the app with: [command]" >> bug_report.md
echo "2. Navigate to: [location]" >> bug_report.md
echo "3. Perform action: [action]" >> bug_report.md
echo "4. Expected: [what should happen]" >> bug_report.md
echo "5. Actual: [what actually happens]" >> bug_report.md

# Try to reproduce 3 times - is it consistent?
```

### Quick Tests:
```bash
# Different environments
NODE_ENV=production npm start  # Production mode?
npm start --debug              # Debug mode?
docker run ...                 # Container issue?

# Different data
# - With empty database
# - With large dataset
# - With special characters
# - With null/undefined values
```

## 🎯 Step 2: ISOLATE

### WITH MCP (Architecture Analyzer):
```
"Trace the execution flow for [feature name]"
"Find all places where [variable/function] is used"
```

### WITHOUT MCP:

#### Binary Search Method:
```bash
# Cut the problem in half repeatedly
# 1. Add midpoint log
console.log('=== MIDPOINT: Data here:', data);

# 2. Did error occur before or after?
# 3. Repeat in that half
```

#### Breadcrumb Trail:
```javascript
// Add numbered checkpoints
console.log('🔍 1: Starting process');
console.log('🔍 2: Data loaded:', data);
console.log('🔍 3: Processing complete');
console.log('🔍 4: Saving results');
// Where does it stop?
```

#### Git Bisect (for regressions):
```bash
git bisect start
git bisect bad HEAD           # Current version is broken
git bisect good v1.2.3         # This version worked
# Git will help find the breaking commit
```

## 🧠 Step 3: UNDERSTAND

### WITH MCP (Smart Reviewer):
```
"Analyze this function for potential issues: [paste code]"
"What could cause [error message]?"
```

### WITHOUT MCP:

#### The 5 Whys Technique:
```
Problem: App crashes on user login
Why? → Authentication fails
Why? → Token is invalid
Why? → Token expired
Why? → Refresh mechanism broken
Why? → API endpoint changed
Root cause found!
```

#### Common Bug Patterns Check:

**Race Conditions:**
```javascript
// Look for async without await
someAsyncCall();  // Missing await?
doSomethingElse(); // This runs immediately!

// Fix:
await someAsyncCall();
doSomethingElse();
```

**Off-by-One Errors:**
```javascript
// Check loop boundaries
for (let i = 0; i <= array.length; i++)  // Should be < not <=
```

**Type Mismatches:**
```javascript
// Check for type coercion issues
"1" + 1 === "11"  // String concatenation
"1" - 1 === 0     // Number coercion
```

**Null/Undefined:**
```javascript
// Add defensive checks
const result = data?.user?.name ?? 'default';
```

## 🔧 Step 4: FIX

### WITH MCP (Refactor Assistant):
```
"Fix this bug with minimal changes: [describe issue and paste code]"
```

### WITHOUT MCP:

#### Minimal Fix Approach:
1. **Smallest possible change** that fixes the issue
2. **Don't refactor** while fixing (separate concerns)
3. **Add defensive code** to prevent recurrence
4. **Document the fix** with a comment

#### Fix Template:
```javascript
// BUG FIX: [Issue description]
// Problem: [What was wrong]
// Solution: [What this fixes]
// Date: [Today's date]
// TODO: Consider refactoring in future

// Original problematic code (commented):
// if (user.role == 'admin') {

// Fixed code:
if (user && user.role === 'admin') {
  // Added null check and strict equality
}
```

## ✅ Step 5: VERIFY

### WITH MCP (Test Generator):
```
"Generate a test that verifies this bug is fixed"
```

### WITHOUT MCP:

#### Verification Checklist:
```bash
# 1. Original bug fixed?
[Run reproduction steps]

# 2. No new bugs introduced?
npm test
npm run lint

# 3. Edge cases handled?
# - Null inputs
# - Empty arrays
# - Large numbers
# - Special characters

# 4. Performance unchanged?
time npm start  # Basic performance check
```

#### Regression Test:
```javascript
// Add a test to prevent this bug from returning
describe('Bug #123 - Login crash', () => {
  it('should handle expired tokens gracefully', () => {
    const expiredToken = generateExpiredToken();
    expect(() => authenticate(expiredToken)).not.toThrow();
    expect(authenticate(expiredToken)).toBe(false);
  });
});
```

## 🚨 Emergency Debug Tools

### Universal Quick Checks:

#### Memory Issues:
```bash
# Node.js
node --inspect app.js  # Open chrome://inspect

# Python
python -m memory_profiler script.py

# Java
jmap -dump:file=heap.bin <pid>
```

#### CPU Issues:
```bash
# Linux/Mac
top -p <pid>

# Node.js
node --prof app.js
node --prof-process isolate-*.log
```

#### Network Issues:
```bash
# Check requests
curl -v https://api.example.com
netstat -an | grep LISTEN
tcpdump -i any port 3000
```

## 🎯 Debug Strategies by Bug Type

### "Works on my machine":
1. Check environment variables
2. Compare dependency versions
3. Check OS-specific code
4. Verify file paths (case sensitivity!)
5. Check timezone/locale differences

### Intermittent bugs:
1. Add extensive logging
2. Check race conditions
3. Monitor resource usage
4. Check external dependencies
5. Use stress testing

### Performance degradation:
1. Profile before/after
2. Check database queries
3. Look for N+1 problems
4. Check caching
5. Monitor memory leaks

## 💡 Pro Tips

### The Rubber Duck Method:
```markdown
1. Explain the bug to a rubber duck (or colleague)
2. Step through the code line by line
3. Often, you'll spot the issue while explaining
```

### Fresh Eyes Technique:
```bash
# After 30 minutes stuck:
git stash          # Save work
git checkout main  # Fresh perspective
# Take a 5-minute break
git stash pop      # Return with fresh eyes
```

### Sanity Checks:
```bash
# Is it plugged in?
- Server running?
- Database connected?
- Correct branch?
- Dependencies installed?
- Environment variables set?
```

## 📝 Debug Log Template

Keep a debug log for complex issues:

```markdown
## Bug: [Description]
**Date:** [Date]
**Severity:** Critical/High/Medium/Low

### Symptoms:
-

### Reproduction:
1.

### Hypotheses Tested:
- [ ] Hypothesis 1: [Result]
- [ ] Hypothesis 2: [Result]

### Solution:
-

### Lessons Learned:
-
```

Remember: Every bug is a learning opportunity! 🐛→📚
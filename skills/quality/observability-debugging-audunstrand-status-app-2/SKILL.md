---
name: Observability-First Debugging
description: Systematic debugging methodology that eliminates guessing and speculation. Add instrumentation to gather specific data that fully explains the problem. Evidence before hypothesis. Observation before solution.
---

# GitHub Copilot Skill: observability-debugging

> **Note:** This skill has been adapted from [claude-skillz](https://github.com/NTCoding/claude-skillz) 
> for use with GitHub Copilot Agent Skills.

---

# Observability-First Debugging

Stop guessing. Add observability. Understand what's actually happening.

## Core Principle

**Measure before you act.** When something isn't working, the solution is almost never to guess and try random fixes. The solution is to add instrumentation that produces the specific information needed to fully explain the issue.

## The Problem

Agents (and developers) fall into a guess-and-check trap:
- Try something → doesn't work
- Guess what might fix it → doesn't work
- Try another random thing → doesn't work
- User gets frusrtrated as the flailing continues

**Why this happens:** Insufficient data. You don't know what's actually happening, so you're shooting in the dark.

## The Solution

**Make the invisible visible.** Add logging, print statements, assertions, or debugging output that shows you:
- What values variables actually contain
- Which code paths are executing
- What external systems are returning
- Where expectations diverge from reality

## Debugging Protocol

### 1. Reproduce & Document Symptoms

**What exactly is failing?**
- Exact error message (copy-paste, don't paraphrase)
- Expected behavior vs actual behavior
- Minimal reproduction steps

**Don't:**
- Guess at what the error "probably means"
- Assume you know the cause from the symptom

### 2. Add Observability FIRST

**Before forming hypotheses, instrument the system:**

Add logging/print statements to show:
- Input values at function entry
- Intermediate computation results
- Return values
- Conditional branch taken
- External API responses
- State changes

**Example:**
```python
def process_request(data):
    print(f"[DEBUG] Received data: {data}")
    print(f"[DEBUG] Data type: {type(data)}")

    result = transform(data)
    print(f"[DEBUG] After transform: {result}")

    if validate(result):
        print(f"[DEBUG] Validation passed")
        return save(result)
    else:
        print(f"[DEBUG] Validation FAILED")
        print(f"[DEBUG] Validation errors: {get_validation_errors(result)}")
        return None
```

**The goal:** Produce output that definitively shows what's happening at each step.

### 3. Run & Observe

Execute with instrumentation active. Capture the output.

**Look for:**
- Values that don't match expectations
- Code paths not executing when they should
- Errors occurring earlier than the visible symptom
- Null/undefined where data should exist

### 4. Form Evidence-Based Hypothesis

**Now that you have data:**
- What does the evidence show?
- Where does reality diverge from expectation?
- What is the earliest point where things go wrong?

**Your hypothesis must:**
- Be based on observed data (not speculation)
- Explain all symptoms
- Be testable

### 5. Test Hypothesis

Add targeted instrumentation or experiments:
- If you think variable X is wrong, print it at every mutation point
- If you think function Y isn't being called, add entry/exit logging
- If you think the data structure is malformed, print its shape

### 6. Iterate

If hypothesis is wrong, the instrumentation will show why. Add more observability and repeat.

## Anti-Patterns to Eliminate

### ❌ Speculation Without Data

"Maybe it's a race condition"
"It might be a caching issue"
"Could be the API timeout"

**Fix:** Add logging that would confirm or deny each theory.

### ❌ Random Changes

Changing code hoping it fixes things without understanding why it broke.

**Fix:** First understand the bug via observability, then fix the root cause.

### ❌ Trying Multiple Things At Once

Making 3 changes simultaneously so you don't know which fixed it (or if it's actually fixed).

**Fix:** One change at a time. Verify each with instrumentation.

### ❌ Assuming Code Does What It Says

"This function should return user data" → doesn't mean it actually does.

**Fix:** Print what it actually returns. Verify assumptions.

## Observability Techniques by Context

### Command-Line Tools
```bash
set -x  # Print each command before executing
command -v foo  # Check if command exists
echo "Value: $VAR"  # Print variable values
```

### Code Debugging
- Print statements at key decision points
- Assertions for invariants
- Log function entry/exit
- Dump data structures
- Stack traces at error points

### API/Network Issues
- Print full request (URL, headers, body)
- Print full response (status, headers, body)
- Print timeout values
- Log retry attempts

### File Operations
- Print file paths being accessed
- Check file existence before operations
- Print file contents after reading
- Verify write success

### Environment Issues
- Print environment variables
- Print working directory
- Print PATH and other config
- Print version info for tools

## Decision Tree

```
Problem occurs
    ↓
Can you see the exact failure point?
    NO → Add logging/prints to trace execution flow
    YES ↓
Do you know the input values at failure?
    NO → Print input values and parameters
    YES ↓
Do you know what the code is actually doing?
    NO → Print intermediate results, branches taken
    YES ↓
Do you know why it's doing the wrong thing?
    NO → Print state, compare to expected state
    YES ↓
Fix the bug
```

## Examples

### Example 1: Test Failure

**Symptom:** Test fails with "Expected 3, got undefined"

**❌ Speculation:**
"Maybe the mock isn't working"
"Could be async timing issue"
[tries random fixes]

**✅ Observability-First:**
```javascript
test('calculates total', () => {
  const items = [1, 2, 3];
  console.log('Input items:', items);

  const result = calculateTotal(items);
  console.log('Result:', result);
  console.log('Result type:', typeof result);

  expect(result).toBe(6);
});
```

**Output shows:** `Result: undefined`

**Evidence-based action:** Check what `calculateTotal` actually returns. Add logging inside that function to see where it fails to compute/return.

### Example 2: API Call Not Working

**Symptom:** API returns 400 error

**❌ Speculation:**
"Maybe the endpoint changed"
"Could be auth token expired"
[tries different endpoints randomly]

**✅ Observability-First:**
```python
url = f"{BASE_URL}/api/users"
headers = {"Authorization": f"Bearer {token}"}
payload = {"name": name, "email": email}

print(f"[DEBUG] URL: {url}")
print(f"[DEBUG] Headers: {headers}")
print(f"[DEBUG] Payload: {payload}")

response = requests.post(url, headers=headers, json=payload)

print(f"[DEBUG] Status: {response.status_code}")
print(f"[DEBUG] Response: {response.text}")
```

**Output shows:** `Response: {"error": "email field is required"}`

**Evidence-based action:** The payload construction is wrong. Check where `email` variable is set.

### Example 3: File Not Found

**Symptom:** `FileNotFoundError: foo.txt`

**❌ Speculation:**
"Maybe the path is wrong"
[tries different path variations randomly]

**✅ Observability-First:**
```python
import os

file_path = "foo.txt"
print(f"[DEBUG] Looking for: {file_path}")
print(f"[DEBUG] Current directory: {os.getcwd()}")
print(f"[DEBUG] Directory contents: {os.listdir('.')}")
print(f"[DEBUG] File exists: {os.path.exists(file_path)}")

if not os.path.exists(file_path):
    abs_path = os.path.abspath(file_path)
    print(f"[DEBUG] Absolute path would be: {abs_path}")
```

**Output shows:** Current directory is `/app/src`, file is in `/app/data`

**Evidence-based action:** Use correct path `../data/foo.txt` or fix working directory.

## Integration with User Feedback

When user says you're going down the wrong path:
1. **Stop immediately**
2. **Ask what they're observing** that led them to that conclusion
3. **Add instrumentation** to verify their insight
4. **Observe output** and adjust approach

User knows their system. When they suggest simple/obvious solutions, they're usually right. Don't overthink it.

## Remember

- Debugging is a science, not guesswork
- Evidence before hypothesis
- Observation before solution
- Simple instrumentation > complex theories
- Listen to user clues

**The goal:** Produce specific data that fully explains the issue, then the fix becomes obvious.

---

Sources:
- [A systematic approach to debugging](https://ntietz.com/blog/how-i-debug-2023/)
- [Observability-based Debugging Mindset](https://mohitkarekar.com/posts/2024/observability-debugging/)
- [MIT 6.031: Debugging](http://web.mit.edu/6.031/www/fa17/classes/13-debugging/)

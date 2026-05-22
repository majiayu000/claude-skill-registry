---
name: runtime-error-explainer
description: Explains runtime errors and compilation failures with actionable debugging guidance. Use when Python or Java code throws runtime exceptions (NullPointerException, TypeError, AttributeError, etc.), compilation errors (syntax errors, type mismatches, import failures), or dependency issues. Analyzes error messages, stack traces, and code context to identify root causes and provide concrete fixes with examples. Distinct from test-related errors - focuses on errors during normal code execution and build processes.
---

# Runtime Error Explainer

Analyze runtime and compilation errors with clear explanations and actionable fixes.

## Core Capabilities

This skill helps debug runtime and compilation errors by:

1. **Parsing error output** - Extract key information from error messages and stack traces
2. **Identifying root causes** - Determine why errors occur during execution or compilation
3. **Explaining clearly** - Translate technical errors into understandable language
4. **Providing fixes** - Suggest concrete code changes with before/after examples
5. **Preventing recurrence** - Recommend best practices to avoid similar errors

## Error Analysis Workflow

### Step 1: Gather Error Context

Collect all relevant information about the error.

**Essential Information:**
- Complete error message and stack trace
- Programming language and version
- Code that triggered the error
- How the error was triggered (command, action, input)

**Additional Context (if available):**
- Recent code changes
- Environment details (OS, IDE, dependencies)
- Input data or parameters that caused error
- Configuration files

**How to Gather:**

```bash
# Python - Run with full traceback
python script.py

# Python - More verbose error output
python -v script.py

# Java - Compile with verbose output
javac -verbose MyClass.java

# Java - Run with stack trace
java -XX:+ShowCodeDetailsInExceptionMessages MyClass
```

### Step 2: Categorize the Error

Identify the error type using `references/error_catalog.md`:

**Error Categories:**

1. **Syntax/Compilation Errors**
   - Python: SyntaxError, IndentationError
   - Java: Compilation errors (missing semicolons, type errors)

2. **Runtime Errors**
   - Python: TypeError, AttributeError, ValueError, KeyError, IndexError
   - Java: NullPointerException, IllegalArgumentException, ArrayIndexOutOfBoundsException

3. **Import/Dependency Errors**
   - Python: ImportError, ModuleNotFoundError
   - Java: ClassNotFoundException, NoClassDefFoundError

4. **Type Errors**
   - Python: TypeError (wrong types in operations)
   - Java: Type mismatch compilation errors

5. **Name/Reference Errors**
   - Python: NameError, UnboundLocalError
   - Java: Variable not initialized, cannot find symbol

### Step 3: Extract Key Information

Pull out critical details from the error.

**From Error Message:**
- Error type and name
- Error description
- Line number where error occurred
- File name
- Variable names or values involved

**From Stack Trace:**
- Execution path leading to error
- Function/method call chain
- Origin of error in your code vs. library code

**Example Python Error:**

```
Traceback (most recent call last):
  File "app.py", line 45, in <module>
    result = process_user(None)
  File "app.py", line 12, in process_user
    return user.name.upper()
AttributeError: 'NoneType' object has no attribute 'name'
```

**Extracted Information:**
- Error type: `AttributeError`
- Problem: Tried to access `.name` on `None`
- Location: `app.py` line 12, in `process_user` function
- Root cause: `user` parameter is `None`

### Step 4: Identify Root Cause

Analyze why the error occurred.

**Common Root Causes:**

**Syntax/Compilation:**
- Missing or mismatched parentheses/brackets
- Incorrect indentation (Python)
- Missing semicolons (Java)
- Typos in keywords or variable names

**Runtime:**
- Null/None values where objects expected
- Wrong data types in operations
- Index out of bounds
- Missing dictionary keys
- Division by zero
- File not found

**Import/Dependency:**
- Module/package not installed
- Incorrect import path
- Circular imports
- Classpath issues (Java)

See `references/error_catalog.md` for detailed root cause analysis for each error type.

### Step 5: Provide Explanation

Structure the explanation with clear sections.

**Explanation Template:**

```markdown
## Error Summary

[One-sentence description of what went wrong]

## What Happened

[Explain the error in plain language]

**Error Type:** [Error name and category]
**Location:** [File and line number]
**Problem:** [What specifically failed]

## Root Cause

[Explain why this happened - the underlying issue]

## How to Fix

### Solution 1: [Most common fix] ⭐

[Specific code change or action]

```[language]
# Before
[problematic code]

# After
[fixed code]
```

**Why this works:** [Brief explanation]

### Solution 2: [Alternative approach]

[Another fix if Solution 1 doesn't apply]

## Verification

[How to verify the fix works]

```bash
[command to test]
```

## Prevention

[How to avoid this error in future]

- [Best practice 1]
- [Best practice 2]
- [Tool or technique recommendation]
```

### Step 6: Suggest Next Steps

Provide actionable debugging guidance.

**If fix is straightforward:**
- Show exact code change
- Provide command to verify
- Mention related code to review

**If more investigation needed:**
- Suggest adding print/logging statements
- Recommend debugging tools
- Propose simplification to isolate issue

**If environmental issue:**
- Suggest checking installation/versions
- Recommend environment verification
- Propose configuration review

## Common Error Patterns

### Python: AttributeError - NoneType

**Error:**
```
AttributeError: 'NoneType' object has no attribute 'method_name'
```

**Explanation:**

```markdown
## Error Summary
Attempted to call a method on None instead of an object instance.

## What Happened

**Error Type:** AttributeError
**Problem:** Code tried to access an attribute or method on `None`

Python functions return `None` by default if no explicit return statement is
used. When you try to call a method on `None`, you get this error.

## Root Cause

Common causes:
1. Function didn't return a value but you expected an object
2. Variable not initialized before use
3. Database/API query returned no result
4. Method called before object creation

## How to Fix

### Solution 1: Add None check ⭐

```python
# Before
result = get_user(user_id)
name = result.name  # Crashes if result is None

# After
result = get_user(user_id)
if result is not None:
    name = result.name
else:
    name = "Unknown"
```

**Why this works:** Defensively handles the case where `get_user` returns None.

### Solution 2: Fix the source function to always return a value

```python
# Before
def get_user(user_id):
    if user_id in users:
        return users[user_id]
    # Implicitly returns None

# After
def get_user(user_id):
    if user_id in users:
        return users[user_id]
    return User(id=user_id, name="Guest")  # Return default user
```

### Solution 3: Use walrus operator with conditional (Python 3.8+)

```python
# Assign and check in one line
if (result := get_user(user_id)) is not None:
    name = result.name
```

## Verification

```bash
python script.py
```

## Prevention

- Always check return values before using them
- Use type hints: `def get_user(user_id: int) -> Optional[User]:`
- Add assertions: `assert result is not None, "User not found"`
- Use Optional type and handle None explicitly
```

### Python: ImportError / ModuleNotFoundError

**Error:**
```
ModuleNotFoundError: No module named 'requests'
```

**Explanation:**

```markdown
## Error Summary
Python cannot find the module you're trying to import.

## What Happened

**Error Type:** ModuleNotFoundError (Python 3) or ImportError (Python 2)
**Problem:** The module is not installed or not in Python's path

## Root Cause

1. Package not installed via pip
2. Wrong virtual environment activated
3. Typo in module name
4. Package installed in different Python version

## How to Fix

### Solution 1: Install the missing package ⭐

```bash
# Install package
pip install requests

# Or if using Python 3 explicitly
pip3 install requests

# Or with specific Python version
python -m pip install requests
```

**Why this works:** Makes the package available to your Python environment.

### Solution 2: Activate correct virtual environment

```bash
# Check current environment
which python

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install package in virtual environment
pip install requests
```

### Solution 3: Check for typos

```python
# Wrong
import reqests  # Typo

# Correct
import requests
```

## Verification

```bash
python -c "import requests; print('Success')"
```

## Prevention

- Use requirements.txt: `pip install -r requirements.txt`
- Use virtual environments for project isolation
- Document all dependencies
- Use `pip freeze > requirements.txt` to capture dependencies
```

### Java: NullPointerException

**Error:**
```
Exception in thread "main" java.lang.NullPointerException
    at com.example.MyClass.process(MyClass.java:25)
```

**Explanation:**

```markdown
## Error Summary
Attempted to use an object reference that is null.

## What Happened

**Error Type:** NullPointerException
**Location:** MyClass.java, line 25
**Problem:** Tried to access a method or field on a null object

## Root Cause

Common causes:
1. Object not initialized before use
2. Method returned null unexpectedly
3. Array element is null
4. Forgotten to instantiate object

## How to Fix

### Solution 1: Add null check ⭐

```java
// Before
String name = user.getName().toUpperCase();

// After
if (user != null && user.getName() != null) {
    String name = user.getName().toUpperCase();
} else {
    String name = "UNKNOWN";
}
```

**Why this works:** Prevents accessing methods on null references.

### Solution 2: Use Optional (Java 8+)

```java
// Before
public User getUser(int id) {
    return userMap.get(id);  // Returns null if not found
}

String name = getUser(123).getName();  // NPE if user not found

// After
public Optional<User> getUser(int id) {
    return Optional.ofNullable(userMap.get(id));
}

String name = getUser(123)
    .map(User::getName)
    .orElse("Unknown");
```

### Solution 3: Initialize objects properly

```java
// Before
private User user;  // Field is null by default

public void process() {
    user.getName();  // NullPointerException
}

// After
private User user = new User();  // Initialize at declaration

// Or in constructor
public MyClass() {
    this.user = new User();
}
```

### Solution 4: Use Objects utility (Java 7+)

```java
import java.util.Objects;

// Throw meaningful exception if null
Objects.requireNonNull(user, "User must not be null");
String name = user.getName();
```

## Verification

```bash
javac MyClass.java && java MyClass
```

## Prevention

- Initialize all object fields
- Use Optional for potentially null values
- Add @Nullable/@NonNull annotations
- Enable null-safety warnings in IDE
- Consider using Objects.requireNonNull() for critical parameters
```

### Java: ClassNotFoundException

**Error:**
```
java.lang.ClassNotFoundException: com.example.MyClass
    at java.net.URLClassLoader.findClass(URLClassLoader.java:382)
```

**Explanation:**

```markdown
## Error Summary
Java cannot find the specified class at runtime.

## What Happened

**Error Type:** ClassNotFoundException
**Problem:** Class exists in source code but not found when running

## Root Cause

1. Class not in classpath
2. Package name doesn't match directory structure
3. .class file not compiled
4. Typo in class name
5. JAR file not included

## How to Fix

### Solution 1: Check classpath ⭐

```bash
# Compile with source files in correct package structure
javac -d bin src/com/example/MyClass.java

# Run with classpath pointing to bin directory
java -cp bin com.example.MyClass
```

**Why this works:** Ensures compiled .class files are in classpath.

### Solution 2: Verify package structure matches directories

```
Project structure should be:
src/
  com/
    example/
      MyClass.java
```

```java
// MyClass.java must declare matching package
package com.example;

public class MyClass {
    public static void main(String[] args) {
        System.out.println("Hello");
    }
}
```

### Solution 3: Include JAR files in classpath

```bash
# If MyClass is in external JAR
java -cp "lib/mylib.jar:." com.example.MyClass

# Windows (use semicolon)
java -cp "lib/mylib.jar;." com.example.MyClass
```

### Solution 4: Use Maven/Gradle (recommended)

Maven automatically manages classpaths.

```xml
<!-- pom.xml -->
<dependencies>
    <dependency>
        <groupId>com.example</groupId>
        <artifactId>my-library</artifactId>
        <version>1.0.0</version>
    </dependency>
</dependencies>
```

## Verification

```bash
# Check if class file exists
ls bin/com/example/MyClass.class

# Verify package declaration matches
head -1 src/com/example/MyClass.java
```

## Prevention

- Use build tools (Maven, Gradle) to manage dependencies
- Follow Java package naming conventions
- Keep package declarations synchronized with directory structure
- Use IDE features to auto-manage imports and packages
```

### Python: SyntaxError

**Error:**
```
  File "script.py", line 10
    if x == 5
           ^
SyntaxError: invalid syntax
```

**Explanation:**

```markdown
## Error Summary
Code has syntax error preventing Python from parsing it.

## What Happened

**Error Type:** SyntaxError
**Location:** Line 10
**Problem:** Missing colon at end of if statement

## Root Cause

Python syntax violated - common causes:
- Missing colons after if/for/while/def/class
- Unmatched parentheses/brackets
- Incorrect indentation
- Invalid operator usage

## How to Fix

### Solution 1: Add missing colon ⭐

```python
# Before
if x == 5
    print("Five")

# After
if x == 5:
    print("Five")
```

**Why this works:** Python requires colon to start code blocks.

### Solution 2: Check for unmatched brackets

```python
# Before
result = calculate(a, b, (c + d)
print(result)

# After
result = calculate(a, b, (c + d))
print(result)
```

### Solution 3: Fix indentation

```python
# Before (mixing tabs and spaces)
def my_function():
    x = 5
  return x  # Indentation error

# After (consistent spaces)
def my_function():
    x = 5
    return x
```

## Verification

```bash
# Python will parse file without running
python -m py_compile script.py

# Or just run it
python script.py
```

## Prevention

- Use IDE with syntax highlighting
- Enable linting (pylint, flake8)
- Use auto-formatters (black, autopep8)
- Configure editor to show whitespace characters
```

### Java: Type Mismatch Compilation Error

**Error:**
```
MyClass.java:15: error: incompatible types: int cannot be converted to String
    String result = 42;
                    ^
```

**Explanation:**

```markdown
## Error Summary
Trying to assign value of wrong type to variable.

## What Happened

**Error Type:** Compilation error - type mismatch
**Location:** Line 15
**Problem:** Assigning int (42) to String variable

## Root Cause

Java is statically typed - variables can only hold values of declared type
or compatible types.

## How to Fix

### Solution 1: Convert type explicitly ⭐

```java
// Before
String result = 42;

// After
String result = String.valueOf(42);
// or
String result = Integer.toString(42);
// or
String result = "" + 42;  // Concatenation with empty string
```

**Why this works:** Explicitly converts int to String.

### Solution 2: Change variable type

```java
// Before
String result = 42;

// After
int result = 42;
```

### Solution 3: Use correct literal type

```java
// Before (assigning int to double)
double price = 10;  // Works but not ideal

// After (use double literal)
double price = 10.0;
```

## Verification

```bash
javac MyClass.java
```

## Prevention

- Use proper type conversions
- Be aware of implicit type casting rules
- Use IDE suggestions for quick fixes
- Understand primitive types vs object types (int vs Integer)
```

## Language-Specific Notes

### Python Error Characteristics

**Common Patterns:**
- Runtime errors only (no compilation phase)
- Clear stack traces with file/line numbers
- Descriptive error messages
- Exception hierarchy (all inherit from BaseException)

**Key Files to Check:**
- Module `__init__.py` for package imports
- `sys.path` for import resolution
- Virtual environment activation

**Debugging Tools:**
```bash
# Interactive debugging
python -m pdb script.py

# Print traceback programmatically
import traceback
traceback.print_exc()
```

### Java Error Characteristics

**Common Patterns:**
- Compilation errors vs runtime errors
- Less descriptive error messages than Python
- Line numbers in stack traces
- Checked vs unchecked exceptions

**Key Files to Check:**
- `pom.xml` (Maven) or `build.gradle` (Gradle)
- Package structure matches directory structure
- CLASSPATH environment variable

**Debugging Tools:**
```bash
# Verbose compilation
javac -verbose MyClass.java

# Show detailed exception messages (Java 14+)
java -XX:+ShowCodeDetailsInExceptionMessages MyClass

# Using debugger
jdb MyClass
```

## Quick Reference: Error Categories

| Category | Python Examples | Java Examples | Common Fix |
|----------|----------------|---------------|------------|
| Null/None errors | AttributeError on None | NullPointerException | Add null checks |
| Type errors | TypeError | Type mismatch error | Fix types or convert |
| Import errors | ModuleNotFoundError | ClassNotFoundException | Check imports/classpath |
| Syntax errors | SyntaxError | Compilation errors | Fix syntax |
| Index errors | IndexError | ArrayIndexOutOfBoundsException | Check array bounds |
| Name errors | NameError | Cannot find symbol | Fix variable names |
| Key errors | KeyError | - | Check dict keys exist |

## Resources

- **`references/error_catalog.md`** - Comprehensive catalog of Python and Java errors with detailed examples, root causes, and solutions
- **`references/debugging_guide.md`** - Systematic debugging strategies, tools, and techniques for complex errors

## Best Practices

1. **Read the full error message** - Don't skip stack traces
2. **Identify error location** - Line number and file are critical
3. **Understand the error type** - Each type has typical causes
4. **Check recent changes** - Often errors relate to recent edits
5. **Reproduce consistently** - Ensure error happens reliably
6. **Simplify to isolate** - Remove code until error disappears
7. **Use debugging tools** - Debuggers are more powerful than print statements
8. **Fix root cause, not symptoms** - Adding try/except without understanding hides problems
9. **Add defensive code** - Null checks, type validation prevent errors
10. **Learn from errors** - Understand why it happened to prevent recurrence

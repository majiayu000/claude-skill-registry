---
name: Wheels Anti-Pattern Detector
description: Automatically detect and prevent common Wheels framework errors before code is generated. This skill activates during ANY Wheels code generation (models, controllers, views, migrations) to validate patterns and prevent known issues. Scans for mixed arguments, query/array confusion, non-existent helpers, and database-specific SQL.
---

# Wheels Anti-Pattern Detector

## Purpose

This skill runs **AUTOMATICALLY** during any Wheels code generation to catch common errors before they're written to files.

## When to Use This Skill

Activate automatically during:
- Model generation (check associations, validations)
- Controller generation (check method calls)
- View generation (check queries, form helpers)
- Migration generation (check SQL compatibility)
- Code review and refactoring
- Any Wheels code modification

## 🚨 Production-Tested Critical Detections

### 1. CLI Generator String Boolean Values (CRITICAL)

**🔴 CRITICAL:** The CLI `wheels g migration` command generates migrations with string boolean values that silently fail.

**Detection Pattern:**
```regex
createTable\s*\([^)]*force\s*=\s*['"][^'"]*['"]
createTable\s*\([^)]*id\s*=\s*['"][^'"]*['"]
```

**Examples to Detect:**
```cfm
❌ t = createTable(name='users', force='false', id='true', primaryKey='id');
❌ t = createTable(name='posts', force='false');
❌ t = createTable(name='comments', id='true');
```

**Auto-Fix:**
```cfm
✅ t = createTable(name='users');
✅ t = createTable(name='posts');
✅ t = createTable(name='comments');
```

**Error Message:**
```
⚠️  CRITICAL: CLI-generated string boolean values detected
Line: 5
Found: createTable(name='users', force='false', id='true', primaryKey='id')
Fix:   createTable(name='users')

CLI generators create STRING booleans ('false', 'true') that don't work.
Remove force/id/primaryKey parameters and use Wheels defaults instead.
This will cause "NoPrimaryKey" errors if not fixed!
```

### 2. Missing setPrimaryKey() in Models (CRITICAL)

**🔴 CRITICAL:** Models must explicitly call `setPrimaryKey("id")` in config(), even when migrations are correct.

**Detection Pattern:**
```regex
component\s+extends\s*=\s*["']Model["'][\s\S]*?function\s+config\s*\(\s*\)\s*\{(?![\s\S]*?setPrimaryKey)
```

**Examples to Detect:**
```cfm
❌ component extends="Model" {
    function config() {
        table("users");
        hasMany(name="posts");  // Missing setPrimaryKey!
    }
}
```

**Auto-Fix:**
```cfm
✅ component extends="Model" {
    function config() {
        table("users");
        setPrimaryKey("id");  // Added!
        hasMany(name="posts");
    }
}
```

**Error Message:**
```
⚠️  CRITICAL: Missing setPrimaryKey() in model config()
Line: 3
Found: config() without setPrimaryKey() declaration
Fix:   Add setPrimaryKey("id") as first line after table() declaration

Even with correct migrations, Wheels ORM requires explicit primary key declaration.
This will cause "Wheels.NoPrimaryKey" errors if not added!
```

### 3. Property Access Without structKeyExists() Check (CRITICAL)

**🔴 CRITICAL:** Accessing properties in beforeCreate/beforeValidation callbacks without existence check causes errors.

**Detection Pattern:**
```regex
function\s+(beforeCreate|beforeValidation|setDefaults)[\s\S]*?if\s*\(\s*!len\s*\(\s*this\.\w+\s*\)\s*\)(?![\s\S]*?structKeyExists)
```

**Examples to Detect:**
```cfm
❌ function setDefaults() {
    if (!len(this.followersCount)) {  // Error if property doesn't exist!
        this.followersCount = 0;
    }
}
```

**Auto-Fix:**
```cfm
✅ function setDefaults() {
    if (!structKeyExists(this, "followersCount") || !len(this.followersCount)) {
        this.followersCount = 0;
    }
}
```

**Error Message:**
```
⚠️  CRITICAL: Property access without structKeyExists() check
Line: 15
Found: if (!len(this.followersCount)) in beforeCreate callback
Fix:   if (!structKeyExists(this, "followersCount") || !len(this.followersCount))

In beforeCreate/beforeValidation callbacks, properties may not exist yet.
This will cause "no accessible Member" errors if not checked!
```

### 4. Wrong Validation Parameter Names (CRITICAL)

**🔴 CRITICAL:** Validation functions use "properties" (plural) not "property" (singular).

**Detection Pattern:**
```regex
validates\w+Of\s*\(\s*property\s*=
```

**Examples to Detect:**
```cfm
❌ validatesPresenceOf(property="username,email")
❌ validatesUniquenessOf(property="email")
❌ validatesFormatOf(property="email", regEx="...")
```

**Auto-Fix:**
```cfm
✅ validatesPresenceOf(properties="username,email")
✅ validatesUniquenessOf(properties="email")
✅ validatesFormatOf(properties="email", regEx="...")
```

**Error Message:**
```
⚠️  CRITICAL: Wrong validation parameter name
Line: 8
Found: validatesPresenceOf(property="username")
Fix:   validatesPresenceOf(properties="username")

Wheels validation functions use "properties" (PLURAL), not "property".
This validation will be silently ignored if not fixed!
```

## Critical Anti-Patterns

### 5. Mixed Argument Styles

**Detection Pattern:**
```regex
(hasMany|belongsTo|hasManyThrough|validatesPresenceOf|validatesUniquenessOf|validatesFormatOf|validatesLengthOf|findByKey|findAll|findOne)\s*\(\s*"[^"]+"\s*,\s*\w+\s*=
```

**Examples:**
```cfm
❌ hasMany("comments", dependent="delete")
❌ belongsTo("user", foreignKey="userId")
❌ validatesPresenceOf("title", message="Required")
❌ findByKey(params.key, include="comments")
❌ findAll(order="id DESC", where="active = 1")
```

**Auto-Fix:**
```cfm
✅ hasMany(name="comments", dependent="delete")
✅ belongsTo(name="user", foreignKey="userId")
✅ validatesPresenceOf(property="title", message="Required")
✅ findByKey(key=params.key, include="comments")
✅ findAll(order="id DESC", where="active = 1")  // No positional args, OK
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Mixed argument styles
Line: 5
Found: hasMany("comments", dependent="delete")
Fix:   hasMany(name="comments", dependent="delete")

Wheels requires consistent parameter syntax - either ALL positional OR ALL named.
When using options like 'dependent', you MUST use named arguments for ALL parameters.
```

### 2. Query/Array Confusion

**Detection Pattern:**
```regex
ArrayLen\s*\(\s*\w+\.(comments|posts|tags|users|[a-z]+)\(\s*\)\s*\)
```

**Examples:**
```cfm
❌ <cfset count = ArrayLen(post.comments())>
❌ <cfloop array="#post.comments()#" index="comment">
❌ <cfif ArrayIsEmpty(user.posts())>
```

**Auto-Fix:**
```cfm
✅ <cfset count = post.comments().recordCount>
✅ <cfloop query="comments">  // After: comments = post.comments()
✅ <cfif user.posts().recordCount == 0>
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: ArrayLen() on query object
Line: 12
Found: ArrayLen(post.comments())
Fix:   post.comments().recordCount

Wheels associations return QUERIES, not arrays. Use .recordCount for count.
```

### 3. Association Access Inside Query Loops

**Detection Pattern:**
```regex
<cfloop\s+query="[^"]+">[\s\S]*?\.\w+\(\)\.recordCount
```

**Examples:**
```cfm
❌ <cfloop query="posts">
    <p>#posts.comments().recordCount# comments</p>
</cfloop>
```

**Auto-Fix:**
```cfm
✅ <cfloop query="posts">
    <cfset postComments = model("Post").findByKey(posts.id).comments()>
    <p>#postComments.recordCount# comments</p>
</cfloop>
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Association access inside query loop
Line: 15
Found: posts.comments().recordCount inside <cfloop query="posts">
Fix:   Load association separately: postComments = model("Post").findByKey(posts.id).comments()

Cannot access associations directly on query objects inside loops.
Must reload the model object first.
```

### 4. Non-Existent Form Helpers

**Detection Pattern:**
```regex
(emailField|passwordField|numberField|dateField|timeField|urlField|telField)\s*\(
```

**Examples:**
```cfm
❌ #emailField(objectName="user", property="email")#
❌ #passwordField(objectName="user", property="password")#
❌ #numberField(objectName="product", property="price")#
❌ #urlField(objectName="company", property="website")#
```

**Auto-Fix:**
```cfm
✅ #textField(objectName="user", property="email", type="email")#
✅ #textField(objectName="user", property="password", type="password")#
✅ #textField(objectName="product", property="price", type="number")#
✅ #textField(objectName="company", property="website", type="url")#
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Non-existent form helper
Line: 23
Found: emailField(objectName="user", property="email")
Fix:   textField(objectName="user", property="email", type="email")

Wheels doesn't have specialized field helpers like emailField().
Use textField() with the 'type' attribute instead.
```

### 5. Rails-Style Nested Routing

**Detection Pattern:**
```regex
resources\s*\([^)]+,\s*(nested|namespace)\s*=
```

**Examples:**
```cfm
❌ resources("posts", nested=resources("comments"))
❌ resources("users", namespace="admin")
```

**Auto-Fix:**
```cfm
✅ resources("posts")
✅ resources("comments")
// Define separately, not nested
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Rails-style nested routing
Line: 8
Found: resources("posts", nested=resources("comments"))
Fix:   resources("posts") and resources("comments") as separate declarations

Wheels doesn't support Rails-style nested resources.
Define resources separately and handle nesting in controllers.
```

### 6. Database-Specific SQL Functions

**Detection Pattern:**
```regex
(DATE_SUB|DATE_ADD|NOW|CURDATE|CURTIME|DATEDIFF|INTERVAL)\s*\(
```

**Examples:**
```cfm
❌ execute("INSERT INTO posts (publishedAt) VALUES (DATE_SUB(NOW(), INTERVAL 1 DAY))")
❌ execute("SELECT * FROM posts WHERE createdAt > CURDATE()")
❌ execute("UPDATE posts SET modifiedAt = NOW()")
```

**Auto-Fix:**
```cfm
✅ var pastDate = DateAdd("d", -1, Now());
   execute("INSERT INTO posts (publishedAt) VALUES (TIMESTAMP '#DateFormat(pastDate, "yyyy-mm-dd")# #TimeFormat(pastDate, "HH:mm:ss")#')")

✅ var today = Now();
   execute("SELECT * FROM posts WHERE createdAt > TIMESTAMP '#DateFormat(today, "yyyy-mm-dd")# 00:00:00'")

✅ var now = Now();
   execute("UPDATE posts SET modifiedAt = TIMESTAMP '#DateFormat(now, "yyyy-mm-dd")# #TimeFormat(now, "HH:mm:ss")#'")
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Database-specific SQL function
Line: 34
Found: DATE_SUB(NOW(), INTERVAL 1 DAY)
Fix:   Use CFML DateAdd() + TIMESTAMP formatting

MySQL-specific date functions won't work across all databases.
Use CFML date functions (DateAdd, DateFormat, TimeFormat) for compatibility.
```

### 7. Missing CSRF Protection Check

**Detection Pattern:**
```regex
<form[^>]*method\s*=\s*["']post["'][^>]*>(?![\s\S]*csrf)
```

**Examples:**
```cfm
❌ <form method="post" action="/users/create">
    <!--- No CSRF token --->
</form>
```

**Auto-Fix:**
```cfm
✅ #startFormTag(action="create", method="post")#
    <!--- CSRF token automatically included --->
#endFormTag()#
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Form without CSRF protection
Line: 45
Found: <form method="post"> without CSRF token
Fix:   Use #startFormTag()# which includes CSRF automatically

Wheels provides built-in CSRF protection.
Use startFormTag() instead of raw <form> tags.
```

### 8. Inconsistent Property Style in config()

**Detection Pattern:**
Check for mixing positional and named arguments within same config() function

**Examples:**
```cfm
❌ function config() {
    hasMany("comments");  // Positional
    belongsTo(name="user");  // Named
}
```

**Auto-Fix:**
```cfm
✅ function config() {
    hasMany(name="comments");  // All named
    belongsTo(name="user");    // All named
}
```

**Error Message:**
```
⚠️  ANTI-PATTERN DETECTED: Inconsistent parameter style in config()
Lines: 5-6
Found: Mixed positional and named arguments
Fix:   Use SAME style for ALL association/validation declarations

config() function should use consistent argument style throughout.
Either ALL positional OR ALL named - never mix them.
```

## Validation Workflow

### Before Writing Any File

1. **Scan Generated Code:** Run all anti-pattern regex checks
2. **If Pattern Detected:**
   - Display warning message
   - Show before/after comparison
   - Auto-fix the code
   - Log the fix for user awareness
3. **Validate Fix:** Ensure fix doesn't introduce new issues
4. **Write Corrected File:** Save the validated code

### Example Validation Output

```
🔍 Validating generated code...

⚠️  3 anti-patterns detected and auto-fixed:

1. [Line 8] Mixed argument styles
   Before: hasMany("comments", dependent="delete")
   After:  hasMany(name="comments", dependent="delete")

2. [Line 15] Query/Array confusion
   Before: ArrayLen(post.comments())
   After:  post.comments().recordCount

3. [Line 23] Non-existent helper
   Before: emailField(objectName="user", property="email")
   After:  textField(objectName="user", property="email", type="email")

✅ All anti-patterns fixed. Writing file...
```

## Integration Points

### Auto-Activation During:

1. **Model Generation** (wheels-model-generator)
   - Check association argument styles
   - Check validation argument styles
   - Check callback definitions

2. **Controller Generation** (wheels-controller-generator)
   - Check findByKey/findAll argument styles
   - Check renderPage/redirectTo calls
   - Check parameter verification

3. **View Generation** (wheels-view-generator)
   - Check query handling
   - Check form helper usage
   - Check association access in loops
   - Check CSRF protection

4. **Migration Generation** (wheels-migration-generator)
   - Check for database-specific SQL
   - Check date/time handling
   - Check transaction structure

## Testing Anti-Pattern Detection

### Test Cases

```cfm
// Test Case 1: Should detect mixed arguments
Input:  hasMany("comments", dependent="delete")
Detect: ✅ YES
Fix:    hasMany(name="comments", dependent="delete")

// Test Case 2: Should allow consistent named arguments
Input:  hasMany(name="comments", dependent="delete")
Detect: ❌ NO (Correct pattern)

// Test Case 3: Should allow consistent positional (no options)
Input:  hasMany("comments")
Detect: ❌ NO (Correct pattern)

// Test Case 4: Should detect ArrayLen on association
Input:  ArrayLen(post.comments())
Detect: ✅ YES
Fix:    post.comments().recordCount

// Test Case 5: Should detect non-existent helper
Input:  emailField(objectName="user", property="email")
Detect: ✅ YES
Fix:    textField(objectName="user", property="email", type="email")

// Test Case 6: Should detect database-specific SQL
Input:  "INSERT INTO posts (date) VALUES (NOW())"
Detect: ✅ YES
Fix:    Use CFML Now() with formatting

// Test Case 7: Should detect inconsistent config styles
Input:  hasMany("comments") + belongsTo(name="user")
Detect: ✅ YES
Fix:    Both use named arguments
```

## Configuration

### Enable/Disable Checks

```json
// .claude/anti-pattern-config.json
{
  "checks": {
    "mixedArguments": true,
    "queryArrayConfusion": true,
    "nonExistentHelpers": true,
    "railsRouting": true,
    "databaseSpecificSQL": true,
    "csrfProtection": true,
    "inconsistentConfig": true
  },
  "autoFix": true,
  "reportLevel": "warning"
}
```

## Success Metrics

- **Detection Rate:** 100% of known anti-patterns caught
- **False Positives:** <5%
- **Auto-Fix Success:** >95%
- **User Awareness:** Clear before/after shown for all fixes

## Related Skills

All Wheels generator skills depend on this skill for validation.

---

**Generated by:** Wheels Anti-Pattern Detector Skill v1.0
**Framework:** CFWheels 3.0+
**Last Updated:** 2025-10-20

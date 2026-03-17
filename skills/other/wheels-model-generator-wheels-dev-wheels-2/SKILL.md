---
name: Wheels Model Generator
description: Generate Wheels ORM models with proper validations, associations, and methods. Use when the user wants to create or modify a Wheels model, add validations, define associations (hasMany, belongsTo, hasManyThrough), or implement custom model methods. Prevents common Wheels-specific errors like mixed argument styles and ensures proper CFML syntax.
---

# Wheels Model Generator

## When to Use This Skill

Activate this skill automatically when:
- User requests to create a new model (e.g., "create a User model")
- User wants to add associations (e.g., "Post hasMany Comments")
- User needs to add validations (e.g., "validate email format")
- User wants to implement custom model methods
- User is modifying existing model configuration
- User mentions: model, validation, association, hasMany, belongsTo, ORM

## Critical Anti-Patterns to Prevent

### ❌ ANTI-PATTERN 1: Mixed Argument Styles

**NEVER mix positional and named arguments in Wheels functions.**

**WRONG:**
```cfm
hasMany("comments", dependent="delete")  // ❌ Mixed
belongsTo("user", foreignKey="userId")   // ❌ Mixed
validatesPresenceOf("title", message="Required")  // ❌ Mixed
```

**CORRECT:**
```cfm
// Option 1: All named parameters (RECOMMENDED)
hasMany(name="comments", dependent="delete")
belongsTo(name="user", foreignKey="userId")
validatesPresenceOf(property="title", message="Required")

// Option 2: All positional parameters (only when no additional options)
hasMany("comments")
belongsTo("user")
validatesPresenceOf("title")
```

### ❌ ANTI-PATTERN 2: Inconsistent Parameter Styles

**Use the SAME style throughout the entire config() function.**

**WRONG:**
```cfm
function config() {
    hasMany("comments");  // Positional
    belongsTo(name="user");  // Named
}
```

**CORRECT:**
```cfm
function config() {
    hasMany(name="comments");  // All named
    belongsTo(name="user");    // All named
}
```

### ❌ ANTI-PATTERN 3: Wrong Parameter Names (CRITICAL)

**🚨 PRODUCTION FINDING: Wheels validation functions use "properties" (PLURAL), not "property"!**

**WRONG:**
```cfm
validatesPresenceOf(property="username,email")  // ❌ "property" parameter doesn't exist!
validatesUniquenessOf(property="email")         // ❌ Wrong parameter name
validatesFormatOf(property="email", regEx="...")  // ❌ Won't work
validatesLengthOf(property="username", minimum=3)  // ❌ Parameter not recognized
```

**CORRECT:**
```cfm
validatesPresenceOf(properties="username,email")  // ✅ Use "properties" (plural)
validatesUniquenessOf(properties="email")         // ✅ Correct
validatesFormatOf(properties="email", regEx="...")  // ✅ Works
validatesLengthOf(properties="username", minimum=3)  // ✅ Recognized
```

**Similarly for custom validation:**
```cfm
validate(methods="customValidation")  // ✅ "methods" (plural)
validate(method="customValidation")   // ❌ "method" doesn't exist
```

## 🚨 Production-Tested Critical Fixes

### 1. setPrimaryKey() Requirement (CRITICAL)

**🔴 CRITICAL DISCOVERY:** Even when migrations correctly create primary keys, models **MUST** explicitly declare them using `setPrimaryKey()` in the `config()` method.

**Problem Symptom:**
```
Error: "Wheels.NoPrimaryKey: No primary key exists on the users table"
```

**Even when migration succeeded:**
```cfm
// Migration appeared successful
t = createTable(name="users");  // Creates id column as primary key
t.create();  // ✅ Reports success
```

**Required Fix in Model:**
```cfm
component extends="Model" {
    function config() {
        table("users");
        setPrimaryKey("id");  // 🚨 MANDATORY - Always add this line!

        // Rest of configuration...
        hasMany(name="tweets", dependent="delete");
        validatesPresenceOf(properties="username,email");
    }
}
```

**Why This Happens:**
- CLI generators may not add `setPrimaryKey()` to generated models
- Wheels ORM requires explicit primary key declaration in model
- Missing this causes "NoPrimaryKey" error even with correct database schema
- **ALWAYS add `setPrimaryKey("id")` to EVERY model's config() method**

**Rule:**
```
✅ MANDATORY: Add setPrimaryKey("id") to EVERY model config() - no exceptions!
```

### 2. Property Access in beforeCreate() Callbacks (CRITICAL)

**🔴 CRITICAL DISCOVERY:** Accessing properties in `beforeCreate()` callbacks without checking existence causes "no accessible Member" errors.

**Problem Symptom:**
```
Error: "Component [app.models.User] has no accessible Member with name [FOLLOWERSCOUNT]"
```

**❌ WRONG - Causes Error:**
```cfm
component extends="Model" {
    function config() {
        beforeCreate("setDefaults");
    }

    function setDefaults() {
        // ❌ Error if property doesn't exist yet!
        if (!len(this.followersCount)) {
            this.followersCount = 0;
        }
    }
}
```

**✅ CORRECT - Always Check Existence First:**
```cfm
component extends="Model" {
    function config() {
        beforeCreate("setDefaults");
    }

    function setDefaults() {
        // ✅ Check existence first!
        if (!structKeyExists(this, "followersCount") || !len(this.followersCount)) {
            this.followersCount = 0;
        }

        if (!structKeyExists(this, "followingCount") || !len(this.followingCount)) {
            this.followingCount = 0;
        }

        if (!structKeyExists(this, "tweetsCount") || !len(this.tweetsCount)) {
            this.tweetsCount = 0;
        }
    }
}
```

**Why This Happens:**
- In `beforeCreate()`, properties may not exist yet in the `this` scope
- Direct access like `this.propertyName` throws error if property doesn't exist
- Must use `structKeyExists(this, "propertyName")` before accessing
- This applies to ANY property access in beforeCreate, beforeValidation callbacks

**Rule:**
```
✅ MANDATORY: Use structKeyExists(this, "property") before accessing properties in beforeCreate()
```

### 3. Complete Production-Ready Model Template

**Use this template for ALL model generation to avoid common issues:**

```cfm
component extends="Model" {

    function config() {
        // 🚨 MANDATORY: Always set primary key
        table("users");
        setPrimaryKey("id");  // CRITICAL - Never omit this!

        // Associations - ALWAYS use named parameters
        hasMany(name="tweets", dependent="delete");
        hasMany(name="likes", dependent="delete");
        hasMany(name="followings", foreignKey="followerId", dependent="delete");
        hasMany(name="followers", foreignKey="followingId", dependent="delete");

        // Validations - Use "properties" (plural)
        validatesPresenceOf(properties="username,email,passwordHash");
        validatesUniquenessOf(properties="username,email", message="[property] already taken");
        validatesFormatOf(properties="email", regEx="^[\w\.-]+@[\w\.-]+\.\w+$", message="Invalid email format");
        validatesLengthOf(properties="username", minimum=3, maximum=50);
        validatesLengthOf(properties="bio", maximum=160, allowBlank=true);

        // Callbacks
        beforeCreate("setDefaults");
    }

    // 🚨 CRITICAL: Always use structKeyExists() in beforeCreate
    function setDefaults() {
        if (!structKeyExists(this, "followersCount") || !len(this.followersCount)) {
            this.followersCount = 0;
        }
        if (!structKeyExists(this, "followingCount") || !len(this.followingCount)) {
            this.followingCount = 0;
        }
        if (!structKeyExists(this, "tweetsCount") || !len(this.tweetsCount)) {
            this.tweetsCount = 0;
        }
    }

    // Custom methods
    function fullName() {
        return "@" & this.username;
    }

    function isFollowing(required numeric userId) {
        var follow = model("Follow").findOne(where="followerId = #this.id# AND followingId = #arguments.userId#");
        return isObject(follow);
    }
}
```

### 4. CLI Generator Post-Generation Checklist

**After using CLI `wheels g model` command, ALWAYS review and fix:**

- [ ] Add `setPrimaryKey("id")` to config() method
- [ ] Change all validation parameters from `property=` to `properties=`
- [ ] Change custom validation from `method=` to `methods=`
- [ ] Add `structKeyExists()` checks in all beforeCreate/beforeValidation callbacks
- [ ] Ensure all association parameters use named style (name=, dependent=)
- [ ] Verify all callback methods are marked `private`
- [ ] Test model instantiation: `model("ModelName").new()` should not error

## Model Generation Template

### Basic Model Structure

```cfm
component extends="Model" {

    function config() {
        // Table configuration (optional - only if table name differs from convention)
        // table(name="custom_table_name");

        // Associations - ALWAYS use named parameters for consistency
        hasMany(name="association_name", dependent="delete");
        belongsTo(name="parent_model");

        // Validations - ALWAYS use named parameters
        validatesPresenceOf(property="field1,field2");
        validatesUniquenessOf(property="field_name");

        // Callbacks (optional)
        beforeValidationOnCreate("methodName");
        afterCreate("methodName");
    }

    // Custom public methods
    public string function customMethod(required string param) {
        // Implementation
        return result;
    }

    // Private helper methods
    private void function helperMethod() {
        // Implementation
    }
}
```

## Association Patterns

### One-to-Many (Parent → Children)

**Parent Model (Post):**
```cfm
component extends="Model" {
    function config() {
        hasMany(name="comments", dependent="delete");
        // dependent="delete" removes associated records when parent is deleted
    }
}
```

**Child Model (Comment):**
```cfm
component extends="Model" {
    function config() {
        belongsTo(name="post");
    }
}
```

### Many-to-Many (Through Join Table)

**Post Model:**
```cfm
component extends="Model" {
    function config() {
        hasMany(name="postTags");
        hasManyThrough(name="tags", through="postTags");
    }
}
```

**Tag Model:**
```cfm
component extends="Model" {
    function config() {
        hasMany(name="postTags");
        hasManyThrough(name="posts", through="postTags");
    }
}
```

**PostTag Join Model:**
```cfm
component extends="Model" {
    function config() {
        belongsTo(name="post");
        belongsTo(name="tag");
    }
}
```

### Self-Referential Association

**User Model (for followers/following):**
```cfm
component extends="Model" {
    function config() {
        hasMany(name="followings", modelName="Follow", foreignKey="followerId");
        hasMany(name="followers", modelName="Follow", foreignKey="followingId");
    }
}
```

## Validation Patterns

### Presence Validation

```cfm
// Single property
validatesPresenceOf(property="email");

// Multiple properties
validatesPresenceOf(property="name,email,password");

// With custom message
validatesPresenceOf(property="email", message="Email is required");

// Conditional validation
validatesPresenceOf(property="password", condition="isNew()");
```

### Uniqueness Validation

```cfm
// Basic uniqueness
validatesUniquenessOf(property="email");

// Case-insensitive uniqueness
validatesUniquenessOf(property="username", message="Username already taken");

// Scoped uniqueness
validatesUniquenessOf(property="slug", scope="categoryId");
```

### Format Validation (Regular Expressions)

```cfm
// Email format
validatesFormatOf(
    property="email",
    regEx="^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$",
    message="Please enter a valid email address"
);

// URL format
validatesFormatOf(
    property="website",
    regEx="^https?://[^\s/$.?#].[^\s]*$",
    message="Please enter a valid URL"
);

// Phone number format (US)
validatesFormatOf(
    property="phone",
    regEx="^\d{3}-?\d{3}-?\d{4}$",
    message="Phone must be in format XXX-XXX-XXXX"
);
```

### Length Validation

```cfm
// Minimum length
validatesLengthOf(property="password", minimum=8);

// Maximum length
validatesLengthOf(property="title", maximum=200);

// Exact length
validatesLengthOf(property="zipCode", is=5);

// Within range
validatesLengthOf(
    property="username",
    minimum=3,
    maximum=20,
    message="Username must be between 3 and 20 characters"
);
```

### Numericality Validation

```cfm
// Must be numeric
validatesNumericalityOf(property="age");

// Integer only
validatesNumericalityOf(property="quantity", onlyInteger=true);

// Greater than
validatesNumericalityOf(
    property="price",
    greaterThan=0,
    message="Price must be positive"
);

// Less than or equal to
validatesNumericalityOf(property="discount", lessThanOrEqualTo=100);

// Within range
validatesNumericalityOf(
    property="rating",
    greaterThanOrEqualTo=1,
    lessThanOrEqualTo=5
);
```

### Confirmation Validation

```cfm
// Password confirmation
validatesConfirmationOf(property="password");

// Requires passwordConfirmation property in form
// <input name="user[password]">
// <input name="user[passwordConfirmation]">
```

### Inclusion/Exclusion Validation

```cfm
// Must be in list
validatesInclusionOf(
    property="status",
    list="draft,published,archived",
    message="Invalid status"
);

// Cannot be in list
validatesExclusionOf(
    property="username",
    list="admin,root,system",
    message="Username is reserved"
);
```

### Custom Validation

```cfm
component extends="Model" {
    function config() {
        // Register custom validation method
        validate(method="customValidation");
    }

    private void function customValidation() {
        // Add error if validation fails
        if (len(this.email) && !isValid("email", this.email)) {
            addError(property="email", message="Invalid email format");
        }

        // Complex business logic
        if (structKeyExists(this, "startDate") && structKeyExists(this, "endDate")) {
            if (this.endDate < this.startDate) {
                addError(property="endDate", message="End date must be after start date");
            }
        }
    }
}
```

## Callback Patterns

### Available Callbacks

```cfm
// Before callbacks
beforeValidation("methodName")
beforeValidationOnCreate("methodName")
beforeValidationOnUpdate("methodName")

beforeSave("methodName")
beforeCreate("methodName")
beforeUpdate("methodName")
beforeDelete("methodName")

// After callbacks
afterValidation("methodName")
afterValidationOnCreate("methodName")
afterValidationOnUpdate("methodName")

afterSave("methodName")
afterCreate("methodName")
afterUpdate("methodName")
afterDelete("methodName")

// New callbacks
afterNew("methodName")
afterFind("methodName")
```

### Common Callback Use Cases

```cfm
component extends="Model" {
    function config() {
        // Auto-generate slug before validation
        beforeValidationOnCreate("generateSlug");

        // Set timestamps manually if needed
        beforeCreate("setCreatedTimestamp");
        beforeUpdate("setUpdatedTimestamp");

        // Hash password before saving
        beforeSave("hashPassword");

        // Send welcome email after user creation
        afterCreate("sendWelcomeEmail");
    }

    private void function generateSlug() {
        if (!len(this.slug) && len(this.title)) {
            this.slug = lCase(reReplace(this.title, "[^a-zA-Z0-9]", "-", "ALL"));
            this.slug = reReplace(this.slug, "-+", "-", "ALL");
            this.slug = reReplace(this.slug, "^-|-$", "", "ALL");
        }
    }

    private void function hashPassword() {
        if (structKeyExists(this, "password") && !isHashed(this.password)) {
            this.password = hash(this.password, "SHA-512");
        }
    }

    private void function sendWelcomeEmail() {
        // Email sending logic
        sendMail(
            to=this.email,
            subject="Welcome!",
            body="Thanks for signing up."
        );
    }
}
```

## Custom Method Patterns

### Common Custom Methods

```cfm
component extends="Model" {

    // Full name accessor
    public string function fullName() {
        return this.firstName & " " & this.lastName;
    }

    // Excerpt generator
    public string function excerpt(numeric length=200) {
        if (!structKeyExists(this, "content")) return "";
        var plain = reReplace(this.content, "<[^>]*>", "", "ALL");
        return len(plain) > arguments.length
            ? left(plain, arguments.length) & "..."
            : plain;
    }

    // Status checker
    public boolean function isPublished() {
        return structKeyExists(this, "published") && this.published;
    }

    // Date formatter
    public string function formattedDate(string format="yyyy-mm-dd") {
        return dateFormat(this.createdAt, arguments.format);
    }

    // URL generator
    public string function url() {
        return "/posts/" & this.slug;
    }

    // Safe deletion check
    public boolean function canDelete() {
        // Don't allow deletion if has associated records
        return this.comments().recordCount == 0;
    }
}
```

## Implementation Checklist

When generating a model, ensure:

- [ ] Component extends="Model"
- [ ] config() function defined
- [ ] All association parameters use NAMED style (name=, dependent=)
- [ ] All validation parameters use NAMED style (property=, message=)
- [ ] Consistent parameter style throughout entire config()
- [ ] Association direction matches database relationships
- [ ] Validations match business requirements
- [ ] Custom methods have return type hints (public/private, string/boolean/numeric)
- [ ] Callback methods are private
- [ ] No mixed argument styles anywhere

## Testing Generated Models

After generating a model, validate it works:

```cfm
// Test instantiation
user = model("User").new();
// Should not throw error

// Test associations are defined
posts = user.posts();
// Should return query object

// Test validations work
user.email = "invalid";
result = user.valid();
// Should return false

errors = user.allErrors();
// Should contain email validation error

// Test custom methods
name = user.fullName();
// Should return concatenated name
```

## Common Model Patterns

### User Authentication Model

See `templates/user-authentication-model.cfc` for complete example.

### Soft Delete Model

```cfm
component extends="Model" {
    function config() {
        // Mark as deleted instead of actually deleting
        beforeDelete("softDelete");
    }

    private void function softDelete() {
        this.deletedAt = now();
        this.save();
        abort();  // Prevent actual deletion
    }

    public query function findActive() {
        return this.findAll(where="deletedAt IS NULL");
    }
}
```

### Timestamped Model

```cfm
component extends="Model" {
    function config() {
        // Wheels automatically handles createdAt and updatedAt
        // if columns exist in database
        // No configuration needed!
    }
}
```

## Related Skills

- **wheels-anti-pattern-detector**: Validates generated model code
- **wheels-migration-generator**: Creates database schema for model
- **wheels-test-generator**: Creates TestBox specs for model
- **wheels-controller-generator**: Creates controller for model

## Quick Reference

### Association Options
- `name` - Association name (required when using named params)
- `dependent` - What to do with associated records: "delete", "deleteAll", "remove", "removeAll"
- `foreignKey` - Custom foreign key column name
- `joinKey` - Custom join key for hasManyThrough
- `modelName` - Override associated model name
- `through` - Join model for hasManyThrough

### Validation Options
- `property` - Property name(s) to validate (required)
- `message` - Custom error message
- `when` - When to run validation: "onCreate", "onUpdate"
- `condition` - Method name that returns boolean
- `allowBlank` - Allow empty string (default false)

### Callback Options
- `method` - Method name to call (or array of method names)

---

**Generated by:** Wheels Model Generator Skill v1.0
**Framework:** CFWheels 3.0+
**Last Updated:** 2025-10-20

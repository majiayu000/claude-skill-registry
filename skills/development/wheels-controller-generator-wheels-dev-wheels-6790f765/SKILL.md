---
name: Wheels Controller Generator
description: Generate Wheels MVC controllers with CRUD actions, filters, parameter verification, and proper rendering. Use when creating or modifying controllers, adding actions, implementing filters for authentication/authorization, handling form submissions, or rendering views/JSON. Ensures proper Wheels conventions and prevents common controller errors.
---

# Wheels Controller Generator

## When to Use This Skill

Activate automatically when:
- User requests to create a new controller (e.g., "create a Users controller")
- User wants to add CRUD actions (index, show, new, create, edit, update, delete)
- User needs filters (beforeAction/afterAction)
- User wants authentication or authorization
- User is implementing API endpoints
- User mentions: controller, action, filter, CRUD, API, JSON, render, redirect

## Critical Patterns

### ✅ CORRECT Controller Structure

```cfm
component extends="Controller" {

    function config() {
        // Parameter verification
        verifies(only="show,edit,update,delete", params="key", paramsTypes="integer");

        // Filters
        filters(through="findResource", only="show,edit,update,delete");
        filters(through="requireAuth", except="index,show");
    }

    // Public action methods
    function index() {
        resources = model("Resource").findAll(order="createdAt DESC");
    }

    // Private filter methods
    private function findResource() {
        resource = model("Resource").findByKey(key=params.key);
        if (!isObject(resource)) {
            flashInsert(error="Resource not found");
            redirectTo(action="index");
        }
    }
}
```

### ❌ ANTI-PATTERNS to Avoid

**Don't mix argument styles:**
```cfm
// ❌ WRONG
resource = model("Resource").findByKey(params.key, include="comments");

// ✅ CORRECT
resource = model("Resource").findByKey(key=params.key, include="comments");
```

**Don't forget parameter verification:**
```cfm
// ❌ WRONG - No verification, vulnerable to injection
function show() {
    post = model("Post").findByKey(key=params.key);
}

// ✅ CORRECT - Verify params before use
function config() {
    verifies(only="show", params="key", paramsTypes="integer");
}
```

**Don't forget CSRF protection in forms:**
```cfm
// ❌ WRONG - Forms without CSRF
#startFormTag(action="create")#

// ✅ CORRECT - CSRF token included by default
#startFormTag(action="create")#  // Wheels adds CSRF automatically
```

## CRUD Controller Template

### Complete CRUD Implementation

```cfm
component extends="Controller" {

    function config() {
        // Verify key parameter is integer
        verifies(only="show,edit,update,delete", params="key", paramsTypes="integer");

        // Load resource for actions that need it
        filters(through="findResource", only="show,edit,update,delete");
    }

    /**
     * List all resources
     */
    function index() {
        resources = model("Resource").findAll(
            order="createdAt DESC",
            include="associations",  // Prevent N+1 queries
            page=params.page
        );
    }

    /**
     * Show single resource
     */
    function show() {
        // Resource loaded by filter
        // Load associated data
        associations = resource.associations(order="createdAt ASC");
    }

    /**
     * New resource form
     */
    function new() {
        resource = model("Resource").new();
    }

    /**
     * Create new resource
     */
    function create() {
        resource = model("Resource").new(params.resource);

        if (resource.save()) {
            flashInsert(success="Resource created successfully!");
            redirectTo(action="show", key=resource.key());
        } else {
            flashInsert(error="Please correct the errors below.");
            renderPage(action="new");
        }
    }

    /**
     * Edit resource form
     */
    function edit() {
        // Resource loaded by filter
    }

    /**
     * Update resource
     */
    function update() {
        // Resource loaded by filter

        if (resource.update(params.resource)) {
            flashInsert(success="Resource updated successfully!");
            redirectTo(action="show", key=resource.key());
        } else {
            flashInsert(error="Please correct the errors below.");
            renderPage(action="edit");
        }
    }

    /**
     * Delete resource
     */
    function delete() {
        // Resource loaded by filter

        if (resource.delete()) {
            flashInsert(success="Resource deleted successfully!");
            redirectTo(action="index");
        } else {
            flashInsert(error="Unable to delete resource.");
            redirectTo(action="show", key=resource.key());
        }
    }

    /**
     * Private filter to load resource
     */
    private function findResource() {
        resource = model("Resource").findByKey(key=params.key);

        if (!isObject(resource)) {
            flashInsert(error="Resource not found.");
            redirectTo(action="index");
        }
    }
}
```

## Filter Patterns

### Authentication Filter

```cfm
component extends="Controller" {

    function config() {
        // Require authentication for all actions except index and show
        filters(through="requireAuth", except="index,show");
    }

    private function requireAuth() {
        if (!structKeyExists(session, "userId")) {
            flashInsert(error="Please log in to continue.");
            redirectTo(controller="sessions", action="new");
        }
    }
}
```

### Authorization Filter

```cfm
component extends="Controller" {

    function config() {
        filters(through="requireAuth");
        filters(through="requireOwnership", only="edit,update,delete");
    }

    private function requireAuth() {
        if (!structKeyExists(session, "userId")) {
            flashInsert(error="Please log in.");
            redirectTo(controller="sessions", action="new");
        }
    }

    private function requireOwnership() {
        resource = model("Resource").findByKey(key=params.key);

        if (!isObject(resource) || resource.userId != session.userId) {
            flashInsert(error="You don't have permission to access this resource.");
            redirectTo(action="index");
        }
    }
}
```

### Data Loading Filter

```cfm
component extends="Controller" {

    function config() {
        // Load current user for all actions
        filters(through="loadCurrentUser");
    }

    private function loadCurrentUser() {
        if (structKeyExists(session, "userId")) {
            currentUser = model("User").findByKey(key=session.userId);
        }
    }
}
```

## Rendering Patterns

### Render View

```cfm
function index() {
    resources = model("Resource").findAll();
    // Automatically renders views/resources/index.cfm
}
```

### Render Specific View

```cfm
function create() {
    resource = model("Resource").new(params.resource);

    if (!resource.save()) {
        // Render the new action's view
        renderPage(action="new");
    }
}
```

### Render JSON (API)

```cfm
function index() {
    resources = model("Resource").findAll();

    renderWith(
        data=resources,
        format="json",
        status=200
    );
}
```

### Render Partial

```cfm
function loadMore() {
    resources = model("Resource").findAll(page=params.page);
    renderPartial(partial="resource", collection=resources);
}
```

### Send File

```cfm
function download() {
    resource = model("Resource").findByKey(key=params.key);

    sendFile(
        file=resource.filePath,
        name=resource.fileName,
        disposition="attachment"
    );
}
```

## Redirect Patterns

### Redirect to Action

```cfm
function create() {
    resource = model("Resource").new(params.resource);

    if (resource.save()) {
        redirectTo(action="show", key=resource.key());
    }
}
```

### Redirect to Controller/Action

```cfm
function logout() {
    structDelete(session, "userId");
    redirectTo(controller="home", action="index");
}
```

### Redirect to URL

```cfm
function external() {
    redirectTo(url="https://wheels.dev");
}
```

### Redirect Back

```cfm
function cancel() {
    redirectTo(back=true, default="index");
}
```

## Flash Message Patterns

### Success Messages

```cfm
flashInsert(success="Operation completed successfully!");
```

### Error Messages

```cfm
flashInsert(error="An error occurred. Please try again.");
```

### Multiple Message Types

```cfm
flashInsert(
    success="Resource created!",
    notice="Check your email for confirmation."
);
```

### Flash Keep (preserve across redirect chain)

```cfm
flashKeep("success");
redirectTo(action="intermediate");
```

## Parameter Handling

### Parameter Verification

```cfm
function config() {
    // Verify key is integer
    verifies(only="show", params="key", paramsTypes="integer");

    // Verify multiple params
    verifies(only="create", params="name,email", paramsTypes="string,string");

    // Verify with default values
    verifies(params="page", default=1, paramsTypes="integer");
}
```

### Safe Parameter Access

```cfm
function index() {
    // Use params with defaults
    page = structKeyExists(params, "page") ? params.page : 1;

    // Or let Wheels handle it with verifies()
    resources = model("Resource").findAll(page=params.page);
}
```

### Nested Parameters (Forms)

```cfm
function create() {
    // Form submits: user[name], user[email], user[password]
    // Wheels creates: params.user = {name="", email="", password=""}

    user = model("User").new(params.user);
}
```

## API Controller Patterns

### JSON API Controller

```cfm
component extends="Controller" {

    function config() {
        // Set default rendering to JSON
        provides("json");

        // Verify API authentication
        filters(through="requireApiAuth");
    }

    function index() {
        resources = model("Resource").findAll();

        renderWith(
            data=resources,
            format="json",
            status=200
        );
    }

    function show() {
        resource = model("Resource").findByKey(key=params.key);

        if (!isObject(resource)) {
            renderWith(
                data={error="Resource not found"},
                format="json",
                status=404
            );
            return;
        }

        renderWith(
            data=resource,
            format="json",
            status=200
        );
    }

    function create() {
        resource = model("Resource").new(params.resource);

        if (resource.save()) {
            renderWith(
                data=resource,
                format="json",
                status=201,
                location=urlFor(action="show", key=resource.key())
            );
        } else {
            renderWith(
                data={errors=resource.allErrors()},
                format="json",
                status=422
            );
        }
    }

    private function requireApiAuth() {
        var authHeader = getHTTPRequestData().headers["Authorization"];

        if (!structKeyExists(local, "authHeader") || !isValidToken(authHeader)) {
            renderWith(
                data={error="Unauthorized"},
                format="json",
                status=401
            );
            abort;
        }
    }
}
```

## Nested Resource Controllers

### Nested Resource Pattern

```cfm
// URL: /posts/5/comments
component extends="Controller" {

    function config() {
        verifies(params="postId", paramsTypes="integer");
        filters(through="loadPost");
    }

    function index() {
        // Post loaded by filter
        comments = post.comments(order="createdAt DESC");
    }

    function create() {
        comment = model("Comment").new(params.comment);
        comment.postId = params.postId;

        if (comment.save()) {
            flashInsert(success="Comment added!");
            redirectTo(controller="posts", action="show", key=params.postId);
        }
    }

    private function loadPost() {
        post = model("Post").findByKey(key=params.postId);

        if (!isObject(post)) {
            flashInsert(error="Post not found.");
            redirectTo(controller="posts", action="index");
        }
    }
}
```

## Implementation Checklist

When generating a controller:

- [ ] Component extends="Controller"
- [ ] config() function defined
- [ ] Parameter verification configured with verifies()
- [ ] Filters defined as private functions
- [ ] All model calls use named parameters
- [ ] Flash messages for user feedback
- [ ] Proper redirects after POST/PUT/DELETE
- [ ] Error handling for not found resources
- [ ] CRUD actions follow conventions
- [ ] Public action methods, private filter methods

## Testing Controllers

```cfm
// Test controller instantiation
controller = controller("Resources");

// Test action execution
controller.processAction("index");

// Test filter execution
controller.processAction("show", {key=1});

// Check variables set by action
expect(controller.resources).toBeQuery();
```

## Related Skills

- **wheels-anti-pattern-detector**: Validates controller code
- **wheels-view-generator**: Creates views for controller actions
- **wheels-test-generator**: Creates controller specs
- **wheels-model-generator**: Creates models used by controller

## Quick Reference

### Common Controller Methods
- `renderPage()` - Render specific view
- `renderPartial()` - Render partial
- `renderWith()` - Render with format (JSON/XML)
- `redirectTo()` - Redirect to action/URL
- `flashInsert()` - Add flash message
- `sendFile()` - Send file download
- `provides()` - Set default formats
- `abort()` - Stop execution

### Parameter Verification Types
- `integer`, `string`, `boolean`, `numeric`, `date`, `time`, `email`, `url`

### Flash Message Types
- `success`, `error`, `warning`, `info`, `notice`

---

**Generated by:** Wheels Controller Generator Skill v1.0
**Framework:** CFWheels 3.0+
**Last Updated:** 2025-10-20

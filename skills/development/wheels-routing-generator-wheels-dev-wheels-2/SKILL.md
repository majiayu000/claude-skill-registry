---
name: Wheels Routing Generator
description: Generate RESTful routes, nested routes, and custom routing patterns for Wheels applications. Use when defining URL structure, creating RESTful resources, or implementing custom route patterns. Ensures proper HTTP verb mapping and route constraints.
---

# Wheels Routing Generator

## When to Use This Skill

Activate automatically when:
- User wants to create routes
- User mentions: routes, routing, URL structure, RESTful
- User needs nested resources
- User wants custom route patterns
- User asks about URL mapping or route constraints

## Routes Configuration File

**Location:** `/config/routes.cfm`

```cfm
<cfscript>
// Basic structure
mapper()
    // Your routes here
.end();
</cfscript>
```

## Basic Route Patterns

### Simple Routes

```cfm
<cfscript>
mapper()
    // GET request to /about -> Pages.about()
    .get(name="about", pattern="about", to="pages##about")

    // POST request to /contact -> Pages.contact()
    .post(name="contact", pattern="contact", to="pages##contact")

    // Multiple HTTP verbs
    .match(name="search", pattern="search", to="posts##search", methods="GET,POST")

    // Route with parameter
    .get(name="post", pattern="posts/[key]", to="posts##show")

    // Root route (home page)
    .root(to="pages##index")
.end();
</cfscript>
```

### RESTful Resources

```cfm
<cfscript>
mapper()
    // Complete RESTful resource
    // Creates 7 routes: index, new, create, show, edit, update, delete
    .resources("posts")

    // Limit to specific actions
    .resources(name="comments", only="index,show")
    .resources(name="photos", except="delete")
.end();
</cfscript>
```

**Generated Routes for `.resources("posts")`:**

| HTTP Verb | Path              | Action  | Purpose              |
|-----------|-------------------|---------|----------------------|
| GET       | /posts            | index   | List all posts       |
| GET       | /posts/new        | new     | Show create form     |
| POST      | /posts            | create  | Create new post      |
| GET       | /posts/[key]      | show    | Show single post     |
| GET       | /posts/[key]/edit | edit    | Show edit form       |
| PATCH/PUT | /posts/[key]      | update  | Update post          |
| DELETE    | /posts/[key]      | delete  | Delete post          |

## Nested Resources

### Parent-Child Resources

```cfm
<cfscript>
mapper()
    // Posts with nested comments
    .resources("posts")
    .resources(name="comments", nested=true)

    // /posts/1/comments - shows comments for post 1
    // /posts/1/comments/2 - shows comment 2 for post 1
.end();
</cfscript>
```

### Multiple Level Nesting

```cfm
<cfscript>
mapper()
    // Blog -> Post -> Comments
    .resources("blogs")
    .resources(name="posts", nested=true)
    .resources(name="comments", nested=true)

    // /blogs/1/posts/2/comments/3
.end();
</cfscript>
```

### Shallow Nesting (Recommended)

```cfm
<cfscript>
mapper()
    // Nested for creation only
    .resources("posts")
    .resources(name="comments", nested=true, only="new,create")

    // Standalone for viewing/editing
    .resources("comments", except="new,create")

    // Result:
    // POST /posts/1/comments (create with parent context)
    // GET /comments/1 (view without deep nesting)
    // PATCH /comments/1 (update without deep nesting)
.end();
</cfscript>
```

## Custom Route Patterns

### Named Routes with Parameters

```cfm
<cfscript>
mapper()
    // Single parameter
    .get(name="userProfile", pattern="users/[username]", to="users##show")

    // Multiple parameters
    .get(
        name="blogPost",
        pattern="[year]/[month]/[slug]",
        to="posts##show"
    )

    // Optional parameters
    .get(
        name="search",
        pattern="search/[[category]]/[[tag]]",
        to="search##index"
    )
.end();
</cfscript>
```

### Wildcard Routes

```cfm
<cfscript>
mapper()
    // Catch-all pattern (use sparingly!)
    .get(
        name="pages",
        pattern="pages/[*path]",
        to="pages##show"
    )
    // Matches: /pages/about, /pages/help/faq, etc.
.end();
</cfscript>
```

### Route Constraints

```cfm
<cfscript>
mapper()
    // Numeric constraint
    .get(
        name="post",
        pattern="posts/[key]",
        to="posts##show",
        constraints={key="[0-9]+"}
    )

    // Alpha constraint
    .get(
        name="tag",
        pattern="tags/[slug]",
        to="tags##show",
        constraints={slug="[a-z-]+"}
    )

    // Date constraint
    .get(
        name="archive",
        pattern="[year]/[month]",
        to="posts##archive",
        constraints={
            year="[0-9]{4}",
            month="[0-9]{2}"
        }
    )
.end();
</cfscript>
```

## Namespace and Scoped Routes

### Controller Namespace

```cfm
<cfscript>
mapper()
    // Admin section
    .namespace("admin")
        .resources("users")
        .resources("posts")
        .resources("settings")
    .endNamespace()

    // Maps to:
    // /admin/users -> admin.Users.index()
    // /admin/posts/1 -> admin.Posts.show(key=1)
.end();
</cfscript>
```

### Path Scoping

```cfm
<cfscript>
mapper()
    // Scope multiple routes under a path
    .scope(path="api/v1", module="api.v1")
        .resources("posts")
        .resources("comments")
    .endScope()

    // Maps to:
    // /api/v1/posts -> api.v1.Posts.index()
    // /api/v1/comments -> api.v1.Comments.index()
.end();
</cfscript>
```

## API Versioning Routes

```cfm
<cfscript>
mapper()
    // API v1
    .scope(path="api/v1", module="api.v1")
        .resources("posts")
        .resources("users")
    .endScope()

    // API v2
    .scope(path="api/v2", module="api.v2")
        .resources("posts")
        .resources("users")
    .endScope()

    // Latest (redirects to current version)
    .get(name="apiLatest", pattern="api/[*path]", to="api##redirectToLatest")
.end();
</cfscript>
```

## RESTful Member and Collection Routes

### Member Routes (Single Resource)

```cfm
<cfscript>
mapper()
    .resources("posts")
        // Custom actions on single post
        .member(name="publish", to="posts##publish", method="patch")
        .member(name="archive", to="posts##archive", method="post")
    .endResources()

    // Maps to:
    // PATCH /posts/1/publish
    // POST /posts/1/archive
.end();
</cfscript>
```

### Collection Routes (All Resources)

```cfm
<cfscript>
mapper()
    .resources("posts")
        // Custom actions on collection
        .collection(name="search", to="posts##search", method="get")
        .collection(name="export", to="posts##export", method="get")
    .endResources()

    // Maps to:
    // GET /posts/search
    // GET /posts/export
.end();
</cfscript>
```

## Route Helpers in Controllers

### Generating URLs

```cfm
// In controllers/views
urlFor(route="post", key=1)
// -> /posts/1

urlFor(route="editPost", key=1)
// -> /posts/1/edit

urlFor(route="posts")
// -> /posts

// With query parameters
urlFor(route="posts", params={tag="rails", page=2})
// -> /posts?tag=rails&page=2

// Absolute URLs
urlFor(route="post", key=1, onlyPath=false)
// -> http://yoursite.com/posts/1
```

### Redirecting

```cfm
// Redirect to named route
redirectTo(route="posts")
redirectTo(route="post", key=1)

// Redirect with flash
redirectTo(route="posts", success="Post created!")
```

### Link Helpers in Views

```cfm
// Link to route
#linkTo(route="posts", text="All Posts")#

// Link with parameters
#linkTo(route="post", key=postId, text=post.title)#

// Link with HTML attributes
#linkTo(route="post", key=1, text="Read More", class="btn btn-primary")#
```

## Form Routes

```cfm
<cfoutput>
    <!-- Create form -->
    #startFormTag(route="posts", method="post")#
        <!-- form fields -->
    #endFormTag()#

    <!-- Update form -->
    #startFormTag(route="post", key=post.id, method="patch")#
        <!-- form fields -->
    #endFormTag()#

    <!-- Delete link -->
    #linkTo(
        route="post",
        key=post.id,
        method="delete",
        text="Delete",
        confirm="Are you sure?"
    )#
</cfoutput>
```

## Advanced Routing Patterns

### Subdomain Routes

```cfm
<cfscript>
mapper()
    // Admin subdomain
    .scope(subdomain="admin")
        .resources("users")
        .resources("settings")
    .endScope()

    // API subdomain
    .scope(subdomain="api")
        .resources("posts")
    .endScope()

    // Wildcard subdomain
    .scope(subdomain="[account]")
        .root(to="accounts##dashboard")
        .resources("projects")
    .endScope()
.end();
</cfscript>
```

### Redirect Routes

```cfm
<cfscript>
mapper()
    // Permanent redirect
    .redirect(from="old-blog", to="posts", statusCode=301)

    // Redirect to external URL
    .redirect(
        from="docs",
        to="https://docs.yoursite.com",
        statusCode=302
    )
.end();
</cfscript>
```

### Route Concerns (Reusable Route Sets)

```cfm
<cfscript>
mapper()
    // Define concern
    .concern(name="commentable")
        .resources(name="comments", nested=true)
    .endConcern()

    // Use concern
    .resources("posts")
        .concerns("commentable")
    .endResources()

    .resources("photos")
        .concerns("commentable")
    .endResources()

    // Both posts and photos now have comments routes
.end();
</cfscript>
```

## Testing Routes

### View All Routes

```cfm
// Create a test action
function testRoutes() {
    routes = application.wheels.routes;
    writeDump(routes);
    abort;
}
```

### Check Route Mapping

```cfm
// Test if route exists
if (structKeyExists(application.wheels.namedRoutes, "post")) {
    // Route exists
}

// Get route pattern
pattern = application.wheels.namedRoutes.post.pattern;
```

## Route Best Practices

### ✅ DO:
- Use RESTful conventions (resources)
- Keep nesting shallow (max 2 levels)
- Use named routes for flexibility
- Add route constraints for validation
- Group related routes with scopes
- Use proper HTTP verbs
- Follow REST conventions consistently

### ❌ DON'T:
- Over-nest resources (avoid `/a/b/c/d/e`)
- Use catch-all routes carelessly
- Hardcode URLs in code (use urlFor)
- Mix REST and non-REST patterns
- Create ambiguous routes
- Forget route constraints on IDs
- Use GET for destructive actions

## Common Route Patterns

### Blog Application

```cfm
<cfscript>
mapper()
    .root(to="posts##index")

    // Public routes
    .get(name="about", pattern="about", to="pages##about")
    .get(name="contact", pattern="contact", to="pages##contact")
    .post(name="contactSubmit", pattern="contact", to="pages##sendContact")

    // Blog routes
    .resources("posts", only="index,show")
    .get(name="archive", pattern="archive/[year]/[month]", to="posts##archive")
    .get(name="tag", pattern="tags/[slug]", to="posts##byTag")

    // Admin section
    .namespace("admin")
        .resources("posts")
        .resources("comments")
        .resources("tags")
    .endNamespace()

    // Authentication
    .get(name="login", pattern="login", to="sessions##new")
    .post(name="sessionCreate", pattern="login", to="sessions##create")
    .delete(name="logout", pattern="logout", to="sessions##delete")
.end();
</cfscript>
```

### E-commerce Application

```cfm
<cfscript>
mapper()
    .root(to="products##index")

    // Products
    .resources("products", only="index,show")
    .get(name="category", pattern="categories/[slug]", to="products##category")

    // Shopping cart
    .get(name="cart", pattern="cart", to="cart##show")
    .post(name="addToCart", pattern="cart/add", to="cart##add")
    .delete(name="removeFromCart", pattern="cart/remove/[key]", to="cart##remove")

    // Checkout
    .get(name="checkout", pattern="checkout", to="checkout##index")
    .post(name="processCheckout", pattern="checkout", to="checkout##process")

    // User account
    .get(name="account", pattern="account", to="users##show")
    .resources("orders", only="index,show")

    // Admin
    .namespace("admin")
        .resources("products")
        .resources("orders")
        .resources("customers")
    .endNamespace()
.end();
</cfscript>
```

### API Routes

```cfm
<cfscript>
mapper()
    // API v1
    .scope(path="api/v1", module="api.v1")
        // Resources with token auth
        .resources("posts")
        .resources("comments")
        .resources("users", except="new,edit")

        // Custom endpoints
        .post(name="apiLogin", pattern="auth/login", to="auth##login")
        .post(name="apiLogout", pattern="auth/logout", to="auth##logout")
        .get(name="apiProfile", pattern="me", to="users##profile")
    .endScope()
.end();
</cfscript>
```

## Debugging Routes

### List All Routes

Add to a controller:

```cfm
function listRoutes() {
    routes = [];

    for (local.key in application.wheels.namedRoutes) {
        local.route = application.wheels.namedRoutes[local.key];
        arrayAppend(routes, {
            name = local.key,
            pattern = local.route.pattern,
            controller = local.route.controller,
            action = local.route.action,
            methods = local.route.methods
        });
    }

    writeDump(routes);
    abort;
}
```

### Test Route Generation

```cfm
// Test in view/controller
<cfdump var="##urlFor(route='post', key=1)##">
<cfdump var="##urlFor(route='posts')##">
```

## Related Skills

- **wheels-controller-generator**: Create controllers for routes
- **wheels-api-generator**: Create API routes
- **wheels-view-generator**: Create views for routes
- **wheels-test-generator**: Test routing

---

**Generated by:** Wheels Routing Generator Skill v1.0

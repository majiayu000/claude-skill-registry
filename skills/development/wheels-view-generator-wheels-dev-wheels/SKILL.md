---
name: Wheels View Generator
description: Generate Wheels view templates with proper query handling, form helpers, and association display. Use when creating or modifying views, forms, layouts, or partials. Prevents common view errors like query/array confusion and incorrect form helper usage. Handles index views, show views, form views, and layouts with proper CFML syntax.
---

# Wheels View Generator

## When to Use This Skill

Activate automatically when:
- User requests to create a view (e.g., "create an index view for posts")
- User wants to create forms
- User needs to display associated data
- User is creating layouts or partials
- User mentions: view, template, form, layout, partial, display, list, show

## Critical Anti-Patterns to Prevent

### ❌ ANTI-PATTERN 1: Query/Array Confusion

**Wheels associations return QUERIES, not arrays!**

**WRONG:**
```cfm
<cfset count = ArrayLen(post.comments())>  ❌
<cfloop array="#comments#" index="comment">  ❌
```

**CORRECT:**
```cfm
<cfset count = post.comments().recordCount>  ✅
<cfloop query="comments">  ✅
```

### ❌ ANTI-PATTERN 2: Association Access Inside Query Loops

**WRONG:**
```cfm
<cfloop query="posts">
    <p>#posts.comments().recordCount# comments</p>  ❌ Fails!
</cfloop>
```

**CORRECT:**
```cfm
<cfloop query="posts">
    <cfset postComments = model("Post").findByKey(posts.id).comments()>
    <p>#postComments.recordCount# comments</p>  ✅ Works!
</cfloop>
```

### ❌ ANTI-PATTERN 3: Non-Existent Form Helpers

**Wheels doesn't have these helpers:**
```cfm
#emailField(...)#  ❌ Doesn't exist
#passwordField(...)#  ❌ Doesn't exist
#numberField(...)#  ❌ Doesn't exist
```

**Use textField() with type attribute:**
```cfm
#textField(objectName="user", property="email", type="email")#  ✅
#textField(objectName="user", property="password", type="password")#  ✅
#textField(objectName="user", property="age", type="number")#  ✅
```

## 🚨 Production-Tested Best Practices

### 1. Association Access in Query Loops (CRITICAL)

**❌ WRONG - Associations Don't Work on Query Columns:**
```cfm
<cfloop query="tweets">
    #tweets.user()#  ❌ FAILS - tweets is a query, not an object
    #tweets.likesCount()#  ❌ FAILS - no such method on query
</cfloop>
```

**✅ CORRECT - Load Object First:**
```cfm
<cfloop query="tweets">
    <cfset tweetObj = model("Tweet").findByKey(tweets.id)>
    <cfset tweetUser = tweetObj.user()>  ✅ Works!
    <p>By: #tweetUser.username#</p>
    <p>Likes: #tweetObj.likesCount#</p>
</cfloop>
```

**✅ BETTER - Preload with include (Prevents N+1):**
```cfm
<!--- In Controller --->
tweets = model("Tweet").findAll(include="user", order="createdAt DESC");

<!--- In View --->
<cfloop query="tweets">
    <!--- User data already joined, no extra queries --->
    <p>By: #tweets.username#</p>
    <p>Tweet: #tweets.content#</p>
</cfloop>
```

### 2. Checking if Query Has Records

```cfm
<!--- ✅ CORRECT --->
<cfif tweets.recordCount>
    <cfloop query="tweets">...</cfloop>
</cfif>

<!--- ❌ WRONG - queries are not arrays --->
<cfif ArrayLen(tweets)>  ❌ Error!
```

### 3. Counter Access Patterns

**Direct column access (if eager loaded):**
```cfm
tweets = model("Tweet").findAll(select="id,content,likesCount");
<cfloop query="tweets">
    <p>#tweets.likesCount# likes</p>  ✅ Direct access
</cfloop>
```

**Association count (if not loaded):**
```cfm
<cfloop query="tweets">
    <cfset tweet = model("Tweet").findByKey(tweets.id)>
    <cfset likeCount = tweet.likes(returnAs="count")>  ✅ Count association
    <p>#likeCount# likes</p>
</cfloop>
```

### 4. Boolean Checks in Views

```cfm
<!--- ✅ CORRECT --->
<cfif user.active>
<cfif structKeyExists(user, "bio") && len(user.bio)>

<!--- ❌ WRONG --->
<cfif user.active == true>  // Redundant
<cfif user.bio>  // Fails if bio doesn't exist
```

### 5. Date Formatting

```cfm
<!--- ✅ CORRECT - Use CFML functions --->
#dateFormat(tweet.createdAt, "mmm dd, yyyy")#
#timeFormat(tweet.createdAt, "h:mm tt")#

<!--- Use custom model methods for consistency --->
#tweet.timeAgo()#  // "5m", "2h", "3d"
```

### 6. Loop Query vs Loop Array

```cfm
<!--- ✅ CORRECT - Wheels returns queries --->
<cfloop query="tweets">
    #tweets.content#
</cfloop>

<!--- ❌ WRONG - Not an array! --->
<cfloop array="#tweets#" index="tweet">  ❌ Error!
```

## Index View Template (List View)

```cfm
<cfparam name="resources">
<cfoutput>

#contentFor(pageTitle="Resources")#

<div class="container">
    <div class="header">
        <h1>Resources</h1>
        <div class="actions">
            #linkTo(text="New Resource", action="new", class="btn btn-primary")#
        </div>
    </div>

    <cfif resources.recordCount>
        <div class="resource-grid">
            <cfloop query="resources">
                <article class="resource-card">
                    <h2>
                        #linkTo(text=resources.title, action="show", key=resources.id)#
                    </h2>

                    <!--- Display excerpt or description --->
                    <p>#left(resources.description, 200)#...</p>

                    <!--- Display associated data (CORRECT pattern) --->
                    <cfset resourceAssoc = model("Resource").findByKey(resources.id).association()>
                    <div class="meta">
                        <span>#resourceAssoc.recordCount# items</span>
                        <span>#dateFormat(resources.createdAt, "mmm dd, yyyy")#</span>
                    </div>

                    <div class="actions">
                        #linkTo(text="View", action="show", key=resources.id, class="btn btn-sm")#
                        #linkTo(text="Edit", action="edit", key=resources.id, class="btn btn-sm")#
                    </div>
                </article>
            </cfloop>
        </div>

        <!--- Pagination if needed --->
        #paginationLinks(prependToLink="page=")#
    <cfelse>
        <div class="empty-state">
            <p>No resources found.</p>
            #linkTo(text="Create First Resource", action="new", class="btn btn-primary")#
        </div>
    </cfif>
</div>

</cfoutput>
```

## Show View Template (Detail View)

```cfm
<cfparam name="resource">
<cfparam name="associations">
<cfoutput>

#contentFor(pageTitle=resource.title)#

<div class="container">
    <div class="header">
        <h1>#resource.title#</h1>
        <div class="actions">
            #linkTo(text="Edit", action="edit", key=resource.id, class="btn")#
            #linkTo(
                text="Delete",
                action="delete",
                key=resource.id,
                method="delete",
                confirm="Are you sure?",
                class="btn btn-danger"
            )#
            #linkTo(text="Back to List", action="index", class="btn")#
        </div>
    </div>

    <div class="resource-content">
        <!--- Display full content --->
        <div class="description">
            #resource.description#
        </div>

        <!--- Display metadata --->
        <div class="metadata">
            <p>
                <strong>Created:</strong>
                #dateFormat(resource.createdAt, "mmmm dd, yyyy")#
                at #timeFormat(resource.createdAt, "h:mm tt")#
            </p>
            <cfif structKeyExists(resource, "updatedAt")>
                <p>
                    <strong>Last Updated:</strong>
                    #dateFormat(resource.updatedAt, "mmmm dd, yyyy")#
                </p>
            </cfif>
        </div>
    </div>

    <!--- Display associated records --->
    <div class="associations-section">
        <h2>Associated Items (#associations.recordCount#)</h2>

        <cfif associations.recordCount>
            <ul class="associations-list">
                <cfloop query="associations">
                    <li>
                        #associations.name#
                        <small>#dateFormat(associations.createdAt, "mmm dd")#</small>
                    </li>
                </cfloop>
            </ul>
        <cfelse>
            <p>No associated items.</p>
        </cfif>
    </div>
</div>

</cfoutput>
```

## Form View Template (New/Edit)

```cfm
<cfparam name="resource">
<cfoutput>

#contentFor(pageTitle=resource.isNew() ? "New Resource" : "Edit Resource")#

<div class="container">
    <h1>#resource.isNew() ? "Create" : "Edit"# Resource</h1>

    <!--- Display form errors if any --->
    <cfif resource.hasErrors()>
        <div class="alert alert-error">
            <p><strong>Please correct the following errors:</strong></p>
            <ul>
                <cfloop collection="#resource.allErrors()#" item="propertyName">
                    <cfloop array="#resource.allErrors(propertyName)#" index="errorMessage">
                        <li>#errorMessage#</li>
                    </cfloop>
                </cfloop>
            </ul>
        </div>
    </cfif>

    #startFormTag(action=resource.isNew() ? "create" : "update", method=resource.isNew() ? "post" : "patch")#

        <!--- Text input with error display --->
        <div class="form-group #resource.hasErrors('title') ? 'has-error' : ''#">
            <label for="resource-title">Title *</label>
            #textField(objectName="resource", property="title", label=false, class="form-control")#
            <cfif resource.hasErrors("title")>
                <span class="error-message">#resource.allErrors("title")[1]#</span>
            </cfif>
        </div>

        <!--- Textarea with error display --->
        <div class="form-group #resource.hasErrors('description') ? 'has-error' : ''#">
            <label for="resource-description">Description</label>
            #textArea(objectName="resource", property="description", label=false, rows=6, class="form-control")#
            <cfif resource.hasErrors("description")>
                <span class="error-message">#resource.allErrors("description")[1]#</span>
            </cfif>
        </div>

        <!--- Email field (use textField with type) --->
        <div class="form-group #resource.hasErrors('email') ? 'has-error' : ''#">
            <label for="resource-email">Email *</label>
            #textField(objectName="resource", property="email", type="email", label=false, class="form-control")#
            <cfif resource.hasErrors("email")>
                <span class="error-message">#resource.allErrors("email")[1]#</span>
            </cfif>
        </div>

        <!--- Number field --->
        <div class="form-group">
            <label for="resource-price">Price</label>
            #textField(objectName="resource", property="price", type="number", step="0.01", label=false, class="form-control")#
        </div>

        <!--- Date field --->
        <div class="form-group">
            <label for="resource-publishedDate">Published Date</label>
            #dateSelect(objectName="resource", property="publishedDate", label=false, class="form-control")#
        </div>

        <!--- Select dropdown --->
        <div class="form-group">
            <label for="resource-status">Status</label>
            #select(
                objectName="resource",
                property="status",
                options="draft,published,archived",
                label=false,
                class="form-control"
            )#
        </div>

        <!--- Checkbox --->
        <div class="form-group">
            <label class="checkbox">
                #checkBox(objectName="resource", property="active", label=false)#
                <span>Active</span>
            </label>
        </div>

        <!--- Association select (belongs to) --->
        <div class="form-group">
            <label for="resource-categoryId">Category</label>
            #select(
                objectName="resource",
                property="categoryId",
                options=model("Category").findAll(),
                valueField="id",
                textField="name",
                includeBlank="-- Select Category --",
                label=false,
                class="form-control"
            )#
        </div>

        <!--- Form actions --->
        <div class="form-actions">
            #submitTag(value=resource.isNew() ? "Create Resource" : "Update Resource", class="btn btn-primary")#
            #linkTo(text="Cancel", action="index", class="btn")#
        </div>

    #endFormTag()#
</div>

</cfoutput>
```

## Layout Template

```cfm
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>#contentFor("pageTitle")# - My App</title>

    <!--- CSS --->
    #styleSheetLinkTag("application")#

    <!--- CSRF meta tags --->
    #csrfMetaTags()#
</head>
<body>
    <!--- Navigation --->
    <nav class="navbar">
        <div class="container">
            #linkTo(text="Home", controller="home", action="index", class="logo")#
            <ul class="nav-menu">
                <li>#linkTo(text="Resources", controller="resources", action="index")#</li>
                <cfif structKeyExists(session, "userId")>
                    <li>#linkTo(text="Profile", controller="users", action="show", key=session.userId)#</li>
                    <li>#linkTo(text="Logout", controller="sessions", action="delete", method="delete")#</li>
                <cfelse>
                    <li>#linkTo(text="Login", controller="sessions", action="new")#</li>
                    <li>#linkTo(text="Sign Up", controller="users", action="new")#</li>
                </cfif>
            </ul>
        </div>
    </nav>

    <!--- Flash messages --->
    <cfif flashKeyExists("success")>
        <div class="alert alert-success">
            #flash("success")#
        </div>
    </cfif>
    <cfif flashKeyExists("error")>
        <div class="alert alert-error">
            #flash("error")#
        </div>
    </cfif>
    <cfif flashKeyExists("notice")>
        <div class="alert alert-notice">
            #flash("notice")#
        </div>
    </cfif>

    <!--- Main content --->
    <main>
        #includeContent()#
    </main>

    <!--- Footer --->
    <footer>
        <div class="container">
            <p>&copy; #year(now())# My App. All rights reserved.</p>
        </div>
    </footer>

    <!--- JavaScript --->
    #javaScriptIncludeTag("application")#
</body>
</html>
```

## Partial Template

```cfm
<!--- File: views/resources/_resource.cfm --->
<cfparam name="resource">
<cfoutput>
    <div class="resource-item">
        <h3>#linkTo(text=resource.title, action="show", key=resource.id)#</h3>
        <p>#resource.excerpt()#</p>
        <div class="meta">
            <span>#dateFormat(resource.createdAt, "mmm dd, yyyy")#</span>
        </div>
    </div>
</cfoutput>

<!--- Usage in parent view: --->
<!--- #includePartial(partial="resource", query=resources)# --->
```

## Form Helper Reference

### Text Inputs

```cfm
<!--- Basic text field --->
#textField(objectName="user", property="name")#

<!--- With type attribute --->
#textField(objectName="user", property="email", type="email")#
#textField(objectName="user", property="password", type="password")#
#textField(objectName="user", property="age", type="number")#
#textField(objectName="user", property="website", type="url")#

<!--- With attributes --->
#textField(
    objectName="user",
    property="name",
    class="form-control",
    placeholder="Enter your name",
    maxlength=100,
    required=true
)#
```

### Textarea

```cfm
#textArea(objectName="post", property="content", rows=10, cols=50)#
```

### Select Dropdown

```cfm
<!--- Simple options --->
#select(objectName="user", property="role", options="user,admin,moderator")#

<!--- From query --->
#select(
    objectName="post",
    property="categoryId",
    options=model("Category").findAll(),
    valueField="id",
    textField="name",
    includeBlank="-- Select Category --"
)#
```

### Checkboxes and Radio Buttons

```cfm
<!--- Single checkbox --->
#checkBox(objectName="user", property="active")#

<!--- Radio buttons --->
#radioButton(objectName="user", property="gender", tagValue="male")# Male
#radioButton(objectName="user", property="gender", tagValue="female")# Female
```

### Date/Time Selects

```cfm
<!--- Date select --->
#dateSelect(objectName="event", property="eventDate")#

<!--- Time select --->
#timeSelect(objectName="event", property="eventTime")#

<!--- Date and time --->
#dateTimeSelect(objectName="event", property="eventDateTime")#
```

## Link Helper Reference

```cfm
<!--- Link to action in same controller --->
#linkTo(text="View", action="show", key=resource.id)#

<!--- Link to different controller --->
#linkTo(text="Home", controller="home", action="index")#

<!--- Link with method (for RESTful routes) --->
#linkTo(text="Delete", action="delete", key=resource.id, method="delete", confirm="Are you sure?")#

<!--- External link --->
#linkTo(text="Wheels Docs", href="https://wheels.dev", target="_blank")#

<!--- Link with custom attributes --->
#linkTo(text="Edit", action="edit", key=resource.id, class="btn btn-primary", data-turbo="false")#
```

## Implementation Checklist

When generating a view:

- [ ] Use `<cfparam>` to declare expected variables
- [ ] Use `<cfoutput>` blocks for dynamic content
- [ ] Use `.recordCount` for query counts (not ArrayLen)
- [ ] Use `<cfloop query="">` for query iteration
- [ ] Handle association access correctly in loops
- [ ] Use textField() with type attribute (not emailField, etc.)
- [ ] Display validation errors for each field
- [ ] Include CSRF protection in forms (automatic with startFormTag)
- [ ] Add flash message displays
- [ ] Use contentFor() to set page titles
- [ ] Provide empty state messages when no records

## Related Skills

- **wheels-anti-pattern-detector**: Validates view code
- **wheels-controller-generator**: Creates controllers that supply view data
- **wheels-model-generator**: Creates models displayed in views

---

**Generated by:** Wheels View Generator Skill v1.0
**Framework:** CFWheels 3.0+
**Last Updated:** 2025-10-20

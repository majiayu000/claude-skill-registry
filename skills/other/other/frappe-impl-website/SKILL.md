---
name: frappe-impl-website
description: >
  Use when building portal pages, Web Forms, website routes, or configuring themes and SEO in Frappe.
  Prevents 404 errors from wrong route resolution, broken Web Form submissions, and missing meta tags for SEO.
  Covers Web Page, Web Form, Portal Settings, Website Settings, website routes, Jinja templates, Blog, Web Template, has_web_view, meta tags, sitemap.
  Keywords: website, portal, Web Form, Web Page, route, theme, SEO, meta tags, has_web_view, Blog, Web Template, sitemap.
license: MIT
compatibility: "Claude Code, Claude.ai Projects, Claude API. Frappe v14-v16."
metadata:
  author: OpenAEC-Foundation
  version: "2.0"
---

# Frappe Website & Portals — Implementation Workflows

Step-by-step workflows for building websites, portals, and public-facing pages. For hooks syntax see `frappe-impl-hooks`. For Jinja templating see `frappe-impl-jinja`.

**Version**: v14/v15/v16 | **Note**: v15+ uses Bootstrap 5; v14 uses Bootstrap 4.

## Quick Decision: Which Page Type?

```
WHAT do you need?
├── Static content page (About, Terms)     → Web Page DocType or www/ HTML
├── Data entry by external users           → Web Form
├── List of records visible on website     → has_web_view on DocType
├── Blog / news articles                   → Blog Post + Blog Category
├── Custom app with sidebar/toolbar        → Custom Portal Page (www/)
└── Dynamic route with parameters          → website_route_rules in hooks.py
```

See `references/decision-tree.md` for the complete decision tree.

## Workflow 1: Create a Portal Page (www/)

Portal pages live in your app's `www/` directory. The file name becomes the URL route.

1. Create `myapp/www/custom_page.html`:

```html
{% extends "templates/web.html" %}
{% block page_content %}
<h1>{{ title }}</h1>
<div>{{ content }}</div>
{% endblock %}
```

2. Create matching controller `myapp/www/custom_page.py`:

```python
import frappe

def get_context(context):
    context.title = "My Custom Page"
    context.content = "Hello World"
    context.no_cache = 1  # ALWAYS set for dynamic content
```

3. Result: page available at `/custom_page`

**File types auto-loaded**: `.html` (template), `.py` (controller), `.css` (styles), `.js` (scripts).

**Subdirectory pattern** — for nested routes:
```
myapp/www/
├── services/
│   ├── index.html        → /services
│   ├── index.py
│   ├── consulting.html   → /services/consulting
│   └── consulting.py
```

### Context Variables Reference

| Key | Type | Effect |
|-----|------|--------|
| `title` | str | Page title and browser tab |
| `no_cache` | bool | Disable page caching |
| `no_header` | bool | Hide the page header |
| `no_breadcrumbs` | bool | Remove breadcrumbs |
| `add_breadcrumbs` | bool | Auto-generate from folder structure |
| `show_sidebar` | bool | Display web sidebar |
| `sitemap` | int | 0 = exclude from sitemap, 1 = include |
| `metatags` | dict | SEO meta tags (see Workflow 7) |

**Rule**: ALWAYS set `no_cache = 1` for pages with user-specific or frequently changing content.

## Workflow 2: Create a Web Form

Web Forms let external users submit data that creates Frappe documents.

1. Navigate to **Web Form** list → **New Web Form**
2. Set **Title**, select target **DocType**, set **Route** (URL slug)
3. Add fields — ALWAYS match `fieldname` to the target DocType field names
4. Configure access:
   - **Login Required**: uncheck for guest submissions
   - **Allow Edit**: let users edit their submissions
   - **Allow Multiple**: let users submit more than once
5. Save and publish

### Guest Submissions

```
ALLOWING guest submissions?
├── YES → Uncheck "Login Required"
│        → Set "Guest Title" for the submission form
│        → ALWAYS add rate limiting in site_config:
│           "rate_limit": {"web_form": "5/hour"}
│        → ALWAYS validate server-side (guests can bypass JS)
└── NO  → Keep "Login Required" checked (default)
```

### Web Form Custom Script (Client)

```javascript
frappe.web_form.on("after_load", function() {
    // Runs after form loads in browser
});

frappe.web_form.on("before_submit", function() {
    // Validate before submission — return false to cancel
    let val = frappe.web_form.get_value("email");
    if (!val) {
        frappe.throw("Email is required");
        return false;
    }
});

frappe.web_form.on("after_submit", function() {
    // Redirect or show message after success
    window.location.href = "/thank-you";
});
```

### Web Form Custom Script (Server — Python)

In the Web Form document, add a Python script:

```python
def get_context(context):
    # Add custom context variables for the template
    context.categories = frappe.get_all("Category", fields=["name", "title"])
```

**Rule**: NEVER trust client-side validation alone for Web Forms. ALWAYS validate in the target DocType's controller or server script.

## Workflow 3: Enable has_web_view on a DocType

This makes individual documents accessible as web pages (e.g., `/articles/my-article`).

1. Open DocType → check **Has Web View** and **Allow Guest to View**
2. Set the **Route** field prefix (e.g., `articles`)
3. ALWAYS add these fields to the DocType:
   - `route` (Data, hidden) — auto-generated URL slug
   - `published` (Check) — controls visibility
4. Create templates in the DocType directory:
   - `{doctype_name}.html` — single record template
   - `{doctype_name}_row.html` — list item template
5. In `hooks.py`, register as website generator:

```python
website_generators = ["Article"]
```

6. In the controller, implement `get_context`:

```python
class Article(WebsiteGenerator):
    website = frappe._dict(
        template="templates/generators/article.html",
        condition_field="published",
        page_title_field="title",
    )

    def get_context(self, context):
        context.related = frappe.get_all(
            "Article",
            filters={"published": 1, "name": ("!=", self.name)},
            fields=["title", "route"],
            limit=5,
        )
```

**Rule**: ALWAYS include a `published` check field. NEVER expose unpublished documents to guests.

## Workflow 4: Website Route Rules (hooks.py)

Route rules map URL patterns to controllers or pages.

```python
# hooks.py
website_route_rules = [
    # Map parameterized URL to a page
    {"from_route": "/projects/<name>", "to_route": "projects/project"},
    # Map URL prefix to DocType
    {"from_route": "/kb/<path:name>", "to_route": "knowledge-base"},
]

# Redirects (301/304)
website_redirects = [
    {"source": "/old-page", "target": "/new-page"},
    {"source": r"/docs(/.*)?", "target": r"https://docs.example.com\1"},
]

# Homepage for logged-in users (role-based)
role_home_page = {
    "Customer": "orders",
    "Supplier": "rfqs",
}

# Dynamic homepage
get_website_user_home_page = "myapp.utils.get_home_page"
```

**Priority order** for homepage: `get_website_user_home_page` > `role_home_page` > Portal Settings > Website Settings.

## Workflow 5: Blog Setup

1. Create **Blog Category** documents (e.g., "News", "Updates")
2. Create **Blog Post** documents:
   - Select category, write content (Markdown or Rich Text)
   - Set **Published** and **Published On** date
   - Blog route auto-generates as `/blog/{slug}`
3. Configure in **Website Settings**:
   - Set blog title
   - Enable/disable comments

**Rule**: ALWAYS set `Published On` date — posts without a date NEVER appear in RSS feeds.

## Workflow 6: Website Theme & Custom CSS

### Via Website Theme DocType

1. Navigate to **Website Theme** → New
2. Configure: fonts, colors, navbar style, button radius
3. Add custom CSS in the **Custom CSS** field
4. Set as active theme in **Website Settings**

### Via hooks.py

```python
# Inject CSS/JS on all web pages
website_context = {
    "favicon": "/assets/myapp/images/favicon.png",
}

update_website_context = "myapp.overrides.website_context"

# Override base template
base_template = "myapp/templates/custom_base.html"
```

## Workflow 7: SEO — Meta Tags, Open Graph & Sitemap

### In portal pages (frontmatter or context)

```python
def get_context(context):
    context.metatags = {
        "title": "My Page Title",
        "description": "Page description for search engines",
        "image": "/assets/myapp/images/og-image.png",
        "og:type": "website",
        "twitter:card": "summary_large_image",
    }
```

### In Web Page DocType

Set meta fields directly: **Meta Title**, **Meta Description**, **Meta Image**.

### Sitemap

- Frappe auto-generates `/sitemap.xml` from published Web Pages and has_web_view documents
- Exclude pages: set `sitemap = 0` in context or frontmatter
- Custom robots.txt: set `robots_txt` path in `site_config.json`

**Rule**: ALWAYS set `meta description` on public pages. NEVER leave it empty — search engines penalize pages without descriptions.

## Workflow 8: Guest Access & Security

```python
# site_config.json — rate limiting
{
    "rate_limit": {
        "web_form": "5/hour",
        "api": "100/hour"
    },
    "allowed_referrers": ["https://mysite.com"],
    "allow_cors": "https://mysite.com"
}
```

**Security rules**:
- ALWAYS enable CSRF protection (default). NEVER set `ignore_csrf` in production
- ALWAYS rate-limit guest-accessible endpoints
- ALWAYS sanitize user input in Web Forms (Frappe does this by default for standard fields)
- NEVER expose internal DocType names in guest-facing URLs without access control

## Anti-Patterns

| Anti-Pattern | Correct Approach |
|---|---|
| Hard-coding HTML in `get_context` | Use Jinja templates with context variables |
| Skipping `no_cache` on dynamic pages | ALWAYS set `no_cache = 1` for user-specific content |
| Guest Web Form without rate limiting | ALWAYS configure rate limits for guest forms |
| Missing `published` field on has_web_view | ALWAYS add published check to prevent data leaks |
| Using `website_route_rules` for simple redirects | Use `website_redirects` instead |
| Putting business logic in www/ controllers | Keep in DocType controllers; www/ is for presentation |

See `references/anti-patterns.md` for expanded anti-patterns with examples.

## See Also

- `frappe-impl-hooks` — Website hooks in detail
- `frappe-impl-jinja` — Jinja templating patterns
- `frappe-impl-controllers` — DocType controllers (WebsiteGenerator)
- `frappe-syntax-clientscripts` — Client-side API for Web Forms
- `references/generators.md` — Portal generators, blog system, custom routing patterns
- `references/workflows.md` — Extended workflow walkthroughs
- `references/examples.md` — Complete code examples
- `references/decision-tree.md` — Full decision tree for page types

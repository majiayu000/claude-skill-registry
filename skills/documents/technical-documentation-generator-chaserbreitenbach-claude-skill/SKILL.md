---
name: technical-documentation-generator
version: 1.0.0
description: |
  Automated HTML architecture documentation generator that produces navigable,
  searchable technical documentation from codebase analysis.
author: QuantQuiver AI R&D
license: MIT

category: tooling
tags:
  - documentation
  - html
  - architecture
  - api-docs
  - code-documentation
  - technical-writing

dependencies:
  skills: []
  python: ">=3.9"
  packages:
    - jinja2
    - markdown
    - pygments
  tools:
    - code_execution
    - bash

triggers:
  - "generate documentation"
  - "create API docs"
  - "architecture documentation"
  - "technical docs"
  - "document codebase"
  - "HTML documentation"
---

# Technical Documentation Generator

## Purpose

An automated HTML architecture documentation generator that produces navigable, searchable technical documentation from codebase analysis. Creates comprehensive documentation including API references, architecture diagrams, and component relationships.

**Problem Space:**
- Documentation often out of sync with code
- Manual documentation is time-consuming
- Architecture knowledge siloed in developers' heads
- No standardized format for technical docs

**Solution Approach:**
- Auto-extract documentation from code
- Generate architecture diagrams from structure
- Create searchable, navigable HTML output
- Support for multiple documentation styles

## When to Use

- New team member onboarding
- Project handoff documentation
- API reference generation
- Architecture decision records
- System overview documentation
- Open source project documentation

## When NOT to Use

- User-facing product documentation
- Marketing materials
- Tutorial/guide creation (use tutorial frameworks)
- Documentation requiring heavy customization

---

## Core Instructions

### Documentation Structure

```
docs/
├── index.html              # Home page with overview
├── architecture/
│   ├── index.html         # Architecture overview
│   ├── components.html    # Component breakdown
│   └── diagrams/          # Generated diagrams
├── api/
│   ├── index.html         # API overview
│   ├── endpoints.html     # REST endpoints
│   └── models.html        # Data models
├── guides/
│   ├── getting-started.html
│   └── deployment.html
├── reference/
│   ├── configuration.html
│   └── environment.html
├── assets/
│   ├── css/
│   ├── js/
│   └── images/
└── search.json            # Search index
```

### Standard Procedures

#### 1. Code Analysis

Extract documentation from:
- Docstrings (Python, JS)
- JSDoc/TSDoc comments
- OpenAPI/Swagger specs
- README files
- Inline comments with specific markers

#### 2. Architecture Extraction

Identify and document:
- Module/package structure
- Class hierarchies
- Function relationships
- API endpoints
- Database schemas

#### 3. Template Rendering

Use Jinja2 templates with:
- Consistent navigation
- Search functionality
- Syntax highlighting
- Responsive design
- Dark mode support

### Documentation Types

| Type | Source | Output |
|------|--------|--------|
| API Reference | Docstrings, OpenAPI | Endpoint documentation |
| Architecture | Directory structure | Component diagrams |
| Configuration | Config files, .env.example | Config reference |
| Models | Type definitions, schemas | Data model docs |
| Guides | Markdown files | HTML guides |

### HTML Template Structure

```html
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - {{ project_name }}</title>
    <link rel="stylesheet" href="{{ base_url }}/assets/css/main.css">
    <link rel="stylesheet" href="{{ base_url }}/assets/css/syntax.css">
</head>
<body>
    <nav class="sidebar">
        <div class="logo">
            <h1>{{ project_name }}</h1>
            <span class="version">v{{ version }}</span>
        </div>
        <div class="search">
            <input type="search" id="search" placeholder="Search docs...">
        </div>
        <ul class="nav-links">
            {% for section in navigation %}
            <li class="nav-section">
                <span class="section-title">{{ section.title }}</span>
                <ul>
                    {% for page in section.pages %}
                    <li><a href="{{ page.url }}"
                           class="{% if page.active %}active{% endif %}">
                        {{ page.title }}
                    </a></li>
                    {% endfor %}
                </ul>
            </li>
            {% endfor %}
        </ul>
    </nav>

    <main class="content">
        <header>
            <nav class="breadcrumb">
                {% for crumb in breadcrumbs %}
                <a href="{{ crumb.url }}">{{ crumb.title }}</a>
                {% if not loop.last %} / {% endif %}
                {% endfor %}
            </nav>
            <button class="theme-toggle" aria-label="Toggle theme">🌓</button>
        </header>

        <article>
            {{ content | safe }}
        </article>

        <footer>
            <div class="nav-footer">
                {% if prev_page %}
                <a href="{{ prev_page.url }}" class="prev">
                    ← {{ prev_page.title }}
                </a>
                {% endif %}
                {% if next_page %}
                <a href="{{ next_page.url }}" class="next">
                    {{ next_page.title }} →
                </a>
                {% endif %}
            </div>
            <p class="generated">Generated {{ generation_date }}</p>
        </footer>
    </main>

    <script src="{{ base_url }}/assets/js/search.js"></script>
    <script src="{{ base_url }}/assets/js/main.js"></script>
</body>
</html>
```

---

## Templates

### API Endpoint Template

```html
<section class="endpoint">
    <header class="endpoint-header">
        <span class="method {{ method | lower }}">{{ method }}</span>
        <code class="path">{{ path }}</code>
    </header>

    <div class="endpoint-body">
        <p class="description">{{ description }}</p>

        {% if parameters %}
        <h4>Parameters</h4>
        <table class="params-table">
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Type</th>
                    <th>Required</th>
                    <th>Description</th>
                </tr>
            </thead>
            <tbody>
                {% for param in parameters %}
                <tr>
                    <td><code>{{ param.name }}</code></td>
                    <td><code>{{ param.type }}</code></td>
                    <td>{{ "Yes" if param.required else "No" }}</td>
                    <td>{{ param.description }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
        {% endif %}

        {% if request_body %}
        <h4>Request Body</h4>
        <pre><code class="language-json">{{ request_body | tojson(indent=2) }}</code></pre>
        {% endif %}

        <h4>Response</h4>
        {% for status, response in responses.items() %}
        <div class="response">
            <span class="status {{ 'success' if status < 400 else 'error' }}">
                {{ status }}
            </span>
            <pre><code class="language-json">{{ response | tojson(indent=2) }}</code></pre>
        </div>
        {% endfor %}
    </div>
</section>
```

### Component Documentation Template

```html
<article class="component">
    <header>
        <h2>{{ component.name }}</h2>
        <span class="badge">{{ component.type }}</span>
    </header>

    <section class="overview">
        <h3>Overview</h3>
        <p>{{ component.description }}</p>
    </section>

    {% if component.dependencies %}
    <section class="dependencies">
        <h3>Dependencies</h3>
        <ul>
            {% for dep in component.dependencies %}
            <li>
                <a href="{{ dep.url }}">{{ dep.name }}</a>
                <span class="dep-type">{{ dep.type }}</span>
            </li>
            {% endfor %}
        </ul>
    </section>
    {% endif %}

    {% if component.methods %}
    <section class="methods">
        <h3>Methods</h3>
        {% for method in component.methods %}
        <div class="method">
            <h4 id="{{ method.id }}">
                <code>{{ method.signature }}</code>
            </h4>
            <p>{{ method.description }}</p>

            {% if method.params %}
            <h5>Parameters</h5>
            <dl>
                {% for param in method.params %}
                <dt><code>{{ param.name }}: {{ param.type }}</code></dt>
                <dd>{{ param.description }}</dd>
                {% endfor %}
            </dl>
            {% endif %}

            {% if method.returns %}
            <h5>Returns</h5>
            <p><code>{{ method.returns.type }}</code> - {{ method.returns.description }}</p>
            {% endif %}

            {% if method.example %}
            <h5>Example</h5>
            <pre><code class="language-python">{{ method.example }}</code></pre>
            {% endif %}
        </div>
        {% endfor %}
    </section>
    {% endif %}
</article>
```

### CSS Theme

```css
/* main.css */
:root {
    --color-primary: #3AA7F9;
    --color-primary-dark: #2A7BC4;
    --color-bg: #FFFFFF;
    --color-bg-secondary: #F8FAFC;
    --color-text: #0F172A;
    --color-text-secondary: #334155;
    --color-border: #E2E8F0;
    --color-code-bg: #1E293B;

    --sidebar-width: 280px;
    --content-max-width: 800px;
}

[data-theme="dark"] {
    --color-bg: #0F172A;
    --color-bg-secondary: #1E293B;
    --color-text: #F8FAFC;
    --color-text-secondary: #94A3B8;
    --color-border: #334155;
    --color-code-bg: #0F172A;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: 'Inter', system-ui, sans-serif;
    background: var(--color-bg);
    color: var(--color-text);
    line-height: 1.6;
}

.sidebar {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: var(--sidebar-width);
    background: var(--color-bg-secondary);
    border-right: 1px solid var(--color-border);
    padding: 1.5rem;
    overflow-y: auto;
}

.content {
    margin-left: var(--sidebar-width);
    padding: 2rem;
    max-width: calc(var(--content-max-width) + 4rem);
}

/* Method badges */
.method.get { background: #22C55E; }
.method.post { background: #3B82F6; }
.method.put { background: #F59E0B; }
.method.delete { background: #EF4444; }

/* Code blocks */
pre {
    background: var(--color-code-bg);
    border-radius: 8px;
    padding: 1rem;
    overflow-x: auto;
}

code {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.9em;
}
```

---

## Examples

### Example 1: Python Package Documentation

**Input**: "Generate documentation for my Python API"

**Process**:
1. Parse all `.py` files for docstrings
2. Extract function signatures and types
3. Build module hierarchy
4. Generate HTML pages for each module
5. Create search index

**Output**: Complete HTML documentation site with:
- Module index
- Class/function reference
- Type annotations
- Usage examples from docstrings

### Example 2: REST API Documentation

**Input**: "Document my Flask REST API with OpenAPI spec"

**Output**: Interactive API documentation with:
- Endpoint listing by resource
- Request/response examples
- Authentication details
- Error code reference

---

## Validation Checklist

Before finalizing documentation:

- [ ] All public APIs documented
- [ ] Examples compile/run
- [ ] Links not broken
- [ ] Search index generated
- [ ] Navigation complete
- [ ] Responsive on mobile
- [ ] Syntax highlighting works
- [ ] Dark mode functions
- [ ] Version number updated

---

## Related Resources

- Skill: `branded-document-suite` - PDF/DOCX exports
- Skill: `repository-auditor` - Code quality metrics
- Sphinx Documentation: https://www.sphinx-doc.org/
- MkDocs: https://www.mkdocs.org/

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- HTML template system
- Code extraction for Python
- Search functionality
- Dark mode support

---
name: rspress-nav
description: Configure RSPress navigation bars and sidebars with _nav.json and _meta.json files. Use when setting up navigation, organizing sidebar sections, or configuring collapsible menu items.
allowed-tools: Read, Write, Edit, Glob, Grep
agent: rspress-doc-agent
---

# RSPress Navigation Configuration

Configure RSPress navigation using `_nav.json` (navbar) and `_meta.json` (sidebar) files.

## Navigation Architecture

RSPress uses two navigation systems:

* **Top Navbar** (`_nav.json`) - Global navigation in the header
* **Sidebar** (`_meta.json`) - Contextual navigation per section/directory

## Navbar Configuration

Place `_nav.json` in the docs root (e.g., `docs/src/en/_nav.json`).

### Navbar Item Fields

| Field        | Type     | Description                                 |
|--------------|----------|---------------------------------------------|
| `text`       | string   | Display text for the nav item               |
| `link`       | string   | URL or path to navigate to                  |
| `activeMatch`| string   | Regex pattern to match active routes        |
| `items`      | array    | Nested dropdown items                       |

### Example Navbar

```json
[
  {
    "text": "Guide",
    "link": "/guide/introduction",
    "activeMatch": "^/guide/"
  },
  {
    "text": "API",
    "items": [
      { "text": "Core API", "link": "/api/core" },
      { "text": "Plugins", "link": "/api/plugins" }
    ]
  }
]
```

## Sidebar Configuration

Place `_meta.json` in each directory to configure sidebar for that section.

### Sidebar Entry Fields

| Field        | Type     | Description                                 |
|--------------|----------|---------------------------------------------|
| `type`       | string   | Entry type: `file`, `dir`, or `divider`     |
| `name`       | string   | File/directory name (without extension)     |
| `label`      | string   | Display text (overrides page title)         |
| `collapsible`| boolean  | Allow expanding/collapsing (dir only)       |
| `collapsed`  | boolean  | Initial collapsed state (dir only)          |
| `link`       | string   | Custom link for directory entries           |

### Example Sidebar

```json
[
  {
    "type": "file",
    "name": "introduction",
    "label": "Getting Started"
  },
  {
    "type": "dir",
    "name": "concepts",
    "label": "Core Concepts",
    "collapsible": true,
    "collapsed": false
  },
  {
    "type": "divider"
  },
  {
    "type": "file",
    "name": "advanced"
  }
]
```

## Common Navigation Patterns

### Auto-Generated Sidebar

Omit `_meta.json` to auto-generate sidebar from directory structure.

### Section Dividers

Use `{"type": "divider"}` to create visual separators in the sidebar.

### Nested Directories

Place `_meta.json` in subdirectories to configure nested sidebar sections. Each directory can have its own metadata configuration.

### Active Route Matching

Use `activeMatch` with regex to highlight navbar items:

```json
{
  "text": "Documentation",
  "link": "/docs/intro",
  "activeMatch": "^/docs/"
}
```

## Configuration Instructions

1. **Create navbar** - Add `_nav.json` in docs root with top-level navigation items
1. **Configure sections** - Add `_meta.json` in each directory to define sidebar structure
1. **Set labels** - Use `label` field to override default titles
1. **Organize with dividers** - Add dividers to group related items
1. **Enable collapsing** - Set `collapsible: true` for expandable directory sections
1. **Test navigation** - Verify active states and links work correctly

## File Structure Example

```text
docs/src/en/
├── _nav.json           # Top navbar configuration
├── guide/
│   ├── _meta.json      # Guide section sidebar
│   ├── introduction.md
│   └── advanced.md
└── api/
    ├── _meta.json      # API section sidebar
    └── reference.md
```

## Notes

* File `name` must match the actual filename (without `.md` extension)
* Auto-generated sidebars use alphabetical order
* Navbar supports one level of nested dropdown items
* Sidebar supports unlimited nesting via directory structure

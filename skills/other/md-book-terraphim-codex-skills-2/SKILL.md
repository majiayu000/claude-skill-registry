---
name: md-book
description: |
  MD-Book documentation generator skill. Use when working with MD-Book, a modern
  mdbook replacement for generating HTML documentation from Markdown files.
  Supports syntax highlighting, live reload, Pagefind search, and Tera templates.
license: Apache-2.0
---

# MD-Book Documentation Generator Skill

Use this skill when working with MD-Book, a modern mdbook replacement for generating HTML documentation from Markdown files.

## Overview

MD-Book is a Rust-based documentation generator that converts Markdown files to beautiful, searchable HTML documentation. It supports multiple markdown formats (Markdown, GFM, MDX), server-side syntax highlighting, live development server, and integrated Pagefind search.

## CLI Usage

### Basic Commands

```bash
# Build documentation (converts markdown to HTML)
md-book -i input_dir -o output_dir

# Development mode with file watching
md-book -i input_dir -o output_dir --watch

# Development with built-in server (default port 3000)
md-book -i input_dir -o output_dir --serve

# Full development mode (watch + serve on custom port)
md-book -i input_dir -o output_dir --watch --serve --port 8080
```

### CLI Options

| Option | Short | Description |
|--------|-------|-------------|
| `--input` | `-i` | Input directory containing markdown files (required) |
| `--output` | `-o` | Output directory for HTML files (required) |
| `--config` | `-c` | Optional path to config file |
| `--watch` | `-w` | Watch for changes and rebuild |
| `--serve` | `-s` | Serve at http://localhost:3000 |
| `--port` | | Port to serve on (default: 3000) |

### Running from Source

```bash
# Clone and build
git clone https://github.com/terraphim/md-book.git
cd md-book
cargo build --release

# Run from source
cargo run -- -i docs -o output
cargo run -- -i docs -o output --serve --watch
```

## Configuration

### Configuration Priority (highest to lowest)

1. CLI arguments
2. Environment variables (MDBOOK_ prefix)
3. Custom config file (--config flag)
4. book.toml in current directory
5. Default values

### book.toml Configuration

Create `book.toml` in your input directory:

```toml
[book]
title = "My Documentation"
authors = ["Your Name"]
description = "Documentation description"
language = "en"

[output.html]
# Security: raw HTML in markdown is DISABLED by default
allow-html = false  # Set to true only if you trust all content authors
mathjax-support = false
```

### Environment Variables

```bash
# Override book title
MDBOOK_BOOK.TITLE="My Book" md-book -i input -o output

# Nested configuration values use underscore
MDBOOK_OUTPUT.HTML.MATHJAX_SUPPORT=true md-book -i input -o output
```

## Project Structure

### Input Directory

```
input/
  index.md          # OPTIONAL: Custom home page content
                    # If present: renders your markdown as home page
                    # If absent: auto-generates card-based navigation
  getting-started.md
  configuration.md
  advanced/         # Subdirectories become sections
    topic1.md
    topic2.md
  images/           # Static assets copied to output
```

### Output Directory

```
output/
  index.html        # Generated home page
  getting-started.html
  configuration.html
  advanced/
    topic1.html
    topic2.html
  css/             # Styles
  js/              # JavaScript (live reload, search, syntax highlighting)
  pagefind/        # Search index (if search feature enabled)
```

## Features

### Syntax Highlighting

Server-side syntax highlighting via syntect. Supports all major languages:

````markdown
```rust
fn main() {
    println!("Hello, world!");
}
```

```python
def hello():
    print("Hello, world!")
```
````

### Full-Text Search (Pagefind)

Search is built in via Pagefind. Requires pagefind CLI:

```bash
# Install pagefind
cargo install pagefind

# Pagefind runs automatically during build
# Manual indexing if needed:
pagefind --site output_dir
```

### Live Reload

When using `--serve --watch`, pages automatically reload on file changes via WebSocket.

### Index Page (Two Methods)

MD-Book supports two ways to create your documentation home page:

#### Method 1: Custom Content with index.md

Create an `index.md` file in your input directory for a custom home page:

```markdown
# Welcome to My Documentation

This is my custom home page content with full markdown support.

## Quick Links

- [Getting Started](getting-started.md)
- [Configuration](configuration.md)
- [API Reference](api/reference.md)
```

When `index.md` exists, its content is rendered as the home page. This gives you full control over the layout and content.

#### Method 2: Auto-Generated Card Navigation

If **no `index.md` is present**, MD-Book automatically generates a card-based home page using Shoelace UI components. This displays:

- A "Documentation" header
- Cards for each section/directory
- Cards for each page within sections
- "Read More" buttons linking to each page

This is ideal for quickly getting started or for projects where you want automatic navigation without maintaining a custom index.

**Choosing Between Methods:**
- Use **index.md** when you want custom welcome content, specific navigation order, or branded messaging
- Use **auto-generated cards** for quick setup or when documentation structure should drive navigation

### Right-Hand TOC

Each page includes a right-hand table of contents for in-page navigation.

## Template Customization

Templates use Tera templating engine:

| Template | Purpose |
|----------|---------|
| `page.html.tera` | Individual page layout |
| `index.html.tera` | Home page |
| `sidebar.html.tera` | Navigation sidebar |
| `header.html.tera` | Page header |
| `footer.html.tera` | Page footer |

### Web Components

Built-in Web Components:
- `doc-toc.js` - Table of contents
- `search-modal.js` - Search interface
- `doc-sidebar.js` - Responsive sidebar
- `simple-block.js` - Content blocks

## Deployment

### Cloudflare Pages (Recommended)

```bash
# Setup
./scripts/setup-cloudflare.sh

# Deploy
./scripts/deploy.sh production
```

### Netlify

```bash
# Build
cargo run -- -i docs -o dist

# Deploy
netlify deploy --prod --dir=dist
```

### GitHub Pages

Use the GitHub Actions workflow:

```yaml
- name: Build site
  run: cargo run -- -i docs -o _site

- name: Deploy to GitHub Pages
  uses: actions/deploy-pages@v4
```

### Other Platforms

Vercel, AWS Amplify, Render, Railway, Fly.io, and DigitalOcean are all supported. See DEPLOYMENT.md for details.

## Testing

```bash
# Unit tests
cargo test --lib --bins

# Integration tests
cargo test --test integration --features "tokio,search,syntax-highlighting"

# All tests
cargo test --all-targets --features "tokio,search,syntax-highlighting"

# Quality checks
make qa              # Format, clippy, tests
make ci-local        # Simulate CI locally
```

## Feature Flags

```toml
# Cargo.toml features
default = ["server", "watcher", "search", "syntax-highlighting"]
server = ["warp", "tokio/full"]           # Dev server with live reload
watcher = ["notify", "tokio/full"]         # File watching
search = ["pagefind"]                      # Pagefind search integration
syntax-highlighting = ["syntect"]          # Code highlighting
wasm = ["wasm-bindgen"]                    # WASM support
```

Build minimal version:
```bash
cargo build --no-default-features
```

## Security Considerations

### HTML in Markdown

Raw HTML is **disabled by default** for security. Enable only if you trust all content:

```toml
[output.html]
allow-html = true  # WARNING: Enables XSS risk
```

### Secrets Management

- Use 1Password integration or environment variables
- Never commit `.env` files
- See `docs/1PASSWORD_SETUP.md` for secure setup

## Common Patterns

### Creating Documentation Project

**With custom index page:**
```bash
mkdir docs
cat > docs/index.md << 'EOF'
# Welcome to My Project

This is the home page with custom content.

## Quick Start
See [Getting Started](getting-started.md) to begin.
EOF

cat > docs/getting-started.md << 'EOF'
# Getting Started

Installation and setup instructions.
EOF

md-book -i docs -o output --serve --watch
```

**With auto-generated card navigation:**
```bash
mkdir docs
# No index.md - cards will be auto-generated

cat > docs/getting-started.md << 'EOF'
# Getting Started

Installation and setup instructions.
EOF

cat > docs/configuration.md << 'EOF'
# Configuration

How to configure the project.
EOF

md-book -i docs -o output --serve --watch
# Home page shows cards linking to all pages automatically
```

### Adding Search

Search works automatically when pagefind is installed:

```bash
cargo install pagefind
md-book -i docs -o output  # Search index generated automatically
```

### Custom Styling

Edit CSS in `src/templates/css/styles.css` or provide custom template directory.

## Troubleshooting

### Build Fails

```bash
# Verify Rust installation
rustc --version
cargo --version

# Clean and rebuild
cargo clean
cargo build --release
```

### Search Not Working

```bash
# Verify pagefind installed
which pagefind

# Manually run indexing
pagefind --site output_dir
```

### Live Reload Not Working

Ensure using both flags together:
```bash
md-book -i docs -o output --watch --serve
```

## Repository

- GitHub: https://github.com/terraphim/md-book
- Issues: https://github.com/terraphim/md-book/issues
- Discussions: https://github.com/terraphim/md-book/discussions

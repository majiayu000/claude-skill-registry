---
name: presenterm
description: Create and deliver terminal-based presentations from markdown files with themes, code execution, mermaid/d2 diagrams, LaTeX/typst formulas, and PDF/HTML export capabilities.
---

# presenterm - Terminal Slideshow Tool

presenterm is a modern terminal-based presentation tool that renders markdown files as slides. It supports themes, code syntax highlighting, images, diagram rendering (mermaid, d2), mathematical formulas (LaTeX, typst), and can export to PDF or HTML.

## Core Principles

- **Markdown-first**: Write presentations in familiar markdown syntax
- **Terminal-native**: Runs entirely in the terminal with rich rendering
- **Advanced rendering**: Render mermaid/d2 diagrams and LaTeX/typst formulas as images
- **Presentation mode**: Separate presentation view with speaker notes support
- **Export capabilities**: Generate PDF or HTML from markdown slides
- **Code execution**: Execute code snippets during presentations
- **Theme support**: Multiple built-in themes and custom theme support

## Installation

```bash
# macOS (Homebrew)
brew install presenterm

# Cargo
cargo install presenterm

# From source
git clone https://github.com/mfontanini/presenterm
cd presenterm
cargo install --path .
```

## Basic Usage

### Running Presentations

```bash
# Run a presentation
presenterm presentation.md

# Use presentation mode (full-screen, controls hidden)
presenterm -p presentation.md
presenterm --present presentation.md

# Use specific theme
presenterm -t dark presentation.md
presenterm --theme catppuccin presentation.md

# List available themes
presenterm --list-themes

# Show current theme
presenterm --current-theme
```

### Exporting

```bash
# Export to PDF
presenterm -e presentation.md
presenterm --export-pdf presentation.md

# Export to PDF with specific output path
presenterm -e presentation.md -o output.pdf
presenterm --export-pdf presentation.md --output slides.pdf

# Export to HTML
presenterm -E presentation.md
presenterm --export-html presentation.md -o presentation.html

# Specify temporary path for export
presenterm -e presentation.md --export-temporary-path /tmp/presenterm
```

## Markdown Syntax

### Slide Separators

```markdown
<!-- Slides are separated by --- -->

# First Slide
Content here

---

# Second Slide
More content

---

# Third Slide
Final slide
```

### Slide Layout

```markdown
# Title Slide
## Subtitle
Author Name

---

# Content Slide

- Bullet point 1
- Bullet point 2
  - Nested point
- Bullet point 3

---

# Code Slide

```rust
fn main() {
    println!("Hello, presenterm!");
}
``` (triple backtick)

---

# Quote Slide

> "The best way to predict the future is to invent it."
> — Alan Kay
```

### Speaker Notes

```markdown
# My Slide

Visible content

<!-- presenter notes
These notes are only visible in presentation mode
They won't appear on the slide itself
-->

More visible content

---

# Another Slide

<!-- speaker notes
- Remember to mention X
- Don't forget Y
- Emphasize Z
-->
```

### Images

```markdown
# Image Slide

![Description](path/to/image.png)

---

# Centered Image

![](./logo.png)
```

### Tables

```markdown
# Table Example

| Feature | Status | Priority |
|---------|--------|----------|
| Export  | Done   | High     |
| Themes  | Done   | High     |
| Images  | Done   | Medium   |
```

### Code Highlighting

````markdown
# Syntax Highlighting

```python
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
```

```rust
fn factorial(n: u64) -> u64 {
    (1..=n).product()
}
```

```javascript
const greet = (name) => {
    console.log(`Hello, ${name}!`);
};
```
````

## Code Execution

### Executable Code Blocks

```bash
# Enable code snippet execution
presenterm -x presentation.md
presenterm --enable-snippet-execution presentation.md

# Enable auto-execution with replacement
presenterm -X presentation.md
presenterm --enable-snippet-execution-replace presentation.md

# Validate snippets without running
presenterm --validate-snippets presentation.md
```

### Executable Code Syntax

````markdown
# Live Demo

```bash +exec
echo "This will execute when you advance to this slide"
date
```

---

# Auto-Replace Demo

```bash +exec_replace
ls -la
```

<!-- The output will replace the code block -->
````

## Advanced Rendering

presenterm supports rendering diagrams and formulas directly from code blocks, converting them to images during presentation load.

### Mermaid Diagrams

Render mermaid diagrams using the `+render` attribute.

**Requirements:**
- Install [mermaid-cli](https://github.com/mermaid-js/mermaid-cli): `npm install -g @mermaid-js/mermaid-cli`

**Syntax:**

````markdown
```mermaid +render
sequenceDiagram
    Alice->>Bob: Hello Bob, how are you?
    Bob-->>Alice: I'm good thanks!
    Alice-)Bob: See you later!
```

```mermaid +render
graph TD
    A[Start] --> B{Is it working?}
    B -->|Yes| C[Great!]
    B -->|No| D[Debug]
    D --> B
```

```mermaid +render
pie title Project Time Distribution
    "Development" : 40
    "Testing" : 25
    "Documentation" : 20
    "Meetings" : 15
```
````

**Configuration (in config.yaml):**

```yaml
mermaid:
  # Theme selection
  theme: dark
  # Background color
  background: "#2E3440"
  # Image scaling
  scale: 2.0
```

**Size control with width attribute:**

````markdown
```mermaid +render +width:80%
graph LR
    A --> B --> C
```
````

**Performance Note:**
- Rendering takes ~2 seconds per diagram
- Rendered asynchronously (default 2 threads)

### d2 Diagrams

Render d2 diagrams for architecture and system diagrams.

**Requirements:**
- Install [d2](https://github.com/terrastruct/d2): `brew install d2` or download from releases

**Syntax:**

````markdown
```d2 +render
# System Architecture
web_server: Web Server {
  shape: rectangle
}
database: Database {
  shape: cylinder
}
cache: Redis Cache {
  shape: stored_data
}

web_server -> database: queries
web_server -> cache: reads/writes
```

```d2 +render
my_table: {
  shape: sql_table
  id: int {constraint: primary_key}
  username: varchar(255)
  email: varchar(255)
  created_at: timestamp
}
```

```d2 +render
direction: right

users -> api: HTTP requests
api -> auth: validate token
api -> database: query data
api -> cache: check cache
```
````

**Configuration (in config.yaml):**

```yaml
d2:
  # Theme selection
  theme: "Nord"
  # Image scaling
  scale: 1.5
```

**Size control:**

````markdown
```d2 +render +width:70%
A -> B -> C
```
````

### LaTeX Formulas

Render LaTeX mathematical formulas as images.

**Requirements:**
- Install [typst](https://github.com/typst/typst): `brew install typst` or `cargo install typst-cli`
- Install [pandoc](https://pandoc.org/installing.html): `brew install pandoc`

**How it works:**
- Pandoc converts LaTeX to typst
- Typst renders the formula to an image

**Syntax:**

````markdown
```latex +render
\[ \sum_{n=1}^{\infty} 2^{-n} = 1 \]
```

```latex +render
\[
E = mc^2
\]
```

```latex +render
\[
\int_{-\infty}^{\infty} e^{-x^2} dx = \sqrt{\pi}
\]
```

```latex +render
\[
\frac{d}{dx}\left( \int_{a}^{x} f(u)\,du\right) = f(x)
\]
```

```latex +render
\[
\begin{bmatrix}
a & b \\
c & d
\end{bmatrix}
\]
```
````

**Configuration (in config.yaml):**

```yaml
# Pixels per inch for formula rendering
typst:
  ppi: 300
```

**Size control:**

````markdown
```latex +render +width:60%
\[ \oint_C \mathbf{F} \cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F}) \cdot d\mathbf{S} \]
```
````

### Typst Formulas

Render typst formulas directly (bypassing LaTeX conversion).

**Requirements:**
- Install [typst](https://github.com/typst/typst): `brew install typst`

**Syntax:**

````markdown
```typst +render
$ sum_(n=1)^oo 1/n^2 = pi^2/6 $
```

```typst +render
$ integral_(-oo)^oo e^(-x^2) d x = sqrt(pi) $
```

```typst +render
$ mat(
  1, 2;
  3, 4;
) $
```
````

**Benefits over LaTeX:**
- Faster (no pandoc conversion step)
- Native typst syntax
- More modern formula typesetting

### Rendering Configuration

**Global config.yaml settings:**

```yaml
# Formula rendering
typst:
  ppi: 300  # Pixels per inch for formulas

# Mermaid diagrams
mermaid:
  theme: dark
  background: "#2E3440"
  scale: 2.0

# d2 diagrams
d2:
  theme: "Nord"
  scale: 1.5
```

### Complete Rendering Example

````markdown
# System Architecture

```d2 +render +width:80%
users: Users {
  shape: person
}
lb: Load Balancer {
  shape: rectangle
}
api: API Servers {
  shape: rectangle
}
db: Database {
  shape: cylinder
}

users -> lb
lb -> api: distribute
api -> db: query
```

---

# Request Flow

```mermaid +render
sequenceDiagram
    participant U as User
    participant A as API
    participant D as Database
    participant C as Cache

    U->>A: Request data
    A->>C: Check cache
    alt Cache hit
        C-->>A: Return cached data
    else Cache miss
        A->>D: Query database
        D-->>A: Return data
        A->>C: Update cache
    end
    A-->>U: Response
```

---

# Algorithm Complexity

```latex +render
\[
T(n) = \begin{cases}
O(1) & \text{best case} \\
O(\log n) & \text{average case} \\
O(n) & \text{worst case}
\end{cases}
\]
```

---

# Mathematical Formula

```typst +render
$ P(A|B) = (P(B|A) dot P(A)) / P(B) $
```
````

## Image Protocols

```bash
# Auto-detect best protocol
presenterm --image-protocol auto presentation.md

# Use iTerm2 protocol
presenterm --image-protocol iterm2 presentation.md

# Use kitty protocol (local mode)
presenterm --image-protocol kitty-local presentation.md

# Use kitty protocol (remote mode)
presenterm --image-protocol kitty-remote presentation.md

# Use sixel protocol
presenterm --image-protocol sixel presentation.md

# Use ASCII blocks (fallback)
presenterm --image-protocol ascii-blocks presentation.md
```

## Themes

### Built-in Themes

```bash
# List all available themes
presenterm --list-themes

# Common themes:
presenterm -t dark presentation.md
presenterm -t light presentation.md
presenterm -t catppuccin presentation.md
presenterm -t dracula presentation.md
presenterm -t gruvbox presentation.md
presenterm -t monokai presentation.md
presenterm -t nord presentation.md
presenterm -t solarized-dark presentation.md
presenterm -t solarized-light presentation.md
```

### Custom Themes

```bash
# Use custom theme from config
presenterm -c ~/.config/presenterm/config.yaml presentation.md
presenterm --config-file custom-config.yaml presentation.md
```

## Speaker Notes Mode

### Publishing Speaker Notes

```bash
# Publish speaker notes to local network
presenterm -P presentation.md
presenterm --publish-speaker-notes presentation.md

# Listen for speaker notes (presenter's view)
presenterm -l
presenterm --listen-speaker-notes
```

This allows you to:
- Run presentation on one screen
- View speaker notes on another device/screen
- Perfect for dual-monitor setups

## Validation

```bash
# Validate that slides don't overflow terminal
presenterm --validate-overflows presentation.md

# Validate code snippets
presenterm --validate-snippets presentation.md

# Combine validations
presenterm --validate-overflows --validate-snippets presentation.md
```

## Keyboard Controls

### During Presentation

```
Navigation:
  ←/→         Previous/Next slide
  Space/Enter Next slide
  Backspace   Previous slide
  Home        First slide
  End         Last slide
  g           Go to specific slide (enter number)

Display:
  f           Toggle fullscreen
  q/Esc       Quit presentation

Code Execution:
  e           Execute code block (with -x flag)

Help:
  ?           Show help/controls
```

## Configuration

### Config File Location

```bash
# Default config locations:
# - Linux: ~/.config/presenterm/config.yaml
# - macOS: ~/Library/Application Support/presenterm/config.yaml
# - Windows: %APPDATA%\presenterm\config.yaml

# Specify custom config
presenterm -c /path/to/config.yaml presentation.md
```

### Example Configuration

```yaml
# config.yaml
theme: catppuccin
image_protocol: auto

# Default options
presentation_mode: true
validate_overflows: true

# Code execution
enable_snippet_execution: false
```

## Common Workflows

### Workflow 1: Create Simple Presentation

```bash
# 1. Create markdown file
cat > demo.md << 'EOF'
# Welcome
## A presenterm demo

---

# Key Features

- Terminal-based
- Markdown syntax
- Multiple themes
- Export to PDF/HTML

---

# Thank You!

Questions?
EOF

# 2. Run presentation
presenterm -p demo.md

# 3. Export to PDF
presenterm -e demo.md -o demo.pdf
```

### Workflow 2: Technical Presentation with Code

````bash
# 1. Create presentation with code examples
cat > tech-talk.md << 'EOF'
# Technical Deep Dive
## Rust Async Programming

---

# Basic Example

```rust
async fn fetch_data() -> Result<String, Error> {
    let response = reqwest::get("https://api.example.com")
        .await?;
    response.text().await
}
```

<!-- presenter notes
Explain async/await syntax
Mention error handling
-->

---

# Live Demo

```bash +exec
cargo --version
rustc --version
```

---

# Questions?

EOF

# 2. Present with code execution enabled
presenterm -x -p tech-talk.md

# 3. Validate before sharing
presenterm --validate-overflows --validate-snippets tech-talk.md

# 4. Export for distribution
presenterm -e tech-talk.md -o tech-talk.pdf
````

### Workflow 3: Dual-Screen Presentation

```bash
# Terminal 1 (presenter view with notes)
presenterm -P presentation.md

# Terminal 2 (or another device - audience view)
presenterm -l

# This shows:
# - Terminal 1: Full presentation with speaker notes visible
# - Terminal 2: Synchronized view following presenter
```

### Workflow 4: Themed Corporate Presentation

```bash
# 1. Create config with company theme
mkdir -p ~/.config/presenterm
cat > ~/.config/presenterm/config.yaml << 'EOF'
theme: solarized-light
presentation_mode: true
validate_overflows: true
EOF

# 2. Create presentation
vim quarterly-review.md

# 3. Preview with theme
presenterm quarterly-review.md

# 4. Export with theme applied
presenterm -e quarterly-review.md -o quarterly-review.pdf

# 5. Also export HTML version
presenterm -E quarterly-review.md -o quarterly-review.html
```

### Workflow 5: Conference Talk

````markdown
# Conference Talk Template

---

# About Me

![Profile](./images/profile.png)

- Name
- Title
- Company
- Twitter: @handle

<!-- presenter notes
- Smile at audience
- Check time: should be at 2 minutes
-->

---

# Agenda

1. Problem Statement
2. Our Approach
3. Demo
4. Results
5. Q&A

---

# Problem Statement

## The Challenge

- Point 1
- Point 2
- Point 3

<!-- presenter notes
- Share personal experience
- Ask if anyone relates
-->

---

# Live Demo

```bash +exec
./demo.sh
```

---

# Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Speed  | 100ms  | 10ms  | 10x         |
| Memory | 500MB  | 50MB  | 10x         |

---

# Thank You!

## Questions?

Slides: https://example.com/slides
Code: https://github.com/user/repo
````

## Best Practices

### Slide Design

1. **One idea per slide**: Keep slides focused
2. **Minimal text**: Use bullets, not paragraphs
3. **Visual hierarchy**: Use headings effectively
4. **Code readability**: Keep code snippets short and readable
5. **Consistent formatting**: Use same style throughout

### File Organization

```
presentation/
├── slides.md           # Main presentation
├── images/             # Image assets
│   ├── logo.png
│   ├── diagram1.png
│   └── screenshot.png
├── code/               # Code examples
│   ├── example1.rs
│   └── demo.py
└── export/             # Exported versions
    ├── slides.pdf
    └── slides.html
```

### Speaker Notes

```markdown
# Slide Title

Visible content

<!-- presenter notes
Time checkpoint: 5 minutes
Key talking points:
- Emphasize security aspect
- Mention customer feedback
- Transition to demo
Reminder: drink water!
-->
```

### Code Examples

1. **Syntax highlighting**: Always specify language
2. **Keep it short**: 10-15 lines max per slide
3. **Highlight key parts**: Use comments to draw attention
4. **Test code**: Ensure examples are correct
5. **Use exec sparingly**: Only for impactful demos

### Validation Before Presenting

```bash
# Full validation checklist
presenterm --validate-overflows presentation.md
presenterm --validate-snippets presentation.md
presenterm -p presentation.md  # Dry run
presenterm -e presentation.md  # Generate backup PDF
```

## Tips and Tricks

### Quick Presentation Template

```bash
# Create new presentation from template
cat > new-talk.md << 'EOF'
# Talk Title
## Subtitle
Your Name

---

# Outline

1. Introduction
2. Main Content
3. Conclusion

---

# Section 1

Content here

---

# Thank You

Questions?
EOF
```

### Rapid Iteration

```bash
# Use watch for live reload during development
# (requires 'entr' or 'watchexec')

# With entr
echo presentation.md | entr presenterm /_

# With watchexec
watchexec -w presentation.md presenterm presentation.md
```

### Export All Formats

```bash
#!/bin/bash
# export-all.sh - Export presentation to all formats

PRESENTATION="$1"
BASENAME="${PRESENTATION%.md}"

echo "Exporting $PRESENTATION..."

# PDF
presenterm -e "$PRESENTATION" -o "${BASENAME}.pdf"
echo "✓ PDF exported"

# HTML
presenterm -E "$PRESENTATION" -o "${BASENAME}.html"
echo "✓ HTML exported"

echo "All exports complete!"
```

### Presentation Checklist

```markdown
## Pre-Presentation Checklist

Technical:
- [ ] Run validation: `presenterm --validate-overflows slides.md`
- [ ] Test code execution blocks
- [ ] Verify images load correctly
- [ ] Check font size visibility
- [ ] Test on actual presentation screen
- [ ] Export backup PDF

Content:
- [ ] Timing (practice run-through)
- [ ] Speaker notes complete
- [ ] Transitions smooth
- [ ] No typos
- [ ] Links working

Setup:
- [ ] Terminal font size readable
- [ ] Theme appropriate for venue
- [ ] Backup presentation on USB
- [ ] Power adapter
- [ ] HDMI/adapter cable
```

## Troubleshooting

### Images Not Displaying

```bash
# Try different image protocols
presenterm --image-protocol iterm2 presentation.md
presenterm --image-protocol kitty-local presentation.md
presenterm --image-protocol ascii-blocks presentation.md  # Fallback

# Check image paths are relative or absolute
# Ensure images exist
ls -la images/
```

### Slides Overflow Terminal

```bash
# Validate first
presenterm --validate-overflows presentation.md

# Solutions:
# 1. Reduce content per slide
# 2. Increase terminal size
# 3. Use smaller font
# 4. Break into multiple slides
```

### Code Execution Not Working

```bash
# Ensure execution is enabled
presenterm -x presentation.md

# Check script permissions
chmod +x script.sh

# Test code block independently first
```

### Theme Not Applied

```bash
# List available themes
presenterm --list-themes

# Check current theme
presenterm --current-theme

# Specify theme explicitly
presenterm -t dark presentation.md

# Check config file location
ls -la ~/.config/presenterm/config.yaml
```

## Integration with Other Tools

### With Git

```bash
# Track presentations in version control
git init
git add presentation.md images/
git commit -m "feat: add initial presentation"

# Create tagged releases for different versions
git tag -a v1.0 -m "Conference version"
```

### With make/just

```just
# justfile
present:
    presenterm -p slides.md

export:
    presenterm -e slides.md -o output.pdf
    presenterm -E slides.md -o output.html

validate:
    presenterm --validate-overflows slides.md
    presenterm --validate-snippets slides.md

all: validate export
```

### With Continuous Integration

```yaml
# .github/workflows/validate-presentation.yml
name: Validate Presentation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install presenterm
        run: cargo install presenterm
      - name: Validate slides
        run: |
          presenterm --validate-overflows presentation.md
          presenterm --validate-snippets presentation.md
      - name: Export PDF
        run: presenterm -e presentation.md -o presentation.pdf
      - name: Upload PDF
        uses: actions/upload-artifact@v2
        with:
          name: presentation
          path: presentation.pdf
```

## Quick Reference

```bash
# Basic usage
presenterm slides.md              # View presentation
presenterm -p slides.md           # Presentation mode
presenterm -t dark slides.md      # With theme

# Export
presenterm -e slides.md           # Export to PDF
presenterm -E slides.md           # Export to HTML
presenterm -e slides.md -o out.pdf # Custom output path

# Validation
presenterm --validate-overflows slides.md
presenterm --validate-snippets slides.md

# Code execution
presenterm -x slides.md           # Enable execution
presenterm -X slides.md           # Auto-replace execution

# Themes
presenterm --list-themes          # List themes
presenterm --current-theme        # Show current theme

# Speaker notes
presenterm -P slides.md           # Publish notes
presenterm -l                     # Listen for notes

# Help
presenterm --help                 # Full help
presenterm --acknowledgements     # Show acknowledgements
presenterm -V                     # Version
```

## Markdown Quick Reference

```markdown
# Slide separator
---

# Headings
# H1
## H2
### H3

# Lists
- Bullet point
  - Nested bullet
1. Numbered item

# Code blocks
```language
code here
``` (triple backtick)

# Images
![Alt text](path/to/image.png)

# Tables
| Col1 | Col2 |
|------|------|
| A    | B    |

# Quotes
> Quote text

# Speaker notes
<!-- presenter notes
Notes here
-->

# Executable code
```bash +exec
command
``` (triple backtick)

# Rendered diagrams
```mermaid +render
graph TD
    A --> B
``` (triple backtick)

```d2 +render
A -> B
``` (triple backtick)

# Rendered formulas
```latex +render
\[ E = mc^2 \]
``` (triple backtick)

```typst +render
$ sum_(i=1)^n i = (n(n+1))/2 $
``` (triple backtick)
```

## Resources

- Official repository: https://github.com/mfontanini/presenterm
- Documentation: https://github.com/mfontanini/presenterm/wiki
- Issue tracker: https://github.com/mfontanini/presenterm/issues
- Installation: `brew install presenterm` or `cargo install presenterm`

## Summary

**Primary directives:**
1. Write presentations in markdown
2. Use presentation mode (`-p`) for actual presentations
3. Use advanced rendering: mermaid/d2 for diagrams, LaTeX/typst for formulas
4. Include speaker notes for complex slides
5. Validate before presenting
6. Export to PDF/HTML for distribution
7. Choose appropriate theme for venue/audience
8. Keep slides simple and focused
9. Test code execution and rendering blocks before presenting

**Most common commands:**
- `presenterm -p slides.md` - Present
- `presenterm -e slides.md` - Export PDF
- `presenterm -t theme slides.md` - Use theme
- `presenterm --validate-overflows slides.md` - Validate
- `presenterm --list-themes` - See themes

**Advanced rendering:**
- Mermaid diagrams: ` ```mermaid +render` (requires mermaid-cli)
- d2 diagrams: ` ```d2 +render` (requires d2)
- LaTeX formulas: ` ```latex +render` (requires typst + pandoc)
- Typst formulas: ` ```typst +render` (requires typst)

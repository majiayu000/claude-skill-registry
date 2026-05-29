---
name: quarto-book-setup
description: Initialize a new Quarto book project with GitHub Pages. Use when creating a new documentation site, tutorial, or book.
user-invocable: true
---

# Set Up New Quarto Book

When the user invokes `/quarto-book-setup`, scaffold a new Quarto book project.

## Gather Information

Ask the user:
1. **Project name** — Directory and repo name
2. **Book title** — Display title for the book
3. **Author** — Who to credit
4. **GitHub org/account** — Where to host (optional, can skip GitHub setup)
5. **Public or private** — Repository visibility

## Create Project Structure

```
project-name/
├── _quarto.yml
├── index.qmd
├── .gitignore
├── .claude/
│   └── CLAUDE.md
├── PLAN.md
├── README.md
├── images/
└── chapters/           # or use part1/, part2/ structure
    └── intro.qmd
```

## _quarto.yml Template

```yaml
project:
  type: book
  output-dir: _book

execute:
  freeze: auto

book:
  title: "BOOK_TITLE"
  author: "AUTHOR"
  date: today
  date-format: "MMMM YYYY"
  chapters:
    - index.qmd
    - chapters/intro.qmd

format:
  html:
    theme:
      light: cosmo
      dark: darkly
    toc: true
    code-copy: true
```

## .gitignore Template

```
_book/
_site/
.quarto/
*.quarto_ipynb
.DS_Store
.Rhistory
.RData
```

## Git and GitHub Setup

If user wants GitHub hosting:

1. Initialize git: `git init`
2. Create initial commit
3. Create repo: `gh repo create ORG/REPO --public --source=. --push`
4. Create gh-pages branch
5. Run `quarto publish gh-pages --no-prompt`
6. Provide the live URL

## Project CLAUDE.md

Create `.claude/CLAUDE.md` with:
- Project overview
- Book structure
- Publish workflow (`/publish`)
- Any project-specific notes

## Final Output

Tell the user:
- Project created at `path/to/project`
- Preview with `quarto preview`
- Publish with `/publish`
- Live URL (if GitHub Pages set up)
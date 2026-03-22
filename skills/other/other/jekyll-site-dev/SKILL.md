---
name: jekyll-site-dev
description: >
  Development reference for the alexgude.com Jekyll site. Use when modifying
  plugins in _plugins/, writing or editing content in _posts/ or _books/,
  working with the markdown output pipeline, book families, build validators,
  CI/CD configuration, or content authoring conventions (excerpts, Liquid
  tags, linking).
---

# Jekyll Site Development Reference

Detailed guides for specific subsystems. Read the relevant file when working
in that area.

## References

- **[CI/CD & Hooks](references/ci-cd-hooks.md)** — GitHub Actions pipeline,
  pre-commit hook behavior. Read when modifying CI workflows or commit hooks.

- **[Build Validators](references/build-validators.md)** — Validators that
  break the build on data errors. Read when adding a validator, debugging a
  `FatalException`, or understanding why a build failed.

- **[Markdown Output Pipeline](references/markdown-output.md)** — Generates
  `.md` files and `/llms.txt` from every page. Read when modifying
  `render_mode` behavior, markdown output assembly, or the llms.txt index.

- **[Book Families & `canonical_url`](references/book-families.md)** —
  Re-review workflow and canonical URL rules. Read when adding or modifying
  book reviews, especially re-reviews.

- **[Content Authoring](references/content-authoring.md)** — Excerpt rules,
  Liquid tag usage, linking conventions. Read when writing or editing blog
  posts or book reviews.

- **[Plugin Patterns](references/plugin-patterns.md)** — Tag structure,
  render mode branching, Finder/Renderer separation, LinkResolverSupport,
  error logging. Read when creating or modifying plugins.

- **[Testing](references/testing.md)** — test_helper.rb API, MockDocument
  vs RealDocLike, factory methods, common test patterns. Read when writing
  or debugging tests.

- **[Gotchas](references/gotchas.md)** — Non-obvious behaviors that cause
  subtle bugs (Document URL access, Page payload snapshot, cache pollution,
  canonical URL filtering). Read when debugging unexpected behavior.

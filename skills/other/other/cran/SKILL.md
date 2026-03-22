---
name: cran
description: >
  Full-arc CRAN submission workflow for R packages: preparation through
  post-acceptance. Use when: (1) Preparing a package for first CRAN submission,
  (2) Preparing a resubmission after rejection, (3) Running and interpreting
  R CMD check --as-cran output, (4) Writing or updating cran-comments.md,
  (5) Responding to CRAN reviewer feedback point-by-point, (6) Triaging
  ERRORs, WARNINGs, and NOTEs from R CMD check, (7) Verifying DESCRIPTION
  metadata, documentation, and URL compliance before submission.
---

# CRAN Submission

> **Surveyverse projects:** R CMD check targets (0 errors, 0 warnings, ≤2 notes),
> pre-approved notes, and `devtools::check()` cadence are defined in
> `r-package-conventions.md §3`. Those rules take precedence over generic guidance here.

## The four-stage arc

| Stage | What you're doing | Reference |
|-------|-------------------|-----------|
| **Prepare** | DESCRIPTION, docs, URLs, admin — the things `devtools::check()` won't catch | [preflight-checklist.md](references/preflight-checklist.md) |
| **Check** | `R CMD check --as-cran`, platform testing, NOTE triage | [check-and-triage.md](references/check-and-triage.md) |
| **Submit** | Build tarball, `devtools::submit_cran()`, write `cran-comments.md` | [submit-and-respond.md](references/submit-and-respond.md) |
| **Respond** | Point-by-point reviewer responses, resubmission | [submit-and-respond.md](references/submit-and-respond.md) |

## Tool map

| Task | Tool |
|------|------|
| Full local check | `devtools::check()` |
| CRAN-style check (fast iteration) | `devtools::check(args = "--as-cran")` |
| CRAN-style check (submission confidence) | `R CMD build .` then `R CMD check --as-cran pkg_x.y.z.tar.gz` |
| Docs and examples only | `devtools::check_man()` |
| Windows + R-devel | `devtools::check_win_devel()` |
| Multi-platform preflight | `rhub::check_for_cran()` |
| URL validation | `urlchecker::url_check()` |
| Submit to CRAN | `devtools::submit_cran()` |
| Generate release issue checklist | `usethis::use_release_issue()` |
| Create `cran-comments.md` | `usethis::use_cran_comments()` |
| Create `NEWS.md` | `usethis::use_news_md()` |
| Bump version | `usethis::use_version()` |

## The CRAN mindset

CRAN checks run in a **minimal, non-interactive environment** with no hidden
dependencies. Write code as if:

- There is no network access during checks (examples, tests, vignettes)
- Nothing is written outside `tempdir()`
- There are no interactive prompts
- Examples run in a few seconds each — not minutes
- No binary executables are bundled in the source package

Prefer fixes that make checks green everywhere over explanations that justify
fragility.

## ERROR / WARNING / NOTE triage

- **ERRORs**: Always blockers. Fix before submission.
- **WARNINGs**: Almost always blockers. Very rare contextual exceptions.
- **NOTEs**: Split into two types:
  - *Actionable* — fix it (undeclared dependency, broken URL, too-long examples)
  - *Contextual* — explain in `cran-comments.md` (incoming feasibility NOTE on new submissions)

When keeping a NOTE, `cran-comments.md` must answer:

1. What is the NOTE?
2. Why does it happen?
3. Why is it safe / expected?
4. What did you do to minimize it?

## Quality gate (recommended order)

1. `devtools::check()` is clean — 0 errors, 0 warnings
2. Preflight checklist complete — see [preflight-checklist.md](references/preflight-checklist.md)
3. Tarball check: `R CMD build .` → `R CMD check --as-cran pkg_x.y.z.tar.gz`
4. Cross-platform: `devtools::check_win_devel()` at minimum; R-hub for broader coverage
5. `cran-comments.md` written and reviewed
6. Ready to respond point-by-point if CRAN asks

## High-frequency failure surfaces

- **DESCRIPTION metadata**: Title case, forbidden phrases, missing `cph` role
- **Documentation**: Missing `@return` or `@examples` on exported functions
- **Examples**: network calls, unseeded randomness, writes outside tempdir, commented-out code
- **URLs**: HTTP instead of HTTPS, redirecting links
- **Undeclared dependencies**: packages used in code/examples/tests but absent from DESCRIPTION
- **Package size / runtime**: large embedded data, slow vignettes or examples

## External resources

- CRAN policy: https://cran.r-project.org/web/packages/policies.html
- CRAN submission checklist: https://cran.r-project.org/web/packages/submission_checklist.html
- Writing R Extensions (R CMD check): https://cran.r-project.org/doc/manuals/r-release/R-exts.html
- R Packages (2e) — releasing to CRAN: https://r-pkgs.org/release.html
- win-builder: https://win-builder.r-project.org/
- macbuilder: https://mac.r-project.org/macbuilder/submit.html

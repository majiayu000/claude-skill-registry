---
name: add-docs-entry
description: Use when adding user-facing documentation entries to the flight-rules guide — covers the Guide DSL, screenshot patterns, multi-user perspectives, CLI registration, and verification
user-invocable: false
---

# Adding Documentation Entries

Add flight-rules-style entries to the "Using PromptGrimoire" guide. Each entry answers a first-person question with actionable steps and Playwright-captured screenshots.

## Files You Will Touch

| File | Purpose |
|------|---------|
| `src/promptgrimoire/docs/scripts/using_promptgrimoire.py` | Guide script — add entry functions here |
| `docs/guides/using-promptgrimoire.md` | Generated output — never edit directly |
| `docs/guides/screenshots/` | Generated screenshots — never edit directly |
| `src/promptgrimoire/docs/guide.py` | Guide DSL (read-only reference) |
| `src/promptgrimoire/docs/seed.py` | DB seeding helpers for guide scripts |

## Before Writing: Screenshot Economy

**Every screenshot costs build time and reader attention.** Before adding a screenshot entry, audit what already exists.

### Decision Process

1. **Read the existing guide** (`docs/guides/using-promptgrimoire.md`) and list every screenshot that already shows the page or element you want to capture
2. **Ask: does an existing screenshot already show this?** If the Publish button is on the same Unit Settings page that another entry already screenshots, you don't need a new one — cross-link instead
3. **Ask: does the other perspective already exist?** If an entry already shows the student Navigator with a Start button, don't re-screenshot it from the student side just because your entry mentions students
4. **Only capture when something genuinely new is shown** — a UI element, state, or indicator that no existing screenshot covers

### When to Use `text_only=True` Instead

Use text-only when your entry's visual content is already captured elsewhere. Cross-link to the existing screenshot:

```python
def _entry_publish_workflow(guide: Guide) -> None:
    """I want to make my activity visible to students."""
    with guide.step(
        "I want to make my activity visible to students", level=3, text_only=True
    ) as g:
        g.note("Unpublished weeks are invisible to students. ...")
        g.note(
            "See [I've enrolled students. What happens next?]"
            "(#ive-enrolled-students-what-happens-next) "
            "for what the student sees after publishing."
        )
```

### When a New Screenshot IS Justified

- A UI element or indicator that **no existing entry shows** (e.g. an expansion panel that only appears in certain states)
- A **different state** of an already-shown page (e.g. the page looks materially different because of a toggle or mode)
- A **different user role** seeing something role-specific that hasn't been captured (e.g. admin-only controls)

**The default is text-only with cross-links. Screenshots are the exception, not the rule.**

## Entry Function Pattern

Every entry is a standalone function. Name it `_entry_<slug>`. Choose the right signature based on what the entry needs:

```python
# Text-only (no browser interaction needed)
def _entry_my_topic(guide: Guide) -> None:

# Needs browser (screenshots from current user)
def _entry_my_topic(page: Page, base_url: str, guide: Guide) -> None:

# Needs Unit Settings page
def _entry_my_topic(page: Page, base_url: str, course_url: str, guide: Guide) -> None:

# Needs browser + course URL (for instructor views)
def _entry_my_topic(page: Page, course_url: str, guide: Guide) -> None:
```

### Text-Only Entry (No Screenshots)

```python
def _entry_explanation(guide: Guide) -> None:
    """First-person question or statement — becomes the heading."""
    with guide.step(
        "What does 'Students with no work' mean?", level=3, text_only=True
    ) as g:
        g.note("Explanation paragraph.")
        g.note("**Diagnosis:** What the indicator means.")
        g.note("**Fix:** What to do about it.")
```

### Entry With Screenshots

```python
def _entry_feature(page: Page, base_url: str, guide: Guide) -> None:
    """I want to do the thing."""
    with guide.step("I want to do the thing", level=3) as g:
        g.note("Navigate to the page and do the thing.")

        # Navigate and wait for element
        _authenticate(page, base_url, "instructor@uni.edu")
        page.goto(f"{base_url}/courses")
        page.locator('[data-testid="my-element"]').wait_for(
            state="visible", timeout=10000
        )

        # Capture with highlight on specific test IDs
        g.screenshot(
            "Description of what the screenshot shows",
            highlight=["my-element"],  # data-testid values to highlight
        )

        g.note("Explanation of what happened.")
```

**Key rules:**
- `guide.step(..., text_only=True)` suppresses auto-screenshot on exit
- Without `text_only=True`, a screenshot auto-captures if you didn't take one explicitly
- `highlight=["foo"]` draws a red border around `[data-testid="foo"]` elements
- `focus="foo"` scrolls to `[data-testid="foo"]` before capture
- Screenshots are numbered automatically per guide (01, 02, ...)

### Multi-User Screenshots

Switch users with `_authenticate()` to show different perspectives:

```python
def _entry_multi_perspective(
    page: Page, base_url: str, course_url: str, guide: Guide
) -> None:
    """Entry showing both instructor and student views."""
    with guide.step("I want to show both views", level=3) as g:
        # Instructor view
        _authenticate(page, base_url, "instructor@uni.edu")
        page.goto(course_url)
        page.locator('[data-testid="indicator"]').wait_for(
            state="visible", timeout=10000
        )
        g.screenshot(
            "Instructor sees the indicator in Unit Settings",
            highlight=["indicator"],
        )

        g.note("From the student side, this is what they see:")

        # Student view
        _authenticate(page, base_url, "student-demo@test.example.edu.au")
        page.locator('[data-testid^="start-activity-btn"]').first.wait_for(
            state="visible", timeout=10000
        )
        g.screenshot("Student sees Start button on Navigator")
```

**Available test users** (seeded by earlier guide scripts):
- `instructor@uni.edu` — instructor, enrolled in UNIT1234
- `student-demo@test.example.edu.au` — student, enrolled in UNIT1234
- `fresh-student@test.example.edu.au` — student with no workspaces yet

To create a new user: `seed_user_and_enrol("email", "Display Name")` (from `promptgrimoire.docs.seed`).

## Registering Your Entry

### 1. Add to the runner function

Entries are called from `_run_screenshot_sections()` or `_run_management_sections()` at the bottom of `using_promptgrimoire.py`. Place your entry in the correct domain section:

```python
def _run_management_sections(...) -> None:
    # ...existing sections...
    guide.section("Enrolment")
    _entry_enrol_students(page, course_url, guide)
    _entry_after_enrolment(page, base_url, guide)
    _entry_my_new_entry(page, base_url, guide)  # <-- add here
```

### 2. Domain sections (existing)

| Runner | Sections |
|--------|----------|
| `_run_screenshot_sections` | Getting Started, Workspaces, Tags, Annotating, Organising, Responding, Export |
| `_run_management_sections` | Unit Settings, Enrolment, Housekeeping, Navigation, Sharing & Collaboration, Content Input |

To add a new domain section: `guide.section("New Domain")` before the first entry.

### 3. No CLI changes needed for entries

`using-promptgrimoire.md` is NOT in `_GENERATED_GUIDE_MARKDOWN` (in `cli/docs.py`) — that tuple only lists guides included in PDF generation. The flight-rules guide is generated as part of the docs build but not PDF'd. You only need to touch `cli/docs.py` if adding an entirely new guide script.

## Verification

After adding entries, run:

```bash
uv run grimoire docs build
```

This:
1. Starts NiceGUI with a test database
2. Runs all guide scripts (instructor, student, personal grimoire, using-promptgrimoire) in sequence via Playwright
3. Captures screenshots
4. Generates markdown in `docs/guides/`
5. Builds the MkDocs site

**Check the output:**
- `docs/guides/using-promptgrimoire.md` — your entry text appears under the correct section
- `docs/guides/screenshots/` — your screenshots exist (named `using-promptgrimoire-NN.png`)
- No Playwright timeouts or missing element errors

## Entry Style Guide

### Headings

First-person questions or statements:
- Happy path: "I want to..." / "How do I..."
- Problem: "Why is..." / "I can't..." / "What does ... mean?"
- Orientation: "How do I know if..."

### Body Structure

- **Happy path**: Context paragraph, screenshot, explanation, cross-link to sequential guide
- **Problem/diagnosis**: `**Diagnosis:**` block, `**Fix:**` block, optional screenshot
- **Orientation**: Explanation with visual indicators described

### Cross-links

Link to sequential guides with relative markdown paths and anchor fragments:

```python
g.note(
    "See [Instructor Setup - Step 6]"
    "(instructor-setup.md#step-6-enrolling-students) "
    "for how instructors add students."
)
```

### Waits

**Never use `page.wait_for_timeout()`** — always wait for a visible element:

```python
# WRONG
page.wait_for_timeout(2000)

# RIGHT
page.locator('[data-testid="my-element"]').wait_for(state="visible", timeout=10000)
```

## Checklist

Before considering an entry complete:

- [ ] **Screenshot audit done** — read existing guide, confirmed no existing screenshot covers this content
- [ ] `text_only=True` used when existing screenshots already cover the visual content (cross-link instead)
- [ ] Function named `_entry_<slug>` with docstring matching the heading
- [ ] Registered in the correct runner function under the right section
- [ ] Screenshots (if any) use `highlight=` to draw attention to relevant elements
- [ ] No `wait_for_timeout` calls — condition-based waits only
- [ ] `uv run grimoire docs build` succeeds
- [ ] Generated markdown contains the entry with correct heading level (`###`)
- [ ] Screenshots (if any) render correctly (check `docs/guides/screenshots/`)

---
name: typst-test-slide
description: "This skill should be used when the user asks to 'test a slide', 'isolate a slide', 'debug a slide', 'preview a single slide', 'test this slide', 'render one slide', or when you need to visually verify a single Typst slide from a presentation in isolation. Provides the exact file setup pattern to avoid access-denied and import errors."
---

# Typst Test Slide - Isolate and Render a Single Slide

Renders a single Typst slide in isolation for debugging or visual verification. This is a recipe, not a workflow.

## Why This Exists

Typst cannot access files outside its project root. Creating test files in `/tmp/` causes "access denied" on every `#import` and `#image()` call. This skill provides the correct pattern.

## Common Errors This Prevents

| Error | Cause | Fix |
|-------|-------|-----|
| `access denied` on `#import "../templates/theme.typ"` | Test file is in `/tmp/` (outside project root) | Put test file in `output/` inside the project |
| `access denied` on `#image(...)` | Image path resolves outside project root | Use `../assets/` from `output/` directory |
| `file not found` on `#import "../../templates/theme.typ"` | Wrong relative depth (used sub-slide depth instead of `output/` depth) | `output/` is one level deep: use `../templates/`, not `../../templates/` |
| Slides don't render (just text) | Missing `#show: university-theme.with(...)` preamble | Include the full preamble (see template below) |

## The Pattern

### 1. Create the test file in `output/`

```bash
cat > output/test-slide.typ << 'EOF'
#import "../templates/theme.typ": *
#show: university-theme.with(
  aspect-ratio: "16-9",
  config-info(
    title: [Test],
    author: [Test],
    date: datetime.today(),
    institution: [UVA],
    logo: image("../assets/LawP_horizontal_short_4c_RGB.png"),
  ),
)

#slide[
// paste slide content here
]
EOF
```

### 2. Compile with `--root .` from project root

```bash
tinymist compile --root . output/test-slide.typ /tmp/test-slide.png --ppi 144
```

The `--root .` flag tells Typst that the project root is the current directory, so `../templates/` from `output/` resolves correctly.

### 3. Clean up

```bash
rm -f output/test-slide.typ
```

## Key Rules

- **Always create in `output/`**, never `/tmp/` or any directory outside the project root.
- **Always compile with `--root .`** from the project root directory.
- **Paths from `output/` go up one level**: `../templates/`, `../assets/`.
- **Paths from `slides/XX-topic/` go up two levels**: `../../templates/`, `../../assets/` -- do not confuse these depths.
- **Delete the test file when done.** `output/` is gitignored but keeping test files around causes confusion.

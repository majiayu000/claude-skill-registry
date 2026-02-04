---
name: brand-yml
description: >
  Create and use brand.yml files for consistent branding across Shiny apps and Quarto documents.
  Use when working with brand styling, colors, fonts, logos, or corporate identity in Shiny or
  Quarto projects. Covers: (1) Creating new _brand.yml files from brand guidelines, (2) Applying
  brand.yml to Shiny for R apps with bslib, (3) Applying brand.yml to Shiny for Python apps with
  ui.Theme, (4) Using brand.yml in Quarto documents, presentations, dashboards, and PDFs, (5)
  Modifying existing brand.yml files, (6) Troubleshooting brand integration issues. Includes
  complete specifications and framework-specific integration guides.
---

# brand.yml Skill

Create and use `_brand.yml` files for consistent branding across Shiny applications and Quarto documents.

## What is brand.yml?

brand.yml is a YAML-based format that translates brand guidelines into a machine-readable file usable across Shiny and Quarto. A single `_brand.yml` file defines:

- **Colors** - Palette and semantic colors (primary, success, warning, etc.)
- **Typography** - Fonts, sizes, weights, line heights
- **Logos** - Multiple sizes and light/dark variants
- **Meta** - Company name, links, identity information

## File Naming Convention

- **Standard name**: `_brand.yml` (auto-discovered by Shiny and Quarto)
- **Custom names**: Any name like `company-brand.yml` (requires explicit paths)
- **Location**: Typically at project root, or in `_brand/` or `brand/` subdirectories

## Decision Tree

Determine the user's goal and follow the appropriate workflow:

1. **Creating a new _brand.yml file?** → Follow "Creating brand.yml Files"
2. **Using brand.yml in Shiny for R?** → Read `references/shiny-r.md`
3. **Using brand.yml in Shiny for Python?** → Read `references/shiny-python.md`
4. **Using brand.yml in Quarto?** → Read `references/quarto.md`
5. **Using brand.yml in R (general)?** → Read `references/brand-yml-in-r.md` (R Markdown, theming functions, programmatic access)
6. **Modifying existing _brand.yml?** → Follow "Modifying Existing Files"
7. **Troubleshooting integration?** → Follow "Troubleshooting"

## Creating brand.yml Files

When creating `_brand.yml` files from brand guidelines:

### Step 1: Gather Information

Collect brand information:
- **Colors**: Primary, secondary, accent colors with hex values
- **Fonts**: Font families and where they're sourced (Google Fonts, local files, etc.)
- **Logos**: Logo file paths or URLs for different sizes
- **Company info**: Name, website, social links (optional)

### Step 2: Read the Specification

Load `references/brand-yml-spec.md` to understand the complete brand.yml structure, field options, and syntax.

### Step 3: Build the File Incrementally

Start with the essential sections and add optional elements:

**Minimum viable _brand.yml:**

```yaml
color:
  palette:
    brand-blue: "#0066cc"
  primary: brand-blue
  background: "#ffffff"

typography:
  fonts:
    - family: Inter
      source: google
      weight: [400, 600]
  base: Inter
```

**Add colors as needed:**

```yaml
color:
  palette:
    brand-blue: "#0066cc"
    brand-orange: "#ff6600"
    brand-gray: "#666666"
  primary: brand-blue
  secondary: brand-gray
  warning: brand-orange
  foreground: "#333333"
  background: "#ffffff"
```

**Add typography details:**

```yaml
typography:
  fonts:
    - family: Inter
      source: google
      weight: [400, 600, 700]
      style: [normal, italic]
    - family: Fira Code
      source: google
      weight: [400, 500]
  base:
    family: Inter
    size: 16px
    line-height: 1.5
  headings:
    family: Inter
    weight: 600
  monospace: Fira Code
```

**Add logos:**

```yaml
logo:
  small: logos/icon.png
  medium: logos/header.png
  large: logos/full.svg
```

**Add meta information:**

```yaml
meta:
  name: Company Name
  link: https://example.com
```

### Step 4: Apply Best Practices

Follow these rules from `references/brand-yml-spec.md`:

- All fields are optional - only include what's needed
- Use hex color format: `"#0066cc"`
- Prefer simple syntax (strings over objects) when possible
- Use lowercase names with hyphens: `brand-blue`, `success-green`
- Include `https://` in all URLs
- Define colors/fonts before referencing them
- For color ranges (shades/tints), choose the midpoint color

### Step 5: Validate Structure

Check that:
- YAML syntax is valid (proper indentation, quotes on hex colors)
- Color references match palette names
- Font families are defined before use
- File paths are relative to `_brand.yml` location
- All URLs include protocol (`https://`)

## Modifying Existing Files

When modifying existing `_brand.yml` files:

1. **Read the current file** to understand existing structure
2. **Consult brand-yml-spec.md** for valid field options
3. **Maintain consistency** with existing naming patterns
4. **Preserve references** - if other colors/elements reference a name, update consistently
5. **Test integration** - verify changes apply correctly in Shiny/Quarto

Common modifications:
- **Adding colors**: Add to `color.palette`, then reference in semantic colors
- **Changing fonts**: Update in `typography.fonts`, ensure weights/styles are available
- **Adding logo variants**: Use `light`/`dark` structure for multiple variants
- **Light/dark mode**: Add `light` and `dark` variants to colors

## Using with Shiny for R

When the user wants to apply brand.yml to a Shiny for R app:

1. **Read `references/shiny-r.md`** for complete integration guide
2. **Key function**: `bs_theme(brand = TRUE)` or `bs_theme(brand = "path")`
3. **Automatic discovery**: Place `_brand.yml` at app root
4. **Page functions**: Works with `page_fluid()`, `page_sidebar()`, etc.

Quick example:

```r
library(shiny)
library(bslib)

ui <- page_fluid(
  theme = bs_theme(brand = TRUE),
  # ... UI elements
)
```

## Using with Shiny for Python

When the user wants to apply brand.yml to a Shiny for Python app:

1. **Read `references/shiny-python.md`** for complete integration guide
2. **Key function**: `ui.Theme.from_brand(__file__)`
3. **Automatic discovery**: Place `_brand.yml` at app root
4. **Installation**: Requires `pip install "shiny[theme]"`

Quick example (Shiny Express):

```python
from shiny.express import ui

ui.page_opts(theme=ui.Theme.from_brand(__file__))
```

Quick example (Shiny Core):

```python
from shiny import App, ui

app_ui = ui.page_fluid(
    theme=ui.Theme.from_brand(__file__),
    # ... UI elements
)
```

## Using with Quarto

When the user wants to apply brand.yml to Quarto documents:

1. **Read `references/quarto.md`** for complete integration guide
2. **Automatic discovery**: Place `_brand.yml` at project root with `_quarto.yml`
3. **Supported formats**: HTML, dashboards, RevealJS, Typst PDFs
4. **Theme layering**: Use `brand` keyword to control precedence

Quick example (document):

```yaml
---
title: "My Document"
format:
  html:
    brand: _brand.yml
---
```

Quick example (project in `_quarto.yml`):

```yaml
project:
  brand: _brand.yml

format:
  html:
    theme: default
```

## Troubleshooting

### Brand Not Applying

**Shiny:**
- Verify file is named `_brand.yml` (with underscore)
- Check file location (app directory or parent directories)
- Try explicit path: `bs_theme(brand = "path/to/_brand.yml")` or `ui.Theme.from_brand("path")`
- For Python: Ensure `libsass` is installed

**Quarto:**
- Verify `_brand.yml` is at project root
- Ensure `_quarto.yml` exists for project-level branding
- Try explicit path in document frontmatter
- Check theme layering order if using custom themes

### Colors Not Matching

- Ensure hex colors have quotes: `"#0066cc"` not `#0066cc`
- Verify color names match palette definitions exactly
- Check semantic colors (primary, success, etc.) reference valid palette names
- Ensure palette is defined before semantic colors

### Fonts Not Loading

- Verify Google Fonts spelling and availability
- Check internet connection (required for Google Fonts)
- Ensure `source: google` or `source: bunny` is specified
- Verify font family names match exactly in typography elements
- For Typst: Check font cache with `quarto typst fonts`

### YAML Syntax Errors

- Check indentation (use spaces, not tabs)
- Ensure hex colors have quotes: `"#447099"`
- Verify colons have space after them: `primary: blue`
- Check list items have hyphens: `- family: Inter`
- Use YAML validator if syntax issues persist

## Reference Documentation

Load these as needed for detailed information:

- **`references/brand-yml-spec.md`**: Complete brand.yml specification with all sections, fields, examples, and validation rules
- **`references/shiny-r.md`**: Using brand.yml with Shiny for R via bslib (bs_theme, automatic discovery, Shiny-specific integration)
- **`references/shiny-python.md`**: Using brand.yml with Shiny for Python via ui.Theme (from_brand(), installation, performance)
- **`references/quarto.md`**: Using brand.yml with Quarto (formats, light/dark mode, layering, extensions, Typst)
- **`references/brand-yml-in-r.md`**: General R usage including R Markdown integration, theming functions (ggplot2, gt, flextable, plotly, thematic), and programmatic brand access

## Key Principles

- **Start simple**: Begin with colors and one font family
- **Keep it concise**: Only include fields directly relevant to the brand
- **Prefer standard names**: Use Bootstrap color names when possible (blue, green, red, etc.)
- **Use automatic discovery**: Name file `_brand.yml` for auto-detection
- **Test across targets**: Verify brand applies correctly in all intended formats
- **Version control**: Include `_brand.yml` in git repository

## Common Patterns

### Light/Dark Mode Colors

```yaml
color:
  primary:
    light: "#0066cc"
    dark: "#3399ff"
  background:
    light: "#ffffff"
    dark: "#1a1a1a"
  foreground:
    light: "#333333"
    dark: "#e0e0e0"
```

Light/dark color modes were added in Quarto version 1.8 and currently are not supported in the R or Python brand.yml packages.

### Logo Variants

```yaml
logo:
  images:
    logo-dark: logos/logo-dark.svg
    logo-white: logos/logo-white.svg
    icon: logos/icon.png
  small: icon
  medium:
    light: logo-dark
    dark: logo-white
```

### Multiple Font Weights

```yaml
typography:
  fonts:
    - family: Inter
      source: google
      weight: [300, 400, 500, 600, 700]
      style: [normal, italic]
  base:
    family: Inter
    weight: 400
  headings:
    family: Inter
    weight: 600
```

### Color Aliases

```yaml
color:
  palette:
    navy: "#003366"
    ocean-blue: "#0066cc"
    sky-blue: "#3399ff"
    primary-color: ocean-blue  # Alias
    brand-blue: ocean-blue     # Alias
    blue: sky-blue             # Alias for primary colors
  primary: brand-blue
```

Include Bootstrap color names when possible, either defined directly or as aliases: `blue`, `indigo`, `purple`, `pink`, `red`, `orange`, `yellow`, `green`, `teal`, `cyan`, `white`, `black`. This is useful for consistency and these colors are picked up automatically by tools that use brand.yml.

## Tips

- **Read specification first**: Always consult `brand-yml-spec.md` when creating or modifying files
- **Framework-specific guides**: Load the appropriate reference (shiny-r.md, shiny-python.md, quarto.md) for integration details
- **Validate incrementally**: Start with minimal structure, test, then add complexity
- **Use references**: Define colors in palette, then reference by name in semantic colors
- **Standard file name**: Use `_brand.yml` for automatic discovery
- **Explicit paths**: Use custom file names only when necessary (shared branding, multiple variants)

---
name: shiny-bslib-theming
description: Advanced theming for Shiny apps using bslib and Bootstrap 5. Use when customizing app appearance with bs_theme(), Bootswatch themes, custom colors, typography, brand.yml integration, Bootstrap Sass variables, custom Sass/CSS rules, dark mode and color modes, dynamic theme switching, real-time theming, theme inspection, or making R plots match the app theme with thematic.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Theming Shiny Apps with bslib

Customize Shiny app appearance using bslib's Bootstrap 5 theming system. From quick Bootswatch themes to advanced Sass customization and dynamic color mode switching.

## Quick Start

**"shiny" preset (recommended starting point):**
```r
page_sidebar(
  theme = bs_theme(),  # "shiny" preset by default — polished, not plain Bootstrap
  ...
)
```

**Bootswatch theme (for a different visual style):**
```r
page_sidebar(
  theme = bs_theme(preset = "zephyr"),  # or "cosmo", "minty", "darkly", etc.
  ...
)
```

**Custom colors and fonts:**
```r
page_sidebar(
  theme = bs_theme(
    version = 5,
    bg = "#FFFFFF",
    fg = "#333333",
    primary = "#2c3e50",
    base_font = font_google("Lato"),
    heading_font = font_google("Montserrat")
  ),
  ...
)
```

**Auto-brand from `_brand.yml`:**
If a `_brand.yml` file exists in your app or project directory, `bs_theme()` automatically discovers and applies it. No code changes needed. Requires the `brand.yml` R package.

```r
bs_theme(brand = FALSE)    # Disable auto-discovery
bs_theme(brand = TRUE)     # Require _brand.yml (error if not found)
bs_theme(brand = "path/to/brand.yml")  # Explicit path
```

## Theming Workflow

1. Start with the `"shiny"` preset (default) or a Bootswatch theme close to your desired look
2. Customize main colors (`bg`, `fg`, `primary`)
3. Adjust fonts with `font_google()` or other font helpers
4. Fine-tune with Bootstrap Sass variables via `...` or `bs_add_variables()`
5. Add custom Sass rules with `bs_add_rules()` if needed
6. Enable `thematic::thematic_shiny()` so plots match the theme
7. Use `bs_themer()` during development for interactive preview

**Example:**
```r
theme <- bs_theme(preset = "minty") |>
  bs_theme_update(
    primary = "#1a9a7f",
    base_font = font_google("Lato")
  ) |>
  bs_add_rules("
    .card { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
  ")
```

## bs_theme()

Central function for creating Bootstrap themes. Returns a `sass::sass_bundle()` object.

```r
bs_theme(
  version = version_default(),
  preset = NULL,        # "shiny" (default for BS5+), "bootstrap", or Bootswatch name
  ...,                  # Bootstrap Sass variable overrides
  brand = NULL,         # brand.yml: NULL (auto), TRUE (require), FALSE (disable), or path
  bg = NULL, fg = NULL,
  primary = NULL, secondary = NULL,
  success = NULL, info = NULL, warning = NULL, danger = NULL,
  base_font = NULL, code_font = NULL, heading_font = NULL,
  font_scale = NULL,    # Scalar multiplier for base font size (e.g., 1.5 = 150%)
  bootswatch = NULL     # Alias for preset
)
```

Use `bs_theme_update(theme, ...)` to modify an existing theme. Use `is_bs_theme(x)` to test if an object is a theme.

### Presets and Bootswatch

**The "shiny" preset (recommended):** `bs_theme()` defaults to `preset = "shiny"` for Bootstrap 5+. This is a polished, purpose-built theme designed specifically for Shiny apps — it is **not** plain Bootstrap. It provides professional styling with well-chosen defaults for cards, sidebars, value boxes, and other bslib components. Start here and customize with colors and fonts before reaching for a Bootswatch theme.

**Vanilla Bootstrap:** Use `preset = "bootstrap"` to remove the "shiny" preset and get unmodified Bootstrap 5 styling.

**Built-in presets:** `builtin_themes()` lists bslib's own presets.

**Bootswatch themes:** `bootswatch_themes()` lists all available Bootswatch themes. Choose one that fits the app's purpose and audience — don't apply one by default.

Popular options: `"zephyr"` (light, modern), `"cosmo"` (clean), `"minty"` (fresh green), `"flatly"` (flat design), `"litera"` (crisp), `"darkly"` (dark), `"cyborg"` (dark), `"simplex"` (minimalist), `"sketchy"` (hand-drawn).

### Main Colors

The most influential colors — changing these affects **hundreds** of CSS rules via variable cascading:

| Parameter | Description |
|---|---|
| `bg` | Background color |
| `fg` | Foreground (text) color |
| `primary` | Primary brand color (links, nav active states, input focus) |
| `secondary` | Default for action buttons |
| `success` | Positive/success states (typically green) |
| `info` | Informational content (typically blue-green) |
| `warning` | Warnings (typically yellow) |
| `danger` | Errors/destructive actions (typically red) |

```r
bs_theme(
  bg = "#202123", fg = "#B8BCC2",
  primary = "#EA80FC", secondary = "#48DAC6"
)
```

**Color tips:**
- `bg`/`fg`: similar hue, large luminance difference (ensure contrast for readability)
- `primary`: contrasts with both `bg` and `fg`; used for hyperlinks, navigation, input focus
- Colors can be any format `htmltools::parseCssColors()` understands

### Typography

Three font arguments: `base_font`, `heading_font`, `code_font`. Use `font_scale` to uniformly scale all font sizes (e.g., `1.5` for 150%).

Each argument accepts a single font, a `font_collection()`, or a character vector of font names.

#### font_google()

Downloads and caches Google Fonts locally (`local = TRUE` by default). Internet needed only on first download.

```r
bs_theme(
  base_font = font_google("Roboto"),
  heading_font = font_google("Montserrat"),
  code_font = font_google("Fira Code")
)
```

With variable weights: `font_google("Crimson Pro", wght = "200..900")`

With specific weights: `font_google("Raleway", wght = c(300, 400, 700))`

**Recommend fallbacks** to avoid Flash of Invisible Text (FOIT) on slow connections:
```r
bs_theme(
  base_font = font_collection(
    font_google("Lato", local = FALSE),
    "Helvetica Neue", "Arial", "sans-serif"
  )
)
```

Font pairing resource: fontpair.co

#### font_link()

CSS web font interface for custom font URLs:
```r
font_link("Crimson Pro",
  href = "https://fonts.googleapis.com/css2?family=Crimson+Pro:wght@200..900")
```

#### font_face()

For locally hosted font files with full `@font-face` control:
```r
font_face(
  family = "Crimson Pro",
  style = "normal",
  weight = "200 900",
  src = "url(fonts/crimson-pro.woff2) format('woff2')"
)
```

#### font_collection()

Combine multiple fonts with fallback order:
```r
font_collection(font_google("Lato"), "Helvetica Neue", "Arial", "sans-serif")
```

## Low-Level Theming Functions

For customizations beyond `bs_theme()`'s named parameters. These work directly with Bootstrap's Sass layers.

### bs_add_variables()

Add or override Bootstrap Sass variable defaults:

```r
theme <- bs_add_variables(
  bs_theme(preset = "sketchy", primary = "orange"),
  "body-bg" = "#EEEEEE",
  "font-family-base" = "monospace",
  "font-size-base" = "1.4rem",
  "btn-padding-y" = ".16rem"
)
```

**The `.where` parameter** controls placement in the Sass compilation order:

| `.where` | When to use |
|---|---|
| `"defaults"` (default) | Set variable defaults with `!default` flag. Placed **before** Bootstrap's own defaults. |
| `"declarations"` | Reference other Bootstrap variables (e.g., `$secondary`). Placed **after** Bootstrap's defaults. |
| `"rules"` | Placed after all rules. Rarely needed. |

**Referencing Bootstrap variables:**
```r
# This fails in bs_theme() because $secondary isn't defined yet:
# bs_theme("progress-bar-bg" = "$secondary")

# Use bs_add_variables with .where = "declarations" instead:
bs_theme() |>
  bs_add_variables("progress-bar-bg" = "$secondary", .where = "declarations")
```

### bs_add_rules()

Add custom Sass/CSS rules that can reference Bootstrap variables and mixins:

```r
theme <- bs_theme(primary = "#007bff") |>
  bs_add_rules("
    .custom-card {
      background: mix($bg, $primary, 95%);
      border: 1px solid $primary;
      padding: $spacer;

      @include media-breakpoint-up(md) {
        padding: $spacer * 2;
      }
    }
  ")
```

From external file: `bs_add_rules(sass::sass_file("www/custom.scss"))`

Available Sass functions: `lighten()`, `darken()`, `mix()`, `rgba()`, `color-contrast()`.
Available Bootstrap mixins: `@include media-breakpoint-up()`, `@include box-shadow()`, `@include border-radius()`.

### bs_add_functions() and bs_add_mixins()

Add custom Sass functions or mixins to the theme bundle:

```r
theme |>
  bs_add_functions("@function my-tint($color) { @return mix(white, $color, 20%); }") |>
  bs_add_rules(".highlight { background: my-tint($primary); }")
```

### bs_bundle()

Append `sass::sass_bundle()` objects to a theme (for packaging reusable theme extensions):

```r
my_extension <- sass::sass_layer(
  defaults = list("my-var" = "red !default"),
  rules = ".my-class { color: $my-var; }"
)
theme <- bs_theme() |> bs_bundle(my_extension)
```

## Bootstrap Sass Variables

Pass any Bootstrap 5 Sass variable through `bs_theme(...)` or `bs_add_variables()`.

**Finding variable names:** https://rstudio.github.io/bslib/articles/bs5-variables/

**Common variables:**
```r
bs_theme(
  "border-radius" = "0.5rem",
  "card-border-radius" = "1rem",
  "card-bg" = "lighten($bg, 5%)",
  "navbar-bg" = "$primary",
  "link-color" = "$primary",
  "font-size-base" = "1rem",
  "spacer" = "1rem",
  "btn-padding-y" = ".5rem",
  "btn-padding-x" = "1rem",
  "input-border-color" = "#dee2e6"
)
```

Values can be Sass expressions referencing variables, functions, and math.

## Bootstrap CSS Custom Properties

See [sass-and-css-variables.md](references/sass-and-css-variables.md) for details on:

- How Sass variables compile into `--bs-*` CSS custom properties
- Runtime vs compile-time variable layers
- How Bootstrap 5.3 color modes use CSS variable overrides
- Per-element theming with `data-bs-theme`
- CSS utility classes for one-off styling

## Dark Mode and Color Modes

See [dark-mode.md](references/dark-mode.md) for details on:

- Bootstrap 5.3's client-side color mode system (`data-bs-theme` attribute)
- `input_dark_mode()` and `toggle_dark_mode()` for user-controlled switching
- Server-side theme switching with `session$setCurrentTheme()`
- Writing custom Sass that works across light/dark modes
- Component compatibility (what responds to theming, what doesn't)

## Theming R Plots

`bs_theme()` only affects CSS. R plot output (rendered server-side as images) won't auto-match. Use the `thematic` package:

```r
library(thematic)
thematic_shiny(font = "auto")  # Call before shinyApp()
shinyApp(ui, server)
```

- Works with base R, ggplot2, and lattice
- Translates CSS colors into R plotting defaults
- `font = "auto"` also matches fonts from `bs_theme()`
- Complements `bs_themer()` for real-time preview

Set global ggplot2 theme for further consistency:
```r
library(ggplot2)
theme_set(theme_minimal())
```

## Dashboard Background Styling

The `bslib-page-dashboard` CSS class adds a light gray background behind the main content area, giving dashboard-style apps a polished look where cards stand out against the background. This is a theming detail — it doesn't change layout behavior, only the visual treatment.

**For `page_sidebar()` dashboards:**
```r
page_sidebar(
  class = "bslib-page-dashboard",
  title = "My Dashboard",
  sidebar = sidebar(...),
  ...
)
```

**For `page_navbar()` with dashboard-focused pages:**
Apply the class to individual `nav_panel()` containers (not `page_navbar()` itself) so only dashboard-oriented pages get the gray background:
```r
page_navbar(
  title = "Analytics",
  nav_panel("Dashboard", class = "bslib-page-dashboard",
    layout_column_wrap(...)
  ),
  nav_panel("Report",
    # No dashboard class — standard white background for prose/reports
    ...
  )
)
```

## Interactive Theming Tools

### bs_theme_preview()

Standalone demo app for previewing a theme with many example UI components:

```r
bslib::bs_theme_preview()                        # Default theme
bslib::bs_theme_preview(bs_theme(preset = "darkly"))  # Custom theme
```

Includes the theming UI by default (`with_themer = TRUE`).

### run_with_themer()

Run an existing Shiny app with the theme editor overlay (instead of `shiny::runApp()`):

```r
run_with_themer(shinyApp(ui, server))
run_with_themer("path/to/app")
```

### bs_themer()

Add the theme editor to your own app's server function:

```r
server <- function(input, output, session) {
  bs_themer()  # Add during development, remove for production
  # ...
}
```

All three tools print the resulting `bs_theme()` code to the R console for easy copy-paste. **Limitations:** Bootstrap 5+ only, Shiny apps and `runtime: shiny` R Markdown only, doesn't affect 3rd-party widgets that don't use `bs_dependency_defer()`.

## Theme Inspection

**Retrieve computed Sass variable values:**
```r
vars <- c("body-bg", "body-color", "primary", "border-radius")
bs_get_variables(bs_theme(), varnames = vars)
bs_get_variables(bs_theme(preset = "darkly"), varnames = vars)
```

**Check contrast (for accessibility):**
```r
bs_get_contrast(bs_theme(), c("primary", "dark", "light"))
```

Aim for WCAG AA compliance: 4.5:1 for normal text, 3:1 for large text.

## Best Practices

1. **Prefer `bs_theme()` over custom CSS** -- variables cascade to all related components automatically
2. **Pin Bootstrap version**: `bs_theme(version = 5)` prevents breakage if defaults change
3. **Use fallback fonts** with `font_collection()` to avoid FOIT on slow connections
4. **Test across components**: inputs, buttons, cards, navs, plots, tables, modals, toasts, mobile
5. **Check accessibility** with `bs_get_contrast()` and browser dev tools
6. **Use CSS utility classes** for one-off styling instead of custom CSS (see [sass-and-css-variables.md](references/sass-and-css-variables.md))
7. **Organize complex themes** in a separate `theme.R`:

```r
# theme.R
app_theme <- function() {
  bs_theme(
    version = 5,
    primary = "#2c3e50",
    base_font = font_google("Lato"),
    heading_font = font_google("Montserrat", wght = c(400, 700))
  ) |>
    bs_add_rules(sass::sass_file("www/custom.scss"))
}
```

## Reference Files

- **[sass-and-css-variables.md](references/sass-and-css-variables.md)** -- Bootstrap's two-layer variable system, CSS custom properties, utility classes
- **[dark-mode.md](references/dark-mode.md)** -- Color modes, dark mode, dynamic theming, component compatibility

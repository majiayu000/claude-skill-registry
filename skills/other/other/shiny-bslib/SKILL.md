---
name: shiny-bslib
description: Build modern Shiny dashboards and applications using bslib (Bootstrap 5). Use when creating new Shiny apps, modernizing legacy apps (fluidPage, fluidRow/column, tabsetPanel, wellPanel, shinythemes), or working with bslib page layouts, grid systems, cards, value boxes, navigation, sidebars, filling layouts, theming, accordions, tooltips, popovers, toasts, or bslib inputs. Assumes familiarity with basic Shiny.
metadata:
  author: Garrick Aden-Buie (@gadenbuie)
  version: "1.0"
license: MIT
---

# Modern Shiny Apps with bslib

Build professional Shiny dashboards using bslib's Bootstrap 5 components and layouts. This skill focuses on modern UI/UX patterns that replace legacy Shiny approaches.

## Quick Start

**Single-page dashboard:**
```r
library(shiny)
library(bslib)

ui <- page_sidebar(
  title = "My Dashboard",
  theme = bs_theme(version = 5),  # "shiny" preset by default
  sidebar = sidebar(
    selectInput("variable", "Variable", choices = names(mtcars))
  ),
  layout_column_wrap(
    width = 1/3,
    fill = FALSE,
    value_box(title = "Users", value = "1,234", theme = "primary"),
    value_box(title = "Revenue", value = "$56K", theme = "success"),
    value_box(title = "Growth", value = "+18%", theme = "info")
  ),
  card(
    full_screen = TRUE,
    card_header("Plot"),
    plotOutput("plot")
  )
)

server <- function(input, output, session) {
  output$plot <- renderPlot({
    hist(mtcars[[input$variable]], main = input$variable)
  })
}

shinyApp(ui, server)
```

**Multi-page dashboard:**
```r
ui <- page_navbar(
  title = "Analytics Platform",
  theme = bs_theme(version = 5),
  nav_panel("Overview", overview_ui),
  nav_panel("Analysis", analysis_ui),
  nav_panel("Reports", reports_ui)
)
```

## Core Concepts

### Page Layouts

- **`page_sidebar()`** -- Single-page dashboard with sidebar (most common)
- **`page_navbar()`** -- Multi-page app with top navigation bar
- **`page_fillable()`** -- Viewport-filling layout for custom arrangements
- **`page_fluid()`** -- Scrolling layout for long-form content

See [page-layouts.md](references/page-layouts.md) for detailed guidance.

### Grid Systems

- **`layout_column_wrap()`** -- Uniform grid with auto-wrapping (recommended for most cases)
- **`layout_columns()`** -- 12-column Bootstrap grid with precise control

See [grid-layouts.md](references/grid-layouts.md) for detailed guidance.

### Cards

Primary container for dashboard content. Support headers, footers, multiple body sections, and full-screen expansion.

See [cards.md](references/cards.md) for detailed guidance.

### Value Boxes

Display key metrics and KPIs with optional icons, sparklines, and built-in theming.

See [value-boxes.md](references/value-boxes.md) for detailed guidance.

### Navigation

- **Page-level**: `page_navbar()` for multi-page apps
- **Component-level**: `navset_card_underline()`, `navset_tab()`, `navset_pill()` for tabbed content

See [navigation.md](references/navigation.md) for detailed guidance.

### Sidebars

- **Page-level**: `page_sidebar()` or `page_navbar(sidebar = ...)`
- **Component-level**: `layout_sidebar()` within cards
- Supports conditional content, dynamic open/close, accordions

See [sidebars.md](references/sidebars.md) for detailed guidance.

### Filling Layouts

The fill system controls how components resize to fill available space. Key concepts: fillable containers, fill items, fill carriers. Fill activates when containers have defined heights.

See [filling.md](references/filling.md) for detailed guidance.

### Theming

- **`bs_theme()`** with Bootswatch themes for quick styling
- **Custom colors**: `bg`, `fg`, `primary` affect hundreds of CSS rules
- **Fonts**: `font_google()` for typography
- **Dynamic theming**: `input_dark_mode()` + `session$setCurrentTheme()`

See [theming.md](references/theming.md) for detailed guidance.

### UI Components

- **Accordions** -- Collapsible sections, especially useful in sidebars
- **Tooltips** -- Hover-triggered help text
- **Popovers** -- Click-triggered containers for secondary UI/inputs
- **Toasts** -- Temporary notification messages

See [accordions.md](references/accordions.md), [tooltips-popovers.md](references/tooltips-popovers.md), and [toasts.md](references/toasts.md).

### Icons

**Recommended: `bsicons` package** (Bootstrap Icons, designed for bslib):
```r
bsicons::bs_icon("graph-up")
bsicons::bs_icon("people", size = "2em")
```

Browse icons: https://icons.getbootstrap.com/

**Alternative: `fontawesome` package:**
```r
fontawesome::fa("envelope")
```

**Accessibility for icon-only triggers:** When an icon is used as the sole trigger for a tooltip, popover, or similar interactive element (no accompanying text), it must be accessible to screen readers. By default, icon packages mark icons as decorative (`aria-hidden="true"`), which hides them from assistive technology.

- **`bsicons::bs_icon()`**: Provide `title` — this automatically sets `a11y = "sem"`
  ```r
  tooltip(
    bs_icon("info-circle", title = "More information"),
    "Tooltip content here"
  )
  ```
- **`fontawesome::fa()`**: Set `a11y = "sem"` and provide `title`
  ```r
  tooltip(
    fa("circle-info", a11y = "sem", title = "More information"),
    "Tooltip content here"
  )
  ```

The `title` should describe the purpose of the trigger (e.g., "More information", "Settings"), not the icon itself (e.g., not "info circle icon").

### Special Inputs

- **`input_switch()`** -- Toggle switch (modern checkbox alternative)
- **`input_dark_mode()`** -- Dark mode toggle
- **`input_task_button()`** -- Button for long-running operations
- **`input_code_editor()`** -- Code editor with syntax highlighting
- **`input_submit_textarea()`** -- Textarea with explicit submission

See [inputs.md](references/inputs.md) for detailed guidance.

## Common Workflows

### Building a Dashboard

1. Choose page layout: `page_sidebar()` (single-page) or `page_navbar()` (multi-page)
2. Add theme with `bs_theme()` (consider Bootswatch for quick start)
3. Create sidebar with inputs for filtering/controls
4. Add value boxes at top for key metrics (set `fill = FALSE` on container)
5. Arrange cards with `layout_column_wrap()` or `layout_columns()`
6. Enable `full_screen = TRUE` on all visualization cards
7. Add `thematic::thematic_shiny()` for plot theming

### Modernizing an Existing App

See [migration.md](references/migration.md) for a complete mapping of legacy patterns to modern equivalents. Key steps:

1. Replace `fluidPage()` with `page_sidebar()` or `page_navbar()`
2. Replace `fluidRow()`/`column()` with `layout_columns()`
3. Wrap outputs in `card(full_screen = TRUE)`
4. Add `theme = bs_theme(version = 5)`
5. Convert key metrics to `value_box()` components
6. Replace `tabsetPanel()` with `navset_card_underline()`

## Guidelines

1. **Prefer bslib page functions** (`page_sidebar()`, `page_navbar()`, `page_fillable()`, `page_fluid()`) over legacy equivalents (`fluidPage()`, `navbarPage()`)
2. **Use `layout_column_wrap()` or `layout_columns()`** for grid layouts instead of `fluidRow()`/`column()`, which don't support filling layouts
3. **Wrap outputs in `card(full_screen = TRUE)`** when building dashboards -- full-screen expansion is a high-value feature
4. **Set `fill = FALSE`** on `layout_column_wrap()` containers holding value boxes (they shouldn't stretch to fill height)
5. **Pin Bootstrap version**: include `theme = bs_theme(version = 5)` or a preset theme
6. **Use `thematic::thematic_shiny()`** in the server so base R and ggplot2 plots match the app theme
7. **Use responsive widths** like `width = "250px"` in `layout_column_wrap()` for auto-adjusting columns
8. **Group sidebar inputs** with `accordion()` when sidebars have many controls
9. **See [migration.md](references/migration.md)** for mapping legacy Shiny patterns to modern bslib equivalents

## Avoid Common Errors

1. Avoid directly nesting `card()` containers. `navset_card_*()` functions are already cards; `nav_panel()` content goes directly inside them without wrapping in `card()`
2. Only use `layout_columns()` and `layout_column_wrap()` for laying out multiple elements. Single children should be passed directly to their container functions.
3. Never nest `page_*()` functions. Only use one top-level page function per app.

## Reference Files

- **[migration.md](references/migration.md)** -- Legacy Shiny to modern bslib migration guide
- **[page-layouts.md](references/page-layouts.md)** -- Page-level layout functions and patterns
- **[grid-layouts.md](references/grid-layouts.md)** -- Multi-column grid systems
- **[cards.md](references/cards.md)** -- Card components and features
- **[value-boxes.md](references/value-boxes.md)** -- Value boxes for metrics and KPIs
- **[navigation.md](references/navigation.md)** -- Navigation containers and patterns
- **[sidebars.md](references/sidebars.md)** -- Sidebar layouts and organization
- **[filling.md](references/filling.md)** -- Fillable containers and fill items
- **[theming.md](references/theming.md)** -- Basic theming (colors, fonts, Bootswatch). See **shiny-bslib-theming** skill for advanced theming
- **[accordions.md](references/accordions.md)** -- Collapsible sections and sidebar organization
- **[tooltips-popovers.md](references/tooltips-popovers.md)** -- Hover tooltips and click-triggered popovers
- **[toasts.md](references/toasts.md)** -- Temporary notification messages
- **[inputs.md](references/inputs.md)** -- Special bslib input widgets
- **[best-practices.md](references/best-practices.md)** -- bslib-specific patterns and common gotchas

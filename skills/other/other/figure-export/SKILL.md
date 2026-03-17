---
name: figure-export
description: >
  Figure export conventions for publication-quality R figures (PDF/PNG/SVG).
  Use when saving plots to files, choosing figure formats, setting DPI or dimensions,
  or exporting ggplot2 or base R figures for manuscripts or Inkscape editing.
user-invocable: false
---

# Figure Export for Inkscape Editing

Best practices for saving R figures as PDF, PNG, and SVG so they are high quality and editable in Inkscape.

## Always Save 3 Formats

Every figure should be saved as PDF, PNG, and SVG:

```r
# PDF — use cairo_pdf to embed fonts properly (handles Arial, Helvetica, etc.)
ggsave("plot.pdf", plot = p, width = 6.8, height = 5.5, device = cairo_pdf)

# PNG — always 300 dpi
ggsave("plot.png", plot = p, width = 6.8, height = 5.5, dpi = 300)

# SVG — use svglite with fix_text_size = FALSE
ggsave("plot.svg", plot = p, width = 6.8, height = 5.5,
       device = function(...) svglite::svglite(..., fix_text_size = FALSE))
```

## SVG Text Editability

**Critical:** `svglite` defaults to `fix_text_size = TRUE`, which adds `textLength` and `lengthAdjust` attributes to every `<text>` element. These lock the text width and prevent editing in Inkscape. Always set `fix_text_size = FALSE`.

This applies everywhere svglite is used:

```r
# Via ggsave (ggplot2 plots)
ggsave(..., device = function(...) svglite::svglite(..., fix_text_size = FALSE))

# Via direct device call (pheatmap, base R graphics)
svglite::svglite("plot.svg", width = w, height = h, fix_text_size = FALSE)
grid::grid.newpage()
grid::grid.draw(p$gtable)
dev.off()
```

**Do NOT use** base R `svg()` or Cairo SVG — they produce bloated SVGs with many style attributes per element and can crash Inkscape with large plots.

## PDF Font Embedding

Use `cairo_pdf` instead of the default `pdf()` device. The default PDF device cannot find non-standard fonts (e.g., Arial) and will error with "failed to find or load PDF CID font". `cairo_pdf` embeds fonts as outlines.

```r
# CORRECT
ggsave("plot.pdf", plot = p, device = cairo_pdf)

# WRONG — will fail with Arial or other non-default fonts
ggsave("plot.pdf", plot = p)  # uses default pdf() device
```

## Font Standardization

Use Arial across all figure elements for consistency and Inkscape compatibility:

```r
# In theme
theme_paper <- function(base_size = 12, base_family = "Arial") {
  theme_bw(base_size = base_size, base_family = base_family) + ...
}

# In geom_text_repel and other text geoms
geom_text_repel(..., family = "Arial")
```

## Rasterizing Dense Point Layers (ggrastr)

For plots with thousands of points (volcano plots, MA plots, scatter plots), rasterize the background points to prevent SVG bloat and Inkscape crashes. Keep foreground points and text as vectors for editability.

```r
library(ggrastr)

ggplot() +
  # Background points — rasterized (becomes single <image> in SVG)
  rasterise(geom_point(
    data = df_background,
    aes(x = x, y = y),
    colour = "grey70", alpha = 0.35, size = 0.9
  ), dpi = 1200) +
  # Foreground points — vector (stays editable)
  geom_point(
    data = df_foreground,
    aes(x = x, y = y, colour = group),
    size = 1.2
  ) +
  # Text labels — vector (stays editable)
  geom_text_repel(...)
```

**DPI for rasterized layers:** Use 1200 dpi for publication quality. 300 dpi is sufficient for drafts.

**ggrastr only works with ggplot2.** For `pheatmap` or base R graphics, the cells are drawn as simple `<rect>` elements which are lightweight — rasterization is not needed.

## Consistent Plot Dimensions

When plots will be assembled into multi-panel figures, use identical `width` and `height` across all plots of the same type. This ensures the plotting windows align without rescaling in Inkscape.

```r
# Define once, use everywhere
VOLCANO_WIDTH <- 6.8
VOLCANO_HEIGHT <- 5.5

ggsave_safe(..., width = VOLCANO_WIDTH, height = VOLCANO_HEIGHT)
```

Different axis limits or thresholds are fine — the key is that the outer plot dimensions match so panels can be tiled.

## ggsave_safe Pattern

A helper that saves all 3 formats from a single call:

```r
ggsave_safe <- function(filename, plot, width, height, units = "in", max_inches = 49, ...) {
  # Guard against oversized plots
  scale_factor <- max(width / max_inches, height / max_inches, 1)
  if (scale_factor > 1) {
    width <- width / scale_factor
    height <- height / scale_factor
  }
  # PDF
  ggplot2::ggsave(filename, plot = plot, width = width, height = height,
                  units = units, device = cairo_pdf, limitsize = FALSE, ...)
  # PNG
  ggplot2::ggsave(sub("\\.pdf$", ".png", filename), plot = plot,
                  width = width, height = height, units = units,
                  dpi = 300, limitsize = FALSE, ...)
  # SVG
  ggplot2::ggsave(sub("\\.pdf$", ".svg", filename), plot = plot,
                  width = width, height = height, units = units,
                  device = function(...) svglite::svglite(..., fix_text_size = FALSE),
                  limitsize = FALSE, ...)
}
```

## Required Packages

```r
library(ggrastr)   # rasterise() for dense point layers
library(svglite)   # clean SVG output
# cairo_pdf is built into grDevices (no extra package needed)
```
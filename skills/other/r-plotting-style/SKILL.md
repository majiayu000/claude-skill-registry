---
name: r-plotting-style
description: R ggplot2 plotting conventions and theme. Use when creating, modifying, or styling ggplot2 plots in R, or when adjusting plot themes, colors, labels, or formatting.
user-invocable: false
---

# R Plotting Conventions

## Default Theme

Always use `theme_classic()` as the base for plots. This provides a clean, minimal style without grid lines.

```r
# Standard theme_clean function for all projects
theme_clean <- function(base_size = 12) {
  theme_classic(base_size = base_size) +
    theme(
      plot.title = element_text(face = "bold", size = base_size * 1.1),
      plot.subtitle = element_text(size = base_size * 0.9, color = "grey40"),
      plot.title.position = "plot",
      plot.caption.position = "plot",
      plot.margin = margin(12, 12, 12, 12),
      axis.line = element_line(linewidth = 0.4, color = "grey30"),
      axis.ticks = element_line(linewidth = 0.3, color = "grey30"),
      axis.text = element_text(size = base_size * 0.9, color = "grey20"),
      axis.title = element_text(size = base_size, color = "grey20"),
      legend.title = element_text(size = base_size * 0.9),
      legend.text = element_text(size = base_size * 0.85),
      strip.text = element_text(face = "bold", size = base_size),
      strip.background = element_blank()
    )
}
```

## Style Preferences

- **No grid lines** — use `theme_classic()` not `theme_bw()`
- **No stacked bar charts** — use grouped/dodged bars instead
- **Clean axis labels** — avoid special characters that may not render (use "3 to 15 min" not "3→15 min")
- **Legends at top** — left-justified when possible
- **Minimal borders and boxes** — keep visual clutter low

## Text Legibility

Ensure text never overlaps or falls off the plot edge:

- **Use `ggrepel`** for data labels — `geom_text_repel()` and `geom_label_repel()` prevent overlap
- **Rotate long axis labels** — `axis.text.x = element_text(angle = 45, hjust = 1)`
- **Sufficient margins** — increase `plot.margin` if labels are clipped
- **Check rendered output** — labels that fit in RStudio may clip in saved PDFs
- **Wrap long text** — use `str_wrap()` for titles or labels exceeding plot width

```r
# Example: repel labels to avoid overlap
library(ggrepel)
ggplot(data, aes(x, y, label = gene)) +

  geom_point() +
  geom_text_repel(max.overlaps = 20, size = 3)
```

## Consistency Across Related Plots

When creating multiple plots of the same type (e.g., per-module heatmaps, cluster markers), keep dimensions and styling consistent so they can be combined in a figure:

- **Fixed dimensions** — use the same `width` and `height` in `ggsave()` for all plots of a type
- **Fixed text sizes** — don't let `base_size` vary between related plots
- **Fixed color scales** — define shared `scale_fill_*` / `scale_color_*` once and reuse
- **Fixed axis ranges** — consider shared limits when comparing across plots
- **Consistent aspect ratio** — use `coord_fixed()` or consistent width/height ratios

```r
# Example: define shared parameters for a set of heatmaps
HEATMAP_WIDTH <- 8
HEATMAP_HEIGHT <- 6
HEATMAP_BASE_SIZE <- 10
HEATMAP_COLORS <- scale_fill_gradient2(low = "blue", mid = "white", high = "red", midpoint = 0)

# Apply consistently to each plot
ggsave(filename, plot, width = HEATMAP_WIDTH, height = HEATMAP_HEIGHT)
```
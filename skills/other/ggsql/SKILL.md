---
name: ggsql
description: Write ggsql queries — a grammar of graphics for SQL. Use when the user wants to create, modify, or understand a ggsql visualization query.
allowed-tools: Bash(ggsql:*)
argument-hint: "[description of desired visualization]"
metadata:
  author: George Stagg (@georgestagg)
  version: "1.0"
license: MIT
---

# ggsql Query Writer

ggsql is a SQL extension for declarative data visualization based on Grammar of Graphics principles. It lets users combine SQL data queries with visualization specifications in a single, composable syntax.

When the user describes a visualization they want, write a valid ggsql query. Use ONLY syntax documented below. NEVER invent clauses, settings, aesthetics, or layer types.

## Query structure

A ggsql query has two parts:

1. **SQL part** (optional): Standard SQL executed on the backend. Any tables, CTEs, or SELECT results are available to the visualization.
2. **VISUALISE part** (required): Begins with `VISUALISE` (or `VISUALIZE`). Everything after this is the visualization query.

There are two patterns for combining SQL with VISUALISE:

### Pattern A: SELECT → VISUALISE

The last SQL statement is a SELECT. Data flows from its result set into VISUALISE, which has no `FROM` clause.

```ggsql
SELECT name, score_a, score_b FROM 'dataset.csv' WHERE value > 50
VISUALISE score_a AS x, score_b AS y
[DRAW / PLACE / SCALE / FACET / PROJECT / LABEL clauses]
```

Works with any SQL that ends in a SELECT: bare SELECT, WITH...SELECT, UNION/INTERSECT/EXCEPT.

### Pattern B: VISUALISE FROM

VISUALISE provides its own data source via `FROM`. Use when referencing a table, file, CTE, or built-in dataset directly without a trailing SELECT.

```ggsql
VISUALISE score_a AS x, score_b AS y FROM 'dataset.csv'
DRAW point
```

```ggsql
WITH summary AS (SELECT category, COUNT(*) AS n FROM 'dataset.csv' GROUP BY category)
VISUALISE category AS x, n AS y FROM summary
DRAW bar
```

## Data sources

Data sources can appear in `VISUALISE ... FROM` or `DRAW ... MAPPING ... FROM`:

- **Table/CTE name** (unquoted): `FROM sales`, `FROM my_cte`
- **File path** (single-quoted string): `FROM 'data.parquet'`, `FROM 'data.csv'`
- **Built-in datasets**: `FROM ggsql:penguins`, `FROM ggsql:airquality`

## VISUALISE clause

Marks the start of the visualization. Optionally defines global mappings inherited by all layers.

```
VISUALISE <mapping>, ... FROM <data-source>
```

### Mapping forms

- **Explicit**: `column AS aesthetic` — e.g. `revenue AS y`
- **Implicit**: `column` — column name must match aesthetic name, e.g. `x` maps to `x`
- **Wildcard**: `*` — all columns with names matching aesthetics are mapped
- **Constants**: `'red' AS fill`, `42 AS size` — literal values mapped to aesthetic

```ggsql
VISUALISE bill_len AS x, bill_dep AS y, species AS fill FROM ggsql:penguins
VISUALISE * FROM my_table
VISUALISE FROM ggsql:penguins
```

## DRAW clause

Defines a layer. Multiple DRAW clauses stack layers (first = bottom, last = top).

```
DRAW <layer-type>
  MAPPING <mapping>, ... FROM <data-source>
  REMAPPING <stat-property> AS <aesthetic>, ...
  SETTING <param> => <value>, ...
  FILTER <condition>
  PARTITION BY <column>, ...
  ORDER BY <column>, ...
```

All subclauses are optional if VISUALISE provides global mappings and data.

### MAPPING

Same syntax as VISUALISE mappings. Layer mappings merge with global mappings (layer takes precedence). Can include `FROM` for layer-specific data.

- Use `null` to prevent inheriting a global mapping: `MAPPING null AS color`

### REMAPPING

For statistical layers (histogram, density, boxplot, violin, smooth, bar without y). Maps calculated statistics to aesthetics. Each layer documents its available stats and default remapping.

```ggsql
DRAW histogram
  MAPPING body_mass AS x
  REMAPPING density AS y  -- use density instead of default count
```

### SETTING

Set literal aesthetic values or layer parameters. Aesthetics set here bypass scales.

```ggsql
DRAW point
  SETTING size => 5, opacity => 0.7, stroke => 'red'
```

**Position adjustment** is a special setting:
```ggsql
SETTING position => 'identity'   -- no adjustment (default for most)
SETTING position => 'stack'      -- stack (default for bar, histogram, area)
SETTING position => 'dodge'      -- side by side (default for boxplot, violin)
SETTING position => 'jitter'     -- random offset
```

### FILTER

SQL WHERE condition applied to layer data. Content is passed to the database:
```ggsql
DRAW point
  FILTER sex = 'female' AND body_mass > 4000
```

### PARTITION BY

Additional grouping columns beyond mapped discrete aesthetics:
```ggsql
DRAW line
  MAPPING Day AS x, Temp AS y
  PARTITION BY Month
```

### ORDER BY

Controls record order (important for path layers):
```ggsql
DRAW path
  ORDER BY timestamp
```

## PLACE clause

Creates annotation layers with literal values only (no data mappings). Supports tuples for multiple annotations.

```
PLACE <layer-type>
  SETTING <aesthetic/param> => <value>, ...
```

```ggsql
PLACE point SETTING x => 5, y => 10, color => 'red'
PLACE rule SETTING y => 70, linetype => 'dotted'
PLACE text SETTING x => (34, 44), y => (66, 49), label => ('Mean = 34', 'Mean = 44')
```

## SCALE clause

Controls how data values are translated to aesthetic values. Sensible defaults are always provided.

```
SCALE <type> <aesthetic> FROM <input-range> TO <output-range> VIA <transform>
  SETTING <param> => <value>, ...
  RENAMING <value> => <label>, ...
```

All parts except `aesthetic` are optional.

### Scale types (optional, placed before aesthetic)

- `CONTINUOUS` — continuous numeric/temporal data
- `DISCRETE` — categorical/string data
- `BINNED` — bin continuous data into discrete groups (never auto-selected, must be explicit)
- `ORDINAL` — ordered discrete data (never auto-selected, must be explicit)
- `IDENTITY` — pass data through unchanged (no legend created)

If omitted, type is inferred from data.

### Aesthetic names

Use the base name: `x`, `y`, `fill`, `stroke`, `color` (sets both fill and stroke), `opacity`, `size`, `linewidth`, `linetype`, `shape`, `panel` (facet), `row`, `column`.

For position families (xmin/xmax/xend/ymin/ymax/yend), scale with the base name: `SCALE x ...`

### FROM (input range)

- Continuous: `FROM (min, max)` — use `null` to infer from data: `FROM (0, null)`
- Discrete: `FROM ('A', 'B', 'C')` — controls order, omitted values are nulled
- Include null explicitly: `FROM ('Torgersen', 'Biscoe', null)`

### TO (output range)

- Array of values: `TO ('red', 'blue', 'green')`, `TO (1, 6)`
- Named palette: `TO viridis`, `TO dark2`, `TO tableau10`

### VIA (transform)

Continuous transforms: `linear`, `log`, `log2`, `ln`, `exp10`, `exp2`, `exp`, `sqrt`, `square`, `asinh`, `pseudo_log`, `pseudo_log2`, `pseudo_ln`, `integer`

Temporal transforms: `date`, `datetime`, `time` — automatically chosen for date/datetime/time columns.

Discrete transforms: `string`, `bool`

```ggsql
SCALE x VIA date        -- treat x as temporal
SCALE y VIA log         -- log transform
SCALE size VIA square   -- scale by radius not area
```

### SETTING

Continuous/binned scales:
- `expand` — expansion factor, scalar or `(mult, add)`. Default `0.05`. Only for x/y.
- `oob` — out-of-bounds: `'keep'` (default for x/y), `'censor'` (default for others), `'squish'`
- `breaks` — integer count, array of values, or interval string for temporal (e.g. `'2 months'`, `'week'`)
- `pretty` — boolean, default `true`. Use Wilkinson's algorithm for nice breaks.
- `reverse` — boolean, default `false`. Reverse scale direction.

Binned scales additionally:
- `closed` — `'left'` (default) or `'right'`

Discrete/ordinal scales:
- `reverse` — boolean

```ggsql
SCALE x SETTING breaks => '2 months'
SCALE y FROM (0, 100) SETTING oob => 'squish'
SCALE BINNED x SETTING breaks => 10, pretty => false
```

### RENAMING

Rename break labels. Direct renaming, wildcard formatting, or both (direct takes priority):

```ggsql
RENAMING 'Adelie' => 'Pygoscelis adeliae', 'adelie' => null  -- direct / suppress
RENAMING * => '{} mm'                -- string interpolation
RENAMING * => '{:Title}'             -- formatters: Title, UPPER, lower, time %B %Y, num %.1f
```

## FACET clause

Split data into small multiples.

```
FACET <column> BY <column>
  SETTING <param> => <value>, ...
```

- 1D: `FACET region` — wrap layout, aesthetic name is `panel`
- 2D: `FACET region BY category` — grid layout, aesthetics are `row` and `column`

### Settings

- `free` — `null` (default/fixed), `'x'`, `'y'`, or `('x', 'y')` for independent scales
- `missing` — `'repeat'` (default, show layer in all panels) or `'null'` (only show in null panel)
- `ncol`/`nrow` — layout dimensions for 1D faceting (only one allowed)

### Customizing strip labels

Use SCALE on the facet aesthetic:
```ggsql
FACET region
SCALE panel
  RENAMING 'N' => 'North', 'S' => 'South'
```

### Filtering panels

Use SCALE FROM to select which panels to show:
```ggsql
FACET island
SCALE panel FROM ('Biscoe', 'Dream')
```

## PROJECT clause

Controls the coordinate system.

```
PROJECT <aesthetic>, ... TO <coord-type>
  SETTING <param> => <value>, ...
```

### Coordinate types

**cartesian** (default) — horizontal x, vertical y
- Settings: `clip` (boolean, default true), `ratio` (aspect ratio number or null)
- Default aesthetics: `x`, `y`

**polar** — angle + radius from center
- Settings: `clip`, `start` (degrees, default 0 = 12 o'clock), `end` (degrees, default start+360), `inner` (0-1 proportion for donut hole, default 0)
- Default aesthetics: `radius` (primary), `angle` (secondary)

Swap aesthetic order to flip axes: `PROJECT y, x TO cartesian`. If no PROJECT clause, coordinate type is inferred from mappings (x/y = cartesian, radius/angle = polar).

```ggsql
PROJECT TO polar SETTING inner => 0.5  -- donut chart
PROJECT TO polar SETTING start => -90, end => 90  -- half-circle gauge
```

## LABEL clause

Override default axis/legend labels and add titles.

```
LABEL
  <aesthetic/title> => <string>, ...
```

Available labels:
- `title` — main title
- `subtitle` — subtitle below title
- `caption` — text below the plot
- Any aesthetic name — axis/legend title: `x`, `y`, `fill`, `color`, etc.
- Use `null` to suppress a label: `fill => null`

```ggsql
LABEL
  title => 'Sales by Region',
  subtitle => 'Q4 2024 data',
  x => 'Date',
  y => 'Revenue (USD)',
  fill => 'Region',
  caption => 'Source: internal sales database'
```

---

## Layer types

### point
Scatterplot. Required: x, y. Optional: size, colour, stroke, fill, opacity, shape.

### line
Line plot sorted along primary axis. Required: x, y. Optional: colour/stroke, opacity, linewidth, linetype. Settings: `position`, `orientation` (`'aligned'`/`'transposed'`).

### path
Like line but connects points in data order (not sorted). Same aesthetics as line.

### bar
Bar chart. Auto-counts if y not provided. Optional: x (categories), y (height), fill, colour, stroke. Stats: `count`, `proportion`. Properties: `weight`. Settings: `position` (default `'stack'`), `width` (0-1). Orientation inferred from mapping (categories on x = vertical, on y = horizontal).

```ggsql
DRAW bar MAPPING species AS x                              -- auto-count
DRAW bar MAPPING species AS x, total AS y                  -- pre-computed
DRAW bar MAPPING species AS x, sex AS fill                 -- stacked (default)
  SETTING position => 'dodge'                              -- side by side
```

### histogram
Bins continuous data. Required: x. Stats: `count`, `density`. Default remapping: `count AS <secondary>`. Settings: `position` (default `'stack'`), `bins` (default 30), `binwidth`, `closed` (`'left'`/`'right'`).

```ggsql
DRAW histogram MAPPING body_mass AS x SETTING binwidth => 100
DRAW histogram MAPPING body_mass AS x REMAPPING density AS y  -- density instead of count
```

### density
Kernel density estimation. Required: x. Stats: `density`, `intensity`. Settings: `position` (default `'identity'`), `bandwidth`, `adjust` (default 1), `kernel` (`'gaussian'` default, `'epanechnikov'`, `'triangular'`, `'rectangular'`, `'biweight'`, `'cosine'`).

### boxplot
Five-number summary with outliers. Required: x (categorical), y (continuous). Stats: `type`, `value`. Settings: `position` (default `'dodge'`), `outliers` (default true), `coef` (whisker IQR multiple, default 1.5), `width` (default 0.9).

### violin
Mirrored kernel density for groups. Required: x (categorical), y (continuous). Stats: `density`, `intensity`. Default remapping: `density AS offset`. Settings: `position` (default `'dodge'`), `bandwidth`, `adjust`, `kernel` (same as density), `width` (default 0.9), `side` (`'both'`/`'left'`/`'bottom'`/`'right'`/`'top'`), `tails` (number or null, default 3).

### smooth
Trendline. Required: x, y. Stats: `intensity`. Settings: `method` (`'nw'` default, `'ols'`, `'tls'`), `bandwidth`, `adjust`, `kernel` (same as density, nw only).

### area
Area chart anchored at zero. Required: x, y. Settings: `position` (default `'stack'`), `orientation`, `total` (normalize stacks), `center` (boolean, for steamgraph).

### ribbon
Like area but with explicit ymin/ymax (unanchored). Required: x, ymin, ymax.

### segment
Line segments between two endpoints. Required: x, y, xend, yend. For axis-aligned intervals where one coordinate is shared between start and end, use `range` instead.

### rule
Reference lines spanning the full panel. Required: x or y. Optional: `slope` (for diagonal: `y = a + slope * x`).

### text
Text labels. Required: x, y, label. Settings: `offset` (number or `(h, v)`), `format` (string interpolation like RENAMING). `hjust`: `'left'`/`'right'`/`'centre'` or 0-1. `vjust`: `'top'`/`'bottom'`/`'middle'` or 0-1.

### rect
Rectangles. Required: pick 2 per axis from center (x/y), min (xmin/ymin), max (xmax/ymax), width, height. Or just center (defaults width/height to 1).

### polygon
Closed shapes from ordered coordinates. Required: x, y. Use PARTITION BY to separate distinct polygons.

### range
Range/interval display between two values along the secondary axis. Required: x, ymin, ymax. Settings: `width` (hinge width in points, default 10, null to hide).

All layers accept common optional aesthetics (colour/stroke, fill, opacity, linewidth, linetype) and `position` setting where applicable.

---

## Named color palettes

- **Discrete**: `ggsql10` (default), `tableau10`, `category10`, `set1`, `set2`, `set3`, `dark2`, `paired`, `pastel1`, `pastel2`, `accent`, `kelly22`
- **Sequential**: `sequential` (default), `viridis`, `plasma`, `magma`, `inferno`, `cividis`, `blues`, `greens`, `oranges`, `reds`, `purples`, `greys`, `ylgnbu`, `ylorbr`, `ylorrd`, `batlow`, `hawaii`, `lajolla`, `turku`, and more
- **Diverging**: `vik`/`diverging`, `rdbu`, `rdylbu`, `rdylgn`, `spectral`, `brbg`, `prgn`, `piyg`, `puor`, `berlin`, `roma`, and more
- **Cyclic**: `romao`/`cyclic`, `bamo`, `broco`, `corko`, `viko`

---

## Common patterns

```ggsql
-- Pie chart
VISUALISE species AS fill FROM ggsql:penguins
DRAW bar
PROJECT TO polar

-- Horizontal bar chart
DRAW bar MAPPING species AS y

-- Multi-series line chart
VISUALISE Date AS x
DRAW line MAPPING Temp AS y, 'Temperature' AS color
DRAW line MAPPING Ozone AS y, 'Ozone' AS color
SCALE x VIA date

-- Lollipop chart
SELECT ROUND(bill_dep) AS bill_dep, COUNT(*) AS n FROM ggsql:penguins GROUP BY 1
VISUALISE bill_dep AS x
DRAW range MAPPING 0 AS ymin, n AS ymax SETTING width => null
DRAW point MAPPING n AS y

-- Ridgeline / joy plot
VISUALISE Temp AS x, Month AS y FROM ggsql:airquality
DRAW violin SETTING width => 4, side => 'top'
SCALE ORDINAL y

-- Bar labels
SELECT island, COUNT(*) AS n FROM ggsql:penguins GROUP BY island
VISUALISE island AS x, n AS y
DRAW bar
DRAW text MAPPING n AS label SETTING vjust => 'top', offset => (0, -11), fill => 'white'

-- CTEs with separate layer data
WITH temps AS (SELECT Date, Temp as value FROM ggsql:airquality),
ozone AS (SELECT Date, Ozone as value FROM ggsql:airquality WHERE Ozone IS NOT NULL)
VISUALISE
DRAW line MAPPING Date AS x, value AS y, 'Temperature' AS color FROM temps
DRAW point MAPPING Date AS x, value AS y, 'Ozone' AS color FROM ozone
SCALE x VIA date
```

---

## CLI

The `ggsql` CLI should be on the PATH. Subcommands: `exec <QUERY>`, `run <FILE>`, `validate <QUERY>`, `parse <QUERY>`. Common options: `--reader <URI>` (default `duckdb://memory`), `--writer <FORMAT>` (default `vegalite`), `--output <PATH>`, `-v` (verbose).

```bash
ggsql validate "VISUALISE x, y FROM data DRAW point"
ggsql exec "VISUALISE bill_len AS x, bill_dep AS y FROM ggsql:penguins DRAW point" -v
ggsql run query.sql --output chart.vl.json
```

---

## Additional References

* https://ggsql.org/syntax/index.llms.md — Online documentation with the latest syntax

---

## Instructions for responding

1. Write a complete, valid ggsql query matching the user's request.
2. Use SQL CTEs/queries before VISUALISE when data shaping is needed.
3. Choose the simplest layer types and settings that achieve the goal.
4. Include SCALE clauses when the defaults are insufficient (e.g. date formatting, custom palettes, range limits).
5. Include LABEL for titles when the context warrants it.
6. Briefly explain your choices after the query.
7. NEVER invent syntax, settings, aesthetics, layer types, or palette names not documented above.
8. If unsure whether a feature exists, say so rather than guessing.
9. Use `ggsql:penguins` or `ggsql:airquality` as example data when no specific data is mentioned.
10. When the user wants to validate a query, use `ggsql validate "<query>"`. When the user wants to see the output, use `ggsql exec "<query>" -v`.

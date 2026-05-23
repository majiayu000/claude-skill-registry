---
name: marimo-notebooks
description: |
  ALWAYS use when: creating/editing marimo notebooks, working with any .py file containing @app.cell decorators, building reactive Python notebooks, doing exploratory data analysis in notebook form, converting Jupyter (.ipynb) to marimo, or when user mentions "marimo", "reactive notebook", or asks for an interactive Python notebook. Covers marimo CLI (edit, run, convert, export), UI components (mo.ui.*), layout functions, SQL integration, caching, state management, and wigglystuff widgets. If a task involves notebooks and Python, invoke this skill first.
---

# Marimo Notebooks

Marimo notebooks are reactive Python notebooks stored as pure `.py` files. Cells auto-execute when dependencies change, modeled as a directed acyclic graph (DAG).

## Core Concepts

### Reactivity Model
- marimo uses **static analysis** to build a dependency graph from variable references and definitions
- When a cell runs, all cells referencing its defined variables **automatically re-run**
- Execution order follows the dependency graph, **not visual cell order**
- Each global variable must be defined by **exactly one cell**
- marimo does **not track object mutations** (like `list.append()`)—mutate in the same cell that creates the object, or create new variables

### Avoiding Variable Name Conflicts
Each global variable must be defined by exactly one cell. Two strategies:

**1. Wrap code in functions (preferred for reusable patterns):**
```python
@app.cell
def _(data):
    def compute_mean_with_new_col(df):
        temp = df.copy()
        temp["new_col"] = temp["x"] * 2
        return temp.mean()

    return (compute_mean_with_new_col(data),)
```

**2. Use meaningful, unique variable names:**
```python
@app.cell
def _(model1_data):
    model1_transformed = model1_data.copy()
    model1_transformed["new_col"] = model1_transformed["x"] * 2
    return (model1_transformed,)
```

Never use underscore prefixes to generate unique variable names. No exceptions.

## Notebook Structure

```python
import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")

@app.cell
def _():
    import marimo as mo
    return (mo,)

@app.cell
def _(mo):
    mo.md("# Hello")
    return

if __name__ == "__main__":
    app.run()
```

Key rules:
- Each cell is a function decorated with `@app.cell`
- Variables shared by returning tuples: `return (var1, var2,)`
- Cells receive variables as parameters: `def _(mo, df):`
- Execution order follows dependency graph, not position
- Name cells descriptively for CellTour targeting: `def model_specification():`

## CLI Commands

```bash
# Create & Edit
marimo new                           # Create new notebook
marimo edit notebook.py              # Open editor
marimo edit notebook.py --watch      # Live reload on file changes

# Run as App
marimo run notebook.py               # Run as app (code hidden by default)
marimo run notebook.py --include-code  # Show code in app view

# Convert
marimo convert notebook.ipynb -o notebook.py  # Jupyter to marimo

# Export
marimo export html notebook.py -o out.html    # Static HTML
marimo export ipynb notebook.py -o out.ipynb  # To Jupyter

# Validate
marimo check notebook.py             # Lint and validate
marimo check notebook.py --fix       # Auto-fix issues
```

## Code Visibility in Run Mode

**CRITICAL FOR TUTORIALS**: By default, `marimo run` hides code. Use `mo.show_code()` to display it.

### mo.show_code() - Per-Cell Display

**IMPORTANT**: Call `mo.show_code()` as a **statement on its own line**, NOT in the return statement.

```python
@app.cell
def model_definition(mo, pm, X, y):
    with pm.Model() as model:
        alpha = pm.Normal("alpha", mu=0, sigma=10)
        beta = pm.Normal("beta", mu=0, sigma=10)
        mu = alpha + beta * X
        pm.Normal("y", mu=mu, sigma=1, observed=y)

    # Show this cell's code alongside its output
    mo.show_code(model, position="above")
    return (model,)
```

**WRONG vs RIGHT patterns:**
```python
# WRONG - do not put mo.show_code() in return statement
return mo.show_code(result)

# RIGHT - call as statement, then return separately  
mo.show_code(result, position="above")
return (result,)
```

- `position="above"` shows code first, then output (best for tutorials)
- `position="below"` shows output first, then code (default)

## Markdown with mo.md()

```python
@app.cell
def _(mo):
    mo.md(r"""
    # Title

    Interpolate Python: {slider}

    **LaTeX**: $f(x) = e^x$

    $$\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$$

    **Icons**: ::lucide:rocket:: or ::mdi:home::
    """)
    return
```

- Use raw strings (`r"""..."""`) for LaTeX
- Interpolate UI elements: `f"Value: {slider}"`
- For complex objects: `f"Plot: {mo.as_html(fig)}"`

## UI Components (mo.ui.*)

### Basic Inputs
```python
slider = mo.ui.slider(0, 100, value=50, label="Value")
number = mo.ui.number(0, 100, value=50)
text = mo.ui.text(value="", placeholder="Enter text")
checkbox = mo.ui.checkbox(value=False, label="Enable")
dropdown = mo.ui.dropdown(["a", "b", "c"], value="a")
radio = mo.ui.radio(["option1", "option2"], value="option1")
multiselect = mo.ui.multiselect(["a", "b", "c"])
```

### Buttons
```python
button = mo.ui.button(label="Click")
run_button = mo.ui.run_button(label="Run")  # For triggering computation
```

### Data Components
```python
table = mo.ui.table(df)            # Interactive table with selection
dataframe = mo.ui.dataframe(df)    # Editable dataframe
data_explorer = mo.ui.data_explorer(df)  # No-code exploration
```

### Grouping UI Elements
```python
# Forms (require submit button)
form = mo.ui.text().form()

# Batch in markdown
form = mo.md("""
**Name**: {name}
**Age**: {age}
""").batch(
    name=mo.ui.text(),
    age=mo.ui.number(0, 120)
).form()
```

See [references/ui_components.md](references/ui_components.md) for complete reference.

## Layout Functions

```python
# Stacking
mo.hstack([el1, el2, el3], justify="center", gap=2)
mo.vstack([el1, el2, el3], align="start", gap=1)

# Containers
mo.accordion({"Section 1": content1, "Section 2": content2})
mo.tabs({"Tab 1": content1, "Tab 2": content2})
mo.callout(content, kind="info")  # info, warn, success, danger, neutral
mo.sidebar([nav_content])

# Display
mo.tree({"a": {"b": 1}})    # Tree view
mo.stat(value="42", label="Users", caption="+5%")
mo.lazy(expensive_component)  # Defer until visible
```

## Output Functions

```python
mo.output.replace(new_content)  # Replace cell output
mo.output.append(additional)    # Append to output
mo.output.clear()               # Clear output

with mo.redirect_stdout():
    print("This goes to cell output")
```

## Status Indicators

```python
# Progress bar
for item in mo.status.progress_bar(items, title="Processing"):
    process(item)

# Spinner
with mo.status.spinner(title="Loading..."):
    load_data()
```

## Control Flow

```python
# Stop execution conditionally
mo.stop(condition, mo.md("*Message when stopped*"))

# Example: require button click
run_button = mo.ui.run_button()
mo.stop(not run_button.value, mo.md("Click Run to execute"))
expensive_computation()
```

## Caching

```python
# In-memory cache (session only)
@mo.cache
def expensive_function(x, y):
    return compute(x, y)

# Persistent cache (survives restarts)
@mo.persistent_cache(name="embeddings")
def compute_embeddings(text):
    return model.encode(text)
```

See [references/caching.md](references/caching.md) for model output caching patterns.

## State Management

**Warning**: Use sparingly—over 99% of cases don't need `mo.state()`.

```python
@app.cell
def _(mo):
    get_count, set_count = mo.state(0)
    return get_count, set_count

@app.cell
def _(mo, get_count, set_count):
    mo.ui.button(
        label=f"Count: {get_count()}",
        on_click=lambda _: set_count(lambda n: n + 1)
    )
    return
```

Use only when maintaining history, synchronizing UI bidirectionally, or introducing cycles.

## Interactive Plotting

```python
# Altair with selection
chart = alt.Chart(df).mark_point().encode(x="x", y="y")
selection = mo.ui.altair_chart(chart, chart_selection="point")
selected_data = selection.value  # DataFrame of selected points

# Plotly
fig = px.scatter(df, x="x", y="y")
interactive = mo.ui.plotly(fig)
interactive.value  # Selected points

# Matplotlib interactive
fig, ax = plt.subplots()
ax.plot(x, y)
mo.mpl.interactive(fig)
```

Supported: Matplotlib, Seaborn, Plotly, Altair, Bokeh, HoloViews, hvPlot

## Wigglystuff Widgets

```python
from wigglystuff import Slider2D, Paint, SortableList, Matrix, CellTour
import marimo as mo

slider2d = mo.ui.anywidget(Slider2D())
slider2d.x, slider2d.y

paint = mo.ui.anywidget(Paint(width=400, height=300))
paint.to_pil()

tour = mo.ui.anywidget(CellTour(
    steps=[
        {"cell_name": "intro", "title": "Welcome", "description": "..."},
        {"cell_name": "model", "title": "Model", "description": "..."},
    ],
    auto_start=False
))
```

See [references/wigglystuff.md](references/wigglystuff.md) for all widgets.

## Best Practices

1. **Wrap reusable code in functions** - Keeps intermediate variables local
2. **Use meaningful, unique variable names** - e.g., `model1_sigma`, `model2_sigma`
3. **Don't mutate across cells** - Mutate in same cell or create new variables
4. **Write idempotent cells** - Same inputs produce same outputs
5. **Use mo.stop()** - Gate expensive operations behind conditions/buttons
6. **Use lazy loading** - `mo.lazy()` for expensive components in tabs/accordions
7. **Cache expensive ops** - `@mo.cache` for session, `@mo.persistent_cache` for disk

## CRITICAL: Pre-Edit Checklist

**BEFORE making ANY edit to a marimo notebook:**

1. **Read the current file state** — The file may have been modified by marimo's editor
2. **Run `marimo check notebook.py`** — Verify valid before and after edits

**AFTER completing edits:**

3. **Grep for `print(`** — Replace ALL print statements with marimo output (`mo.md()`, `mo.stat()`, `mo.callout()`)
4. **Run `marimo check notebook.py`** — Verify no errors introduced

## Common Gotchas

### Output & Display

- **NEVER use print() in cells**: Print statements do NOT display in run mode. Always use:
  - `mo.md(f"**Label:** {value}")` — formatted text
  - `mo.stat(value=f"{x}", label="Label")` — metric cards
  - `mo.callout(content, kind="info")` — callout boxes
  - Return the dataframe/object directly — automatic display

- **mo.show_code() must be called as a statement, not in return**

- **Never delete output without replacing**: When removing print statements, replace with equivalent marimo output

### Reactivity & Variables

- **Closures in loops**: Use default args `lambda v, i=i: ...` not `lambda v: ... i`
- **on_change handlers**: Only work if element is bound to global variable
- **Dynamic UI elements**: Must wrap in `mo.ui.array()`, `mo.ui.dictionary()`, or `mo.ui.batch()`
- **Type annotations**: Registered as references unless quoted: `x: "SomeType"`

### Libraries

- **matplotlib cut-off**: Call `plt.tight_layout()` before outputting
- **dotenv**: Use `dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True))`

## References

- **UI components**: [references/ui_components.md](references/ui_components.md)
- **Wigglystuff widgets**: [references/wigglystuff.md](references/wigglystuff.md)
- **Caching patterns**: [references/caching.md](references/caching.md)
- **Advanced features**: [references/advanced.md](references/advanced.md) (SQL, deployment, testing, routing)
- **Official docs**: https://docs.marimo.io

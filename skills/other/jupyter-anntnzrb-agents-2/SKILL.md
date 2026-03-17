---
name: jupyter
description: "Work with Jupyter notebooks without leaving Claude Code. Execute cells, inspect outputs, validate structure, and convert formats. Activate when working with .ipynb files, user mentions notebooks, Jupyter, or needs to run/debug notebook code."
---

# Jupyter Notebook Skill

Execute, inspect, and manage Jupyter notebooks directly from Claude Code. Eliminates the context-switching loop between CLI and browser.

## Workflow

```
1. INSPECT  → Understand notebook structure (nb.py inspect)
2. EDIT     → Modify cells with NotebookEdit tool
3. EXECUTE  → Run cells and capture outputs (nb.py execute -i)
4. VERIFY   → Read outputs, check for errors (nb.py show --output-only)
5. ITERATE  → Repeat until complete
```

## Setup (One-Time)

```bash
# Install a Jupyter kernel (needed for execution)
uv run --with ipykernel python -m ipykernel install --user --name python3
```

## Scripts

Located in this skill's `scripts/` directory:

| Script | Purpose | Dependencies |
|--------|---------|--------------|
| `nb.py` | Full notebook CLI | nbformat, nbclient, nbconvert |
| `validate.py` | Quick syntax check | nbformat only |

Both scripts are executable with inline dependencies (PEP 723) - uv handles everything automatically.

## CLI Reference

```bash
# Inspect structure
nb.py inspect notebook.ipynb

# Show cell contents
nb.py show notebook.ipynb
nb.py show notebook.ipynb -c 0,2-4      # specific cells
nb.py show notebook.ipynb -o            # include outputs
nb.py show notebook.ipynb --output-only # outputs only
nb.py show notebook.ipynb -o --save-images ./images/  # save images to dir

# Execute cells
nb.py execute notebook.ipynb            # all cells, show output
nb.py execute notebook.ipynb -i         # save outputs back to file
nb.py execute notebook.ipynb -c 0,2-4   # specific cells
nb.py execute notebook.ipynb --save-images ./outputs/  # save images

# Search cells
nb.py grep "import pandas" notebook.ipynb      # find cells with pattern
nb.py grep -i "def.*function" notebook.ipynb   # case-insensitive regex
nb.py grep -C "pattern" notebook.ipynb         # show full cell context
nb.py grep --cells-only "pattern" notebook.ipynb  # just cell indices

# Validate (lightweight - only needs nbformat)
validate.py notebook.ipynb

# Convert
nb.py convert notebook.ipynb --to py
nb.py convert notebook.ipynb --to html -o output.html

# Clear outputs
nb.py clear notebook.ipynb
```

## Quick Patterns

### Execute and Read Outputs (No Browser Needed)

```bash
# Execute all cells, save outputs back to file
nb.py execute notebook.ipynb -i

# Then show just the outputs
nb.py show notebook.ipynb --output-only
```

### Debug a Failing Cell

```bash
# Execute up to the failing cell
nb.py execute notebook.ipynb -c 0-5 --allow-errors

# Inspect the error output
nb.py show notebook.ipynb -c 5 -o
```

### Edit Cell (Built-in Tool)

Use Claude's `NotebookEdit` tool to modify cells:
- `cell_id`: The cell ID or index
- `new_source`: New cell content
- `edit_mode`: "replace", "insert", or "delete"
- `cell_type`: "code" or "markdown"

### Validate Before Commit

```bash
# Quick syntax check (lightweight deps)
validate.py notebook.ipynb

# Clear outputs for clean commits
nb.py clear notebook.ipynb
```

## Tool Integration

| Task | Tool |
|------|------|
| Read notebook structure | `nb.py inspect` |
| Read cell contents | `nb.py show` or `read` tool |
| Edit cells | `NotebookEdit` tool |
| Execute cells | `nb.py execute` |
| View outputs | `nb.py show -o` or `--output-only` |
| Search cells | `nb.py grep` |
| Extract images | `nb.py show -o --save-images DIR` |
| Validate syntax | `validate.py` (fast) or `nb.py validate` |
| Convert formats | `nb.py convert` |

## References

- [reference.md](reference.md) - Notebook structure, execution model, best practices
- [cookbook/workflows.md](cookbook/workflows.md) - Common workflow recipes
- [cookbook/troubleshooting.md](cookbook/troubleshooting.md) - Error handling and debugging

---
name: jupyter-notebook-patterns
description: Reproducible notebook workflows, clean diffs, parameterized execution, testing, and notebook-to-script conversion.
---

# Jupyter Notebook Patterns

## When to Use

### Notebook vs Script Decision Table

| Scenario | Notebook | Script | Hybrid |
|---|---|---|---|
| Exploratory analysis, one-off | Yes | | |
| Production data pipeline | | Yes | |
| Report with inline visuals | Yes | | |
| Shared team utility | | Yes | |
| Parameterized batch runs | | | Papermill |
| ML experiment tracking | Yes | | |
| CI/CD artifact generation | | | nbconvert |
| Code review required | | Yes | nbstripout + notebook |

## Clean Diffs with nbstripout

Notebook JSON includes execution counts, cell outputs, and metadata noise. Strip it.

### Git Filter Setup

```bash
# Install
pip install nbstripout

# Configure for repo (writes to .gitattributes + .git/config)
nbstripout --install

# Or configure globally
nbstripout --install --global

# Verify
cat .gitattributes
# *.ipynb filter=nbstripout
```

### Manual .gitattributes (when you need custom config)

```gitattributes
*.ipynb filter=nbstripout
*.ipynb diff=ipynb
```

### Pre-commit hook alternative

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout
        args: [--extra-keys, "metadata.kernelspec metadata.language_info"]
```

The `--extra-keys` flag strips kernel metadata that causes spurious diffs across environments.

## Parameterized Execution with Papermill

### Basic Parameterized Notebook

Tag a cell with `parameters` in notebook metadata. Papermill injects a new cell after it.

```python
# Cell tagged "parameters"
input_path = "data/default.csv"
n_samples = 1000
model_type = "xgboost"
output_dir = "results/"
```

### Execute Programmatically

```python
import papermill as pm

pm.execute_notebook(
    "template.ipynb",
    "output/run_2024_01.ipynb",
    parameters={
        "input_path": "data/january.csv",
        "n_samples": 5000,
        "model_type": "lightgbm",
        "output_dir": "results/january/",
    },
    kernel_name="python3",
    cwd=".",  # working directory for execution
)
```

### Batch Execution Pattern

```python
from pathlib import Path
import papermill as pm

configs = [
    {"input_path": f"data/{m}.csv", "month": m}
    for m in ["jan", "feb", "mar"]
]

for cfg in configs:
    output = Path(f"output/{cfg['month']}_report.ipynb")
    output.parent.mkdir(parents=True, exist_ok=True)
    pm.execute_notebook(
        "template.ipynb",
        str(output),
        parameters=cfg,
        request_save_on_cell_execute=True,  # checkpoint after each cell
    )
```

## Notebook-to-Script Conversion

### nbconvert CLI

```bash
# To Python script
jupyter nbconvert --to script notebook.ipynb

# To HTML report (execute first)
jupyter nbconvert --to html --execute notebook.ipynb --no-input

# To PDF (requires xelatex)
jupyter nbconvert --to pdf notebook.ipynb
```

### Programmatic Conversion

```python
from nbconvert import PythonExporter
import nbformat

nb = nbformat.read("analysis.ipynb", as_version=4)
exporter = PythonExporter()
script, _ = exporter.from_notebook_node(nb)

# Strip "# In[...]" markers
import re
script = re.sub(r"# In\[.*?\]:\n", "", script)

Path("analysis.py").write_text(script)
```

### jupytext for Round-Trip Sync

```bash
# Pair notebook with .py percent format
jupytext --set-formats ipynb,py:percent notebook.ipynb

# Sync after editing either file
jupytext --sync notebook.ipynb
```

## Testing Notebooks

### conftest.py for Notebook Execution Tests

```python
# tests/conftest.py
import subprocess
import pytest
from pathlib import Path

NOTEBOOK_DIR = Path("notebooks")

def collect_notebooks():
    return sorted(NOTEBOOK_DIR.glob("*.ipynb"))

@pytest.fixture(params=collect_notebooks(), ids=lambda p: p.stem)
def notebook_path(request):
    return request.param

def execute_notebook(path, timeout=300):
    """Execute notebook and return exit code."""
    result = subprocess.run(
        [
            "jupyter", "nbconvert",
            "--to", "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=" + str(timeout),
            "--output", "/dev/null",
            str(path),
        ],
        capture_output=True,
        text=True,
    )
    return result
```

### Test File

```python
# tests/test_notebooks.py
def test_notebook_executes(notebook_path):
    result = execute_notebook(notebook_path)
    assert result.returncode == 0, (
        f"Notebook {notebook_path.name} failed:\n{result.stderr[-500:]}"
    )
```

### Targeted Cell Testing with testbook

```python
from testbook import testbook

@testbook("notebooks/preprocessing.ipynb", execute=["setup", "clean_data"])
def test_cleaning_removes_nulls(tb):
    df = tb.ref("df_clean")
    assert df.isnull().sum().sum() == 0
```

## Gotchas and Anti-Patterns

### Hidden State Bugs
- **Problem**: Running cells out of order creates unreproducible state.
- **Fix**: `Kernel > Restart & Run All` before any commit or share. Automate with `--execute` in CI.

### Out-of-Order Execution
- **Problem**: Cell 5 depends on cell 10's output because you ran them manually out of order.
- **Fix**: Structure notebooks linearly. Use `nbval` or `--execute` in CI to catch this.

### Large Notebooks in Git
- **Problem**: Output cells with images/dataframes bloat repo history.
- **Fix**: nbstripout (above). For intentional output storage, use `nbconvert --to html` and store HTML artifacts instead.

### Kernel Dependency Drift
- **Problem**: `\!pip install` inside notebooks creates unreproducible environments.
- **Fix**: Pin deps in `requirements.txt` or `pyproject.toml`. Use `%pip install` (not `\!pip`) if you must install in-notebook -- it targets the correct kernel.

### Import Spaghetti
- **Problem**: Imports scattered across cells, hard to extract to scripts.
- **Fix**: First code cell = all imports. Tag it for Papermill to skip if needed.

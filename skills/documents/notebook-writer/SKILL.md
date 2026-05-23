---
name: notebook-writer
description: Create and document Jupyter notebooks for reproducible analyses
success_criteria:
  - Notebook structured with clear sections and narrative
  - Code cells properly documented with explanatory markdown
  - Reproducibility ensured (can run end-to-end)
  - Environment requirements documented
  - Outputs properly displayed and interpreted
  - Git-friendly format (Jupytext markdown)
---

# Notebook Writer Skill

You are a specialist in creating well-structured Jupyter notebooks for scientific analyses and documentation.

## When to Use This Skill

Use this skill when:
- Creating parameter sweeps or sensitivity analyses
- Documenting calculations with reproducible code
- Generating analysis reports that combine code, results, and interpretation
- Packaging agent work (Calculator, Researcher) into shareable notebooks

## Notebook Format: Jupytext Markdown

We use **Jupytext-compatible Markdown** for notebooks to enable git-friendly version control.

### Cell Markers

- **Markdown cells**: Regular Markdown text (no special marker)
- **Code cells**: Start with `# %%` on its own line

### Example Structure

```markdown
---
jupyter:
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
---

# Analysis Title

Brief description of what this notebook does.

## Section 1: Data Loading

# %%
import pandas as pd
import numpy as np

# %%
data = pd.read_csv('data.csv')
data.head()

## Section 2: Analysis

Explanation of the analysis approach.

# %%
# Perform calculation
result = np.mean(data['value'])
print(f"Mean: {result:.2f}")
```

## Python Utility API

Many projects provide `src/utils/notebook_builder.py` with helper functions for programmatic notebook creation.

### Core Function: create_notebook_markdown

```python
create_notebook_markdown(
    title: str,
    cells: List[Dict[str, str]],
    output_path: Path,
    kernelspec: Optional[Dict] = None
) -> Path
```

**Parameters:**
- `title`: Notebook title (becomes H1 header)
- `cells`: List of dicts with `'type'` (`'code'` or `'markdown'`) and `'content'`
- `output_path`: Where to save `.md` file
- `kernelspec`: Optional kernel specification (defaults to Python 3)

**Example:**
```python
from pathlib import Path
from src.utils.notebook_builder import create_notebook_markdown

cells = [
    {'type': 'markdown', 'content': '## Introduction\n\nThis analysis...'},
    {'type': 'code', 'content': 'import numpy as np'},
    {'type': 'code', 'content': 'x = np.linspace(0, 10)\nprint(x)'}
]

create_notebook_markdown(
    title="My Analysis",
    cells=cells,
    output_path=Path('docs/analysis/my_analysis.md')
)
```

### Template: Parameter Sweep

```python
create_parameter_sweep_notebook(
    param_name: str,
    param_range: str,
    calculation_code: str,
    output_path: Path
) -> Path
```

Creates a notebook with:
- Imports (numpy, matplotlib, pandas)
- Parameter range definition
- Your calculation code
- Visualization boilerplate

**Example:**
```python
from pathlib import Path
from src.utils.notebook_builder import create_parameter_sweep_notebook

create_parameter_sweep_notebook(
    param_name='temperature',
    param_range='np.linspace(20, 40, 20)',
    calculation_code='''
# Reaction rate calculation
results = []
for T in temperature_values:
    rate = arrhenius_equation(T, activation_energy)
    results.append(rate)
''',
    output_path=Path('analysis/temperature_sweep.md')
)
```

### Template: Analysis Report

```python
create_analysis_report_notebook(
    analysis_title: str,
    sections: List[Dict[str, str]],
    output_path: Path
) -> Path
```

**Section dict keys:**
- `title`: Section heading (required)
- `description`: Explanatory text (optional)
- `code`: Code to execute (optional)
- `interpretation`: Results interpretation (optional)

**Example:**
```python
from src.utils.notebook_builder import create_analysis_report_notebook

sections = [
    {
        'title': 'Model Setup',
        'description': 'Define parameters',
        'code': 'diffusion_coeff = 2.1e-5  # cm²/s'
    },
    {
        'title': 'Calculation',
        'code': 'result = compute_model(diffusion_coeff)',
        'interpretation': 'Result shows X is dominated by Y'
    }
]

create_analysis_report_notebook(
    'Transport Analysis',
    sections,
    Path('analysis/transport.md')
)
```

### Validation Function

```python
validate_notebook(notebook_path: Path) -> bool
```

Validates `.ipynb` structure using nbformat. Returns `True` if valid, raises exception if invalid.

**Example:**
```python
from pathlib import Path
from src.utils.notebook_builder import validate_notebook

validate_notebook(Path('analysis/notebook.ipynb'))
# Returns True or raises ValidationError
```

## Workflow

1. **Create notebook** using utility or manual Markdown
2. **Edit `.md` file** directly (agents write Markdown well)
3. **Convert to `.ipynb`**: `python3 -m jupytext --to ipynb notebook.md`
4. **Run in Jupyter**: `jupyter notebook notebook.ipynb`
5. **Sync changes back**: `python3 -m jupytext --sync notebook.ipynb` (bidirectional)

## Jupyter AI Integration

Modern Jupyter environments (JupyterLab 4.0+, JetBrains IDEs) provide AI-powered assistance to enhance productivity and reduce errors.

### %%ai Magic Commands

The `%%ai` cell magic enables AI-powered code generation and analysis directly in notebooks:

```python
# %%
# %load_ext jupyter_ai_magics

# %%
%%ai chatgpt
Generate a function to calculate the Pearson correlation coefficient between two arrays
```

**Key use cases:**
- **Code generation**: Generate boilerplate code, data transformations, or analysis functions
- **Data exploration**: Ask questions about DataFrames or arrays
- **Debugging assistance**: Get suggestions for fixing errors
- **Documentation**: Generate docstrings or explanations

### Providing Context for Better Results

AI assistants work best when given relevant context. **Always provide**:

1. **API documentation**: For specialized libraries (scanpy, pydeseq2, biopython)
   ```python
   # Include relevant API documentation in a markdown cell
   # Example: scanpy.pp.filter_cells(data, min_genes=200)
   ```

2. **Dataset descriptions**: Shape, columns, data types
   ```python
   # Document your data structure:
   # RNA-seq counts matrix: 20,000 genes × 5,000 cells
   # AnnData object: .X (sparse CSR matrix), .obs (cell metadata), .var (gene metadata)
   ```

3. **Domain context**: Biological meaning, expected ranges, units
   ```python
   # Oxygen consumption rate: 10-20 pmol/s/million cells
   # Temperature: 37°C, pH: 7.4
   ```

### Chat UI Assistance

JupyterLab's chat interface provides conversational help:

**Best practices:**
- Use for exploratory questions: "What's the best way to normalize this data?"
- Ask for code review: "Does this analysis handle missing values correctly?"
- Request visualizations: "Create a heatmap of the top 50 variable genes"
- Get explanations: "Explain what this cell is doing"

### When to Use AI Assistance vs. Manual Coding

**Use AI assistance for:**
- Boilerplate code (imports, data loading templates)
- Exploratory analysis (quick plots, summary statistics)
- Learning new library syntax
- Generating test data or examples

**Write code manually for:**
- Core analysis logic (hypothesis testing, modeling)
- Publication-quality figures (fine-grained control needed)
- Performance-critical sections (AI-generated code may not be optimal)
- Complex domain-specific algorithms

**Warning**: Always verify AI-generated code. Check for:
- Correct library syntax (APIs change frequently)
- Appropriate statistical methods (AI may suggest invalid tests)
- Proper handling of biological data (species, units, measurement context)

### JetBrains AI Assistant

For notebooks in PyCharm/DataSpell:

**Features:**
- **Explain cell**: Understand what code does (Alt+Enter → "Explain")
- **Create visualization**: Generate plots from data descriptions
- **Edit cell**: Refactor or improve code (Alt+Enter → "AI Actions")
- **Fix errors**: Get suggestions for runtime errors

**Access**: Right-click cell → "AI Assistant" or use AI chat sidebar

## Jupytext Configuration

Projects should include `.jupytext.toml` in repository root:

```toml
# Jupytext configuration
# Enables git-friendly notebook version control

# Pair markdown and ipynb files
# Use myst format which supports # %% cell markers
formats = "md:myst,ipynb"
```

This tells Jupytext to:
- Recognize `.md` files as notebooks
- Use MyST Markdown format (supports `# %%` markers)
- Auto-sync with `.ipynb` when either is modified

## Git Tracking Strategy

**Recommended `.gitignore` configuration:**
```gitignore
# Track .md notebooks (Jupytext source), ignore generated .ipynb files
*.ipynb
.ipynb_checkpoints/
```

**What's tracked:**
- ✅ `.md` notebook files (human-readable source)
- ❌ `.ipynb` files (generated, binary JSON)
- ❌ `.ipynb_checkpoints/` (Jupyter temp files)

**Rationale:** `.md` files produce readable git diffs. `.ipynb` files are JSON with embedded outputs and can be regenerated from `.md`.

## Common Operations

### Create from scratch (manual)
1. Write Markdown file with `# %%` markers
2. Add YAML frontmatter (kernel info)
3. Convert: `python3 -m jupytext --to ipynb file.md`

### Convert existing notebook to Markdown
```bash
python3 -m jupytext --to md:myst notebook.ipynb
```

### Edit existing notebook
**Option 1: Edit .md file directly** (recommended for agents)
```bash
# Edit notebook.md in text editor
# Then convert:
python3 -m jupytext --to ipynb notebook.md
```

**Option 2: Edit in Jupyter, sync back**
```bash
jupyter notebook notebook.ipynb
# Make changes in Jupyter
# Sync back to .md:
python3 -m jupytext --sync notebook.ipynb
```

### Validate structure
```bash
python3 -c "
from pathlib import Path
from src.utils.notebook_builder import validate_notebook
validate_notebook(Path('notebook.ipynb'))
print('✓ Valid')
"
```

### Convert multiple notebooks
```bash
# Convert all .md notebooks in a directory
python3 -m jupytext --to ipynb analysis/*.md

# Or sync all paired notebooks
python3 -m jupytext --sync analysis/*.ipynb
```

## Best Practices

1. **Title every notebook** with clear purpose
2. **Start with imports** in first code cell
3. **Explain calculations** with markdown cells before code
4. **Interpret results** with markdown cells after code
5. **Use meaningful variable names** (not x, y, z)
6. **Include units** in comments and axis labels
7. **Save outputs** (figures) to files for documentation

## Reproducibility Standards

Scientific notebooks must be fully reproducible. Every notebook should enable another researcher to:
1. Recreate your computational environment
2. Rerun your analysis and get identical results
3. Understand your data sources and processing steps

### Environment Documentation

**Every notebook must include an environment documentation cell:**

```python
# %%
# Environment Information
# Run: pip freeze > requirements.txt
# Or: conda env export > environment.yml

import sys
import numpy as np
import pandas as pd
import scanpy as sc  # Example for single-cell analysis

print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")
print(f"Pandas: {pd.__version__}")
print(f"Scanpy: {sc.__version__}")

# Include this output in your notebook for documentation
```

**Create environment files:**

```bash
# For pip users:
pip freeze > requirements.txt

# For conda users:
conda env export > environment.yml

# Include these files in your repository
```

**Document kernel selection:**
```markdown
## Computational Environment

- **Kernel**: Python 3.11 (project-env)
- **Dependencies**: See `requirements.txt` for full package list
- **Critical packages**: scanpy==1.10.0, numpy==1.26.3, pandas==2.2.0
```

### Random Seed Setting

**For any stochastic process, set random seeds:**

```python
# %%
# Set random seeds for reproducibility
import numpy as np
import random

RANDOM_SEED = 42  # Document why this value was chosen (convention, previous analysis, etc.)

np.random.seed(RANDOM_SEED)
random.seed(RANDOM_SEED)

# For machine learning:
import torch
torch.manual_seed(RANDOM_SEED)

# For scanpy:
import scanpy as sc
sc.settings.seed = RANDOM_SEED

print(f"Random seed set to {RANDOM_SEED}")
```

**Stochastic processes requiring seeds:**
- UMAP, t-SNE (dimensionality reduction)
- Random forest, neural networks (machine learning)
- Monte Carlo simulations
- Random sampling or bootstrapping
- Graph algorithms with random initialization

### Session Info Output

**End every notebook with a session info cell:**

```python
# %%
# Session Information (for reproducibility)
import session_info

session_info.show(
    dependencies=True,
    html=False
)

# Alternative for single-cell analysis:
# import scanpy as sc
# sc.logging.print_versions()
```

This captures:
- Python version
- Operating system
- Package versions (all dependencies)
- Execution timestamp

### File Path Best Practices

**Use relative paths and variables:**

```python
# %%
from pathlib import Path

# Define paths at the top of the notebook
DATA_DIR = Path("data/raw")
RESULTS_DIR = Path("results/analysis_2025-01-29")

# Ensure output directories exist
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Use variables throughout
input_file = DATA_DIR / "counts.csv"
output_file = RESULTS_DIR / "normalized_counts.csv"
```

**Never use hardcoded absolute paths:**
```python
# BAD:
data = pd.read_csv("/Users/yourname/project/data.csv")

# GOOD:
data = pd.read_csv(DATA_DIR / "data.csv")
```

### Reproducibility Checklist

Before sharing or archiving a notebook:
- [ ] Environment documented (Python version, key package versions)
- [ ] `requirements.txt` or `environment.yml` exists and is current
- [ ] Random seeds set for all stochastic processes
- [ ] Session info cell at end of notebook
- [ ] File paths use variables (not hardcoded)
- [ ] Data sources documented (where to download, version, date)
- [ ] Notebook runs end-to-end without errors (Restart & Run All)
- [ ] Results match expected output (if re-running existing analysis)

**Integration with other skills:**
- **notebook-debugger**: Use to verify end-to-end execution
- **bioinformatician**: Apply reproducibility standards to all computational biology analyses
- **copilot**: Review notebooks for reproducibility compliance

## Project-Specific Usage

Many projects have a `docs/NOTEBOOK-WORKFLOW.md` or similar document with project-specific examples and patterns. Check your project's documentation for:
- Domain-specific notebook templates
- Agent integration patterns (which skills create notebooks)
- Directory structure conventions (where to save notebooks)
- Project-specific best practices

## Troubleshooting

### Issue: Jupytext can't find format

**Error:** `Format 'percent' is not associated to extension '.md'`

**Fix:** Use `md:myst` format in `.jupytext.toml` (not `md:percent`). MyST Markdown supports `# %%` markers.

```toml
formats = "md:myst,ipynb"  # Correct
```

### Issue: Sync not working

**Symptom:** Changes to `.ipynb` don't appear in `.md`

**Solution:**
1. Check `.jupytext.toml` exists and has correct format
2. Run sync explicitly: `python3 -m jupytext --sync notebook.ipynb`
3. Check both files exist (create `.md` first if needed)

### Issue: Validation fails

**Error:** `nbformat.ValidationError`

**Causes:**
- Missing cell IDs (required in nbformat v4.5+)
- Invalid JSON structure
- Missing required fields

**Solution:** Use `notebook_builder.py` utility functions which handle validation automatically.

### Issue: Git shows .ipynb files

**Symptom:** `.ipynb` files appearing in `git status`

**Fix:** Ensure `.gitignore` contains `*.ipynb`. Check with:
```bash
git check-ignore -v notebook.ipynb
```

## Error Prevention

### Common Issues

1. **Missing `# %%`**: Code cells must start with this marker
2. **Frontmatter syntax**: YAML header must be exact (see example structure above)
3. **Path handling**: Use `Path` objects, ensure directories exist
4. **Cell validation**: Use `notebook_builder.validate_notebook()` after creation

### Validation Checklist

Before finalizing a notebook:
- [ ] Frontmatter present with kernelspec
- [ ] All code cells have `# %%` marker
- [ ] Imports in first code cell
- [ ] Results interpreted with markdown
- [ ] Saved to appropriate location
- [ ] Validated with nbformat if creating .ipynb directly

## Dependencies

**Required packages:**
```bash
pip3 install jupytext nbformat
```

**Check installation:**
```bash
pip3 list | grep -E "(jupytext|nbformat)"
```

**Tested versions:**
- jupytext: 1.19+
- nbformat: 5.10+
- Python: 3.9+

## Integration with Other Skills

Common patterns for skill integration:
- **Quantitative analysis skills**: Package calculations as reproducible notebooks with parameter sweeps
- **Research skills**: Document literature-derived parameters with citations in data notebooks
- **Planning skills**: Generate protocol notebooks with expected results and analysis templates
- **Review skills**: Check notebook code for correctness and best practices

---

Remember: Notebooks are for **interactive exploration** and **reproducible documentation**. For production code, use Python modules in `src/`.

**For project-specific examples and patterns**, see your project's documentation (often `docs/NOTEBOOK-WORKFLOW.md` or similar).

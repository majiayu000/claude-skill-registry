---
name: notebook-ml-architect
description: >
  Expert guidance for auditing, refactoring, and designing machine learning
  Jupyter notebooks with production-quality patterns. Use when:
  (1) Analyzing notebook structure and identifying anti-patterns,
  (2) Detecting data leakage and reproducibility issues,
  (3) Refactoring messy notebooks into modular pipelines,
  (4) Generating templates for ML workflows (EDA, classification, experiments),
  (5) Adding reproducibility instrumentation (seeding, logging, env capture),
  (6) Converting notebooks to Python scripts,
  (7) Generating experiment summary reports.
  Triggers on: ML notebook, Jupyter audit, notebook refactor, data leakage,
  experiment template, ipynb best practices, notebook to script, reproducibility.
---

# Notebook ML Architect

Expert guidance for production-quality ML notebooks.

## Quick Reference

| Operation | Use Case |
|-----------|----------|
| **audit** | Analyze notebook for anti-patterns, leakage, reproducibility issues |
| **refactor** | Transform notebook into modular Python pipeline |
| **template** | Generate new notebook from EDA/classification/experiment template |
| **report** | Create markdown summary from executed notebook |
| **convert** | Extract Python script from notebook |

## Audit Workflow

When auditing a notebook:

1. **Read the notebook** using the Read tool
2. **Check structure** against [ml-workflow-guide.md](references/ml-workflow-guide.md)
3. **Detect anti-patterns** using [anti-patterns.md](references/anti-patterns.md)
4. **Check for data leakage** using [leakage-checklist.md](references/leakage-checklist.md)
5. **Run analysis script** if deeper inspection needed:
   ```bash
   python scripts/analyze_notebook.py <notebook.ipynb>
   ```

### Audit Checklist

- [ ] **Execution order**: Cells numbered sequentially (no gaps, no out-of-order)
- [ ] **Random seeds**: Set early (np.random.seed, torch.manual_seed, random.seed)
- [ ] **Imports at top**: All imports in first code cell(s)
- [ ] **No hardcoded paths**: Use relative paths or config variables
- [ ] **Train/test split**: Clear separation before any modeling
- [ ] **No data leakage**: Pre-processing after split, no test data peeking
- [ ] **Modularization**: Functions/classes for reusable logic
- [ ] **Dependencies documented**: requirements.txt or environment.yml referenced

### Severity Levels

- **CRITICAL**: Data leakage, missing train/test split, results unreproducible
- **HIGH**: No seeds, hardcoded paths, execution order issues
- **MEDIUM**: Missing modularization, no dependency docs
- **LOW**: Naming conventions, missing comments, style issues

## Refactoring Guide

Transform notebooks into production pipelines:

### Step 1: Identify Sections
Look for markdown headers that indicate logical sections:
- Data loading
- Preprocessing
- Feature engineering
- Model definition
- Training
- Evaluation

### Step 2: Extract Functions
Convert repeated or complex cell code into functions:
```python
# Before: inline code
df = pd.read_csv('data.csv')
df = df.dropna()
df['feature'] = df['a'] * df['b']

# After: function
def load_and_prepare_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna()
    df['feature'] = df['a'] * df['b']
    return df
```

### Step 3: Create Module Structure
```
project/
├── data.py          # Data loading and preprocessing
├── features.py      # Feature engineering
├── model.py         # Model definition
├── train.py         # Training loop
├── evaluate.py      # Evaluation metrics
├── config.py        # Configuration parameters
└── main.py          # Pipeline entry point
```

### Step 4: Use convert script
```bash
python scripts/convert_to_script.py notebook.ipynb output.py --group-by-sections
```

## Template Generation

Generate new notebooks from templates:

### Available Templates

1. **EDA Template** (`assets/templates/eda_template.ipynb`)
   - Data loading, basic info, missing values, distributions, correlations

2. **Classification Template** (`assets/templates/classification_template.ipynb`)
   - Full supervised learning pipeline with evaluation metrics

3. **Experiment Template** (`assets/templates/experiment_template.ipynb`)
   - Parameterized notebook for experiment tracking

### Using Templates

Copy template to project and customize:
```bash
cp ~/.claude/skills/notebook-ml-architect/assets/templates/classification_template.ipynb ./my_experiment.ipynb
```

Or generate programmatically with modifications.

## Reproducibility Checklist

### Required Elements

1. **Random Seeds**
   Use the reproducibility header snippet:
   ```python
   # Copy from assets/snippets/reproducibility_header.py
   ```

2. **Environment Capture**
   ```python
   import sys
   print(f"Python: {sys.version}")
   for pkg in ['numpy', 'pandas', 'sklearn', 'torch']:
       try:
           mod = __import__(pkg)
           print(f"{pkg}: {mod.__version__}")
       except ImportError:
           pass
   ```

3. **Dependency File**
   ```bash
   pip freeze > requirements.txt
   # Or for conda:
   conda env export > environment.yml
   ```

4. **Data Versioning**
   - Record data source, download date, preprocessing steps
   - Use relative paths from project root
   - Consider DVC for large datasets

## MCP Tool Usage

### Context7 - Library API Lookups

When you need accurate API information:
```
1. Call resolve-library-id with library name
2. Call get-library-docs with the returned ID and topic
```

Examples:
- sklearn train_test_split parameters
- papermill execute_notebook options
- nbformat cell structure

### Exa Search - Current Best Practices

When you need up-to-date recommendations:
- Use `web_search_exa` for discovery
- Use `crawling_exa` to pull full content from good URLs
- Use `deep_search_exa` for focused queries

Examples:
- "PyTorch reproducibility best practices 2024"
- "How to handle class imbalance"
- "MLflow notebook integration"

### GitHub Search - Real-World Patterns

When you need to see how others do it:
```
searchGitHub with:
- query: specific code pattern
- language: ["Python"]
- path: ".ipynb" for notebooks
```

Examples:
- Production notebook seeding patterns
- Evaluation metric implementations
- Config management in notebooks

## Script Reference

### analyze_notebook.py

Parse notebook and extract structure:
```bash
python scripts/analyze_notebook.py <notebook.ipynb> [--output json|text]
```

Output includes:
- Cell counts by type
- Import statements
- Function/class definitions
- Detected issues

### run_notebook.py

Execute notebook with parameters:
```bash
python scripts/run_notebook.py input.ipynb output.ipynb \
  --params '{"learning_rate": 0.01, "epochs": 100}' \
  --timeout 3600
```

### convert_to_script.py

Extract Python from notebook:
```bash
python scripts/convert_to_script.py notebook.ipynb output.py \
  --include-markdown \
  --group-by-sections \
  --add-main
```

## Common Issues and Fixes

### Data Leakage

**Problem**: Preprocessing on full dataset before split
```python
# BAD
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Fits on all data
X_train, X_test = train_test_split(X_scaled)
```

**Fix**: Split first, fit on train only
```python
# GOOD
X_train, X_test = train_test_split(X)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)  # Transform only
```

### Hidden State

**Problem**: Variables from previous runs affect results
```python
# Cell 1 run multiple times
results.append(model.score(X_test, y_test))  # results grows each run
```

**Fix**: Initialize state in cell
```python
results = []  # Always start fresh
results.append(model.score(X_test, y_test))
```

### Missing Seeds

**Problem**: Different results each run
```python
X_train, X_test = train_test_split(X, y)  # Random each time
```

**Fix**: Set seeds explicitly
```python
SEED = 42
X_train, X_test = train_test_split(X, y, random_state=SEED)
```

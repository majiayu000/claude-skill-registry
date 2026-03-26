---
name: structured-content-storage
description: "Enforces structured, highly documented storage for all code and data projects. Auto-activates for: machine learning scripts, data processing, code creation, script modification. Ensures clean directories, comprehensive comments, documentation files (README, data dictionaries, process descriptions, change logs)."
---

# Structured Content Storage Skill

Ensures all created or processed content follows strict organizational and documentation standards with structured storage, comprehensive comments, and complete project documentation.

## When to Use This Skill

**AUTO-ACTIVATES** for any of these tasks:
- Writing machine learning training scripts
- Creating data processing or data cleaning scripts
- Developing any code that processes or transforms data
- Modifying existing structured projects or scripts
- Creating analysis scripts or computational workflows
- Building data pipelines or ETL processes
- Any code creation task that produces files or processes data

## Not For / Boundaries

- Pure conversational queries without code output
- Reading or analyzing existing code without modification
- Simple one-line fixes that don't affect project structure

**Required inputs**: If modifying existing projects, must first read and understand the original structure.

## Quick Reference

### Core Principles

**1. Structured Directory Layout**
```
project-name/
├── README.md                 # Project overview and directory guide
├── src/                      # Source code with detailed comments
│   ├── main.py              # Main entry point
│   └── utils.py             # Utility functions
├── data/                     # Data files
│   ├── raw/                 # Original data
│   ├── processed/           # Cleaned/transformed data
│   └── DATA_DICTIONARY.md   # Data field descriptions
├── docs/                     # Documentation
│   ├── PROCESS.md           # Step-by-step process description
│   └── CHANGELOG.md         # Modification history
├── outputs/                  # Results, models, reports
└── requirements.txt          # Dependencies
```

**2. Code Documentation Standards**
- Every function must have docstring explaining purpose, parameters, returns
- Complex logic must have inline comments explaining the "why"
- File headers must describe the file's purpose and main components
- Magic numbers must be explained or converted to named constants

**3. Required Documentation Files**

**README.md** must include:
- Project purpose and goals
- Directory structure explanation
- Setup and installation instructions
- Usage examples
- Dependencies

**PROCESS.md** must include:
- Step-by-step workflow description
- Data flow diagrams (text-based acceptable)
- Key decisions and rationale
- Expected inputs and outputs

**DATA_DICTIONARY.md** (for data projects) must include:
- Field name, type, description for each column
- Value ranges and constraints
- Data source and collection method
- Update frequency

**CHANGELOG.md** (for modifications) must include:
- Date and version
- What was changed and why
- Files affected
- Breaking changes or migration notes

**4. Modification Protocol**

When modifying existing structured projects:
1. Read and understand original structure
2. Maintain existing organizational patterns
3. Update all affected documentation
4. Add detailed entry to CHANGELOG.md
5. Update comments in modified code sections

### Common Patterns

**Pattern 1: ML Training Project Structure**
```
ml-training-project/
├── README.md                 # Project overview
├── src/
│   ├── train.py             # Training script with detailed comments
│   ├── model.py             # Model architecture
│   ├── data_loader.py       # Data loading utilities
│   └── evaluate.py          # Evaluation metrics
├── data/
│   ├── raw/                 # Original datasets
│   ├── processed/           # Preprocessed data
│   └── DATA_DICTIONARY.md   # Feature descriptions
├── models/                   # Saved model checkpoints
├── logs/                     # Training logs
├── docs/
│   ├── TRAINING_PROCESS.md  # Training methodology
│   └── MODEL_ARCHITECTURE.md # Model design decisions
└── requirements.txt
```

**Pattern 2: Data Cleaning Project Structure**
```
data-cleaning-project/
├── README.md
├── src/
│   ├── clean.py             # Main cleaning script
│   ├── validators.py        # Data validation functions
│   └── transformers.py      # Transformation utilities
├── data/
│   ├── raw/                 # Original data
│   ├── processed/           # Cleaned data
│   ├── DATA_DICTIONARY.md   # Field descriptions
│   └── QUALITY_REPORT.md    # Data quality metrics
├── docs/
│   └── CLEANING_PROCESS.md  # Cleaning steps and rationale
└── requirements.txt
```

**Pattern 3: Code Comment Template**
```python
"""
Module: data_processor.py
Purpose: Process and transform raw sensor data into analysis-ready format

Main components:
- DataLoader: Reads raw CSV files
- DataCleaner: Handles missing values and outliers
- DataTransformer: Applies normalization and feature engineering
"""

def clean_sensor_data(df, threshold=0.95):
    """
    Clean sensor data by removing outliers and handling missing values.

    Args:
        df (pd.DataFrame): Raw sensor data with columns [timestamp, sensor_id, value]
        threshold (float): Completeness threshold (0-1) for keeping sensors

    Returns:
        pd.DataFrame: Cleaned data with outliers removed and missing values imputed

    Process:
        1. Remove sensors with >5% missing data
        2. Detect outliers using IQR method (1.5 * IQR)
        3. Impute remaining missing values with forward fill
    """
    # Remove sensors with insufficient data
    # Threshold of 0.95 means sensor must have 95% valid readings
    completeness = df.groupby('sensor_id')['value'].count() / len(df)
    valid_sensors = completeness[completeness >= threshold].index
    df = df[df['sensor_id'].isin(valid_sensors)]

    # Detect and remove outliers using IQR method
    Q1 = df['value'].quantile(0.25)
    Q3 = df['value'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR  # Standard outlier detection threshold
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df['value'] >= lower_bound) & (df['value'] <= upper_bound)]

    # Forward fill remaining missing values
    # Assumes temporal continuity in sensor readings
    df = df.sort_values(['sensor_id', 'timestamp'])
    df['value'] = df.groupby('sensor_id')['value'].fillna(method='ffill')

    return df
```

**Pattern 4: CHANGELOG.md Entry Template**
```markdown
## [Version 1.2.0] - 2026-01-19

### Changed
- Modified `train.py:45-67` to add early stopping mechanism
  - Reason: Prevent overfitting on small validation sets
  - Added `patience` parameter (default=10 epochs)
  - Monitors validation loss instead of training loss

### Added
- New function `evaluate.py:calculate_confusion_matrix()`
  - Provides detailed classification metrics
  - Outputs confusion matrix visualization

### Fixed
- Fixed data loader bug in `data_loader.py:123`
  - Issue: Incorrect handling of missing timestamps
  - Solution: Added explicit timestamp validation and interpolation

### Files Affected
- `src/train.py` (lines 45-67, 89-92)
- `src/evaluate.py` (new function added)
- `src/data_loader.py` (line 123)
- `docs/TRAINING_PROCESS.md` (updated early stopping section)
```

## Examples

### Example 1: Creating ML Training Script

**Input**: "Create a script to train a neural network for image classification"

**Steps**:
1. Create structured directory layout with src/, data/, models/, docs/
2. Write `src/train.py` with comprehensive docstrings and inline comments
3. Create `README.md` with project overview and directory structure
4. Create `docs/TRAINING_PROCESS.md` describing training methodology
5. Create `docs/MODEL_ARCHITECTURE.md` explaining model design
6. Create `requirements.txt` with all dependencies
7. Add data dictionary if custom dataset is used

**Expected output**: Complete project structure with all documentation files, heavily commented code, and clear organization.

### Example 2: Creating Data Cleaning Script

**Input**: "Write a script to clean customer transaction data"

**Steps**:
1. Create structured directory with src/, data/raw/, data/processed/, docs/
2. Write `src/clean.py` with detailed comments explaining each cleaning step
3. Create `data/DATA_DICTIONARY.md` describing all fields before and after cleaning
4. Create `docs/CLEANING_PROCESS.md` with step-by-step cleaning methodology
5. Create `data/QUALITY_REPORT.md` with data quality metrics (completeness, validity)
6. Create `README.md` with usage instructions and directory guide
7. Add `requirements.txt`

**Expected output**: Structured project with comprehensive documentation of data transformations and quality metrics.

### Example 3: Modifying Existing Structured Project

**Input**: "Update the training script to add learning rate scheduling"

**Steps**:
1. Read existing project structure and understand organization
2. Read `src/train.py` to understand current implementation
3. Make targeted modifications to training loop
4. Add detailed comments explaining new scheduling logic
5. Update `docs/TRAINING_PROCESS.md` with new scheduling section
6. Create detailed CHANGELOG.md entry:
   - What changed (specific line numbers)
   - Why it changed (rationale)
   - How it affects training (expected impact)
7. Update README.md if usage instructions changed

**Expected output**: Modified code with preserved structure, updated documentation, and comprehensive change log.

## References

- `references/documentation-standards.md`: Detailed documentation requirements
- `references/directory-templates.md`: Standard directory structures for different project types
- `references/comment-guidelines.md`: Code commenting best practices
- `assets/templates/`: Ready-to-use project templates

## Maintenance

- Sources: Software engineering best practices, data science project standards, documentation conventions
- Last updated: 2026-01-19
- Known limits: Does not enforce specific coding style (PEP8, etc.) beyond documentation requirements

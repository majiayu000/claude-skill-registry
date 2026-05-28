---
name: excel-translation
version: "1.0.0"
category: data
description: "Excel Translation Skill"
---

# Excel Translation Skill

> Version: 1.0.0
> Category: Data Engineering
> Triggers: Translate Excel calculation files, Spanish to English conversion
> Tools: `scripts/python/translate_excel.py`

## Overview

This skill provides the capability to batch translate engineering calculation Excel files from Spanish to English. It uses a specialized dictionary of engineering terms and preserves the original file structure, formulas, and formatting.

## Capabilities

- **Batch Processing**: Translates all `.xlsx` files in a target directory.
- **Structure Preservation**: Maintains sheet names, cell locations, and formulas.
- **Engineering Vocabulary**: Uses a curated dictionary for accurate technical translation.
- **Safety**: Uses regex-based word boundary detection to prevent partial word replacement errors (e.g., preventing "DE" replacement inside "MODEL").

## Usage

### Command
```bash
python3 scripts/python/translate_excel.py
```

### Configuration
The script is currently configured to target:
`/mnt/github/workspace-hub/doris/62092_sesa/data/calculations`

To change the target, modify the `target_dir` variable in the `main()` function of the script.

### Dictionary
The translation dictionary is embedded in the script. To add new terms, update the `replacements` dictionary in `scripts/python/translate_excel.py`.

## Technical Details

- **Dependencies**: `openpyxl`
- **Logic**:
  1. Iterates through all `.xlsx` files in the target directory (skipping `*_en.xlsx`).
  2. Loads workbook using `openpyxl`.
  3. Translates sheet names (truncating to 31 chars if necessary).
  4. Iterates through all cells with string values.
  5. Applies regex-based replacement for short words and phrase-based replacement for longer terms.
  6. Saves the translated file with `_en.xlsx` suffix.

## Verification

After running the translation, verify the output files (ending in `_en.xlsx`) to ensure:
- Sheet names are legible and correct.
- Technical terms are translated correctly.
- No formula corruption occurred.

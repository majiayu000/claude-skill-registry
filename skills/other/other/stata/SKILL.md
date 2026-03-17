---
name: stata
description: This skill should be used when users need to write, review, or debug Stata code for data cleaning and analysis. Use this skill for tasks involving data import, variable management, data documentation, merging/appending datasets, creating analysis variables, and following IPA/DIME Analytics coding standards. This skill should be invoked when working with .do files, .dta files, or any Stata-related data processing tasks.
---

# Stata Data Cleaning and Analysis Skill

## Contents

- [Core Principles](#core-principles)
- [Project Configuration](#project-configuration)
- [Coding Standards Quick Reference](#coding-standards-quick-reference)
- [Data Cleaning Workflow](#data-cleaning-workflow)
- [Missing Values](#missing-values)
- [Common Operations](#common-operations)
- [Quality Checks](#quality-checks)
- [Troubleshooting](#troubleshooting)
- [References](#references)

## Core Principles

| Principle | Description |
|-----------|-------------|
| **Reproducible** | Code produces identical outputs when run multiple times |
| **Defensive** | Assert statements verify data meets expected conditions |
| **Documented** | Comments explain *why* decisions were made, not just *what* |
| **No PII** | Never process personally identifiable information with AI tools |

### Four-Stage Data Flow

1. **Import** - Combine data into Stata format, apply corrections, remove duplicates
2. **Deidentify** - Remove PII as early as possible
3. **Clean** - Standardize formats, verify consistency
4. **Construct** - Build analysis variables through merging/appending

## Project Configuration

### Do-File Header

```stata
* ==============================================================================
* Project: [Project Name]
* Purpose: [Brief description]
* Author: [Name]
* Created: [Date]
* ==============================================================================

clear all
set more off
version 17.0
set maxvar 5000  // Increase only if genuinely needed
```

### Path Setup

```stata
* Define paths in master do-file (use forward slashes)
global data   "$root/data"
global output "$root/output"

* Usage - always use globals, never cd
use "$data/raw/survey.dta", clear
save "$data/clean/survey_clean.dta", replace
```

## Coding Standards Quick Reference

### Variable Naming

| Prefix | Meaning | Example |
| -------- | --------- | --------- |
| `hh_` | Household | `hh_income` |
| `ind_` | Individual | `ind_age` |
| `bl_`/`el_` | Baseline/Endline | `bl_score` |
| `d_` | Dummy/indicator | `d_employed` |
| `n_` | Count | `n_children` |

### Command Abbreviations

| Safe to abbreviate | Never abbreviate |
| ------------------- | ------------------ |
| `gen`, `reg`, `lab`, `sum`, `tab` | `local`, `global`, `save`, `merge` |
| `bys`, `qui`, `noi`, `cap`, `forv` | `append`, `sort`, `drop`, `keep` |

### Conditionals

```stata
* Good - explicit and clear
replace status = 1 if (employed == 1) & !missing(income)
drop if missing(respondent_id)

* Bad - implicit or unclear
replace status = 1 if employed & income
drop if respondent_id >= .
```

### Line Breaking

```stata
regress income ///
    age i.education i.region ///
    if (sample == 1), ///
    vce(cluster village_id)
```

## Data Cleaning Workflow

### 1. Import and Inspect

```stata
import delimited "$data/raw/survey.csv", clear varnames(1)
describe
codebook, compact
```

### 2. Verify Identifiers

```stata
duplicates report respondent_id
duplicates tag respondent_id, gen(dup_flag)
* Investigate and resolve duplicates
isid respondent_id  // Assert uniqueness
```

### 3. Clean Variables

```stata
* Rename to convention
rename (q1 q2 q3) (resp_age resp_gender resp_education)

* Validate ranges
assert inrange(age, 0, 120) if !missing(age)

* Clean strings
replace name = strtrim(strproper(name))
```

### 4. Document

```stata
label var resp_age "Respondent age in years"
label define gender_lbl 1 "Male" 2 "Female"
label values resp_gender gender_lbl
notes _dta: "Cleaned on `c(current_date)'"
```

### 5. Save and Verify

```stata
compress
save "$data/clean/survey_clean.dta", replace
```

## Missing Values

### IPA Extended Missing Conventions

| Raw Code | Stata | Meaning |
| -------- | ------- | --------- |
| -99 | `.d` | Don't know |
| -98 | `.r` | Refused |
| -97 | `.n` | Not applicable |
| -96 | `.s` | Skipped |
| -95 | `.o` | Other missing |

### Recoding

```stata
* Using mvdecode (efficient)
mvdecode _all, mv(-99=.d \ -98=.r \ -97=.n \ -96=.s)

* Check missing patterns
misstable summarize
```

## Common Operations

### Merging

```stata
use "$data/clean/household.dta", clear
count
local pre_merge = r(N)

merge 1:1 hhid using "$data/admin/treatment.dta"
tab _merge
assert _merge != 2  // No unmatched using expected
keep if _merge == 3
drop _merge
```

### Appending

```stata
use "$data/clean/baseline.dta", clear
gen wave = 1
append using "$data/clean/endline.dta"
replace wave = 2 if missing(wave)
```

### Reshaping

```stata
* Wide to long
reshape long income_, i(hhid) j(year)
rename income_ income

* Long to wide
reshape wide income, i(hhid) j(year)
```

## Quality Checks

```stata
* Summary statistics
summarize, detail
tabstat income expenditure, stats(n mean sd min max)

* Outlier detection
egen income_std = std(income)
list hhid income if abs(income_std) > 3

* Cross-tabulation consistency
tab gender pregnant, missing
assert pregnant == . | pregnant == 0 if gender == 1
```

## Troubleshooting

### Assert Failures

1. Examine failing observations: `list if !(condition)`
2. Check for unexpected missing values
3. Verify data source and transformations
4. Document exceptions if valid

### Merge Issues

1. Check `_merge` distribution with `tab _merge`
2. Investigate unmatched: `list if _merge == 1` or `_merge == 2`
3. Verify key variable types match (string vs numeric)
4. Check for leading/trailing spaces in string keys

### Performance

1. Load only needed variables: `use var1 var2 using "data.dta"`
2. Reshape to long format before loops
3. Use `quietly` to suppress output in loops
4. Increase `maxvar` only when necessary

## References

### Project References

- [Coding Standards](references/coding_standards.md) - Complete DIME Analytics Stata standards
- [Data Cleaning Checklist](references/data_cleaning_checklist.md) - Step-by-step checklist
- [Missing Values Guide](references/missing_values.md) - IPA missing value conventions

### External Resources

- [IPA Data Cleaning Guide](https://data.poverty-action.org/data-cleaning/)
- [DIME Analytics Handbook](https://worldbank.github.io/dime-data-handbook/coding.html)
- [Stata Linter](https://github.com/worldbank/stata-linter)

### Linting

```bash
just lint-stata                      # Lint all do-files
just lint-stata-file scripts/01.do   # Lint specific file
```

### Common Packages

```stata
ssc install ietoolkit    // DIME tools
ssc install estout       // Tables
ssc install fre          // Frequencies
```

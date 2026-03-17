---
name: eln
description: Professional scientific documentation in org-mode electronic lab notebooks with date-based organization, comprehensive record-keeping of hypotheses, methods, results, reasoning, and outcomes for reproducible research
---

# Electronic Lab Notebook (ELN) Skill

This skill provides expert guidance for maintaining professional electronic lab notebooks using org-mode, following best practices for scientific documentation, reproducibility, and research integrity.

## When to Use This Skill

Use this skill when:
- Creating or updating lab notebook entries
- Documenting experiments, calculations, or analyses
- Recording hypotheses and experimental design
- Documenting computational workflows
- Summarizing results and drawing conclusions
- Organizing research notes chronologically
- Creating cross-references between related work
- Preparing documentation for publications or reports
- Ensuring reproducibility of scientific work
- Maintaining professional research records

## Core Principles of Scientific Documentation

### 1. Chronological Organization
Entries are organized by date in a hierarchical structure:
```
notebook/
├── 2025/
│   ├── 01-January/
│   │   ├── 2025-01-15.org
│   │   └── 2025-01-20.org
│   └── 02-February/
│       └── 2025-02-03.org
```

### 2. Complete Documentation
Each entry should contain:
- **What was done**: Detailed description of work
- **Why it was done**: Hypothesis, motivation, reasoning
- **How it was done**: Methods, procedures, parameters
- **What was observed**: Results, data, observations
- **What it means**: Analysis, interpretation, conclusions
- **Next steps**: Follow-up work, questions raised

### 3. Reproducibility
Documentation should enable anyone (including future you) to:
- Understand the reasoning behind decisions
- Reproduce the work exactly
- Access all data and code used
- Follow the chain of logic

### 4. Professional Standards
- Write clearly and professionally
- Be honest about failures and unexpected results
- Date and timestamp all entries
- Never delete or modify past entries (make corrections with new entries)
- Include sufficient detail for independent reproduction

## Org-Mode ELN Structure

### File Organization

#### Date-Based Files
Each day's work goes in a dated file:
```
2025-01-15.org    # Single day's work
```

#### Directory Structure
```
research-notebook/
├── 2025/
│   ├── 01-January/
│   │   ├── 2025-01-15.org
│   │   ├── 2025-01-16.org
│   │   └── data/
│   │       └── 2025-01-15/
│   │           ├── experiment_results.csv
│   │           └── analysis.png
│   └── 02-February/
├── templates/
│   ├── experiment-template.org
│   └── calculation-template.org
├── index.org          # Master index
└── README.org         # Project overview
```

### Entry Template Structure

```org
#+TITLE: Lab Notebook - 2025-01-15
#+AUTHOR: Your Name
#+DATE: [2025-01-15 Wed]
#+FILETAGS: :experiment:catalyst:
#+STARTUP: overview

* Daily Summary
Brief overview of what was accomplished today.

* Entry 1: Hypothesis Testing - CO Adsorption on Pt
:PROPERTIES:
:ID: 2025-01-15-001
:PROJECT: Catalyst_Screening
:STATUS: In_Progress
:RELATED: [[file:2025-01-10.org::*Previous Results]]
:END:

** Objective
What are you trying to accomplish and why?

** Hypothesis
Clear statement of what you expect and the reasoning.

** Background/Context
- Why is this important?
- What previous work led to this?
- What are the key questions?

** Methods
*** Computational Setup
Detailed description of how the work was performed.

#+BEGIN_SRC python
# Include actual code used
from ase.build import fcc111
slab = fcc111('Pt', size=(4,4,4), vacuum=10.0)
#+END_SRC

*** Parameters
- DFT functional: PBE
- Energy cutoff: 400 eV
- k-points: 4×4×1
- Convergence: 0.05 eV/Å

** Results
*** Observations
What actually happened? Include data, figures, output.

#+BEGIN_SRC python :results file
# Analysis code
import matplotlib.pyplot as plt
# ... plotting code ...
plt.savefig('data/2025-01-15/adsorption_energy.png')
return 'data/2025-01-15/adsorption_energy.png'
#+END_SRC

#+RESULTS:
[[file:data/2025-01-15/adsorption_energy.png]]

*** Data
| Metal | E_ads (eV) | Site  |
|-------+------------+-------|
| Pt    |     -1.82  | fcc   |
| Cu    |     -0.95  | hcp   |
| Au    |     -0.45  | ontop |

** Analysis
*** Interpretation
What do these results mean?

*** Comparison with Literature
How do results compare with expected values?

*** Unexpected Findings
Anything surprising or anomalous?

** Conclusions
- Key findings
- Hypothesis supported/rejected
- Confidence level in results

** Issues/Problems
Document any problems encountered and how they were resolved.

** Next Steps
- [ ] Validate with different functional
- [ ] Test larger surface models
- [ ] Calculate reaction barriers

** References
- Previous work: [[file:2025-01-10.org::*Initial Screening]]
- Literature: Smith et al. (2024) DOI:10.1021/xxxxx
- Code: [[file:~/projects/catalyst-screening/run_calculations.py]]

* Entry 2: Another Task
...
```

## Essential Org-Mode Features for ELN

### 1. Properties Drawer
```org
:PROPERTIES:
:ID: unique-identifier
:PROJECT: Project_Name
:STATUS: Planning|In_Progress|Complete|On_Hold
:STARTED: [2025-01-15 Wed]
:COMPLETED: [2025-01-15 Wed]
:RELATED: [[link-to-related-entry]]
:DATA: [[file:./data/2025-01-15/results.csv]]
:END:
```

### 2. Tags
Use tags for categorization and filtering:
```org
#+FILETAGS: :experiment:simulation:catalyst:DFT:
* Entry Title                                              :important:urgent:
```

Common tag categories:
- **Type**: :experiment:, :simulation:, :analysis:, :literature:, :meeting:
- **Topic**: :catalyst:, :materials:, :synthesis:, :characterization:
- **Status**: :todo:, :in_progress:, :done:, :failed:
- **Priority**: :urgent:, :important:, :routine:

### 3. Links
```org
# Internal links
[[file:2025-01-10.org::*Previous Results]]
[[id:2025-01-15-001]]

# External links
[[file:~/data/experiment_001.csv][Data file]]
[[https://doi.org/10.1021/xxxxx][Smith et al. 2024]]

# Code links
[[file:~/projects/analysis/plot_results.py]]
```

### 4. Code Blocks
```org
#+BEGIN_SRC python :results output :session analysis :exports both
import pandas as pd
import matplotlib.pyplot as plt

# Reproducible analysis code
data = pd.read_csv('data/2025-01-15/results.csv')
print(f"Mean energy: {data['energy'].mean():.3f} eV")
#+END_SRC

#+RESULTS:
: Mean energy: -1.234 eV
```

### 5. Tables
```org
| Parameter      | Value     | Units | Notes              |
|----------------+-----------+-------+--------------------|
| Temperature    | 300       | K     | Room temperature   |
| Pressure       | 1         | atm   | Standard           |
| Coverage       | 0.25      | ML    | 1/4 monolayer      |
#+TBLFM: @2$4=Calculated from geometry
```

### 6. TODO Items and Checkboxes
```org
** Next Steps
- [ ] Run convergence test for k-points
- [ ] Compare with experimental data from Lee et al.
- [X] Calculate adsorption energy
- [ ] Write up results for group meeting

** TODO Validate results with different functional
DEADLINE: <2025-01-20 Fri>
:PROPERTIES:
:EFFORT: 2h
:END:
```

### 7. Timestamps
```org
# Active timestamps (appear in agenda)
* Meeting with advisor
<2025-01-20 Fri>

# Inactive timestamps (documentation only)
Calculation started [2025-01-15 Wed]

# Date ranges
Project duration: <2025-01-10 Mon>--<2025-01-30 Mon>
```

## Common Entry Types

### 1. Experimental/Computational Work

```org
* DFT Calculation - Surface Relaxation
:PROPERTIES:
:ID: 2025-01-15-001
:PROJECT: Catalyst_Screening
:TYPE: Calculation
:STATUS: Complete
:END:

** Objective
Optimize the geometry of clean Pt(111) surface.

** Methods
- Calculator: VASP
- Functional: PBE
- ENCUT: 400 eV
- k-points: 6×6×1 Monkhorst-Pack
- Convergence: Forces < 0.05 eV/Å

#+BEGIN_SRC bash
# Command used
vasp_std > vasp.out
#+END_SRC

** Results
- Final energy: -123.45 eV
- Relaxation time: 2.5 hours
- Converged in 45 ionic steps

[[file:./data/2025-01-15/surface_relaxation.png]]

** Analysis
Surface atoms relaxed inward by 0.03 Å (0.8% contraction).
This agrees with literature values (Smith 2023: 0.02-0.04 Å).

** Conclusion
Surface structure validated. Ready for adsorbate calculations.

** Next Steps
- [ ] Add CO adsorbate at FCC site
- [ ] Calculate adsorption energy
```

### 2. Literature Review Entry

```org
* Literature Review - CO Oxidation Mechanisms
:PROPERTIES:
:ID: 2025-01-15-002
:TOPIC: Catalysis
:STATUS: Complete
:END:

** Paper
Smith, J. et al. (2024) "CO Oxidation on Platinum Surfaces"
J. Phys. Chem. C, DOI: 10.1021/xxxxx

** Key Findings
- CO adsorption energy on Pt(111): -1.5 to -1.8 eV (experimental)
- Preferred site: FCC hollow
- Barrier for CO → CO₂: 0.8 eV

** Relevance to Our Work
Their experimental values provide validation targets for our DFT calculations.
Our predicted -1.82 eV is in excellent agreement.

** Questions Raised
- How does coverage affect binding energy?
- What about stepped surfaces?

** References to Follow Up
- [ ] Lee et al. (2023) - Coverage effects
- [ ] Zhang et al. (2024) - Step sites
```

### 3. Data Analysis Entry

```org
* Analysis - Comparing Different Functionals
:PROPERTIES:
:ID: 2025-01-15-003
:PROJECT: Method_Validation
:STATUS: Complete
:END:

** Objective
Compare PBE, PBE+D3, and RPBE for CO adsorption energies.

** Data Sources
- PBE: [[file:2025-01-10.org::*PBE Results]]
- PBE+D3: [[file:2025-01-12.org::*Dispersion Results]]
- RPBE: [[file:2025-01-14.org::*RPBE Calculations]]

** Analysis Code
#+BEGIN_SRC python :results file
import pandas as pd
import matplotlib.pyplot as plt

# Compile results
data = {
    'Functional': ['PBE', 'PBE+D3', 'RPBE'],
    'E_ads': [-1.82, -2.15, -1.45],
    'Experiment': [-1.6, -1.6, -1.6]
}
df = pd.DataFrame(data)

# Plot
plt.figure(figsize=(8, 5))
plt.bar(df['Functional'], df['E_ads'], alpha=0.7, label='Calculated')
plt.axhline(y=-1.6, color='r', linestyle='--', label='Experiment')
plt.ylabel('Adsorption Energy (eV)')
plt.legend()
plt.tight_layout()
plt.savefig('data/2025-01-15/functional_comparison.png', dpi=300)
return 'data/2025-01-15/functional_comparison.png'
#+END_SRC

#+RESULTS:
[[file:data/2025-01-15/functional_comparison.png]]

** Findings
| Functional | E_ads (eV) | Error vs Expt (eV) |
|------------+------------+--------------------|
| PBE        |     -1.82  |              -0.22 |
| PBE+D3     |     -2.15  |              -0.55 |
| RPBE       |     -1.45  |               0.15 |
#+TBLFM: $3=$2-(-1.6);%.2f

** Conclusions
- PBE gives reasonable agreement (within 0.22 eV)
- PBE+D3 overbinds significantly
- RPBE underestimates binding
- **Decision**: Use PBE for production calculations

** Impact on Previous Work
Need to note that PBE tends to overbind slightly when reporting results.
```

### 4. Meeting Notes

```org
* Group Meeting - Project Discussion
:PROPERTIES:
:ID: 2025-01-15-004
:TYPE: Meeting
:ATTENDEES: Prof. Smith, Jane Doe, John Smith
:END:

** Agenda
1. Progress updates
2. Results discussion
3. Next steps

** My Update
Presented CO adsorption results on Pt(111):
- E_ads = -1.82 eV (PBE)
- Good agreement with experiment (-1.6 eV)

** Feedback
- Prof. Smith: Test with larger surface to check size effects
- Jane: Compare with her experimental values (coming next week)
- Need to include dispersion for comparison

** Action Items
- [ ] Run calculations with 6×6×4 slab
- [ ] Prepare summary for Jane's experimental comparison
- [ ] Read paper Prof. Smith suggested: Zhang et al. 2024

** Next Meeting
<2025-01-22 Wed 10:00>
```

### 5. Problem/Debugging Entry

```org
* Troubleshooting - VASP SCF Convergence Issues
:PROPERTIES:
:ID: 2025-01-15-005
:TYPE: Problem
:STATUS: Resolved
:END:

** Problem
VASP calculation not converging after 100 SCF steps.

Error message:
#+BEGIN_EXAMPLE
WARNING: Sub-Space-Matrix is not hermitian in DAV
#+END_EXAMPLE

** Attempted Solutions
1. Increased NELM to 200 - Still failed
2. Changed ALGO from Fast to Normal - No improvement
3. Reduced SIGMA from 0.2 to 0.1 - Failed
4. **Solution**: Used ISMEAR=0 (Gaussian smearing) instead of ISMEAR=1

** Root Cause
System has a band gap. Methfessel-Paxton smearing (ISMEAR=1) is inappropriate.
Gaussian smearing (ISMEAR=0) is better for molecules and systems with gaps.

** Resolution
Changed INCAR:
#+BEGIN_EXAMPLE
ISMEAR = 0
SIGMA = 0.05
#+END_EXAMPLE

Calculation converged in 45 SCF steps.

** Lessons Learned
- Always check if system has a gap before choosing smearing
- For molecules/insulators: Use ISMEAR=0 or ISMEAR=-5
- For metals: ISMEAR=1 or 2 is appropriate

** References
- VASP Wiki: [[https://www.vasp.at/wiki/index.php/ISMEAR]]
```

## Best Practices

### 1. Daily Summaries
Start each file with a brief summary:
```org
* Daily Summary
Today focused on validating DFT functional choice for catalyst project.
Compared PBE, PBE+D3, and RPBE against experimental data. Concluded
that PBE gives best agreement. Started large-scale screening of FCC
metals.

Key accomplishment: Validated methodology for production runs.
Main challenge: VASP convergence issues with molecular systems (resolved).
```

### 2. Honest Documentation
```org
** Results
Expected: E_ads ≈ -1.5 eV
**Observed: E_ads = -0.45 eV**

This is significantly different from literature values.

** Analysis of Discrepancy
Possible causes:
1. Wrong adsorption site? → Checked: FCC is correct
2. Insufficient k-points? → Tested 8×8×1: -0.46 eV (no change)
3. Functional issue? → Literature used PBE, we used PBE
4. **Surface coverage?** → Our 1/16 ML vs literature 1/4 ML

** Resolution
Rerun with higher coverage to match literature conditions.
Original calculation still valid for low-coverage limit.
```

### 3. Version Control Integration
```org
** Computational Details
Code version: catalyst-tools v2.3.1
Git commit: a3f5e2b

#+BEGIN_SRC bash
git log -1 --oneline
#+END_SRC

#+RESULTS:
: a3f5e2b Fix convergence criteria in optimizer
```

### 4. Data Management
```org
** Data Files
- Raw output: [[file:./data/2025-01-15/OUTCAR]]
- Processed data: [[file:./data/2025-01-15/results.csv]]
- Analysis notebook: [[file:./data/2025-01-15/analysis.ipynb]]
- Archived: ~/archives/2025/january/calculation_001.tar.gz

MD5 checksums:
- OUTCAR: 5d41402abc4b2a76b9719d911017c592
- results.csv: 7d793037a0760186574b0282f2f435e7
```

### 5. Cross-Referencing
```org
** Related Work
- Background: [[file:2025-01-05.org::*Literature Review]]
- Previous attempt: [[file:2025-01-12.org::*Failed Calculation]] (explains why approach changed)
- Follow-up: [[file:2025-01-18.org::*Extended Analysis]]
- Project overview: [[file:../index.org::*Catalyst Screening Project]]
```

### 6. Reproducibility Checklist
Every computational entry should enable reproduction:
```org
** Reproducibility Information
- [X] Software versions documented
- [X] Input files included or linked
- [X] Random seeds specified (if applicable)
- [X] Computational environment described
- [X] Data processing code included
- [X] Analysis scripts provided
- [X] Key outputs archived

Environment:
- VASP: 6.4.2
- Python: 3.11.4
- ASE: 3.23.0
- NumPy: 1.24.3
```

## Search and Retrieval

### Using Org-Mode Search
```org
# Search by tag
C-c / m    # Match tags
Search: experiment+DFT-failed

# Search by TODO
C-c / t    # Show TODOs

# Search by text
C-c / r    # Regex search

# Org-agenda
C-c a s    # Search across all agenda files
```

### Creating Index File
```org
#+TITLE: Research Notebook Index
#+STARTUP: overview

* Projects
** [[file:2025/01-January/2025-01-15.org::*Catalyst Screening][Catalyst Screening Project]]
Started: [2025-01-05]
Status: Active

** Method Validation
Started: [2025-01-10]
Status: Complete

* Key Results
** [[file:2025/01-January/2025-01-15.org::*Functional Comparison][Best DFT Functional for CO Adsorption]]
Result: PBE preferred (error < 0.25 eV)

* Important Techniques
** [[file:2025/01-January/2025-01-12.org::*Convergence Testing][How to Test k-point Convergence]]
```

## Templates

### Quick Entry Template
```org
* Short Description
:PROPERTIES:
:ID: YYYY-MM-DD-NNN
:END:

** What I Did

** Why

** Results

** Next Steps
```

### Full Research Entry Template
```org
* Project - Specific Task
:PROPERTIES:
:ID: YYYY-MM-DD-NNN
:PROJECT: Project_Name
:STATUS: In_Progress
:END:

** Objective

** Hypothesis

** Methods

** Results

** Analysis

** Conclusions

** Next Steps
```

## Integration with Computational Workflows

### Embedding Code
```org
#+BEGIN_SRC python :results output :session :exports both
from ase.build import molecule
from ase.optimize import BFGS

mol = molecule('H2O')
# ... calculation code ...
print(f"Optimized energy: {mol.get_potential_energy():.3f} eV")
#+END_SRC
```

### Capturing Output
```org
#+BEGIN_SRC bash :results output
cd ~/calculations/calc_001
grep "energy" OUTCAR | tail -1
#+END_SRC

#+RESULTS:
: free energy = -123.456789 eV
```

### Including Figures
```org
#+CAPTION: CO adsorption energy vs coverage
#+NAME: fig:ads_energy
#+ATTR_ORG: :width 400
[[file:./data/2025-01-15/adsorption_plot.png]]

See Figure [[fig:ads_energy]] for trends.
```

## Professional Writing Guidelines

### 1. Clarity
- Write complete sentences
- Use past tense for work done
- Use present tense for conclusions
- Avoid ambiguous pronouns

### 2. Precision
- Include units: "300 K" not "300"
- Specify parameters: "PBE functional" not "DFT"
- Quantify: "decreased by 15%" not "decreased significantly"

### 3. Organization
- Use hierarchical structure
- One concept per section
- Chronological within day
- Logical grouping across days

### 4. Completeness
- Include negative results
- Document failed attempts
- Explain unexpected outcomes
- Preserve troubleshooting notes

## Response Patterns

When helping with ELN:
1. **Suggest appropriate structure** for the entry type
2. **Ask clarifying questions** about what was done, why, and outcomes
3. **Recommend org-mode features** that fit the task
4. **Ensure reproducibility** - check if enough detail provided
5. **Encourage cross-referencing** to related work
6. **Format code and data** properly
7. **Include metadata** (properties, tags, timestamps)
8. **Maintain professional tone** while being helpful
9. **Prompt for conclusions** and next steps
10. **Suggest organizational improvements** when appropriate

## Common Scenarios

### Starting New Project
```org
* Project Initiation - Catalyst Screening Study
:PROPERTIES:
:ID: 2025-01-15-001
:PROJECT: Catalyst_Screening
:STATUS: Planning
:END:

** Project Goal
Identify optimal catalyst for CO oxidation through computational screening.

** Background
[Literature review, motivation]

** Approach
1. Validate methodology with Pt(111) benchmark
2. Screen FCC metals (Cu, Ag, Au, Pt, Pd, Ni)
3. Analyze trends using d-band model
4. Validate top candidates with experiments

** Success Criteria
- Identify 2-3 promising candidates
- Error < 0.3 eV vs experiment
- Complete by [2025-02-28]

** Initial Tasks
- [ ] Set up calculation framework
- [ ] Run Pt(111) benchmark
- [ ] Compare functionals
```

### Documenting Failure
```org
* Failed Attempt - NEB Calculation
:PROPERTIES:
:ID: 2025-01-15-006
:STATUS: Failed
:END:

** Objective
Calculate CO diffusion barrier on Pt(111).

** Approach
NEB with 7 images, climbing image method.

** Problem
Images diverged after 20 steps. Final image forces > 5 eV/Å.

** Analysis
Initial path guess was poor - CO moved through bulk instead of surface.

** Lessons Learned
- Need better initial path interpolation
- Check geometry of intermediate images before optimization
- Use more images (9-11) for surface diffusion

** Next Attempt
Will use improved path generation script and verify geometries.
Scheduled for [[file:2025-01-16.org][tomorrow]].
```

## Archiving and Long-Term Storage

### End-of-Month Summary
```org
#+TITLE: January 2025 Summary
#+DATE: [2025-01-31]

* Overview
Completed validation of DFT methodology for catalyst project.
Screened 6 FCC metals for CO adsorption. Identified Pt and Pd as
most promising candidates.

* Key Accomplishments
- Validated PBE functional (error < 0.25 eV)
- Completed metal screening
- Resolved VASP convergence issues

* Data Generated
- 24 DFT calculations
- 180 GB raw data (archived to ~/archives/2025/january/)
- 6 publications figures prepared

* Next Month Goals
- Begin reaction barrier calculations
- Compare with experimental data from collaborators
- Draft results section for paper
```

### Year-End Review
Create comprehensive summaries for easy retrieval and reporting.

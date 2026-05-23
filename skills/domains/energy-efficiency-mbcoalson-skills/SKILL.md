---
name: energy-efficiency
description: Comprehensive energy analysis using EnergyPlus, commissioning best practices, and ASHRAE standards for building energy modeling, code compliance verification, and performance optimization
---

# Energy Efficiency Analysis Skill

This skill provides specialized knowledge for building energy analysis and optimization projects.

## Core Capabilities

### Energy Modeling
- EnergyPlus simulation setup and analysis
- OpenStudio model development
- Weather data integration and selection
- HVAC system modeling strategies

### Code Compliance
- ASHRAE 90.1 performance path analysis
- IECC commercial compliance verification
- Energy cost budget calculations
- Baseline model development

### Performance Analysis
- Energy use intensity (EUI) calculations
- Peak demand analysis and optimization
- Load profile evaluation
- Equipment efficiency assessments

## Available Scripts
- scripts/energyplus_postprocess.py: Post-process EnergyPlus outputs
- scripts/ashrae_compliance.py: ASHRAE 90.1 compliance calculations
- scripts/eui_calculator.py: Building EUI analysis

## Reference Materials
- eferences/ashrae_standards.md: Key ASHRAE standard requirements
- eferences/energyplus_tips.md: EnergyPlus modeling best practices
- eferences/iecc_requirements.md: IECC compliance procedures

## Asset Templates
- ssets/compliance_report_template.docx: Standard compliance report format
- ssets/energy_model_checklist.xlsx: QA/QC checklist for models

## Usage Examples
- "Analyze this EnergyPlus model for ASHRAE 90.1 compliance"
- "Calculate the energy savings from this efficiency measure"
- "Generate a code compliance report for this building"
- "Optimize the HVAC system sizing for this model"

## Cost Analysis Tools

### NPV Analysis Email Generator

**Purpose:** Generate lifecycle cost analysis summaries for energy efficiency measures and design alternatives

**Location:** `scripts/npv_analysis_email_generator.py`

**Documentation:** [`docs/TOOL_NPV_Email_Generator.md`](../../docs/TOOL_NPV_Email_Generator.md)

**When to Use:**
- Comparing energy efficiency measure costs vs. savings over lifecycle
- Evaluating HVAC system alternatives (baseline vs. high-efficiency)
- Generating cost comparison reports for LEED energy models
- Creating stakeholder-ready summaries of first costs and NPV

**Common Workflow:**

1. Run energy models for baseline and alternatives
2. Extract annual energy costs from simulation results
3. Input costs into NPV spreadsheet (Assumptions, Upfront_Costs, Cashflows_XNPV sheets)
4. Recalculate formulas if needed
5. Generate formatted summary:
   ```bash
   python scripts/npv_analysis_email_generator.py "path/to/NPV_Analysis.xlsx" \
     -o "path/to/Summary.xlsx" \
     -p "Project Name"
   ```

**Output:**
- Excel summary with color-coded cost comparisons
- Highlights lowest lifecycle cost option
- Ready for client presentations and stakeholder communication

**Integration:**
- Use **xlsx skill** to edit NPV spreadsheet and recalculate formulas
- Use **work-command-center** to track NPV summary as deliverable
- Use **diagnosing-energy-models** for HVAC alternative modeling

**Example Use Cases:**
- "Compare lifecycle costs of GSHP vs. conventional HVAC"
- "Generate NPV summary for LEED cost-benefit analysis"
- "Create stakeholder report showing first cost vs. 25-year savings"

## Saving Next Steps

When energy-efficiency work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "energy-efficiency" \
  --content "## Priority Tasks
1. Complete ASHRAE 90.1 compliance analysis
2. Generate NPV summary for efficiency measures
3. Finalize energy model QA/QC"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`

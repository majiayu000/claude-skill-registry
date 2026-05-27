---
name: diagnosing-energy-models
description: Use this skill when troubleshooting OpenStudio or EnergyPlus energy models that fail to simulate, have geometry errors (intersecting surfaces, non-planar surfaces, story organization issues), need HVAC validation against Engineer of Record specifications, require LEED Appendix G baseline generation, or need systematic diagnostics for complex commercial building models. Handles model triage, geometry rebuild decisions, EOR specification mapping, and quality assurance for LEED compliance.
---

# Energy Model Diagnostics Skill

Systematic troubleshooting, validation, and repair workflows for OpenStudio and EnergyPlus energy models. Particularly useful for LEED projects, complex HVAC systems, and models with geometry errors.

**Key Principle**: All recommendations must be validated against authoritative sources before implementation.

---

## VALIDATION PROTOCOL (CRITICAL)

**Before providing ANY fix recommendations**, validate your approach using these authoritative sources in priority order:

### Required Validation Steps

1. **Check OpenStudio Documentation FIRST** (Primary Source - MANDATORY for geometry and HVAC)
   - Use WebFetch: https://nrel.github.io/OpenStudio-user-documentation/
   - **Version**: OpenStudio 3.9 (default unless specified otherwise)
   - **For**: Geometry issues, HVAC system setup and connections, OpenStudio workflows
   - **Priority Rule**: ALWAYS check OpenStudio docs BEFORE any other source for geometry fixes and HVAC solutions

2. **Search Unmet Hours Community** (Secondary Source - Use with Caution)
   - Use WebSearch: `site:unmethours.com [topic] openstudio`
   - **For**: Real-world troubleshooting, edge cases not in official docs
   - **Caution**: Prioritize answers from well-regarded contributors (NREL staff, Big Ladder Software, high-karma users)
   - **When NOT to use**: As primary source when OpenStudio docs provide clear guidance
   - If Unmet Hours contradicts OpenStudio docs → Trust OpenStudio docs

3. **Reference EnergyPlus Documentation** (Object-Level Details)
   - Use WebFetch: https://bigladdersoftware.com/epx/docs/24-2/input-output-reference/
   - **Version**: EnergyPlus 24.2 (aligns with OpenStudio 3.9)
   - **For**: EnergyPlus object requirements, field definitions, simulation errors

### Validation Checklist

Before recommending any fix:
- [ ] Checked OpenStudio 3.9 documentation FIRST (mandatory for geometry/HVAC)
- [ ] If using Unmet Hours: Verified contributor reputation and answer quality
- [ ] Verified approach compatible with OpenStudio 3.9 / EnergyPlus 24.2
- [ ] Cross-validated if sources conflict (OpenStudio docs take precedence)
- [ ] Included brief source citation in recommendation

**See [validation-sources.md](./validation-sources.md) for detailed instructions on version-specific docs and contributor evaluation.**

---

## Core Capabilities

### Geometry Diagnostics
- **Intersecting Surfaces**: Identify overlapping geometry causing simulation failures
- **Story Organization**: Validate proper vertical building structure (common critical error)
- **Surface Matching**: Verify adjacent surfaces properly matched
- **Non-Planar Surfaces**: Find and fix vertex alignment issues from SketchUp imports

### HVAC System Validation
- **EOR Compliance**: Match modeled systems to Engineer of Record specifications
- **Thermal Zone Assignment**: Verify space-to-zone-to-equipment mappings
- **Plant Loop Integrity**: Check connections between plant equipment and air/water loops
- **Equipment Validation**: Verify equipment types, capacities, and connections

### LEED Compliance
- **Appendix G Baseline**: Generate baseline models per ASHRAE 90.1
- **Building Rotation**: Create and analyze 4 rotated baseline models
- **Percent Savings**: Calculate energy cost budget and verify savings targets
- **Documentation**: Prepare LEED submittal deliverables

### Model Quality Assurance
- **Pre-Simulation Checks**: Validate model completeness before running
- **Error Parsing**: Translate EnergyPlus errors into actionable fixes
- **Results Validation**: Verify simulation outputs are reasonable

---

## Common Error Patterns

**Six major patterns account for most model failures.**

For detailed symptoms, root causes, and step-by-step fixes, see **[common-error-patterns.md](./common-error-patterns.md)**

### Quick Reference

**Pattern 1: Overlapping Building Stories**
- Multiple stories with same Z-coordinate (typically Z=0)
- Causes severe geometry errors, simulation failure
- **Fix**: Consolidate spaces onto correct physical floor levels
- **Validate before fixing**: Check OpenStudio geometry documentation

**Pattern 2: Non-Planar Surfaces**
- Vertices not coplanar, typically from SketchUp geometry
- Causes simulation warnings or failures
- **Fix**: Delete and recreate using OpenStudio SketchUp plugin tools
- **Validate before fixing**: Search Unmet Hours for non-planar surface solutions

**Pattern 3: Unassigned Thermal Zones**
- Spaces without zones or orphaned zones without spaces
- Causes HVAC errors, simulation failure
- **Fix**: Create zone assignment matrix, assign systematically
- **Validate before fixing**: Check OpenStudio thermal zone documentation

**Pattern 4: Missing HVAC Connections**
- Components not connected to plant loops
- Node connection mismatches
- **Fix**: Delete and re-add using proper OpenStudio workflow
- **Validate before fixing**: Check OpenStudio HVAC docs + Unmet Hours

**Pattern 5: Surface Matching Failures**
- Adjacent surfaces not matched (red in 3D view)
- **Fix**: Run surface matching algorithm, check story organization
- **Validate before fixing**: Check OpenStudio surface matching documentation

**Pattern 6: Schedule Type Mismatches**
- Wrong schedule type limits for object field
- **Fix**: Verify required schedule type in EnergyPlus I/O Reference
- **Validate before fixing**: Check EnergyPlus documentation

---

## Diagnostic Workflows

**Five systematic workflows for common scenarios.**

For detailed step-by-step procedures, see **[diagnostic-workflows.md](./diagnostic-workflows.md)**

### Workflow 1: Model Triage (5-10 minutes)

**When**: Model fails to simulate or has unexpected behavior

**Quick Steps**:
1. Check story organization (flag duplicate Z-coordinates)
2. Validate surfaces (count, check for anomalies, intersections)
3. Verify zone assignments (spaces have zones, zones have spaces)
4. Check HVAC topology (plant loops, air loops, terminals connected)
5. Attempt simulation, parse top errors

**Output**: Prioritized list of blocking issues

**Before providing fixes**: Validate approach for each issue type using [validation-sources.md](./validation-sources.md)

### Workflow 2: Geometry Rebuild Decision (15-20 minutes)

**When**: Considering whether to fix or rebuild geometry

**Decision Criteria**:
- **Fix**: <10 intersecting surfaces, correct story organization, high preservation value
- **Rebuild**: >10 intersecting surfaces, multiple stories at Z=0, systemic issues
- **Hybrid**: Extract valuable components, rebuild geometry, reapply

**Time Estimates**:
- Small fix (<5 surfaces): 1-2 hours
- Medium fix (5-10 surfaces): 3-5 hours
- Small building rebuild (<20k sf): 4-8 hours
- Large building rebuild (50-100k sf): 16-24 hours

**Before recommending**: Validate geometry best practices with OpenStudio documentation

### Workflow 3: EOR Specification Mapping (30-45 minutes)

**When**: Starting new model or validating zone assignments

**Key Steps**:
1. Gather EOR documents (mechanical drawings, equipment schedules, BOD)
2. Create equipment matrix (equipment ID, type, spaces served, capacities)
3. Create space assignment matrix (space → zone → equipment → terminal)
4. Validate model against matrices
5. Generate validation report with discrepancies

**Output**: Validated mapping between spaces and EOR equipment

**Before providing recommendations**: Cross-reference EOR specs carefully, validate HVAC approach with OpenStudio docs

### Workflow 4: LEED Baseline Generation

**When**: Ready to create ASHRAE 90.1 Appendix G baseline model

**See [leed-compliance-procedures.md](./leed-compliance-procedures.md) for comprehensive procedures.**

**High-Level Steps**:
1. Verify proposed model completeness (simulation runs, matches EOR)
2. Apply Appendix G transformations (envelope, lighting, HVAC)
3. Create 4 rotations (0°, 90°, 180°, 270°)
4. Run all models, calculate averaged baseline
5. Calculate percent savings
6. Verify unmet hours <300 for all models
7. Generate LEED documentation

**Before baseline generation**: Validate Appendix G requirements for project's ASHRAE 90.1 version and climate zone

### Workflow 5: Systematic Error Resolution

**When**: Multiple simulation errors need methodical resolution

**Key Steps**:
1. Parse error file, categorize by severity and type
2. Prioritize: Severe/fatal → Warnings → Info
3. **Validate fix approaches** using authoritative sources (critical step)
4. Apply fixes iteratively (fix 1-3 errors, re-run, repeat)
5. Document fixes and results

**Before providing fixes**: For EACH error, validate solution approach using [validation-sources.md](./validation-sources.md)

---

## LEED Compliance

For comprehensive LEED procedures, see **[leed-compliance-procedures.md](./leed-compliance-procedures.md)**

### Quick Reference: Prerequisites

**Proposed Model Ready**:
- Simulation runs successfully
- Unmet hours <300
- HVAC systems match EOR specifications
- All spaces have thermal zones
- Schedules and constructions complete

**Baseline Transformation Rules** (ASHRAE 90.1 Appendix G):
- Envelope: Table G3.1.5 baseline assemblies by climate zone
- Lighting: Table G3.1.6 baseline LPDs by space type
- HVAC: Table G3.1.1-1 system selection by building type, size, heating source
- Equipment efficiencies: Tables 6.8.1-X

**Rotation Analysis**:
- Create 4 baseline orientations (0°, 90°, 180°, 270°)
- Average baseline results
- Proposed stays as-designed (1 simulation)

**Percent Savings**:
- ECB = Average of 4 baseline energy costs
- Savings = (ECB - Proposed) / ECB × 100%

**Before LEED work**: Validate Appendix G requirements for project's specific ASHRAE 90.1 version

---

## Quality Control Checklists

### Pre-Simulation Checklist
```
□ All spaces assigned to building stories with correct Z-coordinates
□ All spaces have thermal zones
□ All thermal zones have HVAC equipment or ideal loads
□ All surfaces properly matched (no red in 3D view)
□ No duplicate or overlapping geometry
□ Space types assigned
□ Construction sets assigned
□ Schedules defined and applied
□ Weather file matches project location
```

### Post-Simulation Checklist
```
□ Simulation completed without severe errors
□ Unmet hours <300 (for LEED)
□ Energy consumption reasonable (compare EUI to benchmarks)
□ Equipment sizing reasonable
□ Monthly energy patterns make sense
□ End use breakdown logical
```

### EOR Compliance Checklist
```
□ All equipment from EOR specs in model
□ Equipment types match exactly
□ Thermal zones match EOR space assignments
□ Plant loops correct for water-based systems
□ Terminal types match (VAV vs CV, reheat vs no reheat)
```

---

## Project-Specific Context

### Example Recreation Center

For detailed project context, see **[project-example-recreation-center.md](./project-example-recreation-center.md)**

**Key Project Details**:
- 92,000 sf rec center + pool + library
- LEED V4 + Colorado IDAP (10% below ASHRAE 90.1-2022)
- Engineer of Record: Clarkenersen (see `11_10_2025_ZoneEquipList.pdf`)
- Pre-Thanksgiving 2025 coordination deadline

**Special Considerations**:
- Historical issue: Original model had 5 stories at Z=0 (required complete rebuild)
- Pool: 30' ceiling height, dehumidification system, special modeling
- WAHP systems: Water-to-air heat pumps with **fluid cooler** (NOT cooling tower)
- 6 different RTU/DOAS systems + central plant

**Before working on this project**:
- Reference EOR equipment list: `11_10_2025_ZoneEquipList.pdf`
- Check HVAC rebuild plan: `Example_HVAC_Rebuild_Plan.md`
- Validate pool modeling approach with multiple sources
- Verify fluid cooler (not cooling tower) for WAHP systems

---

## Usage Examples

### Example 1: Model Won't Simulate

**User**: "My energy model won't simulate. Can you diagnose what's wrong?"

**Response Pattern**:
```
1. "I'll run a systematic diagnostic using Workflow 1 (Model Triage)"
2. [Check story organization, surfaces, zones, HVAC]
3. [Identify issues - e.g., "5 stories at Z=0, 8 intersecting surfaces"]
4. **VALIDATE**: Use WebFetch on OpenStudio 3.9 geometry documentation (PRIMARY)
5. [If needed] Search Unmet Hours for similar issues (SECONDARY - check contributor reputation)
6. Provide recommendations citing sources with version:
   "According to OpenStudio 3.9 geometry documentation, Building Story objects must represent physical floor levels, not programmatic areas..."
7. Recommend fix or rebuild based on validated decision criteria
```

**Key**: ALWAYS check OpenStudio docs FIRST, especially for geometry issues

### Example 2: Verify Against EOR Specs

**User**: "Can you check if my model matches the mechanical engineer's specifications?"

**Response Pattern**:
```
1. "I'll use Workflow 3 (EOR Specification Mapping)"
2. Request documents: OSM file, EOR mechanical drawings/equipment schedule
3. Create equipment matrix from EOR specs
4. Export model zone assignments
5. Compare and flag discrepancies
6. **VALIDATE**: Check OpenStudio 3.9 HVAC documentation for proper modeling (PRIMARY)
7. [If needed] Search Unmet Hours for equipment-specific guidance (SECONDARY - prioritize NREL/Big Ladder answers)
8. Provide specific fix instructions for each discrepancy, citing sources:
   "Per OpenStudio 3.9 HVAC systems documentation..."
```

**Key**: Check OpenStudio HVAC docs FIRST before recommending any HVAC changes

### Example 3: LEED Baseline Generation

**User**: "I need to create my LEED baseline model."

**Response Pattern**:
```
1. "I'll guide you through LEED baseline generation (see leed-compliance-procedures.md)"
2. Run pre-simulation checklist on proposed model
3. **VALIDATE**: Check ASHRAE 90.1 version requirements for project
4. **VALIDATE**: WebFetch current Appendix G transformation rules
5. Guide through transformations (envelope, lighting, HVAC)
6. Create 4 rotations
7. Calculate percent savings
8. Verify unmet hours
9. Generate documentation
```

**Key**: Validate Appendix G requirements for specific project version and climate zone

### Example 4: Simulation Error Resolution

**User**: "I'm getting errors about non-planar surfaces. How do I fix this?"

**Response Pattern**:
```
1. "I'll help resolve non-planar surface errors (Pattern 2)"
2. Identify specific surfaces from error file
3. **VALIDATE**: WebFetch OpenStudio 3.9 geometry editor documentation (PRIMARY - mandatory check)
4. [If additional context needed] Search Unmet Hours: "site:unmethours.com non-planar surface openstudio"
   - Check contributor reputation (prefer NREL staff, Big Ladder Software)
   - Verify answer is recent and compatible with OpenStudio 3.x
5. Provide fix strategy citing OpenStudio docs:
   "Per OpenStudio 3.9 geometry documentation, non-planar surfaces should be deleted and recreated..."
   [If using Unmet Hours] "This approach is validated by [contributor name] on Unmet Hours..."
6. Provide step-by-step fix instructions
7. Explain prevention strategies
```

**Key**: OpenStudio docs are PRIMARY source; use Unmet Hours only for additional context and only from trusted contributors

---

## Integration with Other Skills

This skill works in combination with:

- **energy-efficiency**: Post-diagnostic energy calculations and performance analysis
- **writing-openstudio-model-measures**: Create Ruby measures for automated fixes or transformations
- **work-command-center**: Project timeline management and deadline tracking
- **commissioning-reports**: Document model validation in MBCx reports
- **n8n-automation**: Automated model checking in CI/CD pipelines

---

## Best Practices

### Always Validate First (MANDATORY)
- **Never** provide fix recommendations without checking authoritative sources
- **For geometry and HVAC**: ALWAYS check OpenStudio 3.9 documentation FIRST
- Use WebFetch for OpenStudio documentation (version-specific)
- Use WebFetch for EnergyPlus 24.2 documentation (object-level details)
- Use WebSearch for Unmet Hours (secondary, with caution)
- Always cite sources with version: "According to OpenStudio 3.9 [section]..."

### Unmet Hours Usage Rules
- **Primary check**: OpenStudio documentation
- **Secondary check**: Unmet Hours (only if needed for additional context)
- **Evaluate contributors**: Prioritize NREL staff, Big Ladder Software, high-karma users
- **Check dates**: Prefer recent answers compatible with OpenStudio 3.x
- **Cross-validate**: If Unmet Hours contradicts OpenStudio docs → Trust OpenStudio docs
- **Cite carefully**: "Per OpenStudio 3.9 docs... [validated by contributor name on Unmet Hours]"

### Work Systematically
- Follow workflows step-by-step (don't skip steps)
- Fix errors iteratively (not all at once)
- Validate each fix before proceeding to next
- Document assumptions and decisions

### Verify Version Compatibility
- **Default**: OpenStudio 3.9 → EnergyPlus 24.2
- Check OpenStudio version if different (Help → About in OpenStudio Application)
- Verify solutions are compatible with version in use
- Older Unmet Hours answers (OpenStudio 2.x, 1.x) may not apply
- Note version compatibility in recommendations

### Use Progressive Disclosure
- Start with high-level diagnosis
- Provide detailed steps only after validation
- Reference supporting files for comprehensive details
- Keep recommendations focused and actionable

---

## Analysis Tools

### EnergyPlus Results Analyzer

**Location**: `scripts/analyze_energyplus_results.py`

Automated tool to extract, calculate, and structure key metrics from EnergyPlus simulation outputs. Designed to distill E+ results for LLM interpretation and graphing tools, separating calculation work from interpretation.

**Purpose**:
- Extract all metrics from EnergyPlus outputs
- Convert between Imperial and Metric units
- Generate JSON for programmatic use or Markdown for human readability
- Designed for use with future GHG and utility cost calculators

**Usage**:
```bash
# Imperial units, JSON output
python scripts/analyze_energyplus_results.py \
  --input-dir "path/to/run/" \
  --units imperial \
  --format json

# Metric units, Markdown summary
python scripts/analyze_energyplus_results.py \
  --input-dir "path/to/run/" \
  --units metric \
  --format markdown \
  --output summary.md
```

**Input Sources** (priority order):
1. **Priority 1**: `eplusout.sql` - SQLite database (most complete)
2. **Priority 2**: `results.json` - OpenStudio Results measure (supplemental, optional)
3. **Priority 3**: `eplustbl.htm` - HTML tables (fallback)

**Metrics Extracted**:
- Site & Source Energy (GJ, kWh, MBtu, kBtu)
- EUI calculations (MJ/m², kWh/m², kBtu/sf/yr)
- Building areas (m², sf)
- End uses by category (Heating, Cooling, Lighting, Equipment, etc.)
- End uses by fuel type (Electricity, Natural Gas, District, etc.)
- Percentages for all end uses
- Unmet hours (heating, cooling, occupied)
- Peak electric demand
- Utility costs (if available)

**Output Formats**:
- **JSON**: Structured data for LLMs, graphing tools, or downstream analysis
- **Markdown**: Human-readable summary with tables

**When to Use**:
- After model simulation to extract results
- When comparing model iterations
- When preparing data for LLM interpretation
- Before generating reports or visualizations
- As input to future GHG/utility cost calculators

---

## Supporting Files

All supporting files use progressive disclosure to keep this skill concise:

- **[validation-sources.md](./validation-sources.md)**: Detailed instructions for using each authoritative source
- **[common-error-patterns.md](./common-error-patterns.md)**: Six major error patterns with symptoms, causes, and fixes
- **[diagnostic-workflows.md](./diagnostic-workflows.md)**: Five detailed step-by-step diagnostic workflows
- **[leed-compliance-procedures.md](./leed-compliance-procedures.md)**: Comprehensive LEED Appendix G procedures
- **[project-example-recreation-center.md](./project-example-recreation-center.md)**: Example project-specific context

---

## Cost Analysis for HVAC Alternatives

### NPV Analysis Email Generator

**Purpose:** Generate lifecycle cost analysis summaries when comparing HVAC system alternatives (baseline vs. proposed systems)

**Location:** `scripts/npv_analysis_email_generator.py`

**Documentation:** [`docs/TOOL_NPV_Email_Generator.md`](../../docs/TOOL_NPV_Email_Generator.md)

**When to Use:**

1. **After running proposed and baseline models** - Compare lifecycle costs of different HVAC approaches
2. **LEED Appendix G cost analysis** - Show first cost premium vs. lifecycle savings
3. **Value engineering decisions** - Demonstrate cost impact of HVAC system changes
4. **EOR specification validation** - Compare specified system costs vs. alternatives

**Typical Workflow:**

1. **Model multiple HVAC alternatives:**
   - Baseline (code-minimum or existing)
   - Proposed (EOR specification)
   - Alternatives (if evaluating options)

2. **Extract annual energy costs from simulation results**

3. **Input costs into NPV spreadsheet:**
   - First costs (equipment, installation)
   - Annual energy costs (from energy model results)
   - Maintenance costs (if applicable)

4. **Generate formatted summary:**
   ```bash
   python scripts/npv_analysis_email_generator.py "path/to/NPV_Analysis.xlsx" \
     -o "path/to/Summary.xlsx" \
     -p "Project Name - HVAC Alternatives"
   ```

**Output:**
- Excel summary with color-coded comparisons
- First cost vs. lifecycle NPV for each alternative
- Highlights lowest lifecycle cost option
- Ready for stakeholder presentations

**Integration with Other Skills:**
- **energy-efficiency skill** - Use for energy savings calculations
- **xlsx skill** - Edit NPV spreadsheet and recalculate formulas before generating summary
- **work-command-center** - Track NPV summary generation as project deliverable

**Example Use Cases:**
- "Compare lifecycle costs: Water-source heat pump vs. GSHP vs. conventional DX"
- "Generate cost comparison for LEED review submittal"
- "Show client the 25-year NPV of HVAC system alternatives"

---

## Quick Start

**For any diagnostic task**:

1. Identify task type (triage, rebuild decision, EOR validation, LEED baseline, error resolution)
2. Select appropriate workflow from [diagnostic-workflows.md](./diagnostic-workflows.md)
3. **VALIDATE all recommendations** using [validation-sources.md](./validation-sources.md)
4. Check for known patterns in [common-error-patterns.md](./common-error-patterns.md)
5. Provide recommendations with source citations
6. Use quality control checklists to verify completeness

**Remember**: The validation protocol is not optional. Always validate before recommending fixes.

---

## Context Awareness

This skill integrates with work-command-center session tracking:

**Check Active Context:**

```bash
node .claude/skills/work-command-center/tools/session-state.js status
```

Returns: Project name, project number, duration, and deliverables context

**Log Activity Checkpoints:**

```bash
node .claude/skills/work-command-center/tools/session-state.js checkpoint \
  --activity "diagnosing-energy-models: Fixed 8 geometry errors, model ready for simulation"
```

**Signal Completion (called by WCC after skill returns):**

```bash
node .claude/skills/work-command-center/tools/session-state.js skill-complete \
  --skill-name "diagnosing-energy-models" \
  --summary "Diagnosed and repaired geometry errors. Model validates successfully." \
  --outcome "success"
```

**Benefits:**

- WCC tracks time spent in this skill
- Session logs include skill work breakdown
- Context visible across skill transitions
- Deliverables auto-update from skill outcomes

---

**Last Updated**: 2025-11-20
**Version**: 2.1 (Added EnergyPlus Results Analyzer tool)
**Aligned with**: OpenStudio 3.9, EnergyPlus 24.2
**Primary Use Cases**: Recreation center projects, LEED v4 projects, complex HVAC troubleshooting


## Saving Next Steps

When diagnosing-energy-models work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "diagnosing-energy-models" \
  --content "## Priority Tasks
1. Fix geometry errors in energy model
2. Validate HVAC system against EOR specs
3. Generate LEED Appendix G baseline model"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`

---
name: energize-denver-proposals
description: Use when creating or updating Energize Denver compliance proposals including benchmarking, energy audits, compliance pathways, and performance target analysis. Handles proposal generation from template, cost estimation based on building size and service type, timeline planning, and compliance verification against Denver Article XIV requirements for commercial and multifamily buildings (project)
---

# Energize Denver Proposal Generation

Generate professional Iconergy proposals for Energize Denver compliance projects including benchmarking, energy audits, compliance pathways, and performance target consulting.

## When to Use This Skill

Invoke this skill when:
- Creating proposals for Energize Denver compliance services
- Responding to Energize Denver audit or benchmarking requests
- Pricing Energize Denver projects (audits, compliance consulting, benchmarking)
- Generating proposals for Building Performance Requirements compliance
- Working with Denver commercial or multifamily buildings ≥5,000 sq ft

## Quick Start

1. **Gather Building Information**:
   - Building address
   - Square footage (gross floor area)
   - Building type (commercial, multifamily, mixed-use)
   - Energize Denver Building ID (if known)
   - Current EUI and compliance status (if known)

2. **Determine Service Type**:
   - Benchmarking & Data Verification
   - Energy Audit (Level 1, 2, or 3)
   - Compliance Pathway Consulting
   - Performance Target Analysis
   - Alternate Compliance Application

3. **Generate Proposal**:
   Use `scripts/generate-proposal.py` to create customized .docx proposal

## Service Types & Scope

See [./service-types.md](./service-types.md) for detailed scope templates for each Energize Denver service offering.

### Benchmarking & Data Verification
- Submit annual benchmarking data via Energy Star Portfolio Manager
- Compile and submit data verification documents
- Typical timeline: 2-4 weeks
- Pricing: $2,000-$5,000 (T&M or fixed fee)

### Energy Audits
- **Level 1 (Walk-through)**: Basic building assessment, low-cost ECM identification
- **Level 2 (Detailed Analysis)**: Engineering analysis, energy modeling, ECM cost/benefit
- **Level 3 (Investment Grade)**: Detailed engineering, guaranteed savings analysis
- Typical timeline: 4-12 weeks depending on level
- Pricing: See [./pricing-guidelines.md](./pricing-guidelines.md)

### Compliance Pathway Consulting
- Analyze baseline EUI vs. target EUI (2024, 2027, 2030)
- Develop multi-year compliance strategy
- ECM recommendations to meet performance targets
- Alternate compliance pathway applications
- Typical timeline: 6-8 weeks
- Pricing: Based on building complexity and timeline

### Performance Target Analysis
- Establish or verify baseline EUI
- Calculate interim and final performance targets
- Review Energy Star Portfolio Manager data quality
- Typical timeline: 2-4 weeks
- Pricing: $3,000-$8,000

## Energize Denver Compliance Requirements

See [./energize-denver-requirements.md](./energize-denver-requirements.md) for complete Article XIV details.

**Key Requirements:**

### Buildings 25,000+ sq ft:
- **Annual Benchmarking**: Submit energy data by June 1 each year
- **Performance Targets**: Must meet EUI targets for 2024, 2027, 2030
- **Baseline**: Typically 2019 EUI
- **Penalties**: $0.70/kBtu/year for shortfall
- **Reporting**: Energy Star Portfolio Manager required

### Buildings 5,000-24,999 sq ft:
- **LED Lighting OR 20% Solar** by compliance deadline:
  - 15,001-24,999 sf: Dec 31, 2025
  - 10,001-15,000 sf: Dec 31, 2026
  - 5,000-10,000 sf: Dec 31, 2027

### Alternate Compliance Options:
- Timing adjustments for meeting requirements
- Target adjustments for building use characteristics
- Prescriptive options for smaller buildings
- Process loads exemptions for manufacturing/agriculture

## Generating Proposals

### Using the Python Script

```bash
python .claude/skills/energize-denver-proposals/scripts/generate-proposal.py \
  --service "Benchmarking & Data Verification" \
  --building-address "5067 S Wadsworth Blvd, Denver, CO 80123" \
  --square-footage 25000 \
  --building-id 15708 \
  --pricing-model "T&M" \
  --nte 5000 \
  --contact-name "Your Name" \
  --contact-title "Your Title" \
  --contact-phone "720-555-1234" \
  --contact-email "your.email@iconergy.com" \
  --output "output-proposal.docx"
```

### Interactive Mode

```bash
python .claude/skills/energize-denver-proposals/scripts/generate-proposal.py --interactive
```

The script will prompt for all required information and generate a complete proposal.

## Proposal Components

Every Energize Denver proposal includes:

1. **About Iconergy** (standard boilerplate)
2. **Building Information**:
   - Address, square footage, Building ID
   - Service description (Energize Denver-specific)
   - Compliance context
3. **Scope of Work**:
   - Service-specific deliverables
   - Timeline and milestones
   - Exclusions (if applicable)
4. **Pricing**:
   - Fixed fee OR Time & Materials with NTE
   - Payment terms
   - Proposal validity date (~90 days)
5. **Signature Block**: Iconergy contact details
6. **Customer Acceptance**: Sign-off section

## Pricing Guidelines

See [./pricing-guidelines.md](./pricing-guidelines.md) for detailed pricing by service type and building size.

**Quick Reference:**
- Benchmarking: $2K-$5K
- ASHRAE Level 1 Audit: $5K-$10K
- ASHRAE Level 2 Audit: $15K-$35K
- ASHRAE Level 3 Audit: $40K-$80K
- Compliance Pathway: $10K-$25K

Factors affecting pricing:
- Building size (gross floor area)
- Building complexity (# systems, equipment diversity)
- Service level (audit depth, analysis detail)
- Timeline urgency
- Data availability and quality

## Important Notes

### Compliance Deadlines
- **Benchmarking submissions**: Due June 1 annually
- **Performance target compliance**: Calendar years 2024, 2027, 2030
- **Small building LED/solar**: Dec 31, 2025/2026/2027 by size tier

### Data Requirements
- 24 months of utility data (monthly bills)
- Building characteristics (HVAC systems, envelope, occupancy)
- Energy Star Portfolio Manager account access
- Previous benchmarking reports (if available)

### Common Exclusions
- Buildings under 5,000 sq ft
- Manufacturing/agriculture process load buildings (unless minimal)
- Buildings under demolition permit
- Buildings experiencing financial distress

## Resources

- [Energize Denver Official Site](https://energizedenver.org/)
- [City of Denver Building Performance Requirements](https://www.denvergov.org/Government/Agencies-Departments-Offices/Agencies-Departments-Offices-Directory/Climate-Action-Sustainability-and-Resiliency/Cutting-Denvers-Carbon-Pollution/Efficient-Commercial-Buildings/Denver-Building-Regulations/Energize-Denver-Building-Performance-Policy/Buildings-25000-sq-ft-or-Larger/Creating-Your-Compliance-Pathway)
- [Energy Star Portfolio Manager](https://www.energystar.gov/buildings/benchmark)
- Article XIV - High-Performance Existing Buildings Program (see ./energize-denver-requirements.md)

## Workflow Example

1. **Receive Request**: Example Client needs Energize Denver audit pricing for two apartment buildings
2. **Gather Info**: Building IDs 15708 & 15118, square footages, addresses
3. **Determine Service**: ASHRAE Level 2 Energy Audit (typical for compliance pathway)
4. **Calculate Pricing**: Base on sq ft, # buildings, timeline (audits due 12/31/25)
5. **Generate Proposal**: Use script with building info, service type, pricing
6. **Review & Customize**: Verify compliance requirements, adjust scope if needed
7. **Deliver**: Send .docx proposal to client

## Support Files

- `./energize-denver-requirements.md` - Complete Article XIV compliance details
- `./service-types.md` - Scope templates for each service type
- `./pricing-guidelines.md` - Pricing models and factors
- `./templates/proposal-template.docx` - Base Iconergy proposal template
- `./scripts/generate-proposal.py` - Proposal generation script


## Saving Next Steps

When energize-denver-proposals work is complete or paused:

```bash
node .claude/skills/work-command-center/tools/add-skill-next-steps.js \
  --skill "energize-denver-proposals" \
  --content "## Priority Tasks
1. Generate Energize Denver compliance proposal
2. Estimate benchmarking and audit costs
3. Create timeline for compliance pathway"
```

See: `.claude/skills/work-command-center/skill-next-steps-convention.md`

---
slug: "prompt-templates"
display_name: "Prompt Templates"
description: "Reusable prompt templates for construction AI tasks: cost estimation, schedule analysis, document processing, BIM queries. Structured prompts for consistent results."
---

# Prompt Templates for Construction AI

## Overview

Structured, reusable prompt templates optimized for construction industry AI tasks. These templates ensure consistent, high-quality outputs for cost estimation, schedule analysis, document processing, and BIM data queries.

## Template Framework

### Base Template Structure

```python
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from string import Template
import json

@dataclass
class PromptTemplate:
    name: str
    description: str
    template: str
    input_variables: List[str]
    output_format: Optional[str] = None
    examples: List[Dict[str, Any]] = field(default_factory=list)
    category: str = "general"
    version: str = "1.0"

    def format(self, **kwargs) -> str:
        """Format template with provided variables."""
        # Validate all required variables are provided
        missing = [v for v in self.input_variables if v not in kwargs]
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        # Format template
        prompt = Template(self.template).safe_substitute(**kwargs)

        # Add output format if specified
        if self.output_format:
            prompt += f"\n\nOutput Format:\n{self.output_format}"

        return prompt

    def with_examples(self, n: int = 2) -> str:
        """Return template with few-shot examples."""
        examples_text = ""
        for i, ex in enumerate(self.examples[:n], 1):
            examples_text += f"\nExample {i}:\n"
            examples_text += f"Input: {ex.get('input', '')}\n"
            examples_text += f"Output: {ex.get('output', '')}\n"

        return f"{examples_text}\n{self.template}"


class ConstructionPromptLibrary:
    """Library of construction-specific prompt templates."""

    def __init__(self):
        self.templates: Dict[str, PromptTemplate] = {}
        self._register_defaults()

    def register(self, template: PromptTemplate):
        self.templates[template.name] = template

    def get(self, name: str) -> Optional[PromptTemplate]:
        return self.templates.get(name)

    def list_by_category(self, category: str) -> List[PromptTemplate]:
        return [t for t in self.templates.values() if t.category == category]

    def _register_defaults(self):
        # Register all default templates
        for template in DEFAULT_TEMPLATES:
            self.register(template)
```

## Cost Estimation Templates

### Line Item Classification

```python
COST_LINE_ITEM_CLASSIFICATION = PromptTemplate(
    name="cost_line_item_classification",
    description="Classify cost estimate line items to CSI MasterFormat divisions",
    category="cost_estimation",
    input_variables=["line_items"],
    template="""You are a construction cost estimator. Classify each line item to its appropriate CSI MasterFormat division.

Line Items to Classify:
$line_items

For each line item, provide:
1. CSI Division (2-digit)
2. CSI Section (6-digit code)
3. Confidence level (high/medium/low)

Use standard CSI MasterFormat 2020 divisions:
- 03: Concrete
- 04: Masonry
- 05: Metals
- 06: Wood, Plastics, Composites
- 07: Thermal and Moisture Protection
- 08: Openings
- 09: Finishes
- 22: Plumbing
- 23: HVAC
- 26: Electrical
- 31: Earthwork
- 32: Exterior Improvements
- 33: Utilities
""",
    output_format="""JSON array with format:
[
  {
    "line_item": "original description",
    "csi_division": "XX",
    "csi_section": "XX XX XX",
    "csi_title": "Section Title",
    "confidence": "high|medium|low"
  }
]""",
    examples=[
        {
            "input": "4000 PSI concrete for foundations",
            "output": '{"csi_division": "03", "csi_section": "03 30 00", "csi_title": "Cast-in-Place Concrete", "confidence": "high"}'
        }
    ]
)
```

### Unit Cost Validation

```python
COST_UNIT_PRICE_VALIDATION = PromptTemplate(
    name="cost_unit_price_validation",
    description="Validate unit prices against industry standards",
    category="cost_estimation",
    input_variables=["line_items", "location", "year"],
    template="""You are a construction cost analyst. Review these unit prices for reasonableness.

Project Location: $location
Cost Year: $year

Line Items to Review:
$line_items

For each line item:
1. Assess if the unit price is reasonable for the location and year
2. Flag any outliers (too high or too low)
3. Suggest corrections if needed

Consider regional cost factors, labor rates, and material costs for $location.
""",
    output_format="""JSON array:
[
  {
    "line_item": "description",
    "current_unit_cost": 0.00,
    "assessment": "reasonable|high|low",
    "typical_range": {"low": 0.00, "high": 0.00},
    "suggested_unit_cost": 0.00,
    "notes": "explanation"
  }
]"""
)
```

### Estimate Summary Generation

```python
COST_ESTIMATE_SUMMARY = PromptTemplate(
    name="cost_estimate_summary",
    description="Generate executive summary from detailed estimate",
    category="cost_estimation",
    input_variables=["project_name", "estimate_data", "gross_area"],
    template="""Generate an executive summary for this construction cost estimate.

Project: $project_name
Gross Area: $gross_area SF

Estimate Data:
$estimate_data

Create a professional summary including:
1. Total project cost and cost per SF
2. Major cost drivers (top 5 divisions)
3. Key assumptions and exclusions
4. Risk factors affecting the estimate
5. Recommendations for cost optimization

Write in a professional tone suitable for owner/stakeholder presentation.
""",
    output_format="""Markdown format with sections:
## Executive Summary
## Cost Breakdown
## Key Assumptions
## Risk Factors
## Recommendations"""
)
```

## Schedule Analysis Templates

### Critical Path Analysis

```python
SCHEDULE_CRITICAL_PATH = PromptTemplate(
    name="schedule_critical_path_analysis",
    description="Analyze schedule critical path and float",
    category="scheduling",
    input_variables=["schedule_data", "data_date"],
    template="""Analyze the critical path for this construction schedule.

Data Date: $data_date

Schedule Data:
$schedule_data

Provide analysis of:
1. Current critical path activities
2. Near-critical activities (total float < 10 days)
3. Float consumption trends
4. Schedule risk areas
5. Recommendations for protecting the critical path

Focus on activities that could impact the project completion date.
""",
    output_format="""JSON:
{
  "critical_path": [
    {"activity_id": "", "name": "", "duration": 0, "total_float": 0}
  ],
  "near_critical": [...],
  "risk_areas": ["description"],
  "recommendations": ["action item"]
}"""
)
```

### Delay Analysis

```python
SCHEDULE_DELAY_ANALYSIS = PromptTemplate(
    name="schedule_delay_analysis",
    description="Analyze schedule delays and impacts",
    category="scheduling",
    input_variables=["baseline_schedule", "current_schedule", "delay_events"],
    template="""Perform a delay analysis comparing baseline to current schedule.

Baseline Schedule:
$baseline_schedule

Current Schedule:
$current_schedule

Known Delay Events:
$delay_events

Analyze:
1. Total project delay in calendar days
2. Critical path delays vs non-critical delays
3. Concurrent delays
4. Pacing delays
5. Attribution of delays (owner, contractor, third-party, weather)

Use the Time Impact Analysis (TIA) methodology.
""",
    output_format="""JSON:
{
  "total_delay_days": 0,
  "delay_breakdown": {
    "owner_caused": 0,
    "contractor_caused": 0,
    "concurrent": 0,
    "excusable": 0
  },
  "impacted_milestones": [...],
  "recommendations": [...]
}"""
)
```

### Resource Leveling

```python
SCHEDULE_RESOURCE_LEVELING = PromptTemplate(
    name="schedule_resource_leveling",
    description="Suggest resource leveling for over-allocated resources",
    category="scheduling",
    input_variables=["schedule_data", "resource_limits"],
    template="""Analyze resource allocation and suggest leveling strategies.

Schedule Data:
$schedule_data

Resource Limits:
$resource_limits

Identify:
1. Over-allocated resources by period
2. Peak demand periods
3. Activities that can be shifted (have float)
4. Recommended activity adjustments

Maintain critical path while optimizing resource usage.
""",
    output_format="""JSON:
{
  "overallocations": [
    {"resource": "", "period": "", "demand": 0, "limit": 0}
  ],
  "recommendations": [
    {"activity_id": "", "action": "shift|split|extend", "days": 0, "reason": ""}
  ],
  "revised_peak_demand": {}
}"""
)
```

## Document Processing Templates

### RFI Response Generation

```python
DOC_RFI_RESPONSE = PromptTemplate(
    name="doc_rfi_response",
    description="Generate professional RFI response",
    category="document_processing",
    input_variables=["rfi_number", "question", "context", "spec_references"],
    template="""Generate a professional response to this RFI.

RFI Number: $rfi_number

Question:
$question

Context/Background:
$context

Relevant Specification References:
$spec_references

Write a clear, professional response that:
1. Directly addresses the question
2. References relevant specifications
3. Provides clear direction
4. Notes any cost or schedule implications
5. Identifies if further clarification is needed

Maintain a professional, unambiguous tone.
""",
    output_format="""Response in professional letter format with:
- Direct answer to the question
- Supporting references
- Required actions (if any)
- Disclaimer about cost/schedule (if applicable)"""
)
```

### Specification Extraction

```python
DOC_SPEC_EXTRACTION = PromptTemplate(
    name="doc_spec_extraction",
    description="Extract key requirements from specifications",
    category="document_processing",
    input_variables=["spec_text", "section_number"],
    template="""Extract key requirements from this specification section.

Section Number: $section_number

Specification Text:
$spec_text

Extract and categorize:
1. Material requirements (products, standards, grades)
2. Performance requirements (strength, ratings, certifications)
3. Submittal requirements (shop drawings, samples, certifications)
4. Installation requirements (methods, tolerances, conditions)
5. Quality control requirements (testing, inspections)
6. Warranty requirements

Flag any ambiguous or conflicting requirements.
""",
    output_format="""JSON:
{
  "section": "XX XX XX",
  "title": "",
  "materials": [...],
  "performance": [...],
  "submittals": [...],
  "installation": [...],
  "quality_control": [...],
  "warranty": {...},
  "ambiguities": [...]
}"""
)
```

### Change Order Justification

```python
DOC_CHANGE_ORDER = PromptTemplate(
    name="doc_change_order_justification",
    description="Generate change order justification narrative",
    category="document_processing",
    input_variables=["change_description", "cause", "cost_impact", "schedule_impact", "supporting_docs"],
    template="""Generate a professional change order justification.

Change Description:
$change_description

Cause of Change:
$cause

Cost Impact: $cost_impact
Schedule Impact: $schedule_impact

Supporting Documentation:
$supporting_docs

Write a clear justification that:
1. Describes the change and its necessity
2. Explains why this was not included in the original scope
3. Details the cost basis (labor, material, equipment, markup)
4. Explains schedule impact and mitigation
5. References supporting documentation

Maintain a factual, professional tone suitable for owner review.
"""
)
```

## BIM Query Templates

### Element Quantity Extraction

```python
BIM_QTO_EXTRACTION = PromptTemplate(
    name="bim_qto_extraction",
    description="Extract quantities from BIM element data",
    category="bim",
    input_variables=["element_data", "quantity_types"],
    template="""Extract quantities from this BIM element data.

Element Data:
$element_data

Quantity Types Needed:
$quantity_types

For each element:
1. Identify the element type and classification
2. Extract requested quantities
3. Apply appropriate unit conversions
4. Group by classification code

Ensure quantities are in standard construction units (SF, LF, CY, EA, etc.).
""",
    output_format="""JSON:
{
  "summary": [
    {
      "classification": "XX XX XX",
      "description": "",
      "quantity": 0.00,
      "unit": "",
      "element_count": 0
    }
  ],
  "details": [...]
}"""
)
```

### Clash Analysis Summary

```python
BIM_CLASH_ANALYSIS = PromptTemplate(
    name="bim_clash_analysis",
    description="Summarize and prioritize BIM clash detection results",
    category="bim",
    input_variables=["clash_data", "disciplines"],
    template="""Analyze and summarize these BIM clash detection results.

Clash Data:
$clash_data

Disciplines Involved: $disciplines

Provide:
1. Summary of clash counts by discipline pair
2. Priority ranking of clashes (critical/major/minor)
3. Recommended resolution responsibility
4. Pattern analysis (recurring issues)
5. Suggested coordination meetings

Focus on actionable insights for the coordination team.
""",
    output_format="""JSON:
{
  "total_clashes": 0,
  "by_discipline_pair": {...},
  "by_priority": {"critical": 0, "major": 0, "minor": 0},
  "patterns": [...],
  "recommendations": [...]
}"""
)
```

## Template Usage

```python
# Initialize library
library = ConstructionPromptLibrary()

# Get template
template = library.get("cost_line_item_classification")

# Format with variables
prompt = template.format(
    line_items="""
    1. 4000 PSI structural concrete
    2. #5 rebar
    3. CMU block wall
    4. Steel wide flange beams
    5. Spray foam insulation
    """
)

# Use with LLM
response = llm.generate(prompt)

# With few-shot examples
prompt_with_examples = template.with_examples(n=2)
```

## Custom Template Creation

```python
# Create project-specific template
my_template = PromptTemplate(
    name="my_project_template",
    description="Custom template for specific project needs",
    category="custom",
    input_variables=["var1", "var2"],
    template="""
    Your custom prompt here with $var1 and $var2 placeholders.
    """,
    output_format="JSON or other format specification"
)

# Register to library
library.register(my_template)
```

## Best Practices

1. **Be Specific**: Include domain context (CSI codes, construction terms)
2. **Define Output Format**: Always specify expected JSON/Markdown structure
3. **Include Examples**: Few-shot examples improve consistency
4. **Version Templates**: Track changes for reproducibility
5. **Test Thoroughly**: Validate outputs match expected format

## Resources

- **Prompt Engineering Guide**: https://www.promptingguide.ai/
- **CSI MasterFormat**: https://www.csiresources.org/standards/masterformat
- **Construction Terminology**: AIA, AGC, CMAA glossaries

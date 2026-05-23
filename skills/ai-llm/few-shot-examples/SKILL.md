---
name: few-shot-examples
description: "Curated few-shot examples for construction AI tasks: classification, extraction, analysis. Domain-specific examples for improved LLM performance."
---

# Few-Shot Examples for Construction AI

## Overview

Curated few-shot examples for construction industry AI tasks. These examples improve LLM performance by providing domain-specific context for classification, extraction, and analysis tasks.

## Few-Shot Framework

### Example Manager

```python
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import json
import random

@dataclass
class FewShotExample:
    input: str
    output: str
    explanation: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    difficulty: str = "medium"  # easy, medium, hard
    source: str = ""

@dataclass
class ExampleSet:
    name: str
    description: str
    task_type: str
    examples: List[FewShotExample]
    version: str = "1.0"

    def get_examples(self, n: int = 3, difficulty: str = None) -> List[FewShotExample]:
        """Get n examples, optionally filtered by difficulty."""
        filtered = self.examples
        if difficulty:
            filtered = [e for e in self.examples if e.difficulty == difficulty]
        return filtered[:n]

    def get_random_examples(self, n: int = 3) -> List[FewShotExample]:
        """Get n random examples for variety."""
        return random.sample(self.examples, min(n, len(self.examples)))

    def format_for_prompt(self, n: int = 3) -> str:
        """Format examples for inclusion in prompt."""
        examples = self.get_examples(n)
        formatted = []

        for i, ex in enumerate(examples, 1):
            formatted.append(f"Example {i}:")
            formatted.append(f"Input: {ex.input}")
            formatted.append(f"Output: {ex.output}")
            if ex.explanation:
                formatted.append(f"Explanation: {ex.explanation}")
            formatted.append("")

        return "\n".join(formatted)


class ConstructionExampleLibrary:
    """Library of construction-specific few-shot examples."""

    def __init__(self):
        self.example_sets: Dict[str, ExampleSet] = {}
        self._register_defaults()

    def register(self, example_set: ExampleSet):
        self.example_sets[example_set.name] = example_set

    def get(self, name: str) -> Optional[ExampleSet]:
        return self.example_sets.get(name)

    def _register_defaults(self):
        for example_set in DEFAULT_EXAMPLE_SETS:
            self.register(example_set)
```

## CSI Classification Examples

```python
CSI_CLASSIFICATION_EXAMPLES = ExampleSet(
    name="csi_classification",
    description="Examples for classifying line items to CSI MasterFormat",
    task_type="classification",
    examples=[
        FewShotExample(
            input="4000 PSI structural concrete for foundations",
            output=json.dumps({
                "csi_division": "03",
                "csi_section": "03 30 00",
                "csi_title": "Cast-in-Place Concrete",
                "confidence": "high"
            }),
            explanation="Structural concrete is Division 03, Cast-in-Place section",
            tags=["concrete", "structural"],
            difficulty="easy"
        ),
        FewShotExample(
            input="Grade 60 #5 reinforcing steel",
            output=json.dumps({
                "csi_division": "03",
                "csi_section": "03 20 00",
                "csi_title": "Concrete Reinforcing",
                "confidence": "high"
            }),
            explanation="Rebar is in Division 03 under reinforcing, not Division 05 Metals",
            tags=["rebar", "concrete"],
            difficulty="medium"
        ),
        FewShotExample(
            input="8\" CMU block wall with vertical rebar",
            output=json.dumps({
                "csi_division": "04",
                "csi_section": "04 22 00",
                "csi_title": "Concrete Unit Masonry",
                "confidence": "high"
            }),
            explanation="CMU is concrete masonry, Division 04",
            tags=["masonry", "cmu"],
            difficulty="easy"
        ),
        FewShotExample(
            input="W12x26 structural steel beams",
            output=json.dumps({
                "csi_division": "05",
                "csi_section": "05 12 00",
                "csi_title": "Structural Steel Framing",
                "confidence": "high"
            }),
            explanation="Wide flange beams are structural steel, Division 05",
            tags=["steel", "structural"],
            difficulty="easy"
        ),
        FewShotExample(
            input="6\" spray foam insulation R-38",
            output=json.dumps({
                "csi_division": "07",
                "csi_section": "07 21 00",
                "csi_title": "Thermal Insulation",
                "confidence": "high"
            }),
            explanation="All insulation types are in Division 07",
            tags=["insulation", "thermal"],
            difficulty="easy"
        ),
        FewShotExample(
            input="Hollow metal door frame 3'x7'",
            output=json.dumps({
                "csi_division": "08",
                "csi_section": "08 11 00",
                "csi_title": "Metal Doors and Frames",
                "confidence": "high"
            }),
            explanation="Metal doors and frames are in Division 08 Openings",
            tags=["doors", "openings"],
            difficulty="easy"
        ),
        FewShotExample(
            input="5/8\" Type X gypsum board on metal studs",
            output=json.dumps({
                "csi_division": "09",
                "csi_section": "09 29 00",
                "csi_title": "Gypsum Board",
                "confidence": "high"
            }),
            explanation="Gypsum board (drywall) is in Division 09 Finishes",
            tags=["drywall", "finishes"],
            difficulty="easy"
        ),
        FewShotExample(
            input="VCT flooring in corridors",
            output=json.dumps({
                "csi_division": "09",
                "csi_section": "09 65 00",
                "csi_title": "Resilient Flooring",
                "confidence": "high"
            }),
            explanation="VCT (vinyl composition tile) is resilient flooring in Division 09",
            tags=["flooring", "finishes"],
            difficulty="medium"
        ),
        FewShotExample(
            input="Fire sprinkler system - ordinary hazard",
            output=json.dumps({
                "csi_division": "21",
                "csi_section": "21 13 00",
                "csi_title": "Fire-Suppression Sprinkler Systems",
                "confidence": "high"
            }),
            explanation="Fire sprinklers are Division 21 Fire Suppression",
            tags=["fire protection", "mep"],
            difficulty="medium"
        ),
        FewShotExample(
            input="Domestic water piping - copper type L",
            output=json.dumps({
                "csi_division": "22",
                "csi_section": "22 11 00",
                "csi_title": "Facility Water Distribution",
                "confidence": "high"
            }),
            explanation="Domestic water piping is Division 22 Plumbing",
            tags=["plumbing", "mep"],
            difficulty="medium"
        ),
        FewShotExample(
            input="VAV boxes with hot water reheat",
            output=json.dumps({
                "csi_division": "23",
                "csi_section": "23 36 00",
                "csi_title": "Air Terminal Units",
                "confidence": "high"
            }),
            explanation="VAV boxes are air terminal units in Division 23 HVAC",
            tags=["hvac", "mep"],
            difficulty="medium"
        ),
        FewShotExample(
            input="277/480V 3-phase electrical distribution panel",
            output=json.dumps({
                "csi_division": "26",
                "csi_section": "26 24 00",
                "csi_title": "Switchboards and Panelboards",
                "confidence": "high"
            }),
            explanation="Electrical panels are in Division 26",
            tags=["electrical", "mep"],
            difficulty="medium"
        ),
        FewShotExample(
            input="Site excavation and grading - 5000 CY",
            output=json.dumps({
                "csi_division": "31",
                "csi_section": "31 20 00",
                "csi_title": "Earth Moving",
                "confidence": "high"
            }),
            explanation="Excavation and grading is Division 31 Earthwork",
            tags=["sitework", "earthwork"],
            difficulty="easy"
        ),
        FewShotExample(
            input="Asphalt paving for parking lot - 3\" thick",
            output=json.dumps({
                "csi_division": "32",
                "csi_section": "32 12 00",
                "csi_title": "Flexible Paving",
                "confidence": "high"
            }),
            explanation="Asphalt paving is in Division 32 Exterior Improvements",
            tags=["paving", "sitework"],
            difficulty="easy"
        ),
        FewShotExample(
            input="8\" DIP water main with fittings",
            output=json.dumps({
                "csi_division": "33",
                "csi_section": "33 11 00",
                "csi_title": "Water Utility Distribution Piping",
                "confidence": "high"
            }),
            explanation="Site utilities are in Division 33",
            tags=["utilities", "sitework"],
            difficulty="medium"
        )
    ]
)
```

## RFI Classification Examples

```python
RFI_CLASSIFICATION_EXAMPLES = ExampleSet(
    name="rfi_classification",
    description="Examples for classifying RFI types and urgency",
    task_type="classification",
    examples=[
        FewShotExample(
            input="Drawing A-301 shows a door at grid line 5, but the structural drawing S-102 shows a column at the same location. Please clarify.",
            output=json.dumps({
                "rfi_type": "conflict_clarification",
                "disciplines": ["architectural", "structural"],
                "urgency": "high",
                "impact_areas": ["design", "schedule"],
                "suggested_routing": "architect"
            }),
            explanation="Drawing conflict between disciplines requires urgent resolution",
            tags=["conflict", "multi-discipline"],
            difficulty="medium"
        ),
        FewShotExample(
            input="Specification section 09 91 00 calls for Benjamin Moore paint, but we would like to submit Sherwin-Williams as an equal. Is this acceptable?",
            output=json.dumps({
                "rfi_type": "substitution_request",
                "disciplines": ["architectural"],
                "urgency": "low",
                "impact_areas": ["cost"],
                "suggested_routing": "architect"
            }),
            explanation="Substitution request is low urgency, cost-driven",
            tags=["substitution", "finishes"],
            difficulty="easy"
        ),
        FewShotExample(
            input="We encountered rock during excavation at elevation 95.5'. Drawings show bottom of footing at elevation 94.0'. How should we proceed?",
            output=json.dumps({
                "rfi_type": "field_condition",
                "disciplines": ["structural", "geotechnical"],
                "urgency": "critical",
                "impact_areas": ["design", "cost", "schedule"],
                "suggested_routing": "structural_engineer"
            }),
            explanation="Unforeseen site condition affecting structural design is critical",
            tags=["field condition", "foundation"],
            difficulty="hard"
        ),
        FewShotExample(
            input="What is the required fire rating for the corridor walls on Level 2? The drawing notes are unclear.",
            output=json.dumps({
                "rfi_type": "clarification",
                "disciplines": ["architectural"],
                "urgency": "medium",
                "impact_areas": ["design"],
                "suggested_routing": "architect"
            }),
            explanation="Missing information request, medium urgency",
            tags=["fire rating", "clarification"],
            difficulty="easy"
        ),
        FewShotExample(
            input="The mechanical contractor has proposed routing ductwork through the structural transfer beam. Please confirm this is acceptable.",
            output=json.dumps({
                "rfi_type": "coordination",
                "disciplines": ["mechanical", "structural"],
                "urgency": "high",
                "impact_areas": ["design", "schedule"],
                "suggested_routing": "structural_engineer"
            }),
            explanation="MEP penetration through structural element requires SE approval",
            tags=["coordination", "mep", "structural"],
            difficulty="medium"
        )
    ]
)
```

## Cost Analysis Examples

```python
COST_ANALYSIS_EXAMPLES = ExampleSet(
    name="cost_analysis",
    description="Examples for cost analysis and validation",
    task_type="analysis",
    examples=[
        FewShotExample(
            input=json.dumps({
                "item": "Cast-in-place concrete",
                "unit_cost": 850,
                "unit": "CY",
                "location": "New York City",
                "year": 2026
            }),
            output=json.dumps({
                "assessment": "high",
                "typical_range": {"low": 400, "high": 700},
                "variance_percent": 21.4,
                "likely_causes": ["high local labor rates", "difficult access", "small quantity"],
                "recommendation": "Review labor productivity assumptions and access conditions"
            }),
            explanation="NYC concrete costs are high, but $850/CY exceeds typical range",
            tags=["concrete", "unit cost", "validation"],
            difficulty="medium"
        ),
        FewShotExample(
            input=json.dumps({
                "item": "Structural steel erection",
                "unit_cost": 1200,
                "unit": "TON",
                "location": "Houston, TX",
                "year": 2026
            }),
            output=json.dumps({
                "assessment": "reasonable",
                "typical_range": {"low": 1000, "high": 1500},
                "variance_percent": 0,
                "likely_causes": [],
                "recommendation": "No action needed - within expected range"
            }),
            explanation="Steel erection cost is within normal Houston range",
            tags=["steel", "unit cost", "validation"],
            difficulty="easy"
        ),
        FewShotExample(
            input=json.dumps({
                "item": "Gypsum board partition",
                "unit_cost": 3.50,
                "unit": "SF",
                "location": "Phoenix, AZ",
                "year": 2026
            }),
            output=json.dumps({
                "assessment": "low",
                "typical_range": {"low": 6, "high": 12},
                "variance_percent": -41.7,
                "likely_causes": ["missing framing", "missing tape/finish", "labor underestimated"],
                "recommendation": "Verify scope includes metal studs, insulation, and Level 4 finish"
            }),
            explanation="Very low drywall cost likely missing scope items",
            tags=["drywall", "unit cost", "validation"],
            difficulty="medium"
        )
    ]
)
```

## Schedule Analysis Examples

```python
SCHEDULE_ANALYSIS_EXAMPLES = ExampleSet(
    name="schedule_analysis",
    description="Examples for schedule analysis and review",
    task_type="analysis",
    examples=[
        FewShotExample(
            input=json.dumps({
                "activity": "Foundation concrete pour",
                "duration": 45,
                "duration_unit": "days",
                "quantity": 2500,
                "quantity_unit": "CY"
            }),
            output=json.dumps({
                "assessment": "duration_appears_long",
                "typical_production": "100-150 CY/day",
                "expected_duration_range": {"low": 17, "high": 25},
                "possible_reasons": ["phased pours", "complex formwork", "cure time included"],
                "recommendation": "Review activity scope - may include formwork and curing"
            }),
            explanation="45 days for 2500 CY seems long unless multiple activities combined",
            tags=["concrete", "duration", "validation"],
            difficulty="medium"
        ),
        FewShotExample(
            input=json.dumps({
                "activity": "Steel erection",
                "duration": 60,
                "duration_unit": "days",
                "quantity": 500,
                "quantity_unit": "tons",
                "resources": ["1 erection crew"]
            }),
            output=json.dumps({
                "assessment": "reasonable",
                "typical_production": "8-12 tons/day/crew",
                "expected_duration_range": {"low": 42, "high": 63},
                "possible_reasons": [],
                "recommendation": "Duration is within expected range for single crew"
            }),
            explanation="500 tons with 1 crew at 8-10 tons/day = 50-63 days",
            tags=["steel", "duration", "validation"],
            difficulty="medium"
        ),
        FewShotExample(
            input=json.dumps({
                "predecessor": "Foundation complete",
                "successor": "Steel erection",
                "lag": -5,
                "lag_unit": "days"
            }),
            output=json.dumps({
                "assessment": "aggressive",
                "concern": "Steel erection starting 5 days before foundation complete",
                "typical_practice": "FS+0 to FS+5 lag for concrete cure",
                "risk_level": "high",
                "recommendation": "Verify foundation is cured sufficiently before steel loads applied"
            }),
            explanation="Negative lag on foundation to steel is risky",
            tags=["logic", "dependency", "validation"],
            difficulty="hard"
        )
    ]
)
```

## BIM Data Examples

```python
BIM_EXTRACTION_EXAMPLES = ExampleSet(
    name="bim_extraction",
    description="Examples for BIM data extraction and interpretation",
    task_type="extraction",
    examples=[
        FewShotExample(
            input=json.dumps({
                "element_type": "IfcWall",
                "properties": {
                    "Name": "Interior Partition",
                    "IsExternal": False,
                    "FireRating": "1 Hour",
                    "Pset_WallCommon.Width": 0.165,
                    "BaseQuantities.GrossArea": 45.5,
                    "BaseQuantities.NetArea": 42.3
                }
            }),
            output=json.dumps({
                "classification": "Interior wall",
                "fire_rated": True,
                "fire_rating": "1 Hour",
                "thickness_mm": 165,
                "thickness_in": 6.5,
                "gross_area_m2": 45.5,
                "gross_area_sf": 490,
                "net_area_sf": 455,
                "opening_deduction_pct": 7.0
            }),
            explanation="Extract and convert BIM properties to construction quantities",
            tags=["wall", "quantities", "ifc"],
            difficulty="medium"
        ),
        FewShotExample(
            input=json.dumps({
                "element_type": "IfcDoor",
                "properties": {
                    "Name": "D-01",
                    "OverallWidth": 0.914,
                    "OverallHeight": 2.134,
                    "FireRating": None,
                    "Pset_DoorCommon.IsExternal": False,
                    "Pset_DoorCommon.HandicapAccessible": True
                }
            }),
            output=json.dumps({
                "door_type": "D-01",
                "size": "3'-0\" x 7'-0\"",
                "size_standard": "36x84",
                "fire_rated": False,
                "ada_compliant": True,
                "classification": "Interior door, ADA"
            }),
            explanation="Interpret door properties for specification compliance",
            tags=["door", "ada", "ifc"],
            difficulty="easy"
        ),
        FewShotExample(
            input=json.dumps({
                "element_type": "IfcSpace",
                "properties": {
                    "Name": "Conference Room 101",
                    "LongName": "Large Conference Room",
                    "Pset_SpaceCommon.NetFloorArea": 55.7,
                    "Pset_SpaceOccupancyRequirements.OccupancyNumber": 20,
                    "Pset_SpaceFireSafetyRequirements.FireRiskFactor": "Low"
                }
            }),
            output=json.dumps({
                "space_name": "Conference Room 101",
                "net_area_sf": 600,
                "occupancy": 20,
                "area_per_person_sf": 30,
                "occupancy_assessment": "typical for conference",
                "code_check": "IBC allows 15 SF/person for assembly, 600 SF / 15 = 40 max"
            }),
            explanation="Validate space programming against code requirements",
            tags=["space", "occupancy", "code"],
            difficulty="hard"
        )
    ]
)
```

## Using Examples in Prompts

```python
# Initialize library
library = ConstructionExampleLibrary()

# Get example set
csi_examples = library.get("csi_classification")

# Format for prompt
examples_text = csi_examples.format_for_prompt(n=3)

# Build complete prompt
prompt = f"""Classify the following line items to CSI MasterFormat.

{examples_text}

Now classify these items:
1. Aluminum storefront framing
2. Acoustic ceiling tiles
3. Elevator cab finishes
"""

# Or get specific examples
easy_examples = csi_examples.get_examples(n=2, difficulty="easy")
random_examples = csi_examples.get_random_examples(n=3)
```

## Adding Custom Examples

```python
# Create custom example set for your project
my_examples = ExampleSet(
    name="my_project_classification",
    description="Project-specific classification examples",
    task_type="classification",
    examples=[
        FewShotExample(
            input="Your specific input",
            output="Expected output",
            explanation="Why this classification",
            tags=["custom"],
            difficulty="medium"
        )
    ]
)

# Register to library
library.register(my_examples)
```

## Best Practices

1. **Diverse Examples**: Include examples across difficulty levels
2. **Edge Cases**: Add examples for ambiguous situations
3. **Explanations**: Include reasoning for complex examples
4. **Regular Updates**: Add new examples as edge cases are discovered
5. **Balance**: Mix easy and hard examples to calibrate model

## Resources

- **Few-Shot Learning**: https://www.promptingguide.ai/techniques/fewshot
- **CSI MasterFormat**: Complete division listings
- **Construction Terminology**: Industry glossaries and standards

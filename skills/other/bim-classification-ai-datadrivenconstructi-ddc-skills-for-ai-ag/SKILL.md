---
slug: "bim-classification-ai"
display_name: "BIM Classification AI"
description: "Classify BIM elements using AI and standard classification systems. Map elements to UniFormat, MasterFormat, OmniClass, and CWICR codes."
---

# BIM Classification AI

## Business Case

### Problem Statement
BIM models often lack proper classification:
- Elements without classification codes
- Inconsistent naming conventions
- Manual classification is tedious
- Difficult to map to cost databases

### Solution
AI-powered classification system that analyzes BIM element properties and suggests appropriate classification codes from multiple standards.

### Business Value
- **Automation** - Reduce manual classification effort
- **Consistency** - Standardized classification across projects
- **Integration** - Enable cost estimation and QTO
- **Quality** - Improved data quality in BIM models

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re


class ClassificationSystem(Enum):
    """Classification standards."""
    UNIFORMAT = "uniformat"
    MASTERFORMAT = "masterformat"
    OMNICLASS = "omniclass"
    UNICLASS = "uniclass"
    CWICR = "cwicr"


@dataclass
class ClassificationCode:
    """Classification code with metadata."""
    code: str
    title: str
    system: ClassificationSystem
    level: int
    parent_code: Optional[str] = None
    keywords: List[str] = field(default_factory=list)


@dataclass
class ClassificationResult:
    """Result of classification attempt."""
    element_id: str
    element_name: str
    element_category: str
    suggested_codes: List[Tuple[ClassificationCode, float]]  # (code, confidence)
    selected_code: Optional[ClassificationCode] = None
    manual_override: bool = False


class ClassificationDatabase:
    """Classification codes database."""

    def __init__(self):
        self.codes: Dict[ClassificationSystem, List[ClassificationCode]] = {
            system: [] for system in ClassificationSystem
        }
        self._load_standard_codes()

    def _load_standard_codes(self):
        """Load standard classification codes."""
        # UniFormat II codes
        uniformat_codes = [
            ("A", "Substructure", 1, None, ["foundation", "basement", "excavation"]),
            ("A10", "Foundations", 2, "A", ["footing", "pile", "foundation"]),
            ("A1010", "Standard Foundations", 3, "A10", ["spread footing", "strip footing"]),
            ("A1020", "Special Foundations", 3, "A10", ["pile", "caisson", "mat foundation"]),
            ("B", "Shell", 1, None, ["superstructure", "exterior", "roof"]),
            ("B10", "Superstructure", 2, "B", ["floor", "roof", "structure"]),
            ("B1010", "Floor Construction", 3, "B10", ["slab", "deck", "floor"]),
            ("B1020", "Roof Construction", 3, "B10", ["roof", "deck", "truss"]),
            ("B20", "Exterior Enclosure", 2, "B", ["wall", "window", "door"]),
            ("B2010", "Exterior Walls", 3, "B20", ["curtain wall", "masonry", "cladding"]),
            ("B2020", "Exterior Windows", 3, "B20", ["window", "glazing", "storefront"]),
            ("B30", "Roofing", 2, "B", ["roof", "membrane", "insulation"]),
            ("C", "Interiors", 1, None, ["partition", "ceiling", "floor finish"]),
            ("C10", "Interior Construction", 2, "C", ["partition", "door", "glazing"]),
            ("C20", "Stairs", 2, "C", ["stair", "railing", "ladder"]),
            ("C30", "Interior Finishes", 2, "C", ["finish", "paint", "flooring"]),
            ("D", "Services", 1, None, ["mechanical", "electrical", "plumbing"]),
            ("D10", "Conveying", 2, "D", ["elevator", "escalator", "lift"]),
            ("D20", "Plumbing", 2, "D", ["pipe", "fixture", "drain"]),
            ("D30", "HVAC", 2, "D", ["duct", "hvac", "air handling"]),
            ("D40", "Fire Protection", 2, "D", ["sprinkler", "fire", "suppression"]),
            ("D50", "Electrical", 2, "D", ["electrical", "power", "lighting"]),
        ]

        for code, title, level, parent, keywords in uniformat_codes:
            self.codes[ClassificationSystem.UNIFORMAT].append(
                ClassificationCode(code, title, ClassificationSystem.UNIFORMAT, level, parent, keywords)
            )

        # MasterFormat codes (simplified)
        masterformat_codes = [
            ("03", "Concrete", 1, None, ["concrete", "formwork", "reinforcing"]),
            ("03 30 00", "Cast-in-Place Concrete", 2, "03", ["concrete", "pour", "slab"]),
            ("03 41 00", "Precast Structural Concrete", 2, "03", ["precast", "concrete", "panel"]),
            ("04", "Masonry", 1, None, ["brick", "block", "stone"]),
            ("05", "Metals", 1, None, ["steel", "metal", "aluminum"]),
            ("05 12 00", "Structural Steel Framing", 2, "05", ["beam", "column", "steel"]),
            ("06", "Wood, Plastics, Composites", 1, None, ["wood", "timber", "lumber"]),
            ("07", "Thermal and Moisture Protection", 1, None, ["insulation", "roofing", "waterproofing"]),
            ("08", "Openings", 1, None, ["door", "window", "glazing"]),
            ("09", "Finishes", 1, None, ["drywall", "paint", "flooring"]),
            ("21", "Fire Suppression", 1, None, ["sprinkler", "fire", "suppression"]),
            ("22", "Plumbing", 1, None, ["pipe", "fixture", "plumbing"]),
            ("23", "HVAC", 1, None, ["hvac", "duct", "mechanical"]),
            ("26", "Electrical", 1, None, ["electrical", "power", "lighting"]),
        ]

        for code, title, level, parent, keywords in masterformat_codes:
            self.codes[ClassificationSystem.MASTERFORMAT].append(
                ClassificationCode(code, title, ClassificationSystem.MASTERFORMAT, level, parent, keywords)
            )

    def search(self, query: str, system: ClassificationSystem = None) -> List[ClassificationCode]:
        """Search classification codes by keyword."""
        results = []
        query_lower = query.lower()

        systems = [system] if system else list(ClassificationSystem)

        for sys in systems:
            for code in self.codes.get(sys, []):
                # Check title
                if query_lower in code.title.lower():
                    results.append(code)
                    continue
                # Check keywords
                if any(query_lower in kw.lower() for kw in code.keywords):
                    results.append(code)

        return results


class BIMClassificationAI:
    """AI-powered BIM element classification."""

    def __init__(self, classification_db: ClassificationDatabase = None):
        self.db = classification_db or ClassificationDatabase()
        self.category_mappings = self._load_category_mappings()
        self.results: List[ClassificationResult] = []

    def _load_category_mappings(self) -> Dict[str, List[str]]:
        """Load Revit/IFC category to classification mappings."""
        return {
            # Structural
            "Structural Columns": ["B10", "05 12 00", "column", "structural"],
            "Structural Framing": ["B10", "05 12 00", "beam", "framing"],
            "Structural Foundations": ["A10", "03 30 00", "foundation", "footing"],
            "Floors": ["B1010", "03 30 00", "floor", "slab"],
            # Architectural
            "Walls": ["B20", "04", "wall", "partition"],
            "Curtain Walls": ["B2010", "08 44 00", "curtain wall", "glazing"],
            "Windows": ["B2020", "08 50 00", "window", "glazing"],
            "Doors": ["C10", "08 10 00", "door", "opening"],
            "Roofs": ["B30", "07 50 00", "roof", "roofing"],
            "Ceilings": ["C30", "09 51 00", "ceiling", "finish"],
            "Stairs": ["C20", "05 51 00", "stair", "railing"],
            # MEP
            "Ducts": ["D30", "23 31 00", "duct", "hvac"],
            "Pipes": ["D20", "22 11 00", "pipe", "plumbing"],
            "Electrical Equipment": ["D50", "26 20 00", "electrical", "panel"],
            "Lighting Fixtures": ["D50", "26 51 00", "light", "fixture"],
            "Sprinklers": ["D40", "21 13 00", "sprinkler", "fire protection"],
            "Mechanical Equipment": ["D30", "23 70 00", "ahu", "hvac equipment"],
        }

    def classify_element(self,
                        element_id: str,
                        element_name: str,
                        category: str,
                        properties: Dict[str, Any] = None,
                        target_systems: List[ClassificationSystem] = None) -> ClassificationResult:
        """Classify a single BIM element."""

        target_systems = target_systems or [ClassificationSystem.UNIFORMAT, ClassificationSystem.MASTERFORMAT]
        suggestions = []

        # Get keywords from category mapping
        keywords = self.category_mappings.get(category, [])

        # Add keywords from element name
        name_words = re.findall(r'\w+', element_name.lower())
        keywords.extend(name_words)

        # Add keywords from properties
        if properties:
            for key, value in properties.items():
                if isinstance(value, str):
                    keywords.extend(re.findall(r'\w+', value.lower()))

        # Search classification codes
        for system in target_systems:
            for keyword in keywords:
                matches = self.db.search(keyword, system)
                for match in matches:
                    confidence = self._calculate_confidence(match, keywords, category)
                    suggestions.append((match, confidence))

        # Remove duplicates and sort by confidence
        seen = set()
        unique_suggestions = []
        for code, conf in sorted(suggestions, key=lambda x: x[1], reverse=True):
            if code.code not in seen:
                seen.add(code.code)
                unique_suggestions.append((code, conf))

        result = ClassificationResult(
            element_id=element_id,
            element_name=element_name,
            element_category=category,
            suggested_codes=unique_suggestions[:5],
            selected_code=unique_suggestions[0][0] if unique_suggestions else None
        )

        self.results.append(result)
        return result

    def _calculate_confidence(self, code: ClassificationCode,
                             keywords: List[str], category: str) -> float:
        """Calculate classification confidence score."""
        score = 0.0

        # Direct category match
        if category in self.category_mappings:
            if code.code in self.category_mappings[category]:
                score += 0.5

        # Keyword matches
        keyword_matches = sum(1 for kw in keywords if kw.lower() in
                            [k.lower() for k in code.keywords])
        score += min(keyword_matches * 0.1, 0.3)

        # Title match
        title_words = code.title.lower().split()
        title_matches = sum(1 for kw in keywords if kw.lower() in title_words)
        score += min(title_matches * 0.1, 0.2)

        return min(score, 1.0)

    def classify_batch(self, elements_df: pd.DataFrame,
                      id_column: str = 'element_id',
                      name_column: str = 'name',
                      category_column: str = 'category') -> pd.DataFrame:
        """Classify multiple elements from DataFrame."""

        results = []
        for _, row in elements_df.iterrows():
            result = self.classify_element(
                element_id=str(row[id_column]),
                element_name=str(row[name_column]),
                category=str(row[category_column]),
                properties=row.to_dict()
            )

            results.append({
                'element_id': result.element_id,
                'element_name': result.element_name,
                'category': result.element_category,
                'uniformat_code': next((c.code for c, _ in result.suggested_codes
                                       if c.system == ClassificationSystem.UNIFORMAT), None),
                'masterformat_code': next((c.code for c, _ in result.suggested_codes
                                          if c.system == ClassificationSystem.MASTERFORMAT), None),
                'confidence': result.suggested_codes[0][1] if result.suggested_codes else 0
            })

        return pd.DataFrame(results)

    def get_summary(self) -> Dict[str, Any]:
        """Get classification summary."""
        total = len(self.results)
        classified = sum(1 for r in self.results if r.selected_code)
        high_confidence = sum(1 for r in self.results
                            if r.suggested_codes and r.suggested_codes[0][1] > 0.7)

        return {
            'total_elements': total,
            'classified': classified,
            'classification_rate': round(classified / total * 100, 1) if total > 0 else 0,
            'high_confidence': high_confidence,
            'high_confidence_rate': round(high_confidence / total * 100, 1) if total > 0 else 0
        }

    def export_results(self) -> pd.DataFrame:
        """Export classification results to DataFrame."""
        data = []
        for result in self.results:
            row = {
                'element_id': result.element_id,
                'element_name': result.element_name,
                'category': result.element_category,
                'selected_code': result.selected_code.code if result.selected_code else None,
                'selected_title': result.selected_code.title if result.selected_code else None,
                'selected_system': result.selected_code.system.value if result.selected_code else None,
                'manual_override': result.manual_override
            }

            # Add top suggestions
            for i, (code, conf) in enumerate(result.suggested_codes[:3]):
                row[f'suggestion_{i+1}_code'] = code.code
                row[f'suggestion_{i+1}_confidence'] = round(conf, 2)

            data.append(row)

        return pd.DataFrame(data)
```

## Quick Start

```python
# Initialize classifier
classifier = BIMClassificationAI()

# Classify single element
result = classifier.classify_element(
    element_id="12345",
    element_name="Concrete Floor Slab Level 2",
    category="Floors",
    properties={'material': 'Concrete', 'thickness': '200mm'}
)

print(f"Suggested: {result.selected_code.code} - {result.selected_code.title}")
print(f"Confidence: {result.suggested_codes[0][1]:.1%}")
```

## Common Use Cases

### 1. Batch Classification
```python
# Load BIM elements
elements = pd.read_excel("bim_elements.xlsx")

# Classify all
classified = classifier.classify_batch(elements)
classified.to_excel("classified_elements.xlsx")
```

### 2. Map to CWICR
```python
# Get UniFormat code for cost mapping
uniformat = result.selected_code.code
cwicr_code = map_uniformat_to_cwicr(uniformat)
```

### 3. Quality Check
```python
summary = classifier.get_summary()
print(f"Classification rate: {summary['classification_rate']}%")
```

## Resources
- **DDC Book**: Chapter 2.5 - Data Standards
- **Reference**: UniFormat II, CSI MasterFormat

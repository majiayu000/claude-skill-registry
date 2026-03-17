---
name: "cad-to-data"
description: "Convert CAD/BIM files to structured data. Extract element data from Revit, IFC, DWG, DGN files."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw":{"emoji":"🗂️","os":["darwin","linux","win32"],"homepage":"https://datadrivenconstruction.io","requires":{"bins":["python3"]}}}
---

# CAD To Data

## Overview

Based on DDC methodology (Chapter 2.4), this skill converts CAD and BIM files to structured data, extracting element properties, quantities, and relationships from Revit, IFC, DWG, and DGN files.

**Book Reference:** "Преобразование данных в структурированную форму" / "Data Transformation to Structured Form"

## Quick Start

```python
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any, Tuple, Generator
from datetime import datetime
import json

class CADFormat(Enum):
    """Supported CAD/BIM formats"""
    IFC = "ifc"
    RVT = "rvt"
    DWG = "dwg"
    DXF = "dxf"
    DGN = "dgn"
    NWD = "nwd"
    STEP = "step"

class ElementCategory(Enum):
    """BIM element categories"""
    WALL = "wall"
    FLOOR = "floor"
    ROOF = "roof"
    CEILING = "ceiling"
    DOOR = "door"
    WINDOW = "window"
    COLUMN = "column"
    BEAM = "beam"
    STAIR = "stair"
    RAMP = "ramp"
    FURNITURE = "furniture"
    EQUIPMENT = "equipment"
    PIPE = "pipe"
    DUCT = "duct"
    CABLE_TRAY = "cable_tray"
    SPACE = "space"
    GENERIC = "generic"

@dataclass
class Point3D:
    """3D point"""
    x: float
    y: float
    z: float

@dataclass
class BoundingBox3D:
    """3D bounding box"""
    min_point: Point3D
    max_point: Point3D

    @property
    def width(self) -> float:
        return abs(self.max_point.x - self.min_point.x)

    @property
    def depth(self) -> float:
        return abs(self.max_point.y - self.min_point.y)

    @property
    def height(self) -> float:
        return abs(self.max_point.z - self.min_point.z)

    @property
    def volume(self) -> float:
        return self.width * self.depth * self.height

@dataclass
class MaterialInfo:
    """Material information"""
    name: str
    category: str
    color: Optional[str] = None
    area: float = 0.0
    volume: float = 0.0
    properties: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CADElement:
    """Extracted CAD/BIM element"""
    id: str
    guid: str
    name: str
    category: ElementCategory
    type_name: str
    level: Optional[str] = None
    bounding_box: Optional[BoundingBox3D] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    quantities: Dict[str, float] = field(default_factory=dict)
    materials: List[MaterialInfo] = field(default_factory=list)
    relationships: Dict[str, List[str]] = field(default_factory=dict)

@dataclass
class CADLayer:
    """CAD layer information"""
    name: str
    color: Optional[str] = None
    line_type: Optional[str] = None
    visible: bool = True
    element_count: int = 0

@dataclass
class CADExtractionResult:
    """Result of CAD extraction"""
    file_path: str
    file_format: CADFormat
    elements: List[CADElement]
    layers: List[CADLayer]
    levels: List[str]
    total_elements: int
    categories: Dict[str, int]
    extraction_time: float
    metadata: Dict[str, Any] = field(default_factory=dict)


class IFCExtractor:
    """Extract data from IFC files"""

    def __init__(self):
        self.schema_version = "IFC4"
        self.element_mapping = self._build_element_mapping()

    def _build_element_mapping(self) -> Dict[str, ElementCategory]:
        """Map IFC types to categories"""
        return {
            "IfcWall": ElementCategory.WALL,
            "IfcWallStandardCase": ElementCategory.WALL,
            "IfcSlab": ElementCategory.FLOOR,
            "IfcRoof": ElementCategory.ROOF,
            "IfcCeiling": ElementCategory.CEILING,
            "IfcDoor": ElementCategory.DOOR,
            "IfcWindow": ElementCategory.WINDOW,
            "IfcColumn": ElementCategory.COLUMN,
            "IfcBeam": ElementCategory.BEAM,
            "IfcStair": ElementCategory.STAIR,
            "IfcRamp": ElementCategory.RAMP,
            "IfcFurnishingElement": ElementCategory.FURNITURE,
            "IfcPipeSegment": ElementCategory.PIPE,
            "IfcDuctSegment": ElementCategory.DUCT,
            "IfcCableCarrierSegment": ElementCategory.CABLE_TRAY,
            "IfcSpace": ElementCategory.SPACE,
        }

    def extract(
        self,
        file_path: str,
        categories: Optional[List[ElementCategory]] = None
    ) -> CADExtractionResult:
        """
        Extract data from IFC file.

        Args:
            file_path: Path to IFC file
            categories: Optional filter for categories

        Returns:
            Extraction result
        """
        start_time = datetime.now()

        # In production, use ifcopenshell:
        # import ifcopenshell
        # ifc_file = ifcopenshell.open(file_path)

        # Simulated extraction
        elements = self._simulate_ifc_elements()

        # Filter by category if specified
        if categories:
            elements = [e for e in elements if e.category in categories]

        # Build category counts
        category_counts = {}
        for element in elements:
            cat = element.category.value
            category_counts[cat] = category_counts.get(cat, 0) + 1

        # Extract levels
        levels = list(set(e.level for e in elements if e.level))

        extraction_time = (datetime.now() - start_time).total_seconds()

        return CADExtractionResult(
            file_path=file_path,
            file_format=CADFormat.IFC,
            elements=elements,
            layers=[],  # IFC doesn't use layers in traditional sense
            levels=levels,
            total_elements=len(elements),
            categories=category_counts,
            extraction_time=extraction_time,
            metadata={
                "schema": self.schema_version,
                "project_name": "Sample Project"
            }
        )

    def _simulate_ifc_elements(self) -> List[CADElement]:
        """Simulate IFC element extraction"""
        elements = []

        # Sample walls
        for i in range(10):
            elements.append(CADElement(
                id=f"wall_{i}",
                guid=f"1234567890ABCDEF{i:04d}",
                name=f"Basic Wall {i}",
                category=ElementCategory.WALL,
                type_name="Basic Wall:200mm Concrete",
                level="Level 1",
                bounding_box=BoundingBox3D(
                    min_point=Point3D(i * 5, 0, 0),
                    max_point=Point3D(i * 5 + 5, 0.2, 3)
                ),
                properties={
                    "IsExternal": True,
                    "FireRating": "1 HR",
                    "LoadBearing": True
                },
                quantities={
                    "Length": 5.0,
                    "Height": 3.0,
                    "Width": 0.2,
                    "Area": 15.0,
                    "Volume": 3.0
                },
                materials=[
                    MaterialInfo(
                        name="Concrete",
                        category="Concrete",
                        area=15.0,
                        volume=3.0
                    )
                ]
            ))

        # Sample doors
        for i in range(5):
            elements.append(CADElement(
                id=f"door_{i}",
                guid=f"DOOR0000000000{i:04d}",
                name=f"Single Door {i}",
                category=ElementCategory.DOOR,
                type_name="Single Flush:900x2100",
                level="Level 1",
                properties={
                    "FireRating": "None",
                    "IsExternal": False
                },
                quantities={
                    "Width": 0.9,
                    "Height": 2.1,
                    "Area": 1.89
                },
                relationships={
                    "host_wall": [f"wall_{i}"]
                }
            ))

        # Sample spaces
        for i in range(3):
            elements.append(CADElement(
                id=f"space_{i}",
                guid=f"SPACE000000000{i:04d}",
                name=f"Room {i+101}",
                category=ElementCategory.SPACE,
                type_name="Office",
                level="Level 1",
                quantities={
                    "Area": 25.0 + i * 5,
                    "Volume": 75.0 + i * 15,
                    "Perimeter": 20.0 + i * 2
                },
                properties={
                    "OccupancyType": "Office",
                    "DesignOccupancy": 4
                }
            ))

        return elements

    def get_quantities(
        self,
        elements: List[CADElement],
        quantity_type: str = "all"
    ) -> Dict[str, float]:
        """Aggregate quantities from elements"""
        totals = {}

        for element in elements:
            for qty_name, qty_value in element.quantities.items():
                if quantity_type == "all" or qty_name.lower() == quantity_type.lower():
                    key = f"{element.category.value}_{qty_name}"
                    totals[key] = totals.get(key, 0) + qty_value

        return totals


class DWGExtractor:
    """Extract data from DWG/DXF files"""

    def __init__(self):
        self.supported_entities = ["LINE", "POLYLINE", "CIRCLE", "ARC", "TEXT", "MTEXT", "INSERT", "HATCH"]

    def extract(
        self,
        file_path: str,
        layers: Optional[List[str]] = None
    ) -> CADExtractionResult:
        """Extract data from DWG file"""
        start_time = datetime.now()

        # In production, use ezdxf:
        # import ezdxf
        # doc = ezdxf.readfile(file_path)

        # Simulated extraction
        elements, cad_layers = self._simulate_dwg_extraction()

        # Filter by layers if specified
        if layers:
            elements = [e for e in elements if e.properties.get("layer") in layers]

        extraction_time = (datetime.now() - start_time).total_seconds()

        return CADExtractionResult(
            file_path=file_path,
            file_format=CADFormat.DWG,
            elements=elements,
            layers=cad_layers,
            levels=[],
            total_elements=len(elements),
            categories={"generic": len(elements)},
            extraction_time=extraction_time,
            metadata={"units": "millimeters"}
        )

    def _simulate_dwg_extraction(self) -> Tuple[List[CADElement], List[CADLayer]]:
        """Simulate DWG extraction"""
        elements = []
        layers = [
            CADLayer("Walls", "Red", "Continuous", True, 15),
            CADLayer("Doors", "Blue", "Continuous", True, 8),
            CADLayer("Windows", "Cyan", "Continuous", True, 12),
            CADLayer("Dimensions", "Green", "Continuous", True, 50),
            CADLayer("Text", "White", "Continuous", True, 25),
        ]

        # Simulate polylines (walls)
        for i in range(15):
            elements.append(CADElement(
                id=f"polyline_{i}",
                guid=f"PL{i:08d}",
                name=f"Polyline {i}",
                category=ElementCategory.GENERIC,
                type_name="POLYLINE",
                properties={
                    "layer": "Walls",
                    "color": "Red",
                    "closed": True
                },
                quantities={
                    "Length": 10.5 + i * 0.5
                }
            ))

        return elements, layers


class CADDataConverter:
    """
    Convert CAD/BIM files to structured data.
    Based on DDC methodology Chapter 2.4.
    """

    def __init__(self):
        self.ifc_extractor = IFCExtractor()
        self.dwg_extractor = DWGExtractor()

    def convert(
        self,
        file_path: str,
        output_format: str = "json"
    ) -> Dict[str, Any]:
        """
        Convert CAD file to structured data.

        Args:
            file_path: Path to CAD file
            output_format: Output format (json, csv, dataframe)

        Returns:
            Structured data
        """
        # Detect file format
        file_format = self._detect_format(file_path)

        # Extract based on format
        if file_format == CADFormat.IFC:
            result = self.ifc_extractor.extract(file_path)
        elif file_format in [CADFormat.DWG, CADFormat.DXF]:
            result = self.dwg_extractor.extract(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_format}")

        # Convert to output format
        return self._format_output(result, output_format)

    def _detect_format(self, file_path: str) -> CADFormat:
        """Detect CAD file format"""
        extension = file_path.lower().split(".")[-1]

        format_map = {
            "ifc": CADFormat.IFC,
            "rvt": CADFormat.RVT,
            "dwg": CADFormat.DWG,
            "dxf": CADFormat.DXF,
            "dgn": CADFormat.DGN,
            "nwd": CADFormat.NWD,
        }

        return format_map.get(extension, CADFormat.IFC)

    def _format_output(
        self,
        result: CADExtractionResult,
        format: str
    ) -> Dict[str, Any]:
        """Format extraction result"""
        output = {
            "file": result.file_path,
            "format": result.file_format.value,
            "total_elements": result.total_elements,
            "categories": result.categories,
            "levels": result.levels,
            "extraction_time": result.extraction_time,
            "elements": []
        }

        for element in result.elements:
            output["elements"].append({
                "id": element.id,
                "guid": element.guid,
                "name": element.name,
                "category": element.category.value,
                "type": element.type_name,
                "level": element.level,
                "properties": element.properties,
                "quantities": element.quantities,
                "materials": [
                    {"name": m.name, "area": m.area, "volume": m.volume}
                    for m in element.materials
                ]
            })

        return output

    def extract_quantities(
        self,
        file_path: str,
        categories: Optional[List[ElementCategory]] = None
    ) -> Dict[str, Any]:
        """Extract quantity takeoff from CAD file"""
        file_format = self._detect_format(file_path)

        if file_format == CADFormat.IFC:
            result = self.ifc_extractor.extract(file_path, categories)
        else:
            result = self.dwg_extractor.extract(file_path)

        # Aggregate quantities by category
        quantities = {}
        for element in result.elements:
            cat = element.category.value
            if cat not in quantities:
                quantities[cat] = {
                    "count": 0,
                    "totals": {}
                }

            quantities[cat]["count"] += 1

            for qty_name, qty_value in element.quantities.items():
                if qty_name not in quantities[cat]["totals"]:
                    quantities[cat]["totals"][qty_name] = 0
                quantities[cat]["totals"][qty_name] += qty_value

        return {
            "file": file_path,
            "quantities": quantities,
            "summary": {
                "total_elements": result.total_elements,
                "categories": list(quantities.keys())
            }
        }

    def extract_schedule(
        self,
        file_path: str,
        category: ElementCategory,
        fields: List[str]
    ) -> List[Dict]:
        """Extract schedule data for specific category"""
        file_format = self._detect_format(file_path)

        if file_format == CADFormat.IFC:
            result = self.ifc_extractor.extract(file_path, [category])
        else:
            result = self.dwg_extractor.extract(file_path)

        schedule = []
        for element in result.elements:
            if element.category == category:
                row = {"id": element.id, "name": element.name, "type": element.type_name}

                for field in fields:
                    if field in element.properties:
                        row[field] = element.properties[field]
                    elif field in element.quantities:
                        row[field] = element.quantities[field]

                schedule.append(row)

        return schedule

    def export_to_json(
        self,
        result: CADExtractionResult,
        output_path: str
    ):
        """Export extraction result to JSON file"""
        output = self._format_output(result, "json")

        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

    def generate_report(self, result: CADExtractionResult) -> str:
        """Generate extraction report"""
        report = f"""
# CAD Extraction Report

**File:** {result.file_path}
**Format:** {result.file_format.value}
**Total Elements:** {result.total_elements}
**Extraction Time:** {result.extraction_time:.2f}s

## Elements by Category
"""
        for cat, count in result.categories.items():
            report += f"- **{cat.title()}:** {count}\n"

        if result.levels:
            report += "\n## Levels\n"
            for level in result.levels:
                report += f"- {level}\n"

        if result.layers:
            report += "\n## Layers\n"
            for layer in result.layers:
                report += f"- {layer.name}: {layer.element_count} elements\n"

        return report
```

## Common Use Cases

### Extract IFC Data

```python
converter = CADDataConverter()

# Convert IFC to structured data
data = converter.convert("building.ifc", output_format="json")

print(f"Total elements: {data['total_elements']}")
print(f"Categories: {data['categories']}")

# Access elements
for element in data['elements'][:5]:
    print(f"  {element['name']}: {element['type']}")
```

### Extract Quantities

```python
quantities = converter.extract_quantities(
    "building.ifc",
    categories=[ElementCategory.WALL, ElementCategory.FLOOR]
)

print(f"Wall count: {quantities['quantities']['wall']['count']}")
print(f"Total wall area: {quantities['quantities']['wall']['totals']['Area']}")
```

### Generate Schedule

```python
door_schedule = converter.extract_schedule(
    "building.ifc",
    category=ElementCategory.DOOR,
    fields=["Width", "Height", "FireRating", "IsExternal"]
)

for door in door_schedule:
    print(f"{door['name']}: {door.get('Width')}x{door.get('Height')}")
```

### Generate Report

```python
ifc_extractor = IFCExtractor()
result = ifc_extractor.extract("building.ifc")

report = converter.generate_report(result)
print(report)
```

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `CADDataConverter` | Main conversion engine |
| `IFCExtractor` | IFC file extraction |
| `DWGExtractor` | DWG/DXF extraction |
| `CADElement` | Extracted element data |
| `CADExtractionResult` | Complete extraction result |
| `ElementCategory` | BIM element categories |

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 2.4
- **Website**: https://datadrivenconstruction.io

## Next Steps

- Use [image-to-data](../image-to-data/SKILL.md) for image extraction
- Use [qto-report](../../Chapter-3.2/qto-report/SKILL.md) for quantity reports
- Use [bim-validation-pipeline](../../Chapter-4.3/bim-validation-pipeline/SKILL.md) for validation

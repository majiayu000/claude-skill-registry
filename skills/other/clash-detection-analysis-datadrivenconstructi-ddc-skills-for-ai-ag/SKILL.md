---
slug: "clash-detection-analysis"
display_name: "Clash Detection Analysis"
description: "Detect and analyze geometric clashes between BIM elements. Identify hard clashes, soft clashes, and workflow conflicts using spatial analysis and rule-based detection."
---

# Clash Detection Analysis

## Overview

This skill implements automated clash detection for BIM models. Identify conflicts between building elements before construction to prevent costly rework and delays.

**Types of Clashes:**
- **Hard Clash**: Physical intersection of elements
- **Soft Clash**: Clearance/tolerance violations
- **Workflow Clash**: Scheduling/sequencing conflicts

> "Обнаружение коллизий на этапе проектирования может сократить затраты на исправление ошибок до 10 раз по сравнению с исправлением на стройплощадке."

## Quick Start

```python
import ifcopenshell
import ifcopenshell.geom
import numpy as np
from itertools import combinations

# Open model
ifc = ifcopenshell.open("model.ifc")

# Get structural and MEP elements
structural = ifc.by_type("IfcColumn") + ifc.by_type("IfcBeam")
mep = ifc.by_type("IfcPipeSegment") + ifc.by_type("IfcDuctSegment")

# Simple bounding box clash check
settings = ifcopenshell.geom.settings()

def get_bbox(element):
    try:
        shape = ifcopenshell.geom.create_shape(settings, element)
        verts = np.array(shape.geometry.verts).reshape(-1, 3)
        return verts.min(axis=0), verts.max(axis=0)
    except:
        return None, None

def check_bbox_clash(bbox1, bbox2):
    min1, max1 = bbox1
    min2, max2 = bbox2
    if min1 is None or min2 is None:
        return False
    return np.all(max1 >= min2) and np.all(max2 >= min1)

# Find clashes
clashes = []
for s_elem in structural:
    for m_elem in mep:
        bbox1 = get_bbox(s_elem)
        bbox2 = get_bbox(m_elem)
        if check_bbox_clash(bbox1, bbox2):
            clashes.append({
                'element1': s_elem.GlobalId,
                'element2': m_elem.GlobalId,
                'type': 'Structure-MEP'
            })

print(f"Found {len(clashes)} potential clashes")
```

## Clash Detection Engine

### Core Detector Class

```python
import ifcopenshell
import ifcopenshell.geom
import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from itertools import combinations
from scipy.spatial import cKDTree

@dataclass
class Clash:
    element1_id: str
    element1_type: str
    element1_name: str
    element2_id: str
    element2_type: str
    element2_name: str
    clash_type: str
    distance: float
    location: Tuple[float, float, float]
    severity: str

class ClashDetector:
    """Detect clashes between BIM elements"""

    def __init__(self, ifc_path: str):
        self.model = ifcopenshell.open(ifc_path)
        self.settings = ifcopenshell.geom.settings()
        self.settings.set(self.settings.USE_WORLD_COORDS, True)

        self._geometry_cache = {}
        self.clashes: List[Clash] = []

    def _get_geometry(self, element):
        """Get or compute element geometry"""
        if element.GlobalId in self._geometry_cache:
            return self._geometry_cache[element.GlobalId]

        try:
            shape = ifcopenshell.geom.create_shape(self.settings, element)
            verts = np.array(shape.geometry.verts).reshape(-1, 3)
            faces = np.array(shape.geometry.faces).reshape(-1, 3)

            geom = {
                'vertices': verts,
                'faces': faces,
                'min': verts.min(axis=0),
                'max': verts.max(axis=0),
                'center': verts.mean(axis=0)
            }
            self._geometry_cache[element.GlobalId] = geom
            return geom
        except:
            return None

    def detect_hard_clashes(self, group1_types: List[str],
                            group2_types: List[str]) -> List[Clash]:
        """Detect hard clashes (physical intersections) between two groups"""
        group1 = []
        for ifc_type in group1_types:
            group1.extend(self.model.by_type(ifc_type))

        group2 = []
        for ifc_type in group2_types:
            group2.extend(self.model.by_type(ifc_type))

        clashes = []

        for elem1 in group1:
            geom1 = self._get_geometry(elem1)
            if geom1 is None:
                continue

            for elem2 in group2:
                if elem1.GlobalId == elem2.GlobalId:
                    continue

                geom2 = self._get_geometry(elem2)
                if geom2 is None:
                    continue

                # Bounding box check (fast filter)
                if not self._bbox_intersect(geom1, geom2):
                    continue

                # Detailed check
                intersection = self._check_intersection(geom1, geom2)
                if intersection['intersects']:
                    clash = Clash(
                        element1_id=elem1.GlobalId,
                        element1_type=elem1.is_a(),
                        element1_name=elem1.Name or '',
                        element2_id=elem2.GlobalId,
                        element2_type=elem2.is_a(),
                        element2_name=elem2.Name or '',
                        clash_type='Hard',
                        distance=intersection['distance'],
                        location=tuple(intersection['point']),
                        severity=self._classify_severity(intersection['distance'])
                    )
                    clashes.append(clash)

        self.clashes.extend(clashes)
        return clashes

    def detect_soft_clashes(self, group1_types: List[str],
                            group2_types: List[str],
                            clearance: float = 0.1) -> List[Clash]:
        """Detect soft clashes (clearance violations)"""
        group1 = []
        for ifc_type in group1_types:
            group1.extend(self.model.by_type(ifc_type))

        group2 = []
        for ifc_type in group2_types:
            group2.extend(self.model.by_type(ifc_type))

        clashes = []

        for elem1 in group1:
            geom1 = self._get_geometry(elem1)
            if geom1 is None:
                continue

            for elem2 in group2:
                if elem1.GlobalId == elem2.GlobalId:
                    continue

                geom2 = self._get_geometry(elem2)
                if geom2 is None:
                    continue

                # Check if within clearance distance
                distance = self._min_distance(geom1, geom2)

                if distance < clearance and distance > 0:
                    clash = Clash(
                        element1_id=elem1.GlobalId,
                        element1_type=elem1.is_a(),
                        element1_name=elem1.Name or '',
                        element2_id=elem2.GlobalId,
                        element2_type=elem2.is_a(),
                        element2_name=elem2.Name or '',
                        clash_type='Soft',
                        distance=distance,
                        location=tuple((geom1['center'] + geom2['center']) / 2),
                        severity='Medium' if distance < clearance/2 else 'Low'
                    )
                    clashes.append(clash)

        self.clashes.extend(clashes)
        return clashes

    def _bbox_intersect(self, geom1: Dict, geom2: Dict) -> bool:
        """Check if bounding boxes intersect"""
        return (np.all(geom1['max'] >= geom2['min']) and
                np.all(geom2['max'] >= geom1['min']))

    def _check_intersection(self, geom1: Dict, geom2: Dict) -> Dict:
        """Check for actual geometry intersection"""
        # Simplified check using closest points
        tree1 = cKDTree(geom1['vertices'])
        distances, _ = tree1.query(geom2['vertices'], k=1)

        min_dist = distances.min()

        if min_dist < 0.001:  # Intersection threshold
            intersection_idx = np.argmin(distances)
            return {
                'intersects': True,
                'distance': min_dist,
                'point': geom2['vertices'][intersection_idx]
            }

        return {'intersects': False, 'distance': min_dist, 'point': None}

    def _min_distance(self, geom1: Dict, geom2: Dict) -> float:
        """Calculate minimum distance between geometries"""
        tree1 = cKDTree(geom1['vertices'])
        distances, _ = tree1.query(geom2['vertices'], k=1)
        return distances.min()

    def _classify_severity(self, distance: float) -> str:
        """Classify clash severity"""
        if distance < 0.01:
            return 'Critical'
        elif distance < 0.05:
            return 'High'
        elif distance < 0.1:
            return 'Medium'
        else:
            return 'Low'

    def get_clash_report(self) -> pd.DataFrame:
        """Generate clash report as DataFrame"""
        if not self.clashes:
            return pd.DataFrame()

        return pd.DataFrame([
            {
                'Element1_ID': c.element1_id,
                'Element1_Type': c.element1_type,
                'Element1_Name': c.element1_name,
                'Element2_ID': c.element2_id,
                'Element2_Type': c.element2_type,
                'Element2_Name': c.element2_name,
                'Clash_Type': c.clash_type,
                'Distance_m': c.distance,
                'Location_X': c.location[0],
                'Location_Y': c.location[1],
                'Location_Z': c.location[2],
                'Severity': c.severity
            }
            for c in self.clashes
        ])

    def get_summary(self) -> Dict:
        """Get clash detection summary"""
        df = self.get_clash_report()
        if df.empty:
            return {'total': 0}

        return {
            'total': len(self.clashes),
            'by_type': df['Clash_Type'].value_counts().to_dict(),
            'by_severity': df['Severity'].value_counts().to_dict(),
            'critical_count': len(df[df['Severity'] == 'Critical']),
            'element_types_involved': df['Element1_Type'].unique().tolist() +
                                     df['Element2_Type'].unique().tolist()
        }
```

## Clash Sets Configuration

### Common Clash Test Sets

```python
# Define common clash test configurations
CLASH_SETS = {
    'structure_vs_mep': {
        'group1': ['IfcColumn', 'IfcBeam', 'IfcWall', 'IfcSlab'],
        'group2': ['IfcPipeSegment', 'IfcDuctSegment', 'IfcCableSegment'],
        'clearance': 0.05,
        'description': 'Structural elements vs MEP systems'
    },
    'piping_vs_hvac': {
        'group1': ['IfcPipeSegment', 'IfcPipeFitting'],
        'group2': ['IfcDuctSegment', 'IfcDuctFitting'],
        'clearance': 0.10,
        'description': 'Plumbing vs HVAC conflicts'
    },
    'doors_clearance': {
        'group1': ['IfcDoor'],
        'group2': ['IfcColumn', 'IfcWall'],
        'clearance': 0.90,  # Door swing clearance
        'description': 'Door opening clearances'
    },
    'electrical_vs_plumbing': {
        'group1': ['IfcCableSegment', 'IfcElectricDistributionBoard'],
        'group2': ['IfcPipeSegment', 'IfcSanitaryTerminal'],
        'clearance': 0.15,
        'description': 'Electrical safety clearance from water'
    },
    'ceiling_vs_mep': {
        'group1': ['IfcCovering'],
        'group2': ['IfcPipeSegment', 'IfcDuctSegment', 'IfcCableCarrierSegment'],
        'clearance': 0.05,
        'description': 'Ceiling clearance for MEP'
    }
}

def run_all_clash_tests(detector: ClashDetector, clash_sets: Dict = None) -> Dict:
    """Run all configured clash tests"""
    if clash_sets is None:
        clash_sets = CLASH_SETS

    results = {}

    for test_name, config in clash_sets.items():
        print(f"Running: {config['description']}...")

        # Hard clashes
        hard = detector.detect_hard_clashes(config['group1'], config['group2'])

        # Soft clashes
        soft = detector.detect_soft_clashes(
            config['group1'],
            config['group2'],
            config['clearance']
        )

        results[test_name] = {
            'description': config['description'],
            'hard_clashes': len(hard),
            'soft_clashes': len(soft),
            'total': len(hard) + len(soft)
        }

    return results
```

## Report Generation

### Export Clash Report

```python
def export_clash_report(detector: ClashDetector, output_path: str):
    """Export comprehensive clash report to Excel"""
    df = detector.get_clash_report()
    summary = detector.get_summary()

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Summary sheet
        summary_df = pd.DataFrame([{
            'Total Clashes': summary['total'],
            'Critical': summary.get('critical_count', 0),
            'Hard Clashes': summary['by_type'].get('Hard', 0),
            'Soft Clashes': summary['by_type'].get('Soft', 0)
        }])
        summary_df.to_excel(writer, sheet_name='Summary', index=False)

        # All clashes
        if not df.empty:
            df.to_excel(writer, sheet_name='All_Clashes', index=False)

            # By severity
            for severity in ['Critical', 'High', 'Medium', 'Low']:
                severity_df = df[df['Severity'] == severity]
                if not severity_df.empty:
                    severity_df.to_excel(writer, sheet_name=severity, index=False)

    return output_path

def generate_clash_html_report(detector: ClashDetector, output_path: str):
    """Generate HTML report with visualizations"""
    df = detector.get_clash_report()
    summary = detector.get_summary()

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Clash Detection Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .summary {{ background: #f5f5f5; padding: 20px; border-radius: 8px; }}
            .critical {{ background: #ffebee; }}
            .high {{ background: #fff3e0; }}
            table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background: #4CAF50; color: white; }}
        </style>
    </head>
    <body>
        <h1>Clash Detection Report</h1>

        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Total Clashes:</strong> {summary['total']}</p>
            <p><strong>Critical:</strong> {summary.get('critical_count', 0)}</p>
        </div>

        <h2>Clash Details</h2>
        {df.to_html(index=False) if not df.empty else '<p>No clashes found</p>'}
    </body>
    </html>
    """

    with open(output_path, 'w') as f:
        f.write(html)

    return output_path
```

## Quick Reference

| Clash Type | Description | Typical Clearance |
|------------|-------------|-------------------|
| Hard Clash | Physical intersection | 0 mm |
| Soft Clash | Clearance violation | 50-150 mm |
| Workflow | Schedule conflict | N/A |

| Severity | Distance | Action Required |
|----------|----------|-----------------|
| Critical | < 10 mm | Immediate redesign |
| High | 10-50 mm | Priority fix |
| Medium | 50-100 mm | Review needed |
| Low | > 100 mm | Monitor |

## Resources

- **IfcOpenShell**: https://ifcopenshell.org
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `4d-simulation` for time-based clash analysis
- See `bim-validation-pipeline` for validation workflows
- See `ifc-data-extraction` for element data

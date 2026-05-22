---
name: defect-detection-ai
description: "AI-powered construction defect detection using computer vision. Identify cracks, spalling, corrosion, and other defects in concrete, steel, and building components from images and video."
---

# AI Defect Detection

## Overview

This skill implements deep learning-based defect detection for construction quality control. Analyze images and video to automatically identify structural and surface defects, classify severity, and generate inspection reports.

**Detectable Defects:**
- Concrete: Cracks, spalling, honeycombing, efflorescence
- Steel: Corrosion, weld defects, deformation
- Masonry: Mortar deterioration, displacement
- Finishes: Surface defects, coating failures
- MEP: Insulation damage, pipe corrosion

## Quick Start

```python
import torch
import torch.nn as nn
from torchvision import transforms, models
from PIL import Image
from dataclasses import dataclass
from typing import List, Dict, Tuple
from enum import Enum

class DefectType(Enum):
    CRACK = "crack"
    SPALLING = "spalling"
    CORROSION = "corrosion"
    HONEYCOMBING = "honeycombing"
    EFFLORESCENCE = "efflorescence"
    DEFORMATION = "deformation"
    SURFACE_DAMAGE = "surface_damage"
    NO_DEFECT = "no_defect"

class SeverityLevel(Enum):
    MINOR = "minor"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"

@dataclass
class DefectDetection:
    defect_type: DefectType
    confidence: float
    severity: SeverityLevel
    bounding_box: Tuple[int, int, int, int]  # x1, y1, x2, y2
    area_ratio: float  # Defect area as ratio of image

# Simple classifier using pretrained model
class SimpleDefectClassifier:
    def __init__(self, num_classes: int = 8):
        self.model = models.resnet18(pretrained=True)
        self.model.fc = nn.Linear(self.model.fc.in_features, num_classes)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

        self.classes = list(DefectType)

    def predict(self, image_path: str) -> DefectDetection:
        """Classify defect in image"""
        image = Image.open(image_path).convert('RGB')
        input_tensor = self.transform(image).unsqueeze(0)

        with torch.no_grad():
            outputs = self.model(input_tensor)
            probs = torch.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probs, 1)

        defect_type = self.classes[predicted.item()]

        return DefectDetection(
            defect_type=defect_type,
            confidence=confidence.item(),
            severity=self._estimate_severity(confidence.item()),
            bounding_box=(0, 0, image.width, image.height),
            area_ratio=1.0
        )

    def _estimate_severity(self, confidence: float) -> SeverityLevel:
        if confidence > 0.9:
            return SeverityLevel.CRITICAL
        elif confidence > 0.7:
            return SeverityLevel.SEVERE
        elif confidence > 0.5:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR

# Usage
classifier = SimpleDefectClassifier()
# result = classifier.predict("concrete_image.jpg")
# print(f"Defect: {result.defect_type.value}, Confidence: {result.confidence:.2%}")
```

## Comprehensive Defect Detection System

### Object Detection Model

```python
import torch
import torch.nn as nn
from torchvision import transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn
from PIL import Image
import numpy as np
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional
from datetime import datetime
import json

@dataclass
class BoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int

    @property
    def width(self) -> int:
        return self.x2 - self.x1

    @property
    def height(self) -> int:
        return self.y2 - self.y1

    @property
    def area(self) -> int:
        return self.width * self.height

    @property
    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2) // 2, (self.y1 + self.y2) // 2)

@dataclass
class DetectedDefect:
    defect_id: str
    defect_type: DefectType
    confidence: float
    severity: SeverityLevel
    bounding_box: BoundingBox
    area_sqm: Optional[float] = None
    dimensions_mm: Optional[Tuple[float, float]] = None
    metadata: Dict = field(default_factory=dict)

@dataclass
class InspectionResult:
    inspection_id: str
    image_path: str
    timestamp: datetime
    location: str
    element_type: str
    defects: List[DetectedDefect]
    overall_condition: str
    recommended_actions: List[str]

class DefectDetectionModel:
    """Deep learning defect detection with object detection"""

    DEFECT_CLASSES = {
        1: DefectType.CRACK,
        2: DefectType.SPALLING,
        3: DefectType.CORROSION,
        4: DefectType.HONEYCOMBING,
        5: DefectType.EFFLORESCENCE,
        6: DefectType.DEFORMATION,
        7: DefectType.SURFACE_DAMAGE
    }

    def __init__(self, model_path: str = None, device: str = 'cpu'):
        self.device = torch.device(device)

        # Initialize Faster R-CNN
        self.model = fasterrcnn_resnet50_fpn(pretrained=True)

        # Modify for our classes
        num_classes = len(self.DEFECT_CLASSES) + 1  # +1 for background
        in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        self.model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)

        if model_path:
            self.model.load_state_dict(torch.load(model_path, map_location=self.device))

        self.model.to(self.device)
        self.model.eval()

        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])

    def detect(self, image_path: str, confidence_threshold: float = 0.5,
               pixels_per_mm: float = None) -> List[DetectedDefect]:
        """Detect defects in image"""
        image = Image.open(image_path).convert('RGB')
        image_tensor = self.transform(image).to(self.device)

        with torch.no_grad():
            predictions = self.model([image_tensor])

        pred = predictions[0]
        defects = []

        for i in range(len(pred['boxes'])):
            score = pred['scores'][i].item()

            if score < confidence_threshold:
                continue

            label = pred['labels'][i].item()
            box = pred['boxes'][i].cpu().numpy()

            defect_type = self.DEFECT_CLASSES.get(label, DefectType.SURFACE_DAMAGE)

            bbox = BoundingBox(
                x1=int(box[0]),
                y1=int(box[1]),
                x2=int(box[2]),
                y2=int(box[3])
            )

            # Calculate dimensions if scale provided
            dimensions_mm = None
            if pixels_per_mm:
                width_mm = bbox.width / pixels_per_mm
                height_mm = bbox.height / pixels_per_mm
                dimensions_mm = (width_mm, height_mm)

            severity = self._classify_severity(defect_type, bbox, image.size)

            defects.append(DetectedDefect(
                defect_id=f"DEF-{i:04d}",
                defect_type=defect_type,
                confidence=score,
                severity=severity,
                bounding_box=bbox,
                dimensions_mm=dimensions_mm
            ))

        return defects

    def _classify_severity(self, defect_type: DefectType,
                          bbox: BoundingBox,
                          image_size: Tuple[int, int]) -> SeverityLevel:
        """Classify defect severity based on type and size"""
        image_area = image_size[0] * image_size[1]
        defect_ratio = bbox.area / image_area

        # Severity thresholds by defect type
        thresholds = {
            DefectType.CRACK: {'critical': 0.1, 'severe': 0.05, 'moderate': 0.02},
            DefectType.SPALLING: {'critical': 0.15, 'severe': 0.08, 'moderate': 0.03},
            DefectType.CORROSION: {'critical': 0.2, 'severe': 0.1, 'moderate': 0.05},
            DefectType.HONEYCOMBING: {'critical': 0.1, 'severe': 0.05, 'moderate': 0.02},
            DefectType.DEFORMATION: {'critical': 0.05, 'severe': 0.02, 'moderate': 0.01}
        }

        t = thresholds.get(defect_type, {'critical': 0.15, 'severe': 0.08, 'moderate': 0.03})

        if defect_ratio >= t['critical']:
            return SeverityLevel.CRITICAL
        elif defect_ratio >= t['severe']:
            return SeverityLevel.SEVERE
        elif defect_ratio >= t['moderate']:
            return SeverityLevel.MODERATE
        else:
            return SeverityLevel.MINOR


class FastRCNNPredictor(nn.Module):
    """Custom predictor for Faster R-CNN"""

    def __init__(self, in_channels, num_classes):
        super().__init__()
        self.cls_score = nn.Linear(in_channels, num_classes)
        self.bbox_pred = nn.Linear(in_channels, num_classes * 4)

    def forward(self, x):
        scores = self.cls_score(x)
        bbox_deltas = self.bbox_pred(x)
        return scores, bbox_deltas
```

### Crack Analysis System

```python
import cv2
import numpy as np
from typing import List, Tuple, Dict

class CrackAnalyzer:
    """Specialized crack detection and measurement"""

    def __init__(self):
        self.min_crack_length = 10  # pixels
        self.min_crack_width = 2  # pixels

    def detect_cracks(self, image_path: str,
                      pixels_per_mm: float = 1.0) -> List[Dict]:
        """Detect and measure cracks in image"""
        # Load image
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        # Edge detection
        edges = cv2.Canny(enhanced, 50, 150)

        # Morphological operations to connect crack segments
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(edges, kernel, iterations=1)
        closed = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)

        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        cracks = []
        for i, contour in enumerate(contours):
            # Filter by length
            arc_length = cv2.arcLength(contour, False)
            if arc_length < self.min_crack_length:
                continue

            # Get bounding box
            x, y, w, h = cv2.boundingRect(contour)

            # Calculate crack properties
            length_px = arc_length
            width_px = self._estimate_crack_width(gray, contour)

            # Convert to mm
            length_mm = length_px / pixels_per_mm
            width_mm = width_px / pixels_per_mm

            # Classify crack
            crack_type = self._classify_crack(length_mm, width_mm, contour)

            cracks.append({
                'crack_id': f"CRACK-{i:04d}",
                'type': crack_type,
                'length_mm': length_mm,
                'width_mm': width_mm,
                'bounding_box': (x, y, x + w, y + h),
                'contour': contour.tolist(),
                'severity': self._get_crack_severity(width_mm, length_mm),
                'orientation': self._get_crack_orientation(contour)
            })

        return cracks

    def _estimate_crack_width(self, gray_image: np.ndarray,
                             contour: np.ndarray) -> float:
        """Estimate average crack width"""
        # Create mask for contour
        mask = np.zeros(gray_image.shape, dtype=np.uint8)
        cv2.drawContours(mask, [contour], -1, 255, 1)

        # Distance transform
        dist = cv2.distanceTransform(mask, cv2.DIST_L2, 5)

        # Get average distance (half-width)
        nonzero = dist[dist > 0]
        if len(nonzero) > 0:
            return np.mean(nonzero) * 2
        return 0

    def _classify_crack(self, length_mm: float, width_mm: float,
                       contour: np.ndarray) -> str:
        """Classify crack type"""
        # Fit line to get orientation
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        angle = np.arctan2(vy, vx) * 180 / np.pi

        if abs(angle) < 20 or abs(angle) > 160:
            orientation = "horizontal"
        elif 70 < abs(angle) < 110:
            orientation = "vertical"
        else:
            orientation = "diagonal"

        # Check for pattern (simplified)
        if width_mm > 3:
            return "structural_crack"
        elif orientation == "horizontal" and length_mm > 100:
            return "settlement_crack"
        elif orientation == "diagonal":
            return "shear_crack"
        else:
            return "shrinkage_crack"

    def _get_crack_severity(self, width_mm: float, length_mm: float) -> str:
        """Determine crack severity based on dimensions"""
        # Based on ACI 224R guidelines
        if width_mm > 1.0:
            return "critical"
        elif width_mm > 0.4:
            return "severe"
        elif width_mm > 0.2:
            return "moderate"
        else:
            return "minor"

    def _get_crack_orientation(self, contour: np.ndarray) -> float:
        """Get crack orientation angle"""
        [vx, vy, x, y] = cv2.fitLine(contour, cv2.DIST_L2, 0, 0.01, 0.01)
        return float(np.arctan2(vy, vx) * 180 / np.pi)

    def generate_crack_report(self, cracks: List[Dict]) -> Dict:
        """Generate summary report of detected cracks"""
        if not cracks:
            return {'message': 'No cracks detected'}

        total_length = sum(c['length_mm'] for c in cracks)
        max_width = max(c['width_mm'] for c in cracks)
        severity_counts = {}

        for c in cracks:
            sev = c['severity']
            severity_counts[sev] = severity_counts.get(sev, 0) + 1

        return {
            'total_cracks': len(cracks),
            'total_length_mm': total_length,
            'max_width_mm': max_width,
            'avg_width_mm': sum(c['width_mm'] for c in cracks) / len(cracks),
            'by_severity': severity_counts,
            'by_type': self._group_by_type(cracks),
            'most_severe': max(cracks, key=lambda c: c['width_mm'])
        }

    def _group_by_type(self, cracks: List[Dict]) -> Dict:
        """Group cracks by type"""
        grouped = {}
        for c in cracks:
            t = c['type']
            if t not in grouped:
                grouped[t] = []
            grouped[t].append(c['crack_id'])
        return grouped
```

### Inspection Report Generator

```python
from datetime import datetime
import pandas as pd

class DefectInspectionSystem:
    """Complete defect inspection and reporting system"""

    def __init__(self, detection_model: DefectDetectionModel):
        self.model = detection_model
        self.crack_analyzer = CrackAnalyzer()
        self.inspections: List[InspectionResult] = []

    def perform_inspection(self, image_path: str,
                          location: str,
                          element_type: str,
                          pixels_per_mm: float = None) -> InspectionResult:
        """Perform complete inspection on image"""
        # Detect defects
        defects = self.model.detect(image_path, pixels_per_mm=pixels_per_mm)

        # Additional crack analysis for concrete
        if element_type.lower() in ['concrete', 'slab', 'wall', 'column', 'beam']:
            cracks = self.crack_analyzer.detect_cracks(image_path, pixels_per_mm or 1.0)

            # Add detailed crack info to relevant defects
            for defect in defects:
                if defect.defect_type == DefectType.CRACK:
                    for crack in cracks:
                        # Check if crack overlaps with defect bbox
                        if self._boxes_overlap(defect.bounding_box, crack['bounding_box']):
                            defect.metadata['crack_details'] = crack
                            break

        # Determine overall condition
        overall_condition = self._assess_overall_condition(defects)

        # Generate recommendations
        recommendations = self._generate_recommendations(defects, element_type)

        result = InspectionResult(
            inspection_id=f"INS-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            image_path=image_path,
            timestamp=datetime.now(),
            location=location,
            element_type=element_type,
            defects=defects,
            overall_condition=overall_condition,
            recommended_actions=recommendations
        )

        self.inspections.append(result)
        return result

    def _boxes_overlap(self, box1: BoundingBox, box2: Tuple) -> bool:
        """Check if two bounding boxes overlap"""
        x1_1, y1_1, x2_1, y2_1 = box1.x1, box1.y1, box1.x2, box1.y2
        x1_2, y1_2, x2_2, y2_2 = box2

        return not (x2_1 < x1_2 or x2_2 < x1_1 or y2_1 < y1_2 or y2_2 < y1_1)

    def _assess_overall_condition(self, defects: List[DetectedDefect]) -> str:
        """Assess overall structural condition"""
        if not defects:
            return "Good"

        severity_scores = {
            SeverityLevel.MINOR: 1,
            SeverityLevel.MODERATE: 2,
            SeverityLevel.SEVERE: 3,
            SeverityLevel.CRITICAL: 4
        }

        max_severity = max(severity_scores[d.severity] for d in defects)
        total_defects = len(defects)

        if max_severity >= 4 or total_defects > 10:
            return "Critical - Immediate attention required"
        elif max_severity >= 3 or total_defects > 5:
            return "Poor - Repairs needed"
        elif max_severity >= 2 or total_defects > 2:
            return "Fair - Monitor and plan repairs"
        else:
            return "Good - Minor issues only"

    def _generate_recommendations(self, defects: List[DetectedDefect],
                                 element_type: str) -> List[str]:
        """Generate repair recommendations"""
        recommendations = []

        # Group defects by type
        defect_groups = {}
        for d in defects:
            t = d.defect_type
            if t not in defect_groups:
                defect_groups[t] = []
            defect_groups[t].append(d)

        # Generate recommendations by defect type
        for defect_type, group in defect_groups.items():
            max_severity = max(d.severity for d in group)

            if defect_type == DefectType.CRACK:
                if max_severity in [SeverityLevel.CRITICAL, SeverityLevel.SEVERE]:
                    recommendations.append(
                        f"Structural engineer assessment required for {len(group)} crack(s). "
                        f"Consider epoxy injection or structural repair."
                    )
                else:
                    recommendations.append(
                        f"Seal {len(group)} minor crack(s) with appropriate sealant."
                    )

            elif defect_type == DefectType.SPALLING:
                recommendations.append(
                    f"Remove loose concrete and apply repair mortar to {len(group)} spalling area(s). "
                    f"Check reinforcement for corrosion."
                )

            elif defect_type == DefectType.CORROSION:
                recommendations.append(
                    f"Treat {len(group)} corrosion area(s). Clean rust, apply rust converter, "
                    f"and protective coating."
                )

            elif defect_type == DefectType.HONEYCOMBING:
                recommendations.append(
                    f"Fill {len(group)} honeycomb area(s) with non-shrink grout. "
                    f"Investigate concrete placement procedures."
                )

            elif defect_type == DefectType.EFFLORESCENCE:
                recommendations.append(
                    f"Clean efflorescence from {len(group)} area(s). "
                    f"Investigate and address moisture source."
                )

        if not recommendations:
            recommendations.append("Continue regular inspection schedule.")

        return recommendations

    def export_inspection_report(self, inspection_id: str,
                                output_path: str) -> str:
        """Export inspection report to Excel"""
        inspection = next(
            (i for i in self.inspections if i.inspection_id == inspection_id),
            None
        )

        if not inspection:
            raise ValueError(f"Inspection {inspection_id} not found")

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary
            summary = pd.DataFrame([{
                'Inspection ID': inspection.inspection_id,
                'Date': inspection.timestamp.strftime('%Y-%m-%d %H:%M'),
                'Location': inspection.location,
                'Element Type': inspection.element_type,
                'Overall Condition': inspection.overall_condition,
                'Total Defects': len(inspection.defects),
                'Image': inspection.image_path
            }])
            summary.to_excel(writer, sheet_name='Summary', index=False)

            # Defects
            if inspection.defects:
                defect_data = [{
                    'Defect ID': d.defect_id,
                    'Type': d.defect_type.value,
                    'Severity': d.severity.value,
                    'Confidence': f"{d.confidence:.1%}",
                    'Location (x,y)': f"({d.bounding_box.x1}, {d.bounding_box.y1})",
                    'Size (w×h)': f"{d.bounding_box.width}×{d.bounding_box.height}",
                    'Dimensions (mm)': d.dimensions_mm if d.dimensions_mm else 'N/A'
                } for d in inspection.defects]
                pd.DataFrame(defect_data).to_excel(writer, sheet_name='Defects', index=False)

            # Recommendations
            rec_data = [{'#': i+1, 'Recommendation': r}
                       for i, r in enumerate(inspection.recommended_actions)]
            pd.DataFrame(rec_data).to_excel(writer, sheet_name='Recommendations', index=False)

        return output_path

    def get_defect_statistics(self, start_date: datetime = None,
                             end_date: datetime = None) -> Dict:
        """Get defect statistics across inspections"""
        filtered = self.inspections
        if start_date:
            filtered = [i for i in filtered if i.timestamp >= start_date]
        if end_date:
            filtered = [i for i in filtered if i.timestamp <= end_date]

        all_defects = []
        for inspection in filtered:
            all_defects.extend(inspection.defects)

        if not all_defects:
            return {'message': 'No defects found in period'}

        # Statistics
        by_type = {}
        by_severity = {}

        for d in all_defects:
            t = d.defect_type.value
            s = d.severity.value

            by_type[t] = by_type.get(t, 0) + 1
            by_severity[s] = by_severity.get(s, 0) + 1

        return {
            'period': {
                'start': start_date.isoformat() if start_date else 'all',
                'end': end_date.isoformat() if end_date else 'all'
            },
            'total_inspections': len(filtered),
            'total_defects': len(all_defects),
            'by_type': by_type,
            'by_severity': by_severity,
            'avg_defects_per_inspection': len(all_defects) / len(filtered) if filtered else 0
        }
```

## Model Training

```python
import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
import os
from PIL import Image

class DefectDataset(Dataset):
    """Dataset for training defect detection model"""

    def __init__(self, root_dir: str, annotations_file: str, transform=None):
        self.root_dir = root_dir
        self.annotations = self._load_annotations(annotations_file)
        self.transform = transform or transforms.Compose([
            transforms.Resize((800, 800)),
            transforms.ToTensor()
        ])

    def _load_annotations(self, path: str) -> List[Dict]:
        """Load COCO-format annotations"""
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        return data['annotations']

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        ann = self.annotations[idx]
        image_path = os.path.join(self.root_dir, ann['image_file'])
        image = Image.open(image_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        # Prepare target
        boxes = torch.tensor(ann['boxes'], dtype=torch.float32)
        labels = torch.tensor(ann['labels'], dtype=torch.int64)

        target = {
            'boxes': boxes,
            'labels': labels
        }

        return image, target


def train_defect_model(train_dataset: DefectDataset,
                       val_dataset: DefectDataset,
                       num_epochs: int = 10,
                       batch_size: int = 4,
                       learning_rate: float = 0.005):
    """Train defect detection model"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    # Initialize model
    model = fasterrcnn_resnet50_fpn(pretrained=True)
    num_classes = 8  # 7 defect types + background
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    model.to(device)

    # Data loaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True,
                              collate_fn=lambda x: tuple(zip(*x)))
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False,
                           collate_fn=lambda x: tuple(zip(*x)))

    # Optimizer
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate,
                                momentum=0.9, weight_decay=0.0005)

    # Training loop
    for epoch in range(num_epochs):
        model.train()
        total_loss = 0

        for images, targets in train_loader:
            images = [img.to(device) for img in images]
            targets = [{k: v.to(device) for k, v in t.items()} for t in targets]

            loss_dict = model(images, targets)
            losses = sum(loss for loss in loss_dict.values())

            optimizer.zero_grad()
            losses.backward()
            optimizer.step()

            total_loss += losses.item()

        avg_loss = total_loss / len(train_loader)
        print(f"Epoch {epoch+1}/{num_epochs}, Loss: {avg_loss:.4f}")

    return model
```

## Quick Reference

| Defect Type | Detection Method | Typical Severity |
|-------------|------------------|------------------|
| Crack | Edge detection + CNN | Varies by width |
| Spalling | Object detection | Moderate-Severe |
| Corrosion | Color + texture analysis | Moderate-Critical |
| Honeycombing | Object detection | Severe |
| Efflorescence | Color analysis | Minor-Moderate |

## ACI 224R Crack Width Guidelines

| Width (mm) | Condition | Exposure |
|------------|-----------|----------|
| < 0.1 | Acceptable | Any |
| 0.1 - 0.2 | Acceptable | Dry |
| 0.2 - 0.4 | Repair recommended | Humid |
| > 0.4 | Repair required | Any |
| > 1.0 | Structural concern | Any |

## Resources

- **PyTorch**: https://pytorch.org
- **OpenCV**: https://opencv.org
- **ACI 224R**: Crack control in concrete
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `progress-monitoring-cv` for construction progress analysis
- See `safety-compliance-checker` for safety defect integration
- See `bim-validation-pipeline` for model-based quality control

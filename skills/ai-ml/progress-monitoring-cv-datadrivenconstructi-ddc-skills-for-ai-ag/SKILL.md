---
slug: "progress-monitoring-cv"
display_name: "Progress Monitoring Cv"
description: "Monitor construction progress using computer vision. Analyze site photos and drone imagery to track work completion, detect safety issues, and compare against BIM models."
---

# Progress Monitoring with Computer Vision

## Overview

This skill implements computer vision for construction progress monitoring. Analyze site images automatically to track completion, detect hazards, and compare physical progress against planned work.

**Applications:**
- Progress percentage estimation
- Safety compliance detection (PPE, barriers)
- As-built vs BIM comparison
- Material and equipment tracking
- Quality defect detection

## Quick Start

```python
import cv2
import numpy as np
from PIL import Image
import torch
from torchvision import models, transforms

# Load pre-trained model for construction scene analysis
model = models.resnet50(pretrained=True)
model.eval()

# Preprocess image
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                        std=[0.229, 0.224, 0.225])
])

# Load site photo
img = Image.open("site_photo.jpg")
input_tensor = transform(img).unsqueeze(0)

# Analyze
with torch.no_grad():
    output = model(input_tensor)

print("Image analyzed successfully")
```

## Progress Detection System

### Core Progress Analyzer

```python
import cv2
import numpy as np
from PIL import Image
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import torch
from torchvision import models, transforms
from torchvision.models.detection import fasterrcnn_resnet50_fpn

class ConstructionPhase(Enum):
    EXCAVATION = "excavation"
    FOUNDATION = "foundation"
    STRUCTURE = "structure"
    ENCLOSURE = "enclosure"
    MEP_ROUGH = "mep_rough"
    FINISHES = "finishes"
    COMPLETE = "complete"

@dataclass
class ProgressReport:
    timestamp: str
    image_path: str
    detected_phase: ConstructionPhase
    estimated_progress: float
    detected_elements: List[Dict]
    safety_observations: List[Dict]
    quality_issues: List[Dict]
    comparison_to_plan: Optional[float]

class ConstructionProgressAnalyzer:
    """Analyze construction progress from images"""

    def __init__(self, use_gpu: bool = True):
        self.device = torch.device('cuda' if use_gpu and torch.cuda.is_available() else 'cpu')

        # Load detection model
        self.detector = fasterrcnn_resnet50_fpn(pretrained=True)
        self.detector.to(self.device)
        self.detector.eval()

        # Image transform
        self.transform = transforms.Compose([
            transforms.ToTensor()
        ])

        # Construction element labels (would need fine-tuned model in production)
        self.construction_labels = {
            'column': ['column', 'pillar', 'post'],
            'beam': ['beam', 'girder'],
            'slab': ['floor', 'slab', 'deck'],
            'wall': ['wall', 'partition'],
            'scaffold': ['scaffold', 'scaffolding'],
            'crane': ['crane', 'tower crane'],
            'equipment': ['excavator', 'loader', 'truck'],
            'worker': ['person', 'worker']
        }

    def analyze_image(self, image_path: str) -> ProgressReport:
        """Analyze a single construction site image"""
        # Load image
        img = Image.open(image_path).convert('RGB')
        img_tensor = self.transform(img).to(self.device)

        # Run detection
        with torch.no_grad():
            predictions = self.detector([img_tensor])

        # Process detections
        detected_elements = self._process_detections(predictions[0])

        # Estimate phase and progress
        phase = self._estimate_phase(detected_elements, img)
        progress = self._estimate_progress(phase, detected_elements)

        # Safety analysis
        safety_obs = self._analyze_safety(img, detected_elements)

        # Quality check (simplified)
        quality_issues = self._check_quality(img)

        return ProgressReport(
            timestamp=self._get_timestamp(),
            image_path=image_path,
            detected_phase=phase,
            estimated_progress=progress,
            detected_elements=detected_elements,
            safety_observations=safety_obs,
            quality_issues=quality_issues,
            comparison_to_plan=None
        )

    def _process_detections(self, predictions: Dict) -> List[Dict]:
        """Process model predictions into detected elements"""
        elements = []

        boxes = predictions['boxes'].cpu().numpy()
        labels = predictions['labels'].cpu().numpy()
        scores = predictions['scores'].cpu().numpy()

        for box, label, score in zip(boxes, labels, scores):
            if score > 0.5:  # Confidence threshold
                elements.append({
                    'box': box.tolist(),
                    'label': label,
                    'score': float(score),
                    'area': (box[2] - box[0]) * (box[3] - box[1])
                })

        return elements

    def _estimate_phase(self, elements: List[Dict], img: Image) -> ConstructionPhase:
        """Estimate construction phase from detected elements"""
        # Convert to numpy for color analysis
        img_array = np.array(img)

        # Color-based phase estimation (simplified)
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        # Brown/earth tones indicate excavation
        earth_mask = cv2.inRange(hsv, (10, 50, 50), (30, 255, 255))
        earth_ratio = np.sum(earth_mask > 0) / earth_mask.size

        # Gray tones indicate concrete
        gray_mask = cv2.inRange(hsv, (0, 0, 50), (180, 50, 200))
        gray_ratio = np.sum(gray_mask > 0) / gray_mask.size

        # Steel colors
        steel_mask = cv2.inRange(hsv, (0, 0, 100), (180, 30, 255))
        steel_ratio = np.sum(steel_mask > 0) / steel_mask.size

        # Simple phase logic
        if earth_ratio > 0.3:
            return ConstructionPhase.EXCAVATION
        elif gray_ratio > 0.2 and steel_ratio < 0.1:
            return ConstructionPhase.FOUNDATION
        elif steel_ratio > 0.1:
            return ConstructionPhase.STRUCTURE
        else:
            return ConstructionPhase.ENCLOSURE

    def _estimate_progress(self, phase: ConstructionPhase,
                          elements: List[Dict]) -> float:
        """Estimate progress percentage within phase"""
        phase_base_progress = {
            ConstructionPhase.EXCAVATION: 5,
            ConstructionPhase.FOUNDATION: 15,
            ConstructionPhase.STRUCTURE: 35,
            ConstructionPhase.ENCLOSURE: 60,
            ConstructionPhase.MEP_ROUGH: 75,
            ConstructionPhase.FINISHES: 90,
            ConstructionPhase.COMPLETE: 100
        }

        base = phase_base_progress.get(phase, 0)

        # Adjust based on detected elements
        element_count = len(elements)
        adjustment = min(element_count * 0.5, 10)

        return min(base + adjustment, 100)

    def _analyze_safety(self, img: Image, elements: List[Dict]) -> List[Dict]:
        """Analyze safety compliance"""
        observations = []
        img_array = np.array(img)

        # Check for safety vest colors (orange, yellow, green)
        hsv = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        # Orange vest detection
        orange_mask = cv2.inRange(hsv, (10, 100, 100), (25, 255, 255))
        orange_pixels = np.sum(orange_mask > 0)

        # Yellow vest detection
        yellow_mask = cv2.inRange(hsv, (25, 100, 100), (35, 255, 255))
        yellow_pixels = np.sum(yellow_mask > 0)

        if orange_pixels + yellow_pixels < 100:  # Threshold
            observations.append({
                'type': 'PPE_VISIBILITY',
                'severity': 'Medium',
                'message': 'Limited high-visibility clothing detected'
            })

        # Check for workers detected
        worker_count = sum(1 for e in elements if e.get('label') == 1)
        if worker_count > 0:
            observations.append({
                'type': 'WORKER_COUNT',
                'severity': 'Info',
                'message': f'{worker_count} workers detected on site'
            })

        return observations

    def _check_quality(self, img: Image) -> List[Dict]:
        """Check for visible quality issues"""
        issues = []
        img_array = np.array(img)

        # Edge detection for irregularities
        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # High edge density might indicate messy work or issues
        edge_density = np.sum(edges > 0) / edges.size

        if edge_density > 0.3:
            issues.append({
                'type': 'VISUAL_COMPLEXITY',
                'severity': 'Low',
                'message': 'High visual complexity - manual review recommended'
            })

        return issues

    def _get_timestamp(self) -> str:
        from datetime import datetime
        return datetime.now().isoformat()

    def compare_to_bim(self, image_path: str, bim_render_path: str) -> float:
        """Compare site photo to BIM rendering"""
        site_img = cv2.imread(image_path)
        bim_img = cv2.imread(bim_render_path)

        # Resize to same dimensions
        target_size = (800, 600)
        site_img = cv2.resize(site_img, target_size)
        bim_img = cv2.resize(bim_img, target_size)

        # Convert to grayscale
        site_gray = cv2.cvtColor(site_img, cv2.COLOR_BGR2GRAY)
        bim_gray = cv2.cvtColor(bim_img, cv2.COLOR_BGR2GRAY)

        # Calculate structural similarity
        from skimage.metrics import structural_similarity
        similarity, _ = structural_similarity(site_gray, bim_gray, full=True)

        return similarity

    def batch_analyze(self, image_paths: List[str]) -> List[ProgressReport]:
        """Analyze multiple images"""
        return [self.analyze_image(path) for path in image_paths]
```

## Time-Lapse Analysis

```python
class TimeLapseAnalyzer:
    """Analyze construction progress over time from image series"""

    def __init__(self, analyzer: ConstructionProgressAnalyzer):
        self.analyzer = analyzer
        self.reports: List[ProgressReport] = []

    def add_image(self, image_path: str, date: str):
        """Add image to time series"""
        report = self.analyzer.analyze_image(image_path)
        report.timestamp = date
        self.reports.append(report)

    def get_progress_curve(self) -> pd.DataFrame:
        """Generate progress curve from analyzed images"""
        data = [{
            'date': r.timestamp,
            'phase': r.detected_phase.value,
            'progress': r.estimated_progress,
            'element_count': len(r.detected_elements)
        } for r in self.reports]

        return pd.DataFrame(data).sort_values('date')

    def detect_delays(self, planned_progress: pd.DataFrame) -> List[Dict]:
        """Compare actual vs planned progress"""
        actual = self.get_progress_curve()
        delays = []

        for _, row in actual.iterrows():
            planned_row = planned_progress[
                planned_progress['date'] == row['date']
            ]
            if not planned_row.empty:
                planned_pct = planned_row.iloc[0]['progress']
                actual_pct = row['progress']

                if actual_pct < planned_pct - 5:  # 5% tolerance
                    delays.append({
                        'date': row['date'],
                        'planned': planned_pct,
                        'actual': actual_pct,
                        'delay_pct': planned_pct - actual_pct
                    })

        return delays

    def generate_report(self, output_path: str):
        """Generate progress monitoring report"""
        progress_df = self.get_progress_curve()

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            progress_df.to_excel(writer, sheet_name='Progress', index=False)

            # Safety observations
            safety_data = []
            for r in self.reports:
                for obs in r.safety_observations:
                    safety_data.append({
                        'Date': r.timestamp,
                        'Type': obs['type'],
                        'Severity': obs['severity'],
                        'Message': obs['message']
                    })
            if safety_data:
                pd.DataFrame(safety_data).to_excel(
                    writer, sheet_name='Safety', index=False
                )

        return output_path
```

## Quick Reference

| Analysis Type | Method | Output |
|--------------|--------|--------|
| Phase Detection | Color analysis + Object detection | Construction phase |
| Progress % | Element counting + Phase base | Completion percentage |
| Safety Check | Color detection (PPE) + Worker count | Safety observations |
| Quality Check | Edge detection + Anomaly detection | Quality issues |
| BIM Comparison | Structural similarity | Similarity score |

## Resources

- **OpenCV**: https://opencv.org
- **PyTorch**: https://pytorch.org
- **YOLO**: https://ultralytics.com/yolov8
- **DDC Website**: https://datadrivenconstruction.io

## Next Steps

- See `4d-simulation` for schedule comparison
- See `data-visualization` for progress dashboards
- See `risk-assessment-ml` for delay prediction

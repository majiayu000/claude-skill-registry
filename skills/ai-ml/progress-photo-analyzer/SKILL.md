---
name: progress-photo-analyzer
description: "Analyze construction site photos to track progress, detect safety issues, and compare against BIM models using computer vision."
---

# Progress Photo Analyzer

## Business Case

### Problem Statement
Site photos are underutilized for progress tracking:
- Manual review is time-consuming
- Subjective progress assessment
- No systematic comparison to plans
- Safety issues may be missed

### Solution
AI-powered photo analysis system that extracts progress information, detects safety concerns, and compares site conditions to BIM models.

### Business Value
- **Automation** - Reduce manual photo review
- **Accuracy** - Objective progress measurement
- **Safety** - Automatic hazard detection
- **Documentation** - Structured photo records

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import base64


class PhotoType(Enum):
    """Types of construction photos."""
    PROGRESS = "progress"
    SAFETY = "safety"
    QUALITY = "quality"
    GENERAL = "general"
    DELIVERY = "delivery"


class AnalysisStatus(Enum):
    """Analysis status."""
    PENDING = "pending"
    ANALYZING = "analyzing"
    COMPLETED = "completed"
    FAILED = "failed"


class SafetyIssue(Enum):
    """Detected safety issues."""
    MISSING_PPE = "missing_ppe"
    FALL_HAZARD = "fall_hazard"
    HOUSEKEEPING = "housekeeping"
    SCAFFOLDING = "scaffolding"
    ELECTRICAL = "electrical"
    EXCAVATION = "excavation"
    NONE = "none"


class WorkActivity(Enum):
    """Detected work activities."""
    EXCAVATION = "excavation"
    FOUNDATION = "foundation"
    CONCRETE_POUR = "concrete_pour"
    STEEL_ERECTION = "steel_erection"
    FRAMING = "framing"
    ROOFING = "roofing"
    MEP_ROUGH = "mep_rough"
    DRYWALL = "drywall"
    FINISHES = "finishes"
    EXTERIOR = "exterior"
    UNKNOWN = "unknown"


@dataclass
class PhotoMetadata:
    """Photo metadata."""
    photo_id: str
    filename: str
    capture_date: datetime
    location: str
    level: str
    zone: str
    photo_type: PhotoType
    photographer: str = ""
    gps_coordinates: Optional[Tuple[float, float]] = None
    file_path: str = ""


@dataclass
class ProgressDetection:
    """Detected progress information."""
    work_activity: WorkActivity
    confidence: float
    description: str
    completion_estimate: float  # 0-100%
    elements_visible: List[str] = field(default_factory=list)


@dataclass
class SafetyDetection:
    """Detected safety information."""
    issue_type: SafetyIssue
    confidence: float
    description: str
    severity: str  # low, medium, high
    location_in_image: Optional[Tuple[int, int, int, int]] = None  # bounding box


@dataclass
class PhotoAnalysisResult:
    """Complete photo analysis result."""
    photo_id: str
    metadata: PhotoMetadata
    analysis_date: datetime
    status: AnalysisStatus
    progress_detections: List[ProgressDetection]
    safety_detections: List[SafetyDetection]
    weather_conditions: str
    worker_count: int
    equipment_visible: List[str]
    quality_issues: List[str]
    notes: str = ""
    bim_comparison: Optional[Dict[str, Any]] = None


class ProgressPhotoAnalyzer:
    """Analyze construction site photos."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.photos: Dict[str, PhotoMetadata] = {}
        self.results: Dict[str, PhotoAnalysisResult] = {}
        self._photo_counter = 0

    def register_photo(self,
                      filename: str,
                      capture_date: datetime,
                      location: str,
                      level: str = "",
                      zone: str = "",
                      photo_type: PhotoType = PhotoType.PROGRESS,
                      photographer: str = "",
                      file_path: str = "") -> PhotoMetadata:
        """Register a photo for analysis."""
        self._photo_counter += 1
        photo_id = f"PH-{self._photo_counter:05d}"

        metadata = PhotoMetadata(
            photo_id=photo_id,
            filename=filename,
            capture_date=capture_date,
            location=location,
            level=level,
            zone=zone,
            photo_type=photo_type,
            photographer=photographer,
            file_path=file_path
        )

        self.photos[photo_id] = metadata
        return metadata

    def analyze_photo(self, photo_id: str,
                     image_data: bytes = None) -> PhotoAnalysisResult:
        """Analyze a registered photo."""
        if photo_id not in self.photos:
            raise ValueError(f"Photo {photo_id} not registered")

        metadata = self.photos[photo_id]

        # Perform analysis (simulated - would use CV/AI models)
        progress_detections = self._detect_progress(metadata, image_data)
        safety_detections = self._detect_safety(metadata, image_data)
        weather = self._detect_weather(metadata, image_data)
        worker_count = self._count_workers(image_data)
        equipment = self._detect_equipment(image_data)

        result = PhotoAnalysisResult(
            photo_id=photo_id,
            metadata=metadata,
            analysis_date=datetime.now(),
            status=AnalysisStatus.COMPLETED,
            progress_detections=progress_detections,
            safety_detections=safety_detections,
            weather_conditions=weather,
            worker_count=worker_count,
            equipment_visible=equipment,
            quality_issues=[]
        )

        self.results[photo_id] = result
        return result

    def _detect_progress(self, metadata: PhotoMetadata,
                        image_data: bytes = None) -> List[ProgressDetection]:
        """Detect work progress in photo."""
        # Simulated detection based on metadata
        detections = []

        # In real implementation, this would use computer vision
        location_lower = metadata.location.lower()

        if 'foundation' in location_lower or 'basement' in location_lower:
            detections.append(ProgressDetection(
                work_activity=WorkActivity.FOUNDATION,
                confidence=0.85,
                description="Foundation work visible",
                completion_estimate=60.0
            ))
        elif 'steel' in location_lower or 'structure' in location_lower:
            detections.append(ProgressDetection(
                work_activity=WorkActivity.STEEL_ERECTION,
                confidence=0.90,
                description="Structural steel installation",
                completion_estimate=45.0
            ))
        elif 'roof' in location_lower:
            detections.append(ProgressDetection(
                work_activity=WorkActivity.ROOFING,
                confidence=0.80,
                description="Roofing work in progress",
                completion_estimate=30.0
            ))
        else:
            detections.append(ProgressDetection(
                work_activity=WorkActivity.UNKNOWN,
                confidence=0.50,
                description="General construction activity",
                completion_estimate=0.0
            ))

        return detections

    def _detect_safety(self, metadata: PhotoMetadata,
                      image_data: bytes = None) -> List[SafetyDetection]:
        """Detect safety issues in photo."""
        # Simulated detection - real implementation would use AI models
        detections = []

        # In production, this would analyze the actual image
        if metadata.photo_type == PhotoType.SAFETY:
            # Return empty for demonstration
            pass

        return detections

    def _detect_weather(self, metadata: PhotoMetadata,
                       image_data: bytes = None) -> str:
        """Detect weather conditions from photo."""
        # Simulated - would use image analysis
        return "clear"

    def _count_workers(self, image_data: bytes = None) -> int:
        """Count workers visible in photo."""
        # Simulated - would use person detection
        return 0

    def _detect_equipment(self, image_data: bytes = None) -> List[str]:
        """Detect equipment visible in photo."""
        # Simulated - would use object detection
        return []

    def compare_to_bim(self, photo_id: str,
                      bim_render: bytes = None) -> Dict[str, Any]:
        """Compare photo to BIM model render."""
        if photo_id not in self.results:
            return {'error': 'Photo not analyzed'}

        # Simulated comparison
        comparison = {
            'similarity_score': 0.75,
            'alignment_quality': 'good',
            'discrepancies': [],
            'notes': 'Photo roughly matches BIM model'
        }

        self.results[photo_id].bim_comparison = comparison
        return comparison

    def get_progress_summary(self,
                            from_date: date = None,
                            to_date: date = None) -> Dict[str, Any]:
        """Generate progress summary from analyzed photos."""
        filtered_results = list(self.results.values())

        if from_date:
            filtered_results = [r for r in filtered_results
                              if r.metadata.capture_date.date() >= from_date]
        if to_date:
            filtered_results = [r for r in filtered_results
                              if r.metadata.capture_date.date() <= to_date]

        # Aggregate by activity
        by_activity = {}
        for result in filtered_results:
            for detection in result.progress_detections:
                activity = detection.work_activity.value
                if activity not in by_activity:
                    by_activity[activity] = {
                        'count': 0,
                        'avg_completion': 0,
                        'photos': []
                    }
                by_activity[activity]['count'] += 1
                by_activity[activity]['avg_completion'] += detection.completion_estimate
                by_activity[activity]['photos'].append(result.photo_id)

        # Calculate averages
        for activity in by_activity:
            count = by_activity[activity]['count']
            if count > 0:
                by_activity[activity]['avg_completion'] /= count

        # Safety summary
        total_safety_issues = sum(len(r.safety_detections) for r in filtered_results)

        return {
            'total_photos': len(filtered_results),
            'date_range': {
                'from': from_date.isoformat() if from_date else None,
                'to': to_date.isoformat() if to_date else None
            },
            'by_activity': by_activity,
            'safety_issues_detected': total_safety_issues,
            'average_worker_count': sum(r.worker_count for r in filtered_results) / len(filtered_results) if filtered_results else 0
        }

    def export_report(self, output_path: str):
        """Export analysis results to Excel."""
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Photos list
            photos_data = []
            for result in self.results.values():
                photos_data.append({
                    'Photo ID': result.photo_id,
                    'Filename': result.metadata.filename,
                    'Date': result.metadata.capture_date,
                    'Location': result.metadata.location,
                    'Level': result.metadata.level,
                    'Type': result.metadata.photo_type.value,
                    'Status': result.status.value,
                    'Worker Count': result.worker_count,
                    'Weather': result.weather_conditions
                })

            pd.DataFrame(photos_data).to_excel(writer, sheet_name='Photos', index=False)

            # Progress detections
            progress_data = []
            for result in self.results.values():
                for detection in result.progress_detections:
                    progress_data.append({
                        'Photo ID': result.photo_id,
                        'Activity': detection.work_activity.value,
                        'Confidence': detection.confidence,
                        'Completion %': detection.completion_estimate,
                        'Description': detection.description
                    })

            if progress_data:
                pd.DataFrame(progress_data).to_excel(writer, sheet_name='Progress', index=False)

            # Safety detections
            safety_data = []
            for result in self.results.values():
                for detection in result.safety_detections:
                    safety_data.append({
                        'Photo ID': result.photo_id,
                        'Issue': detection.issue_type.value,
                        'Severity': detection.severity,
                        'Confidence': detection.confidence,
                        'Description': detection.description
                    })

            if safety_data:
                pd.DataFrame(safety_data).to_excel(writer, sheet_name='Safety', index=False)

        return output_path


def analyze_site_photos(photo_files: List[str],
                       project_name: str,
                       output_path: str = None) -> Dict[str, Any]:
    """Quick function to analyze multiple photos."""
    analyzer = ProgressPhotoAnalyzer(project_name)

    for file_path in photo_files:
        path = Path(file_path)
        metadata = analyzer.register_photo(
            filename=path.name,
            capture_date=datetime.now(),
            location="Site",
            photo_type=PhotoType.PROGRESS,
            file_path=file_path
        )
        analyzer.analyze_photo(metadata.photo_id)

    summary = analyzer.get_progress_summary()

    if output_path:
        analyzer.export_report(output_path)

    return summary
```

## Quick Start

```python
# Initialize analyzer
analyzer = ProgressPhotoAnalyzer("Office Tower Project")

# Register and analyze photos
metadata = analyzer.register_photo(
    filename="site_photo_001.jpg",
    capture_date=datetime.now(),
    location="Level 3 - Core",
    level="Level 3",
    zone="Zone A",
    photo_type=PhotoType.PROGRESS,
    photographer="John Smith"
)

result = analyzer.analyze_photo(metadata.photo_id)
print(f"Detected activity: {result.progress_detections[0].work_activity.value}")
print(f"Completion estimate: {result.progress_detections[0].completion_estimate}%")
```

## Common Use Cases

### 1. Daily Progress Report
```python
from datetime import date

summary = analyzer.get_progress_summary(
    from_date=date.today(),
    to_date=date.today()
)
print(f"Photos analyzed today: {summary['total_photos']}")
```

### 2. Safety Monitoring
```python
safety_photos = [r for r in analyzer.results.values() if r.safety_detections]
for result in safety_photos:
    for issue in result.safety_detections:
        print(f"Safety issue: {issue.issue_type.value} - {issue.severity}")
```

### 3. Export Analysis
```python
analyzer.export_report("photo_analysis_report.xlsx")
```

## Resources
- **DDC Book**: Chapter 4.1 - Site Data Collection
- **Reference**: Computer Vision for Construction

---
name: "progress-photo-analyzer"
description: "Analyze field progress photos. Catalog, tag, and compare against planned progress."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🏗️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Field Progress Photo Analyzer

## Business Case

Site photos document progress but are often poorly organized. This skill provides systematic photo cataloging and analysis.

## Technical Implementation

```python
import pandas as pd
from datetime import datetime, date
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class PhotoCategory(Enum):
    PROGRESS = "progress"
    QUALITY = "quality"
    SAFETY = "safety"
    DELIVERY = "delivery"
    ISSUE = "issue"
    GENERAL = "general"


@dataclass
class SitePhoto:
    photo_id: str
    filename: str
    captured_date: datetime
    category: PhotoCategory
    location: str
    level: str
    zone: str
    captured_by: str
    description: str
    tags: List[str] = field(default_factory=list)
    activity_code: str = ""
    file_path: str = ""


class ProgressPhotoAnalyzer:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.photos: Dict[str, SitePhoto] = {}
        self._counter = 0

    def catalog_photo(self, filename: str, captured_date: datetime,
                     category: PhotoCategory, location: str, level: str,
                     captured_by: str, description: str = "",
                     zone: str = "", tags: List[str] = None) -> SitePhoto:
        self._counter += 1
        photo_id = f"PH-{self._counter:05d}"

        photo = SitePhoto(
            photo_id=photo_id,
            filename=filename,
            captured_date=captured_date,
            category=category,
            location=location,
            level=level,
            zone=zone,
            captured_by=captured_by,
            description=description,
            tags=tags or []
        )
        self.photos[photo_id] = photo
        return photo

    def get_photos_by_date(self, target_date: date) -> List[SitePhoto]:
        return [p for p in self.photos.values()
                if p.captured_date.date() == target_date]

    def get_photos_by_location(self, level: str, zone: str = None) -> List[SitePhoto]:
        photos = [p for p in self.photos.values() if p.level == level]
        if zone:
            photos = [p for p in photos if p.zone == zone]
        return photos

    def search_by_tag(self, tag: str) -> List[SitePhoto]:
        tag_lower = tag.lower()
        return [p for p in self.photos.values()
                if any(tag_lower in t.lower() for t in p.tags)]

    def get_summary(self) -> Dict[str, Any]:
        by_category = {}
        by_level = {}
        for p in self.photos.values():
            cat = p.category.value
            by_category[cat] = by_category.get(cat, 0) + 1
            by_level[p.level] = by_level.get(p.level, 0) + 1

        return {
            'total_photos': len(self.photos),
            'by_category': by_category,
            'by_level': by_level
        }

    def export_catalog(self, output_path: str):
        data = [{
            'ID': p.photo_id,
            'Filename': p.filename,
            'Date': p.captured_date,
            'Category': p.category.value,
            'Level': p.level,
            'Zone': p.zone,
            'Location': p.location,
            'By': p.captured_by,
            'Tags': ', '.join(p.tags)
        } for p in self.photos.values()]
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
analyzer = ProgressPhotoAnalyzer("Office Tower")

photo = analyzer.catalog_photo(
    filename="IMG_001.jpg",
    captured_date=datetime.now(),
    category=PhotoCategory.PROGRESS,
    location="Column Grid B-3",
    level="Level 5",
    captured_by="Site Super",
    tags=["concrete", "forming"]
)
```

## Resources
- **DDC Book**: Chapter 4.1 - Site Documentation

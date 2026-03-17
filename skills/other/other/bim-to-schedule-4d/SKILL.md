---
name: "bim-to-schedule-4d"
description: "Link BIM elements to schedule activities for 4D simulation. Visualize construction sequence over time."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "📅", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# BIM to Schedule 4D Integration

## Technical Implementation

```python
import pandas as pd
from datetime import date, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from enum import Enum


class LinkStatus(Enum):
    LINKED = "linked"
    UNLINKED = "unlinked"
    PARTIAL = "partial"


@dataclass
class ScheduleActivity:
    activity_id: str
    activity_name: str
    start_date: date
    end_date: date
    duration_days: int
    wbs_code: str
    predecessors: List[str] = field(default_factory=list)


@dataclass
class BIMElement:
    element_id: str
    element_name: str
    category: str
    level: str
    zone: str
    volume: float = 0
    area: float = 0


@dataclass
class BIMScheduleLink:
    link_id: str
    activity_id: str
    element_ids: List[str]
    link_type: str  # install, remove, temporary
    status: LinkStatus


class BIMSchedule4D:
    def __init__(self, project_name: str):
        self.project_name = project_name
        self.activities: Dict[str, ScheduleActivity] = {}
        self.elements: Dict[str, BIMElement] = {}
        self.links: Dict[str, BIMScheduleLink] = {}
        self._link_counter = 0

    def import_schedule(self, schedule_data: List[Dict[str, Any]]):
        for act in schedule_data:
            activity = ScheduleActivity(
                activity_id=act['id'],
                activity_name=act['name'],
                start_date=act['start'],
                end_date=act['end'],
                duration_days=(act['end'] - act['start']).days,
                wbs_code=act.get('wbs', ''),
                predecessors=act.get('predecessors', [])
            )
            self.activities[activity.activity_id] = activity

    def import_elements(self, element_data: List[Dict[str, Any]]):
        for elem in element_data:
            element = BIMElement(
                element_id=elem['id'],
                element_name=elem['name'],
                category=elem['category'],
                level=elem.get('level', ''),
                zone=elem.get('zone', ''),
                volume=elem.get('volume', 0),
                area=elem.get('area', 0)
            )
            self.elements[element.element_id] = element

    def create_link(self, activity_id: str, element_ids: List[str],
                   link_type: str = "install") -> BIMScheduleLink:
        if activity_id not in self.activities:
            return None

        self._link_counter += 1
        link_id = f"LNK-{self._link_counter:05d}"

        # Verify elements exist
        valid_elements = [eid for eid in element_ids if eid in self.elements]

        status = LinkStatus.LINKED if valid_elements else LinkStatus.UNLINKED
        if valid_elements and len(valid_elements) < len(element_ids):
            status = LinkStatus.PARTIAL

        link = BIMScheduleLink(
            link_id=link_id,
            activity_id=activity_id,
            element_ids=valid_elements,
            link_type=link_type,
            status=status
        )
        self.links[link_id] = link
        return link

    def auto_link_by_level(self, level: str, activity_id: str):
        """Auto-link all elements on a level to an activity."""
        level_elements = [e.element_id for e in self.elements.values()
                        if e.level == level]
        if level_elements:
            return self.create_link(activity_id, level_elements)
        return None

    def get_elements_for_date(self, target_date: date) -> List[BIMElement]:
        """Get elements that should be visible on a specific date."""
        visible_elements = []
        for link in self.links.values():
            activity = self.activities.get(link.activity_id)
            if activity and activity.start_date <= target_date <= activity.end_date:
                for elem_id in link.element_ids:
                    if elem_id in self.elements:
                        visible_elements.append(self.elements[elem_id])
        return visible_elements

    def get_unlinked_elements(self) -> List[BIMElement]:
        linked_ids = set()
        for link in self.links.values():
            linked_ids.update(link.element_ids)
        return [e for e in self.elements.values() if e.element_id not in linked_ids]

    def get_unlinked_activities(self) -> List[ScheduleActivity]:
        linked_activities = {link.activity_id for link in self.links.values()}
        return [a for a in self.activities.values() if a.activity_id not in linked_activities]

    def get_link_summary(self) -> Dict[str, Any]:
        total_elements = len(self.elements)
        linked_elements = len(set(
            eid for link in self.links.values() for eid in link.element_ids
        ))

        return {
            'total_activities': len(self.activities),
            'total_elements': total_elements,
            'linked_elements': linked_elements,
            'unlinked_elements': total_elements - linked_elements,
            'total_links': len(self.links),
            'link_coverage': round(linked_elements / total_elements * 100, 1) if total_elements > 0 else 0
        }

    def export_links(self, output_path: str):
        data = []
        for link in self.links.values():
            activity = self.activities.get(link.activity_id)
            data.append({
                'Link ID': link.link_id,
                'Activity': activity.activity_name if activity else '',
                'Start': activity.start_date if activity else None,
                'End': activity.end_date if activity else None,
                'Elements': len(link.element_ids),
                'Type': link.link_type,
                'Status': link.status.value
            })
        pd.DataFrame(data).to_excel(output_path, index=False)
```

## Quick Start

```python
bim4d = BIMSchedule4D("Office Tower")

# Import schedule
bim4d.import_schedule([
    {'id': 'A100', 'name': 'Foundation', 'start': date(2024, 1, 1), 'end': date(2024, 2, 28)},
    {'id': 'A200', 'name': 'Structure L1', 'start': date(2024, 3, 1), 'end': date(2024, 4, 30)}
])

# Import elements
bim4d.import_elements([
    {'id': 'E001', 'name': 'Footing F1', 'category': 'Foundation', 'level': 'Foundation'},
    {'id': 'E002', 'name': 'Column C1', 'category': 'Structure', 'level': 'Level 1'}
])

# Create links
bim4d.create_link('A100', ['E001'])
bim4d.create_link('A200', ['E002'])

summary = bim4d.get_link_summary()
print(f"Link coverage: {summary['link_coverage']}%")
```

## Resources
- **DDC Book**: Chapter 3.3 - 4D BIM

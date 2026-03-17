---
slug: "4d-simulation"
display_name: "4D Simulation"
description: "Create 4D construction simulations by linking BIM elements to project schedules. Generate time-based visualizations, sequence analysis, and construction phasing with Gantt integration."
---

# 4D Simulation for Construction

## Overview

Based on DDC methodology (Chapter 3.3), this skill implements 4D BIM simulations - linking 3D model elements to the 4th dimension: time. Visualize construction sequences, detect scheduling conflicts, and optimize work phasing.

**Book Reference:** "4D, 6D-8D и расчет CO2" / "4D-8D BIM and CO2 Calculation"

> "4D моделирование позволяет визуализировать последовательность строительства и выявлять конфликты на этапе планирования."
> — DDC Book, Chapter 3.3

## Quick Start

```python
import pandas as pd
from datetime import datetime, timedelta

# BIM elements with schedule data
elements = pd.DataFrame({
    'ElementId': ['E001', 'E002', 'E003', 'E004'],
    'Category': ['Foundation', 'Column', 'Beam', 'Slab'],
    'Level': ['Level 0', 'Level 1', 'Level 1', 'Level 1'],
    'Start_Date': ['2024-01-01', '2024-01-15', '2024-02-01', '2024-02-15'],
    'End_Date': ['2024-01-14', '2024-01-31', '2024-02-14', '2024-02-28'],
    'Phase': ['Structure', 'Structure', 'Structure', 'Structure']
})

elements['Start_Date'] = pd.to_datetime(elements['Start_Date'])
elements['End_Date'] = pd.to_datetime(elements['End_Date'])
elements['Duration_Days'] = (elements['End_Date'] - elements['Start_Date']).dt.days

# Get elements active on a specific date
target_date = pd.to_datetime('2024-01-20')
active_elements = elements[
    (elements['Start_Date'] <= target_date) &
    (elements['End_Date'] >= target_date)
]
print(f"Elements under construction on {target_date.date()}:")
print(active_elements[['ElementId', 'Category']])
```

## 4D Data Model

### Schedule-Element Linking

```python
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class ScheduleElementLinker:
    """Link BIM elements to schedule activities"""

    def __init__(self, elements_df: pd.DataFrame, schedule_df: pd.DataFrame):
        self.elements = elements_df.copy()
        self.schedule = schedule_df.copy()
        self.links = pd.DataFrame()

    def auto_link_by_category(self, mapping: Dict[str, str]):
        """Auto-link elements to activities by category mapping

        Args:
            mapping: Dict mapping element categories to activity names
                     e.g., {'Wall': 'Structural Walls', 'Slab': 'Floor Construction'}
        """
        links = []

        for category, activity_name in mapping.items():
            # Find elements of this category
            category_elements = self.elements[
                self.elements['Category'] == category
            ]['ElementId'].tolist()

            # Find matching activity
            activity = self.schedule[
                self.schedule['Activity'].str.contains(activity_name, case=False)
            ]

            if not activity.empty and category_elements:
                for elem_id in category_elements:
                    links.append({
                        'ElementId': elem_id,
                        'ActivityId': activity.iloc[0]['ActivityId'],
                        'Activity': activity.iloc[0]['Activity'],
                        'Start_Date': activity.iloc[0]['Start_Date'],
                        'End_Date': activity.iloc[0]['End_Date']
                    })

        self.links = pd.DataFrame(links)
        return self.links

    def auto_link_by_level(self):
        """Auto-link elements based on level and construction sequence"""
        # Get unique levels in order
        levels = sorted(self.elements['Level'].unique())

        links = []
        for i, level in enumerate(levels):
            level_elements = self.elements[self.elements['Level'] == level]

            # Find activity for this level
            level_activity = self.schedule[
                self.schedule['Activity'].str.contains(level, case=False)
            ]

            if not level_activity.empty:
                for _, elem in level_elements.iterrows():
                    links.append({
                        'ElementId': elem['ElementId'],
                        'ActivityId': level_activity.iloc[0]['ActivityId'],
                        'Activity': level_activity.iloc[0]['Activity'],
                        'Start_Date': level_activity.iloc[0]['Start_Date'],
                        'End_Date': level_activity.iloc[0]['End_Date']
                    })

        self.links = pd.DataFrame(links)
        return self.links

    def manual_link(self, element_id: str, activity_id: str):
        """Manually link element to activity"""
        element = self.elements[self.elements['ElementId'] == element_id]
        activity = self.schedule[self.schedule['ActivityId'] == activity_id]

        if element.empty or activity.empty:
            raise ValueError("Element or activity not found")

        new_link = pd.DataFrame([{
            'ElementId': element_id,
            'ActivityId': activity_id,
            'Activity': activity.iloc[0]['Activity'],
            'Start_Date': activity.iloc[0]['Start_Date'],
            'End_Date': activity.iloc[0]['End_Date']
        }])

        self.links = pd.concat([self.links, new_link], ignore_index=True)
        return self.links

    def get_linked_elements(self):
        """Get elements with schedule data"""
        return self.elements.merge(
            self.links[['ElementId', 'ActivityId', 'Start_Date', 'End_Date']],
            on='ElementId',
            how='left'
        )
```

### 4D Simulation Engine

```python
class Simulation4D:
    """4D construction simulation engine"""

    def __init__(self, linked_elements: pd.DataFrame):
        self.elements = linked_elements.copy()
        self.elements['Start_Date'] = pd.to_datetime(self.elements['Start_Date'])
        self.elements['End_Date'] = pd.to_datetime(self.elements['End_Date'])

        self.project_start = self.elements['Start_Date'].min()
        self.project_end = self.elements['End_Date'].max()

    def get_state_at_date(self, target_date: datetime) -> pd.DataFrame:
        """Get element states at a specific date"""
        target = pd.to_datetime(target_date)

        # Determine state for each element
        conditions = [
            target < self.elements['Start_Date'],  # Not started
            (self.elements['Start_Date'] <= target) & (target <= self.elements['End_Date']),  # In progress
            target > self.elements['End_Date']  # Completed
        ]
        choices = ['not_started', 'in_progress', 'completed']

        self.elements['State'] = np.select(conditions, choices, default='unknown')

        return self.elements.copy()

    def generate_timeline(self, interval_days: int = 7) -> List[Dict]:
        """Generate timeline snapshots"""
        timeline = []
        current_date = self.project_start

        while current_date <= self.project_end:
            state = self.get_state_at_date(current_date)

            snapshot = {
                'date': current_date,
                'not_started': len(state[state['State'] == 'not_started']),
                'in_progress': len(state[state['State'] == 'in_progress']),
                'completed': len(state[state['State'] == 'completed']),
                'total': len(state)
            }
            snapshot['progress_pct'] = (snapshot['completed'] / snapshot['total']) * 100

            timeline.append(snapshot)
            current_date += timedelta(days=interval_days)

        return timeline

    def get_elements_in_progress(self, target_date: datetime) -> pd.DataFrame:
        """Get elements currently under construction"""
        state = self.get_state_at_date(target_date)
        return state[state['State'] == 'in_progress']

    def analyze_construction_sequence(self) -> pd.DataFrame:
        """Analyze construction sequence by category and level"""
        sequence = self.elements.groupby(['Level', 'Category']).agg({
            'Start_Date': 'min',
            'End_Date': 'max',
            'ElementId': 'count'
        }).rename(columns={'ElementId': 'Element_Count'})

        sequence['Duration_Days'] = (sequence['End_Date'] - sequence['Start_Date']).dt.days
        sequence = sequence.sort_values('Start_Date').reset_index()

        return sequence

    def detect_parallel_work(self) -> pd.DataFrame:
        """Detect work happening in parallel"""
        dates = pd.date_range(self.project_start, self.project_end, freq='D')
        parallel_work = []

        for date in dates:
            state = self.get_state_at_date(date)
            in_progress = state[state['State'] == 'in_progress']

            if len(in_progress) > 1:
                categories = in_progress['Category'].unique().tolist()
                levels = in_progress['Level'].unique().tolist()

                parallel_work.append({
                    'date': date,
                    'parallel_count': len(in_progress),
                    'categories': ', '.join(categories),
                    'levels': ', '.join(levels)
                })

        return pd.DataFrame(parallel_work)
```

## Gantt Chart Integration

### Gantt Chart Generator

```python
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Patch

class GanttChartGenerator:
    """Generate Gantt charts for 4D simulation"""

    def __init__(self, elements: pd.DataFrame):
        self.elements = elements.copy()
        self.colors = {
            'Foundation': '#8B4513',
            'Column': '#4169E1',
            'Beam': '#228B22',
            'Slab': '#DC143C',
            'Wall': '#FF8C00',
            'Roof': '#9932CC',
            'MEP': '#20B2AA',
            'Finishes': '#FFD700'
        }

    def create_gantt(self, group_by='Category', figsize=(14, 8)):
        """Create Gantt chart grouped by specified column"""
        fig, ax = plt.subplots(figsize=figsize)

        # Group elements
        groups = self.elements.groupby(group_by)

        y_pos = 0
        y_labels = []
        legend_elements = []

        for group_name, group_df in groups:
            color = self.colors.get(group_name, '#808080')

            for _, row in group_df.iterrows():
                start = row['Start_Date']
                duration = (row['End_Date'] - row['Start_Date']).days

                ax.barh(y_pos, duration, left=start, height=0.6,
                       color=color, alpha=0.8, edgecolor='black', linewidth=0.5)

                y_pos += 1

            y_labels.append(group_name)
            legend_elements.append(Patch(facecolor=color, label=group_name))

        # Formatting
        ax.set_yticks(range(len(self.elements)))
        ax.set_yticklabels(self.elements['ElementId'])
        ax.set_xlabel('Date')
        ax.set_title('Construction Schedule - Gantt Chart', fontsize=14, fontweight='bold')

        # Date formatting
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
        plt.xticks(rotation=45)

        # Legend
        ax.legend(handles=legend_elements, loc='upper right')

        # Grid
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        return fig

    def create_level_gantt(self, figsize=(14, 10)):
        """Create Gantt chart grouped by level"""
        fig, ax = plt.subplots(figsize=figsize)

        levels = sorted(self.elements['Level'].unique())

        for i, level in enumerate(levels):
            level_elements = self.elements[self.elements['Level'] == level]

            for _, row in level_elements.iterrows():
                color = self.colors.get(row['Category'], '#808080')
                start = row['Start_Date']
                duration = (row['End_Date'] - row['Start_Date']).days

                ax.barh(i, duration, left=start, height=0.4,
                       color=color, alpha=0.8, edgecolor='black', linewidth=0.5)

        ax.set_yticks(range(len(levels)))
        ax.set_yticklabels(levels)
        ax.set_xlabel('Date')
        ax.set_ylabel('Building Level')
        ax.set_title('Construction Sequence by Level', fontsize=14, fontweight='bold')

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Add legend
        legend_patches = [Patch(color=c, label=cat) for cat, c in self.colors.items()
                         if cat in self.elements['Category'].values]
        ax.legend(handles=legend_patches, loc='upper right')

        plt.tight_layout()
        return fig

    def create_progress_chart(self, timeline: List[Dict], figsize=(12, 6)):
        """Create S-curve progress chart"""
        df = pd.DataFrame(timeline)

        fig, ax = plt.subplots(figsize=figsize)

        ax.plot(df['date'], df['progress_pct'], 'b-', linewidth=2, label='Progress')
        ax.fill_between(df['date'], 0, df['progress_pct'], alpha=0.3)

        # Add milestones at 25%, 50%, 75%, 100%
        for milestone in [25, 50, 75, 100]:
            ax.axhline(y=milestone, color='gray', linestyle='--', alpha=0.5)
            ax.text(df['date'].iloc[0], milestone + 2, f'{milestone}%',
                   fontsize=9, color='gray')

        ax.set_xlabel('Date')
        ax.set_ylabel('Progress (%)')
        ax.set_title('Project S-Curve', fontsize=14, fontweight='bold')
        ax.set_ylim(0, 105)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        plt.tight_layout()
        return fig
```

## Sequence Analysis

### Construction Sequence Optimizer

```python
class SequenceAnalyzer:
    """Analyze and optimize construction sequences"""

    def __init__(self, elements: pd.DataFrame):
        self.elements = elements.copy()
        self.dependencies = []

    def add_dependency(self, predecessor: str, successor: str, lag_days: int = 0):
        """Add dependency between elements"""
        self.dependencies.append({
            'predecessor': predecessor,
            'successor': successor,
            'lag_days': lag_days
        })

    def check_sequence_violations(self) -> List[Dict]:
        """Check for sequence violations"""
        violations = []

        for dep in self.dependencies:
            pred = self.elements[self.elements['ElementId'] == dep['predecessor']]
            succ = self.elements[self.elements['ElementId'] == dep['successor']]

            if pred.empty or succ.empty:
                continue

            pred_end = pred.iloc[0]['End_Date']
            succ_start = succ.iloc[0]['Start_Date']

            required_start = pred_end + timedelta(days=dep['lag_days'])

            if succ_start < required_start:
                violations.append({
                    'predecessor': dep['predecessor'],
                    'successor': dep['successor'],
                    'predecessor_end': pred_end,
                    'successor_start': succ_start,
                    'required_start': required_start,
                    'violation_days': (required_start - succ_start).days
                })

        return violations

    def check_spatial_conflicts(self) -> List[Dict]:
        """Check for spatial conflicts (same location, same time)"""
        conflicts = []

        # Group by location (Level + Zone if available)
        location_col = 'Level'

        for location, group in self.elements.groupby(location_col):
            if len(group) < 2:
                continue

            # Check for overlapping work
            for i, row1 in group.iterrows():
                for j, row2 in group.iterrows():
                    if i >= j:
                        continue

                    # Check date overlap
                    overlap = (row1['Start_Date'] <= row2['End_Date'] and
                              row2['Start_Date'] <= row1['End_Date'])

                    if overlap:
                        conflicts.append({
                            'location': location,
                            'element1': row1['ElementId'],
                            'element1_category': row1['Category'],
                            'element2': row2['ElementId'],
                            'element2_category': row2['Category'],
                            'overlap_start': max(row1['Start_Date'], row2['Start_Date']),
                            'overlap_end': min(row1['End_Date'], row2['End_Date'])
                        })

        return conflicts

    def calculate_critical_path(self) -> List[str]:
        """Calculate critical path (simplified)"""
        # Build dependency graph
        graph = {}
        for elem in self.elements['ElementId']:
            graph[elem] = {
                'predecessors': [],
                'duration': 0
            }

        for dep in self.dependencies:
            if dep['successor'] in graph:
                graph[dep['successor']]['predecessors'].append(dep['predecessor'])

        # Calculate durations
        for _, row in self.elements.iterrows():
            if row['ElementId'] in graph:
                graph[row['ElementId']]['duration'] = (row['End_Date'] - row['Start_Date']).days

        # Find longest path (simplified critical path)
        def longest_path(node, memo={}):
            if node in memo:
                return memo[node]

            if not graph[node]['predecessors']:
                return graph[node]['duration']

            max_pred = max(
                longest_path(pred, memo) for pred in graph[node]['predecessors']
            )
            memo[node] = max_pred + graph[node]['duration']
            return memo[node]

        # Get all path lengths
        path_lengths = {elem: longest_path(elem) for elem in graph.keys()}

        # Critical path elements
        max_length = max(path_lengths.values())
        critical = [elem for elem, length in path_lengths.items() if length == max_length]

        return critical
```

## Export and Integration

```python
def export_4d_schedule(elements: pd.DataFrame, output_path: str):
    """Export 4D schedule to Excel with multiple views"""
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Full schedule
        elements.to_excel(writer, sheet_name='Schedule', index=False)

        # By level
        level_summary = elements.groupby('Level').agg({
            'ElementId': 'count',
            'Start_Date': 'min',
            'End_Date': 'max'
        }).rename(columns={'ElementId': 'Element_Count'})
        level_summary['Duration_Days'] = (level_summary['End_Date'] - level_summary['Start_Date']).dt.days
        level_summary.to_excel(writer, sheet_name='By_Level')

        # By category
        cat_summary = elements.groupby('Category').agg({
            'ElementId': 'count',
            'Start_Date': 'min',
            'End_Date': 'max'
        }).rename(columns={'ElementId': 'Element_Count'})
        cat_summary.to_excel(writer, sheet_name='By_Category')

    return output_path
```

## Quick Reference

| Concept | Description |
|---------|-------------|
| 4D = 3D + Time | BIM model linked to schedule |
| Activity | Scheduled work item |
| Element State | not_started / in_progress / completed |
| Critical Path | Longest sequence determining project duration |

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 3.3
- **Website**: https://datadrivenconstruction.io

## Next Steps

- See `gantt-chart` for schedule visualization
- See `co2-estimation` for 6D (sustainability) analysis
- See `clash-detection-analysis` for 4D conflict detection

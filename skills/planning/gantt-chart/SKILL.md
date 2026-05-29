---
name: "gantt-chart"
description: "Generate Gantt charts for construction scheduling. Create visual project timelines with dependencies and progress tracking."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🎬", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Gantt Chart Generator

## Business Case

### Problem Statement
Schedule visualization challenges:
- Complex task dependencies
- Progress tracking
- Critical path visibility
- Multi-level WBS display

### Solution
Generate interactive Gantt charts from schedule data with dependency visualization, progress tracking, and export capabilities.

## Technical Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum


class TaskStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    ON_HOLD = "on_hold"


class DependencyType(Enum):
    FS = "finish_to_start"
    SS = "start_to_start"
    FF = "finish_to_finish"
    SF = "start_to_finish"


@dataclass
class Task:
    task_id: str
    name: str
    start_date: date
    end_date: date
    wbs_code: str = ""
    progress: float = 0  # 0-100
    status: TaskStatus = TaskStatus.NOT_STARTED
    assignee: str = ""
    level: int = 0
    is_milestone: bool = False
    is_summary: bool = False
    parent_id: str = ""


@dataclass
class Dependency:
    predecessor_id: str
    successor_id: str
    dep_type: DependencyType = DependencyType.FS
    lag: int = 0


class GanttChartGenerator:
    """Generate Gantt charts for construction scheduling."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        self.tasks: Dict[str, Task] = {}
        self.dependencies: List[Dependency] = []

    def add_task(self, task: Task):
        """Add task to chart."""
        self.tasks[task.task_id] = task

    def add_dependency(self, predecessor_id: str, successor_id: str,
                       dep_type: DependencyType = DependencyType.FS,
                       lag: int = 0):
        """Add dependency between tasks."""
        self.dependencies.append(Dependency(
            predecessor_id=predecessor_id,
            successor_id=successor_id,
            dep_type=dep_type,
            lag=lag
        ))

    def import_from_df(self, df: pd.DataFrame):
        """Import tasks from DataFrame."""

        for _, row in df.iterrows():
            task = Task(
                task_id=str(row['task_id']),
                name=row['name'],
                start_date=pd.to_datetime(row['start_date']).date(),
                end_date=pd.to_datetime(row['end_date']).date(),
                wbs_code=str(row.get('wbs_code', '')),
                progress=float(row.get('progress', 0)),
                level=int(row.get('level', 0)),
                is_milestone=bool(row.get('is_milestone', False)),
                is_summary=bool(row.get('is_summary', False)),
                parent_id=str(row.get('parent_id', ''))
            )
            self.add_task(task)

    def get_project_range(self) -> tuple:
        """Get project date range."""

        if not self.tasks:
            return (date.today(), date.today())

        min_date = min(t.start_date for t in self.tasks.values())
        max_date = max(t.end_date for t in self.tasks.values())
        return (min_date, max_date)

    def get_duration(self, task_id: str) -> int:
        """Get task duration in days."""

        task = self.tasks.get(task_id)
        if task:
            return (task.end_date - task.start_date).days + 1
        return 0

    def generate_text_gantt(self, width: int = 60) -> str:
        """Generate text-based Gantt chart."""

        if not self.tasks:
            return "No tasks"

        lines = []
        start, end = self.get_project_range()
        total_days = (end - start).days + 1
        scale = width / total_days if total_days > 0 else 1

        # Header
        lines.append(f"Project: {self.project_name}")
        lines.append(f"Period: {start} to {end}")
        lines.append("-" * (40 + width))

        # Tasks
        for task in sorted(self.tasks.values(), key=lambda t: (t.level, t.start_date)):
            indent = "  " * task.level
            name = f"{indent}{task.name}"[:35].ljust(35)

            # Bar position
            bar_start = int((task.start_date - start).days * scale)
            bar_length = max(1, int(self.get_duration(task.task_id) * scale))

            # Progress bar
            progress_length = int(bar_length * task.progress / 100)
            bar = " " * bar_start
            bar += "█" * progress_length
            bar += "░" * (bar_length - progress_length)
            bar = bar[:width].ljust(width)

            status_char = "◆" if task.is_milestone else "│"
            lines.append(f"{name} {status_char}{bar}│ {task.progress:.0f}%")

        return "\n".join(lines)

    def generate_mermaid_gantt(self) -> str:
        """Generate Mermaid Gantt diagram."""

        lines = [
            "gantt",
            f"    title {self.project_name}",
            "    dateFormat YYYY-MM-DD",
            ""
        ]

        # Group by WBS prefix
        sections = {}
        for task in self.tasks.values():
            section = task.wbs_code.split('.')[0] if task.wbs_code else "Tasks"
            if section not in sections:
                sections[section] = []
            sections[section].append(task)

        for section, tasks in sections.items():
            lines.append(f"    section {section}")
            for task in sorted(tasks, key=lambda t: t.start_date):
                duration = self.get_duration(task.task_id)
                status = ""
                if task.status == TaskStatus.COMPLETED:
                    status = "done, "
                elif task.status == TaskStatus.IN_PROGRESS:
                    status = "active, "

                if task.is_milestone:
                    lines.append(f"    {task.name} :milestone, {task.start_date}, 0d")
                else:
                    lines.append(f"    {task.name} :{status}{task.task_id}, {task.start_date}, {duration}d")

        return "\n".join(lines)

    def generate_html_gantt(self) -> str:
        """Generate HTML/CSS Gantt chart."""

        start, end = self.get_project_range()
        total_days = (end - start).days + 1

        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Gantt Chart - {self.project_name}</title>
    <style>
        .gantt {{ font-family: Arial, sans-serif; }}
        .task {{ display: flex; margin: 2px 0; height: 25px; align-items: center; }}
        .task-name {{ width: 200px; padding-right: 10px; font-size: 12px; }}
        .task-bar {{ position: relative; height: 20px; background: #e0e0e0; flex: 1; }}
        .bar {{ position: absolute; height: 100%; }}
        .bar-fill {{ background: #4CAF50; }}
        .bar-progress {{ background: #2196F3; }}
        .milestone {{ width: 10px; height: 10px; background: #FF5722; transform: rotate(45deg); margin-left: 10px; }}
    </style>
</head>
<body>
    <div class="gantt">
        <h2>{self.project_name}</h2>
        <p>{start} - {end}</p>
"""

        for task in sorted(self.tasks.values(), key=lambda t: (t.level, t.start_date)):
            left = ((task.start_date - start).days / total_days) * 100
            width = (self.get_duration(task.task_id) / total_days) * 100
            progress_width = width * task.progress / 100

            indent = "&nbsp;" * (task.level * 4)

            if task.is_milestone:
                html += f'<div class="task"><div class="task-name">{indent}{task.name}</div><div class="task-bar"><div class="milestone" style="left:{left}%"></div></div></div>\n'
            else:
                html += f'''<div class="task">
    <div class="task-name">{indent}{task.name}</div>
    <div class="task-bar">
        <div class="bar bar-fill" style="left:{left}%; width:{width}%"></div>
        <div class="bar bar-progress" style="left:{left}%; width:{progress_width}%"></div>
    </div>
</div>\n'''

        html += "</div></body></html>"
        return html

    def get_critical_path(self) -> List[str]:
        """Identify critical path tasks (simplified)."""

        if not self.dependencies:
            return [t.task_id for t in sorted(self.tasks.values(), key=lambda x: x.end_date)[-5:]]

        # Find tasks with no slack (simplified approach)
        critical = []
        _, project_end = self.get_project_range()

        for task in self.tasks.values():
            if task.end_date == project_end:
                critical.append(task.task_id)
                # Trace predecessors
                for dep in self.dependencies:
                    if dep.successor_id == task.task_id:
                        critical.append(dep.predecessor_id)

        return list(set(critical))

    def export_to_excel(self, output_path: str) -> str:
        """Export Gantt data to Excel."""

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Tasks
            tasks_df = pd.DataFrame([{
                'ID': t.task_id,
                'WBS': t.wbs_code,
                'Name': t.name,
                'Start': t.start_date,
                'End': t.end_date,
                'Duration': self.get_duration(t.task_id),
                'Progress': t.progress,
                'Status': t.status.value,
                'Level': t.level
            } for t in self.tasks.values()])
            tasks_df.to_excel(writer, sheet_name='Tasks', index=False)

            # Dependencies
            deps_df = pd.DataFrame([{
                'Predecessor': d.predecessor_id,
                'Successor': d.successor_id,
                'Type': d.dep_type.value,
                'Lag': d.lag
            } for d in self.dependencies])
            deps_df.to_excel(writer, sheet_name='Dependencies', index=False)

        return output_path
```

## Quick Start

```python
from datetime import date, timedelta

# Create Gantt chart
gantt = GanttChartGenerator("Office Building A")

# Add tasks
gantt.add_task(Task("T1", "Foundation", date(2024, 6, 1), date(2024, 6, 30), "01", progress=100))
gantt.add_task(Task("T2", "Structure", date(2024, 7, 1), date(2024, 9, 30), "02", progress=60))
gantt.add_task(Task("T3", "MEP Rough-in", date(2024, 8, 1), date(2024, 10, 31), "03", progress=30))
gantt.add_task(Task("M1", "Topping Out", date(2024, 9, 30), date(2024, 9, 30), is_milestone=True))

# Add dependencies
gantt.add_dependency("T1", "T2")
gantt.add_dependency("T2", "T3")

# Generate text Gantt
print(gantt.generate_text_gantt())
```

## Common Use Cases

### 1. Mermaid Diagram
```python
mermaid = gantt.generate_mermaid_gantt()
print(mermaid)  # Copy to Mermaid editor
```

### 2. HTML Export
```python
html = gantt.generate_html_gantt()
with open("gantt.html", "w") as f:
    f.write(html)
```

### 3. Critical Path
```python
critical = gantt.get_critical_path()
print(f"Critical tasks: {critical}")
```

## Resources
- **DDC Book**: Chapter 3.3 - 4D Scheduling and BIM
- **Website**: https://datadrivenconstruction.io

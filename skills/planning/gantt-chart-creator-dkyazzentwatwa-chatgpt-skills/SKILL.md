---
name: gantt-chart-creator
description: Create project timeline Gantt charts with dependencies, milestones, and progress tracking. Supports static (PNG/SVG) and interactive (HTML) output.
---

# Gantt Chart Creator

Create professional project timeline Gantt charts with task dependencies, milestones, progress tracking, and customizable styling. Perfect for project management, sprint planning, and timeline visualization.

## Quick Start

```python
from scripts.gantt_creator import GanttChartCreator

# Simple task list
gantt = GanttChartCreator()
gantt.add_task("Research", "2024-01-01", "2024-01-07")
gantt.add_task("Design", "2024-01-08", "2024-01-14")
gantt.add_task("Development", "2024-01-15", "2024-01-28")
gantt.add_task("Testing", "2024-01-29", "2024-02-04")
gantt.generate().save("project.png")

# From CSV with progress
gantt = GanttChartCreator()
gantt.from_csv("tasks.csv", task="name", start="start_date", end="end_date", progress="pct")
gantt.title("Q1 Roadmap").show_today().generate().save("roadmap.png")
```

## Features

- **Multiple Input Sources**: CSV, JSON, dict, or programmatic
- **Task Properties**: Name, dates, progress, assignee, category
- **Dependencies**: Finish-to-start and other dependency types
- **Milestones**: Diamond markers for key dates
- **Progress Tracking**: Visual progress bars within tasks
- **Today Marker**: Vertical line showing current date
- **Color Coding**: By category, assignee, or status
- **Output Formats**: PNG, SVG, PDF (matplotlib) or HTML (interactive)

## API Reference

### Initialization

```python
gantt = GanttChartCreator()
```

### Data Input Methods

```python
# From CSV file
gantt.from_csv(
    filepath="tasks.csv",
    task="task_name",           # Task name column
    start="start_date",         # Start date column
    end="end_date",             # End date column
    progress="completion",      # Optional: progress % column
    category="category",        # Optional: for color coding
    assignee="owner"            # Optional: for color coding
)

# From list of task dictionaries
gantt.from_tasks([
    {'name': 'Task 1', 'start': '2024-01-01', 'end': '2024-01-07'},
    {'name': 'Task 2', 'start': '2024-01-08', 'end': '2024-01-14', 'progress': 50},
    {'name': 'Task 3', 'start': '2024-01-15', 'end': '2024-01-21', 'category': 'Dev'}
])

# Add individual tasks
gantt.add_task(
    name="Research Phase",
    start="2024-01-01",
    end="2024-01-14",
    progress=100,               # Optional: 0-100%
    category="Planning",        # Optional: for coloring
    assignee="Alice"            # Optional: for coloring
)

# Add milestones
gantt.add_milestone("Project Kickoff", "2024-01-01")
gantt.add_milestone("Beta Release", "2024-02-15", color="#e74c3c")
```

### Dependencies

```python
# Add task dependencies (finish-to-start by default)
gantt.add_dependency("Design", "Development")  # Development starts after Design
gantt.add_dependency("Development", "Testing")

# Dependency types
gantt.add_dependency("Task A", "Task B", type="FS")  # Finish-to-Start (default)
gantt.add_dependency("Task A", "Task B", type="SS")  # Start-to-Start
gantt.add_dependency("Task A", "Task B", type="FF")  # Finish-to-Finish
gantt.add_dependency("Task A", "Task B", type="SF")  # Start-to-Finish
```

### Styling

```python
# Title
gantt.title("Project Timeline")
gantt.title("Q1 2024 Roadmap", font_size=16)

# Color by category
gantt.color_by("category")
gantt.color_by("category", colors={
    'Planning': '#3498db',
    'Development': '#2ecc71',
    'Testing': '#e74c3c'
})

# Color by assignee
gantt.color_by("assignee")

# Show progress bars
gantt.show_progress(True)

# Show today marker
gantt.show_today(True)
gantt.show_today(True, color='red', label='Today')

# Date range (auto-calculated by default)
gantt.date_range("2024-01-01", "2024-03-31")

# Grid lines
gantt.grid(show=True, style='weekly')  # daily, weekly, monthly
```

### Generation and Export

```python
# Generate static chart (matplotlib)
gantt.generate()

# Generate interactive chart (plotly)
gantt.generate(interactive=True)

# Save static image
gantt.save("chart.png")
gantt.save("chart.svg")
gantt.save("chart.pdf")

# Save interactive HTML
gantt.save("chart.html")

# Get figure object for customization
fig = gantt.get_figure()

# Show in window/notebook
gantt.show()
```

## Data Formats

### CSV Format

```csv
task,start_date,end_date,progress,category,assignee
Research,2024-01-01,2024-01-07,100,Planning,Alice
Design,2024-01-08,2024-01-14,100,Planning,Bob
Backend Dev,2024-01-15,2024-01-28,75,Development,Alice
Frontend Dev,2024-01-15,2024-01-21,50,Development,Carol
Testing,2024-01-29,2024-02-04,0,QA,Dave
```

### Task Dictionary Format

```python
tasks = [
    {
        'name': 'Research',
        'start': '2024-01-01',
        'end': '2024-01-07',
        'progress': 100,
        'category': 'Planning',
        'assignee': 'Alice'
    },
    {
        'name': 'Design',
        'start': '2024-01-08',
        'end': '2024-01-14',
        'progress': 75,
        'category': 'Planning'
    }
]
```

### Date Formats

Supported date formats (auto-detected):
- `YYYY-MM-DD` (ISO format, recommended)
- `MM/DD/YYYY`
- `DD/MM/YYYY`
- `YYYY/MM/DD`

## CLI Usage

```bash
# Basic usage
python gantt_creator.py --input tasks.csv \
    --task name --start start_date --end end_date \
    --output gantt.png

# With progress and categories
python gantt_creator.py --input project.csv \
    --task task --start begin --end finish \
    --progress pct --category type \
    --title "Project Timeline" \
    --output timeline.png

# Interactive HTML
python gantt_creator.py --input tasks.csv \
    --task name --start start --end end \
    --interactive \
    --output gantt.html

# With today marker
python gantt_creator.py --input tasks.csv \
    --task name --start start --end end \
    --show-today \
    --output current_status.png
```

### CLI Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--input` | Input CSV file | Required |
| `--task` | Task name column | Required |
| `--start` | Start date column | Required |
| `--end` | End date column | Required |
| `--progress` | Progress % column | - |
| `--category` | Category column (for coloring) | - |
| `--assignee` | Assignee column (for coloring) | - |
| `--output` | Output file path | `gantt.png` |
| `--title` | Chart title | - |
| `--interactive` | Generate interactive HTML | False |
| `--show-today` | Show today marker | False |
| `--show-progress` | Show progress bars | False |
| `--width` | Chart width | 12 |
| `--height` | Chart height | 6 |

## Examples

### Simple Project Timeline

```python
gantt = GanttChartCreator()
gantt.add_task("Planning", "2024-01-01", "2024-01-14")
gantt.add_task("Development", "2024-01-15", "2024-02-15")
gantt.add_task("Testing", "2024-02-16", "2024-02-28")
gantt.add_task("Deployment", "2024-03-01", "2024-03-07")
gantt.title("Project Alpha")
gantt.generate().save("project_alpha.png")
```

### With Dependencies and Milestones

```python
gantt = GanttChartCreator()

# Add tasks
gantt.add_task("Requirements", "2024-01-01", "2024-01-07")
gantt.add_task("Design", "2024-01-08", "2024-01-14")
gantt.add_task("Backend", "2024-01-15", "2024-01-28")
gantt.add_task("Frontend", "2024-01-15", "2024-01-21")
gantt.add_task("Integration", "2024-01-29", "2024-02-04")
gantt.add_task("Testing", "2024-02-05", "2024-02-11")

# Add milestones
gantt.add_milestone("Kickoff", "2024-01-01")
gantt.add_milestone("Code Freeze", "2024-02-04")
gantt.add_milestone("Launch", "2024-02-12")

# Add dependencies
gantt.add_dependency("Requirements", "Design")
gantt.add_dependency("Design", "Backend")
gantt.add_dependency("Design", "Frontend")
gantt.add_dependency("Backend", "Integration")
gantt.add_dependency("Frontend", "Integration")
gantt.add_dependency("Integration", "Testing")

gantt.title("Development Timeline")
gantt.generate().save("dev_timeline.png")
```

### Color-Coded by Category

```python
gantt = GanttChartCreator()
gantt.from_csv("tasks.csv", task="name", start="start", end="end", category="type")

gantt.color_by("category", colors={
    'Backend': '#3498db',
    'Frontend': '#2ecc71',
    'DevOps': '#9b59b6',
    'QA': '#e74c3c'
})

gantt.title("Sprint 5 Tasks")
gantt.show_today()
gantt.generate().save("sprint5.png")
```

### Progress Tracking

```python
gantt = GanttChartCreator()

gantt.add_task("Research", "2024-01-01", "2024-01-07", progress=100)
gantt.add_task("Design", "2024-01-08", "2024-01-14", progress=100)
gantt.add_task("Development", "2024-01-15", "2024-01-28", progress=60)
gantt.add_task("Testing", "2024-01-29", "2024-02-04", progress=0)

gantt.show_progress(True)
gantt.show_today(True)
gantt.title("Project Status")
gantt.generate().save("status.png")
```

### Interactive HTML Chart

```python
gantt = GanttChartCreator()
gantt.from_csv("project.csv", task="task", start="start", end="end",
               progress="pct", category="team")

gantt.color_by("team")
gantt.show_progress(True)
gantt.title("Interactive Project View")
gantt.generate(interactive=True)
gantt.save("project.html")
```

### Team Workload

```python
gantt = GanttChartCreator()

# Alice's tasks
gantt.add_task("Alice: Research", "2024-01-01", "2024-01-07", assignee="Alice")
gantt.add_task("Alice: Backend", "2024-01-08", "2024-01-21", assignee="Alice")

# Bob's tasks
gantt.add_task("Bob: Design", "2024-01-01", "2024-01-14", assignee="Bob")
gantt.add_task("Bob: Frontend", "2024-01-15", "2024-01-28", assignee="Bob")

# Carol's tasks
gantt.add_task("Carol: Testing", "2024-01-22", "2024-02-04", assignee="Carol")

gantt.color_by("assignee", colors={
    'Alice': '#3498db',
    'Bob': '#2ecc71',
    'Carol': '#e74c3c'
})
gantt.title("Team Workload - January")
gantt.generate().save("team_workload.png")
```

## Dependencies

```
matplotlib>=3.7.0
plotly>=5.15.0
pandas>=2.0.0
kaleido>=0.2.0
```

## Limitations

- Static charts (matplotlib) have limited interactivity
- Complex dependency networks may be hard to visualize
- Date granularity is daily (no hour-level precision)
- Maximum ~50 tasks for readable charts

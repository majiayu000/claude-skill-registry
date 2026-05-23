---
name: "nobim-image-generator"
description: "Generate images and visualizations from Revit/IFC files without BIM software. Python-based noBIM tool for batch processing."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🖼️", "os": ["win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"], "anyBins": ["ifcopenshell"]}}}
---
# noBIM Image Generator

## Business Case

### Problem Statement
Creating visualizations from BIM models typically requires:
- Expensive BIM software licenses
- Manual screenshot capture
- Time-consuming rendering
- Impossible to batch process

### Solution
noBIM tool extracts data and generates visualizations using Python libraries, processing hundreds of projects without BIM software.

### Business Value
- **No license required** - Pure Python solution
- **Batch processing** - Generate images for 1000s of projects
- **Customizable** - Create exactly the visualizations you need
- **Automatable** - Integrate into data pipelines

## Technical Implementation

### Installation
```bash
pip install pandas matplotlib seaborn plotly ifcopenshell
```

### Core Functionality

```python
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from pathlib import Path
from typing import List, Optional, Tuple

class NoBIMVisualizer:
    def __init__(self):
        self.elements = None
        self.project_name = ""

    def load_from_excel(self, xlsx_path: str) -> int:
        """Load BIM data from converted Excel file."""
        self.elements = pd.read_excel(xlsx_path, sheet_name="Elements")
        self.project_name = Path(xlsx_path).stem
        return len(self.elements)

    def generate_3d_scatter(self, output_path: str,
                            color_by: str = "Category",
                            size: Tuple[int, int] = (12, 10)) -> str:
        """Generate 3D scatter plot of elements."""
        if not all(col in self.elements.columns
                   for col in ['BBox_CenterX', 'BBox_CenterY', 'BBox_CenterZ']):
            raise ValueError("Bounding box data required. Export with 'bbox' option.")

        fig = plt.figure(figsize=size)
        ax = fig.add_subplot(111, projection='3d')

        # Get unique categories for coloring
        categories = self.elements[color_by].unique()
        colors = plt.cm.tab20(np.linspace(0, 1, len(categories)))
        color_map = dict(zip(categories, colors))

        for cat in categories:
            subset = self.elements[self.elements[color_by] == cat]
            ax.scatter(
                subset['BBox_CenterX'],
                subset['BBox_CenterY'],
                subset['BBox_CenterZ'],
                c=[color_map[cat]],
                label=cat[:20],
                alpha=0.6,
                s=10
            )

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(f'{self.project_name} - 3D Element Distribution')
        ax.legend(loc='upper left', fontsize=8, ncol=2)

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path

    def generate_floor_plan(self, output_path: str, level: str,
                            size: Tuple[int, int] = (14, 10)) -> str:
        """Generate floor plan visualization for specific level."""
        level_elements = self.elements[self.elements['Level'] == level]

        if level_elements.empty:
            raise ValueError(f"No elements found for level: {level}")

        fig, ax = plt.subplots(figsize=size)

        # Draw walls
        walls = level_elements[level_elements['Category'] == 'Walls']
        for _, wall in walls.iterrows():
            rect = plt.Rectangle(
                (wall['BBox_MinX'], wall['BBox_MinY']),
                wall['BBox_MaxX'] - wall['BBox_MinX'],
                wall['BBox_MaxY'] - wall['BBox_MinY'],
                fill=True, facecolor='gray', edgecolor='black', alpha=0.7
            )
            ax.add_patch(rect)

        # Draw rooms
        rooms = level_elements[level_elements['Category'] == 'Rooms']
        for _, room in rooms.iterrows():
            center_x = (room['BBox_MinX'] + room['BBox_MaxX']) / 2
            center_y = (room['BBox_MinY'] + room['BBox_MaxY']) / 2
            ax.annotate(room.get('RoomName', 'Room'),
                       (center_x, center_y), ha='center', fontsize=8)

        ax.set_aspect('equal')
        ax.set_title(f'{self.project_name} - {level}')
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')

        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path

    def generate_category_chart(self, output_path: str,
                                 size: Tuple[int, int] = (12, 8)) -> str:
        """Generate bar chart of element categories."""
        cat_counts = self.elements['Category'].value_counts().head(20)

        fig, ax = plt.subplots(figsize=size)
        bars = ax.barh(cat_counts.index, cat_counts.values,
                       color=plt.cm.viridis(np.linspace(0, 1, len(cat_counts))))

        ax.set_xlabel('Element Count')
        ax.set_title(f'{self.project_name} - Element Categories')

        # Add count labels
        for bar, count in zip(bars, cat_counts.values):
            ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                   f'{count}', va='center', fontsize=9)

        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
        return output_path

    def generate_volume_treemap(self, output_path: str) -> str:
        """Generate treemap of volumes by category."""
        import plotly.express as px

        vol_by_cat = self.elements.groupby('Category')['Volume'].sum().reset_index()
        vol_by_cat = vol_by_cat[vol_by_cat['Volume'] > 0].sort_values('Volume', ascending=False)

        fig = px.treemap(
            vol_by_cat.head(30),
            path=['Category'],
            values='Volume',
            title=f'{self.project_name} - Volume Distribution'
        )

        fig.write_image(output_path)
        return output_path

    def batch_generate(self, xlsx_files: List[str], output_dir: str) -> List[str]:
        """Generate standard visualizations for multiple projects."""
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        generated = []
        for xlsx in xlsx_files:
            try:
                self.load_from_excel(xlsx)
                base_name = Path(xlsx).stem

                # Generate all visualizations
                self.generate_3d_scatter(str(output_dir / f"{base_name}_3d.png"))
                self.generate_category_chart(str(output_dir / f"{base_name}_categories.png"))

                generated.append(base_name)
                print(f"Generated visualizations for: {base_name}")

            except Exception as e:
                print(f"Error processing {xlsx}: {e}")

        return generated
```

## Usage Examples

### Single Project
```python
viz = NoBIMVisualizer()
viz.load_from_excel("C:/Projects/Office.xlsx")

# Generate 3D view
viz.generate_3d_scatter("office_3d.png", color_by="Category")

# Generate floor plan
viz.generate_floor_plan("office_level1.png", level="Level 1")

# Generate category breakdown
viz.generate_category_chart("office_categories.png")
```

### Batch Processing
```python
from pathlib import Path

viz = NoBIMVisualizer()

# Find all converted files
xlsx_files = list(Path("C:/ConvertedProjects").glob("*.xlsx"))

# Generate visualizations for all
generated = viz.batch_generate(
    [str(f) for f in xlsx_files],
    output_dir="C:/Visualizations"
)

print(f"Generated visualizations for {len(generated)} projects")
```

## Output Examples

| Visualization | Use Case |
|---------------|----------|
| 3D Scatter | Overall project structure |
| Floor Plan | Level-by-level layout |
| Category Chart | Element distribution |
| Volume Treemap | Material quantities |
| Level Comparison | Multi-floor analysis |

## Integration with Reporting

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def create_project_report(xlsx_path: str, output_pdf: str):
    """Generate PDF report with all visualizations."""
    viz = NoBIMVisualizer()
    viz.load_from_excel(xlsx_path)

    # Generate images
    images = {
        '3D View': viz.generate_3d_scatter("temp_3d.png"),
        'Categories': viz.generate_category_chart("temp_cat.png"),
    }

    # Create PDF
    c = canvas.Canvas(output_pdf, pagesize=A4)
    c.drawString(100, 800, f"Project Report: {viz.project_name}")

    y_pos = 700
    for title, img_path in images.items():
        c.drawString(100, y_pos, title)
        c.drawImage(img_path, 100, y_pos - 300, width=400, height=280)
        y_pos -= 350

    c.save()
    return output_pdf
```

## Resources

- **GitHub**: [Revit-IFC-Creating-images](https://github.com/datadrivenconstruction/Revit-IFC-Creating-images)
- **Examples**: See repository for Jupyter notebooks

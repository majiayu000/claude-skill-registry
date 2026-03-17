---
name: orcaflex-visualization
description: Generate visualizations from OrcaFlex simulations including model views,
  time series plots, range graphs, and interactive HTML reports using Plotly for
  comprehensive analysis presentation.
version: 1.0.0
updated: 2026-01-17
category: offshore-engineering
triggers:
- visualization
- plot results
- model view
- time series plot
- range graph
- animation
- HTML report
- interactive plot
---
# OrcaFlex Visualization Skill

Generate comprehensive visualizations from OrcaFlex simulations including model views, plots, and interactive HTML reports.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
dependencies:
  orcaflex-modeling: '>=2.0.0,<3.0.0'
  orcaflex-post-processing: '>=1.0.0,<2.0.0'
orcaflex_version: '>=11.0'
compatibility:
  tested_python:
  - '3.10'
  - '3.11'
  - '3.12'
  - '3.13'
  os:
  - Windows
  - Linux
  - macOS
```

## Changelog

### [1.0.0] - 2026-01-17

**Added:**
- Initial release with OPP visualization integration
- Model view image export
- Interactive Plotly plots
- Time series and range graph visualization
- HTML report generation

## When to Use

- Generating model view images for reports
- Creating time series plots of simulation results
- Visualizing range graphs along line arc lengths
- Building interactive HTML dashboards
- Comparing multiple simulations visually
- Animating simulation results

## Visualization Types

### Model Views

| View Type | Description |
|-----------|-------------|
| Plan View | Top-down view (XY plane) |
| Elevation View | Side view (XZ or YZ plane) |
| 3D View | Isometric perspective |
| Object View | Centered on specific object |

### Plot Types

| Plot | Description | Library |
|------|-------------|---------|
| Time Series | Value vs time | Plotly |
| Range Graph | Value vs arc length | Plotly |
| Histogram | Distribution of values | Plotly |
| Polar | Directional responses | Plotly |
| Heatmap | Multi-variable correlation | Plotly |

## Configuration

### Basic Visualization Configuration

```yaml
# configs/visualization_config.yml

visualization:
  # Model views
  views:
    enabled: true
    output_directory: "images/"
    format: "jpg"
    quality: 95

    view_list:
      - name: "plan_view"
        type: "plan"
        width: 1920
        height: 1080

      - name: "elevation_view"
        type: "elevation"
        plane: "XZ"
        width: 1920
        height: 1080

      - name: "3d_view"
        type: "3d"
        azimuth: 45
        elevation: 30
        width: 1920
        height: 1080

  # Time series plots
  time_series:
    enabled: true
    output_directory: "plots/time_series/"
    format: "html"   # Interactive Plotly

    variables:
      - object: "Mooring_Line_1"
        variable: "Effective Tension"
        label: "Line 1 Tension (kN)"

      - object: "Vessel"
        variable: "Heave"
        label: "Vessel Heave (m)"

  # Range graphs
  range_graphs:
    enabled: true
    output_directory: "plots/range_graphs/"

    objects:
      - name: "Riser"
        variables:
          - "Effective Tension"
          - "Curvature"
          - "Bend Moment"

  # HTML report
  report:
    enabled: true
    output_file: "reports/analysis_report.html"
    title: "OrcaFlex Analysis Report"
    include_summary: true
    include_plots: true
    include_tables: true
```

### Advanced Visualization Configuration

```yaml
# configs/visualization_advanced.yml

visualization:
  # View styling
  view_style:
    background_color: "white"
    sea_surface:
      visible: true
      style: "transparent"
      color: [0, 100, 200, 128]  # RGBA
    seabed:
      visible: true
      style: "solid"
      color: [139, 119, 101]
    objects:
      line_width: 2
      vessel_color: [200, 0, 0]

  # Multiple viewpoints
  viewpoints:
    - name: "bow_view"
      centre_on: "Vessel"
      direction: [1, 0, 0]
      distance: 500

    - name: "stern_view"
      centre_on: "Vessel"
      direction: [-1, 0, 0]
      distance: 500

    - name: "touchdown"
      position: [800, 0, -1450]
      target: "Riser"
      arc_length: 1200

  # Plot styling
  plot_style:
    template: "plotly_white"
    font_family: "Arial"
    font_size: 14
    title_font_size: 18
    color_palette: "viridis"

  # Comparison plots
  comparison:
    enabled: true
    simulations:
      - path: "results/baseline.sim"
        label: "Baseline"
        color: "blue"
      - path: "results/modified.sim"
        label: "Modified"
        color: "red"

    variables:
      - object: "Line_1"
        variable: "Effective Tension"
```

## Python API

### Model View Generation

```python
from digitalmodel.orcaflex.opp_visualization import OPPVisualization
from pathlib import Path

def generate_model_views(
    sim_file: str,
    output_dir: str,
    views: list = None
) -> list:
    """
    Generate model view images from simulation.

    Args:
        sim_file: Path to .sim file
        output_dir: Output directory for images
        views: List of view configurations

    Returns:
        List of generated image paths
    """
    visualizer = OPPVisualization()

    # Default views
    if views is None:
        views = [
            {
                "name": "plan",
                "type": "plan",
                "width": 1920,
                "height": 1080
            },
            {
                "name": "elevation",
                "type": "elevation",
                "plane": "XZ",
                "width": 1920,
                "height": 1080
            },
            {
                "name": "3d",
                "type": "3d",
                "azimuth": 45,
                "elevation": 30,
                "width": 1920,
                "height": 1080
            }
        ]

    # Generate views
    image_paths = visualizer.save_views_for_files(
        sim_files=[sim_file],
        output_directory=Path(output_dir),
        view_parameters=views
    )

    return image_paths

# Example usage
images = generate_model_views(
    sim_file="results/mooring_analysis.sim",
    output_dir="images/",
    views=[
        {"name": "overview", "type": "3d", "azimuth": 45, "elevation": 30}
    ]
)

for img in images:
    print(f"Generated: {img}")
```

### Time Series Plotting

```python
import OrcFxAPI
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def plot_time_series(
    sim_file: str,
    variables: list,
    output_file: str = None
) -> go.Figure:
    """
    Create interactive time series plot.

    Args:
        sim_file: Path to .sim file
        variables: List of {object, variable, label}
        output_file: Optional output HTML file

    Returns:
        Plotly figure
    """
    model = OrcFxAPI.Model(sim_file)

    # Create subplots
    fig = make_subplots(
        rows=len(variables),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=[v.get("label", v["variable"]) for v in variables]
    )

    for i, var_config in enumerate(variables, 1):
        obj = model[var_config["object"]]
        var_name = var_config["variable"]

        # Get time history
        times = obj.SampleTimes(period=None)
        values = obj.TimeHistory(var_name, period=None)

        # Add trace
        fig.add_trace(
            go.Scatter(
                x=times,
                y=values,
                name=var_config.get("label", var_name),
                mode="lines",
                line=dict(width=1)
            ),
            row=i,
            col=1
        )

        # Add statistics annotation
        stats_text = f"Max: {max(values):.2f}, Min: {min(values):.2f}, Mean: {sum(values)/len(values):.2f}"
        fig.add_annotation(
            text=stats_text,
            xref=f"x{i}", yref=f"y{i}",
            x=0.02, y=0.98,
            xanchor="left", yanchor="top",
            showarrow=False,
            bgcolor="white",
            row=i, col=1
        )

    # Update layout
    fig.update_layout(
        height=300 * len(variables),
        showlegend=False,
        title="Time Series Analysis"
    )

    fig.update_xaxes(title_text="Time (s)", row=len(variables), col=1)

    # Save if requested
    if output_file:
        fig.write_html(output_file)
        print(f"Saved: {output_file}")

    return fig

# Example usage
variables = [
    {"object": "Mooring_Line_1", "variable": "Effective Tension", "label": "Line 1 Tension (kN)"},
    {"object": "Vessel", "variable": "Heave", "label": "Vessel Heave (m)"},
    {"object": "Vessel", "variable": "Pitch", "label": "Vessel Pitch (deg)"}
]

fig = plot_time_series(
    sim_file="results/analysis.sim",
    variables=variables,
    output_file="plots/time_series.html"
)
```

### Range Graph Plotting

```python
import OrcFxAPI
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def plot_range_graph(
    sim_file: str,
    object_name: str,
    variables: list,
    output_file: str = None
) -> go.Figure:
    """
    Create range graph (min/max/mean vs arc length).

    Args:
        sim_file: Path to .sim file
        object_name: Line object name
        variables: List of variable names
        output_file: Optional output HTML file

    Returns:
        Plotly figure
    """
    model = OrcFxAPI.Model(sim_file)
    obj = model[object_name]

    # Get arc lengths
    arc_lengths = obj.RangeGraphXaxis(period=None)

    # Create subplots
    fig = make_subplots(
        rows=len(variables),
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        subplot_titles=variables
    )

    for i, var_name in enumerate(variables, 1):
        # Get range graph data
        min_values = obj.RangeGraph(var_name, period=None, arclengthRange=None).Min
        max_values = obj.RangeGraph(var_name, period=None, arclengthRange=None).Max
        mean_values = obj.RangeGraph(var_name, period=None, arclengthRange=None).Mean

        # Add traces
        fig.add_trace(
            go.Scatter(
                x=arc_lengths, y=max_values,
                name=f"{var_name} Max",
                line=dict(color="red", width=2),
                legendgroup=f"var{i}"
            ),
            row=i, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=arc_lengths, y=mean_values,
                name=f"{var_name} Mean",
                line=dict(color="green", width=2),
                legendgroup=f"var{i}"
            ),
            row=i, col=1
        )

        fig.add_trace(
            go.Scatter(
                x=arc_lengths, y=min_values,
                name=f"{var_name} Min",
                line=dict(color="blue", width=2),
                legendgroup=f"var{i}"
            ),
            row=i, col=1
        )

        # Fill between min and max
        fig.add_trace(
            go.Scatter(
                x=list(arc_lengths) + list(arc_lengths)[::-1],
                y=list(max_values) + list(min_values)[::-1],
                fill="toself",
                fillcolor="rgba(128,128,128,0.2)",
                line=dict(color="rgba(255,255,255,0)"),
                showlegend=False
            ),
            row=i, col=1
        )

    # Update layout
    fig.update_layout(
        height=350 * len(variables),
        title=f"Range Graph: {object_name}"
    )

    fig.update_xaxes(title_text="Arc Length (m)", row=len(variables), col=1)

    if output_file:
        fig.write_html(output_file)

    return fig

# Example usage
fig = plot_range_graph(
    sim_file="results/riser_analysis.sim",
    object_name="Riser",
    variables=["Effective Tension", "Curvature", "Bend Moment"],
    output_file="plots/riser_range_graph.html"
)
```

### Polar Plot for Directional Analysis

```python
import plotly.graph_objects as go
import numpy as np

def create_polar_plot(
    headings: list,
    values: list,
    title: str = "Directional Response",
    output_file: str = None
) -> go.Figure:
    """
    Create polar plot for directional analysis.

    Args:
        headings: List of heading angles (degrees)
        values: List of response values
        title: Plot title
        output_file: Optional output HTML file

    Returns:
        Plotly figure
    """
    # Close the polar plot
    headings_closed = list(headings) + [headings[0]]
    values_closed = list(values) + [values[0]]

    fig = go.Figure()

    # Add response trace
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=headings_closed,
        mode="lines+markers",
        name="Response",
        line=dict(color="blue", width=2),
        marker=dict(size=8)
    ))

    # Add limit circle if provided
    limit_value = max(values) * 1.1
    fig.add_trace(go.Scatterpolar(
        r=[limit_value] * (len(headings_closed)),
        theta=headings_closed,
        mode="lines",
        name="Limit",
        line=dict(color="red", width=2, dash="dash")
    ))

    fig.update_layout(
        title=title,
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(values) * 1.2]
            ),
            angularaxis=dict(
                direction="clockwise",
                rotation=90  # 0° at top
            )
        ),
        showlegend=True
    )

    if output_file:
        fig.write_html(output_file)

    return fig

# Example: Operability envelope
headings = list(range(0, 360, 15))
max_tensions = [2450, 2380, 2250, 2180, 2120, 2150, 2200, 2280,
                2350, 2400, 2420, 2380, 2320, 2250, 2180, 2120,
                2100, 2150, 2200, 2280, 2350, 2400, 2440, 2450]

fig = create_polar_plot(
    headings=headings,
    values=max_tensions,
    title="Maximum Tension vs Heading",
    output_file="plots/polar_envelope.html"
)
```

### HTML Report Generation

```python
from pathlib import Path
import plotly.graph_objects as go
from datetime import datetime

def generate_html_report(
    title: str,
    sim_file: str,
    figures: list,
    summary_data: dict,
    output_file: str
) -> str:
    """
    Generate comprehensive HTML report.

    Args:
        title: Report title
        sim_file: Source simulation file
        figures: List of Plotly figures
        summary_data: Summary statistics dictionary
        output_file: Output HTML file path

    Returns:
        Path to generated report
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #f5f5f5;
            }}
            h1 {{
                color: #333;
                border-bottom: 2px solid #007bff;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #555;
                margin-top: 30px;
            }}
            .summary-table {{
                border-collapse: collapse;
                width: 100%;
                max-width: 800px;
                margin: 20px 0;
            }}
            .summary-table th, .summary-table td {{
                border: 1px solid #ddd;
                padding: 12px;
                text-align: left;
            }}
            .summary-table th {{
                background-color: #007bff;
                color: white;
            }}
            .summary-table tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .plot-container {{
                background: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }}
            .metadata {{
                color: #777;
                font-size: 0.9em;
                margin-bottom: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <div class="metadata">
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
            <p>Source: {sim_file}</p>
        </div>

        <h2>Summary Statistics</h2>
        <table class="summary-table">
            <tr>
                <th>Parameter</th>
                <th>Value</th>
                <th>Units</th>
            </tr>
    """

    # Add summary rows
    for key, value in summary_data.items():
        if isinstance(value, dict):
            html_content += f"""
            <tr>
                <td>{key}</td>
                <td>{value.get('value', 'N/A')}</td>
                <td>{value.get('units', '')}</td>
            </tr>
            """
        else:
            html_content += f"""
            <tr>
                <td>{key}</td>
                <td>{value}</td>
                <td></td>
            </tr>
            """

    html_content += """
        </table>

        <h2>Analysis Plots</h2>
    """

    # Add plots
    for i, fig in enumerate(figures):
        plot_div = fig.to_html(full_html=False, include_plotlyjs=False)
        html_content += f"""
        <div class="plot-container">
            {plot_div}
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    # Write file
    with open(output_file, "w") as f:
        f.write(html_content)

    return output_file

# Example usage
summary = {
    "Maximum Tension": {"value": 2450.5, "units": "kN"},
    "Maximum Heave": {"value": 5.2, "units": "m"},
    "Simulation Duration": {"value": 10800, "units": "s"},
    "Water Depth": {"value": 1500, "units": "m"}
}

# Create figures
time_fig = plot_time_series(sim_file, variables)
range_fig = plot_range_graph(sim_file, "Riser", ["Effective Tension"])
polar_fig = create_polar_plot(headings, tensions)

# Generate report
report_path = generate_html_report(
    title="Mooring Analysis Report",
    sim_file="results/mooring_analysis.sim",
    figures=[time_fig, range_fig, polar_fig],
    summary_data=summary,
    output_file="reports/analysis_report.html"
)

print(f"Report generated: {report_path}")
```

### Parallel View Generation

```python
from digitalmodel.orcaflex.opp_visualization import OPPVisualization
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

def generate_views_parallel(
    sim_files: list,
    output_dir: str,
    views: list,
    max_workers: int = 4
) -> list:
    """
    Generate model views in parallel.

    Args:
        sim_files: List of .sim file paths
        output_dir: Output directory
        views: View configurations
        max_workers: Parallel workers

    Returns:
        List of all generated image paths
    """
    visualizer = OPPVisualization()

    all_images = visualizer._save_views_parallel(
        sim_files=sim_files,
        output_directory=Path(output_dir),
        view_parameters=views,
        max_workers=max_workers
    )

    return all_images

# Example: Generate views for all simulations
sim_files = list(Path("results/.sim/").glob("*.sim"))

views = [
    {"name": "plan", "type": "plan"},
    {"name": "3d", "type": "3d", "azimuth": 45, "elevation": 30}
]

images = generate_views_parallel(
    sim_files=sim_files,
    output_dir="images/",
    views=views,
    max_workers=4
)

print(f"Generated {len(images)} images")
```

## Output Formats

### Image Outputs

| Format | Extension | Use Case |
|--------|-----------|----------|
| JPEG | .jpg | General purpose, reports |
| PNG | .png | Transparency, high quality |
| SVG | .svg | Scalable, publications |

### Interactive Outputs

| Format | Extension | Features |
|--------|-----------|----------|
| HTML | .html | Hover, zoom, pan, export |
| JSON | .json | Plotly figure data |

## Best Practices

### Model Views

1. **Resolution** - Use 1920x1080 for reports
2. **Consistent views** - Same viewpoint across simulations
3. **Styling** - Consistent colors and backgrounds
4. **Labeling** - Include object labels in views

### Interactive Plots

1. **Plotly** - Use for all web-based visualization
2. **Subplots** - Group related variables
3. **Hover info** - Include key statistics
4. **Export** - Provide download options

### HTML Reports

1. **Structure** - Clear sections and navigation
2. **Summary first** - Key findings up front
3. **Interactive plots** - Embed Plotly figures
4. **Metadata** - Include source and timestamps

## Error Handling

```python
try:
    images = generate_model_views(sim_file, output_dir)
except OrcFxAPI.OrcaFlexError as e:
    print(f"OrcaFlex error: {e}")
    print("Check simulation file is valid")

except FileNotFoundError:
    print("Simulation file not found")
```

## Related Skills

- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Data extraction
- [orcaflex-operability](../orcaflex-operability/SKILL.md) - Envelope visualization
- [orcaflex-results-comparison](../orcaflex-results-comparison/SKILL.md) - Comparison plots
- [orcaflex-extreme-analysis](../orcaflex-extreme-analysis/SKILL.md) - Extreme value plots

## References

- Plotly Python Documentation
- OrcaFlex: Post-Processing Views
- Source: `src/digitalmodel/modules/orcaflex/opp_visualization.py`
- Source: `src/digitalmodel/solvers/orcaflex/post_results/postProcessPlotting.py`

---
name: chart-generator
description: Generate charts and visualizations from data using various charting libraries and formats.
---

# Chart Generator Skill

Generate charts and visualizations from data using various charting libraries and formats.

## Instructions

You are a data visualization expert. When invoked:

1. **Analyze Data**:
   - Understand data structure and types
   - Identify appropriate chart types
   - Detect data patterns and trends
   - Calculate aggregations and statistics
   - Determine visualization goals

2. **Generate Charts**:
   - Create bar, line, pie, scatter plots
   - Generate heatmaps and tree maps
   - Create histograms and box plots
   - Build time series visualizations
   - Design multi-dimensional charts

3. **Style and Customize**:
   - Apply color schemes and themes
   - Add labels, legends, and annotations
   - Format axes and gridlines
   - Customize tooltips and interactions
   - Ensure accessibility and readability

4. **Export and Embed**:
   - Save as PNG, SVG, PDF
   - Generate interactive HTML charts
   - Embed in markdown reports
   - Create chart APIs
   - Support responsive design

## Usage Examples

```
@chart-generator data.csv --type bar
@chart-generator --line --time-series
@chart-generator --pie --group-by category
@chart-generator --scatter x:age y:income
@chart-generator --heatmap --correlation
@chart-generator --interactive --html
```

## Chart Types and Use Cases

### When to Use Each Chart Type

| Chart Type | Best For | Example Use Case |
|------------|----------|------------------|
| Bar Chart | Comparing categories | Sales by product |
| Line Chart | Trends over time | Revenue over months |
| Pie Chart | Part-to-whole relationships | Market share |
| Scatter Plot | Relationships between variables | Height vs Weight |
| Histogram | Distribution of values | Age distribution |
| Box Plot | Statistical distribution | Salary ranges by department |
| Heatmap | Matrix data, correlations | Feature correlations |
| Area Chart | Cumulative trends | Stacked revenue streams |
| Bubble Chart | 3-dimensional data | Sales vs Profit vs Market Share |
| Treemap | Hierarchical data | Disk space usage |

## Python - Matplotlib

```python
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def create_bar_chart(data, x_col, y_col, title='Bar Chart', output='chart.png'):
    """
    Create a bar chart
    """
    plt.figure(figsize=(10, 6))

    if isinstance(data, pd.DataFrame):
        x = data[x_col]
        y = data[y_col]
    else:
        x = data['labels']
        y = data['values']

    bars = plt.bar(x, y, color='steelblue', alpha=0.8)

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_col if isinstance(data, pd.DataFrame) else 'Category', fontsize=12)
    plt.ylabel(y_col if isinstance(data, pd.DataFrame) else 'Value', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

def create_line_chart(data, x_col, y_col, title='Line Chart', output='chart.png'):
    """
    Create a line chart
    """
    plt.figure(figsize=(12, 6))

    if isinstance(data, pd.DataFrame):
        x = data[x_col]
        y = data[y_col]
    else:
        x = data['x']
        y = data['y']

    plt.plot(x, y, marker='o', linewidth=2, markersize=6, color='steelblue')

    # Add grid
    plt.grid(True, alpha=0.3)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_col if isinstance(data, pd.DataFrame) else 'X', fontsize=12)
    plt.ylabel(y_col if isinstance(data, pd.DataFrame) else 'Y', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

def create_pie_chart(data, labels_col, values_col, title='Pie Chart', output='chart.png'):
    """
    Create a pie chart
    """
    plt.figure(figsize=(10, 8))

    if isinstance(data, pd.DataFrame):
        labels = data[labels_col]
        values = data[values_col]
    else:
        labels = data['labels']
        values = data['values']

    # Create color palette
    colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

    # Create pie chart
    wedges, texts, autotexts = plt.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        startangle=90,
        colors=colors,
        explode=[0.05] * len(labels)  # Slightly separate slices
    )

    # Style percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(10)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

def create_scatter_plot(data, x_col, y_col, color_col=None, size_col=None,
                       title='Scatter Plot', output='chart.png'):
    """
    Create a scatter plot
    """
    plt.figure(figsize=(10, 8))

    if isinstance(data, pd.DataFrame):
        x = data[x_col]
        y = data[y_col]
        c = data[color_col] if color_col else None
        s = data[size_col] if size_col else 50
    else:
        x = data['x']
        y = data['y']
        c = None
        s = 50

    scatter = plt.scatter(x, y, c=c, s=s, alpha=0.6, cmap='viridis')

    if color_col:
        plt.colorbar(scatter, label=color_col)

    # Add trend line
    z = np.polyfit(x, y, 1)
    p = np.poly1d(z)
    plt.plot(x, p(x), "r--", alpha=0.8, label='Trend')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(x_col if isinstance(data, pd.DataFrame) else 'X', fontsize=12)
    plt.ylabel(y_col if isinstance(data, pd.DataFrame) else 'Y', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

def create_histogram(data, column, bins=30, title='Histogram', output='chart.png'):
    """
    Create a histogram
    """
    plt.figure(figsize=(10, 6))

    if isinstance(data, pd.DataFrame):
        values = data[column]
    else:
        values = data

    n, bins, patches = plt.hist(values, bins=bins, color='steelblue',
                                 alpha=0.7, edgecolor='black')

    # Add mean line
    mean_val = np.mean(values)
    plt.axvline(mean_val, color='red', linestyle='dashed', linewidth=2,
                label=f'Mean: {mean_val:.2f}')

    # Add median line
    median_val = np.median(values)
    plt.axvline(median_val, color='green', linestyle='dashed', linewidth=2,
                label=f'Median: {median_val:.2f}')

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xlabel(column if isinstance(data, pd.DataFrame) else 'Value', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

def create_box_plot(data, columns, title='Box Plot', output='chart.png'):
    """
    Create a box plot
    """
    plt.figure(figsize=(10, 6))

    if isinstance(data, pd.DataFrame):
        data_to_plot = [data[col].dropna() for col in columns]
        labels = columns
    else:
        data_to_plot = data
        labels = [f'Group {i+1}' for i in range(len(data))]

    bp = plt.boxplot(data_to_plot, labels=labels, patch_artist=True)

    # Color boxes
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
        patch.set_alpha(0.7)

    plt.title(title, fontsize=16, fontweight='bold')
    plt.ylabel('Value', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

def create_heatmap(data, title='Heatmap', output='chart.png'):
    """
    Create a heatmap (correlation matrix)
    """
    plt.figure(figsize=(10, 8))

    if isinstance(data, pd.DataFrame):
        # Calculate correlation matrix
        corr_matrix = data.corr()
    else:
        corr_matrix = data

    # Create heatmap
    im = plt.imshow(corr_matrix, cmap='coolwarm', aspect='auto',
                    vmin=-1, vmax=1)

    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Correlation', rotation=270, labelpad=20)

    # Set ticks and labels
    plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns,
               rotation=45, ha='right')
    plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)

    # Add correlation values
    for i in range(len(corr_matrix)):
        for j in range(len(corr_matrix.columns)):
            text = plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                          ha='center', va='center', color='black', fontsize=9)

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output
```

## Python - Seaborn

```python
import seaborn as sns

def create_seaborn_chart(data, chart_type, x, y=None, hue=None,
                        title='Chart', output='chart.png'):
    """
    Create charts using Seaborn
    """
    plt.figure(figsize=(12, 6))

    # Set style
    sns.set_style("whitegrid")
    sns.set_palette("husl")

    if chart_type == 'bar':
        sns.barplot(data=data, x=x, y=y, hue=hue)

    elif chart_type == 'line':
        sns.lineplot(data=data, x=x, y=y, hue=hue, marker='o')

    elif chart_type == 'scatter':
        sns.scatterplot(data=data, x=x, y=y, hue=hue, size=hue, alpha=0.6)

    elif chart_type == 'box':
        sns.boxplot(data=data, x=x, y=y, hue=hue)

    elif chart_type == 'violin':
        sns.violinplot(data=data, x=x, y=y, hue=hue)

    elif chart_type == 'dist':
        sns.histplot(data=data, x=x, hue=hue, kde=True)

    elif chart_type == 'heatmap':
        sns.heatmap(data.corr(), annot=True, fmt='.2f', cmap='coolwarm',
                   center=0, square=True, linewidths=1)

    elif chart_type == 'pairplot':
        # Special case - creates its own figure
        g = sns.pairplot(data, hue=hue)
        g.savefig(output, dpi=300, bbox_inches='tight')
        return output

    plt.title(title, fontsize=16, fontweight='bold')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output

# Advanced Seaborn visualizations
def create_facet_grid(data, x, y, col=None, row=None, hue=None,
                     title='Facet Grid', output='chart.png'):
    """
    Create faceted charts
    """
    g = sns.FacetGrid(data, col=col, row=row, hue=hue, height=4)
    g.map(sns.scatterplot, x, y, alpha=0.6)
    g.add_legend()
    g.fig.suptitle(title, y=1.02, fontsize=16, fontweight='bold')

    plt.savefig(output, dpi=300, bbox_inches='tight')
    plt.close()

    return output
```

## JavaScript - Chart.js

```javascript
const { ChartJSNodeCanvas } = require('chartjs-node-canvas');

async function createBarChart(data, options = {}) {
  const width = options.width || 800;
  const height = options.height || 600;

  const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

  const configuration = {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: options.label || 'Dataset',
        data: data.values,
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
        borderColor: 'rgba(54, 162, 235, 1)',
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: options.title || 'Bar Chart',
          font: { size: 18 }
        },
        legend: {
          display: true,
          position: 'top'
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };

  const imageBuffer = await chartJSNodeCanvas.renderToBuffer(configuration);
  return imageBuffer;
}

async function createLineChart(data, options = {}) {
  const width = options.width || 800;
  const height = options.height || 600;

  const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

  const configuration = {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: options.label || 'Dataset',
        data: data.values,
        borderColor: 'rgba(75, 192, 192, 1)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        borderWidth: 2,
        tension: 0.4
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: options.title || 'Line Chart',
          font: { size: 18 }
        }
      },
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  };

  const imageBuffer = await chartJSNodeCanvas.renderToBuffer(configuration);
  return imageBuffer;
}

async function createPieChart(data, options = {}) {
  const width = options.width || 800;
  const height = options.height || 600;

  const chartJSNodeCanvas = new ChartJSNodeCanvas({ width, height });

  const configuration = {
    type: 'pie',
    data: {
      labels: data.labels,
      datasets: [{
        data: data.values,
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(153, 102, 255, 0.6)',
          'rgba(255, 159, 64, 0.6)'
        ],
        borderWidth: 2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: options.title || 'Pie Chart',
          font: { size: 18 }
        },
        legend: {
          position: 'right'
        }
      }
    }
  };

  const imageBuffer = await chartJSNodeCanvas.renderToBuffer(configuration);
  return imageBuffer;
}
```

## Interactive Charts - Plotly

```python
import plotly.express as px
import plotly.graph_objects as go

def create_interactive_bar(data, x, y, title='Bar Chart', output='chart.html'):
    """
    Create interactive bar chart with Plotly
    """
    fig = px.bar(data, x=x, y=y, title=title,
                 color=y, color_continuous_scale='Viridis')

    fig.update_layout(
        font=dict(size=14),
        showlegend=True,
        hovermode='x unified'
    )

    fig.write_html(output)
    return output

def create_interactive_line(data, x, y, title='Line Chart', output='chart.html'):
    """
    Create interactive line chart
    """
    fig = px.line(data, x=x, y=y, title=title, markers=True)

    fig.update_traces(line=dict(width=3))

    fig.update_layout(
        hovermode='x unified',
        font=dict(size=14)
    )

    fig.write_html(output)
    return output

def create_interactive_scatter(data, x, y, color=None, size=None,
                              title='Scatter Plot', output='chart.html'):
    """
    Create interactive scatter plot
    """
    fig = px.scatter(data, x=x, y=y, color=color, size=size,
                    title=title, hover_data=data.columns)

    fig.update_traces(marker=dict(line=dict(width=0.5, color='white')))

    fig.write_html(output)
    return output

def create_3d_scatter(data, x, y, z, color=None, title='3D Scatter',
                     output='chart.html'):
    """
    Create 3D scatter plot
    """
    fig = px.scatter_3d(data, x=x, y=y, z=z, color=color, title=title)

    fig.update_layout(scene=dict(
        xaxis_title=x,
        yaxis_title=y,
        zaxis_title=z
    ))

    fig.write_html(output)
    return output

def create_time_series(data, date_col, value_col, title='Time Series',
                      output='chart.html'):
    """
    Create time series chart
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data[date_col],
        y=data[value_col],
        mode='lines+markers',
        name=value_col,
        line=dict(width=2),
        marker=dict(size=6)
    ))

    # Add range slider
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=7, label="1w", step="day", stepmode="backward"),
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=3, label="3m", step="month", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title=date_col,
        yaxis_title=value_col,
        font=dict(size=14)
    )

    fig.write_html(output)
    return output

def create_dashboard(data, output='dashboard.html'):
    """
    Create multi-chart dashboard
    """
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Bar Chart', 'Line Chart', 'Pie Chart', 'Scatter Plot'),
        specs=[[{'type': 'bar'}, {'type': 'scatter'}],
               [{'type': 'pie'}, {'type': 'scatter'}]]
    )

    # Add charts
    # Bar chart
    fig.add_trace(
        go.Bar(x=data['category'], y=data['value1'], name='Bar'),
        row=1, col=1
    )

    # Line chart
    fig.add_trace(
        go.Scatter(x=data['date'], y=data['value2'], mode='lines', name='Line'),
        row=1, col=2
    )

    # Pie chart
    fig.add_trace(
        go.Pie(labels=data['category'], values=data['value1'], name='Pie'),
        row=2, col=1
    )

    # Scatter plot
    fig.add_trace(
        go.Scatter(x=data['value1'], y=data['value2'], mode='markers', name='Scatter'),
        row=2, col=2
    )

    fig.update_layout(height=800, showlegend=True, title_text="Dashboard")

    fig.write_html(output)
    return output
```

## Chart Styling and Themes

```python
# Matplotlib themes
def apply_matplotlib_theme(theme='default'):
    """
    Apply theme to matplotlib charts
    """
    themes = {
        'default': 'seaborn-v0_8-darkgrid',
        'minimal': 'seaborn-v0_8-whitegrid',
        'dark': 'dark_background',
        'classic': 'classic',
        'ggplot': 'ggplot'
    }

    plt.style.use(themes.get(theme, 'default'))

# Custom color palettes
COLOR_PALETTES = {
    'corporate': ['#003f5c', '#58508d', '#bc5090', '#ff6361', '#ffa600'],
    'pastel': ['#a8e6cf', '#dcedc1', '#ffd3b6', '#ffaaa5', '#ff8b94'],
    'vibrant': ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'],
    'monochrome': ['#2c3e50', '#34495e', '#7f8c8d', '#95a5a6', '#bdc3c7']
}

def apply_color_palette(palette_name='corporate'):
    """Apply custom color palette"""
    colors = COLOR_PALETTES.get(palette_name, COLOR_PALETTES['corporate'])
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=colors)
```

## Export Formats

```python
def export_chart_multiple_formats(fig, base_name='chart'):
    """
    Export chart in multiple formats
    """
    formats = {
        'png': {'dpi': 300, 'transparent': False},
        'svg': {'format': 'svg'},
        'pdf': {'format': 'pdf'},
        'jpg': {'dpi': 300, 'format': 'jpg'}
    }

    files = []

    for fmt, kwargs in formats.items():
        output_file = f"{base_name}.{fmt}"
        fig.savefig(output_file, bbox_inches='tight', **kwargs)
        files.append(output_file)

    return files
```

## Chart Generation Pipeline

```python
def generate_charts_from_data(data, chart_configs, output_dir='charts'):
    """
    Generate multiple charts from data based on configurations

    chart_configs = [
        {
            'type': 'bar',
            'x': 'category',
            'y': 'value',
            'title': 'Sales by Category',
            'output': 'sales_bar.png'
        },
        ...
    ]
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    generated_charts = []

    for config in chart_configs:
        chart_type = config['type']
        output = os.path.join(output_dir, config['output'])

        if chart_type == 'bar':
            create_bar_chart(data, config['x'], config['y'],
                           config.get('title', 'Chart'), output)

        elif chart_type == 'line':
            create_line_chart(data, config['x'], config['y'],
                            config.get('title', 'Chart'), output)

        elif chart_type == 'pie':
            create_pie_chart(data, config['x'], config['y'],
                           config.get('title', 'Chart'), output)

        elif chart_type == 'scatter':
            create_scatter_plot(data, config['x'], config['y'],
                              config.get('color'), config.get('size'),
                              config.get('title', 'Chart'), output)

        elif chart_type == 'heatmap':
            create_heatmap(data, config.get('title', 'Chart'), output)

        generated_charts.append({
            'type': chart_type,
            'title': config.get('title'),
            'file': output
        })

    return generated_charts
```

## Best Practices

1. **Choose appropriate chart types** for your data
2. **Use clear, descriptive titles** and labels
3. **Apply consistent color schemes** across charts
4. **Ensure readability** (font sizes, contrast)
5. **Add context** (annotations, reference lines)
6. **Export in high resolution** (300 DPI minimum)
7. **Consider accessibility** (color-blind friendly palettes)
8. **Test on different screen sizes** (responsive design)
9. **Optimize file sizes** for web use
10. **Document chart generation** code for reproducibility

## Common Chart Patterns

### Comparison Charts
- Bar charts for categorical comparisons
- Grouped bar charts for multi-series comparison
- Stacked bar charts for part-to-whole comparisons

### Trend Charts
- Line charts for time series
- Area charts for cumulative trends
- Sparklines for inline trends

### Distribution Charts
- Histograms for frequency distribution
- Box plots for statistical distribution
- Violin plots for distribution shape

### Relationship Charts
- Scatter plots for correlations
- Bubble charts for 3D relationships
- Heatmaps for matrix relationships

### Composition Charts
- Pie charts for simple part-to-whole
- Stacked area charts for trends over time
- Treemaps for hierarchical composition

## Notes

- Always label axes and provide units
- Use appropriate scales (linear, logarithmic)
- Consider data-ink ratio (minimize chart junk)
- Test charts with different data ranges
- Provide legends when using multiple series
- Use annotations to highlight key insights
- Export charts in vector formats for publications
- Keep color schemes consistent across related charts
- Consider cultural differences in color meanings
- Validate data before visualization

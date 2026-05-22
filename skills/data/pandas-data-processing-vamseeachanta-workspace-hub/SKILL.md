---
name: pandas-data-processing
version: 1.0.0
description: Pandas for time series analysis, OrcaFlex results processing, and marine engineering data workflows
author: workspace-hub
category: programming
tags: [pandas, data-processing, time-series, csv, engineering, orcaflex]
platforms: [python]
---

# Pandas Data Processing Skill

Master Pandas for time series analysis, OrcaFlex results processing, and configuration-driven data workflows in marine and offshore engineering.

## When to Use This Skill

Use Pandas data processing when you need:
- **Time series analysis** - Wave elevation, vessel motions, mooring tensions
- **OrcaFlex results** - Load simulation results, process RAOs, analyze dynamics
- **Multi-format data** - CSV, Excel, HDF5, Parquet for large datasets
- **Statistical analysis** - Summary statistics, rolling windows, resampling
- **Data transformation** - Pivot, melt, merge, group operations
- **Engineering reports** - Automated data extraction and summary generation

**Avoid when:**
- Real-time streaming data (use Polars or streaming libraries)
- Extremely large datasets (>100GB) - use Dask, Vaex, or PySpark
- Pure numerical computation (use NumPy directly)
- Graph/network data (use NetworkX)

## Core Capabilities

### 1. Time Series Analysis

**Load and Process Time Series:**
```python
import pandas as pd
import numpy as np
from pathlib import Path

def load_orcaflex_time_series(
    csv_file: Path,
    time_column: str = 'Time',
    parse_dates: bool = True
) -> pd.DataFrame:
    """
    Load OrcaFlex time series results from CSV.

    Args:
        csv_file: Path to CSV file
        time_column: Name of time column
        parse_dates: Whether to parse time column as datetime

    Returns:
        DataFrame with time as index
    """
    # Load CSV
    df = pd.read_csv(csv_file)

    # Set time as index
    if parse_dates:
        df[time_column] = pd.to_datetime(df[time_column], unit='s')

    df.set_index(time_column, inplace=True)

    return df

# Usage
results = load_orcaflex_time_series(
    Path('data/processed/vessel_motions.csv')
)

print(f"Time range: {results.index[0]} to {results.index[-1]}")
print(f"Duration: {(results.index[-1] - results.index[0]).total_seconds()} seconds")
print(f"Sampling rate: {1 / results.index.to_series().diff().mean().total_seconds():.2f} Hz")
```

**Resampling and Aggregation:**
```python
def resample_time_series(
    df: pd.DataFrame,
    target_frequency: str = '1S',
    method: str = 'mean'
) -> pd.DataFrame:
    """
    Resample time series to target frequency.

    Args:
        df: Input DataFrame with datetime index
        target_frequency: Target frequency ('1S', '0.1S', '1min', etc.)
        method: Aggregation method ('mean', 'max', 'min', 'std')

    Returns:
        Resampled DataFrame
    """
    # Resample
    if method == 'mean':
        resampled = df.resample(target_frequency).mean()
    elif method == 'max':
        resampled = df.resample(target_frequency).max()
    elif method == 'min':
        resampled = df.resample(target_frequency).min()
    elif method == 'std':
        resampled = df.resample(target_frequency).std()
    else:
        raise ValueError(f"Unknown method: {method}")

    # Fill NaN values (forward fill)
    resampled.fillna(method='ffill', inplace=True)

    return resampled

# Example: Downsample from 0.05s to 1s
high_freq_data = load_orcaflex_time_series(
    Path('data/processed/mooring_tension_0.05s.csv')
)

low_freq_data = resample_time_series(
    high_freq_data,
    target_frequency='1S',
    method='mean'
)

print(f"Original points: {len(high_freq_data)}")
print(f"Resampled points: {len(low_freq_data)}")
```

**Rolling Statistics:**
```python
def calculate_rolling_statistics(
    df: pd.DataFrame,
    column: str,
    window: str = '60S'
) -> pd.DataFrame:
    """
    Calculate rolling statistics for time series.

    Args:
        df: Input DataFrame with datetime index
        column: Column name to analyze
        window: Rolling window size (time-based)

    Returns:
        DataFrame with rolling statistics
    """
    stats = pd.DataFrame(index=df.index)

    # Rolling calculations
    rolling = df[column].rolling(window=window)

    stats[f'{column}_mean'] = rolling.mean()
    stats[f'{column}_std'] = rolling.std()
    stats[f'{column}_max'] = rolling.max()
    stats[f'{column}_min'] = rolling.min()

    return stats

# Example: 60-second rolling statistics
tension_stats = calculate_rolling_statistics(
    results,
    column='Tension_Line1',
    window='60S'
)

# Plot rolling mean and standard deviation
import plotly.graph_objects as go

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=results.index,
    y=results['Tension_Line1'],
    name='Raw Tension',
    opacity=0.3
))
fig.add_trace(go.Scatter(
    x=tension_stats.index,
    y=tension_stats['Tension_Line1_mean'],
    name='60s Rolling Mean',
    line=dict(width=3)
))

fig.update_layout(
    title='Mooring Tension: Raw vs Rolling Mean',
    xaxis_title='Time',
    yaxis_title='Tension (kN)'
)
fig.write_html('reports/tension_rolling_mean.html')
```

### 2. Statistical Analysis

**Summary Statistics:**
```python
def generate_statistical_summary(
    df: pd.DataFrame,
    columns: list = None
) -> pd.DataFrame:
    """
    Generate comprehensive statistical summary.

    Args:
        df: Input DataFrame
        columns: Columns to analyze (None = all numeric)

    Returns:
        DataFrame with statistical metrics
    """
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # Standard statistics
    summary = df[columns].describe()

    # Additional statistics
    additional_stats = pd.DataFrame({
        'median': df[columns].median(),
        'skewness': df[columns].skew(),
        'kurtosis': df[columns].kurtosis(),
        'variance': df[columns].var()
    }).T

    # Combine
    full_summary = pd.concat([summary, additional_stats])

    return full_summary

# Example
motion_stats = generate_statistical_summary(
    results,
    columns=['Surge', 'Sway', 'Heave', 'Roll', 'Pitch', 'Yaw']
)

print(motion_stats)

# Export to CSV
motion_stats.to_csv('reports/motion_statistics.csv')
```

**Extreme Value Analysis:**
```python
def extract_extreme_values(
    df: pd.DataFrame,
    column: str,
    n_extremes: int = 10,
    extreme_type: str = 'max'
) -> pd.DataFrame:
    """
    Extract extreme values (max or min) from time series.

    Args:
        df: Input DataFrame with datetime index
        column: Column to analyze
        n_extremes: Number of extreme values to extract
        extreme_type: 'max' or 'min'

    Returns:
        DataFrame with extreme events
    """
    if extreme_type == 'max':
        extremes = df.nlargest(n_extremes, column)
    elif extreme_type == 'min':
        extremes = df.nsmallest(n_extremes, column)
    else:
        raise ValueError("extreme_type must be 'max' or 'min'")

    # Sort by time
    extremes = extremes.sort_index()

    return extremes

# Example: Top 10 maximum tensions
max_tensions = extract_extreme_values(
    results,
    column='Tension_Line1',
    n_extremes=10,
    extreme_type='max'
)

print("Top 10 Maximum Tensions:")
print(max_tensions[['Tension_Line1']])
```

### 3. Data Transformation

**Pivot Operations:**
```python
def pivot_mooring_data(
    df: pd.DataFrame,
    index: str = 'Time',
    columns: str = 'LineID',
    values: str = 'Tension'
) -> pd.DataFrame:
    """
    Pivot long-format mooring data to wide format.

    Args:
        df: Input DataFrame in long format
        index: Index column (usually time)
        columns: Column to pivot (usually line identifier)
        values: Value column (tension, angle, etc.)

    Returns:
        Pivoted DataFrame
    """
    pivoted = df.pivot(
        index=index,
        columns=columns,
        values=values
    )

    # Rename columns
    pivoted.columns = [f'{values}_Line{col}' for col in pivoted.columns]

    return pivoted

# Example: Convert long format to wide format
# Long format:
#   Time  LineID  Tension
#   0.0   1       1500
#   0.0   2       1520
#   0.1   1       1505
#   0.1   2       1525

long_format = pd.DataFrame({
    'Time': [0.0, 0.0, 0.1, 0.1, 0.2, 0.2],
    'LineID': [1, 2, 1, 2, 1, 2],
    'Tension': [1500, 1520, 1505, 1525, 1510, 1530]
})

wide_format = pivot_mooring_data(long_format)
print(wide_format)
# Output:
#       Tension_Line1  Tension_Line2
# Time
# 0.0   1500           1520
# 0.1   1505           1525
# 0.2   1510           1530
```

**Melt Operations:**
```python
def melt_wide_format(
    df: pd.DataFrame,
    id_vars: list = None,
    value_name: str = 'Value',
    var_name: str = 'Parameter'
) -> pd.DataFrame:
    """
    Convert wide-format data to long format.

    Args:
        df: Input DataFrame in wide format
        id_vars: Identifier variables to preserve
        value_name: Name for value column
        var_name: Name for variable column

    Returns:
        Melted DataFrame
    """
    if id_vars is None:
        id_vars = [df.index.name or 'index']
        df_reset = df.reset_index()
    else:
        df_reset = df

    melted = pd.melt(
        df_reset,
        id_vars=id_vars,
        value_name=value_name,
        var_name=var_name
    )

    return melted

# Example: Convert multi-column tensions to long format
wide_data = pd.DataFrame({
    'Time': [0.0, 0.1, 0.2],
    'Tension_Line1': [1500, 1505, 1510],
    'Tension_Line2': [1520, 1525, 1530],
    'Tension_Line3': [1480, 1485, 1490]
})

long_data = melt_wide_format(
    wide_data,
    id_vars=['Time'],
    value_name='Tension',
    var_name='Line'
)

print(long_data)
# Output:
#   Time  Line            Tension
#   0.0   Tension_Line1   1500
#   0.0   Tension_Line2   1520
#   0.0   Tension_Line3   1480
#   ...
```

### 4. Multi-File Processing

**Batch CSV Loading:**
```python
def load_multiple_csv_files(
    directory: Path,
    pattern: str = '*.csv',
    concat_axis: int = 0
) -> pd.DataFrame:
    """
    Load and concatenate multiple CSV files.

    Args:
        directory: Directory containing CSV files
        pattern: Glob pattern for file matching
        concat_axis: Concatenation axis (0=rows, 1=columns)

    Returns:
        Concatenated DataFrame
    """
    csv_files = sorted(directory.glob(pattern))

    if not csv_files:
        raise FileNotFoundError(f"No CSV files found matching {pattern} in {directory}")

    # Load all files
    dfs = []
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        df['source_file'] = csv_file.name  # Track source
        dfs.append(df)

    # Concatenate
    combined = pd.concat(dfs, axis=concat_axis, ignore_index=True)

    print(f"Loaded {len(csv_files)} files, total {len(combined)} rows")

    return combined

# Example: Load all mooring tension results
all_tensions = load_multiple_csv_files(
    Path('data/processed/mooring_tensions/'),
    pattern='tension_line*.csv'
)

print(f"Combined dataset: {all_tensions.shape}")
```

**Multi-Format Data Loading:**
```python
def load_engineering_data(
    file_path: Path,
    file_type: str = None
) -> pd.DataFrame:
    """
    Load data from multiple engineering file formats.

    Args:
        file_path: Path to data file
        file_type: File type ('csv', 'excel', 'hdf5', 'parquet', 'json')
                   If None, inferred from extension

    Returns:
        Loaded DataFrame
    """
    if file_type is None:
        file_type = file_path.suffix.lstrip('.')

    # Load based on type
    if file_type == 'csv':
        df = pd.read_csv(file_path)
    elif file_type in ['xls', 'xlsx', 'excel']:
        df = pd.read_excel(file_path)
    elif file_type in ['h5', 'hdf5']:
        df = pd.read_hdf(file_path)
    elif file_type == 'parquet':
        df = pd.read_parquet(file_path)
    elif file_type == 'json':
        df = pd.read_json(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_type}")

    print(f"Loaded {file_type.upper()}: {df.shape[0]} rows, {df.shape[1]} columns")

    return df

# Usage examples
csv_data = load_engineering_data(Path('data/processed/results.csv'))
excel_data = load_engineering_data(Path('data/processed/summary.xlsx'))
hdf5_data = load_engineering_data(Path('data/processed/large_dataset.h5'))
```

### 5. GroupBy Operations

**Group and Aggregate:**
```python
def group_by_sea_state(
    df: pd.DataFrame,
    hs_column: str = 'Hs',
    tp_column: str = 'Tp',
    hs_bins: list = None,
    tp_bins: list = None
) -> pd.DataFrame:
    """
    Group results by sea state (Hs, Tp bins).

    Args:
        df: Input DataFrame with sea state parameters
        hs_column: Column name for significant wave height
        tp_column: Column name for peak period
        hs_bins: Bins for Hs [0, 2, 4, 6, 8, 10]
        tp_bins: Bins for Tp [0, 6, 8, 10, 12, 14]

    Returns:
        Grouped statistics by sea state
    """
    if hs_bins is None:
        hs_bins = [0, 2, 4, 6, 8, 10, 12]
    if tp_bins is None:
        tp_bins = [0, 6, 8, 10, 12, 14, 16]

    # Create bins
    df['Hs_bin'] = pd.cut(df[hs_column], bins=hs_bins)
    df['Tp_bin'] = pd.cut(df[tp_column], bins=tp_bins)

    # Group and aggregate
    grouped = df.groupby(['Hs_bin', 'Tp_bin']).agg({
        'Tension_Max': ['mean', 'std', 'max'],
        'Motion_Max': ['mean', 'std', 'max'],
        'Offset_Max': ['mean', 'std', 'max']
    })

    return grouped

# Example
sea_state_results = pd.DataFrame({
    'Hs': [2.5, 3.0, 4.5, 5.0, 6.5, 7.0],
    'Tp': [7.0, 8.5, 9.0, 10.5, 11.0, 12.5],
    'Tension_Max': [1500, 1600, 1800, 2000, 2200, 2400],
    'Motion_Max': [2.0, 2.5, 3.0, 3.5, 4.0, 4.5],
    'Offset_Max': [50, 60, 70, 80, 90, 100]
})

grouped_stats = group_by_sea_state(sea_state_results)
print(grouped_stats)
```

**Multi-Level Grouping:**
```python
def analyze_by_loadcase_and_direction(
    df: pd.DataFrame,
    group_columns: list = ['LoadCase', 'Direction'],
    value_columns: list = None
) -> pd.DataFrame:
    """
    Analyze results grouped by load case and direction.

    Args:
        df: Input DataFrame
        group_columns: Columns to group by
        value_columns: Columns to aggregate (None = all numeric)

    Returns:
        Multi-level grouped statistics
    """
    if value_columns is None:
        value_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    # Group and calculate statistics
    grouped = df.groupby(group_columns)[value_columns].agg([
        'count', 'mean', 'std', 'min', 'max'
    ])

    return grouped

# Example
load_case_data = pd.DataFrame({
    'LoadCase': ['Operating', 'Operating', 'Storm', 'Storm', 'Extreme', 'Extreme'],
    'Direction': [0, 45, 0, 45, 0, 45],
    'Tension': [1500, 1520, 2000, 2050, 2500, 2600],
    'Offset': [50, 55, 75, 80, 100, 110]
})

stats_by_case = analyze_by_loadcase_and_direction(load_case_data)
print(stats_by_case)
```

## Complete Examples

### Example 1: OrcaFlex Results Processing

```python
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.graph_objects as go

def process_orcaflex_results(
    results_dir: Path,
    output_dir: Path
) -> dict:
    """
    Complete OrcaFlex results processing pipeline.

    Process time series results, calculate statistics,
    generate reports, and create visualizations.

    Args:
        results_dir: Directory with OrcaFlex CSV results
        output_dir: Directory for processed results

    Returns:
        Dictionary with processing summary
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load vessel motions
    motions = pd.read_csv(results_dir / 'vessel_motions.csv')
    motions['Time'] = pd.to_datetime(motions['Time'], unit='s')
    motions.set_index('Time', inplace=True)

    # 2. Load mooring tensions
    tensions = pd.read_csv(results_dir / 'mooring_tensions.csv')
    tensions['Time'] = pd.to_datetime(tensions['Time'], unit='s')
    tensions.set_index('Time', inplace=True)

    # 3. Calculate statistics
    motion_stats = motions.describe()
    tension_stats = tensions.describe()

    # 4. Identify extreme events
    max_heave = motions['Heave'].idxmax()
    max_tension = tensions.max(axis=1).idxmax()

    # 5. Create summary report
    summary = {
        'motion_statistics': motion_stats,
        'tension_statistics': tension_stats,
        'max_heave_time': max_heave,
        'max_heave_value': motions.loc[max_heave, 'Heave'],
        'max_tension_time': max_tension,
        'max_tension_value': tensions.loc[max_tension].max(),
        'duration_seconds': (motions.index[-1] - motions.index[0]).total_seconds()
    }

    # 6. Export processed data
    motion_stats.to_csv(output_dir / 'motion_statistics.csv')
    tension_stats.to_csv(output_dir / 'tension_statistics.csv')

    # 7. Create time series plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=motions.index,
        y=motions['Heave'],
        name='Heave',
        line=dict(color='blue')
    ))

    fig.add_trace(go.Scatter(
        x=tensions.index,
        y=tensions['Line1_Tension'],
        name='Line 1 Tension',
        yaxis='y2',
        line=dict(color='red')
    ))

    fig.update_layout(
        title='Vessel Motion and Mooring Tension',
        xaxis_title='Time',
        yaxis=dict(title='Heave (m)', side='left'),
        yaxis2=dict(title='Tension (kN)', side='right', overlaying='y'),
        hovermode='x unified'
    )

    fig.write_html(output_dir / 'time_series.html')

    # 8. Create statistics table plot
    fig_stats = go.Figure(data=[go.Table(
        header=dict(
            values=['Metric', 'Heave (m)', 'Line 1 Tension (kN)'],
            fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=[
                ['Mean', 'Std Dev', 'Min', 'Max'],
                [
                    f"{motion_stats.loc['mean', 'Heave']:.3f}",
                    f"{motion_stats.loc['std', 'Heave']:.3f}",
                    f"{motion_stats.loc['min', 'Heave']:.3f}",
                    f"{motion_stats.loc['max', 'Heave']:.3f}"
                ],
                [
                    f"{tension_stats.loc['mean', 'Line1_Tension']:.1f}",
                    f"{tension_stats.loc['std', 'Line1_Tension']:.1f}",
                    f"{tension_stats.loc['min', 'Line1_Tension']:.1f}",
                    f"{tension_stats.loc['max', 'Line1_Tension']:.1f}"
                ]
            ],
            fill_color='lavender',
            align='left'
        )
    )])

    fig_stats.update_layout(title='Statistical Summary')
    fig_stats.write_html(output_dir / 'statistics_table.html')

    print(f"✓ Processed OrcaFlex results")
    print(f"  Duration: {summary['duration_seconds']:.1f} seconds")
    print(f"  Max heave: {summary['max_heave_value']:.2f} m at {summary['max_heave_time']}")
    print(f"  Max tension: {summary['max_tension_value']:.1f} kN at {summary['max_tension_time']}")

    return summary

# Usage
results = process_orcaflex_results(
    results_dir=Path('data/processed/orcaflex_results'),
    output_dir=Path('reports/processed_results')
)
```

### Example 2: Wave Scatter Diagram Analysis

```python
def process_wave_scatter_diagram(
    scatter_csv: Path,
    output_dir: Path
) -> pd.DataFrame:
    """
    Process wave scatter diagram and calculate occurrence frequencies.

    Args:
        scatter_csv: Path to wave scatter CSV
        output_dir: Output directory

    Returns:
        Processed scatter diagram with frequencies
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load scatter diagram
    scatter = pd.read_csv(scatter_csv)

    # Create Hs and Tp bins
    scatter['Hs_bin'] = pd.cut(
        scatter['Hs'],
        bins=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        labels=['0-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']
    )

    scatter['Tp_bin'] = pd.cut(
        scatter['Tp'],
        bins=[0, 4, 6, 8, 10, 12, 14, 16],
        labels=['0-4', '4-6', '6-8', '8-10', '10-12', '12-14', '14-16']
    )

    # Calculate occurrence frequency
    frequency = scatter.groupby(['Hs_bin', 'Tp_bin'])['Occurrence'].sum().reset_index()

    # Pivot for heatmap
    heatmap_data = frequency.pivot(
        index='Hs_bin',
        columns='Tp_bin',
        values='Occurrence'
    ).fillna(0)

    # Calculate annual hours
    heatmap_data_hours = heatmap_data * 8760  # Hours per year

    # Export
    heatmap_data_hours.to_csv(output_dir / 'wave_scatter_annual_hours.csv')

    # Create heatmap
    import plotly.graph_objects as go

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data_hours.values,
        x=heatmap_data_hours.columns,
        y=heatmap_data_hours.index,
        colorscale='Blues',
        text=heatmap_data_hours.values,
        texttemplate='%{text:.1f}',
        colorbar=dict(title='Hours/Year')
    ))

    fig.update_layout(
        title='Wave Scatter Diagram - Annual Occurrence',
        xaxis_title='Tp (s)',
        yaxis_title='Hs (m)'
    )

    fig.write_html(output_dir / 'wave_scatter_heatmap.html')

    print(f"✓ Wave scatter diagram processed")
    print(f"  Total annual hours: {heatmap_data_hours.values.sum():.1f}")
    print(f"  Most common sea state: Hs={heatmap_data_hours.stack().idxmax()[0]}, Tp={heatmap_data_hours.stack().idxmax()[1]}")

    return heatmap_data_hours

# Usage
scatter_processed = process_wave_scatter_diagram(
    scatter_csv=Path('data/raw/wave_scatter.csv'),
    output_dir=Path('reports/wave_analysis')
)
```

### Example 3: Fatigue Damage Calculation

```python
def calculate_fatigue_damage(
    stress_ranges: pd.DataFrame,
    sn_curve: dict,
    design_life_years: float = 25
) -> pd.DataFrame:
    """
    Calculate fatigue damage using stress range histogram.

    Args:
        stress_ranges: DataFrame with stress range bins and counts
        sn_curve: S-N curve parameters {'m': 3.0, 'a': 1.52e12}
        design_life_years: Design life in years

    Returns:
        DataFrame with fatigue damage per bin
    """
    # S-N curve parameters
    m = sn_curve['m']
    a = sn_curve['a']

    # Calculate damage per bin
    stress_ranges['Cycles_to_failure'] = a / (stress_ranges['StressRange'] ** m)
    stress_ranges['Damage'] = stress_ranges['Count'] / stress_ranges['Cycles_to_failure']

    # Scale to design life
    total_simulation_time_years = stress_ranges['SimulationTime_hours'].iloc[0] / 8760
    scale_factor = design_life_years / total_simulation_time_years

    stress_ranges['Damage_Scaled'] = stress_ranges['Damage'] * scale_factor

    # Calculate cumulative damage
    total_damage = stress_ranges['Damage_Scaled'].sum()
    fatigue_life_years = design_life_years / total_damage if total_damage > 0 else np.inf

    # Summary
    summary = pd.DataFrame({
        'Metric': [
            'Total Damage',
            'Design Life (years)',
            'Predicted Fatigue Life (years)',
            'Utilization (%)'
        ],
        'Value': [
            total_damage,
            design_life_years,
            fatigue_life_years,
            (total_damage / 1.0) * 100  # Assuming damage limit = 1.0
        ]
    })

    print(summary)

    return stress_ranges

# Example usage
stress_data = pd.DataFrame({
    'StressRange': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],  # MPa
    'Count': [1e6, 5e5, 2e5, 1e5, 5e4, 2e4, 1e4, 5e3, 2e3, 1e3],
    'SimulationTime_hours': [3] * 10  # 3-hour simulation
})

sn_params = {
    'm': 3.0,      # S-N curve slope
    'a': 1.52e12   # S-N curve constant (DNV F3 curve)
}

fatigue_results = calculate_fatigue_damage(
    stress_ranges=stress_data,
    sn_curve=sn_params,
    design_life_years=25
)

fatigue_results.to_csv('reports/fatigue_damage.csv', index=False)
```

### Example 4: Multi-Source Data Merging

```python
def merge_analysis_results(
    motion_file: Path,
    tension_file: Path,
    environmental_file: Path,
    output_file: Path
) -> pd.DataFrame:
    """
    Merge results from multiple analysis sources.

    Args:
        motion_file: Vessel motion CSV
        tension_file: Mooring tension CSV
        environmental_file: Environmental conditions CSV
        output_file: Output merged CSV

    Returns:
        Merged DataFrame
    """
    # Load individual files
    motions = pd.read_csv(motion_file)
    tensions = pd.read_csv(tension_file)
    environment = pd.read_csv(environmental_file)

    # Merge on time
    merged = motions.merge(
        tensions,
        on='Time',
        how='inner',
        suffixes=('_motion', '_tension')
    )

    merged = merged.merge(
        environment,
        on='Time',
        how='inner'
    )

    # Calculate derived quantities
    merged['Total_Motion'] = np.sqrt(
        merged['Surge']**2 + merged['Sway']**2 + merged['Heave']**2
    )

    merged['Max_Tension'] = merged[[
        col for col in merged.columns if 'Tension' in col
    ]].max(axis=1)

    # Export
    merged.to_csv(output_file, index=False)

    print(f"✓ Merged {len(merged)} records")
    print(f"  Columns: {len(merged.columns)}")
    print(f"  Time range: {merged['Time'].min()} to {merged['Time'].max()}")

    return merged

# Usage
merged_results = merge_analysis_results(
    motion_file=Path('data/processed/vessel_motions.csv'),
    tension_file=Path('data/processed/mooring_tensions.csv'),
    environmental_file=Path('data/processed/environment.csv'),
    output_file=Path('data/processed/merged_results.csv')
)
```

### Example 5: Performance Benchmarking

```python
def benchmark_data_processing_methods(
    data_size: int = 1_000_000
) -> pd.DataFrame:
    """
    Benchmark different Pandas operations for performance.

    Args:
        data_size: Number of rows to test

    Returns:
        Benchmark results
    """
    import time

    # Generate test data
    df = pd.DataFrame({
        'Time': pd.date_range('2025-01-01', periods=data_size, freq='0.1S'),
        'Value1': np.random.randn(data_size),
        'Value2': np.random.randn(data_size),
        'Category': np.random.choice(['A', 'B', 'C'], data_size)
    })

    results = []

    # Test 1: Iterrows (slow)
    start = time.time()
    total = 0
    for idx, row in df.head(10000).iterrows():
        total += row['Value1'] + row['Value2']
    results.append({
        'Method': 'iterrows (10k rows)',
        'Time (s)': time.time() - start,
        'Speed': 'Slow ❌'
    })

    # Test 2: Apply (medium)
    start = time.time()
    df['Sum_Apply'] = df[['Value1', 'Value2']].apply(lambda x: x.sum(), axis=1)
    results.append({
        'Method': 'apply',
        'Time (s)': time.time() - start,
        'Speed': 'Medium ⚠️'
    })

    # Test 3: Vectorized (fast)
    start = time.time()
    df['Sum_Vectorized'] = df['Value1'] + df['Value2']
    results.append({
        'Method': 'vectorized',
        'Time (s)': time.time() - start,
        'Speed': 'Fast ✅'
    })

    # Test 4: NumPy (fastest)
    start = time.time()
    df['Sum_NumPy'] = np.add(df['Value1'].values, df['Value2'].values)
    results.append({
        'Method': 'numpy',
        'Time (s)': time.time() - start,
        'Speed': 'Fastest 🚀'
    })

    # Test 5: GroupBy aggregation
    start = time.time()
    grouped = df.groupby('Category')[['Value1', 'Value2']].mean()
    results.append({
        'Method': 'groupby.mean',
        'Time (s)': time.time() - start,
        'Speed': 'Fast ✅'
    })

    benchmark_df = pd.DataFrame(results)
    print(benchmark_df)

    return benchmark_df

# Run benchmark
benchmark_results = benchmark_data_processing_methods(data_size=1_000_000)
```

## Best Practices

### 1. Memory Efficiency

**Use appropriate data types:**
```python
# ❌ Bad: Default float64
df = pd.DataFrame({'value': np.random.randn(1000000)})
print(f"Memory: {df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

# ✅ Good: Use float32 when precision allows
df_optimized = pd.DataFrame({'value': np.random.randn(1000000).astype(np.float32)})
print(f"Memory: {df_optimized.memory_usage(deep=True).sum() / 1e6:.1f} MB")  # 50% reduction

# ✅ Use categorical for repeated strings
df['category'] = pd.Categorical(['A', 'B', 'C'] * 100000)
```

**Chunking for large files:**
```python
def process_large_csv_in_chunks(
    csv_file: Path,
    chunksize: int = 100_000
) -> pd.DataFrame:
    """Process large CSV in chunks to avoid memory issues."""
    chunks = []

    for chunk in pd.read_csv(csv_file, chunksize=chunksize):
        # Process each chunk
        chunk_processed = chunk[chunk['Value'] > 0]  # Example filter
        chunks.append(chunk_processed)

    # Combine all chunks
    result = pd.concat(chunks, ignore_index=True)

    return result
```

### 2. Vectorization

**Always prefer vectorized operations:**
```python
# ❌ Bad: Loop
df['result'] = 0
for i in range(len(df)):
    df.loc[i, 'result'] = df.loc[i, 'a'] + df.loc[i, 'b']

# ✅ Good: Vectorized
df['result'] = df['a'] + df['b']

# ✅ Better: NumPy for complex operations
df['result'] = np.where(
    df['a'] > 0,
    df['a'] + df['b'],
    df['a'] - df['b']
)
```

### 3. Index Usage

**Use index for time series:**
```python
# ✅ Set datetime index
df['Time'] = pd.to_datetime(df['Time'])
df.set_index('Time', inplace=True)

# Fast slicing
subset = df['2025-01-01':'2025-01-31']

# Fast resampling
daily_mean = df.resample('D').mean()
```

### 4. Data Validation

**Validate data before processing:**
```python
def validate_engineering_data(df: pd.DataFrame) -> bool:
    """Validate engineering data integrity."""
    # Check for missing values
    if df.isnull().any().any():
        print("⚠ Warning: Missing values detected")
        print(df.isnull().sum())

    # Check for duplicates
    if df.duplicated().any():
        print("⚠ Warning: Duplicate rows detected")
        print(f"Duplicates: {df.duplicated().sum()}")

    # Check data types
    print("Data types:")
    print(df.dtypes)

    # Check value ranges
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if (df[col] < 0).any():
            print(f"⚠ Warning: Negative values in {col}")

    return True
```

## Resources

- **Pandas Documentation**: https://pandas.pydata.org/docs/
- **Pandas Cheat Sheet**: https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf
- **Time Series Analysis**: https://pandas.pydata.org/docs/user_guide/timeseries.html
- **GroupBy Operations**: https://pandas.pydata.org/docs/user_guide/groupby.html
- **Performance Tips**: https://pandas.pydata.org/docs/user_guide/enhancingperf.html

---

**Use this skill for all time series analysis and data processing in DigitalModel!**

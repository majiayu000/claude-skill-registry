---
name: signal-analysis
description: Perform signal processing, rainflow cycle counting, and spectral analysis
  for fatigue and time series data. Use for analyzing stress time histories, computing
  FFT/PSD, extracting fatigue cycles (ASTM E1049-85), and batch processing OrcaFlex
  signals.
updated: '2026-01-07'
---
# Signal Analysis Skill

Perform signal processing, rainflow cycle counting, and spectral analysis for fatigue assessment and time series characterization.

## Version Metadata

```yaml
version: 1.0.0
python_min_version: '3.10'
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

### [1.0.0] - 2026-01-07

**Added:**
- Initial version metadata and dependency management
- Semantic versioning support
- Compatibility information for Python 3.10-3.13

**Changed:**
- Enhanced skill documentation structure


## When to Use

- Analyzing fatigue from stress/load time series
- Computing rainflow cycles for damage calculation
- FFT and power spectral density analysis
- Frequency spectrum characterization
- Batch processing OrcaFlex simulation signals
- Time series conditioning and filtering
- Converting time-domain data to frequency-domain

## Prerequisites

- Python environment with `digitalmodel` package installed
- Time series data in CSV, Excel, or OrcaFlex format
- For OrcaFlex signals: completed .sim files

## Signal Processing Types

### 1. Rainflow Cycle Counting (ASTM E1049-85)

Extract stress/load cycles for fatigue analysis using industry-standard rainflow algorithm.

```yaml
signal_analysis:
  rainflow:
    flag: true
    input_file: "data/stress_time_history.csv"
    time_column: "time"
    signal_column: "stress"
    output:
      cycles_file: "results/rainflow_cycles.csv"
      histogram_file: "results/cycle_histogram.html"
      summary_file: "results/rainflow_summary.json"
    options:
      hysteresis_filter: 0.0  # Filter small cycles (fraction of range)
      residual_method: "none"  # none, half_cycles, or pairs
```

### 2. FFT Spectral Analysis

Compute frequency content using Fast Fourier Transform.

```yaml
signal_analysis:
  fft:
    flag: true
    input_file: "data/motion_time_history.csv"
    time_column: "time"
    signal_column: "heave"
    output:
      spectrum_file: "results/fft_spectrum.csv"
      plot_file: "results/fft_spectrum.html"
    options:
      window: "hanning"  # hanning, hamming, blackman, rectangular
      normalize: true
      one_sided: true    # Show positive frequencies only
```

### 3. Power Spectral Density (Welch Method)

Estimate power spectral density with reduced variance using overlapping segments.

```yaml
signal_analysis:
  psd:
    flag: true
    input_file: "data/vessel_motion.csv"
    time_column: "time"
    signal_columns:
      - "surge"
      - "heave"
      - "pitch"
    output:
      psd_file: "results/psd_analysis.csv"
      plot_file: "results/psd_plot.html"
    options:
      method: "welch"
      segment_length: 1024
      overlap: 0.5
      window: "hanning"
      detrend: "linear"
```

### 4. Time Series Conditioning

Prepare raw time series for analysis with filtering and preprocessing.

```yaml
signal_analysis:
  conditioning:
    flag: true
    input_file: "data/raw_signal.csv"
    output_file: "data/conditioned_signal.csv"
    operations:
      - type: "resample"
        target_dt: 0.1  # seconds
        method: "linear"
      - type: "detrend"
        method: "linear"
      - type: "filter"
        filter_type: "lowpass"
        cutoff_frequency: 0.5  # Hz
        order: 4
      - type: "remove_offset"
        method: "mean"  # mean or first_value
```

### 5. OrcaFlex Signal Batch Processing

Process multiple OrcaFlex time histories in parallel.

```yaml
signal_analysis:
  orcaflex_batch:
    flag: true
    sim_directory: "results/.sim/"
    sim_pattern: "*.sim"
    variables:
      - object: "Line1"
        variable_name: "Effective Tension"
        arc_length: 0
      - object: "Vessel1"
        variable_name: "Heave"
    processing:
      rainflow: true
      psd: true
      statistics: true
    output_directory: "results/signal_analysis/"
    parallel: true
    max_workers: 4
```

## Python API

### Rainflow Cycle Counting

```python
from digitalmodel.signal_processing.signal_analysis.rainflow import RainflowCounter

# Initialize counter
counter = RainflowCounter()

# Load time history
import pandas as pd
data = pd.read_csv("stress_time_history.csv")
time = data["time"].values
stress = data["stress"].values

# Extract cycles
cycles = counter.count_cycles(stress)

# Get cycle matrix (range, mean, count)
cycle_matrix = counter.get_cycle_matrix(cycles)

# Calculate damage using S-N curve
from digitalmodel.structural.fatigue_apps import SNCurve
sn_curve = SNCurve.from_code("DNV-RP-C203", "D")
damage = counter.calculate_damage(cycles, sn_curve)

print(f"Total cycles: {len(cycles)}")
print(f"Fatigue damage: {damage:.6f}")
```

### Spectral Analysis

```python
from digitalmodel.signal_processing.signal_analysis.spectral import SpectralAnalyzer
import numpy as np

# Initialize analyzer
analyzer = SpectralAnalyzer()

# Load signal
data = pd.read_csv("motion_time_history.csv")
time = data["time"].values
signal = data["heave"].values
dt = time[1] - time[0]

# Compute FFT
frequencies, amplitudes = analyzer.compute_fft(
    signal,
    dt=dt,
    window="hanning",
    normalize=True
)

# Compute PSD (Welch method)
freq_psd, psd = analyzer.compute_psd(
    signal,
    dt=dt,
    method="welch",
    nperseg=1024,
    overlap=0.5
)

# Find dominant frequency
dominant_freq = analyzer.find_peak_frequency(freq_psd, psd)
print(f"Dominant frequency: {dominant_freq:.3f} Hz")

# Compute spectral moments
m0, m2, m4 = analyzer.compute_spectral_moments(freq_psd, psd)
Tz = np.sqrt(m0/m2)  # Zero-crossing period
print(f"Zero-crossing period: {Tz:.2f} s")
```

### Time Series Processing

```python
from digitalmodel.signal_processing.signal_analysis.time_series import TimeSeriesProcessor

# Initialize processor
processor = TimeSeriesProcessor()

# Load raw data
data = pd.read_csv("raw_signal.csv")
time = data["time"].values
signal = data["stress"].values

# Resample to uniform time step
time_resampled, signal_resampled = processor.resample(
    time, signal,
    target_dt=0.1,
    method="linear"
)

# Detrend
signal_detrended = processor.detrend(signal_resampled, method="linear")

# Apply low-pass filter
signal_filtered = processor.lowpass_filter(
    signal_detrended,
    dt=0.1,
    cutoff_freq=0.5,
    order=4
)

# Remove mean offset
signal_final = processor.remove_offset(signal_filtered, method="mean")

# Save processed signal
processed_df = pd.DataFrame({
    "time": time_resampled,
    "stress": signal_final
})
processed_df.to_csv("processed_signal.csv", index=False)
```

### OrcaFlex Signal Extraction

```python
from digitalmodel.signal_processing.signal_analysis.orcaflex_signals import OrcaFlexSignalExtractor
from pathlib import Path

# Initialize extractor
extractor = OrcaFlexSignalExtractor()

# Extract time history from single .sim file
sim_file = Path("simulation.sim")
time, tension = extractor.extract_time_history(
    sim_file,
    object_name="Line1",
    variable_name="Effective Tension",
    arc_length=0
)

# Batch extraction from multiple .sim files
sim_files = list(Path("results/.sim/").glob("*.sim"))
results = extractor.batch_extract(
    sim_files,
    variables=[
        {"object": "Line1", "variable_name": "Effective Tension"},
        {"object": "Vessel1", "variable_name": "Heave"}
    ],
    parallel=True,
    max_workers=4
)

# Process extracted signals
for sim_name, sim_data in results.items():
    for var_name, (time, signal) in sim_data.items():
        print(f"{sim_name} - {var_name}: {len(signal)} samples")
```

### Generic Time Series Reader

```python
from digitalmodel.signal_processing.signal_analysis.readers import GenericTimeSeriesReader

# Auto-detect file format and load
reader = GenericTimeSeriesReader()

# Read CSV
data = reader.read("data/measurements.csv")

# Read Excel
data = reader.read("data/measurements.xlsx", sheet_name="Sheet1")

# Read OrcaFlex .sim
data = reader.read("simulation.sim", object="Line1", variable="Tension")

# Read with column mapping
data = reader.read(
    "data/custom_format.csv",
    time_column="timestamp_sec",
    signal_columns=["stress_mpa", "strain_mm"]
)
```

## Configuration Examples

### Complete Signal Analysis Workflow

```yaml
basename: signal_analysis_workflow

signal_analysis:
  # Step 1: Condition raw signals
  conditioning:
    flag: true
    input_file: "data/raw_stress.csv"
    output_file: "data/conditioned_stress.csv"
    operations:
      - type: "resample"
        target_dt: 0.1
      - type: "detrend"
        method: "linear"
      - type: "filter"
        filter_type: "lowpass"
        cutoff_frequency: 1.0

  # Step 2: Rainflow counting
  rainflow:
    flag: true
    input_file: "data/conditioned_stress.csv"
    time_column: "time"
    signal_column: "stress"
    output:
      cycles_file: "results/cycles.csv"
      histogram_file: "results/cycle_histogram.html"

  # Step 3: Spectral analysis
  psd:
    flag: true
    input_file: "data/conditioned_stress.csv"
    time_column: "time"
    signal_columns: ["stress"]
    output:
      psd_file: "results/stress_psd.csv"
      plot_file: "results/stress_psd.html"
```

### Fatigue-Focused Analysis

```yaml
signal_analysis:
  rainflow:
    flag: true
    input_file: "data/stress_history.csv"
    output:
      cycles_file: "results/fatigue_cycles.csv"
      summary_file: "results/fatigue_summary.json"
    options:
      hysteresis_filter: 0.01  # Filter cycles < 1% of range

  fatigue_damage:
    flag: true
    cycles_file: "results/fatigue_cycles.csv"
    sn_curve:
      code: "DNV-RP-C203"
      curve_type: "D"
      environment: "seawater_cathodic"
    output:
      damage_file: "results/fatigue_damage.json"
      report_file: "results/fatigue_report.html"
```

## Output Formats

### Rainflow Cycles CSV

```csv
range,mean,count,from_stress,to_stress
245.3,125.6,1.0,3.0,248.3
198.7,156.2,1.0,56.8,255.6
167.4,89.3,0.5,5.6,173.0
```

### PSD Output CSV

```csv
frequency_hz,psd_stress,psd_heave,psd_pitch
0.001,1.23e+06,0.0045,0.00012
0.002,2.45e+06,0.0089,0.00024
0.005,5.67e+06,0.0234,0.00056
```

### Summary Statistics JSON

```json
{
  "signal_name": "stress",
  "sample_count": 36000,
  "duration_sec": 3600,
  "statistics": {
    "min": -125.4,
    "max": 456.7,
    "mean": 165.3,
    "std": 89.2,
    "rms": 188.5
  },
  "spectral": {
    "dominant_frequency_hz": 0.125,
    "bandwidth_parameter": 0.342,
    "spectral_moments": {
      "m0": 7956.4,
      "m2": 123.5,
      "m4": 4.56
    }
  },
  "rainflow": {
    "total_cycles": 1234,
    "max_range": 582.1,
    "mean_range": 156.7
  }
}
```

## Best Practices

### Signal Quality

1. **Check sampling rate** - Ensure Nyquist criterion for frequencies of interest
2. **Remove transients** - Skip build-up periods in OrcaFlex simulations
3. **Validate stationarity** - Use multiple segments for PSD estimation
4. **Handle gaps** - Interpolate or segment around missing data

### Rainflow Analysis

1. **Hysteresis filtering** - Remove small cycles (typically < 1-5% of range)
2. **Residual handling** - Choose appropriate method for incomplete cycles
3. **Cycle binning** - Use consistent bin sizes for histogram comparison
4. **S-N curve matching** - Ensure stress units match S-N curve units

### Performance Optimization

1. **Parallel processing** - Use batch extraction for multiple files
2. **Memory management** - Process long signals in chunks
3. **Downsampling** - Reduce sampling rate if high frequencies not needed
4. **Result caching** - Store intermediate results for reprocessing

## Error Handling

### Common Issues

1. **Non-uniform time step**
   ```python
   # Check and resample if needed
   dt_values = np.diff(time)
   if np.std(dt_values) > 0.001 * np.mean(dt_values):
       time, signal = processor.resample(time, signal, target_dt=np.mean(dt_values))
   ```

2. **NaN values in signal**
   ```python
   # Interpolate or remove
   if np.any(np.isnan(signal)):
       signal = processor.interpolate_nans(time, signal)
   ```

3. **Insufficient samples for PSD**
   ```python
   # Reduce segment length
   if len(signal) < nperseg * 2:
       nperseg = len(signal) // 4
   ```

## Related Skills

- [fatigue-analysis](../fatigue-analysis/SKILL.md) - Use rainflow cycles for fatigue damage calculation
- [orcaflex-post-processing](../orcaflex-post-processing/SKILL.md) - Extract time histories from OrcaFlex
- [structural-analysis](../structural-analysis/SKILL.md) - Stress analysis for signal generation

## References

- ASTM E1049-85: Standard Practices for Cycle Counting in Fatigue Analysis
- Welch, P.D. (1967): The Use of FFT for Estimation of Power Spectra
- DNV-RP-C203: Fatigue Design of Offshore Steel Structures

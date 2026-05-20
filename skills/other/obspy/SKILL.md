---
name: obspy
description: |
  Seismology data processing with ObsPy. Helps with reading seismic waveforms,
  filtering/processing time series, fetching data from FDSN services, and
  earthquake analysis. Use when Claude needs to: (1) Read seismic data formats
  (MiniSEED, SAC, GSE2, SEGY), (2) Filter or process waveforms, (3) Fetch data
  from IRIS/USGS/FDSN services, (4) Search for earthquakes by magnitude/location,
  (5) Plot seismograms or spectrograms, (6) Remove instrument response,
  (7) Analyze station metadata.
version: 1.0.0
author: Geoscience Skills
license: MIT
tags: [Seismology, Waveforms, FDSN, Earthquake, Time Series, ObsPy, MiniSEED, Signal Processing]
dependencies: [obspy>=1.4.0]
complements: [segyio, disba]
workflow_role: processing
---

# ObsPy - Seismology Data Processing

## Quick Reference

```python
from obspy import read, UTCDateTime
from obspy.clients.fdsn import Client

# Read local file (MiniSEED, SAC, etc.)
st = read("data.mseed")
tr = st[0]                          # First trace
print(tr.stats)                     # Metadata

# Fetch from FDSN
client = Client("IRIS")
t = UTCDateTime("2023-02-06T01:17:00")
st = client.get_waveforms("IU", "ANMO", "00", "LHZ", t, t + 3600)
st.plot()
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `Stream` | Container for multiple Trace objects |
| `Trace` | Single waveform with data + metadata |
| `UTCDateTime` | Precise time handling |
| `Inventory` | Station/channel metadata |
| `Catalog` | Earthquake event information |

## Essential Operations

### Read and Inspect
```python
st = read("data.mseed")              # Auto-detect format
tr = st[0]
print(tr.stats.station, tr.stats.channel, tr.stats.sampling_rate)
```

### Filter and Process
```python
st.detrend("demean")                 # Remove mean
st.detrend("linear")                 # Remove trend
st.taper(max_percentage=0.05)        # Taper edges
st.filter("bandpass", freqmin=0.1, freqmax=10.0)
```

### Fetch Waveforms from FDSN
```python
client = Client("IRIS")
t1 = UTCDateTime("2023-02-06T01:17:00")
st = client.get_waveforms("IU", "ANMO", "00", "LHZ", t1, t1 + 3600)
st.write("output.mseed", format="MSEED")
```

### Search Earthquakes
```python
client = Client("USGS")
cat = client.get_events(
    starttime=UTCDateTime("2023-01-01"),
    endtime=UTCDateTime("2023-12-31"),
    minmagnitude=7.0
)
event = cat[0]
print(f"M{event.magnitudes[0].mag} at {event.origins[0].latitude}")
```

### Get Station Metadata
```python
inv = client.get_stations(
    network="IU", station="ANMO",
    level="response"                 # Required for response removal
)
```

### Remove Instrument Response
```python
st = client.get_waveforms("IU", "ANMO", "00", "LHZ", t, t + 3600)
inv = client.get_stations(network="IU", station="ANMO", level="response")
st.remove_response(inventory=inv, output="VEL")  # VEL, DISP, or ACC
```

### Trim and Select
```python
st.trim(UTCDateTime("2023-01-01"), UTCDateTime("2023-01-01T01:00:00"))
st_z = st.select(channel="*Z")       # Vertical only
st_bh = st.select(channel="BH*")     # BH channels
```

### Merge and Handle Gaps
```python
st.print_gaps()                      # Check for gaps
st.merge(method=1, fill_value="interpolate")
```

## Writing Data

```python
st.write("output.mseed", format="MSEED")
st.write("output.sac", format="SAC")
```

## Error Handling

```python
from obspy.clients.fdsn.header import FDSNNoDataException

try:
    st = client.get_waveforms("IU", "ANMO", "00", "LHZ", t1, t2)
except FDSNNoDataException:
    print("No data available")
```

## Common Tips

1. **Always detrend and taper before filtering** to avoid artifacts
2. **Use `level="response"`** when fetching stations for instrument correction
3. **Check for gaps** before processing with `st.print_gaps()`
4. **Wildcards work** in queries: `station="A*"`, `channel="BH?"`
5. **UTCDateTime** accepts ISO strings, timestamps, datetime objects

## When to Use vs Alternatives

| Tool | Best For |
|------|----------|
| **obspy** | Full seismology workflows, FDSN data access, waveform processing |
| **segyio** | Fast, low-level SEG-Y file I/O for reflection seismic data |
| **scipy.signal** | Generic signal processing without seismology-specific features |

**Use obspy when** you need seismological context: FDSN clients, instrument
response removal, earthquake catalogs, or standard seismic formats.

**Use segyio instead** when working exclusively with SEG-Y files for reflection
seismic. segyio is faster for large 3D volumes with inline/crossline access.

**Use scipy.signal instead** when you only need generic filtering or spectral
analysis and don't need seismology-specific metadata or data access.

## Common Workflows

### Fetch and process earthquake waveforms
```
- [ ] Initialize FDSN client: `Client("IRIS")`
- [ ] Search events with `client.get_events()` for target magnitude/region
- [ ] Fetch waveforms with `client.get_waveforms()` for desired stations
- [ ] Get station metadata with `level="response"` for instrument correction
- [ ] Preprocess: detrend, taper, remove instrument response
- [ ] Filter to frequency band of interest
- [ ] Trim to analysis window and export or plot
```

## References

- **[FDSN Data Centers](references/fdsn_clients.md)** - Available data centers and capabilities
- **[Channel Codes](references/channel_codes.md)** - Channel naming convention details
- **[Troubleshooting](references/troubleshooting.md)** - Common issues and solutions

## Scripts

- **[scripts/fetch_earthquake.py](scripts/fetch_earthquake.py)** - Fetch waveforms for an earthquake
- **[scripts/batch_process.py](scripts/batch_process.py)** - Batch process seismic files

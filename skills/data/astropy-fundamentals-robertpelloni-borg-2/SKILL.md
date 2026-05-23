---
name: astropy-fundamentals
description: Work with astronomical data using Astropy for FITS file I/O, coordinate transformations, physical units, precise time handling, and catalog operations. Use when processing telescope images, matching celestial catalogs, handling time-series observations, or building photometry/spectroscopy pipelines. Ideal for astronomy research requiring proper unit handling, coordinate frame transformations, and astronomical time scales.
model: sonnet
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebFetch
---

# Astropy Fundamentals

Master **Astropy**, the foundational Python library for astronomy and astrophysics. Learn to work with astronomical data formats, coordinate systems, physical units, precise time calculations, and scientific tables - the essential toolkit for modern astronomical computing.

**Official Documentation**: https://docs.astropy.org/en/stable/

**GitHub**: https://github.com/astropy/astropy

## Quick Reference Card

### Installation & Setup
```bash
# Using pixi (recommended for scientific projects)
pixi add astropy photutils specutils

# Using pip
pip install astropy[all]

# Optional affiliated packages
pixi add photutils specutils astroquery reproject
```

### Essential Operations
```python
import astropy.units as u
from astropy.io import fits
from astropy.coordinates import SkyCoord
from astropy.time import Time
from astropy.table import Table, QTable
from astropy.wcs import WCS

# Units and Quantities
distance = 10 * u.parsec
wavelength = 5000 * u.angstrom
freq = wavelength.to(u.Hz, equivalencies=u.spectral())

# FITS I/O
with fits.open('image.fits') as hdul:
    data = hdul[0].data
    header = hdul[0].header

# Coordinates
coord = SkyCoord(ra=10.625*u.degree, dec=41.2*u.degree, frame='icrs')
galactic = coord.galactic
separation = coord.separation(other_coord)

# Time
t = Time('2024-01-01T00:00:00', format='isot', scale='utc')
jd = t.jd
future = t + 1*u.day

# Tables
tbl = Table([ra_col, dec_col, flux_col], names=['ra', 'dec', 'flux'])
filtered = tbl[tbl['flux'] > 100]

# WCS
wcs = WCS(header)
ra, dec = wcs.pixel_to_world(x_pix, y_pix)
```

### Quick Decision Tree

```
Working with astronomical data?
├─ FITS files → astropy.io.fits
├─ Celestial coordinates → astropy.coordinates (SkyCoord)
├─ Physical quantities → astropy.units
├─ Astronomical time → astropy.time
├─ Catalogs/tables → astropy.table
├─ Image coordinates → astropy.wcs
├─ Photometry → photutils
└─ Spectroscopy → specutils

Need coordinate transformation?
├─ Simple conversions → SkyCoord.transform_to()
├─ Sky separations → SkyCoord.separation()
├─ Matching catalogs → match_to_catalog_sky()
└─ Custom frames → Define new frame class

Working with units?
├─ Standard units → multiply by u.unit
├─ Unit conversions → quantity.to()
├─ Wavelength/frequency → Use u.spectral() equivalency
└─ Dimensionless → quantity.decompose()

Need precise time?
├─ Single instant → Time()
├─ Arrays of times → Time(array)
├─ Time scales → specify scale='utc', 'tai', etc.
└─ Time formats → specify format='jd', 'isot', etc.
```

## When to Use This Skill

Use Astropy fundamentals when working with:

- **FITS files** from telescopes, surveys, or simulations
- **Celestial coordinates** requiring precise transformations between reference frames
- **Physical quantities** with units (distances, velocities, energies, magnitudes)
- **Astronomical time** needing sub-nanosecond precision or specific time scales
- **Catalogs and tables** from surveys, observations, or simulations
- **Image astrometry** relating pixel positions to sky coordinates
- **Photometric analysis** of point sources or aperture measurements
- **Spectroscopic data** requiring wavelength calibration or line analysis
- **Multi-wavelength astronomy** combining data across electromagnetic spectrum
- **Observational planning** calculating rise/set times, airmass, visibility

## Core Concepts

### 1. Units and Quantities

Physical quantities with dimensional correctness. Attach units to values and convert automatically.

**Key operations:**
- Create: `distance = 10 * u.parsec`
- Convert: `distance.to(u.lightyear)`
- Equivalencies: `wavelength.to(u.Hz, equivalencies=u.spectral())`
- Arithmetic: Units propagate automatically

**See [references/PATTERNS.md](references/PATTERNS.md#units-and-quantities-patterns)** for custom units, logarithmic units, and advanced equivalencies.

### 2. FITS I/O

Standard format for astronomical data. Read/write images and tables with headers.

**Key operations:**
- Open: `fits.open('file.fits')` with context manager
- Access: `hdul[0].data`, `hdul[0].header`
- Headers: Dictionary-like access, add comments
- Memory mapping: `fits.open('file.fits', memmap=True)` for large files

**See [references/PATTERNS.md](references/PATTERNS.md#fits-manipulation-patterns)** for multi-extension FITS, header inheritance, and large file handling.

### 3. Coordinates

Celestial positions with automatic frame transformations.

**Key operations:**
- Create: `SkyCoord(ra=10*u.deg, dec=20*u.deg, frame='icrs')`
- Transform: `coord.galactic`, `coord.transform_to('fk5')`
- Separations: `coord1.separation(coord2)`
- Matching: `coord.match_to_catalog_sky(catalog)`

**See [references/PATTERNS.md](references/PATTERNS.md#coordinate-patterns)** for custom frames, catalog cross-matching, and observer-dependent coordinates.

### 4. Time

Sub-nanosecond precision with multiple time scales and formats.

**Key operations:**
- Create: `Time('2024-01-01', scale='utc')`
- Formats: `.jd`, `.mjd`, `.iso`, `.datetime`
- Scales: `.utc`, `.tai`, `.tt`, `.tdb`
- Arithmetic: `t + 1*u.day`

**See [references/PATTERNS.md](references/PATTERNS.md#time-patterns)** for high-precision calculations, time series, and barycentric corrections.

### 5. Tables

Flexible tabular data with units and metadata.

**Key operations:**
- Create: `Table([col1, col2], names=['a', 'b'])`
- QTable: Preserves Quantity units
- Filter: `tbl[tbl['mag'] < 15]`
- Join: `join(tbl1, tbl2, keys='id')`
- I/O: `.read()`, `.write()` for FITS, CSV, HDF5

**See [references/PATTERNS.md](references/PATTERNS.md#table-patterns)** for masked tables, joins, metadata, and indexing.

### 6. WCS (World Coordinate System)

Maps pixel coordinates to sky coordinates.

**Key operations:**
- Load: `WCS(header)`
- Pixel→Sky: `wcs.pixel_to_world(x, y)` returns SkyCoord
- Sky→Pixel: `wcs.world_to_pixel(coord)`
- Legacy: `wcs.all_pix2world(x, y, 0)` for arrays

**See [references/PATTERNS.md](references/PATTERNS.md#wcs-patterns)** for creating WCS, SIP distortions, and cutouts.

### 7. Photometry (Photutils)

Source detection and aperture photometry.

**Key operations:**
- Detect: `DAOStarFinder(fwhm=3.0, threshold=5*std)`
- Aperture: `CircularAperture(positions, r=5.0)`
- Measure: `aperture_photometry(image, apertures)`
- Background: Use `CircularAnnulus` for local background

**See [references/PATTERNS.md](references/PATTERNS.md#photometry-patterns)** for PSF photometry and grouped sources.

### 8. Spectroscopy (Specutils)

1D spectroscopy with wavelength calibration and line analysis.

**Key operations:**
- Create: `Spectrum1D(spectral_axis=wavelength, flux=flux)`
- Read: `Spectrum1D.read('spec.fits')`
- Convert: `.with_spectral_axis_unit(u.Hz)`
- Lines: `line_flux(spectrum, region)`

**See [references/PATTERNS.md](references/PATTERNS.md#spectroscopy-patterns)** for line fitting, continuum normalization, and redshift measurement.

## Patterns

See [references/PATTERNS.md](references/PATTERNS.md) for detailed patterns including:

**FITS Manipulation:**
- Multi-extension FITS handling
- Header inheritance and propagation
- Large file processing with memory mapping
- Updating headers without loading data

**Units and Quantities:**
- Custom unit definitions
- Logarithmic units (magnitudes, decibels)
- Spectral equivalencies (wavelength/frequency/energy)
- Structured arrays with units

**Coordinates:**
- Custom coordinate frames
- Efficient catalog cross-matching
- Observer-dependent coordinates (AltAz)
- Proper motion and radial velocity

**Time:**
- High-precision time arithmetic
- Time series analysis and folding
- Time zone handling
- Barycentric corrections

**Tables:**
- Masked tables for missing data
- Multi-key joins
- Table metadata and descriptions
- Fast indexing for large tables

**WCS:**
- Creating WCS from astrometry solutions
- SIP distortion polynomials
- Cutouts with WCS preservation

**Photometry:**
- PSF photometry
- Grouped source photometry
- Background subtraction strategies

**Spectroscopy:**
- Spectral line fitting
- Continuum normalization
- Redshift measurement via cross-correlation

## Real-World Examples

See [references/EXAMPLES.md](references/EXAMPLES.md) for complete workflows:

1. **Telescope Image Processing Pipeline**: FITS loading → background subtraction → source detection → aperture photometry → catalog creation with WCS

2. **Catalog Cross-Matching**: Multi-catalog matching with coordinate transformations, quality filtering, and color calculations

3. **Light Curve Analysis**: Time series handling, period search with Lomb-Scargle, phase folding, and binning

4. **Multi-Wavelength SED Construction**: Combining multi-band photometry with proper unit handling and flux conversions

5. **Spectroscopic Redshift Measurement**: Emission line identification, template cross-correlation, and redshift refinement

6. **Observability Calculation**: Target visibility from specific location, airmass calculation, sun/moon constraints

## Common Issues and Solutions

See [references/COMMON_ISSUES.md](references/COMMON_ISSUES.md) for troubleshooting:

**FITS I/O Issues:**
- VerifyError with non-standard FITS
- Memory errors with large files
- Compressed FITS handling

**Unit Problems:**
- UnitConversionError between incompatible units
- Losing units after NumPy operations
- Logarithmic unit confusion

**Coordinate Issues:**
- Frame attribute mismatches
- AltAz requiring location and time
- Slow coordinate transformations

**Time Issues:**
- Time scale confusion (UTC vs TAI vs TDB)
- ISO format parsing ambiguity
- Precision loss in calculations

**Table Issues:**
- Column type mismatches
- Units lost when writing to CSV
- Joining tables with different column names

**WCS Problems:**
- WCS transformations giving NaN
- Pixel origin convention confusion (origin=0 vs origin=1)
- SIP distortion handling

**Performance:**
- Out of memory with large FITS files
- Slow operations on large catalogs
- Vectorization strategies

## Best Practices Checklist

### Units and Quantities
- Always attach units to physical quantities
- Use `.to()` for explicit conversions
- Leverage equivalencies for wavelength/frequency/energy
- Decompose complex units to verify correctness

### FITS Files
- Use context managers (`with fits.open()`) for safe file handling
- Include descriptive header keywords with comments
- Use `memmap=True` for files larger than RAM
- Validate headers before writing

### Coordinates
- Use SkyCoord for all coordinate operations
- Specify frames explicitly
- Use catalog matching instead of manual loops
- Cache transformations for repeated use

### Time
- Specify both format and scale when creating Time objects
- Use appropriate time scale for your science (UTC for observations, TDB for dynamics)
- Work in arrays for efficiency
- Document time system in metadata

### Tables
- Use QTable to preserve units
- Add metadata (descriptions, units) to columns
- Index tables for fast lookups
- Use masked columns for missing data

### Performance
- Work with arrays instead of loops
- Use lazy loading for large FITS files
- Cache expensive computations
- Profile before optimizing

## Resources and References

### Official Documentation
- **Astropy Documentation**: https://docs.astropy.org/en/stable/
- **Astropy Tutorials**: https://learn.astropy.org/
- **Photutils**: https://photutils.readthedocs.io/
- **Specutils**: https://specutils.readthedocs.io/

### Core Modules
- **astropy.io.fits**: https://docs.astropy.org/en/stable/io/fits/
- **astropy.units**: https://docs.astropy.org/en/stable/units/
- **astropy.coordinates**: https://docs.astropy.org/en/stable/coordinates/
- **astropy.time**: https://docs.astropy.org/en/stable/time/
- **astropy.table**: https://docs.astropy.org/en/stable/table/
- **astropy.wcs**: https://docs.astropy.org/en/stable/wcs/

### Community
- **Astropy Discourse**: https://community.openastronomy.org/c/astropy
- **GitHub Issues**: https://github.com/astropy/astropy/issues
- **Stack Overflow**: Tag `astropy`

## Summary

Astropy is the foundational library for astronomical computing in Python, providing essential tools for FITS files, coordinates, units, time, tables, and more.

**Key takeaways:**

- **Units**: Always attach physical units to prevent dimensional errors
- **FITS I/O**: Standard format for astronomical images and tables
- **Coordinates**: SkyCoord simplifies transformations between reference frames
- **Time**: Sub-nanosecond precision with multiple scales and formats
- **Tables**: Flexible tabular data with unit and metadata support
- **WCS**: Maps pixel coordinates to sky positions
- **Photutils**: Source detection and aperture photometry
- **Specutils**: 1D spectroscopy with wavelength calibration

**Progressive Learning Path:**

1. Start with **FITS I/O and tables** for basic data handling
2. Learn **units and quantities** for physical calculations
3. Master **coordinates** for astrometry and sky matching
4. Explore **time handling** for time-series analysis
5. Use **WCS** for image astrometry
6. Apply **photutils** for source extraction
7. Add **specutils** for spectroscopic analysis

For detailed patterns, complete examples, and troubleshooting, see the reference files in the `references/` directory.

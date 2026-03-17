---
name: materials-databases
description: Expert assistant for accessing materials databases (AFLOW and Materials Project) - query crystal structures, materials properties, thermodynamic data, and computational results from comprehensive databases
allowed-tools: "*"
---

# Materials Databases Access Skill

You are an expert assistant for accessing and querying materials science databases, specifically AFLOW and Materials Project. Help users retrieve crystal structures, materials properties, and computational data efficiently.

## Overview

This skill enables access to two major materials databases:

1. **AFLOW** (Automatic Flow for Materials Discovery)
   - 3.5+ million calculated materials
   - Crystal structures, thermodynamic properties, elastic properties
   - No API key required for basic access
   - REST API with simple URL-based queries

2. **Materials Project** (MP)
   - 150,000+ inorganic compounds
   - Electronic structure, phonons, elasticity, surfaces, batteries
   - Requires free API key
   - Python client library (mp-api) with rich functionality

## Installation Requirements

### Materials Project (mp-api)

```bash
# Install the Materials Project API client
pip install mp-api

# Alternative: with conda
conda install -c conda-forge mp-api
```

### AFLOW

AFLOW uses REST API - no Python package installation required. However, for convenience:

```bash
# Optional: Install requests for API calls
pip install requests

# Optional: Install aflow Python package (community-maintained)
pip install aflow
```

### Additional Recommended Packages

```bash
# For structure manipulation and visualization
pip install pymatgen ase

# For data analysis
pip install pandas numpy matplotlib
```

## API Key Setup

### Materials Project API Key

1. **Get an API key:**
   - Visit: https://next-gen.materialsproject.org/api
   - Click "Generate API Key" (requires login with ORCID or email)
   - Copy your API key (format: long alphanumeric string)

2. **Set up authentication:**

   **Option A: Environment variable (recommended)**
   ```bash
   export MP_API_KEY="your_api_key_here"
   ```

   **Option B: Configuration file**
   ```bash
   # Create ~/.config/.mpapi.json or ~/.pmgrc.yaml
   echo '{"MAPI_KEY": "your_api_key_here"}' > ~/.config/.mpapi.json
   ```

   **Option C: Pass directly in code**
   ```python
   from mp_api.client import MPRester

   with MPRester("your_api_key_here") as mpr:
       # Your code here
       pass
   ```

### AFLOW

**No API key required** - AFLOW API is publicly accessible.

## Core Functionality

### Materials Project - Common Queries

**Search by formula:**
```python
from mp_api.client import MPRester

with MPRester(api_key="YOUR_API_KEY") as mpr:
    # Search for all Silicon entries
    docs = mpr.materials.summary.search(formula="Si")

    # Get specific properties
    docs = mpr.materials.summary.search(
        formula="Fe2O3",
        fields=["material_id", "formula_pretty", "band_gap", "energy_per_atom"]
    )
```

**Search by material ID:**
```python
with MPRester() as mpr:  # Uses env var or config file
    structure = mpr.get_structure_by_material_id("mp-149")
    doc = mpr.materials.summary.get_data_by_id("mp-149")
```

**Search by criteria:**
```python
with MPRester() as mpr:
    # Find materials with band gap between 1-3 eV
    docs = mpr.materials.summary.search(
        band_gap=(1, 3),
        elements=["O", "Ti"],
        num_elements=2
    )

    # Find stable materials
    docs = mpr.materials.summary.search(
        energy_above_hull=(0, 0.01),  # Nearly stable
        fields=["material_id", "formula_pretty", "energy_above_hull"]
    )
```

**Available data types:**
- `materials.summary` - General materials properties
- `materials.thermo` - Thermodynamic data
- `materials.electronic_structure` - Band structures, DOS
- `materials.phonon` - Phonon band structures
- `materials.elasticity` - Elastic tensors
- `materials.surface_properties` - Surface energies
- `molecules` - Molecular structures and properties

### AFLOW - REST API Queries

**Basic URL structure:**
```
http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/<system>/<file>?<directives>
```

**Common queries using REST:**
```python
import requests

# Get all keywords for a material
url = "http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/FCC/Ag1/?keywords"
response = requests.get(url)
data = response.text

# Get specific property (e.g., enthalpy)
url = "http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/FCC/Ag1/?enthalpy_formation_atom"
response = requests.get(url)

# Search using AFLUX (AFLOW search language)
url = "http://aflowlib.duke.edu/search/API/?species(Au),Egap(5*),catalog(ICSD)"
response = requests.get(url)
```

**Using aflow Python package (optional):**
```python
import aflow

# Search for materials
results = aflow.search(filter='species(Au),Egap(5*)')

for result in results:
    print(result.enthalpy_formation_atom)
    print(result.Egap)
    structure = result.atoms  # Get ASE Atoms object
```

**Common AFLOW directives:**
- `?keywords` - List all available properties
- `?enthalpy_formation_atom` - Formation enthalpy per atom
- `?Egap` - Band gap
- `?volume_cell` - Unit cell volume
- `?geometry` - Crystal structure (POSCAR format)
- `?files` - List all available files

**AFLUX search syntax:**
```
species(element1,element2)  # Chemical system
Egap(min*,max*)            # Band gap range (eV)
enthalpy_formation_atom(min*,max*)  # Formation enthalpy range
catalog(ICSD)              # Database catalog
```

## Workflow Guidance

### When to Use Materials Project

1. **You need electronic structure data** (band structures, DOS, Fermi surfaces)
2. **Battery materials research** (voltage, capacity calculations)
3. **Surface properties and adsorption energies**
4. **Detailed phonon calculations**
5. **Integration with pymatgen workflows**
6. **Phase stability analysis** (phase diagrams, energy above hull)

### When to Use AFLOW

1. **Large-scale materials screening** (millions of entries)
2. **Elastic properties and mechanical data**
3. **No API key setup possible/desired**
4. **ICSD-based structures** (experimental references)
5. **Quick property lookups** (simple REST calls)

### Combining Both Databases

```python
# Example: Cross-reference findings
from mp_api.client import MPRester
import requests

# Find in Materials Project
with MPRester() as mpr:
    mp_docs = mpr.materials.summary.search(
        formula="TiO2",
        fields=["material_id", "band_gap", "energy_per_atom"]
    )

# Cross-check with AFLOW
aflow_url = "http://aflowlib.duke.edu/search/API/?species(Ti,O),nspecies(2)"
aflow_data = requests.get(aflow_url).json()
```

## Best Practices

1. **Use specific queries** - Request only needed fields to reduce data transfer
   ```python
   docs = mpr.materials.summary.search(
       formula="Li",
       fields=["material_id", "formula_pretty", "band_gap"]  # Specify fields
   )
   ```

2. **Paginate large results** - Use chunk_size for large queries
   ```python
   docs = mpr.materials.summary.search(
       elements=["O"],
       num_chunks=10,  # Fetch in chunks
       chunk_size=1000
   )
   ```

3. **Cache results locally** - Save API results to avoid repeated queries
   ```python
   import pickle

   # Save results
   with open("mp_results.pkl", "wb") as f:
       pickle.dump(docs, f)
   ```

4. **Handle structures properly** - Convert between formats as needed
   ```python
   from pymatgen.io.ase import AseAtomsAdaptor

   # MP Structure → ASE Atoms
   atoms = AseAtomsAdaptor.get_atoms(structure)

   # ASE Atoms → MP Structure
   structure = AseAtomsAdaptor.get_structure(atoms)
   ```

5. **Check API status** - Materials Project has rate limits (typically generous)

## Error Handling

```python
from mp_api.client import MPRester
from mp_api.client.core import MPRestError

try:
    with MPRester() as mpr:
        docs = mpr.materials.summary.search(formula="InvalidFormula")
except MPRestError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Common Tasks

### Task 1: Find Band Gap of a Material

```python
# Materials Project
with MPRester() as mpr:
    docs = mpr.materials.summary.search(
        formula="GaN",
        fields=["material_id", "band_gap", "is_gap_direct"]
    )
    for doc in docs:
        print(f"{doc.material_id}: {doc.band_gap} eV (direct: {doc.is_gap_direct})")

# AFLOW
import requests
url = "http://aflowlib.duke.edu/search/API/?species(Ga,N),Egap"
response = requests.get(url)
```

### Task 2: Get Crystal Structure

```python
# Materials Project - returns pymatgen Structure
with MPRester() as mpr:
    structure = mpr.get_structure_by_material_id("mp-149")
    structure.to(filename="POSCAR")

# AFLOW - returns POSCAR format text
url = "http://aflowlib.duke.edu/AFLOWDATA/ICSD_WEB/FCC/Ag1/?geometry"
poscar = requests.get(url).text
```

### Task 3: Screen for Stable Materials

```python
# Find thermodynamically stable oxides with specific properties
with MPRester() as mpr:
    docs = mpr.materials.summary.search(
        elements=["O"],
        energy_above_hull=(0, 0.05),  # Stable or nearly stable
        band_gap=(1.0, 4.0),  # Semiconducting
        num_elements=(2, 3),  # Binary or ternary
        fields=["material_id", "formula_pretty", "band_gap", "energy_above_hull"]
    )
```

## References

- See `references/materials-project.md` for detailed MP API documentation
- See `references/aflow.md` for AFLOW REST API and AFLUX syntax
- See `examples/` for complete working scripts

## Key Points

- Materials Project requires API key (free); AFLOW does not
- MP has better Python integration; AFLOW uses REST API
- MP: 150k materials, rich electronic/phonon data; AFLOW: 3.5M materials, elastic properties
- Always specify fields in MP queries for efficiency
- Use pymatgen for structure manipulation and analysis
- Both databases are continuously updated with new calculations

---
name: data-journalism
description: Data journalism workflows for analysis, visualization, and storytelling. Use when analyzing datasets, creating charts and maps, cleaning messy data, calculating statistics or building data-driven stories. Essential for reporters, newsrooms and researchers working with quantitative information.
---

# Data journalism methodology

Systematic approaches for finding, analyzing and presenting data in journalism.

## Story structure for data journalism

### Data journalism framework

```markdown

The framework for data journalism was established by Philip Meyer, a journalist for Knight-Ridder, Harvard Nieman Fellow and professor at UNC-Chapel Hill. In his book <i>The New Precision Journalism</i>, which outlines his ideas, Meyer encourages journalists to treat journalism "as if it were a science" by adopting the scientific method:
- Making observation(s) / formulating a questiom
- Researching the question / Collect, store and retrieve data
- Formulate a hypothesis
- Test the hypothesis, using both qualitative (interviews, documents etc.) and quantitative (data analysis etc.) methods
- Analyze the results and reduce them to the most important findings
- Present them to the audience

This process should be thought of as iterative, rather than sequential.

## The data story arc

### 1. The hook (nut graf)
- What's the key finding(s)?
- Why should readers care?
- What's the human impact?

### 2. The evidence
- Show the data
- Explain the methodology
- Acknowledge limitations

### 3. The context
- How does this compare to past?
- How does this compare to elsewhere?
- What's the trend?

### 4. The human element
- Individual examples that illustrate the data
- Expert interpretation
- Affected voices

### 5. The implications
- What does this mean going forward?
- What questions remain?
- What actions could result?

### 6. The methodology box
- Where did data come from?
- How was it analyzed?
- What are the limitations?
- How can readers explore further?
```

### Methodology documentation template

```markdown
## How we did this analysis

### Data sources
[List all data sources with links and access dates]

### Time period
[Specify exactly what time period is covered]

### Definitions
[Define key terms and how you operationalized them]

### Analysis steps
1. [First step of analysis]
2. [Second step]
3. [Continue...]

### Limitations
- [Limitation 1]
- [Limitation 2]

### What we excluded and why
- [Excluded category]: [Reason]

### Verification
[How findings were verified/checked]

### Code and data availability
[Link to GitHub repo if sharing code/data]

### Contact
[How readers can reach you with questions]
```

## Data acquisition

### Public data sources

```markdown
## Federal data sources

### General
- Data.gov - Federal open data portal
- Census Bureau (census.gov) - Demographics, economic data
- BLS (bls.gov) - Employment, inflation, wages
- BEA (bea.gov) - GDP, economic accounts
- Federal Reserve (federalreserve.gov) - Financial data
- SEC EDGAR - Corporate filings

### Specific domains
- EPA (epa.gov/data) - Environmental data
- FDA (fda.gov/data) - Drug approvals, recalls, adverse events
- CDC WONDER - Health statistics
- NHTSA - Vehicle safety data
- DOT - Transportation statistics
- FEC - Campaign finance
- USASpending.gov - Federal contracts and grants

### State and local
- State open data portals (search: "[state] open data")
- Socrata-powered sites (many cities/states)
- OpenStreets, municipal GIS portals
- State comptroller/auditor reports
```

### Data request strategies

```markdown
## Getting data that isn't public

### Public records request (ie. FOIA) for datasets
- Request databases, not just documents
- Ask for data dictionary/schema
- Request in native format (CSV, SQL dump)
- Specify field-level needs

### Building your own dataset
- Scraping public information
- Crowdsourcing from readers
- Systematic document review
- Surveys (with proper methodology)

### Commercial data sources (for newsrooms)
- LexisNexis
- Refinitiv
- Bloomberg
- Industry-specific databases
```

## Data cleaning and preparation

### Common data problems

```python
from typing import Any

import pandas as pd
import numpy as np
from rapidfuzz import fuzz
from itertools import combinations

# Inflation adjustment
import cpi
import wbdata

def standardize_name(name: Any) -> str | None:
    """Standardize name format to 'First Last'."""
    if pd.isna(name):
        return None
    name = str(name).strip().upper()
    # Handle "LAST, FIRST" format
    if ',' in name:
        parts = name.split(',')
        name = f"{parts[1].strip()} {parts[0].strip()}"
    return name

def parse_date(date_str: Any) -> pd.Timestamp | None:
    """Parse dates in various formats."""
    if pd.isna(date_str):
        return None

    formats = [
        '%m/%d/%Y', '%Y-%m-%d', '%B %d, %Y',
        '%d-%b-%y', '%m-%d-%Y', '%Y/%m/%d'
    ]

    for fmt in formats:
        try:
            return pd.to_datetime(date_str, format=fmt)
        except:
            continue

    # Fall back to pandas parser
    try:
        return pd.to_datetime(date_str)
    except:
        return None


def handle_missing(df:pd.DataFrame, thresh:int | None, per_thresh:float | None, required_col:str | None) -> pd.DataFrame:
    '''Handles Dataframes with too many missing values, defined by the user.''' 
    if thresh and data_clean.isna().sum() >= thresh:
        return df.dropna(subset=[required_col]).reset_index(drop=True).copy()
    
    elif per_thresh and (data_clean.isna().sum() / len(data_clean) * 100) >= per_thresh:
        return df.dropna(subset=[required_col]).reset_index(drop=True).copy()
    
    else:
        return df


def handle_duplicates(df:pd.DataFrame, thresh=int | None)
    '''Handle duplicate rows of data.'''
    if thresh and df.duplicated().sum() >= thresh:
        return df.drop_duplicates().reset_index(drop=True).copy()
    else:
        return df


def flag_similar_names(df: pd.DataFrame, name_col: str, threshold: int = 85) -> pd.DataFrame:
    """Flag rows that have potential duplicate names using vectorized comparison."""
    
    names = df[name_col].dropna().unique()
    
    # Use combinations() to avoid nested loop and duplicate comparisons
    dup_names: set[Any] = {
        name
        for name1, name2 in combinations(names, 2)
        if fuzz.ratio(str(name1).lower(), str(name2).lower()) >= threshold
        for name in (name1, name2)
    }
    
    df['has_similar_name'] = df[name_col].isin(dup_names)
    return df


def flag_outliers(series: pd.Series, method: str = 'iqr', threshold: float = 1.5) -> pd.Series:
    """Flag statistical outliers."""
    if method == 'iqr':
        Q1 = series.quantile(0.25)
        Q3 = series.quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - threshold * IQR
        upper = Q3 + threshold * IQR
        return (series < lower) | (series > upper)
    elif method == 'zscore':
        z_scores = np.abs((series - series.mean()) / series.std())
        return z_scores > threshold



# use descriptive variable names and chain methods
data_clean = (pd

            # Load messy data — raw_data is a placeholder
            # Be sure to use the right reader for the filetype
            .read_csv('..data/raw/raw_data.csv')

            # DATA TYPE CORRECTIONS
            # Ensure proper types for analysis
            .assign(# Convert to numeric (handling errors)
                    amount = lambda x: pd.to_numeric(x['amount'], errors='coerce'),
                    
                    # Convert to categorical (saves memory, enables ordering)
                    status = lambda x: pd.to_Categorical(x['status'])) 
            
            .assign(
                    # INCONSISTENT FORMATTING
                    # Problem: Names in different formats
                    # ie. "SMITH, JOHN" vs "John Smith" vs "smith john"
                    name_clean = lambda x: standaridize_name(x['name']),
                    
                    # DATE INCONSISTENCIES
                    # Problem: Dates in multiple formats
                    # ie. "01/15/2024", "2024-01-15", "January 15, 2024", "15-Jan-24"
                    parse_date = lambda x: parse_date(x['date']),
                    
                    # OUTLIERS
                    # Identify potential data entry errors
                    amount_outlier = lambda x: flag_outliers(x['amount']),
                    
                    )
            
            # Fuzzy duplicates (similar but not identical)
            # Use record linkage or manual review
            .pipe(find_similar_names, name_col='name_clean', threshold=85)

            # MISSING VALUES
            # Strategy depends on context
            # First check missing value patterns
            .pipe(handle_missing, thresh=None, per_thresh=None)

            # DUPLICATES — Find and handle duplicates
            .pipe(handle_duplicates, thresh=None)
            
            .reset_index(drop=True)
            .copy())


```

### Data validation checklist

```markdown
## Pre-analysis data validation

### Structural checks
- [ ] Row count matches expected
- [ ] Column count and names correct
- [ ] Data types appropriate
- [ ] No unexpected null columns

### Content checks
- [ ] Date ranges make sense
- [ ] Numeric values within expected bounds
- [ ] Categorical values match expected options
- [ ] Geographic data resolves correctly
- [ ] IDs are unique where expected

### Consistency checks
- [ ] Totals add up to expected values
- [ ] Cross-tabulations balance
- [ ] Related fields are consistent
- [ ] Time series is continuous

### Source verification
- [ ] Can trace back to original source
- [ ] Methodology documented
- [ ] Known limitations noted
- [ ] Update frequency understood
```

## Statistical analysis for journalism

### Basic statistics with context

```python
# Essential statistics for any dataset
def describe_for_journalism(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Generate journalist-friendly statistics."""
    stats = df[col].describe(percentiles=[0.25, 0.5, 0.75, 0.9, 0.99])
    
    # Add skewness to the describe() output
    stats['skewness'] = df[col].skew()
    
    return stats.to_frame(name=col)

# Example interpretation
stats = describe_for_journalism(salaries, 'salary')

print(f"""
ANALYSIS
---------------
We analyzed {stats['count']:,} salary records.

The median salary is ${stats['median']:,.0f}, meaning half of workers
earn more and half earn less.

The average salary is ${stats['mean']:,.0f}, which is
{'higher' if stats['mean'] > stats['median'] else 'lower'} than the median,
indicating the distribution is {'right-skewed (pulled up by high earners)'
if stats['skewness'] > 0 else 'left-skewed'}.

The top 10% of earners make at least ${stats['90th_percentile']:,.0f}.
The top 1% make at least ${stats['99th_percentile']:,.0f}.
""")
```

### Comparisons and context

```python
# Calculate change metrics for a column
def calculate_change(df: pd.DataFrame, col: str, periods: int = 1) -> pd.DataFrame:
    """Add change metrics to a DataFrame using built-in pandas methods.
    
    Args:
        df: Input DataFrame
        col: Column to calculate changes for
        periods: Number of rows to look back (1=previous row, 12=year-over-year for monthly)
    """
    return df.assign(
        absolute_change=df[col].diff(periods),
        percent_change=df[col].pct_change(periods) * 100,
        direction=np.sign(df[col].diff(periods)).map({1: 'increased', -1: 'decreased', 0: 'unchanged'})
    )

# Usage:
# changes = data_clean.pipe(calculate_change, 'revenue', periods=12) # Year-over-year for monthly data

# Per capita calculations (essential for fair comparisons)
def per_capita(value: float, population: float, multiplier: int = 100000) -> float:
    """Calculate per capita rate."""
    return (value / population) * multiplier  # Per 100,000 is standard

# Example: Crime rates
city_a = {'crimes': 5000, 'population': 100000}
city_b = {'crimes': 8000, 'population': 500000}

rate_a = per_capita(city_a['crimes'], city_a['population'])
rate_b = per_capita(city_b['crimes'], city_b['population'])

print(f"City A: {rate_a:.1f} crimes per 100,000 residents")
print(f"City B: {rate_b:.1f} crimes per 100,000 residents")
# City A actually has higher crime rate despite fewer total crimes!


def adjust_for_inflation(
    amount: float | pd.Series, 
    from_year: int | pd.Series, 
    to_year: int,
    country: str = 'US'
) -> float | pd.Series:
    """Adjust dollar amounts for inflation. Works with scalars or Series for .assign().
    
    Args:
        amount: Value(s) to adjust
        from_year: Original year(s) of the amount
        to_year: Target year to adjust to
        country: ISO 2-letter country code (default 'US'). US uses BLS data via cpi package,
                 others use World Bank CPI data (FP.CPI.TOTL indicator)
    """
    if country == 'US':
        # Use cpi package for US (more accurate, from BLS)
        if isinstance(from_year, pd.Series):
            return pd.Series([cpi.inflate(amt, yr, to=to_year) 
                            for amt, yr in zip(amount, from_year)], index=amount.index)
        return cpi.inflate(amount, from_year, to=to_year)
    else:
        # Use World Bank data for other countries
        cpi_data = wbdata.get_dataframe(
            {'FP.CPI.TOTL': 'cpi'}, 
            country=country
        )['cpi'].to_dict()
        
        from_cpi = pd.Series(from_year).map(cpi_data) if isinstance(from_year, pd.Series) else cpi_data[from_year]
        to_cpi = cpi_data[to_year]
        return amount * (to_cpi / from_cpi)

# Usage:
# adjust_for_inflation(100, 2020, 2024)  # US by default
# adjust_for_inflation(100, 2020, 2024, country='GB')  # UK
# df.assign(inf_adjust24=lambda x: adjust_for_inflation(x['amount'], x['year'], 2024, country='DE'))

# Always adjust when comparing dollars across years!
```

### Correlation vs causation

```markdown
## Reporting correlations responsibly

### What you CAN say
- "X and Y are correlated"
- "As X increases, Y tends to increase"
- "Areas with higher X also tend to have higher Y"
- "X is associated with Y"

### What you CANNOT say (without more evidence)
- "X causes Y"
- "X leads to Y"
- "Y happens because of X"

### Questions to ask before implying causation
1. Is there a plausible mechanism?
2. Does the timing make sense (cause before effect)?
3. Is there a dose-response relationship?
4. Has the finding been replicated?
5. Have confounding variables been controlled?
6. Are there alternative explanations?

### Red flags for spurious correlations
- Extremely high correlation (r > 0.95) with unrelated things
- No logical connection between variables
- Third variable could explain both
- Small sample size with high variance
```

## Data visualization

### Chart selection guide

```markdown
## Choosing the right chart

### Comparison
- **Bar chart**: Compare categories
- **Grouped bar**: Compare categories across groups
- **Bullet chart**: Actual vs target

### Change over time
- **Line chart**: Trends over time
- **Area chart**: Cumulative totals over time
- **Slope chart**: Change between two points

### Distribution
- **Histogram**: Distribution of one variable
- **Box plot**: Compare distributions across groups
- **Violin plot**: Detailed distribution shape

### Relationship
- **Scatter plot**: Relationship between two variables
- **Bubble chart**: Three variables (x, y, size)
- **Connected scatter**: Change in relationship over time

### Composition
- **Pie chart**: Parts of a whole (almost never use, max 5 slices, prefer donut charts)
- **Donut chart**: Parts of a whole
- **Stacked bar**: Parts of whole across categories
- **Treemap**: Hierarchical composition

### Geographic
- **Choropleth**: Values by region (use normalized data!)
- **Dot map**: Individual locations
- **Proportional symbol**: Magnitude at locations
```

### Exploratory interactive visualizations with Plotly Express

```python
import plotly.express as px

# Set default template for all charts
px.defaults.template = 'simple_white'

def create_bar_chart(
    data: pd.DataFrame, 
    title: str, 
    source: str,
    desc: str  = '', 
    x_val: str, 
    y_val: str,
    x_lab: str | None,
    y_lab: str | None
) -> px.bar:
    """Create a bar chart."""
    
    fig = px.bar(
        data, 
        x=x_val, 
        y=y_val,
        text=desc,
        title=title,
        labels={'category': (x_lab if x_lab else x_val), 'value': (y_lab if y_lab else y_val)}
    )
    
    return fig

# Example
fig = create_bar_chart(
    data,
    title='Annual Widget Production',
    source='Department of Widgets, 2024',
    desc='The widget department increased its production dramatically starting in 2014.',
    x_val='year',
    y_val='widgets_prod',
    x_lab='Year',
    y_label='Units produced'
)

fig.show()  # Interactive display
```

### Publication-ready automated data visualizations with Datawrapper
```python
import pandas as pd
import datawrapper as dw

# Authentication: Set DATAWRAPPER_ACCESS_TOKEN environment variable, 
# or read from file and pass to create()
with open('datawrapper_api_key.txt', 'r') as f:
    api_key = f.read().strip()

# read in your data
data = pd.read_csv('../data/raw/data.csv')

# Create a bar chart using the new OOP API
chart = dw.BarChart(
    title='My Bar Chart Title',
    intro='Subtitle or description text',
    data=data,

    # Formatting options
    value_label_format=dw.NumberFormat.ONE_DECIMAL,
    show_value_labels=True,
    value_label_alignment='left',
    sort_bars=True,  # sort by value
    reverse_order=False,

    # Source attribution
    source_name='Your Data Source',
    source_url='https://example.com',
    byline='Your Name',

    # Optional: custom base color
    base_color='#1d81a2'
)

# Create and publish (uses DATAWRAPPER_ACCESS_TOKEN env var, or pass token)
chart.create(access_token=api_key)
chart.publish()

# Get chart URL and embed code
print(f"Chart ID: {chart.chart_id}")
print(f"Chart URL: https://datawrapper.dwcdn.net/{chart.chart_id}")
iframe_code = chart.get_iframe_code(responsive=True)

# Update existing chart with new data (for live-updating charts)
existing_chart = dw.get_chart('YOUR_CHART_ID')  # retrieve by ID
existing_chart.data = new_df  # assign new DataFrame
existing_chart.title = 'Updated Title'  # modify properties
existing_chart.update()  # push changes to Datawrapper
existing_chart.publish()  # republish to make live

# Optional — Export chart as image
chart.export(filepath='chart.png', width=800, height=600)

#view chart
chart
```

### Avoiding misleading visualizations

```markdown
## Chart integrity checklist

### Axes
- [ ] Y-axis starts at zero (for bar charts)
- [ ] Axis labels are clear
- [ ] Scale is appropriate (not truncated to exaggerate)
- [ ] Both axes labeled with units

### Data representation
- [ ] All data points visible
- [ ] Colors are distinguishable (including colorblind)
- [ ] Proportions are accurate
- [ ] 3D effects not distorting perception

### Context
- [ ] Title describes what's shown, not conclusion
- [ ] Time period clearly stated
- [ ] Source cited
- [ ] Sample size/methodology noted if relevant
- [ ] Uncertainty shown where appropriate

### Honesty
- [ ] Cherry-picking dates avoided
- [ ] Outliers explained, not hidden
- [ ] Dual axes justified (usually avoid)
- [ ] Annotations don't mislead
```
## Working with geospatial data

### Geocoding data

#### U.S. Census Geocoder

**Best for:** U.S. addresses only. Returns Census geography (tract, block, FIPS codes) along with coordinates—essential for joining with Census demographic data.

**Pros:** Completely free with no API key required. Returns Census geographies (state/county FIPS, tract, block) that let you join with ACS/decennial Census data. Good match rates for standard U.S. addresses.

**Cons:** Limited to 10,000 addresses per batch. U.S. addresses only. Slower than commercial alternatives. Lower match rates for non-standard addresses (PO boxes, rural routes, new construction).

**Use when:** You need to geocode nicely formatted U.S. addresses or you don't have budget for a paid service. 

```python
# pip install censusbatchgeocoder
import censusbatchgeocoder
import pandas as pd

# DataFrame must have columns: id, address, city, state, zipcode
# (state and zipcode are optional but improve match rates)

def census_geocode(
    df: pd.DataFrame,
    id_col: str = 'id',
    address_col: str = 'address',
    city_col: str = 'city',
    state_col: str = 'state',
    zipcode_col: str = 'zipcode',
    chunk_size: int = 9999
) -> pd.DataFrame:
    """
    Geocode a DataFrame using the U.S. Census batch geocoder.
    Automatically handles datasets larger than 10,000 rows by chunking.
    
    Returns DataFrame with: latitude, longitude, state_fips, county_fips, 
    tract, block, is_match, is_exact, returned_address, geocoded_address
    """
    # Rename columns to expected format
    col_map = {id_col: 'id', address_col: 'address', city_col: 'city'}
    if state_col and state_col in df.columns:
        col_map[state_col] = 'state'
    if zipcode_col and zipcode_col in df.columns:
        col_map[zipcode_col] = 'zipcode'
    
    renamed_df = df.rename(columns=col_map)
    records = renamed_df.to_dict('records')
    
    # Small dataset: geocode directly
    if len(records) <= chunk_size:
        results = censusbatchgeocoder.geocode(records)
        return pd.DataFrame(results)
    
    # Large dataset: process in chunks to stay under 10,000 limit
    all_results = []
    for i in range(0, len(records), chunk_size):
        chunk = records[i:i + chunk_size]
        print(f"Geocoding rows {i:,} to {i + len(chunk):,} of {len(records):,}...")
        
        try:
            results = censusbatchgeocoder.geocode(chunk)
            all_results.extend(results)
        except Exception as e:
            print(f"Error on chunk starting at {i}: {e}")
            for record in chunk:
                all_results.append({**record, 'is_match': 'No_Match', 'latitude': None, 'longitude': None})
    
    return pd.DataFrame(all_results)

# Usage:
geocoded = (pd
              .read_csv('../data/raw/addresses.csv')
              .assign(id=lambda x: x.index)
              .pipe(census_geocode, 
                    id_col='id', 
                    address_col='street', 
                    city_col='city'.
                    state_col='state',
                    zipcode_col='zip'))
```

#### Google Maps Geocoder

**Best for:** International addresses, high match rates, and messy/non-standard address formats.

**Pros:** Excellent match rates even for poorly formatted addresses. Works worldwide. Fast and reliable. Returns rich metadata (place types, address components, place IDs).

**Cons:** Costs money ($5 per 1,000 requests after free tier). Requires API key and billing account. Does not return Census geography—you'd need to do a separate spatial join.

**Use when:** You need to geocode international addresses, have messy address data that the Census geocoder can't match, or need the highest possible match rate and have budget for it.

```python
import googlemaps
from typing import Optional

def geocode_address_google(address: str, api_key: str) -> Optional[dict]:
    """
    Geocode address using Google Maps API.
    Requires API key with Geocoding API enabled.
    """
    gmaps = googlemaps.Client(key=api_key)
    result = gmaps.geocode(address)
    
    if result:
        location = result[0]['geometry']['location']
        return {
            'formatted_address': result[0]['formatted_address'],
            'lat': location['lat'],
            'lon': location['lng'],
            'place_id': result[0]['place_id']
        }
    return None

# Batch geocode a DataFrame
def batch_geocode(df: pd.DataFrame, address_col: str, api_key: str) -> pd.DataFrame:
    gmaps = googlemaps.Client(key=api_key)
    
    results = []
    for address in df[address_col]:
        try:
            result = gmaps.geocode(address)
            if result:
                loc = result[0]['geometry']['location']
                results.append({'lat': loc['lat'], 'lon': loc['lng']})
            else:
                results.append({'lat': None, 'lon': None})
        except Exception:
            results.append({'lat': None, 'lon': None})
    
    return pd.concat([df, pd.DataFrame(results)], axis=1)
```

### Geopandas
```python
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Read data from various formats
gdf = gpd.read_file('data.geojson')                    # GeoJSON
gdf = gpd.read_file('data.shp')                         # Shapefile
gdf = gpd.read_file('https://example.com/data.geojson') # From URL
gdf = gpd.read_parquet('data.parquet')                  # GeoParquet (fast!)

# Transform DataFrame with lat/lon to GeoDataFrame
df = pd.read_csv('locations.csv')
geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry)

# Set CRS (Coordinate Reference System)
# EPSG:4326 = WGS84 (standard latitude, longitude)
gdf = gdf.set_crs('EPSG:4326')

# Transform to different CRS (for area/distance calculations, use projected CRS)
gdf_projected = gdf.to_crs('EPSG:3857')  # Web Mercator, for distance in meters

# Basic spatial operations

#Find the area of a shape
gdf['area'] = gdf_projected.geometry.area 

#Find the center of a shape
gdf['centroid'] = gdf.geometry.centroid

#Draw a 1km boundary around a point
gdf['buffer_1km'] = gdf_projected.geometry.buffer(1000) #when set to CRS 3857

# Spatial join: find points within polygons
points = gpd.read_file('points.geojson')
polygons = gpd.read_file('boundaries.geojson')
joined = gpd.sjoin(points, polygons, predicate='within')

# Dissolve: merge geometries by attribute
dissolved = gdf.dissolve(by='state', aggfunc='sum')

# Export to various formats
gdf.to_parquet('output.parquet')          # GeoParquet (recommended)
gdf.to_file('output.geojson', driver='GeoJSON') #for tools that dont support GeoParquet
```

### Geo-Visualization with `.explore()`, `lonboard` and Datawrapper

#### `.explore()`

**Best for:** Quick exploration and prototyping during data analysis.

**Pros:** Built into GeoPandas—method is available on any GeoDataFrame. Great for exploratory data analysis—checking that your data looks right, exploring spatial patterns, and iterating quickly on map designs.

**Cons:** Becomes slow with large datasets (>100k features). Limited customization compared to dedicated mapping libraries. Requires extra dependencies to be installed.

**Use when:** You're in the middle of analysis and want to quickly visualize your GeoDataFrame without switching tools.

**Required dependencies:**
```bash
pip install folium mapclassify matplotlib
```
- `folium` - Required for `.explore()` to work at all (renders the interactive map)
- `mapclassify` - Required when using `scheme=` parameter for classification (e.g., 'naturalbreaks', 'quantiles', 'equalinterval')
- `matplotlib` - Required for colormap (`cmap=`) support

```python
import geopandas as gpd
# folium, mapclassify, and matplotlib must be installed but don't need to be imported
# geopandas imports them automatically when you call .explore()

# Basic interactive map (uses folium under the hood)
gdf.explore()

# Choropleth map with customization
# (requires mapclassify for scheme parameter)
gdf.explore(
    column='population',           # Column for color scale
    cmap='YlOrRd',                 # Matplotlib colormap
    scheme='naturalbreaks',        # Classification scheme (needs mapclassify)
    k=5,                           # Number of bins
    legend=True,
    tooltip=['name', 'population'],  # Columns to show on hover
    popup=True,                    # Show all columns on click
    tiles='CartoDB positron',      # Background tiles
    style_kwds={'color': 'black', 'weight': 0.5}  # Border style
)
```

#### `lonboard`

**Best for:** Large datasets and high-performance visualization in Jupyter notebooks.

**Pros:** GPU-accelerated rendering via deck.gl can handle millions of points smoothly. Excellent interactivity—pan, zoom, and hover work fluidly even with massive datasets. Native support for GeoArrow format for efficient data transfer.

**Cons:** Requires separate installation (`pip install lonboard`). Styling options are more technical (RGBA arrays, deck.gl conventions). 

**Use when:** You have large point datasets (crime incidents, sensor readings, business locations) or need smooth interactivity with 100k+ features.

```python
import geopandas as gpd
from lonboard import viz, Map, ScatterplotLayer, PolygonLayer

# Quick visualization (auto-detects geometry type)
viz(gdf)

# Custom ScatterplotLayer for points
layer = ScatterplotLayer.from_geopandas(
    gdf,
    get_radius=100,
    get_fill_color=[255, 0, 0, 200],  # RGBA
    pickable=True
)
m = Map(layer)
m

# PolygonLayer with color based on column
from lonboard.colormap import apply_continuous_cmap
import matplotlib.pyplot as plt

colors = apply_continuous_cmap(gdf['value'], plt.cm.viridis)
layer = PolygonLayer.from_geopandas(
    gdf,
    get_fill_color=colors,
    get_line_color=[0, 0, 0, 100],
    pickable=True
)
Map(layer)
```

#### Datawrapper

**Best for:** Publication-ready choropleth and proportional symbol maps for articles and reports.

**Pros:** Beautiful, professional defaults out of the box. Generates embeddable, responsive iframes that work in any CMS. Readers can interact (hover, click) without running any code. Accessible and mobile-friendly. Easy to update data programmatically for updating data.

**Cons:** Requires a Datawrapper account (free tier available). Limited to Datawrapper's supported boundary files—you can't bring arbitrary geometries. Less flexibility for custom visualizations.

**Use when:** You need a polished map for publication. Ideal for choropleth maps showing statistics by region (unemployment by state, COVID cases by county, election results by district). Your audience will view the map in a browser, not a notebook.

Unlike `.explore()` or `lonboard`, you don't pass raw geometry—instead you match your data to Datawrapper's built-in boundary files using standard codes (FIPS, ISO, etc.).

```python
import datawrapper as dw
import pandas as pd

# Read API key
with open('datawrapper_api_key.txt', 'r') as f:
    api_key = f.read().strip()

# Prepare data with location codes that match Datawrapper's boundaries
# For US states: use 2-letter abbreviations or FIPS codes
# For countries: use ISO 3166-1 alpha-2 codes
df = pd.DataFrame({
    'state': ['AL', 'AK', 'AZ', 'AR', 'CA'],  # State abbreviations
    'unemployment_rate': [4.9, 3.2, 7.1, 4.2, 5.8]
})

# Create a choropleth map
chart = dw.ChoroplethMap(
    title='Unemployment Rate by State',
    intro='Percentage of labor force unemployed, 2024',
    data=df,

    # Map configuration
    basemap='us-states',           # Built-in US states boundaries
    basemap_key='state',           # Column in your data with location codes
    value_column='unemployment_rate',

    # Styling
    color_palette='YlOrRd',        # Color scheme
    legend_title='Unemployment %',

    # Attribution
    source_name='Bureau of Labor Statistics',
    source_url='https://www.bls.gov/',
    byline='Your Name'
)

# Create and publish
chart.create(access_token=api_key)
chart.publish()

# Get embed code for your article
iframe = chart.get_iframe_code(responsive=True)
print(f"Chart URL: https://datawrapper.dwcdn.net/{chart.chart_id}")

# Update with new data (for live-updating maps)
new_df = pd.DataFrame({...})  # Updated data
existing_chart = dw.get_chart('YOUR_CHART_ID')
existing_chart.data = new_df
existing_chart.update()
existing_chart.publish()
```

**Available Datawrapper basemaps include:**
- `us-states`, `us-counties`, `us-congressional-districts`
- `world`, `europe`, `africa`, `asia`
- Country-specific maps (e.g., `germany-states`, `uk-constituencies`)

### Learning resources

- NICAR (Investigative Reporters & Editors)
- Knight Center for Journalism in the Americas
- Data Journalism Handbook (datajournalism.com)
- Flowing Data (flowingdata.com)
- The Pudding (pudding.cool) - examples
- Sigma Awards (https://www.sigmaawards.org/) - examples

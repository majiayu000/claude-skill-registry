---
name: bsee-sodir-extraction
version: 1.0.0
description: Extract and process energy data from BSEE (Gulf of Mexico) and SODIR (Norway) regulatory databases
author: workspace-hub
category: data-analysis
tags: [bsee, sodir, energy-data, oil-gas, offshore, web-scraping, api]
platforms: [python]
---

# BSEE/SODIR Data Extraction Skill

Master data extraction from the Bureau of Safety and Environmental Enforcement (BSEE) and Norwegian Offshore Directorate (SODIR) for comprehensive offshore energy analysis.

## When to Use This Skill

Use BSEE/SODIR data extraction when you need:
- **Production data** - Oil, gas, water production by field/well
- **Well information** - Directional surveys, completions, drilling data
- **Field data** - Reserves, operators, development status
- **HSE data** - Safety incidents, environmental compliance
- **Economic analysis** - NPV calculations using regulatory data
- **Regulatory compliance** - Track permits, violations, inspections

**Data sources covered:**
- **BSEE (US Gulf of Mexico)**: Production, wells, platforms, safety
- **SODIR (Norway)**: Fields, production, wells, discoveries
- **NPD FactPages**: Norwegian petroleum data (legacy)

## Core Capabilities

### 1. BSEE Data Extraction

**Available datasets:**
- Production data (monthly oil/gas/water)
- Well data (API numbers, directional surveys)
- Platform/structure data
- Operator information
- Safety and incident data (OCS incidents)
- Environmental compliance

**Base URLs:**
```python
BSEE_BASE_URLS = {
    "production": "https://www.data.bsee.gov/Production/",
    "well": "https://www.data.bsee.gov/Well/",
    "platform": "https://www.data.bsee.gov/Platform/",
    "company": "https://www.data.bsee.gov/Company/",
    "field": "https://www.data.bsee.gov/Field/",
    "incidents": "https://www.data.bsee.gov/Incidents/",
}
```

**Production Data Extraction:**
```python
import pandas as pd
import requests
from pathlib import Path
from datetime import datetime
from typing import Optional


def fetch_bsee_production_data(
    year: int,
    output_dir: Path,
    area_code: Optional[str] = None
) -> pd.DataFrame:
    """
    Fetch BSEE production data for a given year.

    Args:
        year: Production year (e.g., 2024)
        output_dir: Directory to save downloaded data
        area_code: Optional area filter ('GC', 'MC', 'WR', etc.)

    Returns:
        DataFrame with production data
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # BSEE provides production data as downloadable files
    url = f"https://www.data.bsee.gov/Production/Files/ogoraan{year}.zip"

    # Download file
    response = requests.get(url, timeout=60)
    response.raise_for_status()

    zip_path = output_dir / f"production_{year}.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    # Extract and read
    import zipfile
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)

    # Read the extracted CSV
    csv_files = list(output_dir.glob(f"*{year}*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV found for {year}")

    df = pd.read_csv(csv_files[0])

    # Filter by area if specified
    if area_code:
        df = df[df["AREA_CODE"] == area_code]

    # Clean column names
    df.columns = df.columns.str.strip().str.upper()

    # Add metadata
    df["EXTRACTION_DATE"] = datetime.now().isoformat()
    df["SOURCE"] = "BSEE"

    print(f"Fetched {len(df)} production records for {year}")

    return df


def aggregate_production_by_field(
    df: pd.DataFrame,
    time_period: str = "monthly"
) -> pd.DataFrame:
    """
    Aggregate production data by field.

    Args:
        df: Raw production DataFrame
        time_period: 'monthly', 'quarterly', or 'annual'

    Returns:
        Aggregated production DataFrame
    """
    # Group by field
    group_cols = ["FIELD_NAME", "AREA_CODE", "BLOCK_NUMBER"]

    if time_period == "monthly":
        group_cols.extend(["PRODUCTION_YEAR", "PRODUCTION_MONTH"])
    elif time_period == "quarterly":
        df["QUARTER"] = ((df["PRODUCTION_MONTH"] - 1) // 3) + 1
        group_cols.extend(["PRODUCTION_YEAR", "QUARTER"])
    else:  # annual
        group_cols.append("PRODUCTION_YEAR")

    # Aggregate
    agg_dict = {
        "OIL_BBL": "sum",
        "GAS_MCF": "sum",
        "WATER_BBL": "sum",
        "WELL_COUNT": "nunique" if "API_NUMBER" in df.columns else "count"
    }

    # Only aggregate columns that exist
    agg_dict = {k: v for k, v in agg_dict.items() if k in df.columns}

    aggregated = df.groupby(group_cols).agg(agg_dict).reset_index()

    return aggregated


# Example usage
production_2024 = fetch_bsee_production_data(
    year=2024,
    output_dir=Path("data/raw/bsee"),
    area_code="GC"  # Green Canyon
)

field_production = aggregate_production_by_field(
    production_2024,
    time_period="monthly"
)

print(field_production.head())
```

**Well Data Extraction:**
```python
def fetch_bsee_well_data(
    api_number: Optional[str] = None,
    field_name: Optional[str] = None,
    output_dir: Path = Path("data/raw/bsee")
) -> pd.DataFrame:
    """
    Fetch BSEE well data.

    Args:
        api_number: Specific API number (14-digit)
        field_name: Filter by field name
        output_dir: Output directory

    Returns:
        DataFrame with well data
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # BSEE Well File download
    url = "https://www.data.bsee.gov/Well/Files/Well.zip"

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    zip_path = output_dir / "well_data.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    import zipfile
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)

    # Read well data
    well_file = output_dir / "Well.csv"
    df = pd.read_csv(well_file)

    # Filter if specified
    if api_number:
        df = df[df["API_WELL_NUMBER"] == api_number]
    if field_name:
        df = df[df["FIELD_NAME"].str.contains(field_name, case=False, na=False)]

    return df


def fetch_directional_surveys(
    api_number: str,
    output_dir: Path = Path("data/raw/bsee")
) -> pd.DataFrame:
    """
    Fetch directional survey data for a well.

    Args:
        api_number: 14-digit API number
        output_dir: Output directory

    Returns:
        DataFrame with directional survey points
    """
    # BSEE provides directional survey data
    url = f"https://www.data.bsee.gov/Well/DirectionalSurvey/Files/DirectionalSurvey.zip"

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    zip_path = output_dir / "directional_surveys.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    import zipfile
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)

    survey_file = output_dir / "DirectionalSurvey.csv"
    df = pd.read_csv(survey_file)

    # Filter by API
    df = df[df["API_WELL_NUMBER"] == api_number]

    # Sort by measured depth
    df = df.sort_values("MEASURED_DEPTH")

    return df


# Example: Get well data for a deepwater field
gom_wells = fetch_bsee_well_data(field_name="THUNDER HORSE")
print(f"Found {len(gom_wells)} wells in Thunder Horse field")
```

**HSE Data Extraction:**
```python
def fetch_bsee_incident_data(
    start_year: int = 2020,
    end_year: int = 2024,
    output_dir: Path = Path("data/raw/bsee")
) -> pd.DataFrame:
    """
    Fetch BSEE incident/accident data.

    Args:
        start_year: Start year for data
        end_year: End year for data
        output_dir: Output directory

    Returns:
        DataFrame with incident records
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Fetch incident data
    url = "https://www.data.bsee.gov/Incidents/Files/Accidents.zip"

    response = requests.get(url, timeout=120)
    response.raise_for_status()

    zip_path = output_dir / "incidents.zip"
    with open(zip_path, "wb") as f:
        f.write(response.content)

    import zipfile
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)

    incident_file = output_dir / "Accidents.csv"
    df = pd.read_csv(incident_file)

    # Convert date columns
    df["INCIDENT_DATE"] = pd.to_datetime(df["INCIDENT_DATE"], errors="coerce")

    # Filter by year range
    df = df[
        (df["INCIDENT_DATE"].dt.year >= start_year) &
        (df["INCIDENT_DATE"].dt.year <= end_year)
    ]

    return df


def calculate_operator_safety_score(
    incidents_df: pd.DataFrame,
    production_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Calculate safety score per operator based on incidents per production.

    Args:
        incidents_df: Incident data
        production_df: Production data

    Returns:
        DataFrame with operator safety metrics
    """
    # Count incidents by operator
    incident_counts = incidents_df.groupby("OPERATOR_NAME").agg({
        "INCIDENT_ID": "count",
        "FATALITY_COUNT": "sum",
        "INJURY_COUNT": "sum"
    }).rename(columns={
        "INCIDENT_ID": "TOTAL_INCIDENTS",
        "FATALITY_COUNT": "TOTAL_FATALITIES",
        "INJURY_COUNT": "TOTAL_INJURIES"
    })

    # Sum production by operator
    production_totals = production_df.groupby("OPERATOR_NAME").agg({
        "OIL_BBL": "sum",
        "GAS_MCF": "sum"
    })

    # Merge
    safety_df = incident_counts.join(production_totals, how="outer").fillna(0)

    # Calculate incidents per million BOE
    safety_df["TOTAL_BOE"] = safety_df["OIL_BBL"] + safety_df["GAS_MCF"] / 6000
    safety_df["INCIDENTS_PER_MM_BOE"] = (
        safety_df["TOTAL_INCIDENTS"] / safety_df["TOTAL_BOE"] * 1e6
    )

    # Risk score (lower is better)
    safety_df["RISK_SCORE"] = (
        safety_df["INCIDENTS_PER_MM_BOE"] +
        safety_df["TOTAL_FATALITIES"] * 10 +
        safety_df["TOTAL_INJURIES"] * 2
    )

    return safety_df.sort_values("RISK_SCORE", ascending=False)


# Example: Safety analysis
incidents = fetch_bsee_incident_data(start_year=2020, end_year=2024)
production = fetch_bsee_production_data(year=2024, output_dir=Path("data/raw/bsee"))

safety_scores = calculate_operator_safety_score(incidents, production)
print("Operator Safety Scores (higher = more risk):")
print(safety_scores.head(10))
```

### 2. SODIR/NPD Data Extraction (Norway)

**Available datasets:**
- Field production (oil, gas, NGL, condensate)
- Well data (exploration, development)
- Discoveries and prospects
- Company information
- Pipeline and infrastructure

**FactPages API:**
```python
import requests
import pandas as pd
from typing import Dict, List, Optional


class SODIRDataFetcher:
    """Fetch data from SODIR (Norwegian Offshore Directorate) FactPages."""

    BASE_URL = "https://factpages.sodir.no/api/v1"

    ENDPOINTS = {
        "fields": "/fields",
        "field_production": "/field-production-yearly",
        "wells": "/wells",
        "discoveries": "/discoveries",
        "companies": "/companies",
        "pipelines": "/pipelines",
        "facilities": "/facilities",
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "User-Agent": "EnergyDataAnalysis/1.0"
        })

    def _fetch(self, endpoint: str, params: Optional[Dict] = None) -> List[Dict]:
        """Fetch data from SODIR API."""
        url = f"{self.BASE_URL}{endpoint}"

        response = self.session.get(url, params=params, timeout=60)
        response.raise_for_status()

        return response.json()

    def get_all_fields(self) -> pd.DataFrame:
        """Get all Norwegian offshore fields."""
        data = self._fetch(self.ENDPOINTS["fields"])
        df = pd.DataFrame(data)
        return df

    def get_field_production(
        self,
        field_name: Optional[str] = None,
        start_year: Optional[int] = None,
        end_year: Optional[int] = None
    ) -> pd.DataFrame:
        """
        Get field production data.

        Args:
            field_name: Filter by field name
            start_year: Start year
            end_year: End year

        Returns:
            DataFrame with production data
        """
        data = self._fetch(self.ENDPOINTS["field_production"])
        df = pd.DataFrame(data)

        # Filter
        if field_name:
            df = df[df["fieldName"].str.contains(field_name, case=False, na=False)]
        if start_year:
            df = df[df["year"] >= start_year]
        if end_year:
            df = df[df["year"] <= end_year]

        return df

    def get_wells(
        self,
        well_type: Optional[str] = None,
        status: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Get well data.

        Args:
            well_type: 'exploration', 'development', or 'other'
            status: Well status filter

        Returns:
            DataFrame with well data
        """
        data = self._fetch(self.ENDPOINTS["wells"])
        df = pd.DataFrame(data)

        if well_type:
            df = df[df["wellType"].str.lower() == well_type.lower()]
        if status:
            df = df[df["status"].str.contains(status, case=False, na=False)]

        return df

    def get_discoveries(self, status: Optional[str] = None) -> pd.DataFrame:
        """Get discoveries data."""
        data = self._fetch(self.ENDPOINTS["discoveries"])
        df = pd.DataFrame(data)

        if status:
            df = df[df["status"].str.contains(status, case=False, na=False)]

        return df


# Example usage
sodir = SODIRDataFetcher()

# Get all fields
fields = sodir.get_all_fields()
print(f"Total Norwegian fields: {len(fields)}")

# Get production for Johan Sverdrup
sverdrup_production = sodir.get_field_production(
    field_name="JOHAN SVERDRUP",
    start_year=2019
)
print(sverdrup_production)

# Get recent exploration wells
exploration_wells = sodir.get_wells(well_type="exploration")
print(f"Total exploration wells: {len(exploration_wells)}")
```

### 3. Combined Analysis

**Cross-Basin Comparison:**
```python
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path


def compare_gom_norway_production(
    gom_data: pd.DataFrame,
    norway_data: pd.DataFrame,
    output_dir: Path = Path("reports")
) -> None:
    """
    Create comparative analysis of GOM vs Norway production.

    Args:
        gom_data: BSEE production data
        norway_data: SODIR production data
        output_dir: Report output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    # Aggregate by year
    gom_annual = gom_data.groupby("PRODUCTION_YEAR").agg({
        "OIL_BBL": "sum",
        "GAS_MCF": "sum"
    }).reset_index()
    gom_annual["REGION"] = "Gulf of Mexico"
    gom_annual["OIL_MM_BBL"] = gom_annual["OIL_BBL"] / 1e6
    gom_annual["GAS_BCF"] = gom_annual["GAS_MCF"] / 1e6

    norway_annual = norway_data.groupby("year").agg({
        "oilProduction": "sum",
        "gasProduction": "sum"
    }).reset_index()
    norway_annual.columns = ["PRODUCTION_YEAR", "OIL_MM_BBL", "GAS_BCF"]
    norway_annual["REGION"] = "Norway"

    # Create comparison chart
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=["Oil Production (MM BBL)", "Gas Production (BCF)"]
    )

    # Oil production
    fig.add_trace(
        go.Bar(
            x=gom_annual["PRODUCTION_YEAR"],
            y=gom_annual["OIL_MM_BBL"],
            name="GOM Oil",
            marker_color="blue"
        ),
        row=1, col=1
    )
    fig.add_trace(
        go.Bar(
            x=norway_annual["PRODUCTION_YEAR"],
            y=norway_annual["OIL_MM_BBL"],
            name="Norway Oil",
            marker_color="red"
        ),
        row=1, col=1
    )

    # Gas production
    fig.add_trace(
        go.Bar(
            x=gom_annual["PRODUCTION_YEAR"],
            y=gom_annual["GAS_BCF"],
            name="GOM Gas",
            marker_color="lightblue"
        ),
        row=1, col=2
    )
    fig.add_trace(
        go.Bar(
            x=norway_annual["PRODUCTION_YEAR"],
            y=norway_annual["GAS_BCF"],
            name="Norway Gas",
            marker_color="pink"
        ),
        row=1, col=2
    )

    fig.update_layout(
        title="Gulf of Mexico vs Norway: Offshore Production Comparison",
        barmode="group",
        height=500
    )

    fig.write_html(output_dir / "gom_norway_comparison.html")
    print(f"Report saved to {output_dir / 'gom_norway_comparison.html'}")
```

### 4. NPV Analysis with Regulatory Data

```python
import numpy as np
import numpy_financial as npf
import pandas as pd
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class EconomicAssumptions:
    """Economic assumptions for NPV calculation."""
    oil_price: float = 75.0      # $/bbl
    gas_price: float = 3.0       # $/mcf
    opex_per_boe: float = 15.0   # $/BOE
    capex_remaining: float = 0   # $ millions (for ongoing development)
    discount_rate: float = 0.10  # 10%
    royalty_rate: float = 0.125  # 12.5% federal royalty
    tax_rate: float = 0.21       # Corporate tax rate


def calculate_field_npv(
    production_df: pd.DataFrame,
    assumptions: EconomicAssumptions,
    forecast_years: int = 10
) -> Tuple[float, pd.DataFrame]:
    """
    Calculate NPV for a field based on BSEE production data.

    Args:
        production_df: Historical production data
        assumptions: Economic assumptions
        forecast_years: Years to forecast

    Returns:
        Tuple of (NPV, detailed cashflow DataFrame)
    """
    # Get latest year's production as baseline
    latest_year = production_df["PRODUCTION_YEAR"].max()
    baseline = production_df[production_df["PRODUCTION_YEAR"] == latest_year]

    annual_oil = baseline["OIL_BBL"].sum()
    annual_gas = baseline["GAS_MCF"].sum()

    # Simple decline curve (exponential decline)
    decline_rate = 0.10  # 10% annual decline

    cashflows = []

    for year in range(1, forecast_years + 1):
        # Decline production
        oil_prod = annual_oil * ((1 - decline_rate) ** year)
        gas_prod = annual_gas * ((1 - decline_rate) ** year)

        # Revenue
        oil_revenue = oil_prod * assumptions.oil_price
        gas_revenue = gas_prod * assumptions.gas_price
        gross_revenue = oil_revenue + gas_revenue

        # Royalties
        royalties = gross_revenue * assumptions.royalty_rate
        net_revenue = gross_revenue - royalties

        # Operating costs
        boe_produced = oil_prod + gas_prod / 6000
        opex = boe_produced * assumptions.opex_per_boe

        # EBITDA
        ebitda = net_revenue - opex

        # CapEx (if any)
        capex = assumptions.capex_remaining / forecast_years if year <= 3 else 0

        # Pre-tax income
        pretax_income = ebitda - capex

        # Taxes
        taxes = max(0, pretax_income * assumptions.tax_rate)

        # Net cash flow
        ncf = pretax_income - taxes

        cashflows.append({
            "Year": year,
            "Oil_BBL": oil_prod,
            "Gas_MCF": gas_prod,
            "Gross_Revenue_MM": gross_revenue / 1e6,
            "Royalties_MM": royalties / 1e6,
            "OPEX_MM": opex / 1e6,
            "CAPEX_MM": capex / 1e6,
            "Pre_Tax_MM": pretax_income / 1e6,
            "Taxes_MM": taxes / 1e6,
            "NCF_MM": ncf / 1e6
        })

    cashflow_df = pd.DataFrame(cashflows)

    # Calculate NPV
    ncf_series = [-assumptions.capex_remaining] + cashflow_df["NCF_MM"].tolist()
    npv = npf.npv(assumptions.discount_rate, ncf_series)

    return npv, cashflow_df


# Example: Calculate NPV for a GOM field
production = fetch_bsee_production_data(
    year=2024,
    output_dir=Path("data/raw/bsee")
)

# Filter to specific field
thunder_horse = production[
    production["FIELD_NAME"].str.contains("THUNDER HORSE", case=False, na=False)
]

assumptions = EconomicAssumptions(
    oil_price=75.0,
    gas_price=3.5,
    opex_per_boe=18.0,
    discount_rate=0.10
)

npv, cashflows = calculate_field_npv(thunder_horse, assumptions)

print(f"Thunder Horse NPV (10 year): ${npv:.1f} MM")
print("\nCashflow Summary:")
print(cashflows.to_string(index=False))
```

## Complete Pipeline Example

```python
"""
Complete BSEE/SODIR data extraction and analysis pipeline.
"""
import pandas as pd
from pathlib import Path
from datetime import datetime
import plotly.graph_objects as go


def run_extraction_pipeline(
    output_dir: Path = Path("data"),
    report_dir: Path = Path("reports")
) -> dict:
    """
    Run complete data extraction and analysis pipeline.

    Returns:
        Dictionary with extraction summary
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    report_dir.mkdir(parents=True, exist_ok=True)

    results = {
        "extraction_date": datetime.now().isoformat(),
        "datasets": {}
    }

    # 1. Extract BSEE Production Data
    print("Fetching BSEE production data...")
    try:
        bsee_production = fetch_bsee_production_data(
            year=2024,
            output_dir=output_dir / "raw" / "bsee"
        )
        bsee_production.to_csv(
            output_dir / "processed" / "bsee_production.csv",
            index=False
        )
        results["datasets"]["bsee_production"] = len(bsee_production)
    except Exception as e:
        print(f"BSEE production error: {e}")
        results["datasets"]["bsee_production"] = "error"

    # 2. Extract BSEE Well Data
    print("Fetching BSEE well data...")
    try:
        bsee_wells = fetch_bsee_well_data(
            output_dir=output_dir / "raw" / "bsee"
        )
        results["datasets"]["bsee_wells"] = len(bsee_wells)
    except Exception as e:
        print(f"BSEE wells error: {e}")
        results["datasets"]["bsee_wells"] = "error"

    # 3. Extract BSEE Incident Data
    print("Fetching BSEE incident data...")
    try:
        incidents = fetch_bsee_incident_data(start_year=2020, end_year=2024)
        incidents.to_csv(
            output_dir / "processed" / "bsee_incidents.csv",
            index=False
        )
        results["datasets"]["bsee_incidents"] = len(incidents)
    except Exception as e:
        print(f"BSEE incidents error: {e}")
        results["datasets"]["bsee_incidents"] = "error"

    # 4. Extract SODIR Data
    print("Fetching SODIR data...")
    try:
        sodir = SODIRDataFetcher()
        norway_fields = sodir.get_all_fields()
        norway_production = sodir.get_field_production(start_year=2020)

        norway_fields.to_csv(
            output_dir / "processed" / "sodir_fields.csv",
            index=False
        )
        norway_production.to_csv(
            output_dir / "processed" / "sodir_production.csv",
            index=False
        )

        results["datasets"]["sodir_fields"] = len(norway_fields)
        results["datasets"]["sodir_production"] = len(norway_production)
    except Exception as e:
        print(f"SODIR error: {e}")
        results["datasets"]["sodir"] = "error"

    # 5. Generate Summary Report
    print("Generating summary report...")
    generate_summary_report(results, report_dir)

    return results


def generate_summary_report(results: dict, report_dir: Path) -> None:
    """Generate HTML summary report."""

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Energy Data Extraction Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            h1 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .success {{ color: green; }}
            .error {{ color: red; }}
        </style>
    </head>
    <body>
        <h1>Energy Data Extraction Report</h1>
        <p><strong>Extraction Date:</strong> {results['extraction_date']}</p>

        <h2>Dataset Summary</h2>
        <table>
            <tr>
                <th>Dataset</th>
                <th>Records</th>
                <th>Status</th>
            </tr>
    """

    for dataset, count in results["datasets"].items():
        status_class = "error" if count == "error" else "success"
        status_text = "Error" if count == "error" else "Success"
        html_content += f"""
            <tr>
                <td>{dataset}</td>
                <td>{count if count != 'error' else 'N/A'}</td>
                <td class="{status_class}">{status_text}</td>
            </tr>
        """

    html_content += """
        </table>
    </body>
    </html>
    """

    report_path = report_dir / "extraction_summary.html"
    with open(report_path, "w") as f:
        f.write(html_content)

    print(f"Summary report saved to {report_path}")


# Run the pipeline
if __name__ == "__main__":
    results = run_extraction_pipeline()
    print("\nExtraction Complete!")
    print(f"Datasets extracted: {len(results['datasets'])}")
```

## Best Practices

### 1. Rate Limiting

```python
import time
from functools import wraps

def rate_limit(calls_per_minute: int = 30):
    """Decorator to rate limit API calls."""
    min_interval = 60.0 / calls_per_minute
    last_call = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_call[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_call[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_minute=30)
def fetch_with_rate_limit(url: str) -> requests.Response:
    return requests.get(url)
```

### 2. Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

@lru_cache(maxsize=100)
def cached_fetch(url: str, cache_hours: int = 24) -> pd.DataFrame:
    """Fetch with caching."""
    cache_file = Path(f".cache/{hash(url)}.parquet")

    if cache_file.exists():
        mtime = datetime.fromtimestamp(cache_file.stat().st_mtime)
        if datetime.now() - mtime < timedelta(hours=cache_hours):
            return pd.read_parquet(cache_file)

    # Fetch fresh data
    response = requests.get(url)
    df = pd.DataFrame(response.json())

    cache_file.parent.mkdir(exist_ok=True)
    df.to_parquet(cache_file)

    return df
```

### 3. Error Handling

```python
import logging
from tenacity import retry, stop_after_attempt, wait_exponential

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def robust_fetch(url: str) -> requests.Response:
    """Fetch with automatic retry on failure."""
    try:
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Fetch failed for {url}: {e}")
        raise
```

## Resources

- **BSEE Data Center**: https://www.data.bsee.gov/
- **SODIR FactPages**: https://factpages.sodir.no/
- **BSEE API Documentation**: https://www.data.bsee.gov/api-documentation
- **NPD (legacy)**: https://www.npd.no/en/facts/

---

**Use this skill for all energy regulatory data extraction in worldenergydata!**

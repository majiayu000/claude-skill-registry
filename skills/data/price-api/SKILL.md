---
name: "price-api"
description: "Fetch construction material prices from open APIs. Track price trends, regional variations, and update cost databases."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🌐", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# Price API for Construction Materials

## Overview
Material prices fluctuate constantly. This skill fetches prices from open sources, tracks trends, and updates cost databases with current market data.

## Python Implementation

```python
import requests
import pandas as pd
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class MaterialCategory(Enum):
    """Construction material categories."""
    CONCRETE = "concrete"
    STEEL = "steel"
    LUMBER = "lumber"
    COPPER = "copper"
    ALUMINUM = "aluminum"
    CEMENT = "cement"
    AGGREGATES = "aggregates"
    ASPHALT = "asphalt"


@dataclass
class MaterialPrice:
    """Material price point."""
    material: str
    price: float
    unit: str
    currency: str
    source: str
    date: datetime
    region: str = ""


@dataclass
class PriceTrend:
    """Price trend analysis."""
    material: str
    current_price: float
    week_change: float
    month_change: float
    year_change: float
    trend_direction: str  # 'up', 'down', 'stable'


class OpenPriceAPI:
    """Client for open material price APIs."""

    # Commodity price sources
    FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"

    # FRED Series IDs for construction commodities
    FRED_SERIES = {
        'steel': 'WPU101',
        'lumber': 'WPS0811',
        'concrete': 'WPU133',
        'copper': 'PCOPPUSDM',
        'aluminum': 'PALUMUSDM'
    }

    def __init__(self, fred_api_key: Optional[str] = None):
        self.fred_api_key = fred_api_key

    def get_fred_prices(self, material: str,
                        start_date: str = None,
                        end_date: str = None) -> List[MaterialPrice]:
        """Get prices from FRED API."""

        if material.lower() not in self.FRED_SERIES:
            return []

        series_id = self.FRED_SERIES[material.lower()]

        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')

        params = {
            'series_id': series_id,
            'observation_start': start_date,
            'observation_end': end_date,
            'file_type': 'json'
        }

        if self.fred_api_key:
            params['api_key'] = self.fred_api_key

        try:
            response = requests.get(self.FRED_BASE, params=params)
            if response.status_code != 200:
                return []

            data = response.json()
            observations = data.get('observations', [])

            prices = []
            for obs in observations:
                try:
                    price = float(obs['value'])
                    prices.append(MaterialPrice(
                        material=material,
                        price=price,
                        unit='index',
                        currency='USD',
                        source='FRED',
                        date=datetime.strptime(obs['date'], '%Y-%m-%d'),
                        region='US'
                    ))
                except (ValueError, KeyError):
                    continue

            return prices

        except Exception as e:
            print(f"Error fetching FRED data: {e}")
            return []

    def to_dataframe(self, prices: List[MaterialPrice]) -> pd.DataFrame:
        """Convert prices to DataFrame."""
        data = [{
            'material': p.material,
            'price': p.price,
            'unit': p.unit,
            'currency': p.currency,
            'source': p.source,
            'date': p.date,
            'region': p.region
        } for p in prices]
        return pd.DataFrame(data)


class ConstructionPriceTracker:
    """Track and analyze construction material prices."""

    # Default regional factors
    REGIONAL_FACTORS = {
        'US_National': 1.0,
        'US_Northeast': 1.15,
        'US_Southeast': 0.95,
        'US_Midwest': 0.92,
        'US_West': 1.10,
        'Germany': 1.25,
        'UK': 1.20,
        'France': 1.18
    }

    def __init__(self):
        self.price_cache: Dict[str, pd.DataFrame] = {}

    def calculate_trend(self, prices: pd.DataFrame) -> PriceTrend:
        """Calculate price trend from historical data."""

        if prices.empty or 'price' not in prices.columns:
            return None

        prices = prices.sort_values('date')
        current = prices['price'].iloc[-1]

        # Calculate changes
        week_ago_idx = len(prices) - 7 if len(prices) >= 7 else 0
        month_ago_idx = len(prices) - 30 if len(prices) >= 30 else 0
        year_ago_idx = len(prices) - 365 if len(prices) >= 365 else 0

        week_price = prices['price'].iloc[week_ago_idx]
        month_price = prices['price'].iloc[month_ago_idx]
        year_price = prices['price'].iloc[year_ago_idx]

        week_change = ((current - week_price) / week_price * 100) if week_price else 0
        month_change = ((current - month_price) / month_price * 100) if month_price else 0
        year_change = ((current - year_price) / year_price * 100) if year_price else 0

        # Determine trend
        if month_change > 5:
            trend = 'up'
        elif month_change < -5:
            trend = 'down'
        else:
            trend = 'stable'

        return PriceTrend(
            material=prices['material'].iloc[0],
            current_price=current,
            week_change=round(week_change, 2),
            month_change=round(month_change, 2),
            year_change=round(year_change, 2),
            trend_direction=trend
        )

    def apply_regional_factor(self, base_price: float,
                              region: str) -> float:
        """Apply regional price factor."""
        factor = self.REGIONAL_FACTORS.get(region, 1.0)
        return base_price * factor

    def update_cost_database(self, cost_df: pd.DataFrame,
                             price_updates: Dict[str, float],
                             date_column: str = 'last_updated') -> pd.DataFrame:
        """Update cost database with new prices."""
        updated = cost_df.copy()

        for material, price in price_updates.items():
            # Find rows with this material
            mask = updated['material'].str.lower() == material.lower()
            if mask.any():
                # Calculate adjustment factor
                old_price = updated.loc[mask, 'unit_price'].mean()
                factor = price / old_price if old_price > 0 else 1

                # Update prices
                updated.loc[mask, 'unit_price'] *= factor
                updated.loc[mask, date_column] = datetime.now()

        return updated


class MaterialPriceEstimator:
    """Estimate material prices when API data unavailable."""

    # Reference prices (USD per unit, as of 2024)
    REFERENCE_PRICES = {
        'concrete_m3': 120,
        'rebar_ton': 800,
        'structural_steel_ton': 1200,
        'lumber_mbf': 450,
        'copper_wire_kg': 12,
        'brick_1000': 550,
        'cement_ton': 130,
        'sand_m3': 35,
        'gravel_m3': 40,
        'drywall_m2': 8,
        'insulation_m2': 25
    }

    def estimate_price(self, material: str,
                       region: str = 'US_National',
                       inflation_adjustment: float = 0) -> float:
        """Estimate current price for material."""
        base_price = self.REFERENCE_PRICES.get(material, 0)

        if base_price == 0:
            return 0

        # Apply inflation
        adjusted = base_price * (1 + inflation_adjustment)

        # Apply regional factor
        tracker = ConstructionPriceTracker()
        return tracker.apply_regional_factor(adjusted, region)

    def bulk_estimate(self, materials: List[str],
                      region: str = 'US_National') -> pd.DataFrame:
        """Estimate prices for multiple materials."""
        estimates = []
        for material in materials:
            price = self.estimate_price(material, region)
            estimates.append({
                'material': material,
                'estimated_price': price,
                'region': region,
                'source': 'estimate',
                'date': datetime.now()
            })
        return pd.DataFrame(estimates)
```

## Quick Start

```python
# Initialize price API
api = OpenPriceAPI(fred_api_key="your_key")

# Get steel prices
steel_prices = api.get_fred_prices('steel')
df = api.to_dataframe(steel_prices)
print(df.tail())

# Analyze trend
tracker = ConstructionPriceTracker()
trend = tracker.calculate_trend(df)
print(f"Steel trend: {trend.trend_direction}, YoY: {trend.year_change}%")
```

## Common Use Cases

### 1. Update Cost Database
```python
tracker = ConstructionPriceTracker()

# New prices from market
updates = {'steel': 1250, 'concrete': 135, 'lumber': 480}

# Update database
updated_db = tracker.update_cost_database(cost_df, updates)
```

### 2. Regional Pricing
```python
base_price = 120  # concrete USD/m3
berlin_price = tracker.apply_regional_factor(base_price, 'Germany')
print(f"Berlin price: ${berlin_price}/m3")
```

### 3. Bulk Estimation
```python
estimator = MaterialPriceEstimator()

materials = ['concrete_m3', 'rebar_ton', 'lumber_mbf']
estimates = estimator.bulk_estimate(materials, region='US_West')
print(estimates)
```

## Resources
- **DDC Book**: Chapter 2.2 - Open Data Sources
- **FRED API**: https://fred.stlouisfed.org/docs/api/

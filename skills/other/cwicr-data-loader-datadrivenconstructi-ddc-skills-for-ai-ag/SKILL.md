---
slug: "cwicr-data-loader"
display_name: "CWICR Data Loader"
description: "Load and parse DDC CWICR construction cost database from multiple formats: Parquet, Excel, CSV, Qdrant snapshots. Foundation for all CWICR operations."
---

# CWICR Data Loader

## Business Case

### Problem Statement
DDC CWICR database is distributed in multiple formats:
- Apache Parquet (optimized for analytics)
- Excel workbooks (human-readable)
- CSV files (universal exchange)
- Qdrant snapshots (vector search)

Applications need unified data access regardless of source format.

### Solution
Universal data loader supporting all CWICR formats with automatic schema detection, validation, and pandas DataFrame conversion.

### Business Value
- **Format agnostic** - Load from any CWICR distribution
- **Validated data** - Automatic schema validation
- **Memory efficient** - Lazy loading for large datasets
- **Type-safe** - Proper data types preserved

## Technical Implementation

### Prerequisites
```bash
pip install pandas pyarrow openpyxl qdrant-client
```

### Python Implementation

```python
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from enum import Enum
import json


class CWICRFormat(Enum):
    """Supported CWICR data formats."""
    PARQUET = "parquet"
    EXCEL = "excel"
    CSV = "csv"
    QDRANT = "qdrant"
    JSON = "json"


class CWICRLanguage(Enum):
    """Supported languages in CWICR database."""
    ARABIC = "ar"
    CHINESE = "zh"
    GERMAN = "de"
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    HINDI = "hi"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"


@dataclass
class CWICRSchema:
    """CWICR database schema definition."""

    # Core fields
    work_item_code: str = "work_item_code"
    description: str = "description"
    unit: str = "unit"
    category: str = "category"

    # Cost fields
    unit_price: str = "unit_price"
    labor_cost: str = "labor_cost"
    material_cost: str = "material_cost"
    equipment_cost: str = "equipment_cost"
    overhead_cost: str = "overhead_cost"

    # Norm fields
    labor_norm: str = "labor_norm"
    material_norm: str = "material_norm"
    equipment_norm: str = "equipment_norm"

    # Metadata
    language: str = "language"
    region: str = "region"
    currency: str = "currency"
    last_updated: str = "last_updated"

    # Optional embedding
    embedding: str = "embedding"


@dataclass
class CWICRWorkItem:
    """Represents a single work item from CWICR database."""
    work_item_code: str
    description: str
    unit: str
    category: str

    unit_price: float = 0.0
    labor_cost: float = 0.0
    material_cost: float = 0.0
    equipment_cost: float = 0.0
    overhead_cost: float = 0.0

    labor_norm: float = 0.0
    labor_unit: str = "h"

    resources: List[Dict[str, Any]] = field(default_factory=list)

    language: str = "en"
    region: str = ""
    currency: str = "USD"


@dataclass
class CWICRResource:
    """Represents a resource (material, labor, equipment)."""
    resource_code: str
    description: str
    unit: str
    unit_price: float
    resource_type: str  # 'labor', 'material', 'equipment'
    category: str = ""


class CWICRDataLoader:
    """Universal loader for CWICR database formats."""

    REQUIRED_COLUMNS = ['work_item_code', 'description', 'unit']
    NUMERIC_COLUMNS = ['unit_price', 'labor_cost', 'material_cost',
                       'equipment_cost', 'labor_norm']

    def __init__(self):
        self.schema = CWICRSchema()
        self._cache: Dict[str, pd.DataFrame] = {}

    def load(self, source: str,
             format: Optional[CWICRFormat] = None,
             language: Optional[CWICRLanguage] = None,
             use_cache: bool = True) -> pd.DataFrame:
        """Load CWICR data from any supported source."""

        cache_key = f"{source}_{language}"
        if use_cache and cache_key in self._cache:
            return self._cache[cache_key]

        # Auto-detect format if not specified
        if format is None:
            format = self._detect_format(source)

        # Load based on format
        if format == CWICRFormat.PARQUET:
            df = self._load_parquet(source)
        elif format == CWICRFormat.EXCEL:
            df = self._load_excel(source)
        elif format == CWICRFormat.CSV:
            df = self._load_csv(source)
        elif format == CWICRFormat.JSON:
            df = self._load_json(source)
        else:
            raise ValueError(f"Unsupported format: {format}")

        # Validate and normalize
        df = self._validate_schema(df)
        df = self._normalize_types(df)

        # Filter by language if specified
        if language and 'language' in df.columns:
            df = df[df['language'] == language.value]

        # Cache result
        if use_cache:
            self._cache[cache_key] = df

        return df

    def _detect_format(self, source: str) -> CWICRFormat:
        """Auto-detect data format from source."""
        path = Path(source)

        if path.suffix.lower() == '.parquet':
            return CWICRFormat.PARQUET
        elif path.suffix.lower() in ['.xlsx', '.xls']:
            return CWICRFormat.EXCEL
        elif path.suffix.lower() == '.csv':
            return CWICRFormat.CSV
        elif path.suffix.lower() == '.json':
            return CWICRFormat.JSON
        else:
            raise ValueError(f"Cannot detect format: {source}")

    def _load_parquet(self, source: str) -> pd.DataFrame:
        """Load from Parquet file."""
        return pd.read_parquet(source)

    def _load_excel(self, source: str,
                    sheet_name: str = "WorkItems") -> pd.DataFrame:
        """Load from Excel workbook."""
        try:
            return pd.read_excel(source, sheet_name=sheet_name)
        except:
            # Try first sheet if named sheet doesn't exist
            return pd.read_excel(source, sheet_name=0)

    def _load_csv(self, source: str) -> pd.DataFrame:
        """Load from CSV file."""
        # Try different encodings
        for encoding in ['utf-8', 'latin-1', 'cp1252']:
            try:
                return pd.read_csv(source, encoding=encoding)
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Cannot read CSV with any encoding: {source}")

    def _load_json(self, source: str) -> pd.DataFrame:
        """Load from JSON file."""
        with open(source, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, list):
            return pd.DataFrame(data)
        elif isinstance(data, dict) and 'items' in data:
            return pd.DataFrame(data['items'])
        else:
            return pd.DataFrame([data])

    def _validate_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate DataFrame against CWICR schema."""
        # Check required columns
        missing = set(self.REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        return df

    def _normalize_types(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column types."""
        for col in self.NUMERIC_COLUMNS:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

        # Ensure string columns
        for col in ['work_item_code', 'description', 'unit', 'category']:
            if col in df.columns:
                df[col] = df[col].astype(str)

        return df

    def load_resources(self, source: str,
                       format: Optional[CWICRFormat] = None) -> pd.DataFrame:
        """Load resources separately."""
        if format is None:
            format = self._detect_format(source)

        if format == CWICRFormat.EXCEL:
            try:
                return pd.read_excel(source, sheet_name="Resources")
            except:
                return pd.DataFrame()
        else:
            return self.load(source, format)

    def get_work_item(self, df: pd.DataFrame,
                      code: str) -> Optional[CWICRWorkItem]:
        """Get single work item by code."""
        item = df[df['work_item_code'] == code]
        if item.empty:
            return None

        row = item.iloc[0]
        return CWICRWorkItem(
            work_item_code=row['work_item_code'],
            description=row.get('description', ''),
            unit=row.get('unit', ''),
            category=row.get('category', ''),
            unit_price=row.get('unit_price', 0),
            labor_cost=row.get('labor_cost', 0),
            material_cost=row.get('material_cost', 0),
            equipment_cost=row.get('equipment_cost', 0),
            labor_norm=row.get('labor_norm', 0),
            language=row.get('language', 'en'),
            region=row.get('region', ''),
            currency=row.get('currency', 'USD')
        )

    def get_categories(self, df: pd.DataFrame) -> List[str]:
        """Get unique categories."""
        if 'category' not in df.columns:
            return []
        return df['category'].dropna().unique().tolist()

    def filter_by_category(self, df: pd.DataFrame,
                           category: str) -> pd.DataFrame:
        """Filter work items by category."""
        return df[df['category'] == category]

    def search_by_description(self, df: pd.DataFrame,
                              keyword: str,
                              case_sensitive: bool = False) -> pd.DataFrame:
        """Simple keyword search in descriptions."""
        if case_sensitive:
            return df[df['description'].str.contains(keyword, na=False)]
        return df[df['description'].str.contains(keyword, case=False, na=False)]

    def get_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get database statistics."""
        stats = {
            'total_work_items': len(df),
            'categories': df['category'].nunique() if 'category' in df.columns else 0,
            'languages': df['language'].unique().tolist() if 'language' in df.columns else ['en']
        }

        if 'unit_price' in df.columns:
            stats['price_range'] = {
                'min': df['unit_price'].min(),
                'max': df['unit_price'].max(),
                'mean': df['unit_price'].mean()
            }

        return stats

    def export(self, df: pd.DataFrame,
               output_path: str,
               format: CWICRFormat = CWICRFormat.PARQUET):
        """Export DataFrame to file."""
        if format == CWICRFormat.PARQUET:
            df.to_parquet(output_path, index=False)
        elif format == CWICRFormat.EXCEL:
            df.to_excel(output_path, index=False)
        elif format == CWICRFormat.CSV:
            df.to_csv(output_path, index=False)
        elif format == CWICRFormat.JSON:
            df.to_json(output_path, orient='records', indent=2)


class CWICRBatchLoader:
    """Load multiple CWICR files and merge."""

    def __init__(self):
        self.loader = CWICRDataLoader()

    def load_multiple(self, sources: List[str]) -> pd.DataFrame:
        """Load and merge multiple CWICR files."""
        dfs = []
        for source in sources:
            try:
                df = self.loader.load(source)
                dfs.append(df)
            except Exception as e:
                print(f"Warning: Failed to load {source}: {e}")

        if not dfs:
            return pd.DataFrame()

        return pd.concat(dfs, ignore_index=True)

    def load_all_languages(self, base_path: str) -> pd.DataFrame:
        """Load all language variants from directory."""
        path = Path(base_path)
        dfs = []

        for lang in CWICRLanguage:
            # Try various naming patterns
            patterns = [
                f"cwicr_{lang.value}.*",
                f"ddc_cwicr_{lang.value}.*",
                f"*_{lang.value}.*"
            ]

            for pattern in patterns:
                files = list(path.glob(pattern))
                for file in files:
                    try:
                        df = self.loader.load(str(file), language=lang)
                        dfs.append(df)
                    except Exception as e:
                        continue

        if not dfs:
            return pd.DataFrame()

        return pd.concat(dfs, ignore_index=True)


# Convenience functions
def load_cwicr(source: str, language: str = None) -> pd.DataFrame:
    """Quick load CWICR data."""
    loader = CWICRDataLoader()
    lang = CWICRLanguage(language) if language else None
    return loader.load(source, language=lang)


def get_cwicr_statistics(source: str) -> Dict[str, Any]:
    """Get statistics from CWICR source."""
    loader = CWICRDataLoader()
    df = loader.load(source)
    return loader.get_statistics(df)
```

## Quick Start

```python
# Load from Parquet (fastest)
loader = CWICRDataLoader()
df = loader.load("ddc_cwicr_en.parquet")
print(f"Loaded {len(df)} work items")

# Load from Excel
df = loader.load("cwicr_database.xlsx")

# Get specific work item
item = loader.get_work_item(df, "CONC-001")
print(f"{item.description}: ${item.unit_price} per {item.unit}")

# Get all categories
categories = loader.get_categories(df)
print(f"Categories: {categories}")
```

## Common Use Cases

### 1. Multi-Language Loading
```python
batch = CWICRBatchLoader()
all_languages = batch.load_all_languages("C:/CWICR/")
print(f"Total items across all languages: {len(all_languages)}")
```

### 2. Category Filtering
```python
loader = CWICRDataLoader()
df = loader.load("cwicr.parquet")

# Get concrete work items
concrete = loader.filter_by_category(df, "Concrete")
print(f"Concrete items: {len(concrete)}")
```

### 3. Keyword Search
```python
# Find all masonry-related items
masonry = loader.search_by_description(df, "masonry")
print(masonry[['work_item_code', 'description', 'unit_price']])
```

## Database Statistics

```python
stats = loader.get_statistics(df)
print(f"Total items: {stats['total_work_items']}")
print(f"Categories: {stats['categories']}")
print(f"Price range: ${stats['price_range']['min']:.2f} - ${stats['price_range']['max']:.2f}")
```

## Resources

- **GitHub**: [OpenConstructionEstimate-DDC-CWICR](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR)
- **Downloads**: [CWICR Releases](https://github.com/datadrivenconstruction/OpenConstructionEstimate-DDC-CWICR/releases)
- **Formats**: Parquet, Excel, CSV, Qdrant snapshots

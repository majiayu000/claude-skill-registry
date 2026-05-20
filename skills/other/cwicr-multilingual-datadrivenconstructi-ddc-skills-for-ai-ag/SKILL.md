---
name: "cwicr-multilingual"
description: "Work with CWICR database across 9 languages. Cross-language matching, translation, and regional pricing."
homepage: "https://datadrivenconstruction.io"
metadata: {"openclaw": {"emoji": "🗄️", "os": ["darwin", "linux", "win32"], "homepage": "https://datadrivenconstruction.io", "requires": {"bins": ["python3"]}}}
---
# CWICR Multilingual Support

## Overview
CWICR database supports 9 languages with consistent work item codes. This skill enables cross-language work item matching, translation, and regional price comparison.

## Supported Languages

| Code | Language | Region | Currency |
|------|----------|--------|----------|
| AR | Arabic | Dubai | AED |
| DE | German | Berlin | EUR |
| EN | English | Toronto | CAD |
| ES | Spanish | Barcelona | EUR |
| FR | French | Paris | EUR |
| HI | Hindi | Mumbai | INR |
| PT | Portuguese | São Paulo | BRL |
| RU | Russian | St. Petersburg | RUB |
| ZH | Chinese | Shanghai | CNY |

## Python Implementation

```python
import pandas as pd
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class CWICRLanguage(Enum):
    """Supported CWICR languages."""
    ARABIC = ("ar", "Arabic", "AED", "Dubai")
    GERMAN = ("de", "German", "EUR", "Berlin")
    ENGLISH = ("en", "English", "CAD", "Toronto")
    SPANISH = ("es", "Spanish", "EUR", "Barcelona")
    FRENCH = ("fr", "French", "EUR", "Paris")
    HINDI = ("hi", "Hindi", "INR", "Mumbai")
    PORTUGUESE = ("pt", "Portuguese", "BRL", "São Paulo")
    RUSSIAN = ("ru", "Russian", "RUB", "St. Petersburg")
    CHINESE = ("zh", "Chinese", "CNY", "Shanghai")

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def name(self) -> str:
        return self.value[1]

    @property
    def currency(self) -> str:
        return self.value[2]

    @property
    def region(self) -> str:
        return self.value[3]


@dataclass
class MultilingualWorkItem:
    """Work item with translations."""
    work_item_code: str
    translations: Dict[str, str]  # language_code -> description
    prices: Dict[str, float]      # language_code -> unit_price
    unit: str


class CWICRMultilingual:
    """Work with CWICR across languages."""

    # Exchange rates to USD (approximate)
    EXCHANGE_RATES = {
        'AED': 0.27,
        'EUR': 1.08,
        'CAD': 0.74,
        'INR': 0.012,
        'BRL': 0.20,
        'RUB': 0.011,
        'CNY': 0.14,
        'USD': 1.0
    }

    def __init__(self, databases: Dict[str, pd.DataFrame] = None):
        """Initialize with language databases."""
        self.databases = databases or {}
        self._index_databases()

    def _index_databases(self):
        """Create code-based index for each database."""
        self.indexes = {}
        for lang, df in self.databases.items():
            if 'work_item_code' in df.columns:
                self.indexes[lang] = df.set_index('work_item_code')

    def load_database(self, language: CWICRLanguage,
                      file_path: str):
        """Load database for specific language."""
        # Detect format and load
        if file_path.endswith('.parquet'):
            df = pd.read_parquet(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        else:
            raise ValueError(f"Unsupported format: {file_path}")

        self.databases[language.code] = df
        if 'work_item_code' in df.columns:
            self.indexes[language.code] = df.set_index('work_item_code')

    def get_item_translations(self, work_item_code: str) -> MultilingualWorkItem:
        """Get all translations for a work item."""

        translations = {}
        prices = {}
        unit = ""

        for lang, index in self.indexes.items():
            if work_item_code in index.index:
                row = index.loc[work_item_code]
                translations[lang] = str(row.get('description', ''))
                prices[lang] = float(row.get('unit_price', 0))
                if not unit:
                    unit = str(row.get('unit', ''))

        return MultilingualWorkItem(
            work_item_code=work_item_code,
            translations=translations,
            prices=prices,
            unit=unit
        )

    def translate(self, work_item_code: str,
                  from_lang: str,
                  to_lang: str) -> Optional[str]:
        """Translate work item description."""

        if to_lang not in self.indexes:
            return None

        if work_item_code in self.indexes[to_lang].index:
            return str(self.indexes[to_lang].loc[work_item_code].get('description', ''))

        return None

    def compare_prices(self, work_item_code: str,
                       normalize_to_usd: bool = True) -> Dict[str, float]:
        """Compare prices across regions."""

        prices = {}

        for lang, index in self.indexes.items():
            if work_item_code in index.index:
                price = float(index.loc[work_item_code].get('unit_price', 0))

                if normalize_to_usd:
                    # Get currency for this language
                    currency = self._get_currency(lang)
                    rate = self.EXCHANGE_RATES.get(currency, 1.0)
                    price = price * rate

                prices[lang] = round(price, 2)

        return prices

    def _get_currency(self, lang_code: str) -> str:
        """Get currency for language code."""
        for lang in CWICRLanguage:
            if lang.code == lang_code:
                return lang.currency
        return 'USD'

    def find_cheapest_region(self, work_item_code: str) -> Tuple[str, float]:
        """Find region with lowest price (USD normalized)."""

        prices = self.compare_prices(work_item_code, normalize_to_usd=True)

        if not prices:
            return ('', 0)

        cheapest = min(prices.items(), key=lambda x: x[1])
        return cheapest

    def find_most_expensive_region(self, work_item_code: str) -> Tuple[str, float]:
        """Find region with highest price (USD normalized)."""

        prices = self.compare_prices(work_item_code, normalize_to_usd=True)

        if not prices:
            return ('', 0)

        expensive = max(prices.items(), key=lambda x: x[1])
        return expensive

    def cross_language_search(self, query: str,
                              source_lang: str) -> Dict[str, List[str]]:
        """Search in one language, get results in all languages."""

        if source_lang not in self.databases:
            return {}

        source_df = self.databases[source_lang]

        # Find matching codes
        matches = source_df[
            source_df['description'].str.contains(query, case=False, na=False)
        ]['work_item_code'].tolist()

        # Get translations for matches
        results = {}
        for code in matches[:10]:  # Limit to 10
            item = self.get_item_translations(code)
            results[code] = item.translations

        return results

    def price_comparison_report(self, work_item_codes: List[str]) -> pd.DataFrame:
        """Generate price comparison report across regions."""

        rows = []
        for code in work_item_codes:
            item = self.get_item_translations(code)
            prices_usd = self.compare_prices(code, normalize_to_usd=True)

            row = {
                'code': code,
                'description': item.translations.get('en', list(item.translations.values())[0] if item.translations else ''),
                'unit': item.unit
            }

            for lang, price in prices_usd.items():
                row[f'price_{lang}_usd'] = price

            if prices_usd:
                row['min_price'] = min(prices_usd.values())
                row['max_price'] = max(prices_usd.values())
                row['price_variance'] = row['max_price'] - row['min_price']

            rows.append(row)

        return pd.DataFrame(rows)


class LanguageDetector:
    """Detect language of construction text."""

    # Common construction terms by language
    KEYWORDS = {
        'en': ['concrete', 'wall', 'floor', 'door', 'window', 'steel', 'brick'],
        'de': ['beton', 'wand', 'boden', 'tür', 'fenster', 'stahl', 'ziegel'],
        'es': ['hormigón', 'pared', 'piso', 'puerta', 'ventana', 'acero', 'ladrillo'],
        'fr': ['béton', 'mur', 'plancher', 'porte', 'fenêtre', 'acier', 'brique'],
        'ru': ['бетон', 'стена', 'пол', 'дверь', 'окно', 'сталь', 'кирпич'],
        'zh': ['混凝土', '墙', '地板', '门', '窗', '钢', '砖'],
        'pt': ['concreto', 'parede', 'piso', 'porta', 'janela', 'aço', 'tijolo'],
        'ar': ['خرسانة', 'جدار', 'أرضية', 'باب', 'نافذة', 'فولاذ', 'طوب'],
        'hi': ['कंक्रीट', 'दीवार', 'फर्श', 'दरवाजा', 'खिड़की', 'इस्पात', 'ईंट']
    }

    @staticmethod
    def detect(text: str) -> str:
        """Detect language of text."""
        text_lower = text.lower()

        scores = {}
        for lang, keywords in LanguageDetector.KEYWORDS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[lang] = score

        if scores:
            return max(scores.items(), key=lambda x: x[1])[0]

        return 'en'  # Default to English
```

## Quick Start

```python
# Initialize multilingual support
multi = CWICRMultilingual()

# Load databases
multi.load_database(CWICRLanguage.ENGLISH, "cwicr_en.parquet")
multi.load_database(CWICRLanguage.GERMAN, "cwicr_de.parquet")
multi.load_database(CWICRLanguage.SPANISH, "cwicr_es.parquet")

# Get translations
item = multi.get_item_translations("CONC-001")
print(f"EN: {item.translations.get('en')}")
print(f"DE: {item.translations.get('de')}")
```

## Price Comparison

```python
# Compare concrete prices across regions
prices = multi.compare_prices("CONC-001", normalize_to_usd=True)
print(prices)

# Find cheapest region
region, price = multi.find_cheapest_region("CONC-001")
print(f"Cheapest: {region} at ${price}")
```

## Resources
- **DDC Book**: Chapter 2.2 - Open Data Integration
- **CWICR Database**: 9 languages, 55,000+ items

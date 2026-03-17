---
name: tool-authoring
description: Creating reusable tools in tools/ directory that workflows can import and use
---

# Tool Authoring Skill

Use this skill to create reusable tools that multiple workflows can import and use.

## Tool Philosophy

**Tools are libraries, workflows are applications.**

- Tools encapsulate reusable capabilities (API clients, data processors, formatters)
- Workflows import and orchestrate tools to solve specific problems
- Good tools are focused, well-tested, and well-documented

## Tool Structure

```
tools/
  my_tool/
    __init__.py          # Package marker, exports main functions
    tool.py              # Main implementation
    config.yaml          # Tool metadata and dependencies
    README.md            # Documentation (optional)
    tests.py             # Unit tests (optional)
```

## Creating a Tool

```bash
# Create tool directory
raw create my_tool --tool -d "Brief description of what it does"

# This creates:
# - tools/my_tool/
# - tools/my_tool/__init__.py
# - tools/my_tool/tool.py
# - tools/my_tool/config.yaml
```

## Tool config.yaml

```yaml
id: my_tool
name: my_tool
version: 1.0.0
description: Fetch stock prices and financial data from Yahoo Finance API
dependencies:
  - yfinance>=0.2.28
  - pandas>=2.0.0
```

## Tool Implementation Pattern

### 1. Simple Function Tool

```python
# tools/my_tool/tool.py
"""Tool for fetching stock data from Yahoo Finance."""

import yfinance as yf
from typing import Any


def fetch_stock_price(symbol: str) -> dict[str, Any]:
    """Fetch current stock price for a given symbol.

    Args:
        symbol: Stock ticker symbol (e.g., "AAPL", "TSLA")

    Returns:
        Dictionary with price, change, volume, etc.

    Raises:
        ValueError: If symbol is invalid
        ConnectionError: If API is unavailable
    """
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info

        return {
            "symbol": symbol,
            "price": info.get("currentPrice"),
            "change": info.get("regularMarketChange"),
            "change_percent": info.get("regularMarketChangePercent"),
            "volume": info.get("volume"),
            "market_cap": info.get("marketCap"),
        }
    except Exception as e:
        raise ValueError(f"Failed to fetch data for {symbol}: {e}")


def fetch_historical_data(
    symbol: str,
    period: str = "1mo"
) -> list[dict[str, Any]]:
    """Fetch historical price data.

    Args:
        symbol: Stock ticker symbol
        period: Time period ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y")

    Returns:
        List of historical data points with date, open, high, low, close, volume
    """
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period=period)

    return [
        {
            "date": str(date.date()),
            "open": row["Open"],
            "high": row["High"],
            "low": row["Low"],
            "close": row["Close"],
            "volume": row["Volume"],
        }
        for date, row in hist.iterrows()
    ]
```

### 2. Class-Based Tool

```python
# tools/email_sender/tool.py
"""Tool for sending emails via SMTP."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any


class EmailClient:
    """SMTP email client with retry logic."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        username: str | None = None,
        password: str | None = None,
    ):
        """Initialize email client.

        Args:
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port (default: 587 for TLS)
            username: SMTP username (optional)
            password: SMTP password (optional)
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password

    def send_email(
        self,
        to: str | list[str],
        subject: str,
        body: str,
        html: bool = False,
    ) -> bool:
        """Send an email.

        Args:
            to: Recipient email(s)
            subject: Email subject
            body: Email body (text or HTML)
            html: Whether body is HTML (default: False)

        Returns:
            True if sent successfully

        Raises:
            ConnectionError: If SMTP connection fails
        """
        # Normalize to list
        recipients = [to] if isinstance(to, str) else to

        # Create message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.username or "noreply@example.com"
        msg["To"] = ", ".join(recipients)

        # Add body
        mime_type = "html" if html else "plain"
        msg.attach(MIMEText(body, mime_type))

        # Send via SMTP
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                if self.username and self.password:
                    server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            raise ConnectionError(f"Failed to send email: {e}")
```

### 3. Tool with State Management

```python
# tools/cache_manager/tool.py
"""Tool for caching API responses."""

import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Any


class CacheManager:
    """Simple file-based cache with TTL."""

    def __init__(self, cache_dir: Path, ttl_seconds: int = 3600):
        """Initialize cache manager.

        Args:
            cache_dir: Directory to store cache files
            ttl_seconds: Time-to-live for cache entries (default: 1 hour)
        """
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl_seconds = ttl_seconds

    def _get_cache_path(self, key: str) -> Path:
        """Get cache file path for a key."""
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.json"

    def get(self, key: str) -> Any | None:
        """Get cached value if not expired."""
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        # Check expiry
        mtime = datetime.fromtimestamp(cache_path.stat().st_mtime)
        if datetime.now() - mtime > timedelta(seconds=self.ttl_seconds):
            cache_path.unlink()  # Delete expired cache
            return None

        # Load and return
        return json.loads(cache_path.read_text())

    def set(self, key: str, value: Any) -> None:
        """Store value in cache."""
        cache_path = self._get_cache_path(key)
        cache_path.write_text(json.dumps(value))

    def clear(self) -> int:
        """Clear all cache entries."""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        return count
```

## Tool __init__.py Exports

Make main functions easily importable:

```python
# tools/my_tool/__init__.py
"""Yahoo Finance data fetching tool."""

from tools.my_tool.tool import fetch_stock_price, fetch_historical_data

__all__ = ["fetch_stock_price", "fetch_historical_data"]
```

## Using Tools in Workflows

```python
# In workflow run.py
from tools.yahoo_finance import fetch_stock_price
from tools.email_sender import EmailClient
from tools.cache_manager import CacheManager

class MyWorkflow(BaseWorkflow[MyParams]):
    def run(self) -> int:
        # Use tools
        price_data = fetch_stock_price("AAPL")

        cache = CacheManager(self.workflow_dir / "cache")
        cache.set("last_price", price_data)

        email = EmailClient("smtp.example.com", username="user", password="pass")
        email.send_email("user@example.com", "Price Alert", f"Price: {price_data['price']}")

        return 0
```

## Tool Testing

```python
# tools/my_tool/tests.py
"""Tests for my_tool."""

import pytest
from tools.my_tool import fetch_stock_price


def test_fetch_stock_price():
    """Test fetching stock price."""
    result = fetch_stock_price("AAPL")

    assert "symbol" in result
    assert result["symbol"] == "AAPL"
    assert "price" in result
    assert isinstance(result["price"], (int, float))


def test_fetch_invalid_symbol():
    """Test error handling for invalid symbol."""
    with pytest.raises(ValueError):
        fetch_stock_price("INVALID_SYMBOL_XYZ")
```

## Tool Documentation

```markdown
# Yahoo Finance Tool

Fetch stock prices, historical data, and financial information from Yahoo Finance API.

## Installation

This tool is automatically available after running `raw init`.

## Functions

### `fetch_stock_price(symbol: str) -> dict`

Fetch current stock price and market data.

**Parameters:**
- `symbol` (str): Stock ticker symbol (e.g., "AAPL", "TSLA")

**Returns:**
Dictionary with keys: symbol, price, change, change_percent, volume, market_cap

**Example:**
```python
from tools.yahoo_finance import fetch_stock_price

data = fetch_stock_price("AAPL")
print(f"Current price: ${data['price']}")
```

### `fetch_historical_data(symbol: str, period: str = "1mo") -> list[dict]`

Fetch historical price data.

**Parameters:**
- `symbol` (str): Stock ticker symbol
- `period` (str): Time period - "1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y"

**Returns:**
List of historical data points with date, open, high, low, close, volume

**Example:**
```python
from tools.yahoo_finance import fetch_historical_data

history = fetch_historical_data("AAPL", period="1mo")
for entry in history:
    print(f"{entry['date']}: ${entry['close']}")
```
```

## Tool Design Principles

1. **Single Responsibility**: Each tool does one thing well
2. **Type Hints**: Use type hints everywhere for clarity
3. **Error Handling**: Raise specific exceptions with helpful messages
4. **Documentation**: Docstrings for all public functions
5. **No Side Effects**: Tools shouldn't modify global state
6. **Testable**: Design for easy unit testing
7. **Dependency Management**: Pin versions in config.yaml

## Common Tool Categories

- **API Clients**: Wrappers for external APIs (weather, stocks, news)
- **Data Processors**: Parsing, transformation, validation
- **File Handlers**: Reading, writing, converting file formats
- **Utilities**: Caching, retry logic, rate limiting
- **Formatters**: Output generation (PDF, HTML, markdown)

## Searchable Tool Descriptions

When creating tools, write descriptions for discoverability:

```yaml
# Good: Specific, searchable
description: Fetch real-time stock prices, historical data, and dividends from Yahoo Finance API

# Bad: Vague
description: Tool for getting stock data
```

## Tool Versioning

Increment version when making breaking changes:

```yaml
# config.yaml
version: 1.0.0  # Initial release
version: 1.1.0  # Add new function (backward compatible)
version: 2.0.0  # Change function signature (breaking)
```

Published workflows pin tool versions for reproducibility.

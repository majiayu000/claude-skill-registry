---
name: generate-asset-price-chart
description: Generate candlestick price charts for any asset from existing OHLC data, without handling data fetching.
---

# Generate Asset Price Chart (from OHLC data)

Render a candlestick chart image from preloaded OHLC candles. This skill focuses only on chart generation logic (no API calls).

## When to use
- You already have OHLC candles and need a visual chart
- You want to generate PNG charts in backend jobs or bots
- You need a reusable chart renderer for any asset/timeframe

## Required tools / APIs
- No external API required
- Node.js option: `canvas`
- Python option: `matplotlib`

Install:

```bash
# Node.js
npm install canvas

# Python
python -m pip install matplotlib
```

Input OHLC format expected by both examples:
- Array of rows: `[timestamp, open, high, low, close]`
- `timestamp` can be unix ms or any x-axis label value

## Skills

### generate_candlestick_chart_with_nodejs

```javascript
import { createCanvas } from "canvas";
import { writeFile } from "node:fs/promises";

function validateOhlc(data) {
  if (!Array.isArray(data) || data.length === 0) {
    throw new Error("OHLC data must be a non-empty array");
  }

  data.forEach((row, index) => {
    if (!Array.isArray(row) || row.length < 5) {
      throw new Error(`Invalid row at index ${index}. Expected [timestamp, open, high, low, close]`);
    }

    const [, open, high, low, close] = row;
    [open, high, low, close].forEach((v) => {
      if (!Number.isFinite(v)) {
        throw new Error(`Non-numeric OHLC value at row ${index}`);
      }
    });
  });
}

function generateCandlestickChart(ohlcData, options = {}) {
  validateOhlc(ohlcData);

  const width = options.width ?? 1200;
  const height = options.height ?? 600;
  const padding = options.padding ?? 60;

  const canvas = createCanvas(width, height);
  const ctx = canvas.getContext("2d");

  // Background
  ctx.fillStyle = "#1e1e2e";
  ctx.fillRect(0, 0, width, height);

  const chartWidth = width - padding * 2;
  const chartHeight = height - padding * 2;

  const highs = ohlcData.map((d) => d[2]);
  const lows = ohlcData.map((d) => d[3]);

  const minPrice = Math.min(...lows);
  const maxPrice = Math.max(...highs);
  const priceRange = Math.max(maxPrice - minPrice, 1e-9);

  const xStep = chartWidth / Math.max(ohlcData.length, 1);
  const yScale = chartHeight / priceRange;

  // Grid
  ctx.strokeStyle = "#333";
  ctx.lineWidth = 1;
  for (let i = 0; i <= 5; i++) {
    const y = padding + (chartHeight / 5) * i;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(width - padding, y);
    ctx.stroke();
  }

  // Candles
  ohlcData.forEach(([, open, high, low, close], index) => {
    const x = padding + index * xStep + xStep / 2;

    const highY = height - padding - (high - minPrice) * yScale;
    const lowY = height - padding - (low - minPrice) * yScale;
    const openY = height - padding - (open - minPrice) * yScale;
    const closeY = height - padding - (close - minPrice) * yScale;

    const bullish = close >= open;
    ctx.strokeStyle = bullish ? "#4caf50" : "#f44336";
    ctx.fillStyle = ctx.strokeStyle;

    // Wick
    ctx.beginPath();
    ctx.moveTo(x, highY);
    ctx.lineTo(x, lowY);
    ctx.stroke();

    // Body
    const bodyTop = Math.min(openY, closeY);
    const bodyHeight = Math.max(Math.abs(openY - closeY), 2); // keep flat candles visible
    const bodyWidth = Math.max(xStep * 0.6, 1);
    ctx.fillRect(x - bodyWidth / 2, bodyTop, bodyWidth, bodyHeight);
  });

  return canvas.toBuffer("image/png");
}

// Example usage with existing OHLC array
const sample = [
  [1700000000000, 100, 110, 95, 108],
  [1700000600000, 108, 112, 104, 106],
  [1700001200000, 106, 115, 103, 113],
  [1700001800000, 113, 118, 109, 111],
  [1700002400000, 111, 119, 110, 117],
];

const image = generateCandlestickChart(sample, { width: 1200, height: 600 });
await writeFile("candlestick.png", image);
console.log("Saved: candlestick.png");
```

## Agent prompt
```text
You are generating a candlestick chart image from existing OHLC data only.
Do not fetch market data and do not add API logic.

Input format is an array of [timestamp, open, high, low, close].
Use either Node.js (canvas) or Python (matplotlib) to render candles with:
- dark background,
- simple horizontal grid,
- green bullish candles,
- red bearish candles,
- visible wick and body.

Return:
1) the code used,
2) output filename,
3) a short validation note (e.g., candle count rendered).
```

## Best practices
- Validate OHLC shape before rendering
- Ensure candle body has a minimum visible height for flat candles
- Keep rendering pure: chart function accepts data and returns/saves image
- Separate fetching/ETL from visualization

## Troubleshooting
- `Module not found: canvas` → run `npm install canvas`
- Python import error for matplotlib → run `python -m pip install matplotlib`
- Blank/flat chart → verify that OHLC values are numeric and vary across candles
- Inverted y-axis feeling → confirm conversion formula maps higher prices upward

## See also
- [trading-indicators-from-price-data.md](trading-indicators-from-price-data.md) — derive indicators before plotting
- [get-crypto-price.md](get-crypto-price.md) — fetch data separately, then pass OHLC into this chart skill
# AI Economist Skill

A unified tool for central bank policy analysis and real-time GDP nowcasting for the US and Canada.

## Features

### 🏦 Policy Oracle (Taylor Rule Engine)
- **Multi-Model Gap Estimation**: Calculates output gaps using Okun's Law (Labor), HP Filter (Statistical), and Capacity Utilization (Industrial).
- **Non-Linear Taylor Rule**: Implements asymmetric central bank preferences for high inflation scenarios.
- **Bayesian Inference**: Provides statistical confidence intervals for the model-implied policy rates.
- **Visual Analytics**: Generates sensitivity charts showing policy rate requirements across different macro scenarios.

### 🚀 GDP Nowcast (GDPCastNow)
- **Quant Bridge Model**: Extracts latent macro factors using SVD/PCA from high-frequency indicators (Industrial Production, Retail Sales, Payrolls, etc.).
- **AI Sentiment Correction**: Scrapes news RSS feeds and official flash estimates (StatCan) to adjust quantitative forecasts with real-time sentiment.
- **Official Integration**: Direct scraping of StatCan "Daily" reports for the most recent economic outlooks.

## Usage

### 1. Requirements
Ensure you have the dependencies installed:
```bash
pip install -r requirements.txt
```

### 2. Execution
Run the unified CLI entry point:

**Analyze Policy Rates (Taylor Rule):**
```bash
python main.py policy --country US
python main.py policy --country Canada
```

**Run GDP Nowcast:**
```bash
python main.py gdp --country US
python main.py gdp --country Canada
```

## Configuration
The tool uses FRED (Federal Reserve Economic Data) for most macro indicators. An API key is required.
- Environment Variable: `FRED_API_KEY`
- Default: A fallback key is provided in the code but using your own is recommended.

---
*Powered by Antigravity AI*

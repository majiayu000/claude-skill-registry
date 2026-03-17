---
name: braiins-insights
description: Braiins Learn - Bitcoin mining profitability calculators, charts, and data dashboard
---

# Braiins Insights (Learn)

Interactive Bitcoin mining analytics platform providing profitability calculators, network charts, and mining data dashboard.

## Description

Braiins Insights (rebranded as "Braiins Learn") is a web-based analytics platform offering:

- **Profitability Calculator** - Comprehensive Bitcoin mining profit and ROI analysis
- **Charts & Data** - Network hashrate, difficulty, and mining economics visualization
- **Dashboard** - Real-time Bitcoin price, network statistics, and mining metrics
- **Educational Resources** - Links to blog posts and Bitcoin mining guides

**Platform URL**: https://learn.braiins.com

**Note**: This is an interactive web application, not traditional documentation. The skill describes the calculator features and how to use the tools.

## When to Use This Skill

Use this skill when you need to:
- **Calculate mining profitability** with detailed inputs (hashrate, power, electricity cost, BTC price)
- **Project future earnings** with difficulty and price increment modeling
- **Analyze break-even scenarios** for CapEx recovery and electricity costs
- **Model debt financing** for mining equipment purchases
- **Understand cost to mine 1 BTC** based on current network conditions
- **Compare mining scenarios** with different hardware configurations
- **Plan mining investments** with IRR and cash flow projections
- **Assess halving impact** on mining economics

## Platform Features

### Bitcoin Mining Profitability Calculator

**URL**: https://learn.braiins.com/en/profitability-calculator

**Time Period Configuration**:
- Future Projection (customizable months)
- Months to Next Halving (auto-calculated)

**Core Inputs**:
- **Currency**: USD or BTC
- **BTC Price**: Current or projected Bitcoin price
- **Network Difficulty**: Current mining difficulty
- **Hashrate**: Your mining equipment hashrate (TH/s)
- **Power Consumption**: Equipment wattage (W)
- **Electricity Price**: Cost per kWh (USD)
- **Block Subsidy**: Current block reward (3.125 BTC post-2024 halving)
- **Avg. Transaction Fees**: Per-block transaction fee earnings (BTC)

**Advanced Options**:
- **Revenue Fees & Downtime**: Pool fees and equipment downtime (%)
- **Profit Fees**: Additional operational fees (%)
- **Difficulty Increment**: Expected difficulty change (%/year)
- **Price Increment**: Expected BTC price change (%/year)
- **Halving Difficulty Drop**: Expected difficulty adjustment at halving (%)

**Debt Financing** (when enabled):
- Loan amount and terms
- Interest rates and payment schedules
- BTC collateral requirements
- Monthly payment calculations

### Profitability Metrics Calculated

**Break-Even Analysis**:
- **USD CapEx Break Even**: Months to recover equipment cost in USD
- **BTC CapEx Break Even**: Months to recover equipment cost in BTC
- **Electricity Break Even**: Maximum electricity price for profitability (USD/kWh)
- **Hardware Fully Depreciated**: Timeline for complete depreciation

**Financial Metrics**:
- **IRR**: Internal Rate of Return (%)
- **Cumulative Profit from Mining**: Total profit over projection period (USD)
- **Final Value of BTC Holdings**: Value of mined BTC at end (USD)
- **Total BTC Mined**: Cumulative Bitcoin earned

**Cost Analysis**:
- **Avg. Cost to Mine 1 BTC**: All-in cost per Bitcoin (USD)
- **Monthly Loan Payment**: Debt service if financing enabled (USD)
- **Total Cost of Loan**: Total interest paid over loan term (USD)
- **BTC Collateral for Loan**: Bitcoin required as collateral

### Visualization Tabs

**Profit & Cash Flow**:
- Monthly/cumulative profit charts
- Cash flow projections over time
- Revenue vs. expenses breakdown

**Balance Sheet**:
- Asset valuation over time
- Liability tracking for financed equipment
- Equity position evolution

**Cost of Production**:
- Cost to mine 1 BTC over time
- Break-even price analysis
- Operating expense trends

### Charts & Dashboard

**URL**: https://learn.braiins.com/en/charts

**Network Metrics**:
- Bitcoin network hashrate distribution
- Mining difficulty historical trends
- Block subsidy and halving timeline
- Transaction fee trends

**Dashboard** (https://learn.braiins.com/en):
- Real-time BTC price (USD)
- Current network statistics
- Quick links to calculators and charts

## Usage Example

### Basic Profitability Calculation

1. Navigate to https://learn.braiins.com/en/profitability-calculator
2. Configure inputs:
   - **Hashrate**: 100 TH/s (e.g., Antminer S19 Pro)
   - **Consumption**: 3250 W
   - **Electricity Price**: $0.06/kWh
   - **BTC Price**: $87,689 (current)
   - **Network Difficulty**: 148,258,433,855,481 (current)
   - **Block Subsidy**: 3.125 BTC (current epoch)
3. Review metrics:
   - Check break-even months
   - Analyze profitability at current conditions
   - Project future earnings with difficulty/price changes

### Advanced Scenario Modeling

1. Enable **Advanced Options**:
   - Set **Difficulty Increment**: 5%/year (conservative estimate)
   - Set **Price Increment**: 10%/year (bullish scenario)
   - Account for pool fees: 2%
2. Enable **Debt Financing** (if applicable):
   - Enter equipment loan amount
   - Set interest rate and term
   - Review monthly payment impact on cash flow
3. Compare scenarios:
   - Switch between USD and BTC break-even views
   - Analyze sensitivity to electricity price changes
   - Model halving impact with difficulty drop assumptions

## Quick Reference

### Calculator Shortcuts
- **User Guide**: Click "User Guide" button for in-app help
- **Share**: Generate shareable link to current calculation
- **Currency Toggle**: Switch between USD and BTC display

### Key Assumptions
- **Current Block Reward**: 3.125 BTC (post-April 2024 halving)
- **Next Halving**: ~2028 (3 years from now)
- **Average Block Time**: 10 minutes (~144 blocks/day)

### Profitability Rule of Thumb
```
Daily Revenue = (Hashrate / Network Hashrate) × 144 blocks × Block Reward
Daily Cost = (Power Consumption / 1000) × 24h × Electricity Price

Profitable if: Daily Revenue > Daily Cost
```

## Related Braiins Tools

- **Braiins Pool**: Mining pool for earning steady rewards (see braiins-pool skill)
- **Braiins OS**: Firmware for optimizing ASIC miner efficiency
- **Braiins Manager**: Fleet management for mining operations
- **Braiins Toolbox**: Collection of mining utilities and tools

## Notes

- **Platform Rebrand**: Formerly "Braiins Insights", now "Braiins Learn"
- **Interactive Tool**: This is a web application, not static documentation
- **Real-Time Data**: Calculator uses current network difficulty and BTC price
- **Projection Accuracy**: Future projections depend on difficulty/price increment assumptions
- **Educational Focus**: Platform includes links to blog, books, and learning resources
- **No Authentication Required**: Calculator is publicly accessible
- **Mobile Responsive**: Works on desktop and mobile browsers

## Limitations

- **No Documentation Pages**: Platform is primarily an interactive tool, not narrative docs
- **Dynamic Content**: All content is JavaScript-rendered (requires browser)
- **No API Access**: Calculator is web-only (no programmatic API documented)
- **Projection Uncertainty**: Future earnings depend heavily on BTC price and difficulty assumptions

---

**Generated by Skill Seeker** | Interactive Tool Documentation
**Last Updated**: 2025-12-28
**Platform URL**: https://learn.braiins.com
**Status**: Interactive web application (not traditional documentation)

---
name: braiins-ecosystem
description: Unified Braiins ecosystem skill covering all Bitcoin mining tools - OS firmware, Pool, Toolbox, Manager, Proxy, and Insights calculator
---

# Braiins Ecosystem

Comprehensive skill for the complete Braiins Bitcoin mining ecosystem - covering firmware, pool services, management tools, and profitability analysis.

## Description

The Braiins ecosystem provides an integrated suite of Bitcoin mining tools from hardware firmware to pool services and operational management:

- **Braiins OS** - ASIC miner firmware with API and build system
- **Braiins Pool** - Bitcoin mining pool (oldest active pool, est. 2010)
- **Braiins Toolbox** - Batch management GUI/CLI for mining operations
- **Braiins Manager** - Web-based monitoring and management dashboard
- **Braiins Farm Proxy** - Stratum V2 proxy for hashrate aggregation
- **Braiins Insights** - Interactive profitability calculator and analytics

**Official Resources:**
- [Braiins.com](https://braiins.com)
- [Braiins Academy](https://academy.braiins.com)
- [GitHub Organization](https://github.com/braiins)

## Ecosystem Overview

### The Complete Mining Stack

```
┌─────────────────────────────────────────────────────────┐
│                  Braiins Ecosystem                      │
├─────────────────────────────────────────────────────────┤
│  PLANNING                                               │
│  • Braiins Insights - Profitability calculator          │
├─────────────────────────────────────────────────────────┤
│  FIRMWARE                                               │
│  • Braiins OS - ASIC firmware with autotuning          │
│  • BOS+ API - Programmatic miner control               │
├─────────────────────────────────────────────────────────┤
│  MANAGEMENT                                             │
│  • Braiins Toolbox - Batch operations (GUI/CLI)        │
│  • Braiins Manager - Web dashboard monitoring          │
├─────────────────────────────────────────────────────────┤
│  NETWORKING                                             │
│  • Braiins Farm Proxy - Hashrate aggregation           │
│  • Stratum V2 - Enhanced mining protocol                │
├─────────────────────────────────────────────────────────┤
│  MINING                                                 │
│  • Braiins Pool - FPPS pool (0% fee with Braiins OS)   │
│  • Solo Mining - High-variance solo option              │
└─────────────────────────────────────────────────────────┘
```

## Quick Reference by Use Case

### Starting a New Mining Operation

1. **Plan Profitability** → Use **braiins-insights** skill
   - Calculate break-even scenarios
   - Model electricity costs and BTC price projections
   - Analyze IRR and cash flow with DPS modeling

2. **Select Hardware** → Consult **braiins-insights** skill
   - Review supported ASIC models (S21, S19, S17, M5x, M3x, M2x families)
   - Calculate cost to mine 1 BTC with different hardware

3. **Install Firmware** → Use **braiins-os** and **braiins-toolbox** skills
   - Deploy Braiins OS via Toolbox batch installation
   - Configure autotuning for efficiency
   - Set up BOS+ API for programmatic control

4. **Configure Mining** → Use **braiins-pool** skill
   - Connect to Braiins Pool (FPPS, 0% fee with Braiins OS)
   - Set up Lightning Network payouts for instant withdrawals
   - Enable Stratum V2 for enhanced security

5. **Monitor Operations** → Use **braiins-manager** skill
   - Real-time dashboards for hashrate, power, temperature
   - Alert configuration for proactive maintenance
   - Multi-user access for team collaboration

### Optimizing Existing Operations

**Performance Tuning** → **braiins-toolbox** + **braiins-os**
- Batch-set power/hashrate targets across devices
- Enable DPS (Dynamic Power Scaling) for electricity cost optimization
- Configure cooling modes and temperature thresholds

**Large-Scale Management** → **braiins-toolbox** + **braiins-manager** + **braiins-proxy**
- Use Toolbox for batch firmware updates
- Aggregate hashrate through Farm Proxy
- Monitor fleet through Manager dashboard

**Profitability Analysis** → **braiins-insights** + **braiins-pool**
- Calculate current mining profitability
- Model halving impact on revenue
- Track actual rewards via Pool statistics

## Individual Skill Summaries

### 1. Braiins OS (braiins-os skill)
**Purpose**: Bitcoin mining ASIC firmware with advanced features

**Key Features**:
- **Autotuning**: Automatic power/hashrate optimization
- **BOS+ API**: REST API for programmatic miner management (v1.8.0)
- **Build System**: Package feeds for customization
- **Stratum V2**: Enhanced mining protocol support

**When to Use**:
- Installing/upgrading ASIC miner firmware
- Building custom firmware configurations
- Integrating miners with automation systems
- Accessing miner metrics programmatically

**Quick Commands**:
```bash
# API example (requires BOS+ API)
curl -X GET "http://miner-ip/api/v1/status"
```

---

### 2. Braiins Pool (braiins-pool skill)
**Purpose**: Bitcoin mining pool (oldest active pool, est. 2010)

**Key Features**:
- **FPPS Rewards**: Full Pay Per Share with transaction fee inclusion
- **0% Fees**: When mining with Braiins OS firmware
- **Lightning Payouts**: Instant, low-cost Bitcoin transfers
- **Stratum V2**: Next-generation mining protocol
- **Solo Mining**: 0.5% fee, anonymous mining option
- **API Access**: Full JSON API for custom integrations

**When to Use**:
- Connecting miners to mining pool
- Setting up Lightning Network payouts
- Calculating FPPS reward estimates
- Implementing Stratum V2 protocol
- Solo mining with low fees

**Quick Commands**:
```bash
# Pool connection
stratum+tcp://stratum.braiins.com:3333

# Solo mining
stratum+tcp://solo.stratum.braiins.com:3333
```

**Pool Stats**:
- Current Block Reward: 3.125 BTC (post-2024 halving)
- Pool Fee: 2.5% standard, 0% with Braiins OS
- Payout Schedule: Daily at 9:00 UTC

---

### 3. Braiins Insights (braiins-insights skill)
**Purpose**: Interactive Bitcoin mining profitability calculator

**Key Features**:
- **Profitability Calculator**: Comprehensive ROI analysis with customizable inputs
- **Future Projections**: Model difficulty and price changes over time
- **Break-Even Analysis**: CapEx recovery timelines in USD and BTC
- **Debt Financing**: Loan modeling with payment schedules
- **Cost Analysis**: Calculate cost to mine 1 BTC
- **Halving Impact**: Model next halving effect on revenue

**When to Use**:
- Planning mining investments
- Calculating break-even scenarios
- Modeling debt financing options
- Analyzing halving impact
- Comparing mining hardware profitability

**Calculator Inputs**:
- Hashrate (TH/s), Power Consumption (W)
- Electricity Price (USD/kWh)
- BTC Price, Network Difficulty
- Difficulty/Price increment rates
- Optional: Loan amount, interest rate, DPS parameters

**URL**: https://learn.braiins.com/en/profitability-calculator

---

### 4. Braiins Toolbox (braiins-toolbox skill)
**Purpose**: Batch management tool for mining operations (GUI + CLI)

**Key Features**:
- **Network Scanning**: Discover miners on local network (Antminers, Whatsminers, Avalons, Icerivers)
- **Firmware Management**: Batch install/uninstall/upgrade Braiins OS
- **System Management**: Reboot, collect data/logs, locate devices
- **Miner Management**: Configure pools, start/stop mining
- **Performance Tuning**: Set power/hashrate targets, enable DPS
- **Cooling Management**: Configure fan speeds and temperatures
- **Keyboard Shortcuts**: Command Palette (⌘+P / Ctrl+P) for mouse-free workflow

**When to Use**:
- Managing multiple miners simultaneously
- Scanning network for device discovery
- Deploying Braiins OS remotely
- Batch configuration changes
- Automating workflows with CLI

**Quick Commands**:
```bash
# Scan network
$ ./braiins-toolbox scan '10.10.10-11.*'

# Install Braiins OS
$ ./braiins-toolbox firmware install '10.10.10-11.*'

# Set pool URLs
$ ./braiins-toolbox miner set-pool-urls \
  --url 'stratum+tcp://user@stratum.braiins.com:3333' \
  '10.10.10-11.*'

# Set power target
$ ./braiins-toolbox tuner target --power 3318 '10.10.10-11.*'
```

**Platform Support**: Windows, macOS, Linux (x86_64, aarch64, armv7)

---

### 5. Braiins Manager (braiins-manager skill)
**Purpose**: Web-based dashboard for mining fleet monitoring

**Key Features**:
- **Real-Time Monitoring**: Live hashrate, power, temperature
- **Fleet Organization**: Group miners by site, model, or custom criteria
- **Performance Analytics**: Historical data and trend analysis
- **Alert System**: Email/SMS notifications for issues
- **Multi-User Access**: Role-based permissions (admin, operator, viewer)
- **Remote Configuration**: Adjust settings from centralized interface

**When to Use**:
- Monitoring mining operations at scale
- Managing multiple sites geographically
- Setting up proactive maintenance alerts
- Collaborating with team members
- Analyzing performance trends

**Access**:
- Cloud: manager.braiins.com
- Self-Hosted: Deploy on-premise for air-gapped operations

**Note**: Placeholder skill - full documentation at https://academy.braiins.com/en/braiins-manager/

---

### 6. Braiins Farm Proxy (braiins-proxy skill)
**Purpose**: High-performance mining proxy for hashrate aggregation

**Key Features**:
- **Protocol Support**: Stratum V1 and V2
- **Hashrate Aggregation**: Combine multiple miners into single upstream connection
- **Failover Protection**: Automatic pool switching
- **Bandwidth Optimization**: Reduce internet usage for large farms
- **Latency Reduction**: Local proxy closer to miners

**When to Use**:
- Aggregating hashrate from 100+ miners
- Implementing failover to backup pools
- Reducing bandwidth costs
- Deploying Stratum V2 across operations
- Optimizing connection stability

**Deployment Pattern**:
```
Miners (1000s) → Farm Proxy → Mining Pool
  ↓ Stratum V1/V2   ↓ Aggregated    ↓ Single connection
```

**Note**: Placeholder skill - full documentation at https://academy.braiins.com/en/braiins-proxy/

---

## Integration Workflows

### Complete Mining Farm Setup

```bash
# 1. Plan profitability (Insights)
Visit: https://learn.braiins.com/en/profitability-calculator

# 2. Scan and discover miners (Toolbox)
$ ./braiins-toolbox scan '10.10.*.*' --output devices.csv

# 3. Install Braiins OS firmware (Toolbox → OS)
$ ./braiins-toolbox firmware install \
  --contract-code 'XYZ' \
  '10.10.*.*'

# 4. Configure mining pool (Toolbox → Pool)
$ ./braiins-toolbox miner set-pool-urls \
  --url 'stratum+tcp://user@stratum.braiins.com:3333' \
  '10.10.*.*'

# 5. Enable DPS and set power targets (Toolbox → OS)
$ ./braiins-toolbox tuner set-dps on \
  --power-step 200 \
  --min-power-target 2500 \
  '10.10.*.*'

# 6. Monitor operations (Manager)
Login to: manager.braiins.com
```

### Optimizing for Low Electricity Costs

**Scenario**: Take advantage of cheap overnight electricity

1. **Calculate Economics** (Insights):
   - Model DPS with price increment assumptions
   - Set shutdown thresholds for peak hours

2. **Configure DPS** (Toolbox):
   ```bash
   $ ./braiins-toolbox tuner set-dps on \
     --shutdown-enabled true \
     --shutdown-duration 8 \
     '10.10.*.*'
   ```

3. **Monitor Impact** (Manager):
   - Track profitability over 24-hour cycles
   - Adjust thresholds based on actual costs

### Multi-Site Mining Operation

1. **Deploy Farm Proxies** (Proxy):
   - One proxy per site for local aggregation
   - Reduces WAN bandwidth to pool

2. **Centralized Management** (Manager):
   - Organize sites in Manager dashboard
   - Set site-specific alert thresholds

3. **Batch Operations** (Toolbox):
   - Use Toolbox CLI for scripted updates
   - Schedule maintenance windows per site

4. **Profitability Tracking** (Insights + Pool):
   - Compare site profitability
   - Optimize power targets per location

---

## Braiins Advantages

### 0% Pool Fees
When using Braiins OS firmware with Braiins Pool, miners pay 0% pool fees (standard 2.5% fee is fully rebated).

### Integrated Ecosystem
All tools work seamlessly together:
- Toolbox can deploy OS firmware
- OS firmware integrates with Manager monitoring
- Pool statistics feed into Insights profitability models
- Proxy optimizes connections to Pool

### Stratum V2
Braiins pioneered Stratum V2 protocol, offering:
- Enhanced security (encrypted connections)
- Job negotiation (miners choose transaction sets)
- Bandwidth efficiency
- Support across OS, Pool, and Proxy

### Lightning Network Payouts
Instant, low-cost Bitcoin withdrawals from Pool via Lightning Network.

---

## Related Skills

For detailed information, use individual skills:
- **braiins-os** - ASIC firmware and API documentation
- **braiins-pool** - Mining pool configuration and solo mining
- **braiins-insights** - Profitability calculator and financial modeling
- **braiins-toolbox** - Batch management and network scanning
- **braiins-manager** - Fleet monitoring and alerts (placeholder)
- **braiins-proxy** - Hashrate aggregation and failover (placeholder)

---

## External Resources

- **Official Website**: https://braiins.com
- **Academy**: https://academy.braiins.com
- **GitHub**: https://github.com/braiins
- **Pool Dashboard**: https://braiins.com/pool
- **Manager Dashboard**: https://manager.braiins.com
- **Insights Calculator**: https://learn.braiins.com

---

## Notes

- **Ecosystem Completeness**: Covers planning (Insights), firmware (OS), management (Toolbox/Manager), networking (Proxy), and mining (Pool)
- **Zero-Fee Advantage**: Braiins OS + Braiins Pool = 0% pool fees
- **Protocol Leadership**: Braiins developed Stratum V2, supported across ecosystem
- **Scale Support**: Tools designed for operations from single miner to thousands of devices
- **Open Source**: Many components available on GitHub for customization
- **Active Development**: Regular updates across all tools (BOS+ API v1.8.0 as of Nov 2025)

---

**Generated by Skill Seeker** | Ecosystem Integration Skill
**Last Updated**: 2025-12-28
**Component Skills**: 6 individual Braiins skills unified
**Total Documentation**: 200+ pages across all skills combined

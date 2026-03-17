---
name: braiins-pool
description: Comprehensive Braiins Pool skill - oldest Bitcoin mining pool with FPPS rewards, Lightning payouts, and Stratum V2 support
---

# Braiins Pool

Comprehensive skill for Braiins Pool - the oldest active Bitcoin mining pool in the world (est. 2010), formerly known as "bitcoin.cz" and "Slush Pool".

## Description

This skill provides complete coverage of Braiins Pool's mining services, including:

- **Pool Mining** - FPPS (Full Pay Per Share) reward model with guaranteed payouts
- **Quick Start Guide** - Complete setup instructions for miners
- **Mining Configuration** - Hardware setup, worker management, and monitoring
- **Hashrate Specification** - Understanding nominal vs. effective hashrate
- **Rewards & Payouts** - FPPS calculation, Lightning Network integration, payout customization
- **User Account Management** - Security, access profiles, 2FA, and history exports
- **Device Monitoring** - Email/mobile alerts, API configuration, worker states
- **Stratum V2** - Next-generation mining protocol with enhanced security
- **Solo Mining** - High-risk, high-reward solo mining option
- **Comprehensive FAQs** - Mining basics, ASIC hardware, profitability guidance

**Official Resources:**
- [Braiins Pool](https://braiins.com/pool)
- [Braiins Pool Academy](https://academy.braiins.com/en/braiins-pool/about/)
- [Solo Mining](https://solo.braiins.com)

## When to Use This Skill

Use this skill when you need to:
- **Set up Bitcoin mining** with Braiins Pool for the first time
- **Configure mining devices** (ASIC miners) to connect to the pool
- **Understand hashrate metrics** (nominal, effective, scoring)
- **Calculate mining rewards** using FPPS model with coinbase and transaction fee cuts
- **Set up Lightning payouts** for instant, low-cost Bitcoin transfers
- **Manage user accounts** with 2FA, access profiles, and watcher links
- **Monitor mining devices** with email/mobile alerts and API integrations
- **Implement Stratum V2** protocol for enhanced security and efficiency
- **Try solo mining** for high-variance, high-reward Bitcoin mining
- **Troubleshoot mining issues** including stale rates, connection problems, hardware failures
- **Understand pool fees** and how to get 0% fees with Braiins OS
- **Select mining hardware** (ASIC miners for SHA-256 algorithm)
- **Learn about Bitcoin halvings** and their impact on mining rewards

## Quick Reference

### Pool Information
- **Founded**: 2010 (first block mined)
- **Former Names**: bitcoin.cz, Slush Pool
- **Reward Model**: FPPS (Full Pay Per Share)
- **Pool Fee**: 2.5% (0% when using Braiins OS firmware)
- **Payout Schedule**: Daily at 9:00 UTC
- **Current Block Reward**: 3.125 BTC (post-2024 halving)

### Connection Details
**Pool URL**: `stratum+tcp://stratum.braiins.com:3333`
**User ID Format**: `userName.workerName`
**Stratum V2**: Default port 3336 (automatic location-based routing)

### Quick Start
```bash
# Configuration needed:
# 1. Pool URL: stratum+tcp://stratum.braiins.com:3333
# 2. User ID: yourUsername.workerName
# 3. Password: anything (not used)

# For Stratum V2:
# Pool URL includes public key for authentication
# Requires Braiins OS firmware
```

### Solo Mining
```bash
# Solo Mining URLs:
stratum+tcp://solo.stratum.braiins.com:3333
stratum+tcp://solo.stratum.braiins.com:443
stratum+tcp://solo.stratum.braiins.com:25

# Username: <bitcoin_address>.<optional_workername>
# Fee: 0.5% (credited to CKPool authors)
# Check stats: https://solo.braiins.com/stats/<bitcoin_address>
```

### FPPS Reward Formula
```
Coinbase Reward Cut (CRC) = (S × C) / (D × 2^32)
Transaction Fee Cut (TFC) = (AF × S) / (D × 2^32)
Total Reward (TR) = CRC + TFC - Pool Fee

Where:
  S = Shares submitted
  C = Coinbase block reward (3.125 BTC)
  D = Network difficulty
  AF = Average mining fee
```

### API Endpoints
- **Pool Stats**: `https://pool.braiins.com/stats/json/btc`
- **User Profile**: `https://pool.braiins.com/accounts/profile/json/btc/`
- **Daily Rewards**: `https://pool.braiins.com/accounts/rewards/json/btc?from=YYYY-MM-DD&to=YYYY-MM-DD`
- **Workers**: `https://pool.braiins.com/accounts/workers/json/btc`
- **Payouts**: `https://pool.braiins.com/accounts/payouts/json/btc?from=YYYY-MM-DD&to=YYYY-MM-DD`

**Authentication**: Include `Pool-Auth-Token` or `X-Pool-Auth-Token` in HTTP header

## Available References

### Setup & Configuration
- `references/about.md` - Pool history and overview
- `references/quick-start.md` - Quick setup guide for miners
- `references/bitcoin-mining-setup.md` - Complete setup walkthrough

### Mining Operations
- `references/hashrate-specification.md` - Understanding hashrate metrics
- `references/rewards-and-payouts.md` - FPPS model, Lightning payouts, payout customization
- `references/monitoring.md` - Device monitoring, mobile app, API configuration

### Account Management
- `references/user-accounts.md` - Account security, access profiles, 2FA, history exports

### Advanced Features
- `references/stratum-v2-manual.md` - Next-gen mining protocol setup
- `references/solo-mining.md` - Solo mining configuration and statistics

### Help & Troubleshooting
- `references/faqs-mining-basics.md` - Comprehensive FAQs covering ASIC miners, hardware selection, halvings, stale rates, orphan blocks

## Usage

### Setting Up Mining

1. **Register Account**: Sign up at https://braiins.com/pool
2. **Configure Miner**: See `quick-start.md` for device-specific instructions
3. **Register Payout Address**: Set Bitcoin or Lightning address in Funds > Wallets
4. **Enable Monitoring**: Configure alerts in Mining > Settings > Reporting

### Understanding Rewards

See `rewards-and-payouts.md` for detailed FPPS calculation:
- Coinbase reward cut based on network difficulty and shares submitted
- Transaction fee cut based on average block fees
- Daily reward calculation at 9:00 UTC
- Lightning or on-chain payout options

### API Integration

See `monitoring.md` for complete API documentation:
- Generate access token in Settings > Access Profiles
- Use `Pool-Auth-Token` header for authentication
- Rate limit: ~1 request per 5 seconds
- Available endpoints: stats, profile, workers, rewards, payouts

### Troubleshooting

See `faqs-mining-basics.md` for common issues:
- **How to check if mining**: Look for share submissions (~1/5sec), non-zero 5min hashrate
- **Stale rate issues**: Check network latency and mining device performance
- **Profitability**: Use Cost to Mine 1 BTC calculator for break-even analysis

## Key Features

### Financial Account System
- **Financial Accounts**: Storage for confirmed mining rewards
- **Reward Splits**: Automatically distribute rewards across multiple accounts
- **Payout Rules**: Customize payout frequency (daily/weekly/monthly) or threshold-based
- **Lightning Network**: Instant payouts with near-zero fees via Lightning addresses

### Monitoring & Alerts
- **Worker States**: OK, Low, Offline, Disabled
- **5-Minute Snapshots**: Effective hashrate monitoring
- **Email Alerts**: Configurable threshold-based notifications
- **Mobile App**: iOS and Android apps for on-the-go monitoring (not for mining)
- **API Access**: Full JSON API for custom integrations

### Security Features
- **2FA Support**: TOTP (mobile app) and U2F (hardware tokens like Trezor)
- **Access Profiles**: Granular permissions (full, read-only, limited read-only)
- **Watcher Links**: Anonymous read-only access via shareable URLs
- **API Token Management**: Regenerable tokens per access profile

## Notes

- **Pool History**: Oldest active Bitcoin pool, mining since 2010
- **Fee Structure**: 2.5% standard fee, 0% when using Braiins OS firmware
- **Stratum V2**: Requires Braiins OS firmware (stock firmware uses Stratum V1)
- **Lightning Payouts**: Custodial wallets work seamlessly; self-custodial wallets require 24h+ invoice expiration
- **Solo Mining**: 0.5% fee (credited to CKPool), anonymous (no registration required)
- **API Rate Limits**: ~1 request per 5 seconds; exceeding may result in IP ban
- **Worker Monitoring**: 5-minute snapshots; designated worker names enable per-device tracking
- **Halving Impact**: Next halving ~2028, reducing reward from 3.125 BTC to 1.5625 BTC

## Academy Content Integration

✅ **Successfully Scraped** (10 Academy pages, ~59KB):
- Complete setup guides (quick start, Bitcoin mining setup)
- Hashrate specification and FPPS reward mathematics
- Rewards, payouts, and Lightning Network integration
- User account management and security features
- Comprehensive monitoring and API documentation
- Stratum V2 protocol specifications
- Solo mining configuration and statistics
- Extensive FAQs covering mining basics, hardware, profitability

---

**Generated by Skill Seeker** | Comprehensive Multi-Source Scraper
**Last Updated**: 2025-12-28
**Total References**: 10 files (59KB)
**Sources**: Braiins Pool Academy (Playwright-scraped JavaScript-rendered content)

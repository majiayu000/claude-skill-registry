---
name: apple-search-ads
description: Manage Apple Search Ads campaigns, keywords, and reporting. Use when setting up campaigns, adding keywords, checking performance, or optimizing Apple Search Ads for any iOS app. Implements Apple's recommended 4-campaign structure (Brand, Category, Competitor, Discovery).
allowed-tools: Bash, Read, Grep, Glob
---

# Apple Search Ads Management

Full management of Apple Search Ads campaigns for iOS apps using the ASA CLI tool.

## Capabilities

This skill enables you to:
- Set up Apple's recommended 4-campaign structure
- Add keywords with automatic routing (exact → target, broad → discovery, negative → discovery)
- Block irrelevant search terms with negative keywords
- Promote winning keywords from Discovery to exact match campaigns
- Generate performance reports (campaign, keyword, search term level)
- Audit campaign structure against Apple's best practices
- Pause/enable campaigns
- **Automated optimization** - analyze search terms and batch promote/block keywords

## Prerequisites

### Running with uv (Recommended)

No installation required. Just use `uv run`:

```bash
cd /path/to/apple-search-ads-cli
uv run asa config setup
uv run asa campaigns list
```

### Alternative: pip install

```bash
cd /path/to/apple-search-ads-cli
pip install -e .
asa config setup
```

### Configuration

```bash
uv run asa config setup
```

You'll need from Apple Ads dashboard (https://ads.apple.com/):
- Organization ID
- Client ID, Team ID, Key ID
- Private key file (EC key pair)

To generate keys:
```bash
openssl ecparam -genkey -name prime256v1 -noout -out private-key.pem
openssl ec -in private-key.pem -pubout -out public-key.pem
```

### Verify Setup

```bash
asa config test
```

---

## Command Reference

### Configuration Commands

| Command | Description |
|---------|-------------|
| `asa config setup` | Interactive credential and app setup |
| `asa config show` | Display current configuration |
| `asa config test` | Test API connection |

### Campaign Commands

| Command | Description |
|---------|-------------|
| `asa campaigns list` | List all campaigns |
| `asa campaigns list --bids` | Include ad group default bids |
| `asa campaigns list --filter "term"` | Filter campaigns by name |
| `asa campaigns list --status RUNNING` | Filter by status (RUNNING, PAUSED) |
| `asa campaigns create <name>` | Create a new campaign |
| `asa campaigns update <ID>` | Update campaign name/budget/status |
| `asa campaigns audit` | Check structure vs Apple recommendations |
| `asa campaigns audit --verbose` | Show detailed ad group info |
| `asa campaigns setup` | Create 4-campaign structure |
| `asa campaigns setup --dry-run` | Preview without creating |
| `asa campaigns pause <ID>` | Pause specific campaign |
| `asa campaigns pause --all` | Pause all managed campaigns |
| `asa campaigns enable <ID>` | Enable specific campaign |
| `asa campaigns enable --all` | Enable all managed campaigns |
| `asa campaigns delete <ID>` | Delete specific campaign |

### Ad Group Commands

| Command | Description |
|---------|-------------|
| `asa adgroups list <campaign_id>` | List ad groups for a campaign |
| `asa adgroups create <name> -c <campaign_id>` | Create a new ad group |
| `asa adgroups update <ID> -c <campaign_id>` | Update ad group settings |
| `asa adgroups pause <ID> -c <campaign_id>` | Pause an ad group |
| `asa adgroups enable <ID> -c <campaign_id>` | Enable an ad group |
| `asa adgroups delete <ID> -c <campaign_id>` | Delete an ad group |

### Keyword Commands

| Command | Description |
|---------|-------------|
| `asa keywords list` | List keywords (interactive selection) |
| `asa keywords list --campaign <ID>` | List keywords for specific campaign |
| `asa keywords list --negatives` | List negative keywords |
| `asa keywords list --filter "term"` | Filter keywords containing text |
| `asa keywords list --status ACTIVE` | Filter by status (ACTIVE, PAUSED) |
| `asa keywords list --match-type EXACT` | Filter by match type (EXACT, BROAD) |
| `asa keywords add "<kw1>,<kw2>" --type brand` | Add brand keywords |
| `asa keywords add "<kw1>,<kw2>" --type category` | Add category keywords |
| `asa keywords add "<kw1>,<kw2>" --type competitor` | Add competitor keywords |
| `asa keywords add-negatives "<kw1>,<kw2>" --all` | Block terms in all campaigns |
| `asa keywords add-negatives "<kw1>,<kw2>" --all --force` | Block terms without confirmation |
| `asa keywords promote "<kw1>,<kw2>" --target category` | Graduate from Discovery |
| `asa keywords delete` | Delete keywords (interactive) |
| `asa keywords delete --ids "123,456" --force` | Delete specific keywords by ID |
| `asa keywords update-bid --bid 2.50` | Update keyword bid amount |
| `asa keywords pause` | Pause a keyword |
| `asa keywords pause --all` | Pause all active keywords in ad group |
| `asa keywords enable` | Enable a paused keyword |
| `asa keywords enable --all` | Enable all paused keywords in ad group |

### Report Commands

| Command | Description |
|---------|-------------|
| `asa reports summary` | Performance summary (last 30 days) |
| `asa reports summary --days 7` | Custom date range |
| `asa reports keywords` | Keyword performance |
| `asa reports keywords --sort cpa` | Sort by CPA |
| `asa reports adgroups --all` | Ad group performance for all campaigns |
| `asa reports adgroups --campaign <ID>` | Ad group performance for specific campaign |
| `asa reports impression-share --all` | Impression share / Share of Voice report |
| `asa reports impression-share --min-impressions 50` | Filter by minimum impressions |
| `asa reports search-terms` | All search terms |
| `asa reports search-terms --winners` | Terms to promote (good CPA) |
| `asa reports search-terms --negatives` | Terms to block (spend, no installs) |

### Optimization Commands

| Command | Description |
|---------|-------------|
| `asa optimize` | Run automated optimization workflow |
| `asa optimize --dry-run` | Preview changes without applying |
| `asa optimize --days 7` | Analyze last 7 days (default: 14) |
| `asa optimize --cpa-threshold 3.00` | Max CPA for winners (default: $5.00) |
| `asa optimize --min-installs 3` | Min installs to promote (default: 2) |
| `asa optimize --min-spend 2.00` | Min spend to block (default: $1.00) |
| `asa optimize --min-impressions 100` | Min impressions to consider a term |
| `asa optimize --exclude "term1,term2"` | Exclude specific terms from analysis |
| `asa optimize --target brand` | Target campaign type (default: category) |
| `asa optimize --auto-approve` | Skip confirmation prompts |
| `asa optimize --json` | Output results as JSON (implies --dry-run) |

---

## Campaign Structure

Apple's recommended 4-campaign structure:

| Campaign | Purpose | Match Type | Search Match |
|----------|---------|------------|--------------|
| **Brand** | App/company name | Exact | OFF |
| **Category** | App functionality | Exact | OFF |
| **Competitor** | Competitor apps | Exact | OFF |
| **Discovery** | Keyword mining | Broad + Search Match | ON |

### Keyword Routing

When you add keywords with `--type brand/category/competitor`:
1. **EXACT match** → Target campaign
2. **BROAD match** → Discovery (for mining related terms)
3. **NEGATIVE** → Discovery (prevents double-paying)

---

## Common Workflows

### Initial Setup

```bash
# 1. Configure (no installation required with uv)
cd /path/to/apple-search-ads-cli
uv run asa config setup
# Enter: Org ID, Client ID, Team ID, Key ID, private key path
# Enter: App ID, App name, Countries, Default bid

# 2. Test connection
uv run asa config test

# 3. Audit existing campaigns
uv run asa campaigns audit

# 4. Create 4-campaign structure (preview first)
uv run asa campaigns setup --countries US --budget 50 --dry-run
uv run asa campaigns setup --countries US --budget 50
```

### Adding Initial Keywords

```bash
# Brand keywords (your app name)
asa keywords add "myapp,myapp app,my app" --type brand

# Category keywords (what your app does)
asa keywords add "photo editor,image filter,picture effects" --type category

# Competitor keywords (other apps)
asa keywords add "vsco,snapseed,lightroom" --type competitor
```

### Weekly Optimization

**Option 1: Automated (Recommended)**

```bash
# Preview what will change
asa optimize --dry-run

# Run optimization with confirmation
asa optimize

# Or run automatically without prompts
asa optimize --auto-approve
```

The `asa optimize` command automatically:
1. Analyzes Discovery search terms (last 14 days)
2. Identifies winners (≥2 installs, CPA ≤ $5)
3. Identifies losers (≥$1 spend, 0 installs)
4. Promotes winners to target campaign (adds as exact + negative in Discovery)
5. Blocks losers across all managed campaigns

**Option 2: Manual**

```bash
# 1. Check overall performance
asa reports summary --days 7

# 2. Find winning search terms
asa reports search-terms --winners

# 3. Promote winners to exact match
asa keywords promote "best photo app,picture editor free" --target category

# 4. Find wasted spend
asa reports search-terms --negatives

# 5. Block wasteful terms
asa keywords add-negatives "auto clicker,signal app,testflight,crypto trading" --all
```

### Troubleshooting

```bash
# Check campaign structure issues
asa campaigns audit --verbose

# List all campaigns including non-managed
asa campaigns list --all

# Check specific campaign keywords
asa keywords list --campaign 12345

# Check negative keywords
asa keywords list --negatives --campaign 12345
```

---

## Campaign Naming

The CLI identifies campaign types by looking for these keywords in the campaign name (case-insensitive):

| Keyword | Campaign Type |
|---------|---------------|
| `brand` | Brand campaign |
| `category` | Category campaign |
| `competitor` | Competitor campaign |
| `discovery` | Discovery campaign |

Examples of valid names:
- `Brand` (simple)
- `My Brand Campaign`
- `MyApp Category`
- `competitor-us`

---

## Example Keywords

### Brand Keywords (your app/company name)
```
[appname], [appname] app, [company] invest
```

### Category Keywords (what your app does)
```
photo editor, image filter, picture effects, camera app
```

### Competitor Keywords (competing apps)
```
[competitor1] app, [competitor2], [competitor3]
```

### Common Negative Keywords (block these)
```
auto clicker, signal app, testflight, crypto trading, forex trading, stock trading, day trading
```

---

## API Coverage

The CLI covers these Apple Search Ads API operations:

| Category | Operations |
|----------|------------|
| **Campaigns** | list, get, create, update, pause, enable, delete |
| **Ad Groups** | list, create, update, pause, enable, delete |
| **Keywords** | list, add, add negatives, delete, update bid, pause, enable |
| **Reports** | campaign, keyword, search terms |

**Not yet implemented** (advanced features):
- Creative sets
- Geo-targeting beyond country level
- Budget orders

---

## API Notes

**Bulk Operations**: The CLI uses Apple's bulk API endpoints for keyword operations (enable, pause, delete, update bid). These are more efficient than individual requests.

**Caching**: Apple's API may show stale data after delete operations. If keywords still appear in listings after deletion, the delete was successful but the cache hasn't refreshed. Attempting to modify deleted keywords will return "keyword deleted" errors.

**Search Terms Reports**: Search term reports require campaigns to have accumulated sufficient data (typically a few days of activity). New campaigns may return empty results.

**Error Handling**: Keyword add operations (`add_keywords`, `add_negative_keywords`) return both successful additions and any errors (e.g., duplicate keywords). The CLI displays both:
- Successfully added keywords are shown in green
- Duplicates or other errors are shown with details but don't fail the overall operation

**Authentication Retry**: The CLI automatically retries requests (up to 2 times) when authentication tokens expire, refreshing the token transparently.

---

## Documentation

- **Apple Best Practices**: https://ads.apple.com/app-store/best-practices/campaign-structure
- **Apple API Docs**: https://developer.apple.com/documentation/apple_ads

---
name: autotrader
description: Search millions of new and used cars from dealers and private sellers.
category: automotive
---
# Autotrader Skill

Search millions of new and used cars from dealers and private sellers.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/autotrader/install.sh | bash
```

Or manually:
```bash
cp -r skills/autotrader ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set AUTOTRADER_EMAIL "your_email"
canifi-env set AUTOTRADER_PASSWORD "your_password"
```

## Privacy & Authentication

**Your credentials, your choice.** Canifi LifeOS respects your privacy.

### Option 1: Manual Browser Login (Recommended)
If you prefer not to share credentials with Claude Code:
1. Complete the [Browser Automation Setup](/setup/automation) using CDP mode
2. Login to the service manually in the Playwright-controlled Chrome window
3. Claude will use your authenticated session without ever seeing your password

### Option 2: Environment Variables
If you're comfortable sharing credentials, you can store them locally:
```bash
canifi-env set SERVICE_EMAIL "your-email"
canifi-env set SERVICE_PASSWORD "your-password"
```

**Note**: Credentials stored in canifi-env are only accessible locally on your machine and are never transmitted.

## Capabilities

1. **Search Listings**: Find cars with advanced filters
2. **Save Favorites**: Bookmark vehicles of interest
3. **Price Analysis**: View market pricing data
4. **Dealer Contact**: Connect with sellers
5. **Trade-In Value**: Estimate your car's worth

## Usage Examples

### Search Cars
```
User: "Find certified pre-owned BMWs on Autotrader"
Assistant: Returns matching listings
```

### Check Price
```
User: "Is this car priced fairly?"
Assistant: Returns market comparison
```

### Save Listing
```
User: "Save this car to my favorites"
Assistant: Adds to saved list
```

### Get Trade Value
```
User: "What's my car worth for trade-in?"
Assistant: Returns estimated value
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Dealer network integration

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Listing Gone | Sold or removed | Search again |
| Contact Failed | Dealer issue | Try phone |
| Value Error | VIN issue | Verify details |

## Notes

- Largest online marketplace
- New and used cars
- Dealer and private listings
- No public API
- Price comparison tools
- Certified pre-owned options

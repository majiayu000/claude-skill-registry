---
name: turo
description: Rent unique cars from local hosts or share your own vehicle.
category: automotive
---
# Turo Skill

Rent unique cars from local hosts or share your own vehicle.

## Quick Install

```bash
curl -sSL https://canifi.com/skills/turo/install.sh | bash
```

Or manually:
```bash
cp -r skills/turo ~/.canifi/skills/
```

## Setup

Configure via [canifi-env](https://canifi.com/setup/scripts):

```bash
# First, ensure canifi-env is installed:
# curl -sSL https://canifi.com/install.sh | bash

canifi-env set TURO_EMAIL "your_email"
canifi-env set TURO_PASSWORD "your_password"
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

1. **Search Cars**: Find available rentals nearby
2. **Book Trip**: Reserve vehicles for trips
3. **Host Vehicle**: List your car for sharing
4. **Manage Bookings**: View and modify reservations
5. **Earnings Track**: Monitor hosting income

## Usage Examples

### Find Car
```
User: "Find a convertible on Turo for this weekend"
Assistant: Returns available convertibles
```

### Book Rental
```
User: "Book this Tesla on Turo"
Assistant: Initiates booking process
```

### Check Earnings
```
User: "How much have I earned hosting on Turo?"
Assistant: Returns hosting earnings
```

### List Vehicle
```
User: "List my car on Turo"
Assistant: Starts listing process
```

## Authentication Flow

1. Account-based authentication
2. No official API
3. Browser automation required
4. Insurance verification

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Login Failed | Invalid credentials | Check account |
| Booking Failed | Unavailable | Try different dates |
| Listing Error | Verification needed | Complete profile |
| Payment Failed | Card issue | Update payment |

## Notes

- Peer-to-peer car sharing
- Unique vehicle selection
- Insurance included
- Host earnings potential
- No public API
- Mobile app required for trips

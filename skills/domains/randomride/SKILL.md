---
name: randomride
description: "One-click random ride booking to interesting nearby places. Intelligently picks destinations (restaurants, bars, parks, museums) and books real Uber/Lyft/Grab rides. Learns preferences over time with controlled randomness. Use when: feeling adventurous, want spontaneous outings, exploring a city. NOT for: specific destinations, commuting, or planned trips."
homepage: https://pawhub.ai/randomride
metadata:
  {
    "openpaw":
      {
        "emoji": "🎲",
        "requires": { "bins": ["python3"] },
        "install":
          [{ "id": "bundled", "kind": "bundled", "label": "Random Ride (bundled Python skill)" }],
      },
  }
---

# Random Ride 🎲

One-click random ride booking to interesting places. Press a button, go somewhere interesting.

## When to Use

- **Feeling adventurous** - Want to discover new places spontaneously
- **Exploring a city** - Let randomness guide you to interesting spots
- **Breaking routine** - Need to get out but don't know where to go
- **Date night** - Surprise your partner with a mystery destination
- **Solo adventure** - Trust the algorithm to find something fun

## When NOT to Use

- **Specific destination** - Use regular Uber/Lyft if you know where you're going
- **Commuting** - Not for daily work/school trips
- **Time-sensitive** - Don't use if you need to be somewhere at a specific time
- **Tight budget** - Set strict price limits or stick to planned trips

## What It Does

- Intelligently picks destinations (restaurants, bars, parks, museums, cafes)
- Books real rides with Uber, Lyft, Grab, or Ola (region-dependent)
- Learns your preferences over time
- Filters by distance, price, and destination type
- Controlled randomness - respects your budget and distance limits
- Falls back to mock mode if no credentials (safe testing)

## Quick Start

Via Telegram:

```
/randomride
/randomride $20 5km
/randomride restaurant
/randomride bar 3km
```

Via CLI:

```bash
cd ~/.openpaw/skills/randomride
python3 cli.py ride 20 5 restaurant
```

## Setup (First Run)

The skill auto-detects missing credentials and shows setup instructions:

```bash
# Create secure directory
mkdir -p ~/.openpaw/secrets
chmod 700 ~/.openpaw/secrets

# Add your Uber credentials
cat > ~/.openpaw/secrets/.uber_credentials.json << 'EOF'
{
  "client_id": "your_uber_client_id",
  "server_token": "your_uber_server_token"
}
EOF

# Secure the file
chmod 600 ~/.openpaw/secrets/.uber_credentials.json
```

**Get Uber API credentials:** https://developer.uber.com

**For CloudPaw (Render):** Use `/opt/render/.openpaw/secrets/.uber_credentials.json`

## Commands

### Telegram

- `/randomride` - Random ride (defaults: $40, 15km)
- `/randomride $20 5km` - Max $20, within 5km
- `/randomride restaurant` - Random restaurant
- `/randomride bar 3km` - Random bar within 3km
- `/randomride config distance 10km` - Set max distance
- `/randomride config price $50` - Set max price
- `/randomride history` - See past rides

### CLI

```bash
python3 cli.py ride                    # Use defaults
python3 cli.py ride 20 5 restaurant    # $20, 5km, restaurant
python3 cli.py config price 30
python3 cli.py history
```

## Regional Support

- **North America:** Uber, Lyft
- **Europe:** Uber
- **Southeast Asia:** Grab, Uber
- **India:** Ola, Uber
- **Other regions:** Mock mode (picks destination, provides booking link)

## Security

✅ **Credentials stored OUTSIDE git repo**

- LocalPaw: `~/.openpaw/secrets/.uber_credentials.json`
- CloudPaw: `/opt/render/.openpaw/secrets/.uber_credentials.json`

✅ **Protected by .gitignore**

- No credentials committed to git
- User data and history excluded

✅ **Secure permissions**

- Directory: `chmod 700`
- Files: `chmod 600`

✅ **Mock mode fallback**

- Safe testing without credentials
- No real rides booked until configured

See `SECURITY.md` for full details.

## How It Works

1. Gets your current location (manual or automatic)
2. Fetches nearby points of interest (POIs) within distance limit
3. Filters by price, type, and avoided locations
4. Picks one using weighted random selection (higher rated = more likely)
5. Books real ride with Uber/Lyft/Grab/Ola
6. Sends you destination name, ETA, and price

**Intelligent randomness:** Not purely random - weights destinations by rating and learns from your behavior over time.

## Bundled Dependencies

This skill includes all dependencies (PyJWT) - no pip install needed!

```
randomride/
├── vendor/          # Bundled PyJWT library
├── cli.py          # Command-line interface
├── random_ride.py  # Core logic
├── uber_api.py     # Uber API wrapper
└── SKILL.md        # This file
```

## Testing Without Credentials

The skill works in mock mode if credentials aren't configured:

```bash
cd ~/.openpaw/skills/randomride
python3 cli.py ride 20 5 restaurant
# Output: ⚠ Uber API not available (fallback to mock)
#         🚕 Ride booked to Casa Basso. 8 min away. $18.
```

## Status

✅ **Production ready**

- Full Uber API integration (asymmetric key auth)
- Real pricing estimates and ETAs
- Preference learning enabled
- Security hardened
- Mock mode for testing
- Auto-setup guide on first run

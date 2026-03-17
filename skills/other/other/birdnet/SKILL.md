---
name: birdnet
version: 1.0.0
description: Query BirdNET-Go bird detections. View recent birds, search by species, get detection details.
metadata: {"openclaw":{"emoji":"🐦","requires":{"bins":["curl","jq"]}}}
---

# BirdNET-Go

Query your BirdNET-Go bird sound identification system.

## Setup

Create `~/.clawdbot/credentials/birdnet/config.json`:
```json
{
  "url": "http://192.168.1.50:783"
}
```

No API key needed for local access.

## Commands

### List recent detections
```bash
bash scripts/birdnet.sh recent [limit]
```
Shows the most recent bird detections with confidence scores.

### Search detections by species
```bash
bash scripts/birdnet.sh search "Common Raven"
```
Search for detections of a specific bird species.

### Get detection details
```bash
bash scripts/birdnet.sh detection <id>
```
Get full details about a specific detection including weather data.

### Get species info
```bash
bash scripts/birdnet.sh species "Corvus corax"
```
Get information about a species including rarity score and taxonomy.

### Today's summary
```bash
bash scripts/birdnet.sh today
```
Summary of today's bird detections.

## Output Format

Recent detections show:
- Common name (Scientific name)
- Confidence score (0.0-1.0)
- Date and time
- Verification status

## API Endpoints Used

- `GET /api/v2/detections` - List detections
- `GET /api/v2/detections/:id` - Get detection details
- `GET /api/v2/species` - Get species information

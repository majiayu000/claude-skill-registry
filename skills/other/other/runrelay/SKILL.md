---
name: runrelay
description: "Search and book flights, hotels, and travel via RunRelay API. Covers 300+ airlines including low-cost carriers (Ryanair, Wizz Air, EasyJet) that no other API offers. Use when: (1) user asks about flights or hotels, (2) user wants to plan or book a trip, (3) user needs LCC coverage, (4) travel agent or concierge tasks. MCP-compatible, OpenAI-compatible."
---

# RunRelay — Travel API for AI Agents

The only travel API that covers **low-cost carriers** (Ryanair, Wizz Air, EasyJet = 33% of EU flights) alongside 300+ GDS airlines. Human-in-the-loop booking for LCCs, instant API for GDS.

## Setup

```bash
# Add to ~/.openclaw/.env
RUNRELAY_API_KEY=rr_live_your_key_here
```

Get key: https://app.runrelay.io

## Base URL

`https://api.runrelay.io`

Auth: `Authorization: Bearer $RUNRELAY_API_KEY`

## Search Flights

```bash
curl -X POST https://api.runrelay.io/api/search-flights \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RUNRELAY_API_KEY" \
  -d '{
    "origin": "DXB",
    "destination": "LHR",
    "departureDate": "2026-03-15",
    "passengers": {"adults": 1}
  }'
```

**Response:** Array of offers sorted by 30% time + 30% price + 20% airline + 15% layover.

### Tiers
- **Tier 1 (Instant):** Duffel/GDS — 300+ airlines, instant results
- **Tier 2 (HITL):** Human operators — Ryanair, Wizz Air, EasyJet. 3-8 min async. Polling via `GET /api/search-status/:id`

## Search Hotels

```bash
curl -X POST https://runrelay-hotels.fly.dev/api/search-hotels \
  -H "Content-Type: application/json" \
  -d '{
    "city": "London",
    "checkin": "2026-03-15",
    "checkout": "2026-03-20",
    "guests": 2
  }'
```

Provider: RateHawk (700K+ properties worldwide).

## Book Flight

```bash
curl -X POST https://api.runrelay.io/api/book-flight \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $RUNRELAY_API_KEY" \
  -d '{
    "offerId": "off_abc123",
    "passengers": [{
      "firstName": "John",
      "lastName": "Doe",
      "email": "john@example.com",
      "phone": "+44123456789",
      "birthDate": "1990-01-15",
      "gender": "male"
    }]
  }'
```

## Multi-Agent Trip Planning

Orchestrate parallel flight + hotel + activity searches:

```bash
curl -X POST https://prefy.com/api/v1/orchestrate \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "LHR",
    "origin": "DXB",
    "date": "2026-03-15",
    "nights": 5
  }'
```

Returns combined results from 3 parallel agents.

## MCP Server

RunRelay also works as an MCP server for Claude, Cursor, and other MCP clients:
- Endpoint: `https://api.runrelay.io`
- Protocol: MCP (Model Context Protocol)
- Tools: `search_flights`, `search_hotels`, `book_flight`, `get_booking`

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search-flights` | POST | Search flights (GDS + LCC) |
| `/api/search-status/:id` | GET | Poll HITL search status |
| `/api/flights/:id` | GET | Flight offer details |
| `/api/book-flight` | POST | Book a flight |
| `/api/bookings` | GET | List bookings |
| `/api/search-hotels` | POST | Search hotels (RateHawk) |
| `/api/v1/orchestrate` | POST | Multi-agent trip planning |

## Why RunRelay

- **Only API with LCC coverage** — Ryanair, Wizz = 33% of EU market
- **Human-in-the-loop** — real operators book what APIs can't
- **MCP native** — first travel MCP server
- **OpenAI-compatible** — drop-in for any AI agent
- **B2B ready** — white-label, API keys, usage dashboard

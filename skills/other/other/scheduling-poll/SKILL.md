---
name: scheduling-poll
description: Create a Morgen scheduling poll and pre-fill your availability. Use when "create scheduling poll", "find time to meet", "scheduling poll", "when can we meet", "poll for meeting time", or coordinating group availability.
user-invocable: false
---

# Scheduling Poll

Create a Morgen scheduling poll via Firestore REST API, pre-fill your availability, and return the shareable link. No browser required.

## Inputs

Parse from the user's natural language request:

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| Title | NO | "Scheduling Poll" | Poll title |
| Dates | YES | — | Specific dates (e.g., "Mar 16 and 17") |
| Availability | NO | — | Your free times per day (e.g., "10am-12pm Mon, 10am-4pm Tue") |
| Time increment | NO | 30 | Slot duration in minutes (15, 30, or 60) |
| Time range | NO | 9:00-17:00 | Overall time range for the poll grid |
| Your name | NO | "Edwin" | Name for your availability response |

## Workflow

```
User request parsed
    |
    v
1. PARSE inputs from natural language
    |  Resolve dates to YYYY-MM-DD (use `date` for current year)
    |  Parse availability windows per day
    |
    v
2. CHECK calendar availability (optional enrichment)
    |  morgen calendar free --start YYYY-MM-DDTHH:MM:SS --end YYYY-MM-DDTHH:MM:SS
    |  (only if user didn't specify availability explicitly)
    |
    v
3. CREATE POLL via Firestore REST API
    |  POST to Firestore → get document ID
    |
    v
4. SUBMIT YOUR AVAILABILITY (if availability provided)
    |  PATCH to Firestore → add response with time slots
    |
    v
5. RETURN the poll URL to user
    |  https://www.morgen.so/scheduling-poll?id={POLL_ID}
```

## API Details

### Constants

```
APIKEY = "${GOOGLE_API_KEY}"
PROJECT = "morgen-scheduling-poll"
BASE_URL = "https://firestore.googleapis.com/v1/projects/morgen-scheduling-poll/databases/(default)/documents/polls"
```

### Step 3: Create Poll

```bash
POLL_ID=$(curl -s -X POST \
  "${BASE_URL}?key=${APIKEY}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "title": {"stringValue": "TITLE_HERE"},
      "dates": {"arrayValue": {"values": [{"stringValue": "YYYY-MM-DD"}, ...]}},
      "timeRange": {"mapValue": {"fields": {"start": {"stringValue": "HH:MM"}, "end": {"stringValue": "HH:MM"}}}},
      "timeIncrement": {"integerValue": "30"},
      "timezone": {"stringValue": "America/New_York"},
      "daysOnly": {"booleanValue": false},
      "genericDays": {"booleanValue": false},
      "responses": {"mapValue": {"fields": {}}},
      "createdAt": {"timestampValue": "CURRENT_UTC_ISO"}
    }
  }' | python3 -c "import json,sys; name=json.load(sys.stdin)['name']; print(name.split('/')[-1])")

echo "Poll URL: https://www.morgen.so/scheduling-poll?id=${POLL_ID}"
```

### Step 4: Submit Availability

Availability slots are **ISO 8601 UTC timestamps** at `timeIncrement` intervals.

**Time conversion:** Local time → UTC. For America/New_York:
- EST (Nov-Mar before DST): UTC-5 → add 5 hours
- EDT (Mar DST start - Nov): UTC-4 → add 4 hours
- Use `date` to determine current offset

**Slot generation example:** For "10am-12pm" with 30-min increment:
→ slots at 10:00, 10:30, 11:00, 11:30 (end time is exclusive)

```bash
RESP_ID="resp_$(date +%s)"

curl -s -X PATCH \
  "${BASE_URL}/${POLL_ID}?key=${APIKEY}&updateMask.fieldPaths=responses.${RESP_ID}" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "responses": {
        "mapValue": {
          "fields": {
            "RESP_ID": {
              "mapValue": {
                "fields": {
                  "name": {"stringValue": "Edwin"},
                  "availability": {
                    "arrayValue": {
                      "values": [
                        {"stringValue": "YYYY-MM-DDTHH:MM:SS.000Z"},
                        ...
                      ]
                    }
                  },
                  "ifNeeded": {"arrayValue": {"values": []}},
                  "updatedAt": {"timestampValue": "CURRENT_UTC_ISO"}
                }
              }
            }
          }
        }
      }
    }
  }'
```

### Availability Slot Format

Each slot is an ISO UTC timestamp string: `"2026-03-16T14:00:00.000Z"`

To generate slots from local availability:

```python
# Example: Mon Mar 16, 10am-12pm ET (EDT, UTC-4)
# 10:00 AM EDT = 14:00 UTC
# Slots: 14:00, 14:30, 15:00, 15:30 (end exclusive)
```

**Pattern:** For each availability window `[start_local, end_local)` on date `YYYY-MM-DD`:
1. Convert start/end to UTC hours
2. Generate slots at `timeIncrement` intervals from start (inclusive) to end (exclusive)
3. Format as `YYYY-MM-DDTHH:MM:SS.000Z`

## Iron Law: Use `date` for UTC Offset

**NEVER hardcode UTC offset.** Always determine it dynamically:

```bash
# Get current UTC offset for America/New_York
TZ=America/New_York date +%z  # Returns -0400 (EDT) or -0500 (EST)
```

Or for a specific date:

```bash
TZ=America/New_York date -j -f "%Y-%m-%d %H:%M" "2026-03-16 10:00" +%z
```

## Iron Law: Verify Poll Creation

After the POST, verify the response contains a document `name` field. Extract the poll ID (last path segment) and construct the URL.

## Example

User: "scheduling poll mar 16 and 17, I'm free 10am-12pm Mon and 10am-4pm Tue"

**Parsed:**
- Title: "Scheduling Poll"
- Dates: 2026-03-16 (Mon), 2026-03-17 (Tue)
- Availability:
  - Mon 3/16: 10:00 AM - 12:00 PM ET
  - Tue 3/17: 10:00 AM - 4:00 PM ET
- Time range: 09:00-17:00 (covers all slots)
- Increment: 30 min

**Generated UTC slots:**
Mon (EDT, UTC-4): 14:00, 14:30, 15:00, 15:30
Tue (EDT, UTC-4): 14:00, 14:30, 15:00, 15:30, 16:00, 16:30, 17:00, 17:30, 18:00, 18:30, 19:00, 19:30

**Output:**
```
Poll created: https://www.morgen.so/scheduling-poll?id=XXXXX
Your availability (Edwin) has been submitted:
  Mon 3/16: 10:00 AM - 12:00 PM
  Tue 3/17: 10:00 AM - 4:00 PM
Share this link with participants!
```

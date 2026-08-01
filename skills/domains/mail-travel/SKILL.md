---
name: mail-travel
description: >-
  Find flight bookings, hotel reservations, travel itineraries, and booking confirmations from email. Use when user asks about upcoming trips, travel plans, booking references, flight details, or hotel reservations. Arguments: optional destination, airline, date range, or booking service.
disable-model-invocation: false
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Mail Travel — Bookings, Flights, and Itineraries

Search: **$ARGUMENTS** (default: recent and upcoming travel)

## Step 1: Find travel-related emails
```bash
DB="$HOME/Library/Mail/V10/MailData/Envelope Index"

sqlite3 "$DB" "
SELECT datetime(m.date_received,'unixepoch','localtime') as dt,
       s.subject, a.address as sender, a.comment as name,
       mb.url, m.ROWID
FROM messages m
JOIN subjects  s  ON m.subject = s.ROWID
JOIN addresses a  ON m.sender  = a.ROWID
JOIN mailboxes mb ON m.mailbox = mb.ROWID
WHERE m.deleted = 0
  AND mb.url NOT LIKE '%Spam%' AND mb.url NOT LIKE '%Trash%'
  AND (
    -- Travel booking senders
    a.address LIKE '%agoda%'
    OR a.address LIKE '%booking.com%'
    OR a.address LIKE '%airbnb%'
    OR a.address LIKE '%travelio%'
    OR a.address LIKE '%tiket%'
    OR a.address LIKE '%traveloka%'
    OR a.address LIKE '%expedia%'
    OR a.address LIKE '%hotels.com%'
    OR a.address LIKE '%airasia%'
    OR a.address LIKE '%garuda%'
    OR a.address LIKE '%lionair%'
    OR a.address LIKE '%batik%'
    OR a.address LIKE '%citilink%'
    OR a.address LIKE '%singaporeair%'
    OR a.address LIKE '%united%'
    OR a.address LIKE '%delta%'
    OR a.address LIKE '%emirates%'
    OR a.address LIKE '%gojek%'
    OR a.address LIKE '%grab%'
    -- By subject
    OR s.subject LIKE '%flight%'
    OR s.subject LIKE '%hotel%'
    OR s.subject LIKE '%booking%'
    OR s.subject LIKE '%reservation%'
    OR s.subject LIKE '%itinerary%'
    OR s.subject LIKE '%check-in%'
    OR s.subject LIKE '%boarding%'
    OR s.subject LIKE '%e-ticket%'
    OR s.subject LIKE '%confirmation%'
    OR s.subject LIKE '%your trip%'
    OR s.subject LIKE '%upcoming trip%'
    OR s.subject LIKE '%airport%'
  )
ORDER BY m.date_received DESC
LIMIT 100;" 2>/dev/null
```

## Step 2: Filter by destination/dates if specified
If $ARGUMENTS contains a destination or date, add LIKE filters on subject.

## Step 3: Parse booking details
```bash
python3 ~/.claude/skills/_mail-shared/parser.py <ROWID1> <ROWID2> ...
```

From bodies extract:
- **Flights**: origin → destination, airline, flight number, departure date/time, arrival, class, booking reference
- **Hotels**: property name, check-in/check-out dates, room type, booking ID
- **Rental/Apartment**: property ID, address, check-in time, host contact
- **Total amount paid**
- **Cancellation policy**
- **Booking reference/ID**

## Step 4: Build itinerary view
Sort by travel date (not email received date) to create a chronological itinerary.

## Output Format
Group by trip (cluster bookings by date proximity):

**Trip: [Destination] — [Date Range]**
- Flight: [route] on [date] — Ref: [booking ref]
- Hotel: [name] [check-in] to [check-out] — Ref: [ID]
- Total spent: [amount]

Also note:
- Pending check-ins (upcoming within 7 days)
- Pending refunds from cancelled trips
- Baggage allowance if mentioned

---
name: parcel-tracking
description: "Track parcels and check delivery status for Australian and international couriers. Searches Gmail for dispatch/shipping emails and provides tracking links for all major Australian couriers including AusPost, StarTrack, Aramex, CouriersPlease, Sendle, Toll, Team Global Express, DHL, FedEx, TNT, Hunter Express, Border Express, Direct Freight Express, and UPS. Triggers: 'where is my parcel', 'track my order', 'has my package arrived', 'tracking status', 'check tracking', 'where is my delivery'."
---

# Parcel Tracking

Find tracking numbers from Gmail dispatch emails and check delivery status for Australian and international couriers.

## When to Use

- "Where's my parcel / package / order?"
- "Has my [product] arrived / shipped yet?"
- "Track my order from [store]"
- "What's the status of my delivery?"
- "Do I have a tracking number for [item]?"
- User pastes or mentions a tracking number
- "Check the StarTrack / AusPost / Aramex / Toll tracking"

## Workflow

### Step 1: Find the Tracking Number

If the user already provided a tracking number, skip to Step 2.

Otherwise, search Gmail for dispatch emails. Look for recent messages matching:

```
dispatched OR shipped OR "tracking number" OR "consignment number" newer_than:30d
```

For a specific store or order, narrow the search:
```
from:mwave.com.au dispatched
from:amazon.com.au shipped
```

Read the email body and extract:
- Tracking / consignment number
- Carrier name
- Order number
- Dispatch date
- Delivery notes (signature required, etc.)

**Gmail access**: Use whatever Gmail tool is available (Gmail MCP, gws CLI `gws gmail`, or ask the user to check manually and paste the tracking number).

### Step 2: Identify the Carrier and Build the Tracking Link

Use the table below to identify the carrier from the tracking number format or dispatch email, then build the direct tracking link where possible.

| Carrier | Number format / example | Direct tracking link |
|---------|------------------------|----------------------|
| **AusPost / StarTrack** | Alphanumeric, e.g. `36VJ65064757`, `JD123456789AU` | `https://auspost.com.au/mypost/track/details/{NUMBER}` |
| **Sendle** | 6-8 alphanumeric chars, e.g. `SNFJJ3` | `https://track.sendle.com/tracking?ref={NUMBER}` |
| **DHL** | 10-12 digits, e.g. `1234567890` | `https://www.dhl.com/au-en/home/tracking.html?tracking-id={NUMBER}` |
| **FedEx** | 12-15 digits, or AU+10 digits | `https://www.fedex.com/apps/fedextrack/?tracknumbers={NUMBER}` |
| **TNT** (now FedEx) | 9 digits, e.g. `907384999` | `https://www.tnt.com/express/en_au/site/shipping-tools/tracking.html` (paste) |
| **UPS** | Starts with 1Z, 18 chars | `https://www.ups.com/track?tracknum={NUMBER}` |
| **Aramex** (formerly Fastway) | Numeric label number, varies | `https://www.aramex.com.au/tools/track` (paste) |
| **CouriersPlease** | Numeric or CP prefix | `https://www.couriersplease.com.au/tools-track` (paste) |
| **Toll / MyToll** | Numeric consignment, varies | `https://mytoll.com/` (paste) |
| **Team Global Express** | Numeric, varies | `https://myteamge.com/` (paste) |
| **Hunter Express** | Alphanumeric, e.g. `AIM478695` | `https://www.hunterexpress.com.au/tracking/` (paste) |
| **Border Express** | Numeric, varies | `https://www.borderexpress.com.au/tracking/` (paste) |
| **Direct Freight Express** | Numeric consignment | `https://www.directfreight.com.au/ConsignmentStatus.aspx` (paste) |

**Deep-links** (tracking number in URL): AusPost/StarTrack, Sendle, DHL, FedEx, UPS.

**Form-based** (provide link + number separately): Aramex, CouriersPlease, Toll, Team Global Express, Hunter Express, Border Express, Direct Freight Express, TNT.

**If carrier is unknown:** Default to AusPost (most common in Australia), or ask the user to check their dispatch email.

### Step 3: Try to Get Live Status

If web scraping tools are available, try scraping the tracking page:

```
url: {direct tracking URL}
wait_for: 3000 (many tracking pages are JS-rendered)
```

Many tracking pages return limited data when scraped. AusPost is particularly JS-heavy. If scraping returns useful status info, include it. If not, just provide the direct link. Don't mention failed scrapes to the user.

If browser automation is available (Chrome MCP, Playwright), navigate to the tracking page and read the status directly.

If no scraping/browser tools are available, skip this step and provide the link.

### Step 4: Present Results

Always include:
1. **Current status** (from scrape if available, or from dispatch email)
2. **Direct tracking link** (always)
3. **Expected delivery window** (if known)
4. **Delivery notes** (signature required, card-to-collect, etc.)

#### Example: Carrier with Deep Link

```
Order IN03069870 — Mac mini x 2
Dispatched by Mwave via AusPost/StarTrack on 17 Mar

Tracking: 36VJ65064757
Status: In transit — processed at Sydney sorting facility
Expected: Thu 19 – Fri 20 Mar
Note: Signature required. If no one home, parcel goes to local post office.

Track live: https://auspost.com.au/mypost/track/details/36VJ65064757
```

#### Example: Form-Based Carrier

```
Order 12345 — [item]
Dispatched via Toll on 15 Mar

Consignment: TXY9876543
Expected: 3-5 business days

Track at: https://mytoll.com/
Paste consignment number: TXY9876543
```

### Handling Multiple Parcels

Search broadly:
```
(dispatched OR shipped OR "on its way" OR "tracking number") newer_than:30d
```

Present each parcel as a separate block.

## Carrier Contact Numbers (Australia)

| Carrier | Phone | Hours (AEST/AEDT) |
|---------|-------|-------------------|
| AusPost / StarTrack eParcel | 13 13 18 | Mon-Fri 8am-6pm |
| StarTrack (account customers) | 13 23 45 | Business hours |
| CouriersPlease | 13 00 36 16 | Business hours |
| Toll Priority | 13 15 31 | Mon-Fri 7am-10pm, Sat-Sun 7am-5pm |
| Toll IPEC | 1300 865 547 | Business hours |
| Hunter Express | 02 9780 4099 | Business hours |
| DHL | 13 14 06 | Business hours |
| FedEx / TNT | 13 26 10 | Business hours |
| UPS | 13 26 77 | Business hours |
| Aramex | See aramex.com.au/contact-us | Business hours |
| Sendle | Online only (support form) | — |
| Team Global Express | myteamge.com contact form | — |

## Carrier-Specific Notes

**AusPost / StarTrack**
- URL format: `https://auspost.com.au/mypost/track/details/{TRACKING_NUMBER}` — tracking number goes directly in the path
- Sparse tracking events after Sydney (Lidcombe/Chullora) processing is normal for regional deliveries
- Allow up to 24 hours after dispatch for tracking to appear
- Signature-required parcels go to local post office if undelivered

**Sendle**
- Sendle halted all parcel pick-ups in early 2025 and directed customers to Aramex. Existing Sendle shipments still trackable.
- Deep link: `https://track.sendle.com/tracking?ref={SENDLE_REFERENCE}`

**Toll vs Team Global Express**
- Toll Global Express was sold and rebranded as Team Global Express — different tracking system
- Domestic Toll parcels (IPEC, Priority, Express) still use MyToll

## Tool Flexibility

This skill works with whatever tools are available:

| Tool | What it enables |
|------|----------------|
| Gmail access (any MCP or CLI) | Search dispatch emails for tracking numbers |
| Web scraper (any MCP) | Attempt live status from tracking pages |
| Browser automation (Chrome MCP, Playwright) | Navigate tracking pages for JS-rendered status |
| None of the above | User provides tracking number, skill provides the correct link |

---
name: fever-sync-specialist
description: "Sync and integrate Fever Partners API for plans, reviews, attendees, and venues. Use when implementing Fever data sync, debugging API issues, or building review/analytics features."
---

# Fever Sync Specialist

Sync and manage data from Fever Partners API including plans, reviews, attendees, and venues.

## When to Use

- Implementing Fever data sync features
- Debugging Fever API integration issues
- Building reviews or analytics features from Fever data
- Working with Fever venues, plans, or sessions

## Fever API Architecture

### Base URLs

| Service | URL | Purpose |
|---------|-----|---------|
| B2C API | `https://services.feverup.com` | Consumer-facing API |
| B2B API | `https://services.feverup.com/b2b` | Legacy B2B API |
| B2B Partners | `https://services.feverup.com/b2b-partners` | Partners API (main) |
| B2B IAM | `https://services.feverup.com/b2b-iam` | Identity/Auth |
| B2C Site | `https://services.feverup.com/b2c_site` | Site config |

### Authentication

All B2B APIs require authentication:

```
Authorization: B2bToken {token}
X-Client-Version: w.12.0.1
Accept: application/json
```

Token is obtained after login to partners.feverup.com and stored in browser.

---

## Available Endpoints

### 1. Reviews API (Reverse Engineered)

**Endpoint:**
```
GET /b2b-partners/1.0/partners/{partner_id}/reviews
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `items_per_page` | int | Reviews per page (default: 10) |
| `page` | int | Page number (1-indexed) |
| `city_id` | string | Filter by city ID |
| `place_id` | int | Filter by venue ID |
| `question_type` | string | Review type: `general-review` |
| `order_by` | string | Sort field: `answered_at` |
| `order_by_direction` | string | `desc` or `asc` |

**Response:**
```json
{
  "data": {
    "questions_rating": [
      {
        "average": "4.6",
        "id": "uuid",
        "number_of_ratings": 2044,
        "title": "How would you rate the experience overall?",
        "type": "general-review"
      }
    ],
    "reviews": [
      {
        "answers": [
          {
            "flagged": false,
            "hidden": false,
            "id": "uuid",
            "question_id": "uuid",
            "question_title": "How would you rate the experience overall?",
            "question_type": "general-review",
            "rating": 5,
            "reasoning": "Optional text review"
          }
        ],
        "city_id": "1004611",
        "city_name": "Dortmund",
        "city_timezone": "Europe/Berlin",
        "place_address": "Schützenstraße 35, Dortmund",
        "place_id": 23810,
        "plan_id": 416711,
        "plan_name": "Candlelight: Tribut an Coldplay",
        "session_name": "Zone D",
        "session_starts_at": "2025-11-28T19:30:00Z",
        "ticket_id": 100585215,
        "user_first_name": "Alexandra",
        "user_id": 82692035,
        "user_image_url": "https://...",
        "user_last_name": "Dröge"
      }
    ]
  }
}
```

---

### 2. Plans API

**Endpoint:**
```
GET /b2b-partners/2.0/partners/{partner_id}/plans
```

**Response:**
```json
{
  "data": {
    "plans": [
      {
        "id": 501864,
        "name": "Ballet of Lights: Cinderella",
        "status": "on_sale",
        "kind": "standard",
        "partner_id": 8486,
        "timezone": "Europe/Berlin",
        "image_url": "https://...",
        "is_published": true,
        "is_sold_out": false,
        "is_hidden_feed": false,
        "is_asset_based": false,
        "has_multiple_places": false,
        "first_session_date": "2026-02-28T14:30:00Z",
        "last_session_date": "2026-04-09T18:30:00Z",
        "next_session_date": "2026-02-28T14:30:00Z",
        "next_session_date_with_attendees": "2026-02-28T14:30:00Z",
        "last_expired_session_date": null,
        "last_expired_session_date_with_attendees": null,
        "first_place_address": "Bautzner Landstraße 7, Dresden",
        "first_place_city_name": "Dresden",
        "created_at": "2025-11-11T17:27:57.705000Z",
        "places": [
          {
            "id": 25788,
            "name": "Parkhotel Dresden",
            "address": "Bautzner Landstraße 7, Dresden",
            "zip_code": "01324",
            "city": {
              "id": 1004916,
              "name": "Dresden",
              "currency": "EUR",
              "timezone": "Europe/Berlin"
            }
          }
        ]
      }
    ]
  }
}
```

---

### 3. Survey Replies API

**Endpoint:**
```
GET /b2b-partners/1.0/partners/{partner_id}/survey-replies
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `only_last_reply` | bool | Return only latest reply |

**Response:**
```json
{
  "data": [
    {
      "id": "uuid",
      "external_id": "0896d458bc004d12",
      "partner_id": 8486,
      "user_id": 42001,
      "reply_at": "2024-12-30T19:03:15.319869Z",
      "next_scheduled_reply_at": "2025-03-30T19:03:15.319869Z"
    }
  ]
}
```

---

### 4. User Info API

**Endpoint:**
```
GET /b2b-iam/1.0/users/me
```

**Response:**
```json
{
  "data": {
    "id": 52740,
    "email": "user@example.com",
    "name": "User Name",
    "username": "user@example.com",
    "language": "de_DE",
    "status": "active",
    "type": "regular",
    "interface": "staff",
    "source": "feverzone",
    "business": null,
    "kiosk": null
  }
}
```

---

### 5. User Permissions API

**Endpoint:**
```
GET /b2b-iam/1.0/users/{user_id}/organizations/{org_id}/permissions
```

**Response:**
```json
{
  "data": {
    "permissions": [
      "can_search_cities",
      "can_search_plans",
      "can_view_attendees",
      "can_view_partner_detail",
      "can_view_reviews",
      "can_view_survey_replies",
      "can_view_validation"
    ]
  }
}
```

---

### 6. Other Known Endpoints (from bundle analysis)

| Endpoint | Description |
|----------|-------------|
| `GET /1.0/partners/{id}/cities` | List cities |
| `GET /1.0/partners/{id}/places` | List venues |
| `GET /1.0/partners/{id}/plans-with-analytics` | Plans with analytics data |
| `GET /1.0/partners/{id}/booking-agents` | Booking agents |
| `GET /1.0/partners/{id}/resellers` | Resellers |
| `GET /1.0/partners/{id}/users` | Partner users |
| `GET /1.0/partners/{id}/kiosks` | Kiosks |
| `GET /1.0/partners/{id}/onsite-setups` | On-site setups |
| `GET /1.0/partners/{id}/cash-registers` | Cash registers |
| `GET /1.0/partners/{id}/template-coupons` | Coupon templates |

---

## Public B2C API (No Auth Required)

### Plan Details with Rating

```
GET https://feverup.com/api/4.4/plans/{plan_id}/
```

**Response includes:**
```json
{
  "id": 266311,
  "name": "The Jury Experience",
  "rating": {
    "is_hidden": false,
    "num_ratings": 254,
    "average": 4.35
  },
  "should_display_featured_review_answers": true
}
```

**Note:** Individual reviews are NOT available via public API. They are server-side rendered into the HTML at `feverup.com/m/{plan_id}` for SEO purposes.

---

## Test Scripts

Located in `.claude/skills/fever-sync-specialist/scripts/`:

### Test Reviews API (B2B - Auth Required)
```bash
./.claude/skills/fever-sync-specialist/scripts/test-fever-reviews.sh [city_id] [place_id] [page] [items_per_page]

# Requires:
export FEVER_PARTNER_ID="8486"
export FEVER_B2B_TOKEN="your-token"

# Get token from browser DevTools after logging into partners.feverup.com
```

### Test Public Rating API (B2C - No Auth)
```bash
./.claude/skills/fever-sync-specialist/scripts/test-fever-b2c-reviews.sh
```

### Token Retrieval
1. Log into https://partners.feverup.com
2. Open DevTools → Network tab
3. Find any request to `services.feverup.com`
4. Copy the `Authorization` header value (without "B2bToken " prefix)

---

## Data Mapping for Ballee

### Reviews → Ballee Events
| Fever Field | Ballee Field | Notes |
|-------------|--------------|-------|
| `plan_id` | `fever_plan_id` | Link to event |
| `place_id` | `fever_venue_id` | Link to venue |
| `rating` | `rating` | 1-5 scale |
| `reasoning` | `review_text` | Optional text |
| `session_starts_at` | `session_date` | Session datetime |
| `user_first_name` | `reviewer_name` | Partial name |

### Plans → Ballee Events
| Fever Field | Ballee Field |
|-------------|--------------|
| `id` | `fever_plan_id` |
| `name` | `name` |
| `status` | `status` |
| `first_session_date` | `start_date` |
| `last_session_date` | `end_date` |
| `places[].id` | `fever_venue_id` |
| `places[].city.id` | `fever_city_id` |

---

## Ballee Sync Implementation

### Key Files

| File | Purpose |
|------|---------|
| `apps/web/app/admin/sync/_lib/server/fever-api.client.ts` | API client with auth, pagination |
| `apps/web/app/admin/sync/_lib/server/fever-reviews-sync.service.ts` | Main sync service |
| `apps/web/app/admin/sync/_lib/server/fever-venue-mapping.service.ts` | Venue mapping management |
| `apps/web/app/admin/sync/_lib/server/fever-reviews-sync-actions.ts` | Server actions |
| `apps/web/app/api/cron/fever-sync/route.ts` | Hourly cron endpoint |

### Database Tables

| Table | Purpose |
|-------|---------|
| `fever_sync_configs` | API credentials, partner IDs, last sync status |
| `fever_reviews` | Individual reviews with ticket_id dedup |
| `fever_venue_mappings` | Fever place_id → Ballee venue_id mapping |
| `events.fever_plan_id` | Link events to Fever plans |
| `events.fever_average_rating` | Cached aggregate rating |

### Sync Modes

```typescript
// Full sync - fetches all reviews
await syncFeverReviewsAction({ incremental: false });

// Incremental sync - only new reviews since last_sync_at
await syncFeverReviewsAction({ incremental: true });
```

### Cron Configuration

`vercel.json`:
```json
{
  "crons": [{
    "path": "/api/cron/fever-sync",
    "schedule": "0 * * * *"
  }]
}
```

- Default: Incremental sync (hourly)
- Force full: `?full=true` query parameter

### Matching Algorithm

Reviews are linked to events via exact matching (no fuzzy matching):

```sql
UPDATE fever_reviews fr
SET event_id = e.id
FROM events e
WHERE e.fever_plan_id = fr.fever_plan_id
  AND DATE(e.event_date) = DATE(fr.session_starts_at AT TIME ZONE e.timezone);
```

---

## Troubleshooting

### 401 Unauthorized
- Token expired - get new token from browser DevTools
- Wrong partner ID

### Empty Reviews
- Check `can_view_reviews` permission
- Try without city/place filters first
- Verify partner has reviews

### Rate Limiting
- Fever may rate limit aggressive polling
- Implement exponential backoff
- Cache responses appropriately

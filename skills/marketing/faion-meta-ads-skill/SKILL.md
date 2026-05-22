---
name: faion-meta-ads-skill
user-invocable: false
description: ""
---

# Meta Ads API Mastery

**Complete guide to Meta Marketing API for Facebook & Instagram advertising (2025-2026)**

---

## Quick Reference

| Area | Key Elements |
|------|--------------|
| **Authentication** | Access tokens, App permissions, System users, Token refresh |
| **Campaign Structure** | Business Account > Ad Account > Campaign > Ad Set > Ad > Creative |
| **Targeting** | Demographics, Interests, Custom Audiences, Lookalikes |
| **Budget** | Daily/lifetime budgets, CBO, bid strategies |
| **Reporting** | Insights API, breakdowns, date ranges, async reports |
| **Conversion** | Pixel, CAPI, offline events, attribution |

---

## API Overview

### Base URL

```
https://graph.facebook.com/v20.0/
```

### Object Hierarchy

```
Business Account (business_id)
└── Ad Account (act_123456789)
    └── Campaign (campaign_id)
        └── Ad Set (adset_id)
            └── Ad (ad_id)
                └── Creative (creative_id)
                    └── Media (image/video)
```

### API Versions

| Version | Release | Support Until |
|---------|---------|---------------|
| v20.0 | May 2024 | May 2027 |
| v19.0 | Jan 2024 | Jan 2027 |
| v18.0 | Sep 2023 | Sep 2026 |

**Rule:** Always use explicit versioning. Migrate before deprecation.

---

## Authentication

### Access Token Types

| Type | Duration | Use Case |
|------|----------|----------|
| **User Token** | Short-lived (1-2 hours) | Interactive apps |
| **Long-lived User** | ~60 days | Server apps, extended access |
| **Page Token** | Never expires | Page management |
| **System User Token** | Never expires | Automated systems, APIs |

### Getting Access Tokens

**1. User Token (OAuth Flow):**
```
https://www.facebook.com/v20.0/dialog/oauth?
  client_id={app-id}&
  redirect_uri={redirect-uri}&
  scope=ads_management,ads_read,business_management
```

**2. Exchange for Long-lived:**
```bash
curl -X GET "https://graph.facebook.com/v20.0/oauth/access_token?\
grant_type=fb_exchange_token&\
client_id={app-id}&\
client_secret={app-secret}&\
fb_exchange_token={short-lived-token}"
```

**3. System User Token (Recommended for automation):**
```
Business Manager → System Users → Generate New Token
→ Select app → Select permissions → Generate
```

### Required Permissions

| Permission | Purpose |
|------------|---------|
| `ads_management` | Create, edit, manage ads |
| `ads_read` | Read ad performance data |
| `business_management` | Manage business assets |
| `pages_read_engagement` | Read page metrics |
| `leads_retrieval` | Access lead form data |

### Token Validation

```bash
curl -X GET "https://graph.facebook.com/debug_token?\
input_token={token-to-check}&\
access_token={app-id}|{app-secret}"
```

**Response:**
```json
{
  "data": {
    "app_id": "123456789",
    "is_valid": true,
    "scopes": ["ads_management", "ads_read"],
    "expires_at": 1735689600
  }
}
```

---

## Campaign Management

### Campaign Objectives (v20.0+)

| Objective | Code | Use Case |
|-----------|------|----------|
| **Awareness** | `OUTCOME_AWARENESS` | Brand reach, video views |
| **Traffic** | `OUTCOME_TRAFFIC` | Website visits |
| **Engagement** | `OUTCOME_ENGAGEMENT` | Post engagement, page likes |
| **Leads** | `OUTCOME_LEADS` | Lead forms, instant forms |
| **App Promotion** | `OUTCOME_APP_PROMOTION` | App installs |
| **Sales** | `OUTCOME_SALES` | Conversions, catalog sales |

### Create Campaign

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/campaigns" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Summer Sale 2026",
    "objective": "OUTCOME_SALES",
    "status": "PAUSED",
    "special_ad_categories": [],
    "buying_type": "AUCTION"
  }'
```

**Response:**
```json
{
  "id": "23849857358"
}
```

### Campaign Budget Optimization (CBO)

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/campaigns" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "CBO Campaign",
    "objective": "OUTCOME_SALES",
    "status": "PAUSED",
    "daily_budget": 10000,
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP"
  }'
```

**Note:** Budget is in cents (10000 = $100.00)

### Update Campaign

```bash
curl -X POST "https://graph.facebook.com/v20.0/{campaign-id}" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Updated Campaign Name",
    "status": "ACTIVE"
  }'
```

### Campaign Status Values

| Status | Meaning |
|--------|---------|
| `ACTIVE` | Running and delivering |
| `PAUSED` | Manually paused |
| `DELETED` | Soft-deleted (recoverable) |
| `ARCHIVED` | Completed, read-only |

---

## Ad Set Management

### Create Ad Set

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adsets" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "US 25-54 Lookalike",
    "campaign_id": "{campaign-id}",
    "billing_event": "IMPRESSIONS",
    "optimization_goal": "OFFSITE_CONVERSIONS",
    "daily_budget": 5000,
    "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    "status": "PAUSED",
    "targeting": {
      "geo_locations": {
        "countries": ["US"]
      },
      "age_min": 25,
      "age_max": 54,
      "genders": [1, 2],
      "publisher_platforms": ["facebook", "instagram"],
      "facebook_positions": ["feed", "right_hand_column"],
      "instagram_positions": ["stream", "story", "explore"]
    },
    "start_time": "2026-01-20T00:00:00-0800",
    "end_time": "2026-02-20T23:59:59-0800",
    "promoted_object": {
      "pixel_id": "{pixel-id}",
      "custom_event_type": "PURCHASE"
    }
  }'
```

### Bid Strategies

| Strategy | Code | Description |
|----------|------|-------------|
| **Lowest Cost** | `LOWEST_COST_WITHOUT_CAP` | Maximize results within budget |
| **Cost Cap** | `COST_CAP` | Control cost per result |
| **Bid Cap** | `LOWEST_COST_WITH_BID_CAP` | Maximum bid per auction |
| **ROAS** | `LOWEST_COST_WITH_MIN_ROAS` | Minimum return on ad spend |

### Optimization Goals

| Goal | Code | Best For |
|------|------|----------|
| Conversions | `OFFSITE_CONVERSIONS` | Website sales/leads |
| Link Clicks | `LINK_CLICKS` | Traffic campaigns |
| Impressions | `IMPRESSIONS` | Reach/awareness |
| Landing Page Views | `LANDING_PAGE_VIEWS` | Quality traffic |
| Lead Generation | `LEAD_GENERATION` | Lead forms |
| App Installs | `APP_INSTALLS` | Mobile apps |

### Placement Options

```json
{
  "targeting": {
    "publisher_platforms": ["facebook", "instagram", "audience_network", "messenger"],
    "facebook_positions": [
      "feed",
      "right_hand_column",
      "instant_article",
      "marketplace",
      "video_feeds",
      "story",
      "search",
      "instream_video",
      "facebook_reels"
    ],
    "instagram_positions": [
      "stream",
      "story",
      "explore",
      "reels",
      "search"
    ],
    "messenger_positions": [
      "messenger_home",
      "sponsored_messages",
      "story"
    ],
    "audience_network_positions": [
      "classic",
      "rewarded_video"
    ]
  }
}
```

---

## Audience Targeting

### Demographics

```json
{
  "targeting": {
    "geo_locations": {
      "countries": ["US", "CA", "GB"],
      "regions": [{"key": "4081"}],
      "cities": [{"key": "2421836", "radius": 25, "distance_unit": "mile"}],
      "zips": [{"key": "US:90210"}]
    },
    "age_min": 25,
    "age_max": 54,
    "genders": [1, 2],
    "locales": [6, 24],
    "user_os": ["iOS", "Android"]
  }
}
```

**Gender Codes:** 1 = Male, 2 = Female

### Interest Targeting

```json
{
  "targeting": {
    "interests": [
      {"id": "6003139266461", "name": "Entrepreneurship"},
      {"id": "6003107902433", "name": "Small business"}
    ],
    "behaviors": [
      {"id": "6002714895372", "name": "Engaged Shoppers"}
    ]
  }
}
```

**Find Interest IDs:**
```bash
curl -X GET "https://graph.facebook.com/v20.0/search?\
type=adinterest&\
q=entrepreneurship&\
access_token={token}"
```

### Custom Audiences

**Create from Customer List:**
```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Email Subscribers 2026",
    "subtype": "CUSTOM",
    "description": "Newsletter subscribers",
    "customer_file_source": "USER_PROVIDED_ONLY"
  }'
```

**Add Users:**
```bash
curl -X POST "https://graph.facebook.com/v20.0/{audience-id}/users" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "payload": {
      "schema": ["EMAIL", "FN", "LN"],
      "data": [
        ["hash(email1@example.com)", "hash(john)", "hash(doe)"],
        ["hash(email2@example.com)", "hash(jane)", "hash(smith)"]
      ]
    }
  }'
```

**Note:** All PII must be SHA256 hashed before upload.

### Website Custom Audiences

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Website Visitors 30 Days",
    "subtype": "WEBSITE",
    "rule": {
      "inclusions": {
        "operator": "or",
        "rules": [
          {
            "event_sources": [{"id": "{pixel-id}", "type": "pixel"}],
            "retention_seconds": 2592000,
            "filter": {
              "operator": "and",
              "filters": [
                {"field": "url", "operator": "i_contains", "value": "/products"}
              ]
            }
          }
        ]
      }
    }
  }'
```

### Lookalike Audiences

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/customaudiences" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Lookalike US 1%",
    "subtype": "LOOKALIKE",
    "origin_audience_id": "{source-audience-id}",
    "lookalike_spec": {
      "type": "similarity",
      "country": "US",
      "ratio": 0.01
    }
  }'
```

**Lookalike Sizes:** 1-10% (1% = most similar, 10% = broader reach)

### Exclusion Targeting

```json
{
  "targeting": {
    "exclusions": {
      "custom_audiences": [
        {"id": "{existing-customer-audience-id}"}
      ]
    },
    "excluded_connections": [
      {"id": "{page-id}"}
    ]
  }
}
```

---

## Ad Creative

### Create Image Ad

```bash
# 1. Upload image
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adimages" \
  -H "Authorization: Bearer {access-token}" \
  -F "filename=@image.jpg"

# Response: {"images": {"image.jpg": {"hash": "abc123..."}}}

# 2. Create creative
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adcreatives" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Summer Sale Creative",
    "object_story_spec": {
      "page_id": "{page-id}",
      "link_data": {
        "image_hash": "abc123...",
        "link": "https://example.com/sale",
        "message": "Shop our biggest sale of the year!",
        "name": "Summer Sale - Up to 50% Off",
        "description": "Limited time offer on all products",
        "call_to_action": {
          "type": "SHOP_NOW",
          "value": {
            "link": "https://example.com/sale"
          }
        }
      }
    }
  }'
```

### Create Video Ad

```bash
# 1. Upload video (async)
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/advideos" \
  -H "Authorization: Bearer {access-token}" \
  -F "source=@video.mp4" \
  -F "title=Product Demo"

# 2. Check upload status
curl -X GET "https://graph.facebook.com/v20.0/{video-id}?fields=status"

# 3. Create creative (after status = ready)
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adcreatives" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Video Ad Creative",
    "object_story_spec": {
      "page_id": "{page-id}",
      "video_data": {
        "video_id": "{video-id}",
        "title": "Product Demo",
        "message": "See our product in action!",
        "call_to_action": {
          "type": "LEARN_MORE",
          "value": {"link": "https://example.com"}
        }
      }
    }
  }'
```

### Call to Action Types

| Type | Best For |
|------|----------|
| `SHOP_NOW` | E-commerce |
| `LEARN_MORE` | Information |
| `SIGN_UP` | Lead generation |
| `BOOK_NOW` | Appointments |
| `DOWNLOAD` | Apps |
| `GET_OFFER` | Promotions |
| `GET_QUOTE` | Services |
| `CONTACT_US` | Direct contact |
| `SUBSCRIBE` | Newsletters |
| `APPLY_NOW` | Applications |

### Image Specifications

| Placement | Recommended Size | Ratio |
|-----------|------------------|-------|
| Feed | 1080x1080px | 1:1 |
| Stories | 1080x1920px | 9:16 |
| Right Column | 1200x628px | 1.91:1 |
| Carousel | 1080x1080px | 1:1 |

### Video Specifications

| Spec | Requirement |
|------|-------------|
| Format | MP4, MOV |
| Max size | 4GB |
| Max length | 240 min (Feed), 15s (Stories) |
| Min resolution | 720p |
| Aspect ratio | 1:1, 4:5, 9:16, 16:9 |

---

## Ad Creation

### Create Ad

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/ads" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Summer Sale Ad v1",
    "adset_id": "{adset-id}",
    "creative": {"creative_id": "{creative-id}"},
    "status": "PAUSED",
    "tracking_specs": [
      {
        "action.type": ["offsite_conversion"],
        "fb_pixel": ["{pixel-id}"]
      }
    ]
  }'
```

### Dynamic Creative

```bash
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/adsets" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Dynamic Creative Ad Set",
    "campaign_id": "{campaign-id}",
    "optimization_goal": "OFFSITE_CONVERSIONS",
    "billing_event": "IMPRESSIONS",
    "daily_budget": 5000,
    "status": "PAUSED",
    "targeting": {...},
    "is_dynamic_creative": true
  }'

# Create ad with asset feed
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/ads" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "name": "Dynamic Creative Ad",
    "adset_id": "{adset-id}",
    "status": "PAUSED",
    "creative": {
      "creative_id": "{creative-id}"
    },
    "asset_feed_spec": {
      "images": [
        {"hash": "hash1"},
        {"hash": "hash2"},
        {"hash": "hash3"}
      ],
      "titles": [
        {"text": "Title Option 1"},
        {"text": "Title Option 2"}
      ],
      "bodies": [
        {"text": "Body text option 1"},
        {"text": "Body text option 2"}
      ],
      "call_to_action_types": ["SHOP_NOW", "LEARN_MORE"]
    }
  }'
```

---

## Conversion Tracking

### Meta Pixel Setup

```html
<!-- Base Pixel Code -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', '{pixel-id}');
fbq('track', 'PageView');
</script>
```

### Standard Events

| Event | Parameters |
|-------|------------|
| `ViewContent` | content_ids, content_type, value, currency |
| `AddToCart` | content_ids, content_type, value, currency |
| `InitiateCheckout` | content_ids, value, currency, num_items |
| `AddPaymentInfo` | content_ids, value, currency |
| `Purchase` | content_ids, content_type, value, currency, num_items |
| `Lead` | content_name, value, currency |
| `CompleteRegistration` | status, value, currency |
| `Search` | search_string, content_ids |

### Track Events

```javascript
// Standard event
fbq('track', 'Purchase', {
  content_ids: ['SKU123'],
  content_type: 'product',
  value: 99.99,
  currency: 'USD',
  num_items: 1
});

// Custom event
fbq('trackCustom', 'PromoCodeUsed', {
  promo_code: 'SUMMER2026',
  discount_amount: 15.00
});
```

### Conversions API (Server-Side)

```bash
curl -X POST "https://graph.facebook.com/v20.0/{pixel-id}/events" \
  -H "Authorization: Bearer {access-token}" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {
        "event_name": "Purchase",
        "event_time": 1735689600,
        "action_source": "website",
        "event_source_url": "https://example.com/checkout/complete",
        "user_data": {
          "em": ["hash(email)"],
          "ph": ["hash(phone)"],
          "client_ip_address": "123.45.67.89",
          "client_user_agent": "Mozilla/5.0...",
          "fbc": "_fbc cookie value",
          "fbp": "_fbp cookie value"
        },
        "custom_data": {
          "currency": "USD",
          "value": 99.99,
          "content_ids": ["SKU123"],
          "content_type": "product",
          "num_items": 1
        }
      }
    ]
  }'
```

### Event Deduplication

```javascript
// Browser (Pixel)
fbq('track', 'Purchase', {
  value: 99.99,
  currency: 'USD'
}, {eventID: 'order_12345'});

// Server (CAPI)
{
  "event_name": "Purchase",
  "event_id": "order_12345",
  ...
}
```

**Rule:** Use same `event_id` for Pixel and CAPI to prevent double-counting.

---

## Reporting & Insights

### Get Campaign Insights

```bash
curl -X GET "https://graph.facebook.com/v20.0/{campaign-id}/insights?\
fields=spend,impressions,clicks,cpc,cpm,ctr,reach,frequency,\
actions,cost_per_action_type,conversions,conversion_values&\
date_preset=last_7d&\
access_token={token}"
```

### Date Presets

| Preset | Period |
|--------|--------|
| `today` | Current day |
| `yesterday` | Previous day |
| `this_week_sun_today` | Sunday to today |
| `last_7d` | Last 7 days |
| `last_14d` | Last 14 days |
| `last_30d` | Last 30 days |
| `last_90d` | Last 90 days |
| `this_month` | Current month |
| `last_month` | Previous month |
| `lifetime` | All time |

### Custom Date Range

```bash
curl -X GET "https://graph.facebook.com/v20.0/{campaign-id}/insights?\
fields=spend,impressions,actions&\
time_range={'since':'2026-01-01','until':'2026-01-31'}&\
access_token={token}"
```

### Breakdowns

```bash
# By age and gender
curl -X GET "https://graph.facebook.com/v20.0/{campaign-id}/insights?\
fields=spend,impressions,actions&\
breakdowns=age,gender&\
date_preset=last_7d&\
access_token={token}"

# By placement
curl -X GET "https://graph.facebook.com/v20.0/{campaign-id}/insights?\
fields=spend,impressions,actions&\
breakdowns=publisher_platform,platform_position&\
date_preset=last_7d&\
access_token={token}"

# By device
curl -X GET "https://graph.facebook.com/v20.0/{campaign-id}/insights?\
fields=spend,impressions,actions&\
breakdowns=device_platform&\
date_preset=last_7d&\
access_token={token}"
```

### Available Breakdowns

| Breakdown | Description |
|-----------|-------------|
| `age` | Age ranges |
| `gender` | Male, Female, Unknown |
| `country` | Country codes |
| `region` | State/province |
| `dma` | Designated market area |
| `publisher_platform` | Facebook, Instagram, etc. |
| `platform_position` | Feed, Stories, etc. |
| `device_platform` | Mobile, Desktop |
| `impression_device` | iOS, Android, Desktop |
| `product_id` | Catalog products |
| `hourly_stats_aggregated_by_advertiser_time_zone` | By hour |

### Action Types

| Action | Description |
|--------|-------------|
| `link_click` | Clicks on links |
| `post_engagement` | Total engagement |
| `purchase` | Purchase conversions |
| `lead` | Lead conversions |
| `add_to_cart` | Add to cart events |
| `initiate_checkout` | Checkout initiations |
| `page_engagement` | Page interactions |
| `video_view` | Video views |
| `landing_page_view` | Landing page loads |
| `omni_purchase` | Cross-platform purchases |

### Async Reports (Large Data)

```bash
# 1. Create report
curl -X POST "https://graph.facebook.com/v20.0/act_{ad-account-id}/insights" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "level": "ad",
    "fields": ["spend", "impressions", "clicks", "actions"],
    "date_preset": "last_90d",
    "breakdowns": ["age", "gender"]
  }'

# Response: {"report_run_id": "123456789"}

# 2. Check status
curl -X GET "https://graph.facebook.com/v20.0/{report-run-id}?\
fields=async_status,async_percent_completion&\
access_token={token}"

# 3. Get results (when complete)
curl -X GET "https://graph.facebook.com/v20.0/{report-run-id}/insights?\
access_token={token}"
```

---

## Budget Optimization

### Daily vs Lifetime Budget

```json
// Daily budget - consistent spend
{
  "daily_budget": 5000,
  "billing_event": "IMPRESSIONS"
}

// Lifetime budget - flexible pacing
{
  "lifetime_budget": 100000,
  "start_time": "2026-01-20T00:00:00-0800",
  "end_time": "2026-02-20T23:59:59-0800",
  "pacing_type": ["standard"]
}
```

### Budget Recommendations

```bash
curl -X GET "https://graph.facebook.com/v20.0/act_{ad-account-id}/delivery_estimate?\
targeting_spec={targeting-json}&\
optimization_goal=OFFSITE_CONVERSIONS&\
access_token={token}"
```

### Scaling Strategies

| Method | Approach | Best For |
|--------|----------|----------|
| **Vertical** | Increase budget 20-30% every 3-4 days | Proven ad sets |
| **Horizontal** | Duplicate to new audiences | Expand reach |
| **CBO** | Campaign-level optimization | Multiple ad sets |

### Bid Caps

```json
{
  "bid_strategy": "COST_CAP",
  "bid_amount": 1500
}
```

**Note:** Bid amount in cents (1500 = $15.00)

---

## Best Practices

### Rate Limiting

| Limit Type | Rate | Handling |
|------------|------|----------|
| Marketing API | Varies by tier | Implement exponential backoff |
| Ad Account | ~200 calls/hour | Batch requests |
| Insights | Async for large data | Use report runs |

**Headers to Check:**
```
x-business-use-case-usage
x-app-usage
x-ad-account-usage
```

### Error Handling

```json
{
  "error": {
    "message": "Error message",
    "type": "OAuthException",
    "code": 190,
    "error_subcode": 460,
    "fbtrace_id": "ABC123"
  }
}
```

| Code | Meaning | Action |
|------|---------|--------|
| 1 | API Unknown | Retry |
| 2 | API Service | Retry with backoff |
| 4 | API Too Many Calls | Wait, reduce frequency |
| 17 | API User Too Many Calls | Wait 1 hour |
| 190 | Access token expired | Refresh token |
| 200 | Permissions error | Check permissions |
| 294 | Invalid custom audience | Verify audience exists |

### Batch Requests

```bash
curl -X POST "https://graph.facebook.com/v20.0" \
  -H "Authorization: Bearer {access-token}" \
  -d '{
    "batch": [
      {"method": "GET", "relative_url": "{campaign-id-1}/insights?fields=spend"},
      {"method": "GET", "relative_url": "{campaign-id-2}/insights?fields=spend"},
      {"method": "GET", "relative_url": "{campaign-id-3}/insights?fields=spend"}
    ]
  }'
```

**Limit:** 50 requests per batch

### Naming Conventions

```
Campaign: [Objective]_[Audience]_[Date]
Ad Set: [Targeting]_[Placement]_[Budget]
Ad: [Creative Type]_[Version]_[Date]
Audience: [Type]_[Source]_[Size]

Example:
Campaign: Sales_Lookalike-US-1%_2026-01
Ad Set: LAL-US-1%_FB-IG-Feed_$50d
Ad: Video-15s_v1_2026-01-20
Audience: WCA_Purchasers-30d_50k
```

---

## Python SDK Example

```python
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad

# Initialize
FacebookAdsApi.init(
    app_id='YOUR_APP_ID',
    app_secret='YOUR_APP_SECRET',
    access_token='YOUR_ACCESS_TOKEN'
)

# Create campaign
ad_account = AdAccount('act_123456789')
campaign = ad_account.create_campaign(params={
    'name': 'Python SDK Campaign',
    'objective': Campaign.Objective.outcome_sales,
    'status': Campaign.Status.paused,
    'special_ad_categories': [],
})
print(f"Campaign ID: {campaign['id']}")

# Create ad set
adset = ad_account.create_ad_set(params={
    'name': 'Python SDK Ad Set',
    'campaign_id': campaign['id'],
    'daily_budget': 5000,
    'billing_event': AdSet.BillingEvent.impressions,
    'optimization_goal': AdSet.OptimizationGoal.offsite_conversions,
    'bid_strategy': AdSet.BidStrategy.lowest_cost_without_cap,
    'targeting': {
        'geo_locations': {'countries': ['US']},
        'age_min': 25,
        'age_max': 54,
    },
    'status': AdSet.Status.paused,
    'promoted_object': {
        'pixel_id': 'YOUR_PIXEL_ID',
        'custom_event_type': 'PURCHASE'
    }
})
print(f"Ad Set ID: {adset['id']}")

# Get insights
insights = campaign.get_insights(params={
    'date_preset': 'last_7d',
    'fields': ['spend', 'impressions', 'clicks', 'cpc', 'actions']
})
for insight in insights:
    print(insight)
```

### Install SDK

```bash
pip install facebook-business
```

---

## Common Workflows

### 1. Launch New Campaign

```
1. Create Campaign (objective, budget)
2. Create Ad Set (targeting, optimization)
3. Upload Media (images/videos)
4. Create Creative
5. Create Ad (link creative to ad set)
6. Review → Set to ACTIVE
```

### 2. A/B Testing

```
1. Create Campaign
2. Create 2+ Ad Sets with one variable different:
   - Different audiences
   - Different placements
   - Different bid strategies
3. Equal budgets, run 7+ days
4. Analyze with breakdown reports
5. Scale winner, pause losers
```

### 3. Retargeting Funnel

```
1. Cold audience (prospecting)
   → Website visitors (7 days)
   → Product viewers (14 days)
   → Cart abandoners (7 days)
   → Purchasers (exclude)

2. Different messaging per stage
3. Frequency caps to prevent fatigue
```

---

## Tools & Resources

| Resource | Purpose |
|----------|---------|
| [Graph API Explorer](https://developers.facebook.com/tools/explorer/) | Test API calls |
| [Marketing API Docs](https://developers.facebook.com/docs/marketing-apis/) | Official documentation |
| [Ads Manager](https://adsmanager.facebook.com/) | Manual campaign management |
| [Business Manager](https://business.facebook.com/) | Asset management |
| [Events Manager](https://business.facebook.com/events_manager/) | Pixel & CAPI setup |
| [Ads Help Center](https://www.facebook.com/business/help/) | Support documentation |

---

## Security Considerations

### Token Security

1. **Never expose tokens in client-side code**
2. **Use environment variables** for token storage
3. **Rotate tokens periodically** (every 60 days for long-lived)
4. **Limit permissions** to only what's needed
5. **Monitor token usage** for anomalies

### Data Privacy

1. **Hash all PII** before sending to API
2. **Comply with GDPR/CCPA** for audience data
3. **Implement consent management** for tracking
4. **Provide opt-out mechanisms**
5. **Audit data flows** regularly

---

## Sources

- [Meta Marketing API Documentation](https://developers.facebook.com/docs/marketing-apis/)
- [Graph API Reference](https://developers.facebook.com/docs/graph-api/)
- [Meta Pixel Documentation](https://developers.facebook.com/docs/meta-pixel/)
- [Conversions API Guide](https://developers.facebook.com/docs/marketing-api/conversions-api/)
- [Facebook Business Help Center](https://www.facebook.com/business/help/)
- [Meta for Developers Blog](https://developers.facebook.com/blog/)

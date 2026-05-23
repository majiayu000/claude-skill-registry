---
name: matomo-api
description: Matomo (Piwik) analytics platform API. Use for web analytics, tracking implementation, reporting API integration, plugin development, PHP/JavaScript tracking clients, and database schema understanding.
---

# Matomo API Skill

Comprehensive API reference for Matomo (formerly Piwik), the open-source web analytics platform. Covers tracking APIs, reporting APIs, JavaScript/PHP clients, and database schema.

## When to Use This Skill

This skill should be triggered when:
- Implementing Matomo tracking on websites or applications
- Building integrations with Matomo's Reporting API
- Querying analytics data programmatically
- Setting up event tracking, goal conversions, or ecommerce tracking
- Working with Matomo's JavaScript or PHP tracking clients
- Understanding Matomo's database structure for custom queries
- Implementing consent management and privacy controls
- Debugging Matomo tracking issues

## Quick Reference

### Tracking HTTP API Endpoint

```
https://your-matomo-domain.example/matomo.php
```

**Required Parameters:**
- `idsite` - Website ID being tracked
- `rec=1` - Required to enable tracking

**Common Parameters:**
- `action_name` - Page title for pageviews
- `url` - Full URL of the current action
- `_id` - 16-character hexadecimal visitor ID
- `rand` - Random value to prevent caching
- `apiv=1` - API version

### Event Tracking Parameters
- `e_c` - Event category
- `e_a` - Event action
- `e_n` - Event name
- `e_v` - Event value (numeric)

### Goal Conversion
- `idgoal` - Goal ID to trigger conversion
- `revenue` - Monetary value for conversion

### Ecommerce Parameters
- `ec_id` - Order ID
- `ec_items` - JSON array of items
- `revenue` - Total order value
- `ec_st` - Subtotal
- `ec_tx` - Tax
- `ec_sh` - Shipping
- `ec_dt` - Discount

### Reporting API Endpoint

```
https://your-matomo-domain.example/index.php?module=API&method=MODULE.METHOD&format=FORMAT
```

**Standard Parameters:**
| Parameter | Values | Purpose |
|-----------|--------|---------|
| `idSite` | Integer or comma-separated | Website ID(s) |
| `period` | day, week, month, year, range | Time period |
| `date` | YYYY-MM-DD or magic keywords | Specific date |
| `format` | xml, json, csv, tsv, html, rss | Output format |
| `token_auth` | Your API token | Authentication |

**Date Magic Keywords:**
- `today`, `yesterday`
- `lastWeek`, `lastMonth`, `lastYear`
- `lastX` (e.g., `last7`)
- `previousX` (e.g., `previous30`)

### JavaScript Tracking

```javascript
// Page view
_paq.push(['trackPageView', 'Custom Page Title']);

// Event
_paq.push(['trackEvent', 'Category', 'Action', 'Name', Value]);

// Goal conversion
_paq.push(['trackGoal', goalId, customRevenue]);

// Site search
_paq.push(['trackSiteSearch', 'keyword', 'category', resultsCount]);

// Ecommerce order
_paq.push(['trackEcommerceOrder', orderId, grandTotal, subTotal, tax, shipping, discount]);
```

### PHP Tracking

```php
use MatomoTracker;

$tracker = new MatomoTracker($idSite, 'https://matomo.example.com/');
$tracker->setTokenAuth($token);
$tracker->setUserId($userId);
$tracker->doTrackPageView('Page Title');
$tracker->doTrackEvent('Category', 'Action', 'Name', $value);
$tracker->doTrackGoal($idGoal, $revenue);
```

### Consent Management (JavaScript)

```javascript
// Require consent before tracking
_paq.push(['requireConsent']);

// When user gives consent
_paq.push(['setConsentGiven']);

// Cookie-specific consent
_paq.push(['requireCookieConsent']);
_paq.push(['rememberCookieConsentGiven', hoursToExpire]);

// Opt-out
_paq.push(['optUserOut']);
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **tracking-http-api.md** - HTTP Tracking API specification
- **reporting-api.md** - Reporting API methods and parameters
- **javascript-client.md** - JavaScript Tracking Client reference
- **php-client.md** - PHP Tracking Client reference
- **database-schema.md** - Database tables and relationships

## Common Patterns

### Bulk Tracking (HTTP)

```json
POST https://matomo.example.com/matomo.php
{
  "requests": [
    "?idsite=1&rec=1&url=https://example.org/page1",
    "?idsite=1&rec=1&url=https://example.org/page2"
  ],
  "token_auth": "your_token_here"
}
```

### Bulk API Requests (Reporting)

```
?module=API&method=API.getBulkRequest
&urls[0]=method%3DVisitsSummary.get%26idSite%3D1%26period%3Dday%26date%3Dtoday
&urls[1]=method%3DActions.getPageUrls%26idSite%3D1%26period%3Dday%26date%3Dtoday
```

### Segmentation

```
# Visits from mobile devices in United States
&segment=deviceType==smartphone;countryCode==us

# Visits with specific event
&segment=eventCategory==Video;eventAction==Play
```

### PHP Bulk Tracking

```php
$tracker->enableBulkTracking();
$tracker->doTrackPageView('Page 1');
$tracker->doTrackPageView('Page 2');
$tracker->doTrackEvent('Category', 'Action');
$tracker->doBulkTrack(); // Send all at once
```

## Key API Modules

### Visitor Analytics
- `VisitsSummary` - Overall visit metrics
- `UserCountry` - Geographic data
- `DevicesDetection` - Device and browser info
- `UserLanguage` - Language preferences

### Actions & Content
- `Actions` - Pages, downloads, outlinks
- `Events` - Custom event tracking
- `Contents` - Content impression tracking

### Conversions
- `Goals` - Goal conversions and revenue
- `Ecommerce` - Ecommerce transactions

### Traffic Sources
- `Referrers` - Traffic source analysis
- `MarketingCampaignsReporting` - Campaign tracking

### Real-time
- `Live` - Real-time visitor data
- `Live.getLastVisitsDetails` - Recent visitor details

## Core Metrics

| Metric | Description |
|--------|-------------|
| `nb_uniq_visitors` | Unique visitors |
| `nb_visits` | Total visits (30-min session) |
| `nb_actions` | Page views, downloads, outlinks |
| `bounce_rate` | Single-page visit percentage |
| `avg_time_on_page` | Average page duration |
| `revenue` | Goal/ecommerce revenue |
| `conversion_rate` | Goal achievement ratio |

## Database Tables

### Log Data (Raw)
- `log_visit` - Individual visits
- `log_link_visit_action` - Actions within visits
- `log_action` - Action definitions (URLs, titles)
- `log_conversion` - Goal conversions
- `log_conversion_item` - Ecommerce items

### Archive Data (Aggregated)
- `archive_numeric_YYYY_MM` - Numeric metrics
- `archive_blob_YYYY_MM` - Report data (compressed)

### Configuration
- `site` - Website configuration
- `goal` - Goal definitions
- `segment` - Saved segments
- `user` - User accounts
- `access` - User permissions

## Authentication

### Token Authentication
```
&token_auth=YOUR_TOKEN_HERE
```

- Create tokens in: Administration > Personal > Security > Auth tokens
- Never share URLs containing tokens publicly
- Use POST requests with token in body for enhanced security

### Features Requiring Auth
- IP address override (`cip`)
- Custom timestamp (`cdt`)
- Geolocation override (`country`, `region`, `city`, `lat`, `long`)

## Performance Tips

1. **Use Bulk Tracking** - Batch multiple tracking calls
2. **Cache API Responses** - Set appropriate cache headers
3. **Use Segments Sparingly** - Complex segments impact performance
4. **Archive Data** - Query archive tables for historical reports
5. **Limit Results** - Use `filter_limit` to restrict row counts

## Resources

- [Official API Documentation](https://developer.matomo.org/api-reference)
- [Tracking HTTP API](https://developer.matomo.org/api-reference/tracking-api)
- [Reporting API](https://developer.matomo.org/api-reference/reporting-api)
- [JavaScript Client](https://developer.matomo.org/api-reference/tracking-javascript)
- [PHP Client](https://developer.matomo.org/api-reference/PHP-Piwik-Tracker)
- [Database Schema](https://developer.matomo.org/guides/database-schema)

## Notes

- Matomo was formerly known as Piwik
- API supports both Matomo 4.x and 5.x versions
- Session timeout default is 30 minutes
- Visitor ID is 16-character hexadecimal
- All tracking requests should include `rec=1` parameter

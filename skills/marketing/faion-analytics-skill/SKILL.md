---
name: faion-analytics-skill
user-invocable: false
description: ""
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npm:*, npx:*, curl:*)
---

# Analytics Skill

**Communication: User's language. Docs/code: English.**

## Purpose

Provides comprehensive analytics integration patterns for web applications. Covers Google Analytics 4 (GA4), Plausible Analytics, event tracking, custom dimensions, conversion tracking, funnel analysis, and privacy compliance (GDPR/CCPA).

## 3-Layer Architecture Position

```
Layer 1: Domain Skills (faion-marketing-domain-skill)
    ↓ calls
Layer 2: Agents (faion-ads-agent, faion-growth-agent)
    ↓ uses
Layer 3: Technical Skills (this) ← faion-analytics-skill
```

---

# Section 1: Google Analytics 4 (GA4)

## 1.1 Setup and Configuration

### Measurement ID

GA4 uses Measurement IDs in format `G-XXXXXXXXXX`.

```html
<!-- gtag.js installation -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### Data Streams

| Stream Type | Use Case | Configuration |
|-------------|----------|---------------|
| Web | Websites | Domain, enhanced measurement |
| iOS | iOS apps | Bundle ID, App Store ID |
| Android | Android apps | Package name, Firebase |

### Enhanced Measurement

Auto-tracked events when enabled:
- `page_view` - Page loads
- `scroll` - 90% page depth
- `click` - Outbound links
- `view_search_results` - Site search
- `video_start`, `video_progress`, `video_complete` - Video engagement
- `file_download` - File downloads

```javascript
// Disable specific enhanced measurement
gtag('config', 'G-XXXXXXXXXX', {
  'send_page_view': false,  // Disable auto page_view
});
```

### User Properties

```javascript
// Set user properties for segmentation
gtag('set', 'user_properties', {
  subscription_tier: 'premium',
  account_age_days: 365,
  preferred_language: 'en'
});
```

## 1.2 Event Tracking

### Event Categories

| Category | Description | Examples |
|----------|-------------|----------|
| Automatic | Collected by default | `first_visit`, `session_start` |
| Enhanced | Require enhanced measurement | `scroll`, `click`, `file_download` |
| Recommended | Google-defined schemas | `login`, `sign_up`, `purchase` |
| Custom | Your own events | `feature_used`, `feedback_submitted` |

### Recommended Events

```javascript
// Sign up
gtag('event', 'sign_up', {
  method: 'email'  // or 'google', 'facebook'
});

// Login
gtag('event', 'login', {
  method: 'email'
});

// Purchase (ecommerce)
gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 99.99,
  currency: 'USD',
  items: [{
    item_id: 'SKU_001',
    item_name: 'Premium Plan',
    price: 99.99,
    quantity: 1
  }]
});

// Begin checkout
gtag('event', 'begin_checkout', {
  currency: 'USD',
  value: 99.99,
  items: [...]
});

// Add to cart
gtag('event', 'add_to_cart', {
  currency: 'USD',
  value: 29.99,
  items: [{
    item_id: 'SKU_002',
    item_name: 'Pro Subscription',
    price: 29.99,
    quantity: 1
  }]
});
```

### Custom Events

```javascript
// Feature usage tracking
gtag('event', 'feature_used', {
  feature_name: 'dark_mode',
  feature_category: 'settings'
});

// Content engagement
gtag('event', 'article_read', {
  article_id: 'sdd-intro-001',
  article_category: 'methodology',
  read_percentage: 100,
  time_on_page: 180
});

// Subscription events
gtag('event', 'subscription_started', {
  plan_name: 'Plus',
  plan_price: 19,
  billing_cycle: 'monthly',
  trial: false
});

// Error tracking
gtag('event', 'error_occurred', {
  error_type: 'api_error',
  error_message: 'Payment failed',
  error_code: 402
});
```

### Event Parameters

| Parameter | Type | Max Length | Description |
|-----------|------|------------|-------------|
| event_name | string | 40 chars | Event identifier |
| event_params | object | 25 params | Custom parameters |
| param_name | string | 40 chars | Parameter key |
| param_value | string/number | 100 chars | Parameter value |

## 1.3 Custom Dimensions and Metrics

### Configuration

Custom dimensions/metrics configured in GA4 Admin:
1. Admin → Data display → Custom definitions
2. Create custom dimension/metric
3. Scope: Event or User

### Event-scoped Dimensions

```javascript
// Register in GA4 Admin first, then send:
gtag('event', 'page_view', {
  content_type: 'article',      // custom dimension
  author_name: 'Ruslan Faion',  // custom dimension
  word_count: 1500              // custom metric
});
```

### User-scoped Dimensions

```javascript
// Persists across sessions
gtag('set', 'user_properties', {
  user_tier: 'premium',
  signup_source: 'product_hunt',
  lifetime_value: 299
});
```

## 1.4 Conversion Goals

### Setting Up Conversions

1. Admin → Events
2. Mark event as conversion (toggle)
3. Or create via API

### Key Conversion Events

```javascript
// Subscription conversion
gtag('event', 'generate_lead', {
  currency: 'USD',
  value: 19.00,
  lead_source: 'landing_page'
});

// Trial started
gtag('event', 'start_trial', {
  plan_name: 'Pro',
  trial_duration_days: 14
});

// Upgrade conversion
gtag('event', 'upgrade_plan', {
  from_plan: 'Free',
  to_plan: 'Plus',
  value: 19.00
});
```

### Conversion Value

```javascript
// Assign monetary value to conversions
gtag('event', 'purchase', {
  value: 99.99,
  currency: 'USD',
  transaction_id: 'T12345'
});
```

## 1.5 Funnel Analysis

### Funnel Definition (in GA4 UI)

```
Funnel: Subscription Flow
Step 1: landing_page_view
Step 2: pricing_view
Step 3: begin_checkout
Step 4: payment_info_entered
Step 5: purchase
```

### Track Funnel Steps

```javascript
// Step 1: Landing page
gtag('event', 'landing_page_view', {
  page_variant: 'A',
  utm_source: 'google'
});

// Step 2: Pricing view
gtag('event', 'pricing_view', {
  displayed_plans: ['Free', 'Plus', 'Pro']
});

// Step 3: Checkout started
gtag('event', 'begin_checkout', {
  selected_plan: 'Plus',
  value: 19.00,
  currency: 'USD'
});

// Step 4: Payment info
gtag('event', 'add_payment_info', {
  payment_type: 'credit_card'
});

// Step 5: Purchase
gtag('event', 'purchase', {
  transaction_id: 'T12345',
  value: 19.00,
  currency: 'USD'
});
```

### Funnel Analysis Queries

Use GA4 Explorations:
1. Explore → Funnel exploration
2. Configure steps
3. Analyze drop-off rates

## 1.6 GA4 Data API (Reporting)

### Authentication

```bash
# Service account setup
# 1. Create service account in Google Cloud Console
# 2. Add to GA4 property as viewer/editor
# 3. Download JSON key
```

### Python Client

```python
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
    FilterExpression,
    Filter
)

# Initialize client
client = BetaAnalyticsDataClient()
property_id = "properties/XXXXXXXXX"

# Run report
request = RunReportRequest(
    property=property_id,
    date_ranges=[DateRange(start_date="7daysAgo", end_date="today")],
    dimensions=[
        Dimension(name="eventName"),
        Dimension(name="date")
    ],
    metrics=[
        Metric(name="eventCount"),
        Metric(name="totalUsers")
    ]
)

response = client.run_report(request)

for row in response.rows:
    print(f"{row.dimension_values[0].value}: {row.metric_values[0].value}")
```

### Common Dimensions and Metrics

| Dimensions | Description |
|------------|-------------|
| `date` | Date (YYYYMMDD) |
| `eventName` | Event name |
| `pagePath` | Page URL path |
| `sessionSource` | Traffic source |
| `deviceCategory` | Desktop/Mobile/Tablet |
| `country` | User country |

| Metrics | Description |
|---------|-------------|
| `eventCount` | Event occurrences |
| `totalUsers` | Unique users |
| `sessions` | Session count |
| `averageSessionDuration` | Avg session length |
| `bounceRate` | Bounce rate |
| `conversions` | Conversion count |

### REST API

```bash
# Get report via REST
curl -X POST \
  "https://analyticsdata.googleapis.com/v1beta/properties/XXXXXXXXX:runReport" \
  -H "Authorization: Bearer $(gcloud auth print-access-token)" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges": [{"startDate": "7daysAgo", "endDate": "today"}],
    "dimensions": [{"name": "eventName"}],
    "metrics": [{"name": "eventCount"}]
  }'
```

---

# Section 2: Plausible Analytics

## 2.1 Setup

### Script Installation

```html
<!-- Basic installation -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>

<!-- Self-hosted -->
<script defer data-domain="yourdomain.com" src="https://analytics.yourdomain.com/js/script.js"></script>

<!-- With custom events -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.tagged-events.js"></script>

<!-- With file downloads -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.file-downloads.js"></script>

<!-- All extensions -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.tagged-events.file-downloads.outbound-links.js"></script>
```

### Custom Domain (Proxy)

```nginx
# Nginx proxy for privacy
location /js/script.js {
    proxy_pass https://plausible.io/js/script.js;
    proxy_set_header Host plausible.io;
}

location /api/event {
    proxy_pass https://plausible.io/api/event;
    proxy_set_header Host plausible.io;
}
```

```html
<!-- Use proxied script -->
<script defer data-domain="yourdomain.com" data-api="/api/event" src="/js/script.js"></script>
```

### Gatsby Integration

```javascript
// gatsby-config.js
module.exports = {
  plugins: [
    {
      resolve: 'gatsby-plugin-plausible',
      options: {
        domain: 'yourdomain.com',
        // Optional: self-hosted
        customDomain: 'analytics.yourdomain.com',
      },
    },
  ],
};
```

### React Integration

```javascript
// PlausibleProvider.jsx
import { useEffect } from 'react';

export function PlausibleProvider({ domain, children }) {
  useEffect(() => {
    const script = document.createElement('script');
    script.defer = true;
    script.dataset.domain = domain;
    script.src = 'https://plausible.io/js/script.js';
    document.head.appendChild(script);

    return () => {
      document.head.removeChild(script);
    };
  }, [domain]);

  return children;
}
```

## 2.2 Event Tracking

### Custom Events

```javascript
// Basic event
plausible('signup');

// Event with props (custom properties)
plausible('signup', {
  props: {
    plan: 'premium',
    source: 'landing_page'
  }
});

// Revenue tracking
plausible('purchase', {
  revenue: { currency: 'USD', amount: 99.99 },
  props: {
    plan: 'Pro',
    billing: 'annual'
  }
});
```

### Goal Tracking

```javascript
// Define goals in Plausible dashboard first

// Track goal completion
plausible('Download', {
  props: {
    file: 'sdd-guide.pdf',
    format: 'pdf'
  }
});

// Track 404 errors
plausible('404', {
  props: {
    path: document.location.pathname
  }
});
```

### CSS Class Events (Tagged Events)

```html
<!-- Auto-track clicks with class -->
<a href="/pricing" class="plausible-event-name=Pricing+View">View Pricing</a>

<!-- With props -->
<button class="plausible-event-name=CTA+Click plausible-event-position=header">
  Get Started
</button>
```

## 2.3 Plausible Stats API

### Authentication

```bash
# API key from Plausible Settings → API Keys
export PLAUSIBLE_API_KEY="your-api-key"
```

### Aggregate Stats

```bash
# Get aggregate stats
curl "https://plausible.io/api/v1/stats/aggregate?site_id=yourdomain.com&period=30d&metrics=visitors,pageviews,bounce_rate,visit_duration" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Response:
{
  "results": {
    "visitors": {"value": 12500},
    "pageviews": {"value": 45000},
    "bounce_rate": {"value": 42.5},
    "visit_duration": {"value": 185}
  }
}
```

### Timeseries Data

```bash
# Daily visitors over 30 days
curl "https://plausible.io/api/v1/stats/timeseries?site_id=yourdomain.com&period=30d&metrics=visitors" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Response:
{
  "results": [
    {"date": "2026-01-01", "visitors": 450},
    {"date": "2026-01-02", "visitors": 520},
    ...
  ]
}
```

### Breakdown Reports

```bash
# Top pages
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=event:page&metrics=visitors,pageviews" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Top sources
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=visit:source&metrics=visitors" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Device breakdown
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=visit:device&metrics=visitors" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Custom event breakdown
curl "https://plausible.io/api/v1/stats/breakdown?site_id=yourdomain.com&period=30d&property=event:name&metrics=visitors,events" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"
```

### Realtime Stats

```bash
# Current visitors (last 5 minutes)
curl "https://plausible.io/api/v1/stats/realtime/visitors?site_id=yourdomain.com" \
  -H "Authorization: Bearer $PLAUSIBLE_API_KEY"

# Response:
10  # Number of current visitors
```

### Python Client

```python
import requests

class PlausibleClient:
    def __init__(self, api_key: str, site_id: str, base_url: str = "https://plausible.io"):
        self.api_key = api_key
        self.site_id = site_id
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_key}"}

    def aggregate(self, period: str = "30d", metrics: list = None):
        """Get aggregate stats."""
        metrics = metrics or ["visitors", "pageviews", "bounce_rate"]
        params = {
            "site_id": self.site_id,
            "period": period,
            "metrics": ",".join(metrics)
        }
        response = requests.get(
            f"{self.base_url}/api/v1/stats/aggregate",
            headers=self.headers,
            params=params
        )
        return response.json()

    def timeseries(self, period: str = "30d", metrics: list = None):
        """Get timeseries data."""
        metrics = metrics or ["visitors"]
        params = {
            "site_id": self.site_id,
            "period": period,
            "metrics": ",".join(metrics)
        }
        response = requests.get(
            f"{self.base_url}/api/v1/stats/timeseries",
            headers=self.headers,
            params=params
        )
        return response.json()

    def breakdown(self, property: str, period: str = "30d", metrics: list = None):
        """Get breakdown by property."""
        metrics = metrics or ["visitors"]
        params = {
            "site_id": self.site_id,
            "period": period,
            "property": property,
            "metrics": ",".join(metrics)
        }
        response = requests.get(
            f"{self.base_url}/api/v1/stats/breakdown",
            headers=self.headers,
            params=params
        )
        return response.json()

    def realtime_visitors(self):
        """Get current visitors."""
        response = requests.get(
            f"{self.base_url}/api/v1/stats/realtime/visitors",
            headers=self.headers,
            params={"site_id": self.site_id}
        )
        return int(response.text)


# Usage
client = PlausibleClient(
    api_key="your-api-key",
    site_id="yourdomain.com"
)

# Get last 30 days stats
stats = client.aggregate(period="30d", metrics=["visitors", "pageviews"])
print(f"Visitors: {stats['results']['visitors']['value']}")

# Get top pages
pages = client.breakdown(property="event:page", metrics=["visitors", "pageviews"])
for page in pages['results'][:10]:
    print(f"{page['page']}: {page['visitors']} visitors")
```

---

# Section 3: Event Tracking Patterns

## 3.1 SaaS Metrics Events

### User Lifecycle

```javascript
// Acquisition
function trackSignup(method, source) {
  // GA4
  gtag('event', 'sign_up', { method, source });
  // Plausible
  plausible('Signup', { props: { method, source } });
}

// Activation
function trackActivation(feature) {
  gtag('event', 'activation', { first_feature: feature });
  plausible('Activation', { props: { feature } });
}

// Retention
function trackReturn(daysSinceLastVisit) {
  gtag('event', 'user_return', { days_away: daysSinceLastVisit });
  plausible('Return', { props: { days_away: daysSinceLastVisit } });
}

// Revenue
function trackPurchase(plan, price, currency) {
  gtag('event', 'purchase', {
    value: price,
    currency,
    items: [{ item_name: plan, price }]
  });
  plausible('Purchase', {
    revenue: { currency, amount: price },
    props: { plan }
  });
}

// Referral
function trackReferral(referrerId) {
  gtag('event', 'referral_signup', { referrer_id: referrerId });
  plausible('Referral', { props: { referrer_id: referrerId } });
}
```

### Feature Usage

```javascript
// Generic feature tracker
function trackFeatureUsage(featureName, action, metadata = {}) {
  gtag('event', 'feature_usage', {
    feature_name: featureName,
    feature_action: action,
    ...metadata
  });
  plausible('Feature', {
    props: {
      name: featureName,
      action,
      ...metadata
    }
  });
}

// Examples
trackFeatureUsage('dark_mode', 'enabled');
trackFeatureUsage('export', 'pdf_downloaded', { page_count: 5 });
trackFeatureUsage('ai_assistant', 'query', { query_length: 150 });
```

## 3.2 Content Engagement

### Article Tracking

```javascript
// Read progress tracking
function trackReadProgress(articleId, percentage) {
  const milestones = [25, 50, 75, 100];
  if (milestones.includes(percentage)) {
    gtag('event', 'article_progress', {
      article_id: articleId,
      progress: percentage
    });
    plausible('Article Progress', {
      props: { article_id: articleId, progress: percentage }
    });
  }
}

// Time on page
function trackTimeOnPage(articleId, seconds) {
  const milestones = [30, 60, 120, 300];
  milestones.forEach(milestone => {
    if (seconds >= milestone) {
      gtag('event', 'time_milestone', {
        article_id: articleId,
        seconds: milestone
      });
    }
  });
}

// Scroll depth with IntersectionObserver
function trackScrollDepth() {
  const markers = [25, 50, 75, 100];
  markers.forEach(depth => {
    const marker = document.getElementById(`scroll-${depth}`);
    if (marker) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            gtag('event', 'scroll_depth', { depth });
            observer.unobserve(entry.target);
          }
        });
      });
      observer.observe(marker);
    }
  });
}
```

### Video Tracking

```javascript
// Video engagement
function trackVideo(videoId, action, progress = null) {
  const data = { video_id: videoId, action };
  if (progress !== null) data.progress = progress;

  gtag('event', 'video_engagement', data);
  plausible('Video', { props: data });
}

// Usage
video.addEventListener('play', () => trackVideo('intro-video', 'play'));
video.addEventListener('pause', () => trackVideo('intro-video', 'pause'));
video.addEventListener('ended', () => trackVideo('intro-video', 'complete'));

// Progress tracking
video.addEventListener('timeupdate', () => {
  const progress = Math.floor((video.currentTime / video.duration) * 100);
  if ([25, 50, 75].includes(progress)) {
    trackVideo('intro-video', 'progress', progress);
  }
});
```

## 3.3 Conversion Tracking

### Multi-Step Funnel

```javascript
class FunnelTracker {
  constructor(funnelName) {
    this.funnelName = funnelName;
    this.startTime = null;
  }

  trackStep(stepNumber, stepName, metadata = {}) {
    if (stepNumber === 1) {
      this.startTime = Date.now();
    }

    const timeFromStart = this.startTime
      ? Math.floor((Date.now() - this.startTime) / 1000)
      : 0;

    gtag('event', 'funnel_step', {
      funnel_name: this.funnelName,
      step_number: stepNumber,
      step_name: stepName,
      time_from_start: timeFromStart,
      ...metadata
    });

    plausible('Funnel Step', {
      props: {
        funnel: this.funnelName,
        step: stepNumber,
        name: stepName,
        ...metadata
      }
    });
  }

  trackCompletion(value = 0, currency = 'USD') {
    const totalTime = this.startTime
      ? Math.floor((Date.now() - this.startTime) / 1000)
      : 0;

    gtag('event', 'funnel_complete', {
      funnel_name: this.funnelName,
      value,
      currency,
      total_time_seconds: totalTime
    });

    plausible('Funnel Complete', {
      revenue: { currency, amount: value },
      props: {
        funnel: this.funnelName,
        time_seconds: totalTime
      }
    });
  }

  trackAbandonment(lastStep) {
    gtag('event', 'funnel_abandon', {
      funnel_name: this.funnelName,
      last_step: lastStep
    });

    plausible('Funnel Abandon', {
      props: {
        funnel: this.funnelName,
        last_step: lastStep
      }
    });
  }
}

// Usage
const checkoutFunnel = new FunnelTracker('checkout');
checkoutFunnel.trackStep(1, 'cart_view', { items_count: 2 });
checkoutFunnel.trackStep(2, 'shipping_info');
checkoutFunnel.trackStep(3, 'payment_info');
checkoutFunnel.trackStep(4, 'review_order');
checkoutFunnel.trackCompletion(99.99, 'USD');
```

### A/B Test Tracking

```javascript
// Track experiment exposure
function trackExperiment(experimentId, variant) {
  gtag('event', 'experiment_exposure', {
    experiment_id: experimentId,
    variant_id: variant
  });

  // Set as user property for segmentation
  gtag('set', 'user_properties', {
    [`exp_${experimentId}`]: variant
  });

  plausible('Experiment', {
    props: {
      experiment: experimentId,
      variant
    }
  });
}

// Track conversion within experiment
function trackExperimentConversion(experimentId, variant, conversionType, value = 0) {
  gtag('event', 'experiment_conversion', {
    experiment_id: experimentId,
    variant_id: variant,
    conversion_type: conversionType,
    value
  });

  plausible('Experiment Conversion', {
    revenue: value > 0 ? { currency: 'USD', amount: value } : undefined,
    props: {
      experiment: experimentId,
      variant,
      type: conversionType
    }
  });
}
```

---

# Section 4: Privacy Compliance

## 4.1 GDPR Compliance

### Cookie Consent Integration

```javascript
// Cookie consent manager integration
class AnalyticsManager {
  constructor() {
    this.consentGiven = false;
    this.queuedEvents = [];
  }

  init() {
    // Check for existing consent
    const consent = localStorage.getItem('analytics_consent');
    if (consent === 'granted') {
      this.enableAnalytics();
    }
  }

  grantConsent() {
    localStorage.setItem('analytics_consent', 'granted');
    this.consentGiven = true;
    this.enableAnalytics();
    this.flushQueue();
  }

  revokeConsent() {
    localStorage.setItem('analytics_consent', 'denied');
    this.consentGiven = false;
    this.disableAnalytics();
  }

  enableAnalytics() {
    // GA4 consent update
    gtag('consent', 'update', {
      'analytics_storage': 'granted'
    });
    this.consentGiven = true;
  }

  disableAnalytics() {
    gtag('consent', 'update', {
      'analytics_storage': 'denied'
    });
    // Clear existing cookies
    this.clearAnalyticsCookies();
  }

  track(eventName, params = {}) {
    if (this.consentGiven) {
      gtag('event', eventName, params);
      plausible(eventName, { props: params });
    } else {
      // Queue events for later
      this.queuedEvents.push({ eventName, params, timestamp: Date.now() });
    }
  }

  flushQueue() {
    this.queuedEvents.forEach(({ eventName, params }) => {
      gtag('event', eventName, params);
      plausible(eventName, { props: params });
    });
    this.queuedEvents = [];
  }

  clearAnalyticsCookies() {
    // GA4 cookies
    const gaCookies = ['_ga', '_ga_*', '_gid', '_gat'];
    gaCookies.forEach(name => {
      document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/; domain=.${window.location.hostname}`;
    });
  }
}

const analytics = new AnalyticsManager();
analytics.init();
```

### GA4 Consent Mode

```javascript
// Default consent state (before user choice)
gtag('consent', 'default', {
  'analytics_storage': 'denied',
  'ad_storage': 'denied',
  'ad_user_data': 'denied',
  'ad_personalization': 'denied'
});

// After user grants consent
function onConsentGranted(preferences) {
  gtag('consent', 'update', {
    'analytics_storage': preferences.analytics ? 'granted' : 'denied',
    'ad_storage': preferences.marketing ? 'granted' : 'denied',
    'ad_user_data': preferences.marketing ? 'granted' : 'denied',
    'ad_personalization': preferences.marketing ? 'granted' : 'denied'
  });
}
```

### Data Retention Settings

```javascript
// Configure data retention (in GA4 Admin)
// Options: 2 months, 14 months

// Reset user data on logout
gtag('config', 'G-XXXXXXXXXX', {
  'user_id': undefined  // Clear user identification
});
```

## 4.2 CCPA Compliance

### Do Not Sell Implementation

```javascript
// Check for Global Privacy Control signal
function checkGPC() {
  return navigator.globalPrivacyControl === true;
}

// Honor Do Not Sell preference
function initAnalyticsWithCCPA() {
  const doNotSell = localStorage.getItem('ccpa_opt_out') === 'true' || checkGPC();

  if (doNotSell) {
    // Disable data sharing/selling
    gtag('set', 'restricted_data_processing', true);
  }
}

// Opt-out handler
function handleCCPAOptOut() {
  localStorage.setItem('ccpa_opt_out', 'true');
  gtag('set', 'restricted_data_processing', true);
}
```

## 4.3 Privacy-First Analytics (Plausible)

Plausible is GDPR-compliant by design:
- No cookies
- No personal data collection
- No cross-site tracking
- EU-hosted option available

```html
<!-- Plausible - no consent needed in most cases -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>

<!-- Optional: Exclude yourself from tracking -->
<script>
  if (localStorage.getItem('plausible_ignore') === 'true') {
    window.plausible = function() {};
  }
</script>
```

## 4.4 IP Anonymization

### GA4 (Automatic)

GA4 automatically anonymizes IP addresses. No additional configuration needed.

### Custom Server-Side

```python
# For server-side tracking
import hashlib

def anonymize_ip(ip_address: str) -> str:
    """Anonymize IP by hashing."""
    # Remove last octet for IPv4
    if '.' in ip_address:
        parts = ip_address.split('.')
        parts[-1] = '0'
        return '.'.join(parts)
    # Remove last 80 bits for IPv6
    elif ':' in ip_address:
        return ip_address.rsplit(':', 5)[0] + '::'
    return ip_address
```

---

# Section 5: Best Practices

## 5.1 Implementation Checklist

### Pre-Launch

- [ ] Choose analytics platform(s) (GA4, Plausible, or both)
- [ ] Set up properties/sites
- [ ] Install tracking code
- [ ] Configure consent management
- [ ] Define key events and conversions
- [ ] Set up custom dimensions/metrics
- [ ] Configure data retention
- [ ] Test tracking in development

### Event Naming

| Convention | Example | Description |
|------------|---------|-------------|
| snake_case | `button_click` | GA4 recommended |
| Title Case | `Button Click` | Plausible goals |
| Consistent | Always use same format | Easier analysis |

### Parameter Guidelines

- Keep parameter names short but descriptive
- Use consistent naming across events
- Limit to 25 parameters per event (GA4)
- Use numbers for metrics, strings for dimensions

## 5.2 Debugging

### GA4 DebugView

```javascript
// Enable debug mode
gtag('config', 'G-XXXXXXXXXX', {
  'debug_mode': true
});

// Or via URL parameter
// ?debug_mode=1
```

### Browser DevTools

```javascript
// Log all analytics calls
const originalGtag = window.gtag;
window.gtag = function() {
  console.log('gtag call:', arguments);
  originalGtag.apply(this, arguments);
};
```

### Plausible Debug

```javascript
// Check if Plausible loaded
console.log('Plausible loaded:', typeof window.plausible === 'function');

// Log Plausible calls
const originalPlausible = window.plausible;
window.plausible = function() {
  console.log('plausible call:', arguments);
  if (originalPlausible) originalPlausible.apply(this, arguments);
};
```

## 5.3 Performance

### Async Loading

```html
<!-- GA4 - async by default -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>

<!-- Plausible - defer loading -->
<script defer data-domain="yourdomain.com" src="https://plausible.io/js/script.js"></script>
```

### Lazy Loading Analytics

```javascript
// Load analytics after user interaction
let analyticsLoaded = false;

function loadAnalytics() {
  if (analyticsLoaded) return;
  analyticsLoaded = true;

  // Load GA4
  const gaScript = document.createElement('script');
  gaScript.async = true;
  gaScript.src = 'https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX';
  document.head.appendChild(gaScript);

  gaScript.onload = () => {
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-XXXXXXXXXX');
  };
}

// Trigger on first interaction
['scroll', 'click', 'touchstart'].forEach(event => {
  document.addEventListener(event, loadAnalytics, { once: true, passive: true });
});
```

### Batch Events

```javascript
// Batch multiple events
class EventBatcher {
  constructor(flushInterval = 5000) {
    this.queue = [];
    this.flushInterval = flushInterval;
    setInterval(() => this.flush(), flushInterval);
  }

  add(eventName, params) {
    this.queue.push({ eventName, params, timestamp: Date.now() });
  }

  flush() {
    if (this.queue.length === 0) return;

    // Send batched events
    this.queue.forEach(({ eventName, params }) => {
      gtag('event', eventName, params);
    });

    this.queue = [];
  }
}
```

---

# Section 6: Framework Integration

## 6.1 React/Gatsby

```javascript
// hooks/useAnalytics.js
import { useCallback } from 'react';

export function useAnalytics() {
  const trackEvent = useCallback((eventName, params = {}) => {
    // GA4
    if (typeof gtag !== 'undefined') {
      gtag('event', eventName, params);
    }

    // Plausible
    if (typeof plausible !== 'undefined') {
      plausible(eventName, { props: params });
    }
  }, []);

  const trackPageView = useCallback((path, title) => {
    if (typeof gtag !== 'undefined') {
      gtag('event', 'page_view', {
        page_path: path,
        page_title: title
      });
    }

    // Plausible auto-tracks page views
  }, []);

  return { trackEvent, trackPageView };
}

// Usage in component
function PricingPage() {
  const { trackEvent } = useAnalytics();

  const handlePlanSelect = (plan) => {
    trackEvent('plan_selected', { plan_name: plan });
  };

  return (
    <button onClick={() => handlePlanSelect('Pro')}>
      Select Pro Plan
    </button>
  );
}
```

## 6.2 Django Integration

```python
# analytics/middleware.py
class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Track server-side events if needed
        if hasattr(request, 'analytics_events'):
            for event in request.analytics_events:
                # Send to GA4 Measurement Protocol
                self.send_to_ga4(event)

        return response

    def send_to_ga4(self, event):
        import requests

        payload = {
            'client_id': event.get('client_id'),
            'events': [{
                'name': event.get('name'),
                'params': event.get('params', {})
            }]
        }

        requests.post(
            f'https://www.google-analytics.com/mp/collect?measurement_id=G-XXXXXXXXXX&api_secret=YOUR_SECRET',
            json=payload
        )


# views.py
def purchase_view(request):
    # Server-side event tracking
    if not hasattr(request, 'analytics_events'):
        request.analytics_events = []

    request.analytics_events.append({
        'client_id': request.session.get('ga_client_id'),
        'name': 'purchase',
        'params': {
            'value': 99.99,
            'currency': 'USD',
            'transaction_id': 'T12345'
        }
    })

    return JsonResponse({'status': 'success'})
```

## 6.3 Server-Side Tracking (GA4 Measurement Protocol)

```python
import requests
import uuid

def track_server_event(
    measurement_id: str,
    api_secret: str,
    client_id: str,
    event_name: str,
    params: dict = None
):
    """Send event to GA4 via Measurement Protocol."""
    url = f"https://www.google-analytics.com/mp/collect?measurement_id={measurement_id}&api_secret={api_secret}"

    payload = {
        "client_id": client_id,
        "events": [{
            "name": event_name,
            "params": params or {}
        }]
    }

    response = requests.post(url, json=payload)
    return response.status_code == 204


# Usage
track_server_event(
    measurement_id="G-XXXXXXXXXX",
    api_secret="YOUR_API_SECRET",
    client_id="user_123",
    event_name="subscription_renewed",
    params={
        "plan": "Pro",
        "value": 35.00,
        "currency": "USD"
    }
)
```

---

# Related Skills and Agents

| Component | Relationship |
|-----------|--------------|
| faion-ads-agent | Uses this skill for conversion tracking |
| faion-growth-agent | Uses this skill for funnel analysis |
| faion-marketing-domain-skill | Orchestrates analytics workflows |
| faion-google-ads-skill | Shares conversion data with Google Ads |
| faion-meta-ads-skill | Shares conversion data with Meta |
| faion-seo-skill | Tracks organic traffic metrics |

---

*Analytics Skill v1.0 - 2026-01-18*
*Platforms: GA4, Plausible*
*Features: Event Tracking, Custom Dimensions, Conversions, Funnels, Reporting API, Privacy Compliance*

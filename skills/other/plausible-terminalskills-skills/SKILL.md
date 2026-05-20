---
name: plausible
category: data-ai
version: 1.0.0
description: >-
  Privacy-first web analytics with Plausible — lightweight script tag, no cookies,
  GDPR-compliant by default. Self-host with Docker or use Plausible Cloud.
  Covers script installation, custom event goals, pageview filtering, the Stats
  API for programmatic access, and Google Search Console integration. Use when
  tasks involve adding website analytics without cookie banners, replacing Google
  Analytics with a privacy-friendly alternative, or querying traffic data via API.
author: terminal-skills
tags: [plausible, analytics, privacy, web-analytics, gdpr, self-hosted]
license: Apache-2.0
compatibility: 'platform: linux, platform: macos, platform: windows'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags: [plausible, analytics, privacy, web-analytics, gdpr]
---

# Plausible Analytics

Privacy-first, cookie-free web analytics. Lightweight script (<1KB), no personal data collection, GDPR/CCPA/PECR compliant out of the box.

## Self-Hosting with Docker Compose

```yaml
# docker-compose.yml — Plausible Community Edition self-hosted stack.
# Runs Plausible with PostgreSQL for user data and ClickHouse for analytics.
version: '3.8'

services:
  plausible:
    image: ghcr.io/plausible/community-edition:v2
    command: sh -c "sleep 10 && /entrypoint.sh db createdb && /entrypoint.sh db migrate && /entrypoint.sh run"
    ports:
      - '8000:8000'
    environment:
      BASE_URL: https://analytics.example.com
      SECRET_KEY_BASE: '<generate-with-openssl-rand-base64-48>'
      DATABASE_URL: postgres://plausible:plausible@db:5432/plausible
      CLICKHOUSE_DATABASE_URL: http://clickhouse:8123/plausible_events
    depends_on:
      - db
      - clickhouse

  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: plausible
      POSTGRES_USER: plausible
      POSTGRES_PASSWORD: plausible
    volumes:
      - postgres-data:/var/lib/postgresql/data

  clickhouse:
    image: clickhouse/clickhouse-server:24.3-alpine
    volumes:
      - clickhouse-data:/var/lib/clickhouse
    ulimits:
      nofile:
        soft: 262144
        hard: 262144

volumes:
  postgres-data:
  clickhouse-data:
```

```bash
# deploy.sh — Generate a secret key and start Plausible.
SECRET=$(openssl rand -base64 48)
echo "SECRET_KEY_BASE=$SECRET" >> .env
docker compose up -d
echo "Plausible is running at http://localhost:8000"
echo "Create your admin account at http://localhost:8000/register"
```

## Script Tag Installation

```html
<!-- index.html — Add the Plausible tracking script to your site.
     No cookies, no personal data, under 1KB gzipped. -->
<head>
  <!-- Basic pageview tracking -->
  <script defer data-domain="example.com"
    src="https://analytics.example.com/js/script.js"></script>

  <!-- With custom event tracking enabled -->
  <script defer data-domain="example.com"
    src="https://analytics.example.com/js/script.tagged-events.js"></script>

  <!-- With hash-based routing (SPAs) -->
  <script defer data-domain="example.com"
    src="https://analytics.example.com/js/script.hash.js"></script>

  <!-- Multiple extensions combined -->
  <script defer data-domain="example.com"
    src="https://analytics.example.com/js/script.hash.tagged-events.outbound-links.js"></script>
</head>
```

## Custom Event Goals

```javascript
// analytics.js — Track custom events for conversion goals in Plausible.
// Events appear in Goals section of the Plausible dashboard.

// Basic event
function trackSignup() {
  plausible('Signup')
}

// Event with custom properties (requires Business plan or self-hosted)
function trackPurchase(plan, amount) {
  plausible('Purchase', {
    props: {
      plan: plan,
      amount: amount,
    },
  })
}

// Revenue tracking
function trackRevenue(amount, currency) {
  plausible('Purchase', {
    revenue: { amount: amount, currency: currency },
    props: { plan: 'pro' },
  })
}

// Track form submissions
document.getElementById('contact-form').addEventListener('submit', function () {
  plausible('Contact Form Submission', {
    props: { source: document.referrer || 'direct' },
  })
})

// Track 404 pages (add script.file-downloads.js extension)
// Plausible auto-tracks file downloads and outbound links with extensions
```

## Next.js Integration

```typescript
// app/layout.tsx — Add Plausible to a Next.js App Router site.
// Uses next-plausible for automatic route change tracking in SPAs.
import PlausibleProvider from 'next-plausible'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <PlausibleProvider
          domain="example.com"
          customDomain="https://analytics.example.com"
          selfHosted={true}
          taggedEvents={true}
        />
      </head>
      <body>{children}</body>
    </html>
  )
}
```

```typescript
// components/pricing-button.tsx — Track custom events in React components.
// Uses the usePlausible hook for type-safe event tracking.
'use client'
import { usePlausible } from 'next-plausible'

type PlausibleEvents = {
  'Plan Selected': { plan: string; price: number }
  'CTA Clicked': { location: string }
}

export function PricingButton({ plan, price }: { plan: string; price: number }) {
  const plausible = usePlausible<PlausibleEvents>()

  return (
    <button
      onClick={() => plausible('Plan Selected', { props: { plan, price } })}
    >
      Choose {plan}
    </button>
  )
}
```

## Stats API

```python
# plausible_api.py — Query the Plausible Stats API for traffic data.
# Returns aggregate stats, timeseries, and breakdowns.
import requests
from datetime import date

PLAUSIBLE_HOST = 'https://analytics.example.com'
API_KEY = 'your-api-key'
SITE_ID = 'example.com'

headers = {'Authorization': f'Bearer {API_KEY}'}

def get_realtime_visitors() -> int:
    """Get current number of visitors on the site."""
    r = requests.get(
        f'{PLAUSIBLE_HOST}/api/v1/stats/realtime/visitors',
        headers=headers,
        params={'site_id': SITE_ID}
    )
    return r.json()

def get_aggregate(period: str = '30d', metrics: str = 'visitors,pageviews,bounce_rate,visit_duration') -> dict:
    """Get aggregate stats for a time period."""
    r = requests.get(
        f'{PLAUSIBLE_HOST}/api/v1/stats/aggregate',
        headers=headers,
        params={
            'site_id': SITE_ID,
            'period': period,
            'metrics': metrics,
        }
    )
    return r.json()['results']

def get_top_pages(period: str = '30d', limit: int = 10) -> list:
    """Get top pages by visitors."""
    r = requests.get(
        f'{PLAUSIBLE_HOST}/api/v1/stats/breakdown',
        headers=headers,
        params={
            'site_id': SITE_ID,
            'period': period,
            'property': 'event:page',
            'limit': limit,
            'metrics': 'visitors,pageviews',
        }
    )
    return r.json()['results']

def get_traffic_sources(period: str = '30d') -> list:
    """Get breakdown of traffic sources."""
    r = requests.get(
        f'{PLAUSIBLE_HOST}/api/v1/stats/breakdown',
        headers=headers,
        params={
            'site_id': SITE_ID,
            'period': period,
            'property': 'visit:source',
            'metrics': 'visitors,bounce_rate',
        }
    )
    return r.json()['results']
```

## Proxy Script Through Your Domain

```nginx
# nginx.conf — Proxy Plausible script through your domain.
# Avoids ad blockers and keeps all traffic first-party.
server {
    listen 443 ssl;
    server_name example.com;

    # Proxy the Plausible script
    location = /js/script.js {
        proxy_pass https://analytics.example.com/js/script.js;
        proxy_set_header Host analytics.example.com;
        proxy_ssl_server_name on;

        # Cache the script for 6 hours
        proxy_cache_valid 200 6h;
        proxy_cache_valid 404 1m;
    }

    # Proxy the event endpoint
    location = /api/event {
        proxy_pass https://analytics.example.com/api/event;
        proxy_set_header Host analytics.example.com;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_ssl_server_name on;
    }
}
```

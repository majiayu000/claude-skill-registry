---
name: UTM Tracking and Campaign Tracking
description: Adding UTM parameters to URLs to track marketing campaign effectiveness across channels, including UTM builder, attribution models, analytics integration, and campaign reporting.
---

# UTM Tracking and Campaign Tracking

> **Current Level:** Intermediate  
> **Domain:** Marketing / Analytics

---

## Overview

UTM (Urchin Tracking Module) parameters are tags added to URLs to track the effectiveness of marketing campaigns across various channels. They help identify where traffic is coming from and how users interact with your content.

---

## Core Concepts

### Table of Contents

1. [UTM Parameters Explained](#utm-parameters-explained)
2. [UTM Builder Implementation](#utm-builder-implementation)
3. [Tracking UTM Parameters](#tracking-utm-parameters)
4. [Storing Campaign Data](#storing-campaign-data)
5. [Attribution Models](#attribution-models)
6. [Analytics Integration](#analytics-integration)
7. [Link Shortening](#link-shortening)
8. [QR Code Generation](#qr-code-generation)
9. [Campaign Reporting](#campaign-reporting)
10. [Best Practices](#best-practices)
11. [Naming Conventions](#naming-conventions)

---

## UTM Parameters Explained

### Standard UTM Parameters

```typescript
interface UTMParameters {
  // Required parameters
  utm_source: string;    // Traffic source (e.g., google, facebook, newsletter)
  utm_medium: string;    // Marketing medium (e.g., cpc, banner, email)
  utm_campaign: string;  // Campaign name (e.g., spring_sale, product_launch)

  // Optional parameters
  utm_term?: string;      // Search terms (for paid search)
  utm_content?: string;  // Used to differentiate ads (e.g., text_link, image_ad)
  utm_id?: string;       // Campaign ID (Google Ads auto-populates this)
}

// UTM parameter validation
function validateUTM(params: Partial<UTMParameters>): {
  valid: boolean;
  errors: string[];
} {
  const errors: string[] = [];

  // Required parameters
  if (!params.utm_source) {
    errors.push('utm_source is required');
  }
  if (!params.utm_medium) {
    errors.push('utm_medium is required');
  }
  if (!params.utm_campaign) {
    errors.push('utm_campaign is required');
  }

  // Validate parameter format
  if (params.utm_source && params.utm_source.length > 100) {
    errors.push('utm_source must be less than 100 characters');
  }
  if (params.utm_medium && params.utm_medium.length > 100) {
    errors.push('utm_medium must be less than 100 characters');
  }
  if (params.utm_campaign && params.utm_campaign.length > 100) {
    errors.push('utm_campaign must be less than 100 characters');
  }

  return {
    valid: errors.length === 0,
    errors,
  };
}
```

### Common UTM Sources

```typescript
const UTM_SOURCES = {
  // Search engines
  GOOGLE: 'google',
  BING: 'bing',
  YAHOO: 'yahoo',
  DUCKDUCKGO: 'duckduckgo',

  // Social platforms
  FACEBOOK: 'facebook',
  INSTAGRAM: 'instagram',
  TWITTER: 'twitter',
  LINKEDIN: 'linkedin',
  TIKTOK: 'tiktok',
  YOUTUBE: 'youtube',
  PINTEREST: 'pinterest',

  // Email
  NEWSLETTER: 'newsletter',
  EMAIL_CAMPAIGN: 'email',
  EMAIL_BLAST: 'email_blast',

  // Direct
  DIRECT: 'direct',
  NONE: '(none)',

  // Referral
  REFERRAL: 'referral',

  // Other
  AFFILIATE: 'affiliate',
  PARTNER: 'partner',
  INFLUENCER: 'influencer',
  PR: 'pr',
  PAID: 'paid',
  ORGANIC: 'organic',
} as const;
```

### Common UTM Mediums

```typescript
const UTM_MEDIUMS = {
  // Paid advertising
  CPC: 'cpc',           // Cost per click
  PPC: 'ppc',           // Pay per click
  CPM: 'cpm',           // Cost per mille (thousand impressions)
  PAID_SEARCH: 'paid_search',
  DISPLAY: 'display',
  SOCIAL_PAID: 'social_paid',

  // Organic
  ORGANIC_SEARCH: 'organic_search',
  ORGANIC_SOCIAL: 'organic_social',
  REFERRAL: 'referral',

  // Email
  EMAIL: 'email',
  NEWSLETTER: 'newsletter',

  // Direct
  DIRECT: 'direct',
  NONE: '(none)',

  // Other
  AFFILIATE: 'affiliate',
  PARTNER: 'partner',
  WEBINAR: 'webinar',
  EVENT: 'event',
  PR: 'pr',
  QR_CODE: 'qr_code',
} as const;
```

---

## UTM Builder Implementation

### URL Builder

```typescript
class UTMBuilder {
  /**
   * Build URL with UTM parameters
   */
  static buildURL(
    baseURL: string,
    utmParams: UTMParameters
  ): string {
    const url = new URL(baseURL);

    // Add UTM parameters
    url.searchParams.set('utm_source', utmParams.utm_source);
    url.searchParams.set('utm_medium', utmParams.utm_medium);
    url.searchParams.set('utm_campaign', utmParams.utm_campaign);

    if (utmParams.utm_term) {
      url.searchParams.set('utm_term', utmParams.utm_term);
    }

    if (utmParams.utm_content) {
      url.searchParams.set('utm_content', utmParams.utm_content);
    }

    if (utmParams.utm_id) {
      url.searchParams.set('utm_id', utmParams.utm_id);
    }

    return url.toString();
  }

  /**
   * Build URL with campaign details
   */
  static buildCampaignURL(
    baseURL: string,
    campaign: {
      source: string;
      medium: string;
      name: string;
      term?: string;
      content?: string;
    }
  ): string {
    return this.buildURL(baseURL, {
      utm_source: campaign.source,
      utm_medium: campaign.medium,
      utm_campaign: campaign.name,
      utm_term: campaign.term,
      utm_content: campaign.content,
    });
  }

  /**
   * Build social media URLs
   */
  static buildSocialURL(
    platform: 'facebook' | 'twitter' | 'linkedin' | 'instagram',
    baseURL: string,
    campaign: string,
    content?: string
  ): string {
    const sourceMap = {
      facebook: UTM_SOURCES.FACEBOOK,
      twitter: UTM_SOURCES.TWITTER,
      linkedin: UTM_SOURCES.LINKEDIN,
      instagram: UTM_SOURCES.INSTAGRAM,
    };

    return this.buildCampaignURL(baseURL, {
      source: sourceMap[platform],
      medium: UTM_MEDIUMS.SOCIAL_PAID,
      name: campaign,
      content,
    });
  }

  /**
   * Build email campaign URLs
   */
  static buildEmailURL(
    baseURL: string,
    campaign: string,
    emailType: 'newsletter' | 'promotional' | 'transactional',
    content?: string
  ): string {
    return this.buildCampaignURL(baseURL, {
      source: UTM_SOURCES.NEWSLETTER,
      medium: UTM_MEDIUMS.EMAIL,
      name: campaign,
      content: content || emailType,
    });
  }

  /**
   * Build paid search URLs
   */
  static buildPaidSearchURL(
    baseURL: string,
    campaign: string,
    keyword: string,
    adGroup?: string
  ): string {
    return this.buildCampaignURL(baseURL, {
      source: UTM_SOURCES.GOOGLE,
      medium: UTM_MEDIUMS.CPC,
      name: campaign,
      term: keyword,
      content: adGroup,
    });
  }

  /**
   * Build QR code URLs
   */
  static buildQRCodeURL(
    baseURL: string,
    campaign: string,
    location?: string
  ): string {
    return this.buildCampaignURL(baseURL, {
      source: UTM_SOURCES.QR_CODE,
      medium: UTM_MEDIUMS.QR_CODE,
      name: campaign,
      content: location,
    });
  }
}

// Usage examples
const campaignURL = UTMBuilder.buildURL('https://example.com/product', {
  utm_source: 'google',
  utm_medium: 'cpc',
  utm_campaign: 'summer_sale',
  utm_term: 'running shoes',
  utm_content: 'text_ad',
});

const socialURL = UTMBuilder.buildSocialURL(
  'facebook',
  'https://example.com/product',
  'summer_sale',
  'image_ad'
);

const emailURL = UTMBuilder.buildEmailURL(
  'https://example.com/product',
  'summer_sale',
  'newsletter',
  'cta_button'
);
```

### React Component

```tsx
import React, { useState } from 'react';

interface UTMBuilderProps {
  baseURL: string;
  onURLGenerated: (url: string) => void;
}

const UTMBuilderComponent: React.FC<UTMBuilderProps> = ({
  baseURL,
  onURLGenerated,
}) => {
  const [params, setParams] = useState<Partial<UTMParameters>>({
    utm_source: '',
    utm_medium: '',
    utm_campaign: '',
    utm_term: '',
    utm_content: '',
  });

  const [generatedURL, setGeneratedURL] = useState('');
  const [errors, setErrors] = useState<string[]>([]);

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>
  ) => {
    const { name, value } = e.target;
    setParams(prev => ({ ...prev, [name]: value }));
  };

  const handleGenerate = () => {
    const validation = validateUTM(params);
    if (!validation.valid) {
      setErrors(validation.errors);
      return;
    }

    setErrors([]);
    const url = UTMBuilder.buildURL(baseURL, params as UTMParameters);
    setGeneratedURL(url);
    onURLGenerated(url);
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(generatedURL);
  };

  return (
    <div className="utm-builder">
      <h3>UTM URL Builder</h3>

      <div className="form-group">
        <label>Base URL</label>
        <input
          type="text"
          value={baseURL}
          readOnly
          className="base-url"
        />
      </div>

      <div className="form-group">
        <label>Source *</label>
        <select
          name="utm_source"
          value={params.utm_source}
          onChange={handleChange}
          required
        >
          <option value="">Select source...</option>
          <option value="google">Google</option>
          <option value="facebook">Facebook</option>
          <option value="twitter">Twitter</option>
          <option value="linkedin">LinkedIn</option>
          <option value="newsletter">Newsletter</option>
          <option value="email">Email</option>
        </select>
      </div>

      <div className="form-group">
        <label>Medium *</label>
        <select
          name="utm_medium"
          value={params.utm_medium}
          onChange={handleChange}
          required
        >
          <option value="">Select medium...</option>
          <option value="cpc">CPC (Cost Per Click)</option>
          <option value="ppc">PPC (Pay Per Click)</option>
          <option value="email">Email</option>
          <option value="social">Social</option>
          <option value="display">Display</option>
          <option value="referral">Referral</option>
        </select>
      </div>

      <div className="form-group">
        <label>Campaign Name *</label>
        <input
          type="text"
          name="utm_campaign"
          value={params.utm_campaign}
          onChange={handleChange}
          placeholder="e.g., summer_sale_2024"
          required
        />
      </div>

      <div className="form-group">
        <label>Term (Optional)</label>
        <input
          type="text"
          name="utm_term"
          value={params.utm_term}
          onChange={handleChange}
          placeholder="e.g., running shoes"
        />
      </div>

      <div className="form-group">
        <label>Content (Optional)</label>
        <input
          type="text"
          name="utm_content"
          value={params.utm_content}
          onChange={handleChange}
          placeholder="e.g., text_link, image_ad"
        />
      </div>

      {errors.length > 0 && (
        <div className="errors">
          {errors.map((error, i) => (
            <div key={i} className="error">{error}</div>
          ))}
        </div>
      )}

      <button onClick={handleGenerate}>Generate URL</button>

      {generatedURL && (
        <div className="generated-url">
          <label>Generated URL:</label>
          <input
            type="text"
            value={generatedURL}
            readOnly
          />
          <button onClick={handleCopy}>Copy</button>
        </div>
      )}
    </div>
  );
};

export default UTMBuilderComponent;
```

---

## Tracking UTM Parameters

### Server-Side Tracking

```typescript
import express from 'express';

const app = express();

// UTM tracking middleware
function trackUTM(req: express.Request, res: express.Response, next: express.NextFunction) {
  const { utm_source, utm_medium, utm_campaign, utm_term, utm_content, utm_id } = req.query;

  if (utm_source || utm_medium || utm_campaign) {
    // Store UTM parameters in session
    req.session.utm = {
      source: utm_source as string,
      medium: utm_medium as string,
      campaign: utm_campaign as string,
      term: utm_term as string,
      content: utm_content as string,
      id: utm_id as string,
      timestamp: new Date(),
    };

    // Store in cookie for persistence
    res.cookie('utm_params', JSON.stringify(req.session.utm), {
      maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
    });

    // Track analytics event
    analytics.track('UTM Parameters Detected', {
      source: utm_source,
      medium: utm_medium,
      campaign: utm_campaign,
      term: utm_term,
      content: utm_content,
      userId: req.session.userId,
    });
  }

  next();
}

app.use(trackUTM);

// Get UTM parameters for current user
app.get('/api/utm/current', (req, res) => {
  const utm = req.session.utm || parseUTMCookie(req.cookies.utm_params);
  res.json({ utm });
});

function parseUTMCookie(cookie: string): UTMParameters | null {
  try {
    return JSON.parse(cookie);
  } catch {
    return null;
  }
}
```

### Client-Side Tracking

```typescript
// UTM parameter parser
class UTMParser {
  /**
   * Parse UTM parameters from URL
   */
  static parseFromURL(url: string): UTMParameters | null {
    const urlObj = new URL(url);
    const params = urlObj.searchParams;

    const utmParams: Partial<UTMParameters> = {
      utm_source: params.get('utm_source') || undefined,
      utm_medium: params.get('utm_medium') || undefined,
      utm_campaign: params.get('utm_campaign') || undefined,
      utm_term: params.get('utm_term') || undefined,
      utm_content: params.get('utm_content') || undefined,
      utm_id: params.get('utm_id') || undefined,
    };

    // Check if any UTM parameters exist
    const hasUTM = Object.values(utmParams).some(v => v !== undefined);
    if (!hasUTM) return null;

    // Validate
    const validation = validateUTM(utmParams);
    if (!validation.valid) {
      console.warn('Invalid UTM parameters:', validation.errors);
      return null;
    }

    return utmParams as UTMParameters;
  }

  /**
   * Parse UTM parameters from current URL
   */
  static parseFromCurrentURL(): UTMParameters | null {
    return this.parseFromURL(window.location.href);
  }

  /**
   * Parse UTM parameters from query string
   */
  static parseFromQueryString(queryString: string): UTMParameters | null {
    const url = `https://example.com?${queryString}`;
    return this.parseFromURL(url);
  }

  /**
   * Store UTM parameters in localStorage
   */
  static storeUTM(utm: UTMParameters): void {
    const data = {
      ...utm,
      timestamp: new Date().toISOString(),
    };
    localStorage.setItem('utm_params', JSON.stringify(data));
  }

  /**
   * Get stored UTM parameters
   */
  static getStoredUTM(): (UTMParameters & { timestamp: string }) | null {
    try {
      const data = localStorage.getItem('utm_params');
      if (!data) return null;

      // Check if UTM is still valid (30 days)
      const parsed = JSON.parse(data);
      const age = Date.now() - new Date(parsed.timestamp).getTime();
      if (age > 30 * 24 * 60 * 60 * 1000) {
        localStorage.removeItem('utm_params');
        return null;
      }

      return parsed;
    } catch {
      return null;
    }
  }

  /**
   * Clear stored UTM parameters
   */
  static clearUTM(): void {
    localStorage.removeItem('utm_params');
  }

  /**
   * Initialize UTM tracking on page load
   */
  static initialize(): UTMParameters | null {
    // Check if UTM parameters exist in URL
    const utm = this.parseFromCurrentURL();

    if (utm) {
      // Store new UTM parameters
      this.storeUTM(utm);

      // Track analytics
      analytics.track('UTM Parameters Detected', utm);
    }

    return utm;
  }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
  UTMParser.initialize();
});

// Get UTM parameters for use in application
const currentUTM = UTMParser.getStoredUTM();
```

---

## Storing Campaign Data

### Database Schema

```sql
-- Campaigns table
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  utm_source VARCHAR(100),
  utm_medium VARCHAR(100),
  utm_campaign VARCHAR(100),
  utm_term VARCHAR(100),
  utm_content VARCHAR(100),
  utm_id VARCHAR(100),
  start_date TIMESTAMP,
  end_date TIMESTAMP,
  budget DECIMAL(10, 2),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Campaign visits
CREATE TABLE campaign_visits (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL,
  user_id UUID,
  session_id VARCHAR(255),
  utm_source VARCHAR(100),
  utm_medium VARCHAR(100),
  utm_campaign VARCHAR(100),
  utm_term VARCHAR(100),
  utm_content VARCHAR(100),
  utm_id VARCHAR(100),
  landing_page VARCHAR(500),
  referrer VARCHAR(500),
  ip_address INET,
  user_agent TEXT,
  device_type VARCHAR(50),
  browser VARCHAR(50),
  os VARCHAR(50),
  country VARCHAR(100),
  city VARCHAR(100),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Campaign conversions
CREATE TABLE campaign_conversions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  campaign_id UUID REFERENCES campaigns(id) ON DELETE SET NULL,
  visit_id UUID REFERENCES campaign_visits(id) ON DELETE SET NULL,
  user_id UUID,
  conversion_type VARCHAR(100),
  conversion_value DECIMAL(10, 2),
  page_url VARCHAR(500),
  created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_campaign_visits_campaign_id ON campaign_visits(campaign_id);
CREATE INDEX idx_campaign_visits_user_id ON campaign_visits(user_id);
CREATE INDEX idx_campaign_visits_session_id ON campaign_visits(session_id);
CREATE INDEX idx_campaign_visits_created_at ON campaign_visits(created_at);
CREATE INDEX idx_campaign_conversions_campaign_id ON campaign_conversions(campaign_id);
CREATE INDEX idx_campaign_conversions_user_id ON campaign_conversions(user_id);
CREATE INDEX idx_campaign_conversions_created_at ON campaign_conversions(created_at);
```

### Data Storage Implementation

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

interface CampaignVisitData {
  campaignId?: string;
  userId?: string;
  sessionId: string;
  utm: UTMParameters;
  landingPage: string;
  referrer?: string;
  ipAddress?: string;
  userAgent?: string;
}

class CampaignTracker {
  /**
   * Track campaign visit
   */
  async trackVisit(data: CampaignVisitData): Promise<string> {
    // Find or create campaign
    let campaignId = data.campaignId;

    if (!campaignId && data.utm) {
      campaignId = await this.findOrCreateCampaign(data.utm);
    }

    // Parse device info
    const deviceInfo = this.parseDeviceInfo(data.userAgent || '');

    // Store visit
    const visit = await prisma.campaignVisit.create({
      data: {
        campaignId,
        userId: data.userId,
        sessionId: data.sessionId,
        utmSource: data.utm.utm_source,
        utmMedium: data.utm.utm_medium,
        utmCampaign: data.utm.utm_campaign,
        utmTerm: data.utm.utm_term,
        utmContent: data.utm.utm_content,
        utmId: data.utm.utm_id,
        landingPage: data.landingPage,
        referrer: data.referrer,
        ipAddress: data.ipAddress,
        userAgent: data.userAgent,
        deviceType: deviceInfo.deviceType,
        browser: deviceInfo.browser,
        os: deviceInfo.os,
      },
    });

    return visit.id;
  }

  /**
   * Track conversion
   */
  async trackConversion(params: {
    visitId?: string;
    userId?: string;
    conversionType: string;
    conversionValue?: number;
    pageUrl: string;
  }): Promise<void> {
    // Find visit if not provided
    let visitId = params.visitId;

    if (!visitId && params.userId) {
      const latestVisit = await prisma.campaignVisit.findFirst({
        where: { userId: params.userId },
        orderBy: { createdAt: 'desc' },
      });
      visitId = latestVisit?.id;
    }

    await prisma.campaignConversion.create({
      data: {
        visitId,
        userId: params.userId,
        conversionType: params.conversionType,
        conversionValue: params.conversionValue,
        pageUrl: params.pageUrl,
      },
    });
  }

  /**
   * Find or create campaign
   */
  private async findOrCreateCampaign(utm: UTMParameters): Promise<string> {
    // Try to find existing campaign
    let campaign = await prisma.campaign.findFirst({
      where: {
        utmSource: utm.utm_source,
        utmMedium: utm.utm_medium,
        utmCampaign: utm.utm_campaign,
      },
    });

    if (campaign) {
      return campaign.id;
    }

    // Create new campaign
    campaign = await prisma.campaign.create({
      data: {
        name: utm.utm_campaign,
        utmSource: utm.utm_source,
        utmMedium: utm.utm_medium,
        utmCampaign: utm.utm_campaign,
        utmTerm: utm.utm_term,
        utmContent: utm.utm_content,
        utmId: utm.utm_id,
      },
    });

    return campaign.id;
  }

  /**
   * Parse device info from user agent
   */
  private parseDeviceInfo(userAgent: string): {
    deviceType: string;
    browser: string;
    os: string;
  } {
    // Simplified device detection
    const isMobile = /Mobile|Android|iPhone/i.test(userAgent);
    const isTablet = /Tablet|iPad/i.test(userAgent);

    const deviceType = isMobile ? 'mobile' : isTablet ? 'tablet' : 'desktop';

    let browser = 'unknown';
    if (/Chrome/i.test(userAgent)) browser = 'chrome';
    else if (/Firefox/i.test(userAgent)) browser = 'firefox';
    else if (/Safari/i.test(userAgent)) browser = 'safari';
    else if (/Edge/i.test(userAgent)) browser = 'edge';

    let os = 'unknown';
    if (/Windows/i.test(userAgent)) os = 'windows';
    else if (/Mac/i.test(userAgent)) os = 'macos';
    else if (/Linux/i.test(userAgent)) os = 'linux';
    else if (/Android/i.test(userAgent)) os = 'android';
    else if (/iOS/i.test(userAgent)) os = 'ios';

    return { deviceType, browser, os };
  }
}
```

---

## Attribution Models

### Attribution Model Types

```typescript
enum AttributionModel {
  FIRST_TOUCH = 'first_touch',
  LAST_TOUCH = 'last_touch',
  LINEAR = 'linear',
  TIME_DECAY = 'time_decay',
  POSITION_BASED = 'position_based',
  DATA_DRIVEN = 'data_driven',
}

interface AttributionResult {
  model: AttributionModel;
  campaignId: string;
  attributedValue: number;
  attributionPercentage: number;
}

class AttributionCalculator {
  /**
   * Calculate first touch attribution
   */
  static calculateFirstTouch(
    visits: CampaignVisit[],
    totalValue: number
  ): AttributionResult {
    const firstVisit = visits[0];
    return {
      model: AttributionModel.FIRST_TOUCH,
      campaignId: firstVisit.campaignId!,
      attributedValue: totalValue,
      attributionPercentage: 100,
    };
  }

  /**
   * Calculate last touch attribution
   */
  static calculateLastTouch(
    visits: CampaignVisit[],
    totalValue: number
  ): AttributionResult {
    const lastVisit = visits[visits.length - 1];
    return {
      model: AttributionModel.LAST_TOUCH,
      campaignId: lastVisit.campaignId!,
      attributedValue: totalValue,
      attributionPercentage: 100,
    };
  }

  /**
   * Calculate linear attribution
   */
  static calculateLinear(
    visits: CampaignVisit[],
    totalValue: number
  ): AttributionResult[] {
    const valuePerVisit = totalValue / visits.length;

    return visits.map(visit => ({
      model: AttributionModel.LINEAR,
      campaignId: visit.campaignId!,
      attributedValue: valuePerVisit,
      attributionPercentage: (1 / visits.length) * 100,
    }));
  }

  /**
   * Calculate time decay attribution
   */
  static calculateTimeDecay(
    visits: CampaignVisit[],
    totalValue: number,
    halfLifeDays: number = 7
  ): AttributionResult[] {
    const now = Date.now();
    const halfLifeMs = halfLifeDays * 24 * 60 * 60 * 1000;

    // Calculate decay factors
    const decayFactors = visits.map(visit => {
      const age = now - visit.createdAt.getTime();
      const decay = Math.pow(0.5, age / halfLifeMs);
      return decay;
    });

    const totalDecay = decayFactors.reduce((sum, d) => sum + d, 0);

    return visits.map((visit, i) => {
      const attributionPercentage = (decayFactors[i] / totalDecay) * 100;
      const attributedValue = (attributionPercentage / 100) * totalValue;

      return {
        model: AttributionModel.TIME_DECAY,
        campaignId: visit.campaignId!,
        attributedValue,
        attributionPercentage,
      };
    });
  }

  /**
   * Calculate position-based attribution (40/20/40)
   */
  static calculatePositionBased(
    visits: CampaignVisit[],
    totalValue: number
  ): AttributionResult[] {
    const results: AttributionResult[] = [];

    for (let i = 0; i < visits.length; i++) {
      let attributionPercentage: number;

      if (i === 0 || i === visits.length - 1) {
        attributionPercentage = 40; // First and last touch get 40%
      } else {
        attributionPercentage = 20 / Math.max(visits.length - 2, 1); // Middle touches share 20%
      }

      results.push({
        model: AttributionModel.POSITION_BASED,
        campaignId: visits[i].campaignId!,
        attributedValue: (attributionPercentage / 100) * totalValue,
        attributionPercentage,
      });
    }

    return results;
  }
}
```

---

## Analytics Integration

### Google Analytics 4 Integration

```typescript
// Track UTM parameters with GA4
function trackUTMWithGA4(utm: UTMParameters): void {
  gtag('event', 'page_view', {
    campaign_source: utm.utm_source,
    campaign_medium: utm.utm_medium,
    campaign_name: utm.utm_campaign,
    campaign_term: utm.utm_term,
    campaign_content: utm.utm_content,
    campaign_id: utm.utm_id,
  });
}

// Track conversion with campaign data
function trackConversionWithGA4(
  conversionType: string,
  value?: number,
  utm?: UTMParameters
): void {
  gtag('event', 'conversion', {
    conversion_type: conversionType,
    value,
    currency: 'USD',
    campaign_source: utm?.utm_source,
    campaign_medium: utm?.utm_medium,
    campaign_name: utm?.utm_campaign,
  });
}

// Initialize GA4 with custom parameters
function initializeGA4(measurementId: string): void {
  gtag('js', new Date());
  gtag('config', measurementId, {
    campaign_source: UTMParser.getStoredUTM()?.utm_source,
    campaign_medium: UTMParser.getStoredUTM()?.utm_medium,
    campaign_name: UTMParser.getStoredUTM()?.utm_campaign,
  });
}
```

### Mixpanel Integration

```typescript
// Track UTM parameters with Mixpanel
function trackUTMWithMixpanel(utm: UTMParameters): void {
  mixpanel.people.set({
    'utm_source': utm.utm_source,
    'utm_medium': utm.utm_medium,
    'utm_campaign': utm.utm_campaign,
    'utm_term': utm.utm_term,
    'utm_content': utm.utm_content,
  });

  mixpanel.track('Campaign Visit', {
    'utm_source': utm.utm_source,
    'utm_medium': utm.utm_medium,
    'utm_campaign': utm.utm_campaign,
    'utm_term': utm.utm_term,
    'utm_content': utm.utm_content,
  });
}

// Track conversion with campaign data
function trackConversionWithMixpanel(
  conversionType: string,
  value?: number,
  utm?: UTMParameters
): void {
  mixpanel.track('Conversion', {
    'conversion_type': conversionType,
    'value': value,
    'utm_source': utm?.utm_source,
    'utm_medium': utm?.utm_medium,
    'utm_campaign': utm?.utm_campaign,
  });
}
```

---

## Link Shortening

### Bitly Integration

```typescript
// npm install bitly
import BitlyClient from 'bitly';

const bitly = new BitlyClient(process.env.BITLY_API_KEY!);

async function shortenURL(
  longURL: string,
  title?: string,
  tags?: string[]
): Promise<string> {
  const response = await bitly.shorten(longURL);

  if (title || tags) {
    await bitly.updateBitlink(response.link, {
      title,
      tags,
    });
  }

  return response.link;
}

// Shorten UTM URL
async function shortenUTMURL(
  baseURL: string,
  utm: UTMParameters,
  campaignName?: string
): Promise<string> {
  const longURL = UTMBuilder.buildURL(baseURL, utm);
  const shortURL = await shortenURL(longURL, campaignName);

  return shortURL;
}

// Get click analytics for short link
async function getLinkClicks(bitlink: string): Promise<{
  clicks: number;
  countries: Record<string, number>;
  referrers: Record<string, number>;
}> {
  const response = await bitly.clicks(bitlink);
  const countryResponse = await bitly.countriesByClicks(bitlink);
  const referrerResponse = await bitly.referringNetworks(bitlink);

  return {
    clicks: response.clicks,
    countries: countryResponse.countries,
    referrers: referrerResponse.referring_networks,
  };
}
```

### Custom Short URL Implementation

```typescript
import crypto from 'crypto';

class URLShortener {
  constructor(private prisma: PrismaClient) {}

  /**
   * Create short URL
   */
  async createShortURL(params: {
    longURL: string;
    customAlias?: string;
    expiresAt?: Date;
    userId?: string;
  }): Promise<string> {
    // Generate or use custom alias
    const alias = params.customAlias || this.generateAlias();

    // Store in database
    await this.prisma.shortURL.create({
      data: {
        alias,
        longURL: params.longURL,
        expiresAt: params.expiresAt,
        userId: params.userId,
        clicks: 0,
      },
    });

    return `${process.env.BASE_URL}/${alias}`;
  }

  /**
   * Get original URL from short URL
   */
  async getLongURL(alias: string): Promise<string | null> {
    const shortURL = await this.prisma.shortURL.findUnique({
      where: { alias },
    });

    if (!shortURL) {
      return null;
    }

    // Check if expired
    if (shortURL.expiresAt && shortURL.expiresAt < new Date()) {
      return null;
    }

    // Increment click count
    await this.prisma.shortURL.update({
      where: { alias },
      data: { clicks: { increment: 1 } },
    });

    return shortURL.longURL;
  }

  /**
   * Generate random alias
   */
  private generateAlias(length: number = 6): string {
    return crypto
      .randomBytes(Math.ceil(length / 2))
      .toString('hex')
      .slice(0, length);
  }

  /**
   * Get URL analytics
   */
  async getAnalytics(alias: string): Promise<{
    clicks: number;
    createdAt: Date;
    lastClickedAt?: Date;
  }> {
    const shortURL = await this.prisma.shortURL.findUnique({
      where: { alias },
    });

    if (!shortURL) {
      throw new Error('Short URL not found');
    }

    return {
      clicks: shortURL.clicks,
      createdAt: shortURL.createdAt,
      lastClickedAt: shortURL.lastClickedAt || undefined,
    };
  }
}

// Express routes
const shortener = new URLShortener(prisma);

app.post('/api/shorten', express.json(), async (req, res) => {
  const { longURL, customAlias, expiresAt } = req.body;

  try {
    const shortURL = await shortener.createShortURL({
      longURL,
      customAlias,
      expiresAt: expiresAt ? new Date(expiresAt) : undefined,
    });
    res.json({ shortURL });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create short URL' });
  }
});

app.get('/:alias', async (req, res) => {
  const { alias } = req.params;

  const longURL = await shortener.getLongURL(alias);

  if (!longURL) {
    return res.status(404).send('URL not found');
  }

  res.redirect(longURL);
});
```

---

## QR Code Generation

### QR Code Library Integration

```typescript
// npm install qrcode
import QRCode from 'qrcode';

interface QRCodeOptions {
  width?: number;
  margin?: number;
  color?: {
    dark?: string;
    light?: string;
  };
  errorCorrectionLevel?: 'L' | 'M' | 'Q' | 'H';
}

/**
 * Generate QR code as data URL
 */
async function generateQRCodeDataURL(
  url: string,
  options: QRCodeOptions = {}
): Promise<string> {
  return await QRCode.toDataURL(url, {
    width: options.width || 300,
    margin: options.margin || 2,
    color: {
      dark: options.color?.dark || '#000000',
      light: options.color?.light || '#FFFFFF',
    },
    errorCorrectionLevel: options.errorCorrectionLevel || 'M',
  });
}

/**
 * Generate QR code as buffer
 */
async function generateQRCodeBuffer(
  url: string,
  options: QRCodeOptions = {}
): Promise<Buffer> {
  return await QRCode.toBuffer(url, {
    width: options.width || 300,
    margin: options.margin || 2,
    color: {
      dark: options.color?.dark || '#000000',
      light: options.color?.light || '#FFFFFF',
    },
    errorCorrectionLevel: options.errorCorrectionLevel || 'M',
  });
}

/**
 * Generate QR code for UTM campaign
 */
async function generateCampaignQRCode(
  baseURL: string,
  campaign: {
    source: string;
    medium: string;
    name: string;
    location?: string;
  },
  options?: QRCodeOptions
): Promise<string> {
  const url = UTMBuilder.buildQRCodeURL(
    baseURL,
    campaign.name,
    campaign.location
  );

  return await generateQRCodeDataURL(url, options);
}

/**
 * Generate batch QR codes
 */
async function generateBatchQRCodes(
  baseURL: string,
  campaigns: Array<{
    source: string;
    medium: string;
    name: string;
    location?: string;
  }>,
  options?: QRCodeOptions
): Promise<Array<{ campaign: string; qrCode: string }>> {
  const results = [];

  for (const campaign of campaigns) {
    const qrCode = await generateCampaignQRCode(baseURL, campaign, options);
    results.push({ campaign: campaign.name, qrCode });
  }

  return results;
}
```

### React QR Code Component

```tsx
import React, { useState, useEffect } from 'react';
import QRCode from 'qrcode.react';

interface QRCodeGeneratorProps {
  baseURL: string;
  campaign: {
    source: string;
    medium: string;
    name: string;
    location?: string;
  };
  size?: number;
  onGenerated?: (url: string) => void;
}

const QRCodeGenerator: React.FC<QRCodeGeneratorProps> = ({
  baseURL,
  campaign,
  size = 300,
  onGenerated,
}) => {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const generate = async () => {
      const generatedURL = UTMBuilder.buildQRCodeURL(
        baseURL,
        campaign.name,
        campaign.location
      );
      setUrl(generatedURL);
      setLoading(false);
      onGenerated?.(generatedURL);
    };

    generate();
  }, [baseURL, campaign]);

  const handleDownload = async () => {
    const canvas = document.querySelector('canvas') as HTMLCanvasElement;
    if (canvas) {
      const dataUrl = canvas.toDataURL('image/png');
      const link = document.createElement('a');
      link.download = `qr-${campaign.name}.png`;
      link.href = dataUrl;
      link.click();
    }
  };

  if (loading) {
    return <div>Loading QR code...</div>;
  }

  return (
    <div className="qr-code-generator">
      <QRCode value={url} size={size} />
      <button onClick={handleDownload}>Download QR Code</button>
      <div className="qr-url">
        <label>URL:</label>
        <input type="text" value={url} readOnly />
      </div>
    </div>
  );
};

export default QRCodeGenerator;
```

---

## Campaign Reporting

### Campaign Metrics

```typescript
interface CampaignMetrics {
  campaignId: string;
  campaignName: string;
  visits: number;
  uniqueVisitors: number;
  conversions: number;
  conversionRate: number;
  totalValue: number;
  averageOrderValue: number;
  costPerVisit?: number;
  costPerConversion?: number;
  returnOnAdSpend?: number;
}

class CampaignReporter {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get campaign metrics
   */
  async getCampaignMetrics(
    campaignId: string,
    startDate?: Date,
    endDate?: Date
  ): Promise<CampaignMetrics> {
    const where: any = { campaignId };

    if (startDate || endDate) {
      where.createdAt = {};
      if (startDate) where.createdAt.gte = startDate;
      if (endDate) where.createdAt.lte = endDate;
    }

    const [visits, uniqueVisitors, conversions] = await Promise.all([
      this.prisma.campaignVisit.count({ where }),
      this.prisma.campaignVisit.groupBy({
        by: ['userId'],
        where: { ...where, userId: { not: null } },
      }).then(groups => groups.length),
      this.prisma.campaignConversion.findMany({
        where: { campaignId },
      }),
    ]);

    const totalValue = conversions.reduce((sum, c) => sum + (c.conversionValue || 0), 0);
    const conversionRate = visits > 0 ? (conversions.length / visits) * 100 : 0;
    const averageOrderValue = conversions.length > 0 ? totalValue / conversions.length : 0;

    return {
      campaignId,
      campaignName: await this.getCampaignName(campaignId),
      visits,
      uniqueVisitors,
      conversions: conversions.length,
      conversionRate,
      totalValue,
      averageOrderValue,
    };
  }

  /**
   * Get campaign comparison
   */
  async compareCampaigns(
    campaignIds: string[],
    startDate?: Date,
    endDate?: Date
  ): Promise<CampaignMetrics[]> {
    const metrics = await Promise.all(
      campaignIds.map(id => this.getCampaignMetrics(id, startDate, endDate))
    );

    return metrics.sort((a, b) => b.totalValue - a.totalValue);
  }

  /**
   * Get campaign trends
   */
  async getCampaignTrends(
    campaignId: string,
    period: 'day' | 'week' | 'month',
    startDate: Date,
    endDate: Date
  ): Promise<Array<{
    date: Date;
    visits: number;
    conversions: number;
    revenue: number;
  }>> {
    const visits = await this.prisma.campaignVisit.findMany({
      where: {
        campaignId,
        createdAt: { gte: startDate, lte: endDate },
      },
      orderBy: { createdAt: 'asc' },
    });

    const conversions = await this.prisma.campaignConversion.findMany({
      where: {
        campaignId,
        createdAt: { gte: startDate, lte: endDate },
      },
      orderBy: { createdAt: 'asc' },
    });

    // Group by period
    const grouped = new Map<string, { visits: number; conversions: number; revenue: number }>();

    for (const visit of visits) {
      const key = this.getDateKey(visit.createdAt, period);
      const existing = grouped.get(key) || { visits: 0, conversions: 0, revenue: 0 };
      existing.visits++;
      grouped.set(key, existing);
    }

    for (const conversion of conversions) {
      const key = this.getDateKey(conversion.createdAt, period);
      const existing = grouped.get(key) || { visits: 0, conversions: 0, revenue: 0 };
      existing.conversions++;
      existing.revenue += conversion.conversionValue || 0;
      grouped.set(key, existing);
    }

    return Array.from(grouped.entries()).map(([date, data]) => ({
      date: this.parseDateKey(date),
      ...data,
    }));
  }

  private async getCampaignName(campaignId: string): Promise<string> {
    const campaign = await this.prisma.campaign.findUnique({
      where: { id: campaignId },
    });
    return campaign?.name || 'Unknown';
  }

  private getDateKey(date: Date, period: string): string {
    const d = new Date(date);
    switch (period) {
      case 'day':
        return d.toISOString().split('T')[0];
      case 'week':
        const weekStart = new Date(d);
        weekStart.setDate(d.getDate() - d.getDay());
        return weekStart.toISOString().split('T')[0];
      case 'month':
        return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}`;
      default:
        return d.toISOString().split('T')[0];
    }
  }

  private parseDateKey(key: string): Date {
    return new Date(key);
  }
}
```

---

## Best Practices

### UTM Parameter Guidelines

```typescript
// UTM parameter validation rules
const UTM_VALIDATION_RULES = {
  // Use lowercase, underscores, and hyphens only
  format: /^[a-z0-9_-]+$/,

  // Maximum lengths
  maxLength: {
    source: 100,
    medium: 100,
    campaign: 100,
    term: 100,
    content: 100,
  },

  // Reserved words to avoid
  reserved: ['direct', 'none', 'referral', 'organic'],
};

function sanitizeUTMValue(value: string, paramType: keyof typeof UTM_VALIDATION_RULES.maxLength): string {
  // Convert to lowercase
  let sanitized = value.toLowerCase();

  // Replace spaces with underscores
  sanitized = sanitized.replace(/\s+/g, '_');

  // Remove special characters
  sanitized = sanitized.replace(/[^a-z0-9_-]/g, '');

  // Truncate to max length
  const maxLength = UTM_VALIDATION_RULES.maxLength[paramType];
  if (sanitized.length > maxLength) {
    sanitized = sanitized.substring(0, maxLength);
  }

  return sanitized;
}

// Example usage
const sanitizedCampaign = sanitizeUTMValue('Summer Sale 2024!', 'campaign');
// Result: 'summer_sale_2024'
```

### Tracking Best Practices

```typescript
// Consistent tracking implementation
class UTMBestPractices {
  /**
   * Always use consistent UTM parameters
   */
  static ensureConsistency(utm: UTMParameters): UTMParameters {
    return {
      utm_source: this.sanitizeValue(utm.utm_source),
      utm_medium: this.sanitizeValue(utm.utm_medium),
      utm_campaign: this.sanitizeValue(utm.utm_campaign),
      utm_term: utm.utm_term ? this.sanitizeValue(utm.utm_term) : undefined,
      utm_content: utm.utm_content ? this.sanitizeValue(utm.utm_content) : undefined,
    };
  }

  private static sanitizeValue(value: string): string {
    return value.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_-]/g, '');
  }

  /**
   * Track first touchpoint only
   */
  static shouldTrackFirstTouch(userId: string): boolean {
    // Check if user already has UTM data
    return !this.hasExistingUTMData(userId);
  }

  private static hasExistingUTMData(userId: string): boolean {
    // Implement check for existing UTM data
    return false;
  }

  /**
   * Use consistent campaign naming
   */
  static generateCampaignName(
    type: string,
    year: number,
    season?: string,
    variant?: string
  ): string {
    const parts = [type, year];

    if (season) {
      parts.push(season);
    }

    if (variant) {
      parts.push(variant);
    }

    return parts.join('_').toLowerCase();
  }
}

// Example campaign names
UTMBestPractices.generateCampaignName('sale', 2024, 'summer');
// Result: 'sale_2024_summer'

UTMBestPractices.generateCampaignName('launch', 2024, 'q1', 'beta');
// Result: 'launch_2024_q1_beta'
```

---

## Naming Conventions

### Campaign Naming Template

```typescript
interface CampaignNamingTemplate {
  channel: string;
  campaignType: string;
  year: number;
  quarter?: string;
  month?: string;
  season?: string;
  variant?: string;
  audience?: string;
}

class CampaignNamer {
  /**
   * Generate campaign name using template
   */
  static generateName(template: CampaignNamingTemplate): string {
    const parts: string[] = [];

    // Channel
    parts.push(template.channel);

    // Campaign type
    parts.push(template.campaignType);

    // Time period
    if (template.quarter) {
      parts.push(template.year.toString());
      parts.push(`q${template.quarter}`);
    } else if (template.season) {
      parts.push(template.year.toString());
      parts.push(template.season);
    } else if (template.month) {
      parts.push(template.year.toString());
      parts.push(template.month);
    } else {
      parts.push(template.year.toString());
    }

    // Variant
    if (template.variant) {
      parts.push(template.variant);
    }

    // Audience
    if (template.audience) {
      parts.push(template.audience);
    }

    return parts.join('_').toLowerCase();
  }

  /**
   * Parse campaign name
   */
  static parseName(name: string): CampaignNamingTemplate {
    const parts = name.split('_');

    return {
      channel: parts[0],
      campaignType: parts[1],
      year: parseInt(parts[2]),
      quarter: parts[3]?.startsWith('q') ? parts[3][1] : undefined,
      season: parts[3] && !parts[3].startsWith('q') ? parts[3] : undefined,
      variant: parts[4],
      audience: parts[5],
    };
  }
}

// Example usage
const campaignName = CampaignNamer.generateName({
  channel: 'facebook',
  campaignType: 'retargeting',
  year: 2024,
  quarter: '1',
  variant: 'video',
  audience: 'new_users',
});
// Result: 'facebook_retargeting_2024_q1_video_new_users'
```

---

---

## Quick Start

### UTM Builder

```typescript
interface UTMParams {
  source: string      // utm_source
  medium: string      // utm_medium
  campaign: string    // utm_campaign
  term?: string       // utm_term
  content?: string    // utm_content
}

function buildUTMUrl(baseUrl: string, params: UTMParams): string {
  const url = new URL(baseUrl)
  url.searchParams.set('utm_source', params.source)
  url.searchParams.set('utm_medium', params.medium)
  url.searchParams.set('utm_campaign', params.campaign)
  if (params.term) url.searchParams.set('utm_term', params.term)
  if (params.content) url.searchParams.set('utm_content', params.content)
  return url.toString()
}

// Usage
const url = buildUTMUrl('https://example.com', {
  source: 'facebook',
  medium: 'social',
  campaign: 'summer-sale'
})
```

### Track UTM Parameters

```typescript
// Extract UTM from URL
function extractUTM(url: string): UTMParams | null {
  const urlObj = new URL(url)
  const source = urlObj.searchParams.get('utm_source')
  const medium = urlObj.searchParams.get('utm_medium')
  const campaign = urlObj.searchParams.get('utm_campaign')
  
  if (!source || !medium || !campaign) {
    return null
  }
  
  return {
    source,
    medium,
    campaign,
    term: urlObj.searchParams.get('utm_term') || undefined,
    content: urlObj.searchParams.get('utm_content') || undefined
  }
}

// Store in session
sessionStorage.setItem('utm_params', JSON.stringify(extractUTM(window.location.href)))
```

---

## Production Checklist

- [ ] **UTM Builder**: UTM URL builder implemented
- [ ] **Parameter Tracking**: Track UTM parameters
- [ ] **Storage**: Store UTM data
- [ ] **Attribution**: Attribution model defined
- [ ] **Analytics Integration**: Integrate with analytics
- [ ] **Link Shortening**: Link shortening if needed
- [ ] **QR Codes**: QR code generation
- [ ] **Reporting**: Campaign reporting
- [ ] **Naming Convention**: Consistent naming convention
- [ ] **Documentation**: Document UTM structure
- [ ] **Testing**: Test UTM tracking
- [ ] **Monitoring**: Monitor campaign performance

---

## Anti-patterns

### ❌ Don't: Inconsistent Naming

```typescript
// ❌ Bad - Inconsistent
utm_source=facebook
utm_source=Facebook
utm_source=FB
// Same source, different names!
```

```typescript
// ✅ Good - Consistent
utm_source=facebook  // Always lowercase
utm_medium=social   // Always lowercase
utm_campaign=summer-sale  // Always kebab-case
```

### ❌ Don't: No Attribution

```markdown
# ❌ Bad - No attribution model
All conversions attributed to last click
# Ignores other touchpoints!
```

```markdown
# ✅ Good - Multi-touch attribution
First touch: 20%
Middle touch: 30%
Last touch: 50%
# Recognizes all touchpoints
```

---

## Integration Points

- **Campaign Management** (`28-marketing-integration/campaign-management/`) - Campaign tracking
- **Analytics** (`23-business-analytics/`) - Campaign analytics
- **Marketing Automation** (`28-marketing-integration/marketing-automation/`) - Automated campaigns

---

## Further Reading

- [UTM Parameters Guide](https://support.google.com/analytics/answer/1033863)
- [Campaign Attribution](https://www.optimizely.com/optimization-glossary/attribution-modeling/)

## Resources

- [Google Analytics Campaign URL Builder](https://ga-dev-tools.google/ga4/campaign-url-builder/)
- [UTM.io](https://utms.io/)
- [Bitly API Documentation](https://dev.bitly.com/api-reference)
- [QRCode.js Library](https://github.com/davidshimjs/qrcodejs)

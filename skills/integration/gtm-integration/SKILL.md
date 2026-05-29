---
name: gtm-integration
description: Generic Google Tag Manager integration patterns for any project. Use when setting up GTM, managing tags/triggers, or implementing conversion tracking. Framework for project-specific implementations.
---

# GTM Integration Framework

Generic patterns for Google Tag Manager integration across any project.

## When to Use

- Setting up GTM from scratch
- Adding conversion tracking
- Managing tags, triggers, and variables
- Integrating with analytics platforms
- Implementing event tracking

## NOT Project-Specific

This is a **framework skill** providing generic patterns. For project-specific implementations:
- Create implementation skill in your project
- Reference this framework with `extends: "analytics-framework/gtm-integration"`
- Add project-specific configuration via skill.config.json

## Core Concepts

### GTM Architecture

```
GTM Container
├── Tags (what fires)
│   ├── GA4 Event
│   ├── Google Ads Conversion
│   ├── PostHog Event
│   └── Facebook Pixel
├── Triggers (when to fire)
│   ├── Page View
│   ├── Click
│   ├── Form Submission
│   └── Custom Event
└── Variables (data to pass)
    ├── Data Layer Variables
    ├── JavaScript Variables
    └── Constants
```

### Event Standardization Pattern

**Always use standardized event names across platforms:**

```typescript
// Define standard events
export const EVENTS = {
  PAGE_VIEW: 'page_view',
  FORM_STARTED: 'form_started',
  FORM_SUBMITTED: 'form_submitted',
  CONVERSION: 'conversion'
};

// Use same event name everywhere
dataLayer.push({ event: EVENTS.FORM_SUBMITTED, formId: 'contact' });
```

## Implementation Patterns

### 1. Setup @akson Analytics Package

```bash
npm install @akson/cortex-analytics @akson/cortex-gtm @akson/cortex-utilities
```

### 2. Create gtm.config.yaml

```yaml
container:
  id: ${GTM_CONTAINER_ID}
  workspace:
    name: "Default Workspace"

variables:
  - name: "GA4 Measurement ID"
    type: "constant"
    value: ${GA4_MEASUREMENT_ID}

  - name: "dataLayer Variable - Event"
    type: "dataLayer"
    key: "event"

tags:
  - name: "GA4 Configuration"
    type: "gaa"  # Google Analytics 4
    firing_triggers:
      - "All Pages"
    fields:
      measurementId: "{{GA4 Measurement ID}}"

  - name: "GA4 Event - Form Submission"
    type: "gaawe"  # GA4 Event
    firing_triggers:
      - "Form Submission Trigger"
    fields:
      eventName: "form_submitted"
      eventParameters:
        - name: "form_id"
          value: "{{Form ID Variable}}"

triggers:
  - name: "All Pages"
    type: "pageview"

  - name: "Form Submission Trigger"
    type: "customEvent"
    customEventFilter:
      - type: "equals"
        arg0: "{{Event}}"
        arg1: "form_submitted"
```

### 3. Create Service Account

```bash
# 1. Go to Google Cloud Console
# 2. Create service account with GTM permissions
# 3. Download JSON key
# 4. Store securely (1Password, .env, config/)

# Never commit service account keys!
# Add to .gitignore:
echo "config/*-automation.json" >> .gitignore
```

### 4. CLI Operations

```bash
# Validate configuration
npm run gtm:validate

# Preview changes (dry run)
npm run gtm:plan

# Apply changes
npm run gtm:apply

# Check status
npm run gtm:status

# Backup current state
npm run gtm:backup
```

### 5. Event Tracking Pattern

```typescript
// Client-side event tracking
export function trackEvent(eventName: string, params?: Record<string, any>) {
  if (typeof window !== 'undefined' && window.dataLayer) {
    window.dataLayer.push({
      event: eventName,
      ...params,
      timestamp: Date.now()
    });
  }
}

// Usage
trackEvent('form_submitted', {
  formId: 'contact',
  formType: 'lead_generation'
});
```

## Conversion Tracking Pattern

### Google Ads Conversion Tag

```yaml
tags:
  - name: "Google Ads Conversion - Form Submit"
    type: "awct"  # AdWords Conversion Tracking
    firing_triggers:
      - "Form Submission Trigger"
    fields:
      conversionId: ${CONVERSION_ID}
      conversionLabel: ${CONVERSION_LABEL}
      remarketingOnly: false
```

### Conversion Linker (Required)

```yaml
tags:
  - name: "Conversion Linker"
    type: "gclidw"  # Google Click ID Writer
    firing_triggers:
      - "All Pages"
```

## Multi-Platform Integration

### Pattern: Same Event, Multiple Platforms

```typescript
function trackConversion(eventName: string, data: any) {
  // GTM/GA4
  dataLayer.push({ event: eventName, ...data });

  // PostHog
  if (window.posthog) {
    window.posthog.capture(eventName, data);
  }

  // Facebook Pixel
  if (window.fbq) {
    window.fbq('trackCustom', eventName, data);
  }
}
```

## Testing & Debugging

### GTM Preview Mode

1. Open GTM container
2. Click "Preview"
3. Enter your website URL
4. Test event firing in Tag Assistant

### Debug Console

```typescript
// Enable dataLayer debugging
window.dataLayer = window.dataLayer || [];
window.dataLayer.push({ event: 'gtm.js', 'gtm.start': new Date().getTime() });

// Log all dataLayer pushes
const originalPush = window.dataLayer.push;
window.dataLayer.push = function(...args) {
  console.log('[DataLayer]', args);
  return originalPush.apply(this, args);
};
```

## Configuration Requirements

**Environment Variables:**
- `GTM_CONTAINER_ID` - Container ID (e.g., GTM-XXXXXXX)
- `GA4_MEASUREMENT_ID` - GA4 property ID (e.g., G-XXXXXXXXXX)
- `CONVERSION_ID` - Google Ads conversion ID
- `CONVERSION_LABEL` - Conversion label for specific action

**Required Files:**
- `config/gtm-api-automation.json` - Service account key
- `gtm.config.yaml` - GTM configuration

**Service Account Permissions:**
- `tagmanager.accounts.get`
- `tagmanager.containers.get`
- `tagmanager.versions.update`
- `tagmanager.containers.versions.publish`

## Key Rules

### DO:
- Use standardized event names
- Test in GTM preview mode before publishing
- Create backups before major changes
- Validate configuration with `gtm:plan`
- Use environment variables for IDs
- Document all custom events

### DON'T:
- Hardcode container IDs or conversion labels
- Mix event naming conventions
- Deploy without testing
- Skip validation step
- Commit service account keys
- Create duplicate tags for same event

## Package Scripts

Add to your `package.json`:

```json
{
  "scripts": {
    "gtm:validate": "cortex-gtm validate",
    "gtm:plan": "cortex-gtm plan",
    "gtm:apply": "cortex-gtm apply",
    "gtm:status": "cortex-gtm status",
    "gtm:backup": "cortex-gtm backup"
  }
}
```

## Resources

- **@akson/cortex-gtm**: GTM management package
- **@akson/cortex-analytics**: Unified analytics CLI
- **@akson/cortex-utilities**: Standardized event constants
- **GTM API Docs**: https://developers.google.com/tag-platform/tag-manager/api/v2
- **GA4 Event Reference**: https://support.google.com/analytics/answer/9267735

## Example Implementations

See project-specific skills that extend this framework:
- `myarmy-skills/gtm-myarmy` - MyArmy landing page implementation
- Your implementation here!

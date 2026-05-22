---
name: lead-scoring-myarmy
extends: lead-generation-framework/lead-scoring-system
description: MyArmy lead scoring for Swiss military custom badge manufacturing leads
---

# MyArmy Lead Scoring Implementation

Extends `lead-generation-framework/lead-scoring-system` with Swiss military market lead funnel.

## Lead Funnel

MyArmy targets **Swiss Army personnel** for custom military badges (funktionsabzeichen, truppenabzeichen). The funnel differs from standard B2C due to:
- High-value custom orders (CHF 500-5000)
- B2B2C model (unit commanders order for their teams)
- Long sales cycle (2-6 weeks from inquiry to order)
- WhatsApp as primary communication channel

### Scoring Model (1-100)

| Score | Stage | Actions | Expected Conversion |
|-------|-------|---------|---------------------|
| **0-20** | **Cold** | Page view, organic search arrival | 10% → Warm |
| **21-40** | **Warm** | Product page view, design gallery browsing | 25% → Hot |
| **41-60** | **Hot** | Contact form started, pricing inquiry | 40% → Very Hot |
| **61-80** | **Very Hot** | WhatsApp contact, quote request | 60% → Conversion |
| **81-100** | **Conversion** | Order placed, payment completed | 100% Complete |

## Scoring Events

```typescript
export const MYARMY_SCORING_EVENTS = {
  // Awareness (0-20)
  LANDING_PAGE_VIEW: { score: 5, event: 'page_view' },
  ORGANIC_MILITARY_KEYWORD: { score: 10, event: 'organic_military_arrival' },
  SOCIAL_MEDIA_ARRIVAL: { score: 8, event: 'social_arrival' },

  // Interest (21-40)
  FUNKTIONSABZEICHEN_VIEW: { score: 15, event: 'product_view_funktionsabzeichen' },
  CUSTOM_DESIGN_GALLERY: { score: 20, event: 'design_gallery_viewed' },
  PRICING_PAGE_VIEW: { score: 25, event: 'pricing_viewed' },
  REKRUTENSCHULE_CONTENT: { score: 18, event: 'rekrutenschule_content_viewed' },

  // Consideration (41-60)
  CONTACT_FORM_STARTED: { score: 40, event: 'contact_form_started' },
  DESIGN_INQUIRY: { score: 50, event: 'custom_design_inquiry' },
  EMAIL_SUBMITTED: { score: 60, event: 'contact_email_submitted' },

  // Intent (61-80)
  WHATSAPP_CLICK: { score: 70, event: 'whatsapp_link_clicked' },
  WHATSAPP_MESSAGE_SENT: { score: 85, event: 'whatsapp_message_received' },
  PHONE_CALL: { score: 80, event: 'phone_call_received' },

  // Conversion (81-100)
  QUOTE_SUBMITTED: { score: 90, event: 'quote_request_submitted' },
  DESIGN_APPROVED: { score: 95, event: 'design_approved' },
  ORDER_PLACED: { score: 100, event: 'order_placed' }
};
```

## Implementation

```typescript
import { LeadScoringService } from '@/lib/lead-scoring';
import { MYARMY_SCORING_EVENTS } from './events';

// Track page view
export async function trackLandingPageView(
  leadId: string,
  page: string,
  source: string
) {
  let scoreDelta = MYARMY_SCORING_EVENTS.LANDING_PAGE_VIEW.score;

  // Bonus for military keyword arrivals
  if (source === 'organic' && isMilitaryKeyword(page)) {
    scoreDelta = MYARMY_SCORING_EVENTS.ORGANIC_MILITARY_KEYWORD.score;
  }

  await leadScoring.trackEvent(leadId, {
    event_name: MYARMY_SCORING_EVENTS.LANDING_PAGE_VIEW.event,
    score_delta: scoreDelta,
    timestamp: new Date(),
    metadata: { page, source }
  });
}

// Track WhatsApp contact (critical conversion point)
export async function trackWhatsAppContact(
  leadId: string,
  phoneNumber: string,
  message?: string
) {
  const scoreDelta = message
    ? MYARMY_SCORING_EVENTS.WHATSAPP_MESSAGE_SENT.score // 85
    : MYARMY_SCORING_EVENTS.WHATSAPP_CLICK.score;       // 70

  const lead = await leadScoring.trackEvent(leadId, {
    event_name: message
      ? MYARMY_SCORING_EVENTS.WHATSAPP_MESSAGE_SENT.event
      : MYARMY_SCORING_EVENTS.WHATSAPP_CLICK.event,
    score_delta: scoreDelta,
    timestamp: new Date(),
    metadata: { phoneNumber, hasMessage: !!message }
  });

  // Create urgent SLA (1 hour response time)
  if (lead.score >= 80) {
    await createSLA(leadId, 'urgent');
    await notifySalesTeam(lead);
  }
}

// Track order placement
export async function trackOrderPlaced(
  leadId: string,
  orderId: string,
  orderValue: number
) {
  await leadScoring.trackEvent(leadId, {
    event_name: MYARMY_SCORING_EVENTS.ORDER_PLACED.event,
    score_delta: MYARMY_SCORING_EVENTS.ORDER_PLACED.score,
    timestamp: new Date(),
    metadata: {
      orderId,
      orderValue,
      currency: 'CHF'
    }
  });

  // Mark as converted
  await markLeadConverted(leadId, orderId, orderValue);
}
```

## Swiss Military Context

### Target Audience
- **Primary**: Swiss Army unit commanders (Zugführer, Kompaniekommandant)
- **Secondary**: Individual soldiers (Rekruten, Durchdiener)
- **Tertiary**: Veterans associations (Militärvereine)

### Key Products
- **Funktionsabzeichen**: Function badges (CHF 12-25 each, min order 20)
- **Truppenabzeichen**: Unit patches (CHF 8-15 each, min order 50)
- **Rekrutenschule Souvenirs**: Custom RS badges (CHF 15-30 each, min order 30)

### Average Order Values
- Small orders (individuals): CHF 150-300
- Medium orders (squads): CHF 500-1200
- Large orders (companies): CHF 2000-5000

### Conversion Characteristics
- **Decision makers**: Unit commanders (B2B)
- **End users**: Soldiers (B2C experience)
- **Communication**: WhatsApp preferred (85% of conversions)
- **Language**: Swiss German primary, High German acceptable
- **Timeline**: 2-6 weeks inquiry to order

## Score Decay

Swiss military procurement has **seasonal patterns**:
- **Peak**: September-November (new recruits)
- **Low**: June-August (summer break)

Apply aggressive decay during low season:

```typescript
function applySeasonalDecay(score: number, daysSinceLastActivity: number): number {
  const currentMonth = new Date().getMonth();
  const isLowSeason = currentMonth >= 5 && currentMonth <= 7; // June-August

  const baseDecayRate = 0.02; // 2% per day
  const seasonalDecayRate = isLowSeason ? 0.04 : 0.02; // 4% in low season

  const decayFactor = Math.pow(1 - seasonalDecayRate, daysSinceLastActivity);
  return Math.floor(score * decayFactor);
}
```

## Lead Routing

```typescript
async function routeMyArmyLead(lead: Lead): Promise<void> {
  // Hot leads (80+) → Sales rep (1 hour SLA)
  if (lead.score >= 80) {
    await assignToSalesRep(lead);
    await createSLA(lead.id, 'urgent'); // 1 hour
    await sendWhatsAppNotification(lead);
  }
  // Warm leads (60-79) → Marketing automation (4 hour SLA)
  else if (lead.score >= 60) {
    await addToNurtureSequence(lead, 'warm_lead_sequence');
    await createSLA(lead.id, 'high'); // 4 hours
  }
  // Cold leads (40-59) → Weekly newsletter
  else if (lead.score >= 40) {
    await addToNewsletter(lead);
    await createSLA(lead.id, 'normal'); // 24 hours
  }
  // Very cold (<40) → No immediate action
  else {
    await addToRemarketing(lead);
  }
}
```

## Integration with SLA Tracking

```typescript
import { SLATrackingService } from '@/lib/sla-tracking';

// When lead score changes, update SLA
export async function onLeadScoreUpdate(lead: Lead, previousScore: number) {
  const previousTier = determineSLATier(previousScore);
  const newTier = determineSLATier(lead.score);

  if (previousTier !== newTier) {
    // Update SLA tier
    const sla = await getSLAForLead(lead.id);
    if (sla) {
      await updateSLATier(sla.id, newTier);
    } else {
      await createSLA(lead.id, newTier);
    }

    // Notify if escalated to urgent
    if (newTier === 'urgent' && previousTier !== 'urgent') {
      await notifyUrgentLead(lead);
    }
  }
}

function determineSLATier(score: number): 'urgent' | 'high' | 'normal' | 'low' {
  if (score >= 80) return 'urgent';   // 1 hour
  if (score >= 60) return 'high';     // 4 hours
  if (score >= 40) return 'normal';   // 24 hours
  return 'low';                       // 48 hours
}
```

## Analytics

```typescript
// Monthly lead funnel report
export async function generateMonthlyLeadReport(month: string) {
  const leads = await getLeadsForMonth(month);

  const funnel = {
    cold_to_warm: 0,
    warm_to_hot: 0,
    hot_to_very_hot: 0,
    very_hot_to_conversion: 0
  };

  const conversionRates = {
    cold_to_warm: 0,
    warm_to_hot: 0,
    hot_to_very_hot: 0,
    very_hot_to_conversion: 0,
    overall: 0
  };

  // Calculate progression
  // ... implementation

  return {
    month,
    total_leads: leads.length,
    conversions: leads.filter(l => l.score >= 100).length,
    funnel,
    conversionRates,
    avgScoreBySource: calculateAvgScoreBySource(leads),
    topConversionPath: identifyTopPath(leads)
  };
}
```

## Key Rules

### DO:
- Give bonus score for military keywords (militär badge, funktionsabzeichen)
- Track WhatsApp contacts with high priority (85 points)
- Consider seasonal patterns (RS intake Sept-Nov)
- Route hot leads immediately (<1 hour)
- Track Swiss German vs High German preference

### DON'T:
- Treat like standard e-commerce (longer cycle)
- Ignore unit commander decision-making power
- Forget minimum order quantities in scoring
- Skip WhatsApp as conversion channel
- Assume year-round steady demand

## Environment Variables

```bash
SUPABASE_URL="https://your-project.supabase.co"
SUPABASE_ANON_KEY="your-anon-key"
WHATSAPP_BUSINESS_NUMBER="+41791234567"
SALES_REP_EMAIL="sales@myarmy.ch"
```

## Resources

- **Framework**: `lead-generation-framework/lead-scoring-system`
- **SLA Integration**: `lead-generation-framework/sla-tracking`
- **MyArmy Context**: `/landing/docs/business/swiss-military-market.md`

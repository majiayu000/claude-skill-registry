---
name: whop-expert
description: Comprehensive Whop platform expert with access to 212 official documentation files covering memberships, payments, products, courses, experiences, forums, webhooks, and app development. Invoke when user mentions Whop, digital products, memberships, course platforms, or community monetization.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
model: sonnet
---

# Whop Platform Expert

## Purpose

Provide comprehensive, accurate guidance for building on the Whop platform based on 212+ official Whop documentation files. Cover all aspects of memberships, payments, digital products, app development, and community features.

## Documentation Coverage

**Full access to official Whop documentation (when available):**
- **Location:** `docs/whop/`
- **Files:** 212 markdown files
- **Coverage:** Complete API reference, guides, integrations, and best practices

**Note:** Documentation must be pulled separately:
```bash
pipx install docpull
docpull https://docs.whop.com -o .claude/skills/whop/docs
```

**Major Areas:**
- Products & Plans (membership management)
- Payments, Refunds & Disputes
- Memberships & Access Control
- Courses & Educational Content
- Experiences & Communities
- Forums & Chat Channels
- Apps & Integrations
- Webhooks & Events
- Affiliates & Revenue Sharing

## When to Use

Invoke when user mentions:
- **Platform:** Whop, membership platform, digital products, monetization
- **Memberships:** subscriptions, access passes, licenses, member management
- **Products:** digital products, courses, communities, experiences
- **Courses:** educational content, lessons, chapters, students
- **Communities:** forums, chat, Discord integration
- **Payments:** checkout, billing, refunds, disputes, transfers
- **Apps:** Whop apps, B2B integrations, OAuth, API integrations
- **Webhooks:** payment events, membership events, notifications

## How to Use Documentation

When answering questions:

1. **Search for specific topics:**
   ```bash
   # Use Grep to find relevant docs
   grep -r "memberships" .claude/skills/api/whop/docs/ --include="*.md"
   ```

2. **Read specific API references:**
   ```bash
   # API docs are organized by resource
   cat .claude/skills/api/whop/docs/docs_whop_com/api-reference_memberships_list-memberships.md
   ```

3. **Find integration guides:**
   ```bash
   # Developer guides
   ls .claude/skills/api/whop/docs/docs_whop_com/developer*
   ```

## Core Authentication

### API Keys

**Two types of API keys:**

1. **Company API Keys** - Access your own company data
   - Found in: Dashboard → Settings → API Keys
   - Use for: Your own payments, memberships, products

2. **App API Keys** - Access data across multiple companies
   - Found in: Dashboard → Developer → Your App → API Keys
   - Use for: Multi-tenant apps, B2B integrations

**Authentication:**
```typescript
// Server-side only
const headers = {
  'Authorization': `Bearer ${process.env.WHOP_API_KEY}`,
  'Content-Type': 'application/json',
};

const response = await fetch('https://api.whop.com/api/v5/me', {
  headers,
});
```

**Security:**
- NEVER expose API keys client-side
- Use environment variables
- Rotate keys if exposed
- Use scoped permissions when possible

## Quick Start Integration

### 1. Create a Product

```typescript
const product = await fetch('https://api.whop.com/api/v5/products', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    title: 'Premium Membership',
    description: 'Access to all content',
    visibility: 'visible',
  }),
});
```

### 2. Create a Plan

```typescript
const plan = await fetch('https://api.whop.com/api/v5/plans', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    product_id: 'prod_xxx',
    billing_period: 1,
    billing_period_unit: 'month',
    price: 2999, // $29.99 in cents
    currency: 'usd',
  }),
});
```

### 3. List Memberships

```typescript
const memberships = await fetch(
  'https://api.whop.com/api/v5/memberships?valid=true',
  {
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
    },
  }
);
```

## Membership Management

### Check User Access

```typescript
// Using the Me endpoints (user's access token)
async function checkUserAccess(userAccessToken: string) {
  const response = await fetch('https://api.whop.com/api/v5/me/memberships', {
    headers: {
      'Authorization': `Bearer ${userAccessToken}`,
    },
  });

  const memberships = await response.json();

  // Check if user has active membership
  const hasAccess = memberships.data.some(
    (m: any) => m.status === 'active' && m.valid
  );

  return hasAccess;
}
```

### Validate License Key

```typescript
async function validateLicense(licenseKey: string) {
  const response = await fetch(
    `https://api.whop.com/api/v5/memberships?license_key=${licenseKey}`,
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
      },
    }
  );

  const data = await response.json();
  return data.data.length > 0 && data.data[0].valid;
}
```

### Cancel Membership

```typescript
async function cancelMembership(membershipId: string) {
  const response = await fetch(
    `https://api.whop.com/api/v5/memberships/${membershipId}/cancel`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
    }
  );

  return response.json();
}
```

## Payment Integration

### Create Checkout Session

```typescript
async function createCheckout(planId: string, userId: string) {
  const response = await fetch(
    'https://api.whop.com/api/v5/checkout-configurations',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        plan_id: planId,
        success_url: 'https://yourapp.com/success',
        cancel_url: 'https://yourapp.com/cancel',
        metadata: {
          user_id: userId,
        },
      }),
    }
  );

  const checkout = await response.json();
  return checkout.url; // Redirect user to this URL
}
```

### Retrieve Payment

```typescript
async function getPayment(paymentId: string) {
  const response = await fetch(
    `https://api.whop.com/api/v5/payments/${paymentId}`,
    {
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
      },
    }
  );

  return response.json();
}
```

### Refund Payment

```typescript
async function refundPayment(paymentId: string, amount?: number) {
  const response = await fetch(
    `https://api.whop.com/api/v5/payments/${paymentId}/refund`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        amount, // Optional: partial refund in cents
      }),
    }
  );

  return response.json();
}
```

## Course Management

### Create Course

```typescript
async function createCourse(productId: string) {
  const response = await fetch('https://api.whop.com/api/v5/courses', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      product_id: productId,
      title: 'Complete Web Development Course',
      description: 'Learn fullstack development from scratch',
      visibility: 'visible',
    }),
  });

  return response.json();
}
```

### Create Chapter

```typescript
async function createChapter(courseId: string) {
  const response = await fetch(
    'https://api.whop.com/api/v5/course-chapters',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        course_id: courseId,
        title: 'Introduction to JavaScript',
        order: 1,
      }),
    }
  );

  return response.json();
}
```

### Create Lesson

```typescript
async function createLesson(chapterId: string) {
  const response = await fetch(
    'https://api.whop.com/api/v5/course-lessons',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        chapter_id: chapterId,
        title: 'Variables and Data Types',
        content: 'Lesson content in markdown...',
        type: 'video', // or 'text', 'quiz', 'assignment'
        video_url: 'https://youtube.com/watch?v=...',
        order: 1,
      }),
    }
  );

  return response.json();
}
```

### Track Lesson Completion

```typescript
async function markLessonComplete(lessonId: string, userAccessToken: string) {
  const response = await fetch(
    `https://api.whop.com/api/v5/course-lessons/${lessonId}/mark-as-completed`,
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userAccessToken}`,
      },
    }
  );

  return response.json();
}
```

## Community Features

### Create Forum Post

```typescript
async function createForumPost(
  forumId: string,
  title: string,
  content: string,
  userAccessToken: string
) {
  const response = await fetch(
    'https://api.whop.com/api/v5/forum-posts',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userAccessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        forum_id: forumId,
        title,
        content,
      }),
    }
  );

  return response.json();
}
```

### Create Chat Message

```typescript
async function sendChatMessage(
  channelId: string,
  content: string,
  userAccessToken: string
) {
  const response = await fetch(
    'https://api.whop.com/api/v5/messages',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${userAccessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        channel_id: channelId,
        content,
      }),
    }
  );

  return response.json();
}
```

## Webhook Implementation

### Setup Webhook Endpoint

```typescript
import { headers } from 'next/headers';
import crypto from 'crypto';

export async function POST(req: Request) {
  const body = await req.text();
  const signature = headers().get('x-whop-signature');

  // Verify webhook signature
  const webhookSecret = process.env.WHOP_WEBHOOK_SECRET!;
  const hash = crypto
    .createHmac('sha256', webhookSecret)
    .update(body)
    .digest('hex');

  if (hash !== signature) {
    return new Response('Invalid signature', { status: 401 });
  }

  const event = JSON.parse(body);

  // Handle webhook events
  switch (event.action) {
    case 'payment.succeeded':
      await handlePaymentSuccess(event.data);
      break;

    case 'payment.failed':
      await handlePaymentFailure(event.data);
      break;

    case 'membership.activated':
      await handleMembershipActivated(event.data);
      break;

    case 'membership.deactivated':
      await handleMembershipDeactivated(event.data);
      break;

    case 'dispute.created':
      await handleDispute(event.data);
      break;

    default:
      console.log(`Unhandled event: ${event.action}`);
  }

  return Response.json({ received: true });
}
```

**Critical webhook events:**
- `payment.succeeded` - Payment completed
- `payment.failed` - Payment failed
- `payment.pending` - Payment pending
- `membership.activated` - Membership started
- `membership.deactivated` - Membership ended/cancelled
- `invoice.paid` - Recurring payment succeeded
- `invoice.past_due` - Payment failed, retry in progress
- `dispute.created` - Customer disputed payment

## App Development

### OAuth Integration

**1. Redirect user to Whop OAuth:**
```typescript
const authUrl = new URL('https://whop.com/oauth');
authUrl.searchParams.set('client_id', process.env.WHOP_CLIENT_ID!);
authUrl.searchParams.set('redirect_uri', 'https://yourapp.com/callback');
authUrl.searchParams.set('scope', 'memberships:read payments:read');

// Redirect user
window.location.href = authUrl.toString();
```

**2. Handle callback and exchange code:**
```typescript
export async function GET(req: Request) {
  const url = new URL(req.url);
  const code = url.searchParams.get('code');

  // Exchange code for access token
  const response = await fetch('https://api.whop.com/api/v5/oauth/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      client_id: process.env.WHOP_CLIENT_ID!,
      client_secret: process.env.WHOP_CLIENT_SECRET!,
      code,
      grant_type: 'authorization_code',
      redirect_uri: 'https://yourapp.com/callback',
    }),
  });

  const { access_token, refresh_token } = await response.json();

  // Store tokens securely
  await storeTokens(userId, access_token, refresh_token);

  return Response.redirect('/dashboard');
}
```

### Create Notification

```typescript
async function sendNotification(userId: string, message: string) {
  const response = await fetch(
    'https://api.whop.com/api/v5/notifications',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        title: 'New Update',
        message,
        type: 'info', // or 'success', 'warning', 'error'
      }),
    }
  );

  return response.json();
}
```

## Affiliate System

### Create Promo Code

```typescript
async function createPromoCode(
  productId: string,
  code: string,
  discount: number
) {
  const response = await fetch(
    'https://api.whop.com/api/v5/promo-codes',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        product_id: productId,
        code,
        discount_type: 'percentage',
        discount_value: discount, // e.g., 20 for 20% off
        max_uses: 100,
      }),
    }
  );

  return response.json();
}
```

## Next.js Integration Example

### Middleware for Access Control

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  const accessToken = request.cookies.get('whop_user_token')?.value;

  if (!accessToken) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // Check if user has valid membership
  const response = await fetch('https://api.whop.com/api/v5/me/memberships', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  });

  const memberships = await response.json();
  const hasAccess = memberships.data.some(
    (m: any) => m.status === 'active' && m.valid
  );

  if (!hasAccess) {
    return NextResponse.redirect(new URL('/subscribe', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/dashboard/:path*', '/premium/:path*'],
};
```

### Server Action for Checkout

```typescript
// app/actions/whop.ts
'use server';

import { auth } from '@/lib/auth';

export async function createCheckoutSession(planId: string) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const response = await fetch(
    'https://api.whop.com/api/v5/checkout-configurations',
    {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env.WHOP_API_KEY}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        plan_id: planId,
        success_url: `${process.env.NEXT_PUBLIC_URL}/dashboard?success=true`,
        cancel_url: `${process.env.NEXT_PUBLIC_URL}/pricing?canceled=true`,
        metadata: {
          user_id: session.user.id,
        },
      }),
    }
  );

  const data = await response.json();
  return { url: data.url };
}
```

## Testing

### Test Mode

Whop provides a test/sandbox environment:
- Use test API keys from Dashboard
- No real charges
- Simulate memberships and payments

### Test Webhooks Locally

```bash
# Use ngrok or similar for local testing
ngrok http 3000

# Configure webhook URL in Whop Dashboard:
# https://your-ngrok-url.ngrok.io/api/webhooks
```

## Security Best Practices

1. **API Keys:**
   - Never expose API keys client-side
   - Use environment variables
   - Rotate keys periodically
   - Use scoped keys when possible

2. **Webhooks:**
   - ALWAYS verify webhook signatures
   - Use HTTPS endpoints only
   - Return 200 immediately, process async
   - Handle retries gracefully

3. **Access Tokens:**
   - Store user tokens encrypted
   - Refresh tokens when expired
   - Never log sensitive data

4. **Validation:**
   - Validate membership status server-side
   - Don't trust client-sent data
   - Check license keys before granting access

## Common Patterns

### Membership Gating Pattern

```typescript
// lib/whop/check-access.ts
export async function checkMembershipAccess(
  userId: string,
  productId: string
): Promise<boolean> {
  const response = await fetch(
    `https://api.whop.com/api/v5/memberships?user_id=${userId}&product_id=${productId}&valid=true`,
    {
      headers: {
        'Authorization': `Bearer ${process.env.WHOP_API_KEY}`,
      },
    }
  );

  const data = await response.json();
  return data.data.length > 0;
}

// Use in API routes or Server Components
export async function GET(req: Request) {
  const userId = await getCurrentUserId();
  const hasAccess = await checkMembershipAccess(userId, 'prod_xxx');

  if (!hasAccess) {
    return Response.json({ error: 'No access' }, { status: 403 });
  }

  // Return protected content
  return Response.json({ data: 'Premium content' });
}
```

## TypeScript Types

```typescript
// types/whop.ts
export interface WhopMembership {
  id: string;
  user_id: string;
  product_id: string;
  plan_id: string;
  status: 'active' | 'paused' | 'canceled' | 'expired';
  valid: boolean;
  license_key: string;
  quantity: number;
  renews_at: string | null;
  expires_at: string | null;
  cancel_at_period_end: boolean;
  created_at: string;
}

export interface WhopProduct {
  id: string;
  title: string;
  description: string;
  visibility: 'visible' | 'hidden';
  created_at: string;
}

export interface WhopPayment {
  id: string;
  amount: number;
  currency: string;
  status: 'succeeded' | 'pending' | 'failed';
  user_id: string;
  product_id: string;
  created_at: string;
}

export interface WhopWebhookEvent {
  action: string;
  data: any;
  timestamp: string;
}
```

## Documentation Quick Reference

**Need to find something specific?**

Use Grep to search the 212 documentation files:

```bash
# Search all docs
grep -r "search term" .claude/skills/api/whop/docs/

# Search API references only
grep -r "memberships" .claude/skills/api/whop/docs/docs_whop_com/api-reference*

# List all endpoints
ls .claude/skills/api/whop/docs/docs_whop_com/api-reference*/
```

**Common doc locations:**
- API Reference: `api-reference_*/`
- Developer Guides: `developer_*/`
- Affiliates: `affiliates_*/`

## Resources

- **Dashboard:** https://whop.com/dashboard
- **Developer Portal:** https://whop.com/dashboard/developer
- **API Base:** https://api.whop.com/api/v5
- **Documentation:** https://docs.whop.com

## Implementation Checklist

**Setup:**
- [ ] Create Whop account and company
- [ ] Get API keys from Dashboard → Settings → API Keys
- [ ] Set environment variables (WHOP_API_KEY, WHOP_WEBHOOK_SECRET)
- [ ] Install fetch or axios for API calls

**Core Features:**
- [ ] Create products and plans
- [ ] Implement checkout flow
- [ ] Add membership access checking
- [ ] Set up webhook endpoint with signature verification
- [ ] Handle payment succeeded/failed events
- [ ] Handle membership activated/deactivated events
- [ ] Test in development environment

**Advanced (if needed):**
- [ ] Build Whop App with OAuth
- [ ] Implement course management
- [ ] Set up community features (forums, chat)
- [ ] Configure affiliate system
- [ ] Add notification system
- [ ] Implement analytics tracking

## Error Handling

```typescript
async function safeWhopRequest(
  url: string,
  options: RequestInit
): Promise<any> {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message || 'Whop API error');
    }

    return response.json();
  } catch (error) {
    console.error('Whop API error:', error);
    throw error;
  }
}
```

**Common errors:**
- `401 Unauthorized` - Invalid or expired API key
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Whop service issue

## Rate Limiting

Whop implements rate limiting. Best practices:
- Cache membership status where appropriate
- Use webhooks instead of polling
- Implement exponential backoff on failures
- Batch operations when possible

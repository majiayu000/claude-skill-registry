---
name: Helpdesk System Integration
description: Connecting applications with customer support platforms like Zendesk, Intercom, and Freshdesk to manage tickets, user accounts, support workflows, SSO integration, and widget embedding.
---

# Helpdesk System Integration

> **Current Level:** Intermediate  
> **Domain:** Customer Support / Integration

---

## Overview

Helpdesk system integration connects your application with customer support platforms like Zendesk, Intercom, and Freshdesk to manage tickets, user accounts, and support workflows. Effective integration includes SSO, widget embedding, automated ticket creation, and SLA management.

---

## Core Concepts

### Table of Contents

1. [Helpdesk Platforms Comparison](#helpdesk-platforms-comparison)
2. [Zendesk API Integration](#zendesk-api-integration)
3. [Intercom Integration](#intercom-integration)
4. [Freshdesk API](#freshdesk-api)
5. [SSO Integration](#sso-integration)
6. [Widget Embedding](#widget-embedding)
7. [Automated Ticket Creation](#automated-ticket-creation)
8. [SLA Management](#sla-management)
9. [Analytics Integration](#analytics-integration)
10. [Best Practices](#best-practices)

---

## Helpdesk Platforms Comparison

| Platform | Best For | Pricing | Key Features |
|----------|-----------|----------|---------------|
| **Zendesk** | Enterprise, multi-channel | Tiered pricing | Robust API, multi-brand support, extensive integrations |
| **Intercom** | SaaS, customer engagement | Tiered pricing | Live chat, user segmentation, automation |
| **Freshdesk** | SMB, ease of use | Free tier, tiered pricing | Simple UI, good for small teams |
| **Help Scout** | Email-based support | Tiered pricing | Email-focused, clean interface |
| **Front** | Multi-channel inbox | Tiered pricing | Unified inbox, collaboration features |

---

## Zendesk API Integration

### Authentication

```typescript
// Zendesk API client
class ZendeskClient {
  private baseUrl: string;
  private authHeader: string;

  constructor(
    subdomain: string,
    email: string,
    apiToken: string
  ) {
    this.baseUrl = `https://${subdomain}.zendesk.com/api/v2`;
    this.authHeader = Buffer.from(`${email}/token:${apiToken}`).toString('base64');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Basic ${this.authHeader}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Zendesk API error');
    }

    return response.json();
  }
}

// Initialize client
const zendesk = new ZendeskClient(
  process.env.ZENDESK_SUBDOMAIN!,
  process.env.ZENDESK_EMAIL!,
  process.env.ZENDESK_API_TOKEN!
);
```

### Ticket Creation

```typescript
interface ZendeskTicket {
  subject: string;
  description: string;
  requester: {
    name: string;
    email: string;
  };
  priority?: 'urgent' | 'high' | 'normal' | 'low';
  status?: 'new' | 'open' | 'pending' | 'hold' | 'solved' | 'closed';
  type?: 'question' | 'incident' | 'problem' | 'task';
  tags?: string[];
  custom_fields?: Record<string, any>;
}

class ZendeskTicketManager {
  constructor(private client: ZendeskClient) {}

  /**
   * Create a new ticket
   */
  async createTicket(ticket: ZendeskTicket): Promise<{ id: number; url: string }> {
    const response = await this.client.request<{ ticket: any }>('/tickets.json', {
      method: 'POST',
      body: JSON.stringify({ ticket }),
    });

    return {
      id: response.ticket.id,
      url: `${this.client.baseUrl}/tickets/${response.ticket.id}`,
    };
  }

  /**
   * Create ticket from user feedback
   */
  async createFeedbackTicket(params: {
    userId: string;
    userEmail: string;
    userName: string;
    subject: string;
    description: string;
    priority?: string;
    category?: string;
  }): Promise<number> {
    const ticket: ZendeskTicket = {
      subject: params.subject,
      description: params.description,
      requester: {
        name: params.userName,
        email: params.userEmail,
      },
      priority: (params.priority as any) || 'normal',
      type: 'question',
      tags: ['feedback', `user-${params.userId}`],
      custom_fields: {
        user_id: params.userId,
        feedback_category: params.category,
      },
    };

    const result = await this.createTicket(ticket);
    return result.id;
  }

  /**
   * Create ticket from error report
   */
  async createErrorTicket(params: {
    userId: string;
    userEmail: string;
    userName: string;
    error: Error;
    context: {
      url: string;
      userAgent: string;
      timestamp: Date;
    };
  }): Promise<number> {
    const description = `
**Error Report**

**User:** ${params.userName} (${params.userEmail})
**User ID:** ${params.userId}
**Timestamp:** ${new Date(params.context.timestamp).toISOString()}
**URL:** ${params.context.url}
**User Agent:** ${params.context.userAgent}

**Error Message:**
${params.error.message}

**Stack Trace:**
\`\`\`
${params.error.stack}
\`\`\`
    `.trim();

    const ticket: ZendeskTicket = {
      subject: `Error: ${params.error.message}`,
      description,
      requester: {
        name: params.userName,
        email: params.userEmail,
      },
      priority: 'high',
      type: 'incident',
      tags: ['error', `user-${params.userId}`],
      custom_fields: {
        user_id: params.userId,
        error_name: params.error.name,
        error_message: params.error.message,
      },
    };

    const result = await this.createTicket(ticket);
    return result.id;
  }

  /**
   * Update ticket
   */
  async updateTicket(
    ticketId: number,
    updates: Partial<ZendeskTicket>
  ): Promise<void> {
    await this.client.request(`/tickets/${ticketId}.json`, {
      method: 'PUT',
      body: JSON.stringify({ ticket: updates }),
    });
  }

  /**
   * Add comment to ticket
   */
  async addComment(
    ticketId: number,
    comment: string,
    isPublic: boolean = false
  ): Promise<void> {
    await this.client.request(`/tickets/${ticketId}.json`, {
      method: 'PUT',
      body: JSON.stringify({
        ticket: {
          comment: {
            body: comment,
            public: isPublic,
          },
        },
      }),
    });
  }
}
```

### User Management

```typescript
class ZendeskUserManager {
  constructor(private client: ZendeskClient) {}

  /**
   * Create or update user
   */
  async upsertUser(user: {
    externalId: string;
    name: string;
    email: string;
    phone?: string;
    organization?: string;
    role?: 'end-user' | 'agent' | 'admin';
    customFields?: Record<string, any>;
  }): Promise<{ id: number; created: boolean }> {
    // Try to find existing user
    try {
      const existing = await this.findUserByEmail(user.email);
      if (existing) {
        // Update user
        await this.client.request(`/users/${existing.id}.json`, {
          method: 'PUT',
          body: JSON.stringify({ user }),
        });
        return { id: existing.id, created: false };
      }
    } catch {
      // User not found, create new
    }

    // Create new user
    const response = await this.client.request<{ user: any }>('/users.json', {
      method: 'POST',
      body: JSON.stringify({ user }),
    });

    return { id: response.user.id, created: true };
  }

  /**
   * Find user by email
   */
  async findUserByEmail(email: string): Promise<any | null> {
    try {
      const response = await this.client.request<{ users: any[] }>(
        `/users/search.json?query=${encodeURIComponent(email)}`
      );
      return response.users[0] || null;
    } catch {
      return null;
    }
  }

  /**
   * Find user by external ID
   */
  async findUserByExternalId(externalId: string): Promise<any | null> {
    try {
      const response = await this.client.request<{ users: any[] }>(
        `/users/search.json?external_id=${encodeURIComponent(externalId)}`
      );
      return response.users[0] || null;
    } catch {
      return null;
    }
  }

  /**
   * Get user tickets
   */
  async getUserTickets(userId: number): Promise<any[]> {
    const response = await this.client.request<{ tickets: any[] }>(
      `/users/${userId}/tickets/requested.json`
    );
    return response.tickets;
  }

  /**
   * Suspend user
   */
  async suspendUser(userId: number): Promise<void> {
    await this.client.request(`/users/${userId}.json`, {
      method: 'PUT',
      body: JSON.stringify({ user: { suspended: true } }),
    });
  }

  /**
   * Unsuspend user
   */
  async unsuspendUser(userId: number): Promise<void> {
    await this.client.request(`/users/${userId}.json`, {
      method: 'PUT',
      body: JSON.stringify({ user: { suspended: false } }),
    });
  }
}
```

### Custom Fields

```typescript
class ZendeskCustomFields {
  constructor(private client: ZendeskClient) {}

  /**
   * Create custom field
   */
  async createCustomField(field: {
    type: 'text' | 'textarea' | 'date' | 'integer' | 'decimal' | 'checkbox' | 'dropdown' | 'multiselect';
    title: string;
    description?: string;
    key?: string;
    required?: boolean;
    visible_in_portal?: boolean;
    editable_in_portal?: boolean;
    options?: string[];
  }): Promise<number> {
    const response = await this.client.request<{ ticket_field: any }>(
      '/ticket_fields.json',
      {
        method: 'POST',
        body: JSON.stringify({ ticket_field: field }),
      }
    );

    return response.ticket_field.id;
  }

  /**
   * Get custom fields
   */
  async getCustomFields(): Promise<any[]> {
    const response = await this.client.request<{ ticket_fields: any[] }>(
      '/ticket_fields.json'
    );
    return response.ticket_fields;
  }

  /**
   * Update custom field
   */
  async updateCustomField(
    fieldId: number,
    updates: Partial<typeof field>
  ): Promise<void> {
    await this.client.request(`/ticket_fields/${fieldId}.json`, {
      method: 'PUT',
      body: JSON.stringify({ ticket_field: updates }),
    });
  }
}
```

### Webhooks

```typescript
import express from 'express';

const app = express();

// Verify Zendesk webhook signature
function verifyZendeskSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const crypto = require('crypto');
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('base64');

  return signature === expectedSignature;
}

// Webhook handler
app.post('/webhooks/zendesk', express.raw({ type: 'application/json' }), (req, res) => {
  const signature = req.headers['x-zendesk-webhook-signature'] as string;
  const payload = req.body.toString();

  // Verify signature
  if (!verifyZendeskSignature(payload, signature, process.env.ZENDESK_WEBHOOK_SECRET!)) {
    return res.status(401).send('Invalid signature');
  }

  const event = JSON.parse(payload);

  // Process webhook
  switch (event.topic) {
    case 'ticket.created':
      handleTicketCreated(event);
      break;
    case 'ticket.updated':
      handleTicketUpdated(event);
      break;
    case 'ticket.comment.created':
      handleCommentCreated(event);
      break;
    case 'user.created':
      handleUserCreated(event);
      break;
  }

  res.status(200).send('OK');
});

async function handleTicketCreated(event: any): Promise<void> {
  console.log('Ticket created:', event.ticket.id);
  
  // Sync with internal system
  await syncTicketToDatabase(event.ticket);
}

async function handleTicketUpdated(event: any): Promise<void> {
  console.log('Ticket updated:', event.ticket.id);
  
  // Update internal system
  await updateTicketInDatabase(event.ticket);
}

async function handleCommentCreated(event: any): Promise<void> {
  console.log('Comment created:', event.ticket.id);
  
  // Notify user if needed
  if (event.comment.public) {
    await notifyUserOfNewComment(event.ticket, event.comment);
  }
}

async function handleUserCreated(event: any): Promise<void> {
  console.log('User created:', event.user.id);
  
  // Sync user
  await syncUserToDatabase(event.user);
}
```

---

## Intercom Integration

### Authentication

```typescript
// npm install intercom-client
import Intercom from 'intercom-client';

const intercom = new Intercom.Client({
  token: process.env.INTERCOM_ACCESS_TOKEN!,
});

// Intercom OAuth 2.0
class IntercomOAuth {
  private clientId: string;
  private clientSecret: string;
  private redirectUri: string;

  constructor() {
    this.clientId = process.env.INTERCOM_CLIENT_ID!;
    this.clientSecret = process.env.INTERCOM_CLIENT_SECRET!;
    this.redirectUri = `${process.env.APP_URL}/auth/intercom/callback`;
  }

  /**
   * Get authorization URL
   */
  getAuthUrl(): string {
    return `https://app.intercom.io/oauth?${new URLSearchParams({
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      response_type: 'code',
      state: this.generateState(),
    })}`;
  }

  /**
   * Exchange code for access token
   */
  async exchangeCodeForToken(code: string): Promise<{
    accessToken: string;
    tokenType: string;
  }> {
    const response = await fetch('https://api.intercom.io/auth/eagle/token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        code,
        client_id: this.clientId,
        client_secret: this.clientSecret,
        redirect_uri: this.redirectUri,
      }),
    });

    const data = await response.json();
    return {
      accessToken: data.access_token,
      tokenType: data.token_type,
    };
  }

  private generateState(): string {
    return Math.random().toString(36).substring(2);
  }
}
```

### Conversations

```typescript
class InterconConversationManager {
  constructor(private client: Intercom.Client) {}

  /**
   * Create message
   */
  async createMessage(params: {
    userId: string;
    message: string;
    from: {
      type: 'user' | 'admin';
      id: string;
    };
  }): Promise<string> {
    const response = await this.client.conversations.create({
      message_type: 'inapp',
      body: params.message,
      from: params.from,
      to: {
        type: 'user',
        id: params.userId,
      },
    });

    return response.id;
  }

  /**
   * Create conversation from user
   */
  async createConversationFromUser(params: {
    email: string;
    name: string;
    message: string;
    userId?: string;
  }): Promise<string> {
    const response = await this.client.conversations.create({
      message_type: 'email',
      subject: 'New conversation',
      body: params.message,
      from: {
        type: 'user',
        id: params.userId,
        email: params.email,
        name: params.name,
      },
      to: {
        type: 'admin',
        id: process.env.INTERCOM_ADMIN_ID!,
      },
    });

    return response.id;
  }

  /**
   * Get conversation
   */
  async getConversation(conversationId: string): Promise<any> {
    return await this.client.conversations.find({ id: conversationId });
  }

  /**
   * List conversations
   */
  async listConversations(params?: {
    userId?: string;
    status?: 'open' | 'closed';
    page?: number;
  }): Promise<any[]> {
    const options: any = {};

    if (params?.userId) {
      options.intercom_user_id = params.userId;
    }
    if (params?.status) {
      options.open = params.status === 'open';
    }
    if (params?.page) {
      options.page = params.page;
    }

    const response = await this.client.conversations.list(options);
    return response.conversations;
  }

  /**
   * Reply to conversation
   */
  async replyToConversation(params: {
    conversationId: string;
    message: string;
    adminId: string;
    isInternal?: boolean;
  }): Promise<void> {
    await this.client.conversations.reply({
      id: params.conversationId,
      admin_id: params.adminId,
      message_type: params.isInternal ? 'note' : 'comment',
      body: params.message,
    });
  }

  /**
   * Close conversation
   */
  async closeConversation(conversationId: string, adminId: string): Promise<void> {
    await this.client.conversations.reply({
      id: conversationId,
      admin_id: adminId,
      message_type: 'close',
      body: 'Closing conversation',
    });
  }
}
```

### Users

```typescript
class IntercomUserManager {
  constructor(private client: Intercom.Client) {}

  /**
   * Create or update user
   */
  async upsertUser(user: {
    userId?: string;
    email: string;
    name?: string;
    phone?: string;
    signedUpAt?: Date;
    customAttributes?: Record<string, any>;
  }): Promise<{ id: string }> {
    const response = await this.client.users.create({
      user_id: user.userId,
      email: user.email,
      name: user.name,
      phone: user.phone,
      signed_up_at: user.signedUpAt?.toISOString(),
      custom_attributes: user.customAttributes,
    });

    return { id: response.id };
  }

  /**
   * Find user by email
   */
  async findUserByEmail(email: string): Promise<any | null> {
    try {
      const response = await this.client.users.find({ email });
      return response;
    } catch {
      return null;
    }
  }

  /**
   * Find user by user ID
   */
  async findUserByUserId(userId: string): Promise<any | null> {
    try {
      const response = await this.client.users.find({ user_id: userId });
      return response;
    } catch {
      return null;
    }
  }

  /**
   * Delete user
   */
  async deleteUser(userId: string): Promise<void> {
    await this.client.users.delete({ user_id: userId });
  }

  /**
   * Merge users
   */
  async mergeUsers(fromUserId: string, toUserId: string): Promise<void> {
    await this.client.users.merge({
      user_id: toUserId,
      from_user_id: fromUserId,
    });
  }
}
```

### Events

```typescript
class IntercomEventManager {
  constructor(private client: Intercom.Client) {}

  /**
   * Create event
   */
  async createEvent(params: {
    userId: string;
    eventName: string;
    metadata?: Record<string, any>;
    createdAt?: Date;
  }): Promise<void> {
    await this.client.events.create({
      user_id: params.userId,
      event_name: params.eventName,
      created_at: params.createdAt?.toISOString(),
      metadata: params.metadata,
    });
  }

  /**
   * Track user action
   */
  async trackUserAction(params: {
    userId: string;
    action: string;
    context?: Record<string, any>;
  }): Promise<void> {
    await this.createEvent({
      userId: params.userId,
      eventName: params.action,
      metadata: params.context,
    });
  }

  /**
   * Track page view
   */
  async trackPageView(params: {
    userId: string;
    url: string;
    title?: string;
  }): Promise<void> {
    await this.createEvent({
      userId: params.userId,
      eventName: 'page_view',
      metadata: {
        url: params.url,
        title: params.title,
      },
    });
  }
}
```

### Articles

```typescript
class IntercomArticleManager {
  constructor(private client: Intercom.Client) {}

  /**
   * Create article
   */
  async createArticle(article: {
    title: string;
    description: string;
    body: string;
    authorId: string;
    parentId?: string;
    state?: 'draft' | 'published';
  }): Promise<string> {
    const response = await this.client.articles.create({
      title: article.title,
      description: article.description,
      body: article.body,
      author_id: article.authorId,
      parent_id: article.parentId,
      state: article.state || 'draft',
    });

    return response.id;
  }

  /**
   * Update article
   */
  async updateArticle(
    articleId: string,
    updates: Partial<typeof article>
  ): Promise<void> {
    await this.client.articles.update({
      id: articleId,
      ...updates,
    });
  }

  /**
   * Get article
   */
  async getArticle(articleId: string): Promise<any> {
    return await this.client.articles.find({ id: articleId });
  }

  /**
   * List articles
   */
  async listArticles(params?: {
    state?: 'draft' | 'published';
    parentId?: string;
    page?: number;
  }): Promise<any[]> {
    const response = await this.client.articles.list(params || {});
    return response.articles;
  }

  /**
   * Delete article
   */
  async deleteArticle(articleId: string): Promise<void> {
    await this.client.articles.delete({ id: articleId });
  }
}
```

---

## Freshdesk API

### Authentication

```typescript
class FreshdeskClient {
  private baseUrl: string;
  private authHeader: string;

  constructor(domain: string, apiKey: string) {
    this.baseUrl = `https://${domain}.freshdesk.com/api/v2`;
    this.authHeader = Buffer.from(`${apiKey}:X`).toString('base64');
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers: {
        'Authorization': `Basic ${this.authHeader}`,
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.errors?.[0]?.message || 'Freshdesk API error');
    }

    return response.json();
  }
}

// Initialize client
const freshdesk = new FreshdeskClient(
  process.env.FRESHDESK_DOMAIN!,
  process.env.FRESHDESK_API_KEY!
);
```

### Ticket Operations

```typescript
class FreshdeskTicketManager {
  constructor(private client: FreshdeskClient) {}

  /**
   * Create ticket
   */
  async createTicket(ticket: {
    subject: string;
    description: string;
    email: string;
    name: string;
    priority?: number;
    status?: number;
    type?: string;
    tags?: string[];
    customFields?: Record<string, any>;
  }): Promise<number> {
    const response = await this.client.request<{ id: number }>('/tickets', {
      method: 'POST',
      body: JSON.stringify(ticket),
    });

    return response.id;
  }

  /**
   * Get ticket
   */
  async getTicket(ticketId: number): Promise<any> {
    return await this.client.request(`/tickets/${ticketId}`);
  }

  /**
   * Update ticket
   */
  async updateTicket(ticketId: number, updates: any): Promise<void> {
    await this.client.request(`/tickets/${ticketId}`, {
      method: 'PUT',
      body: JSON.stringify(updates),
    });
  }

  /**
   * List tickets
   */
  async listTickets(params?: {
    status?: number;
    priority?: number;
    email?: string;
    page?: number;
  }): Promise<any[]> {
    const queryParams = new URLSearchParams();

    if (params?.status) queryParams.append('status', params.status.toString());
    if (params?.priority) queryParams.append('priority', params.priority.toString());
    if (params?.email) queryParams.append('email', params.email);
    if (params?.page) queryParams.append('page', params.page.toString());

    const response = await this.client.request<{ data: any[] }>(
      `/tickets?${queryParams.toString()}`
    );

    return response.data;
  }

  /**
   * Add reply to ticket
   */
  async addReply(ticketId: number, reply: {
    body: string;
    isPrivate?: boolean;
    userId?: number;
  }): Promise<void> {
    await this.client.request(`/tickets/${ticketId}/reply`, {
      method: 'POST',
      body: JSON.stringify({
        body: reply.body,
        private: reply.isPrivate || false,
        user_id: reply.userId,
      }),
    });
  }
}
```

---

## SSO Integration

### SAML SSO

```typescript
// npm install passport-saml
import { Strategy as SamlStrategy } from 'passport-saml';

const samlStrategy = new SamlStrategy(
  {
    entryPoint: process.env.SAML_ENTRY_POINT!,
    issuer: process.env.SAML_ISSUER!,
    cert: process.env.SAML_CERT!,
    callbackUrl: `${process.env.APP_URL}/auth/saml/callback`,
  },
  async (profile: any, done: any) => {
    // Find or create user
    const user = await findOrCreateUser(profile);
    done(null, user);
  }
);

// Configure passport
import passport from 'passport';

passport.use('saml', samlStrategy);

// SAML login route
app.get('/auth/saml', passport.authenticate('saml', {
  failureRedirect: '/login',
  successRedirect: '/dashboard',
}));

// SAML callback route
app.post(
  '/auth/saml/callback',
  passport.authenticate('saml', { failureRedirect: '/login' }),
  (req, res) => {
    res.redirect('/dashboard');
  }
);
```

### JWT SSO for Helpdesk

```typescript
// Generate JWT for helpdesk SSO
import jwt from 'jsonwebtoken';

function generateHelpdeskJWT(user: {
  id: string;
  email: string;
  name: string;
}): string {
  return jwt.sign(
    {
      iat: Math.floor(Date.now() / 1000),
      name: user.name,
      email: user.email,
      user_id: user.id,
    },
    process.env.HELPDESK_SHARED_SECRET!,
    {
      algorithm: 'HS256',
      expiresIn: '10m',
    }
  );
}

// Helpdesk SSO redirect
app.get('/support/sso', (req, res) => {
  const user = req.user;

  if (!user) {
    return res.redirect('/login');
  }

  const token = generateHelpdeskJWT(user);
  const ssoUrl = `${process.env.HELPDESK_URL}/access/jwt?jwt=${token}`;

  res.redirect(ssoUrl);
});
```

---

## Widget Embedding

### Zendesk Widget

```html
<!-- Zendesk Web Widget -->
<script id="ze-snippet" src="https://static.zdassets.com/ekr/snippet.js?key=YOUR_WIDGET_KEY"></script>

<script>
  // Initialize widget
  zE('webWidget', 'setLocale', 'en');
  zE('webWidget', 'identify', {
    name: 'John Doe',
    email: 'john@example.com',
  });

  // Customize widget
  zE('webWidget', 'updateSettings', {
    webWidget: {
      color: {
        theme: '#007bff',
      },
      launcher: {
        label: {
          '*': 'Support',
        },
      },
      contactForm: {
        fields: [
          { id: 'description', prefill: 'How can we help?' },
        ],
      },
    },
  });

  // Open widget programmatically
  function openSupportWidget() {
    zE('webWidget', 'open');
  }

  // Close widget
  function closeSupportWidget() {
    zE('webWidget', 'close');
  }

  // Set user context
  function setUserContext(user) {
    zE('webWidget', 'identify', {
      name: user.name,
      email: user.email,
      organization: user.organization,
    });
  }
</script>
```

### Intercom Widget

```html>
<!-- Intercom Messenger -->
<script>
  window.intercomSettings = {
    app_id: 'YOUR_APP_ID',
    name: 'John Doe',
    email: 'john@example.com',
    created_at: 1234567890,
    user_id: 'user_123',
    user_hash: 'USER_HASH', // For secure mode
  };

  (function(){var w=window;var ic=w.Intercom;if(typeof ic==="function"){ic('reattach_activator');ic('update',w.intercomSettings);}else{var d=document;var i=function(){i.c(arguments);};i.q=[];i.c=function(args){i.q.push(args);};w.Intercom=i;var l=function(){var s=d.createElement('script');s.type='text/javascript';s.async=true;s.src='https://widget.intercom.io/widget/YOUR_APP_ID';var x=d.getElementsByTagName('script')[0];x.parentNode.insertBefore(s,x);};if(document.readyState==='complete'){l();}else if(w.attachEvent){w.attachEvent('onload',l);}else{w.addEventListener('load',l,false);}})();
</script>

<script>
  // Open Intercom
  function openIntercom() {
    Intercom('show');
  }

  // Close Intercom
  function closeIntercom() {
    Intercom('hide');
  }

  // Update user
  function updateIntercomUser(user) {
    Intercom('update', {
      name: user.name,
      email: user.email,
      user_id: user.id,
    });
  }

  // Start conversation
  function startConversation(message) {
    Intercom('showNewMessage', message);
  }
</script>
```

### React Component

```tsx
import React, { useEffect } from 'react';

interface SupportWidgetProps {
  platform: 'zendesk' | 'intercom';
  user?: {
    name: string;
    email: string;
    id?: string;
  };
  onOpen?: () => void;
  onClose?: () => void;
}

const SupportWidget: React.FC<SupportWidgetProps> = ({
  platform,
  user,
  onOpen,
  onClose,
}) => {
  useEffect(() => {
    // Load widget script
    loadWidgetScript(platform);

    // Identify user if provided
    if (user) {
      identifyUser(platform, user);
    }

    // Set up event listeners
    setupEventListeners(platform, onOpen, onClose);

    return () => {
      // Cleanup
      removeEventListeners(platform);
    };
  }, [platform, user]);

  const openWidget = () => {
    if (platform === 'zendesk') {
      (window as any).zE('webWidget', 'open');
    } else if (platform === 'intercom') {
      (window as any).Intercom('show');
    }
  };

  return (
    <button onClick={openWidget} className="support-button">
      Get Support
    </button>
  );
};

function loadWidgetScript(platform: string): void {
  if (platform === 'zendesk') {
    const script = document.createElement('script');
    script.id = 'ze-snippet';
    script.src = `https://static.zdassets.com/ekr/snippet.js?key=${process.env.ZENDESK_WIDGET_KEY}`;
    document.head.appendChild(script);
  } else if (platform === 'intercom') {
    const script = document.createElement('script');
    script.src = 'https://widget.intercom.io/widget/' + process.env.INTERCOM_APP_ID;
    document.head.appendChild(script);
  }
}

function identifyUser(platform: string, user: any): void {
  if (platform === 'zendesk') {
    (window as any).zE('webWidget', 'identify', user);
  } else if (platform === 'intercom') {
    (window as any).Intercom('update', user);
  }
}

function setupEventListeners(
  platform: string,
  onOpen?: () => void,
  onClose?: () => void
): void {
  if (platform === 'zendesk') {
    (window as any).zE('webWidget:on', 'open', onOpen);
    (window as any).zE('webWidget:on', 'close', onClose);
  } else if (platform === 'intercom') {
    (window as any).Intercom('onUnreadCountChanged', (count) => {
      if (count > 0 && onOpen) onOpen();
    });
  }
}

function removeEventListeners(platform: string): void {
  // Remove event listeners
}

export default SupportWidget;
```

---

## Automated Ticket Creation

### Error Tracking Integration

```typescript
// Create ticket from error
async function createTicketFromError(error: Error, context: {
  userId: string;
  userEmail: string;
  userName: string;
  url: string;
  userAgent: string;
}): Promise<number> {
  const zendesk = new ZendeskTicketManager(zendeskClient);

  return await zendesk.createErrorTicket({
    userId: context.userId,
    userEmail: context.userEmail,
    userName: context.userName,
    error,
    context: {
      url: context.url,
      userAgent: context.userAgent,
      timestamp: Date.now(),
    },
  });
}

// Global error handler
if (typeof window !== 'undefined') {
  window.addEventListener('error', async (event) => {
    const user = getCurrentUser();
    if (user) {
      await createTicketFromError(event.error, {
        userId: user.id,
        userEmail: user.email,
        userName: user.name,
        url: window.location.href,
        userAgent: navigator.userAgent,
      });
    }
  });

  // Unhandled promise rejection
  window.addEventListener('unhandledrejection', async (event) => {
    const user = getCurrentUser();
    if (user) {
      await createTicketFromError(new Error(event.reason), {
        userId: user.id,
        userEmail: user.email,
        userName: user.name,
        url: window.location.href,
        userAgent: navigator.userAgent,
      });
    }
  });
}
```

### Form Submission Integration

```typescript
// Create ticket from form submission
async function createTicketFromForm(formData: {
  name: string;
  email: string;
  subject: string;
  message: string;
  category?: string;
  priority?: string;
}): Promise<number> {
  const zendesk = new ZendeskTicketManager(zendeskClient);

  return await zendesk.createTicket({
    subject: formData.subject,
    description: formData.message,
    requester: {
      name: formData.name,
      email: formData.email,
    },
    priority: (formData.priority as any) || 'normal',
    type: 'question',
    tags: ['form-submission', formData.category].filter(Boolean),
    custom_fields: {
      form_category: formData.category,
    },
  });
}

// Express route for form submission
app.post('/api/support/ticket', express.json(), async (req, res) => {
  try {
    const ticketId = await createTicketFromForm(req.body);
    res.json({ success: true, ticketId });
  } catch (error) {
    console.error('Error creating ticket:', error);
    res.status(500).json({ success: false, error: 'Failed to create ticket' });
  }
});
```

---

## SLA Management

### SLA Tracking

```typescript
interface SLAPolicy {
  id: string;
  name: string;
  conditions: {
    priority?: string[];
    customerTier?: string[];
  };
  responseTime: number; // in hours
  resolutionTime: number; // in hours
}

class SLAManager {
  private policies: SLAPolicy[] = [];

  constructor(policies: SLAPolicy[]) {
    this.policies = policies;
  }

  /**
   * Get applicable SLA policy
   */
  getApplicablePolicy(ticket: {
    priority: string;
    customerTier: string;
  }): SLAPolicy | null {
    return this.policies.find(policy => {
      const priorityMatch = !policy.conditions.priority ||
        policy.conditions.priority.includes(ticket.priority);

      const tierMatch = !policy.conditions.customerTier ||
        policy.conditions.customerTier.includes(ticket.customerTier);

      return priorityMatch && tierMatch;
    }) || null;
  }

  /**
   * Calculate SLA due dates
   */
  calculateSLADates(ticket: {
    createdAt: Date;
    priority: string;
    customerTier: string;
  }): {
    responseDue: Date;
    resolutionDue: Date;
    policy: SLAPolicy;
  } | null {
    const policy = this.getApplicablePolicy(ticket);
    if (!policy) return null;

    const responseDue = new Date(
      ticket.createdAt.getTime() + policy.responseTime * 60 * 60 * 1000
    );
    const resolutionDue = new Date(
      ticket.createdAt.getTime() + policy.resolutionTime * 60 * 60 * 1000
    );

    return { responseDue, resolutionDue, policy };
  }

  /**
   * Check SLA compliance
   */
  checkSLACompliance(ticket: {
    createdAt: Date;
    respondedAt?: Date;
    resolvedAt?: Date;
    priority: string;
    customerTier: string;
  }): {
    responseCompliant: boolean;
    resolutionCompliant: boolean;
    responseOverdue?: number; // in hours
    resolutionOverdue?: number; // in hours
  } | null {
    const slaDates = this.calculateSLADates(ticket);
    if (!slaDates) return null;

    const responseCompliant = !ticket.respondedAt ||
      ticket.respondedAt <= slaDates.responseDue;

    const resolutionCompliant = !ticket.resolvedAt ||
      ticket.resolvedAt <= slaDates.resolutionDue;

    let responseOverdue: number | undefined;
    let resolutionOverdue: number | undefined;

    if (ticket.respondedAt && ticket.respondedAt > slaDates.responseDue) {
      responseOverdue = (ticket.respondedAt.getTime() - slaDates.responseDue.getTime()) / (1000 * 60 * 60);
    }

    if (ticket.resolvedAt && ticket.resolvedAt > slaDates.resolutionDue) {
      resolutionOverdue = (ticket.resolvedAt.getTime() - slaDates.resolutionDue.getTime()) / (1000 * 60 * 60);
    }

    return {
      responseCompliant,
      resolutionCompliant,
      responseOverdue,
      resolutionOverdue,
    };
  }
}

// Example SLA policies
const slaPolicies: SLAPolicy[] = [
  {
    id: 'enterprise-urgent',
    name: 'Enterprise Urgent',
    conditions: {
      priority: ['urgent'],
      customerTier: ['enterprise'],
    },
    responseTime: 1, // 1 hour
    resolutionTime: 4, // 4 hours
  },
  {
    id: 'enterprise-normal',
    name: 'Enterprise Normal',
    conditions: {
      priority: ['high', 'normal'],
      customerTier: ['enterprise'],
    },
    responseTime: 4, // 4 hours
    resolutionTime: 24, // 1 day
  },
  {
    id: 'standard-urgent',
    name: 'Standard Urgent',
    conditions: {
      priority: ['urgent'],
      customerTier: ['standard', 'free'],
    },
    responseTime: 8, // 8 hours
    resolutionTime: 48, // 2 days
  },
  {
    id: 'standard-normal',
    name: 'Standard Normal',
    conditions: {
      priority: ['high', 'normal', 'low'],
      customerTier: ['standard', 'free'],
    },
    responseTime: 24, // 1 day
    resolutionTime: 72, // 3 days
  },
];
```

---

## Analytics Integration

### Ticket Analytics

```typescript
interface TicketAnalytics {
  totalTickets: number;
  openTickets: number;
  closedTickets: number;
  averageResolutionTime: number; // in hours
  averageResponseTime: number; // in hours
  slaComplianceRate: number;
  byPriority: Record<string, number>;
  byCategory: Record<string, number>;
}

class TicketAnalytics {
  constructor(private prisma: PrismaClient) {}

  /**
   * Get ticket analytics
   */
  async getAnalytics(params: {
    startDate: Date;
    endDate: Date;
  }): Promise<TicketAnalytics> {
    const where = {
      createdAt: {
        gte: params.startDate,
        lte: params.endDate,
      },
    };

    const [total, open, closed, tickets] = await Promise.all([
      this.prisma.ticket.count({ where }),
      this.prisma.ticket.count({
        where: { ...where, status: 'open' },
      }),
      this.prisma.ticket.count({
        where: { ...where, status: 'closed' },
      }),
      this.prisma.ticket.findMany({
        where,
        include: { sla: true },
      }),
    ]);

    // Calculate average times
    const closedTickets = tickets.filter(t => t.status === 'closed');
    const averageResolutionTime = closedTickets.length > 0
      ? closedTickets.reduce((sum, t) => {
          if (t.resolvedAt && t.createdAt) {
            return sum + (t.resolvedAt.getTime() - t.createdAt.getTime()) / (1000 * 60 * 60);
          }
          return sum;
        }, 0) / closedTickets.length
      : 0;

    const averageResponseTime = closedTickets.length > 0
      ? closedTickets.reduce((sum, t) => {
          if (t.respondedAt && t.createdAt) {
            return sum + (t.respondedAt.getTime() - t.createdAt.getTime()) / (1000 * 60 * 60);
          }
          return sum;
        }, 0) / closedTickets.length
      : 0;

    // Calculate SLA compliance
    const slaCompliant = closedTickets.filter(t => t.sla?.compliant).length;
    const slaComplianceRate = closedTickets.length > 0
      ? (slaCompliant / closedTickets.length) * 100
      : 0;

    // Group by priority
    const byPriority: Record<string, number> = {};
    for (const ticket of tickets) {
      byPriority[ticket.priority] = (byPriority[ticket.priority] || 0) + 1;
    }

    // Group by category
    const byCategory: Record<string, number> = {};
    for (const ticket of tickets) {
      const category = ticket.category || 'uncategorized';
      byCategory[category] = (byCategory[category] || 0) + 1;
    }

    return {
      totalTickets: total,
      openTickets: open,
      closedTickets: closed,
      averageResolutionTime,
      averageResponseTime,
      slaComplianceRate,
      byPriority,
      byCategory,
    };
  }
}
```

---

## Best Practices

### Integration Best Practices

```typescript
// 1. Always sync user data
async function syncUserToHelpdesk(user: any): Promise<void> {
  await zendeskUserManager.upsertUser({
    externalId: user.id,
    name: user.name,
    email: user.email,
    phone: user.phone,
    organization: user.organization,
    customFields: {
      plan: user.plan,
      signup_date: user.createdAt.toISOString(),
    },
  });
}

// 2. Use webhooks for real-time updates
async function handleHelpdeskWebhook(event: any): Promise<void> {
  switch (event.topic) {
    case 'ticket.created':
      await handleNewTicket(event.ticket);
      break;
    case 'ticket.updated':
      await handleTicketUpdate(event.ticket);
      break;
    case 'ticket.solved':
      await handleTicketSolved(event.ticket);
      break;
  }
}

// 3. Implement retry logic for API calls
async function retryWithBackoff<T>(
  fn: () => Promise<T>,
  maxRetries: number = 3
): Promise<T> {
  let lastError: Error | null = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;
      if (attempt < maxRetries - 1) {
        const delay = Math.pow(2, attempt) * 1000;
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }
  }

  throw lastError;
}

// 4. Cache user data
const userCache = new Map<string, any>();

async function getCachedUser(userId: string): Promise<any> {
  if (userCache.has(userId)) {
    return userCache.get(userId);
  }

  const user = await db.user.findUnique({ where: { id: userId } });
  userCache.set(userId, user);
  return user;
}

// 5. Log all API interactions
function logApiCall(platform: string, method: string, endpoint: string, data?: any): void {
  console.log(`[${platform}] ${method} ${endpoint}`, data);
}
```

---

---

## Quick Start

### Zendesk Integration

```typescript
const zendesk = require('node-zendesk')

const client = zendesk.createClient({
  username: process.env.ZENDESK_EMAIL,
  token: process.env.ZENDESK_API_TOKEN,
  remoteUri: `https://${process.env.ZENDESK_SUBDOMAIN}.zendesk.com/api/v2`
})

// Create ticket
async function createTicket(ticket: Ticket) {
  return await client.tickets.create({
    ticket: {
      subject: ticket.subject,
      comment: { body: ticket.description },
      priority: ticket.priority,
      requester: { email: ticket.userEmail }
    }
  })
}
```

---

## Production Checklist

- [ ] **Platform Selection**: Choose helpdesk platform
- [ ] **API Integration**: Integrate with helpdesk API
- [ ] **SSO Integration**: Single sign-on setup
- [ ] **Widget Embedding**: Embed helpdesk widget
- [ ] **Automated Tickets**: Auto-create tickets
- [ ] **SLA Management**: SLA tracking
- [ ] **Analytics**: Analytics integration
- [ ] **Error Handling**: Handle API errors
- [ ] **Testing**: Test integration
- [ ] **Documentation**: Document integration
- [ ] **Monitoring**: Monitor integration health
- [ ] **Support**: Support team training

---

## Anti-patterns

### ❌ Don't: No SSO

```markdown
# ❌ Bad - Separate login
Users login to app
Users login separately to helpdesk
# Poor UX!
```

```markdown
# ✅ Good - SSO
Users login to app
Helpdesk uses SSO
# Seamless experience
```

### ❌ Don't: No Automation

```markdown
# ❌ Bad - Manual ticket creation
User reports issue → Support creates ticket manually
# Slow!
```

```markdown
# ✅ Good - Automated
User reports issue → Ticket auto-created
# Fast and consistent
```

---

## Integration Points

- **Ticketing System** (`29-customer-support/ticketing-system/`) - Ticket management
- **Live Chat** (`29-customer-support/live-chat/`) - Chat to ticket
- **SSO Integration** (`24-security-practices/sso-integration/`) - Single sign-on

---

## Further Reading

- [Zendesk API Documentation](https://developer.zendesk.com/api-reference/)
- [Intercom API Documentation](https://developers.intercom.com/)
- [Freshdesk API Documentation](https://developers.freshdesk.com/api/)
- [Passport SAML Strategy](https://www.passportjs.org/packages/passport-saml/)

## Resources

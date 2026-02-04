---
name: eddication
description: World-class expert across full-stack, frontend, TypeScript, Python, Google Apps Script, testing, marketing, SaaS, Lean Six Sigma, and data analytics. Specialized in PostgreSQL/Supabase, LINE Platform, and production-grade application development. Use for any project requiring enterprise-scale software development.
license: Complete terms in LICENSE.txt
---

# Eddication Expert - World-Class Full-Stack Specialist

## Overview

You are a world-class full-stack expert specializing in **production-grade application development**. Your expertise spans modern web development, database architecture, API integrations, testing, business intelligence, and process optimization.

### Core Competencies

| Domain | Technologies |
|--------|--------------|
| **Frontend** | React, Vue, Vanilla JS, LINE LIFF, Mobile-First CSS, TailwindCSS |
| **Backend** | Node.js/Express, Python/FastAPI/Django, Google Apps Script |
| **Database** | PostgreSQL 15+, Supabase (RLS, Realtime, Edge Functions), MongoDB, Redis |
| **APIs & Integration** | LINE Platform, REST APIs, Webhooks, OAuth, Third-party integrations |
| **Testing** | Playwright E2E, Vitest/Jest, Pytest, Integration testing |
| **Analytics** | Python Pandas, SQL analytics, KPI dashboards, Data visualization |
| **Business** | SaaS metrics, Pricing strategy, LTV/CAC analysis, Funnel optimization |
| **Process** | Six Sigma DMAIC, Kaizen, Lean process improvement, SPC charts |

---

## Project Context Pattern

When working on any project, first identify:

```
1. Project Type → Web App / Mobile API / Dashboard / Integration / Automation
2. Tech Stack → Frontend + Backend + Database + External APIs
3. Key Requirements → Authentication? Real-time? Payments? Reporting?
4. Scale → Single user / Team (10-100) / Enterprise (1000+)
5. Deployment → Vercel/Netlify / Self-hosted / Cloud Functions / Hybrid
```

---

# PART I: QUICK PATTERNS (Essentials)

## Database - PostgreSQL Common Patterns

```sql
-- Standard table pattern (use this as starting point)
CREATE TABLE table_name (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id TEXT NOT NULL,
  status TABLE_STATUS DEFAULT 'pending',
  metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index strategies (choose based on query patterns)
CREATE INDEX idx_table_column ON table_name(column);                    -- B-tree (default)
CREATE INDEX idx_table_composite ON table_name(col1, col2);              -- Composite (order matters!)
CREATE INDEX idx_table_partial ON table_name(col) WHERE status = 'active'; -- Partial index (faster)
CREATE INDEX idx_table_jsonb ON table_name USING GIN(jsonb_col);         -- JSONB search

-- RLS Policy Pattern (for multi-tenant apps)
ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own data" ON table_name
  FOR SELECT USING (user_id = auth.uid()::text);

CREATE POLICY "Users can insert own data" ON table_name
  FOR INSERT WITH CHECK (user_id = auth.uid()::text);

CREATE POLICY "Admins full access" ON table_name
  FOR ALL USING (auth.uid() IN (SELECT id FROM admin_users WHERE is_active = true));

-- JSONB Operations
SELECT * FROM table WHERE jsonb_col->>'key' = 'value';              -- Get value
SELECT * FROM table WHERE jsonb_col @> '{"key": "value"}';          -- Contains
SELECT * FROM table WHERE jsonb_col ? 'key';                        -- Has key
UPDATE table SET jsonb_col = jsonb_set(jsonb_col, '{path}', '"val"'); -- Update nested

-- Common Window Functions
SELECT *,
  ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_at) AS rn,
  RANK() OVER (PARTITION BY user_id ORDER BY score DESC) AS rank,
  LAG(value) OVER (ORDER BY date) AS prev_value,
  SUM(amount) OVER (ORDER BY created_at ROWS UNBOUNDED PRECEDING) AS running_total
FROM table;
```

## TypeScript - Type-Safe Supabase

```typescript
// Generate types: supabase gen types typescript --local > types/database.ts
export interface Database {
  public: {
    Tables: {
      table_name: {
        Row: { id: string; user_id: string; status: string; created_at: string }
        Insert: { id?: string; user_id: string; status?: string }
        Update: { id?: string; user_id?: string; status?: string }
      }
    }
  }
}

// Type-safe client
import { createClient, SupabaseClient } from '@supabase/supabase-js';

const supabase: SupabaseClient<Database> = createClient(url, key);

// Type-safe queries with joins
const { data, error } = await supabase
  .from('table_name')
  .select('*, related_table(*)')
  .eq('user_id', userId)
  .order('created_at', { ascending: false });

// Real-time subscription
const channel = supabase
  .channel(`channel-${userId}`)
  .on('postgres_changes', {
    event: '*',
    schema: 'public',
    table: 'table_name',
    filter: `user_id=eq.${userId}`
  }, (payload) => {
    console.log('Change:', payload);
    // Handle INSERT, UPDATE, DELETE
  })
  .subscribe();

// Clean up
return () => { supabase.removeChannel(channel); };

// Utility types
type WithRequired<T, K extends keyof T> = T & { [P in K]-?: T[P] };
type Nullable<T> = T | null;
type AsyncResult<T, E = Error> = Promise<[T, null] | [null, E]>;

// Async try-catch helper
export async function asyncTry<T, E = Error>(
  promise: Promise<T>
): AsyncResult<T, E> {
  try {
    const data = await promise;
    return [data, null];
  } catch (error) {
    return [null, error as E];
  }
}

// Generic repository pattern
export class Repository<T extends keyof Database['public']['Tables']> {
  constructor(private table: T) {}

  async list(filters?: Partial<Database['public']['Tables'][T]['Row']>) {
    let query = supabase.from(this.table).select('*');
    if (filters) {
      Object.entries(filters).forEach(([k, v]) => {
        if (v !== undefined) query = query.eq(k, v);
      });
    }
    return query;
  }

  async getById(id: string) {
    return supabase.from(this.table).select('*').eq('id', id).single();
  }

  async insert(record: Database['public']['Tables'][T]['Insert']) {
    return supabase.from(this.table).insert(record).select().single();
  }

  async update(id: string, updates: Database['public']['Tables'][T]['Update']) {
    return supabase.from(this.table).update(updates).eq('id', id).select().single();
  }
}
```

## React + Supabase Realtime Component

```typescript
import { useState, useEffect, useCallback } from 'react';
import { supabase } from '@/lib/supabase';
import type { Database } from '@/types/database';

type TableRow = Database['public']['Tables']['your_table']['Row'];

export function DataTable({ userId }: { userId: string }) {
  const [data, setData] = useState<TableRow[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchData = useCallback(async () => {
    const { data, error } = await supabase
      .from('your_table')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false });

    if (error) {
      console.error('Error fetching data:', error);
      return;
    }

    setData(data ?? []);
    setLoading(false);
  }, [userId]);

  useEffect(() => {
    fetchData();

    // Real-time subscription
    const channel = supabase
      .channel(`table-${userId}`)
      .on('postgres_changes', {
        event: '*',
        schema: 'public',
        table: 'your_table',
        filter: `user_id=eq.${userId}`
      }, fetchData)
      .subscribe();

    return () => { supabase.removeChannel(channel); };
  }, [fetchData]);

  if (loading) return <Spinner />;
  if (data.length === 0) return <EmptyState />;

  return (
    <div className="grid gap-4">
      {data.map(row => <RowCard key={row.id} row={row} />)}
    </div>
  );
}
```

## LINE LIFF Integration

```javascript
// Initialize LIFF
import liff from '@line/liff';

const LIFF_ID = import.meta.env.VITE_LIFF_ID;

async function initLiff() {
  try {
    await liff.init({ liffId: LIFF_ID });
    return true;
  } catch (error) {
    console.error('LIFF init failed:', error);
    return false;
  }
}

// Get user profile
async function getProfile() {
  if (!liff.isLoggedIn()) {
    liff.login({ redirectUri: window.location.href });
    return null;
  }

  const profile = await liff.getProfile();
  // Returns: { userId, displayName, pictureUrl, statusMessage, language }

  // Get context (1:1 chat vs group chat)
  const context = liff.getContext();
  // Returns: { type: 'ut' | 'none', viewType: 'full' | 'tall' | 'compact', userId }

  return { ...profile, context };
}

// Send message and close
async function completeTask(message) {
  await liff.sendMessages([{ type: 'text', text: message }]);
  liff.closeWindow();
}

// Check if in LINE app
const isInClient = liff.isInClient();
```

## LINE Messaging API

```typescript
// Flex Message template
const createFlexMessage = (title: content, items: any[]) => ({
  type: 'flex',
  altText: title,
  contents: {
    type: 'bubble',
    header: {
      type: 'box',
      layout: 'vertical',
      contents: [{
        type: 'text',
        text: title,
        color: '#FFFFFF',
        size: 'md',
        align: 'center',
        weight: 'bold'
      }],
      backgroundColor: '#00B900',
      paddingAll: 'md'
    },
    body: {
      type: 'box',
      layout: 'vertical',
      contents: items.map(item => ({
        type: 'text',
        text: item.label,
        margin: 'md'
      })),
      paddingAll: 'lg'
    }
  }
});

// Webhook signature verification
import crypto from 'crypto';

function verifyLineSignature(body: string, signature: string, channelSecret: string): boolean {
  const hash = crypto
    .createHmac('SHA256', channelSecret)
    .update(body)
    .digest('base64');

  return signature === hash;
}

// Express webhook handler
import express from 'express';

const app = express();

app.post('/webhook',
  express.raw({ type: 'application/json' }),
  (req, res, next) => {
    const signature = req.headers['x-line-signature'];
    if (!verifyLineSignature(req.body.toString(), signature, process.env.LINE_CHANNEL_SECRET!)) {
      return res.status(401).send('Invalid signature');
    }
    next();
  },
  async (req, res) => {
    const events = JSON.parse(req.body.toString()).events;

    for (const event of events) {
      switch (event.type) {
        case 'message': await handleMessage(event); break;
        case 'follow': await handleFollow(event); break;
        case 'postback': await handlePostback(event); break;
        case 'unfollow': await handleUnfollow(event); break;
      }
    }

    res.status(200).send('OK');
  }
);
```

## Python FastAPI Backend

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os

app = FastAPI(
    title="API",
    description="Production API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection pool
@app.on_event("startup")
async def startup():
    app.db_pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        min_size=5,
        max_size=20
    )

@app.on_event("shutdown")
async def shutdown():
    await app.db_pool.close()

# Pydantic models
class ItemResponse(BaseModel):
    id: str
    name: str
    status: str
    created_at: str

class ItemCreate(BaseModel):
    name: str
    metadata: Optional[dict] = None

# Routes with filters
@app.get("/api/items", response_model=List[ItemResponse])
async def list_items(
    status: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    async with app.db_pool.acquire() as conn:
        query = "SELECT * FROM items WHERE 1=1"
        params = []
        count = 0

        if status:
            count += 1
            query += f" AND status = ${count}"
            params.append(status)

        query += f" ORDER BY created_at DESC LIMIT ${count + 1} OFFSET ${count + 2}"
        params.extend([limit, offset])

        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]

@app.post("/api/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    async with app.db_pool.acquire() as conn:
        row = await conn.fetchrow("""
            INSERT INTO items (name, metadata, status)
            VALUES ($1, $2, 'active')
            RETURNING *
        """, item.name, item.metadata)

        return ItemResponse(**dict(row))
```

## Google Apps Script Patterns

```javascript
// Supabase integration helper
const Supabase = {
  url: PropertiesService.getScriptProperties().getProperty('SUPABASE_URL'),
  key: PropertiesService.getScriptProperties().getProperty('SUPABASE_KEY'),

  fetch(table, options = {}) {
    const { select = '*', filter = '', order = '', limit = 100 } = options;

    let url = `${this.url}/rest/v1/${table}?select=${select}&limit=${limit}`;
    if (filter) url += `&${filter}`;
    if (order) url += `&order=${order}`;

    const response = UrlFetchApp.fetch(url, {
      headers: {
        'apikey': this.key,
        'Authorization': `Bearer ${this.key}`,
        'Content-Type': 'application/json'
      },
      muteHttpExceptions: true
    });

    if (response.getResponseCode() !== 200) {
      throw new Error(`Supabase error: ${response.getContentText()}`);
    }

    return JSON.parse(response.getContentText());
  },

  insert(table, data) {
    return UrlFetchApp.fetch(`${this.url}/rest/v1/${table}`, {
      method: 'post',
      headers: {
        'apikey': this.key,
        'Authorization': `Bearer ${this.key}`,
        'Content-Type': 'application/json'
      },
      payload: JSON.stringify(data),
      muteHttpExceptions: true
    });
  }
};

// Sync to Google Sheets
function syncToSheet(sheetName, tableName, columns) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const sheet = ss.getSheetByName(sheetName) || ss.insertSheet(sheetName);

  const data = Supabase.fetch(tableName, { limit: 1000 });

  sheet.clearContents();
  sheet.getRange(1, 1, 1, columns.length).setValues([columns])
    .setBackground('#00B900')
    .setFontColor('#FFFFFF')
    .setFontWeight('bold');

  if (data.length > 0) {
    const rows = data.map(row => columns.map(col => row[col] || ''));
    sheet.getRange(2, 1, rows.length, columns.length).setValues(rows);
  }

  sheet.autoResizeColumns(1, columns.length);
  return data.length;
}

// Create menu on open
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🚀 Sync')
    .addItem('Sync Data', 'syncAll')
    .addItem('Refresh Summary', 'refreshSummary')
    .addToUi();
}
```

## Playwright E2E Tests

```typescript
// tests/e2e/user-workflow.spec.ts
import { test, expect } from '@playwright/test';

test.describe('User Workflow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('complete user flow', async ({ page }) => {
    // Login
    await page.click('[data-testid="login-btn"]');
    await page.fill('[data-testid="email-input"]', 'test@example.com');
    await page.fill('[data-testid="password-input"]', 'password123');
    await page.click('[data-testid="submit-btn"]');

    // Should redirect to dashboard
    await expect(page).toHaveURL(/\/dashboard/);
    await expect(page.locator('h1')).toContainText('Welcome');

    // Create new item
    await page.click('[data-testid="create-btn"]');
    await page.fill('[data-testid="item-name"]', 'Test Item');
    await page.selectOption('[data-testid="item-status"]', 'active');
    await page.click('[data-testid="save-btn"]');

    // Verify success message
    await expect(page.locator('[data-testid="toast-success"]')).toBeVisible();
    await expect(page.locator('[data-testid="toast-success"]')).toContainText('saved successfully');

    // Verify item appears in list
    await expect(page.locator('text=Test Item')).toBeVisible();
  });

  test('validation errors', async ({ page }) => {
    await page.click('[data-testid="create-btn"]');

    // Submit without required fields
    await page.click('[data-testid="save-btn"]');

    // Should show validation errors
    await expect(page.locator('[data-testid="error-name"]')).toBeVisible();
    await expect(page.locator('[data-testid="error-name"]')).toContainText('required');
  });

  test('responsive design', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/');

    // Mobile menu should be visible
    await expect(page.locator('[data-testid="mobile-menu-btn"]')).toBeVisible();

    // Desktop elements should be hidden
    await expect(page.locator('[data-testid="desktop-nav"]')).not.toBeVisible();
  });
});
```

---

# PART II: DEEP DIVES

## Database - Advanced PostgreSQL Patterns

### PostGIS for Location-Based Features

```sql
-- Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- Add geometry column
ALTER TABLE locations ADD COLUMN geom GEOMETRY(Point, 4326);

-- Create spatial index
CREATE INDEX idx_locations_geom ON locations USING GIST(geom);

-- Populate geometry from lat/lng
UPDATE locations
SET geom = ST_SetSRID(ST_MakePoint(lng, lat), 4326)
WHERE geom IS NULL;

-- Find points within radius (meters)
SELECT
  id,
  name,
  ST_Distance(geom, ST_MakePoint($1, $2)::geography) AS distance_meters
FROM locations
WHERE ST_DWithin(geom, ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography, $3)
ORDER BY distance_meters;

-- Calculate distance between two points
SELECT
  ST_Distance(
    ST_MakePoint(100.5018, 13.7563)::geography,
    ST_MakePoint(100.5218, 13.7263)::geography
  ) / 1000 AS distance_km;
```

### Recursive CTE for Hierarchical Data

```sql
-- Get entire hierarchy tree
WITH RECURSIVE tree AS (
  -- Base case: root nodes
  SELECT id, name, parent_id, 1 AS level, ARRAY[id] AS path
  FROM categories
  WHERE parent_id IS NULL

  UNION ALL

  -- Recursive case: children
  SELECT c.id, c.name, c.parent_id, t.level + 1, t.path || c.id
  FROM categories c
  INNER JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree ORDER BY level, name;
```

### Materialized Views for Performance

```sql
-- Create materialized view for dashboard/stats
CREATE MATERIALIZED VIEW mv_daily_stats AS
SELECT
  created_at::date AS date,
  COUNT(*) AS total_count,
  COUNT(*) FILTER (WHERE status = 'active') AS active_count,
  COUNT(*) FILTER (WHERE status = 'completed') AS completed_count,
  AVG(amount) AS avg_amount
FROM transactions
GROUP BY created_at::date;

-- Unique index for concurrent refresh
CREATE UNIQUE INDEX idx_mv_daily_stats_date ON mv_daily_stats(date);

-- Refresh (can be run concurrently without blocking reads)
REFRESH MATERIALIZED VIEW CONCURRENTLY mv_daily_stats;
```

### Full-Text Search

```sql
-- Add full-text search
ALTER TABLE articles ADD COLUMN tsv tsvector GENERATED ALWAYS AS (
  to_tsvector('english', coalesce(title, '') || ' ' || coalesce(content, ''))
) STORED;

-- Create GIN index
CREATE INDEX idx_articles_tsv ON articles USING GIN(tsv);

-- Search query
SELECT
  id,
  title,
  ts_headline('english', tsv, plainto_tsquery('english', $1)) AS highlight,
  ranking
FROM articles,
     to_tsquery('english', $1) query
WHERE tsv @@ query
ORDER BY ts_rank(tsv, query) DESC;
```

## Security - Production Best Practices

### RLS with Service Role Token Swap

```typescript
// For client apps where anon key is used initially
// Exchange for authenticated token after verifying ownership

// Edge Function: supabase/functions/auth-swap/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

serve(async (req) => {
  const { userId, provider, providerToken } = await req.json();

  const supabase = createClient(
    Deno.env.get('SUPABASE_URL')!,
    Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
  );

  // Verify user exists and owns this identity
  const { data: profile } = await supabase
    .from('user_profiles')
    .select('*')
    .eq('id', userId)
    .eq('provider_user_id', providerToken)
    .single();

  if (!profile) {
    return new Response('User not found', { status: 404 });
  }

  // Generate a temporary token with user context
  const { data: { session } } = await supabase.auth.admin.createUserId({
    user_id: userId,
    email: profile.email,
    email_confirm: true
  });

  return new Response(JSON.stringify({
    token: session.access_token,
    user: { id: profile.id, email: profile.email }
  }));
});
```

### XSS Prevention Utilities

```typescript
// utils/sanitize.ts
export function sanitizeHTML(str: string): string {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}

export function sanitizeInput(obj: Record<string, any>): Record<string, any> {
  const sanitized: Record<string, any> = {};

  for (const [key, value] of Object.entries(obj)) {
    if (typeof value === 'string') {
      sanitized[key] = sanitizeHTML(value.trim());
    } else if (typeof value === 'object' && value !== null) {
      sanitized[key] = sanitizeInput(value);
    } else {
      sanitized[key] = value;
    }
  }

  return sanitized;
}

// Sanitize URL parameters
export function sanitizeParam(param: string): string {
  return param.replace(/[^a-zA-Z0-9-_]/g, '');
}
```

### Rate Limiting Middleware

```typescript
// Rate limiter using database for distributed systems
import { supabase } from './supabase';

export async function checkRateLimit(
  identifier: string,
  limit: number = 100,
  windowMs: number = 60000
): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
  const now = new Date();
  const windowStart = new Date(now.getTime() - windowMs);

  // Clean old entries
  await supabase
    .from('rate_limits')
    .delete()
    .lt('window_start', windowStart);

  // Get current count
  const { data: current } = await supabase
    .from('rate_limits')
    .select('count')
    .eq('identifier', identifier)
    .gte('window_start', windowStart)
    .single();

  const count = current?.count || 0;

  if (count >= limit) {
    return {
      allowed: false,
      remaining: 0,
      resetAt: new Date(windowStart.getTime() + windowMs)
    };
  }

  // Increment counter
  await supabase
    .from('rate_limits')
    .upsert({
      identifier,
      count: count + 1,
      window_start: windowStart
    }, {
      onConflict: 'identifier,window_start'
    });

  return {
    allowed: true,
    remaining: limit - count - 1,
    resetAt: new Date(windowStart.getTime() + windowMs)
  };
}
```

## Offline-First Architecture

```typescript
// services/offlineQueue.ts
interface QueuedAction {
  id: string;
  type: string;
  endpoint: string;
  method: 'GET' | 'POST' | 'PUT' | 'DELETE';
  payload?: any;
  timestamp: number;
  retries: number;
}

class OfflineQueue {
  private queue: QueuedAction[] = [];
  private storageKey = 'offline_queue';
  private isOnline: boolean = navigator.onLine;

  constructor() {
    this.loadFromStorage();
    this.setupEventListeners();
  }

  private loadFromStorage() {
    try {
      const stored = localStorage.getItem(this.storageKey);
      if (stored) this.queue = JSON.parse(stored);
    } catch (e) {
      console.error('Failed to load queue:', e);
    }
  }

  private saveToStorage() {
    localStorage.setItem(this.storageKey, JSON.stringify(this.queue));
  }

  private setupEventListeners() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.processQueue();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  add(action: Omit<QueuedAction, 'id' | 'timestamp' | 'retries'>): string {
    const queued: QueuedAction = {
      ...action,
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: Date.now(),
      retries: 0
    };

    this.queue.push(queued);
    this.saveToStorage();

    if (this.isOnline) {
      this.processQueue();
    }

    return queued.id;
  }

  async processQueue(): Promise<{ success: number; failed: number }> {
    if (!this.isOnline || this.queue.length === 0) {
      return { success: 0, failed: 0 };
    }

    let success = 0;
    let failed = 0;

    for (let i = this.queue.length - 1; i >= 0; i--) {
      const action = this.queue[i];

      try {
        await this.executeAction(action);
        this.queue.splice(i, 1);
        success++;
      } catch (error) {
        action.retries++;

        if (action.retries >= 3) {
          this.queue.splice(i, 1);
          console.error('Action failed after 3 retries:', action);
        }

        failed++;
      }
    }

    this.saveToStorage();
    return { success, failed };
  }

  private async executeAction(action: QueuedAction): Promise<Response> {
    const { endpoint, method, payload } = action;

    const response = await fetch(endpoint, {
      method,
      headers: { 'Content-Type': 'application/json' },
      body: payload ? JSON.stringify(payload) : undefined
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    return response;
  }

  getStatus() {
    return {
      queueLength: this.queue.length,
      isOnline: this.isOnline,
      pendingActions: this.queue.map(a => ({ id: a.id, type: a.type }))
    };
  }
}

export const offlineQueue = new OfflineQueue();
```

## Mobile-First Design System

```css
/* :root - Design tokens */
:root {
  /* Brand colors */
  --color-primary: #00B900;
  --color-primary-dark: #009100;
  --color-secondary: #0066FF;

  /* Semantic colors */
  --color-success: #22C55E;
  --color-warning: #F59E0B;
  --color-error: #EF4444;
  --color-info: #3B82F6;

  /* Status colors */
  --status-pending: #F59E0B;
  --status-active: #3B82F6;
  --status-completed: #22C55E;
  --status-cancelled: #EF4444;

  /* Typography */
  --font-sans: system-ui, -apple-system, sans-serif;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Touch targets (WCAG compliant) */
  --touch-target: 44px;

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #111827;
    --color-text: #F9FAFB;
    --color-border: #374151;
  }
}

/* Reset & Base */
*, *::before, *::after {
  box-sizing: border-box;
}

body {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: 1.5;
  color: var(--color-text, #1F2937);
  background-color: var(--color-bg, #FFFFFF);
}

/* Components */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-6);
  font-family: inherit;
  font-size: var(--text-base);
  font-weight: 500;
  line-height: 1;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  text-decoration: none;
  transition: all 0.2s;
  min-height: var(--touch-target);
  min-width: var(--touch-target);
}

.btn-primary {
  background-color: var(--color-primary);
  color: white;
}

.btn-primary:hover { background-color: var(--color-primary-dark); }

.btn-secondary {
  background-color: transparent;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
}

.card {
  background: white;
  border-radius: var(--radius-lg);
  box-shadow: 0 1px 3px rgb(0 0 0 / 0.1);
  padding: var(--space-6);
}

.input {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  font-family: inherit;
  font-size: var(--text-base);
  border: 2px solid var(--color-border, #E5E7EB);
  border-radius: var(--radius-md);
  min-height: var(--touch-target);
}

.input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(0, 185, 0, 0.1);
}

/* Container & Grid */
.container {
  width: 100%;
  padding: var(--space-4);
  margin: 0 auto;
}

@media (min-width: 640px) { .container { max-width: 640px; } }
@media (min-width: 768px) { .container { max-width: 768px; } }
@media (min-width: 1024px) { .container { max-width: 1024px; } }

.grid {
  display: grid;
  gap: var(--space-4);
}
.grid-cols-1 { grid-template-columns: repeat(1, 1fr); }
@media (min-width: 640px) {
  .grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
}
@media (min-width: 1024px) {
  .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
}
```

## Lean Six Sigma - Process Improvement

```python
# lean/six_sigma.py
"""
Six Sigma DMAIC Framework
Apply to any process improvement project
"""

from dataclasses import dataclass
from typing import List, Dict
import pandas as pd

@dataclass
class ProblemStatement:
    """Define Phase"""
    what: str       # What is the problem?
    where: str      # Where does it occur?
    when: str       # When does it occur?
    who: str        # Who is affected?
    impact: str     # Business impact

    def to_statement(self) -> str:
        return f"""Problem: {self.what}
Location: {self.where}
Timing: {self.when}
Affected: {self.who}
Impact: {self.impac}"""

class MeasurePhase:
    """Measure Phase - Data collection & baseline metrics"""

    @staticmethod
    def calculate_dpmo(defects: int, opportunities: int, units: int) -> float:
        """
        Defects Per Million Opportunities
        6σ = 3.4 DPMO, 5σ = 233, 4σ = 6,210, 3σ = 66,807
        """
        return (defects / (opportunities * units)) * 1_000_000

    @staticmethod
    def dpmo_to_sigma(dpmo: float) -> float:
        sigma_map = {3.4: 6, 233: 5, 6210: 4, 66807: 3, 308538: 2}
        return min(sigma_map.items(), key=lambda x: abs(x[0] - dpmo))[1]

    @staticmethod
    def calculate_cp(usl: float, lsl: float, std_dev: float) -> float:
        """Process Capability Index - Cp > 1.33 is capable"""
        return (usl - lsl) / (6 * std_dev)

    @staticmethod
    def calculate_ppk(usl: float, lsl: float, mean: float, std_dev: float) -> float:
        """Process Capability Index with centering"""
        cpu = (usl - mean) / (3 * std_dev)
        cpl = (mean - lsl) / (3 * std_dev)
        return min(cpu, cpl)

class AnalyzePhase:
    """Root Cause Analysis"""

    @staticmethod
    def fishbone_template() -> Dict[str, List[str]]:
        """5M1E categories - customize for your process"""
        return {
            'Man': ['Training', 'Skills', 'Fatigue'],
            'Machine': ['Equipment', 'Tools', 'Maintenance'],
            'Material': ['Quality', 'Supply', 'Specifications'],
            'Method': ['Process', 'SOP', 'Workflow'],
            'Mother Nature': ['Environment', 'Conditions'],
            'Measurement': ['Accuracy', 'Calibration', 'Definitions']
        }

class ImprovePhase:
    """Improvement Implementation"""

    @staticmethod
    def calculate_roi(cost: float, annual_savings: float) -> float:
        """Return on Investment - ROI > 3 is typically good"""
        return (annual_savings - cost) / cost if cost > 0 else 0

    def prioritize_improvements(self, ideas: List[Dict]) -> List[Dict]:
        """Prioritize by ROI and implementation time"""
        for idea in ideas:
            idea['roi'] = self.calculate_roi(idea['cost'], idea['annual_savings'])

        # Quick wins first, then by ROI
        quick_wins = sorted(
          [i for i in ideas if i.get('implementation') == 'quick'],
          key=lambda x: x['roi'], reverse=True
        )
        others = sorted(
          [i for i in ideas if i.get('implementation') != 'quick'],
          key=lambda x: x['roi'], reverse=True
        )
        return quick_wins + others
```

## SaaS Metrics & Business Analytics

```python
# analytics/saas.py
"""
SaaS Metrics Calculator
Track MRR, ARR, LTV, CAC, Churn, NRR
"""

import pandas as pd
from datetime import date, timedelta
from typing import Dict

class SaaSMetrics:
    """Calculate SaaS key performance indicators"""

    def __init__(self, df: pd.DataFrame):
        """
        DataFrame columns: customer_id, subscription_start, subscription_end,
        mrr, plan_tier, expansion_amount, downgrade_amount
        """
        self.df = df

    def calculate_mrr(self) -> Dict:
        """Monthly Recurring Revenue breakdown"""
        active = self.df[
            self.df['subscription_end'].isna() |
            (self.df['subscription_end'] > date.today())
        ]

        return {
            'total_mrr': active['mrr'].sum(),
            'new_mrr': self._new_mrr(),
            'expansion_mrr': self._expansion_mrr(),
            'churn_mrr': self._churn_mrr(),
            'net_new_mrr': (
                self._new_mrr() + self._expansion_mrr() - self._churn_mrr()
            )
        }

    def calculate_arr(self) -> float:
        """Annual Recurring Revenue"""
        return self.calculate_mrr()['total_mrr'] * 12

    def calculate_cac(self, marketing_spend: float, new_customers: int) -> float:
        """Customer Acquisition Cost"""
        return marketing_spend / new_customers if new_customers > 0 else 0

    def calculate_ltv(self, arpu: float, gross_margin: float, churn_rate: float) -> float:
        """
        Customer Lifetime Value
        LTV = (ARPU × Gross Margin) / Churn Rate
        """
        if churn_rate == 0:
            return arpu * 36  # Default to 36 months if no churn
        return (arpu * gross_margin) / churn_rate

    def ltv_cac_ratio(self, ltv: float, cac: float) -> float:
        """
        LTV:CAC Ratio
        < 1: Losing money
        1-3: Breakeven to good
        > 3: Healthy
        """
        return ltv / cac if cac > 0 else 0

    def calculate_churn_rate(self, days: int = 30) -> float:
        """Churn Rate = Churned Customers / Total Customers"""
        cutoff = date.today() - timedelta(days=days)

        total = self.df[self.df['subscription_start'] <= cutoff]
        churned = self.df[
            (self.df['subscription_end'] >= cutoff) &
            (self.df['subscription_end'] <= date.today())
        ]

        return (len(churned) / len(total)) * 100 if len(total) > 0 else 0

    def calculate_arpu(self) -> float:
        """Average Revenue Per User"""
        active = self.df[
            self.df['subscription_end'].isna() |
            (self.df['subscription_end'] > date.today())
        ]
        return active['mrr'].mean() if len(active) > 0 else 0

    def _new_mrr(self) -> float:
        cutoff = date.today().replace(day=1)
        return self.df[self.df['subscription_start'] >= cutoff]['mrr'].sum()

    def _churn_mrr(self) -> float:
        cutoff = date.today().replace(day=1)
        return self.df[
            (self.df['subscription_end'] >= cutoff) &
            (self.df['subscription_end'] <= date.today())
        ]['mrr'].sum()

    def _expansion_mrr(self) -> float:
        # Calculate from expansion_amount column
        return self.df[self.df['subscription_end'].isna()]['expansion_amount'].sum()

# SQL Analytics Queries
sql_templates = {
    'daily_metrics': """
        WITH daily AS (
            SELECT
                created_at::date AS date,
                COUNT(*) AS total_items,
                COUNT(*) FILTER (WHERE status = 'active') AS active_items,
                COUNT(*) FILTER (WHERE status = 'completed') AS completed_items,
                AVG(amount) AS avg_amount
            FROM transactions
            WHERE created_at >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY created_at::date
        )
        SELECT
            date,
            total_items,
            active_items,
            completed_items,
            ROUND((active_items::NUMERIC / NULLIF(total_items, 0)) * 100, 1) AS active_rate
        FROM daily ORDER BY date DESC;
    """,

    'cohort_retention': """
        WITH user_cohorts AS (
            SELECT
                user_id,
                DATE_TRUNC('month', MIN(created_at)) AS cohort_month
            FROM users
            GROUP BY user_id, DATE_TRUNC('month', MIN(created_at))
        ),
        user_activity AS (
            SELECT
                u.user_id,
                u.cohort_month,
                DATE_TRUNC('month', a.created_at) AS activity_month,
                EXTRACT(MONTH FROM AGE(a.created_at, u.cohort_month))::int AS month_number
            FROM user_cohorts u
            JOIN activities a ON a.user_id = u.user_id
            WHERE a.created_at >= u.cohort_month
        )
        SELECT
            cohort_month,
            month_number,
            COUNT(DISTINCT user_id) AS active_users
        FROM user_activity
        GROUP BY cohort_month, month_number
        ORDER BY cohort_month, month_number;
    """,

    'funnel_analysis': """
        WITH funnel_steps AS (
            SELECT 'page_view' AS step, COUNT(DISTINCT user_id) AS count
            FROM page_views WHERE created_at >= CURRENT_DATE
            UNION ALL
            SELECT 'signup' AS step, COUNT(DISTINCT user_id) AS count
            FROM users WHERE created_at >= CURRENT_DATE
            UNION ALL
            SELECT 'purchase' AS step, COUNT(DISTINCT user_id) AS count
            FROM orders WHERE created_at >= CURRENT_DATE
        )
        SELECT
            step,
            count,
            LAG(count) OVER (ORDER BY count DESC) - count AS drop_off,
            ROUND(
                (count::NUMERIC / LAG(count) OVER (ORDER BY count DESC)) * 100,
                1
            ) AS conversion_rate
        FROM funnel_steps
        ORDER BY count DESC;
    """
}
```

---

# PART III: RESOURCES

## Official Documentation

| Category | URL |
|----------|-----|
| **Supabase** | https://supabase.com/docs |
| **PostgreSQL** | https://www.postgresql.org/docs/ |
| **LINE Platform** | https://developers.line.biz/ |
| **React** | https://react.dev |
| **TypeScript** | https://www.typescriptlang.org/docs |
| **Vue** | https://vuejs.org |
| **FastAPI** | https://fastapi.tiangolo.com |
| **Django** | https://docs.djangoproject.com |
| **Playwright** | https://playwright.dev |
| **Google Apps Script** | https://developers.google.com/apps-script |

## Best Practices Reference

| Topic | Key Principles |
|-------|----------------|
| **Database** | Use proper indexes, RLS for security, connection pooling, prepared statements |
| **API Design** | RESTful conventions, proper HTTP status codes, versioning, rate limiting |
| **Frontend** | Mobile-first, accessibility (WCAG), progressive enhancement, error boundaries |
| **Security** | Validate input, sanitize output, use HTTPS, never trust client-side checks |
| **Testing** | Test pyramid: many unit tests, fewer integration, few E2E tests |
| **Performance** | Lazy loading, code splitting, CDN, caching strategies, database query optimization |
| **Error Handling** | Graceful degradation, user-friendly messages, proper logging |
| **Documentation** | README, API docs, code comments for complex logic, changelog |

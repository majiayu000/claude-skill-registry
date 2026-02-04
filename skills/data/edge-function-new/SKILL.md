---
name: edge-function-new
description: "Create a new Supabase Edge Function with Deno"
---

# Create Edge Function

Create a new Supabase Edge Function.

## Function Specification

$ARGUMENTS

## Supabase Edge Functions Overview

Edge Functions run on Deno Deploy (not Node.js):
- TypeScript/JavaScript support
- Run globally at the edge
- Access to Supabase client
- HTTP triggers
- Fast cold starts

## Create Edge Function

### 1. **Initialize Function**

```bash
npx supabase functions new function-name
```

### 2. **Function Structure**

```typescript
// supabase/functions/function-name/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req: Request) => {
  try {
    // 1. Parse request
    const { data } = await req.json()

    // 2. Create Supabase client
    const supabaseClient = createClient(
      Deno.env.get('SUPABASE_URL') ?? '',
      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
      {
        global: {
          headers: {
            Authorization: req.headers.get('Authorization')!
          }
        }
      }
    )

    // 3. Verify user (if needed)
    const {
      data: { user },
      error: authError
    } = await supabaseClient.auth.getUser()

    if (authError || !user) {
      return new Response(
        JSON.stringify({ error: 'Unauthorized' }),
        { status: 401, headers: { 'Content-Type': 'application/json' } }
      )
    }

    // 4. Business logic
    const result = await processData(data, user)

    // 5. Return response
    return new Response(
      JSON.stringify({ data: result }),
      {
        status: 200,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }
    )
  } catch (error) {
    return new Response(
      JSON.stringify({ error: error.message }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    )
  }
})
```

### 3. **Common Use Cases**

**Webhook Handler**
```typescript
serve(async (req) => {
  const signature = req.headers.get('stripe-signature')
  // Verify webhook signature
  // Process event
  return new Response('OK', { status: 200 })
})
```

**Scheduled Function** (with pg_cron)
```typescript
serve(async () => {
  // Run daily cleanup, send emails, etc.
  const supabase = createClient(url, serviceKey)
  await supabase.from('old_records').delete().lt('created_at', oldDate)
  return new Response('Done', { status: 200 })
})
```

**API Proxy/Transform**
```typescript
serve(async (req) => {
  const apiKey = Deno.env.get('THIRD_PARTY_API_KEY')
  const response = await fetch('https://api.example.com/data', {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  })
  const data = await response.json()
  // Transform and return
  return new Response(JSON.stringify(data), { status: 200 })
})
```

### 4. **Testing Locally**

```bash
# Start Supabase locally
npx supabase start

# Serve function locally
npx supabase functions serve function-name

# Test with curl
curl -X POST http://localhost:54321/functions/v1/function-name \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key":"value"}'
```

### 5. **Deploy Function**

```bash
# Deploy to Supabase
npx supabase functions deploy function-name

# Set secrets
npx supabase secrets set API_KEY=your-secret-key

# View logs
npx supabase functions logs function-name
```

### 6. **Calling from Frontend**

```typescript
// Using Supabase client
const { data, error } = await supabase.functions.invoke('function-name', {
  body: { key: 'value' }
})

// Direct fetch
const response = await fetch(
  `${SUPABASE_URL}/functions/v1/function-name`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ key: 'value' })
  }
)
```

### 7. **Best Practices**

**Security**
- Verify user authentication
- Use RLS policies
- Validate all inputs
- Use service role key sparingly
- Set CORS headers correctly

**Performance**
- Keep functions small and focused
- Use streaming for large responses
- Cache when possible
- Handle timeouts (max 150s)

**Error Handling**
- Proper HTTP status codes
- Consistent error format
- Log errors for debugging
- Don't expose sensitive info

**Code Organization**
- One function per file
- Extract utilities to shared folder
- Use TypeScript for type safety
- Import from Deno-compatible URLs

### 8. **Environment Variables**

```bash
# Set locally
echo "API_KEY=secret" > supabase/functions/.env

# Set in production
npx supabase secrets set API_KEY=secret

# Access in function
const apiKey = Deno.env.get('API_KEY')
```

### 9. **CORS Handling**

```typescript
serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST',
        'Access-Control-Allow-Headers': 'authorization, content-type'
      }
    })
  }
  // Handle request
})
```

Generate production-ready Edge Functions with proper error handling, authentication, and type safety.

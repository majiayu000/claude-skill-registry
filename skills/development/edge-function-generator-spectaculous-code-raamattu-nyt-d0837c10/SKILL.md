---
name: edge-function-generator
description: Expert assistant for creating and maintaining Supabase Edge Functions for the KR92 Bible Voice project. Use when creating Edge Functions, setting up CORS, integrating shared modules, adding JWT validation, or configuring environment variables.
---

# Edge Function Generator

## Capabilities
- Scaffold new Edge Functions with proper structure
- Set up CORS headers and error handling
- Integrate shared modules (_shared/)
- Add JWT validation and logging
- Configure environment variables

## Edge Function Structure

### Location
```
supabase/functions/
├── _shared/              # Shared modules
│   ├── ai-prompt.ts
│   ├── ai-config.ts
│   └── ai-providers.ts
├── function-name/
│   └── index.ts
```

### Deployment
- Lovable Cloud: Auto-deploy on save
- Manual: `supabase functions deploy function-name`

## Usage Examples

### Example 1: Create Basic Edge Function
**User:** "Create a new edge function to get verse of the day"

**Assistant:**
```typescript
// supabase/functions/verse-of-the-day/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Initialize Supabase client
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey);

    // Get today's day of year
    const now = new Date();
    const start = new Date(now.getFullYear(), 0, 0);
    const diff = now.getTime() - start.getTime();
    const dayOfYear = Math.floor(diff / (1000 * 60 * 60 * 24));

    // Get verse (use modulo to cycle through verses)
    const { data: verses, error } = await supabase
      .from('verses')
      .select('id, text, osis, books(name_fi)')
      .eq('version_id', 'finstlk201-uuid')
      .limit(1)
      .range(dayOfYear % 31102, dayOfYear % 31102); // Total verses in Bible

    if (error) throw error;

    const verse = verses?.[0];
    if (!verse) throw new Error('No verse found');

    return new Response(
      JSON.stringify({
        success: true,
        verse: {
          text: verse.text,
          reference: verse.osis,
          book: verse.books?.name_fi
        }
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    );
  } catch (error) {
    console.error('Error:', error);
    return new Response(
      JSON.stringify({
        success: false,
        error: error.message
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      }
    );
  }
});
```

### Example 2: Edge Function with JWT Authentication
**User:** "Create edge function for user to save custom bookmark with note"

**Assistant:**
```typescript
// supabase/functions/save-bookmark-with-note/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface RequestBody {
  verse_id: string;
  osis: string;
  note?: string;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Get JWT token from header
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      throw new Error('Missing authorization header');
    }

    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey, {
      global: {
        headers: { Authorization: authHeader },
      },
    });

    // Get authenticated user
    const { data: { user }, error: userError } = await supabase.auth.getUser();
    if (userError || !user) {
      throw new Error('Unauthorized');
    }

    // Parse request body
    const body: RequestBody = await req.json();
    const { verse_id, osis, note } = body;

    if (!verse_id || !osis) {
      throw new Error('Missing required fields: verse_id, osis');
    }

    // Save bookmark
    const { data: bookmark, error: bookmarkError } = await supabase
      .from('bookmarks')
      .insert({
        user_id: user.id,
        verse_id,
        osis,
      })
      .select()
      .single();

    if (bookmarkError) throw bookmarkError;

    // Save note if provided
    let noteData = null;
    if (note) {
      const { data, error: noteError } = await supabase
        .from('user_notes')
        .insert({
          user_id: user.id,
          verse_id,
          osis,
          note_text: note,
        })
        .select()
        .single();

      if (noteError) throw noteError;
      noteData = data;
    }

    return new Response(
      JSON.stringify({
        success: true,
        bookmark,
        note: noteData,
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    );
  } catch (error) {
    console.error('Error:', error);

    const status = error.message === 'Unauthorized' ? 401 : 500;

    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status,
      }
    );
  }
});
```

### Example 3: Edge Function with AI Integration
**User:** "Create edge function for AI-powered verse explanation"

**Assistant:**
```typescript
// supabase/functions/explain-verse/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { getPrompt } from '../_shared/ai-prompt.ts';
import { getFeatureConfig } from '../_shared/ai-config.ts';
import { callAIProvider } from '../_shared/ai-providers.ts';

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface RequestBody {
  verse_id: string;
  osis: string;
  context?: string;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  const startTime = Date.now();

  try {
    const authHeader = req.headers.get('Authorization');
    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const supabase = createClient(supabaseUrl, supabaseKey, {
      global: { headers: authHeader ? { Authorization: authHeader } : {} },
    });

    // Get user (optional for this feature)
    const { data: { user } } = await supabase.auth.getUser();

    // Parse request
    const body: RequestBody = await req.json();
    const { verse_id, osis, context } = body;

    // Get verse text
    const { data: verse, error: verseError } = await supabase
      .from('verses')
      .select('text, books(name_fi), chapter_number, verse_number')
      .eq('id', verse_id)
      .single();

    if (verseError) throw verseError;

    // Get AI configuration
    const featureConfig = await getFeatureConfig(supabase, 'explain_verse', 'prod');
    if (!featureConfig) {
      throw new Error('AI feature not configured');
    }

    // Get prompt template
    const prompt = await getPrompt(supabase, 'explain_verse', {
      verse_text: verse.text,
      reference: osis,
      context: context || 'general Bible study',
    }, 'prod');

    // Call AI provider
    const aiResponse = await callAIProvider(
      featureConfig.ai_vendor,
      featureConfig.ai_model,
      prompt.systemPrompt,
      prompt.userPrompt,
      {
        temperature: featureConfig.param_overrides?.temperature || 0.7,
        max_tokens: featureConfig.param_overrides?.max_tokens || 500,
      }
    );

    const latencyMs = Date.now() - startTime;

    // Log usage
    await supabase.from('ai_usage_logs').insert({
      user_id: user?.id || null,
      actor_type: user ? 'user' : 'system',
      feature: 'explain_verse',
      context_id: verse_id,
      context_ref: osis,
      ai_vendor: featureConfig.ai_vendor,
      ai_model: featureConfig.ai_model,
      prompt_tokens: aiResponse.usage.promptTokens,
      completion_tokens: aiResponse.usage.completionTokens,
      total_tokens: aiResponse.usage.totalTokens,
      cost_usd: aiResponse.cost,
      latency_ms: latencyMs,
      status: 'success',
      prompt_version_id: prompt.versionId,
    });

    return new Response(
      JSON.stringify({
        success: true,
        explanation: aiResponse.content,
        verse: {
          text: verse.text,
          reference: osis,
          book: verse.books?.name_fi,
        },
        metadata: {
          model: featureConfig.ai_model,
          latencyMs,
          tokens: aiResponse.usage.totalTokens,
        },
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 200,
      }
    );
  } catch (error) {
    console.error('Error:', error);

    return new Response(
      JSON.stringify({
        success: false,
        error: error.message,
      }),
      {
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
        status: 500,
      }
    );
  }
});
```

## Edge Function Templates

### Minimal Template
```typescript
import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    // Your logic here

    return new Response(
      JSON.stringify({ success: true }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});
```

### With Authentication
```typescript
const { data: { user }, error: userError } = await supabase.auth.getUser();
if (userError || !user) {
  throw new Error('Unauthorized');
}
```

### With Request Validation
```typescript
const body = await req.json();

// Validate required fields
const required = ['field1', 'field2'];
for (const field of required) {
  if (!body[field]) {
    throw new Error(`Missing required field: ${field}`);
  }
}
```

## Common Patterns

### 1. CORS Headers
Always include for client access:
```typescript
const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};
```

### 2. Error Handling
```typescript
try {
  // Logic
} catch (error) {
  console.error('Error:', error);
  return new Response(
    JSON.stringify({ success: false, error: error.message }),
    { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
  );
}
```

### 3. Supabase Client
```typescript
const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
const supabase = createClient(supabaseUrl, supabaseKey);
```

### 4. Environment Variables
```typescript
const apiKey = Deno.env.get('EXTERNAL_API_KEY');
if (!apiKey) {
  throw new Error('Missing API key configuration');
}
```

## Deployment

### Via Lovable Cloud
- Save file → auto-deploys
- View logs in Supabase Dashboard

### Via CLI
```bash
supabase functions deploy function-name
```

### Test Locally
```bash
supabase functions serve function-name
```

## Testing Edge Functions

### cURL Test
```bash
curl -X POST https://project.supabase.co/functions/v1/function-name \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"key": "value"}'
```

### TypeScript Test
```typescript
const { data, error } = await supabase.functions.invoke('function-name', {
  body: { key: 'value' }
});
```

## Related Documentation
- See `Docs/02-DESIGN.md` for Edge Functions overview
- See `Docs/06-AI-ARCHITECTURE.md` for AI integration patterns

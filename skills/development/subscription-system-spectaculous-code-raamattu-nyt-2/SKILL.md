---
name: subscription-system
description: Expert assistant for designing and implementing subscription features across the Raamattu Nyt monorepo. Use when adding feature limits, implementing quota checks, creating plan-based access controls, building upgrade flows, or extending the subscription system.
---

# Subscription System Developer

## Context Files (Read First)

For schema and plan details, read from `Docs/context/`:
- `Docs/context/db-schema-short.md` - Quota tables and structures
- `Docs/context/supabase-map.md` - RPC functions for quotas

## Capabilities
- Design and implement feature gating with plan-based access
- Create database migrations for quota tables and usage tracking
- Build React hooks for subscription state management
- Implement Edge Function quota enforcement
- Create upgrade modal flows and UI components
- Extend quota system for new feature types (tokens, counts, size limits)

## Reference Documentation
**Primary:** `Docs/13-SUBSCRIPTION-SYSTEM.md`

## Architecture Overview

### Plan Tiers
| Plan | Target | AI Tokens | Feature Access |
|------|--------|-----------|----------------|
| `unauth` | Guests | 2,000 | Very limited |
| `basic` | Free users | 10,000 | Moderate |
| `pro` | Paid | 50,000 | Full |
| `premium` | Top tier | 200,000 | Full + extras |
| `admin` | Admins | Unlimited | All |

### Limit Types
| Type | Window | Example |
|------|--------|---------|
| `tokens` | `rolling` | AI features (6-hour window) |
| `count` | `lifetime` | Max notes per user |
| `count` | `monthly` | PDF exports per month |
| `size` | `none` | Max content length |
| `boolean` | `none` | Feature on/off |

## Usage Examples

### Example 1: Add New Feature with Count Limit
**User:** "Add user notes feature with 50 notes limit for basic plan"

**Assistant:**

#### Step 1: Database Migration
```sql
-- Migration: YYYYMMDDHHMMSS_add_user_notes_with_limits.sql

-- Create user_notes table
CREATE TABLE public.user_notes (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  verse_id text NOT NULL,  -- OSIS reference
  content text NOT NULL,
  content_length integer GENERATED ALWAYS AS (length(content)) STORED,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE (user_id, verse_id)
);

-- Enable RLS
ALTER TABLE public.user_notes ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view own notes"
ON public.user_notes FOR SELECT
USING (user_id = auth.uid());

CREATE POLICY "Users can create own notes"
ON public.user_notes FOR INSERT
WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own notes"
ON public.user_notes FOR UPDATE
USING (user_id = auth.uid());

CREATE POLICY "Users can delete own notes"
ON public.user_notes FOR DELETE
USING (user_id = auth.uid());

-- Indexes
CREATE INDEX idx_user_notes_user_id ON public.user_notes(user_id);
CREATE INDEX idx_user_notes_verse_id ON public.user_notes(verse_id);

-- Trigger for updated_at
CREATE TRIGGER set_user_notes_updated_at
BEFORE UPDATE ON public.user_notes
FOR EACH ROW
EXECUTE FUNCTION public.handle_updated_at();

-- Add quota entries for user-notes feature
INSERT INTO bible_schema.ai_plan_quotas (plan_key, feature_key, tokens_per_window, enabled) VALUES
  ('unauth', 'user-notes', 0, false),      -- Locked
  ('basic', 'user-notes', 50, true),       -- 50 notes max
  ('pro', 'user-notes', 500, true),        -- 500 notes max
  ('premium', 'user-notes', 999999, true), -- Effectively unlimited
  ('admin', 'user-notes', 999999999, true);

-- RPC to check if user can create note
CREATE OR REPLACE FUNCTION public.can_create_note(p_content_length integer DEFAULT 0)
RETURNS jsonb
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
SET search_path = 'public', 'bible_schema'
AS $$
DECLARE
  v_user_id uuid;
  v_plan_key text;
  v_note_limit integer;
  v_size_limit integer;
  v_current_count integer;
  v_enabled boolean;
BEGIN
  v_user_id := auth.uid();

  -- Get plan
  v_plan_key := bible_schema.get_effective_plan(v_user_id);

  -- Get quota config
  SELECT tokens_per_window, enabled
  INTO v_note_limit, v_enabled
  FROM bible_schema.ai_plan_quotas
  WHERE plan_key = v_plan_key AND feature_key = 'user-notes';

  -- Check if feature enabled
  IF NOT COALESCE(v_enabled, false) THEN
    RETURN jsonb_build_object(
      'allowed', false,
      'reason', CASE WHEN v_user_id IS NULL THEN 'auth_required' ELSE 'feature_locked' END,
      'current', 0,
      'limit', 0,
      'upgrade_suggestion', CASE
        WHEN v_plan_key = 'unauth' THEN 'basic'
        WHEN v_plan_key = 'basic' THEN 'pro'
        ELSE 'premium'
      END
    );
  END IF;

  -- Get current note count
  SELECT COUNT(*) INTO v_current_count
  FROM public.user_notes
  WHERE user_id = v_user_id;

  -- Size limit per plan
  v_size_limit := CASE v_plan_key
    WHEN 'basic' THEN 2000
    WHEN 'pro' THEN 10000
    WHEN 'premium' THEN 50000
    ELSE 50000
  END;

  -- Check count limit
  IF v_current_count >= v_note_limit THEN
    RETURN jsonb_build_object(
      'allowed', false,
      'reason', 'limit_reached',
      'current', v_current_count,
      'limit', v_note_limit,
      'upgrade_suggestion', CASE
        WHEN v_plan_key = 'basic' THEN 'pro'
        ELSE 'premium'
      END
    );
  END IF;

  -- Check size limit
  IF p_content_length > v_size_limit THEN
    RETURN jsonb_build_object(
      'allowed', false,
      'reason', 'size_exceeded',
      'current', p_content_length,
      'limit', v_size_limit,
      'upgrade_suggestion', CASE
        WHEN v_plan_key = 'basic' THEN 'pro'
        ELSE 'premium'
      END
    );
  END IF;

  RETURN jsonb_build_object(
    'allowed', true,
    'reason', 'ok',
    'current', v_current_count,
    'limit', v_note_limit,
    'remaining', v_note_limit - v_current_count,
    'size_limit', v_size_limit
  );
END;
$$;

GRANT EXECUTE ON FUNCTION public.can_create_note TO authenticated, anon;
```

#### Step 2: React Hook
```typescript
// apps/raamattu-nyt/src/hooks/useUserNotes.ts

import { useAuth } from "@shared-auth/hooks/useAuth";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import type { PlanKey } from "@/components/ai-quota";
import { supabase } from "@/integrations/supabase/client";

interface NoteCheckResult {
  allowed: boolean;
  reason: 'ok' | 'limit_reached' | 'size_exceeded' | 'feature_locked' | 'auth_required';
  current: number;
  limit: number;
  remaining?: number;
  size_limit?: number;
  upgrade_suggestion?: PlanKey;
}

interface UserNote {
  id: string;
  verse_id: string;
  content: string;
  content_length: number;
  created_at: string;
  updated_at: string;
}

interface UpgradeModalState {
  open: boolean;
  variant: "limit-reached" | "feature-locked" | "unauth";
  featureName?: string;
  requiredPlan?: PlanKey;
}

export function useUserNotes() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [upgradeModalState, setUpgradeModalState] = useState<UpgradeModalState>({
    open: false,
    variant: "limit-reached",
  });

  // Fetch user's notes
  const { data: notes, isLoading, refetch } = useQuery<UserNote[]>({
    queryKey: ["user-notes", user?.id],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("user_notes")
        .select("*")
        .order("created_at", { ascending: false });

      if (error) throw error;
      return data;
    },
    enabled: !!user,
  });

  // Check if can create note
  const checkCanCreate = async (contentLength: number = 0): Promise<NoteCheckResult> => {
    const { data, error } = await (supabase.rpc as any)("can_create_note", {
      p_content_length: contentLength,
    });

    if (error) throw error;
    return data as NoteCheckResult;
  };

  // Create note mutation
  const createNote = useMutation({
    mutationFn: async ({ verseId, content }: { verseId: string; content: string }) => {
      // Pre-flight check
      const check = await checkCanCreate(content.length);

      if (!check.allowed) {
        // Show appropriate modal
        if (check.reason === 'auth_required') {
          setUpgradeModalState({ open: true, variant: 'unauth' });
        } else if (check.reason === 'feature_locked') {
          setUpgradeModalState({
            open: true,
            variant: 'feature-locked',
            featureName: 'Notes',
            requiredPlan: check.upgrade_suggestion
          });
        } else {
          setUpgradeModalState({
            open: true,
            variant: 'limit-reached',
            featureName: 'Notes',
            requiredPlan: check.upgrade_suggestion
          });
        }
        throw new Error(check.reason);
      }

      const { data, error } = await supabase
        .from("user_notes")
        .upsert({
          user_id: user!.id,
          verse_id: verseId,
          content
        })
        .select()
        .single();

      if (error) throw error;
      return data;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user-notes"] });
    },
  });

  // Delete note mutation
  const deleteNote = useMutation({
    mutationFn: async (noteId: string) => {
      const { error } = await supabase
        .from("user_notes")
        .delete()
        .eq("id", noteId);

      if (error) throw error;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["user-notes"] });
    },
  });

  // Check and prompt pattern
  const checkOrPrompt = async (contentLength: number = 0): Promise<boolean> => {
    const check = await checkCanCreate(contentLength);

    if (!check.allowed) {
      if (check.reason === 'auth_required') {
        setUpgradeModalState({ open: true, variant: 'unauth' });
      } else if (check.reason === 'feature_locked') {
        setUpgradeModalState({
          open: true,
          variant: 'feature-locked',
          featureName: 'Notes',
          requiredPlan: check.upgrade_suggestion
        });
      } else {
        setUpgradeModalState({
          open: true,
          variant: 'limit-reached',
          featureName: 'Notes',
          requiredPlan: check.upgrade_suggestion
        });
      }
      return false;
    }
    return true;
  };

  return {
    notes: notes || [],
    loading: isLoading,

    // CRUD operations
    createNote: createNote.mutateAsync,
    deleteNote: deleteNote.mutateAsync,

    // Check functions
    checkCanCreate,
    checkOrPrompt,

    // Modal management
    upgradeModalState,
    hideUpgradeModal: () => setUpgradeModalState(prev => ({ ...prev, open: false })),

    refetch,
  };
}
```

#### Step 3: Component Integration
```typescript
// Usage in VerseActions.tsx

import { useUserNotes } from "@/hooks/useUserNotes";
import { UpgradeModal } from "@/components/ai-quota";

function VerseActions({ verse }: { verse: Verse }) {
  const { checkOrPrompt, createNote, upgradeModalState, hideUpgradeModal } = useUserNotes();
  const [noteContent, setNoteContent] = useState("");

  const handleSaveNote = async () => {
    // Single function call: checks limit AND shows modal if denied
    if (!await checkOrPrompt(noteContent.length)) return;

    await createNote({ verseId: verse.osis, content: noteContent });
    setNoteContent("");
  };

  return (
    <>
      <Button onClick={handleSaveNote}>Save Note</Button>

      <UpgradeModal
        open={upgradeModalState.open}
        onOpenChange={hideUpgradeModal}
        variant={upgradeModalState.variant === 'unauth' ? 'unauth' : 'feature-locked'}
        currentPlan="basic"
        featureName={upgradeModalState.featureName}
        requiredPlan={upgradeModalState.requiredPlan}
      />
    </>
  );
}
```

---

### Example 2: Add Notification Channel Feature
**User:** "Add WhatsApp notification integration for pro users"

**Assistant:**

#### Step 1: Database Migration
```sql
-- Migration: YYYYMMDDHHMMSS_add_notification_preferences.sql

-- Create notification_preferences table
CREATE TABLE public.notification_preferences (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  channel text NOT NULL CHECK (channel IN ('email', 'whatsapp', 'telegram', 'push')),
  enabled boolean DEFAULT false,
  frequency text CHECK (frequency IN ('daily', 'weekly', 'instant')),
  phone_number text,           -- For WhatsApp/Telegram
  telegram_chat_id text,       -- Telegram specific
  preferences jsonb DEFAULT '{}',
  verified_at timestamptz,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  UNIQUE (user_id, channel)
);

-- Create notification_queue table
CREATE TABLE public.notification_queue (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  channel text NOT NULL,
  payload jsonb NOT NULL,
  scheduled_for timestamptz NOT NULL,
  sent_at timestamptz,
  status text DEFAULT 'pending' CHECK (status IN ('pending', 'sent', 'failed', 'cancelled')),
  error_message text,
  retry_count integer DEFAULT 0,
  created_at timestamptz DEFAULT now()
);

-- Enable RLS
ALTER TABLE public.notification_preferences ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.notification_queue ENABLE ROW LEVEL SECURITY;

-- RLS for preferences
CREATE POLICY "Users can manage own notification preferences"
ON public.notification_preferences FOR ALL
USING (user_id = auth.uid());

-- RLS for queue (users can view their own)
CREATE POLICY "Users can view own notification queue"
ON public.notification_queue FOR SELECT
USING (user_id = auth.uid());

-- Add quota entries for notification channels
INSERT INTO bible_schema.ai_plan_quotas (plan_key, feature_key, tokens_per_window, enabled) VALUES
  -- Email: basic+
  ('unauth', 'notifications-email', 0, false),
  ('basic', 'notifications-email', 1, true),
  ('pro', 'notifications-email', 1, true),
  ('premium', 'notifications-email', 1, true),
  ('admin', 'notifications-email', 1, true),

  -- WhatsApp: pro+
  ('unauth', 'notifications-whatsapp', 0, false),
  ('basic', 'notifications-whatsapp', 0, false),
  ('pro', 'notifications-whatsapp', 1, true),
  ('premium', 'notifications-whatsapp', 1, true),
  ('admin', 'notifications-whatsapp', 1, true),

  -- Telegram: pro+
  ('unauth', 'notifications-telegram', 0, false),
  ('basic', 'notifications-telegram', 0, false),
  ('pro', 'notifications-telegram', 1, true),
  ('premium', 'notifications-telegram', 1, true),
  ('admin', 'notifications-telegram', 1, true);

-- RPC to check notification channel access
CREATE OR REPLACE FUNCTION public.can_use_notification_channel(p_channel text)
RETURNS jsonb
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
AS $$
DECLARE
  v_user_id uuid;
  v_plan_key text;
  v_enabled boolean;
  v_feature_key text;
BEGIN
  v_user_id := auth.uid();
  v_plan_key := bible_schema.get_effective_plan(v_user_id);
  v_feature_key := 'notifications-' || p_channel;

  SELECT enabled INTO v_enabled
  FROM bible_schema.ai_plan_quotas
  WHERE plan_key = v_plan_key AND feature_key = v_feature_key;

  IF NOT COALESCE(v_enabled, false) THEN
    RETURN jsonb_build_object(
      'allowed', false,
      'reason', CASE
        WHEN v_user_id IS NULL THEN 'auth_required'
        ELSE 'feature_locked'
      END,
      'channel', p_channel,
      'plan_key', v_plan_key,
      'required_plan', CASE
        WHEN p_channel IN ('whatsapp', 'telegram') THEN 'pro'
        ELSE 'basic'
      END
    );
  END IF;

  RETURN jsonb_build_object(
    'allowed', true,
    'reason', 'ok',
    'channel', p_channel,
    'plan_key', v_plan_key
  );
END;
$$;

GRANT EXECUTE ON FUNCTION public.can_use_notification_channel TO authenticated, anon;
```

#### Step 2: Edge Function for WhatsApp
```typescript
// supabase/functions/send-whatsapp-notification/index.ts

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2";

const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
};

interface WhatsAppPayload {
  phone_number: string;
  message: string;
  template_name?: string;
  template_params?: Record<string, string>;
}

serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders });
  }

  try {
    const authHeader = req.headers.get('Authorization');
    if (!authHeader) {
      throw new Error('Missing authorization');
    }

    const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
    const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;
    const twilioAccountSid = Deno.env.get('TWILIO_ACCOUNT_SID');
    const twilioAuthToken = Deno.env.get('TWILIO_AUTH_TOKEN');
    const twilioWhatsAppFrom = Deno.env.get('TWILIO_WHATSAPP_FROM');

    const supabase = createClient(supabaseUrl, supabaseKey, {
      global: { headers: { Authorization: authHeader } },
    });

    // Get user
    const { data: { user }, error: userError } = await supabase.auth.getUser();
    if (userError || !user) {
      throw new Error('Unauthorized');
    }

    // Check feature access
    const { data: accessCheck } = await supabase.rpc('can_use_notification_channel', {
      p_channel: 'whatsapp'
    });

    if (!accessCheck?.allowed) {
      return new Response(
        JSON.stringify({
          success: false,
          error_code: 'FEATURE_LOCKED',
          error: 'WhatsApp notifications require Pro plan',
          required_plan: accessCheck?.required_plan
        }),
        { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 403 }
      );
    }

    // Get user's WhatsApp preference
    const { data: pref } = await supabase
      .from('notification_preferences')
      .select('phone_number, verified_at')
      .eq('user_id', user.id)
      .eq('channel', 'whatsapp')
      .single();

    if (!pref?.phone_number || !pref?.verified_at) {
      throw new Error('WhatsApp not configured or verified');
    }

    const body: WhatsAppPayload = await req.json();

    // Send via Twilio
    const twilioUrl = `https://api.twilio.com/2010-04-01/Accounts/${twilioAccountSid}/Messages.json`;

    const formData = new URLSearchParams();
    formData.append('From', `whatsapp:${twilioWhatsAppFrom}`);
    formData.append('To', `whatsapp:${pref.phone_number}`);
    formData.append('Body', body.message);

    const twilioResponse = await fetch(twilioUrl, {
      method: 'POST',
      headers: {
        'Authorization': 'Basic ' + btoa(`${twilioAccountSid}:${twilioAuthToken}`),
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    const result = await twilioResponse.json();

    if (!twilioResponse.ok) {
      throw new Error(result.message || 'Failed to send WhatsApp message');
    }

    // Log to queue
    await supabase.from('notification_queue').insert({
      user_id: user.id,
      channel: 'whatsapp',
      payload: body,
      scheduled_for: new Date().toISOString(),
      sent_at: new Date().toISOString(),
      status: 'sent',
    });

    return new Response(
      JSON.stringify({ success: true, message_sid: result.sid }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
    );

  } catch (error) {
    console.error('Error:', error);
    return new Response(
      JSON.stringify({ success: false, error: error.message }),
      { headers: { ...corsHeaders, 'Content-Type': 'application/json' }, status: 500 }
    );
  }
});
```

---

### Example 3: Extend Quota Table for New Limit Types
**User:** "Modify quota system to support count and size limits"

**Assistant:**

```sql
-- Migration: YYYYMMDDHHMMSS_extend_quota_system.sql

-- Add limit_type column
ALTER TABLE bible_schema.ai_plan_quotas
ADD COLUMN IF NOT EXISTS limit_type text DEFAULT 'tokens'
CHECK (limit_type IN ('tokens', 'count', 'size', 'boolean'));

-- Add window_type column
ALTER TABLE bible_schema.ai_plan_quotas
ADD COLUMN IF NOT EXISTS window_type text DEFAULT 'rolling'
CHECK (window_type IN ('rolling', 'monthly', 'lifetime', 'none'));

-- Add size_limit column for size-based limits
ALTER TABLE bible_schema.ai_plan_quotas
ADD COLUMN IF NOT EXISTS size_limit integer;

-- Update comments
COMMENT ON COLUMN bible_schema.ai_plan_quotas.limit_type IS
'Type of limit: tokens (AI usage), count (item count), size (bytes/chars), boolean (on/off)';

COMMENT ON COLUMN bible_schema.ai_plan_quotas.window_type IS
'Time window: rolling (N minutes), monthly (calendar), lifetime (forever), none (no tracking)';

-- Create unified feature check function
CREATE OR REPLACE FUNCTION bible_schema.can_use_feature(
  p_feature_key text,
  p_amount integer DEFAULT 1
)
RETURNS jsonb
LANGUAGE plpgsql
STABLE
SECURITY DEFINER
SET search_path = 'bible_schema', 'public'
AS $$
DECLARE
  v_user_id uuid;
  v_plan_key text;
  v_quota record;
  v_current_usage integer;
  v_window_start timestamptz;
  v_allowed boolean;
  v_deny_reason text;
BEGIN
  v_user_id := auth.uid();
  v_plan_key := bible_schema.get_effective_plan(v_user_id);

  -- Get quota configuration
  SELECT * INTO v_quota
  FROM bible_schema.ai_plan_quotas
  WHERE plan_key = v_plan_key AND feature_key = p_feature_key;

  -- No config = denied
  IF v_quota IS NULL THEN
    RETURN jsonb_build_object(
      'allowed', false,
      'reason', 'feature_not_configured',
      'plan_key', v_plan_key
    );
  END IF;

  -- Feature disabled
  IF NOT v_quota.enabled THEN
    RETURN jsonb_build_object(
      'allowed', false,
      'reason', CASE WHEN v_user_id IS NULL THEN 'auth_required' ELSE 'feature_locked' END,
      'plan_key', v_plan_key,
      'upgrade_suggestion', CASE
        WHEN v_plan_key = 'unauth' THEN 'basic'
        WHEN v_plan_key = 'basic' THEN 'pro'
        ELSE 'premium'
      END
    );
  END IF;

  -- Boolean type: just check enabled
  IF v_quota.limit_type = 'boolean' THEN
    RETURN jsonb_build_object(
      'allowed', true,
      'reason', 'ok',
      'plan_key', v_plan_key
    );
  END IF;

  -- Calculate window
  v_window_start := CASE v_quota.window_type
    WHEN 'rolling' THEN
      now() - (COALESCE(public.get_app_setting('ai_quota_window_minutes', '360')::integer, 360) || ' minutes')::interval
    WHEN 'monthly' THEN
      date_trunc('month', now())
    WHEN 'lifetime' THEN
      '-infinity'::timestamptz
    ELSE
      '-infinity'::timestamptz
  END;

  -- Get current usage based on limit type
  IF v_quota.limit_type = 'tokens' THEN
    SELECT COALESCE(SUM(total_tokens), 0) INTO v_current_usage
    FROM bible_schema.ai_usage_logs
    WHERE feature = p_feature_key
      AND created_at >= v_window_start
      AND status = 'success'
      AND ((v_user_id IS NULL AND user_id IS NULL) OR user_id = v_user_id);
  ELSIF v_quota.limit_type = 'count' THEN
    -- Count from feature-specific table (customize per feature)
    v_current_usage := 0; -- Override in feature-specific functions
  ELSIF v_quota.limit_type = 'size' THEN
    v_current_usage := p_amount; -- Size check is immediate
  END IF;

  -- Check limit
  v_allowed := (v_current_usage + p_amount) <= v_quota.tokens_per_window;

  IF NOT v_allowed THEN
    v_deny_reason := CASE v_quota.limit_type
      WHEN 'tokens' THEN 'quota_exceeded'
      WHEN 'count' THEN 'limit_reached'
      WHEN 'size' THEN 'size_exceeded'
      ELSE 'quota_exceeded'
    END;
  END IF;

  RETURN jsonb_build_object(
    'allowed', v_allowed,
    'reason', COALESCE(v_deny_reason, 'ok'),
    'current', v_current_usage,
    'limit', v_quota.tokens_per_window,
    'remaining', GREATEST(0, v_quota.tokens_per_window - v_current_usage),
    'limit_type', v_quota.limit_type,
    'window_type', v_quota.window_type,
    'plan_key', v_plan_key,
    'upgrade_suggestion', CASE
      WHEN NOT v_allowed THEN
        CASE WHEN v_plan_key = 'basic' THEN 'pro' ELSE 'premium' END
      ELSE NULL
    END
  );
END;
$$;

GRANT EXECUTE ON FUNCTION bible_schema.can_use_feature TO authenticated, anon;
```

---

## Unified Pattern: checkOrPrompt

The recommended pattern for all gated features:

```typescript
// Hook provides checkOrPrompt function
const { checkOrPrompt } = useFeatureHook();

// In component - single call handles everything:
// 1. Checks if feature allowed
// 2. Shows appropriate modal if denied
// 3. Returns boolean for flow control
const handleAction = async () => {
  if (!await checkOrPrompt()) return;  // Modal shown automatically

  // Proceed with action
  await performAction();
};
```

This pattern:
- Reduces boilerplate in components
- Ensures consistent upgrade flow
- Handles all deny reasons (auth, locked, quota, limit)
- Works for all feature types

## Key Files

| File | Purpose |
|------|---------|
| `Docs/13-SUBSCRIPTION-SYSTEM.md` | Full system documentation |
| `supabase/migrations/20260107180305_*.sql` | AI quota core schema |
| `supabase/migrations/20260107180306_*.sql` | Quota RPC functions |
| `apps/raamattu-nyt/src/hooks/useAIQuota.ts` | AI quota hook (reference) |
| `apps/raamattu-nyt/src/components/ai-quota/` | UI components |
| `packages/shared-auth/` | Shared auth hooks |

## Checklist for New Features

- [ ] Add quota entries to `ai_plan_quotas` for all 5 plans
- [ ] Create RPC function for feature-specific checks
- [ ] Build React hook with `checkOrPrompt` pattern
- [ ] Integrate UpgradeModal in component
- [ ] Add feature to PlansComparison component
- [ ] Update admin panel if needed
- [ ] Add feature to `13-SUBSCRIPTION-SYSTEM.md`
- [ ] Test all plan tiers (unauth, basic, pro, premium, admin)

## Related Skills
- `supabase-migration-writer` - Database migrations
- `edge-function-generator` - Edge Functions
- `admin-panel-builder` - Admin UI
- `rls-policy-validator` - RLS security

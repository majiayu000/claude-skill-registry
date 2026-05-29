---
name: supabase
category: database
version: 2.0.0
description: Supabase patterns with Australian context and Privacy Act 1988 compliance
author: Unite Group
priority: 3
triggers:
  - supabase
  - database
  - auth
  - postgres
---

# Supabase Patterns

## Client Setup

```typescript
import { createBrowserClient } from '@supabase/ssr'
import { createServerClient } from '@supabase/ssr'

// Browser client
const supabase = createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Server client (Next.js App Router)
const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
        cookies: {
            getAll() {
                return request.cookies.getAll()
            },
            setAll(cookiesToSet) {
                cookiesToSet.forEach(({ name, value, options }) =>
                    request.cookies.set(name, value)
                )
            },
        },
    }
)
```

## Authentication

```typescript
// Sign up (Australian user)
const { data, error } = await supabase.auth.signUp({
    email: 'user@example.com.au',
    password: 'securePassword123',
    options: {
        emailRedirectTo: 'https://unite-group.com.au/auth/callback',
        data: {
            locale: 'en-AU',
            timezone: 'Australia/Brisbane',
            country: 'Australia'
        }
    }
})

// Sign in
const { data, error } = await supabase.auth.signInWithPassword({
    email: 'user@example.com.au',
    password: 'securePassword123'
})

// Get current user
const { data: { user }, error } = await supabase.auth.getUser()

// Sign out
const { error } = await supabase.auth.signOut()

// Update user metadata (Australian context)
const { data, error } = await supabase.auth.updateUser({
    data: {
        locale: 'en-AU',
        state: 'QLD',
        timezone: 'Australia/Brisbane'
    }
})
```

## Queries

```typescript
// Select with relations
const { data, error } = await supabase
    .from('posts')
    .select('id, title, created_at, author:users(name, email)')
    .eq('status', 'active')
    .order('created_at', { ascending: false })
    .limit(10)

// Insert (Australian user data)
const { data, error } = await supabase
    .from('users')
    .insert({
        email: 'user@example.com.au',
        name: 'John Smith',
        phone: '0412 345 678',  // Australian mobile format
        state: 'QLD',
        postcode: '4000',
        created_at: new Date().toISOString()  // Will be formatted DD/MM/YYYY on display
    })
    .select()
    .single()

// Update
const { data, error } = await supabase
    .from('posts')
    .update({ title: 'Updated Title' })
    .eq('id', postId)
    .select()
    .single()

// Delete
const { data, error } = await supabase
    .from('posts')
    .delete()
    .eq('id', postId)
```

## RLS Policies (Row Level Security)

```sql
-- Enable RLS
ALTER TABLE posts ENABLE ROW LEVEL SECURITY;

-- Public read access
CREATE POLICY "read_all" ON posts
FOR SELECT
USING (true);

-- Users can only insert their own posts
CREATE POLICY "insert_own" ON posts
FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can only update their own posts
CREATE POLICY "update_own" ON posts
FOR UPDATE
USING (auth.uid() = user_id);

-- Users can only delete their own posts
CREATE POLICY "delete_own" ON posts
FOR DELETE
USING (auth.uid() = user_id);

-- Privacy Act 1988 compliance: Users can access their own PII
CREATE POLICY "users_read_own_data" ON users
FOR SELECT
USING (auth.uid() = id);

-- Privacy Act 1988 compliance: Users can update their own data
CREATE POLICY "users_update_own_data" ON users
FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);
```

## Realtime Subscriptions

```typescript
// Subscribe to table changes
const channel = supabase
    .channel('posts')
    .on(
        'postgres_changes',
        {
            event: '*',  // INSERT, UPDATE, DELETE
            schema: 'public',
            table: 'posts'
        },
        (payload) => {
            console.log('Change received!', payload)
        }
    )
    .subscribe()

// Unsubscribe
await channel.unsubscribe()

// Australian-specific: Subscribe to state-based updates
const qldChannel = supabase
    .channel('qld-jobs')
    .on(
        'postgres_changes',
        {
            event: 'INSERT',
            schema: 'public',
            table: 'jobs',
            filter: 'state=eq.QLD'
        },
        (payload) => {
            console.log('New QLD job:', payload)
        }
    )
    .subscribe()
```

## Storage

```typescript
// Upload file
const { data, error } = await supabase.storage
    .from('avatars')
    .upload(`${userId}/avatar.png`, file, {
        cacheControl: '3600',
        upsert: true
    })

// Get public URL
const { data } = supabase.storage
    .from('avatars')
    .getPublicUrl(`${userId}/avatar.png`)

// Download file
const { data, error } = await supabase.storage
    .from('avatars')
    .download(`${userId}/avatar.png`)

// Delete file
const { data, error } = await supabase.storage
    .from('avatars')
    .remove([`${userId}/avatar.png`])

// List files (Privacy Act 1988: User can only list their own files)
const { data, error } = await supabase.storage
    .from('documents')
    .list(`${userId}/`, {
        limit: 100,
        offset: 0,
        sortBy: { column: 'created_at', order: 'desc' }
    })
```

## Edge Functions

```typescript
// Call edge function
const { data, error } = await supabase.functions.invoke('generate-invoice', {
    body: {
        userId: user.id,
        items: [
            { description: 'Water damage restoration', amount: 1500.00 },
            { description: 'Mould remediation', amount: 800.00 }
        ],
        abn: '12 345 678 901',  // Australian Business Number
        gst: 0.10  // 10% GST for Australia
    }
})

// Edge function with Australian context
const { data, error } = await supabase.functions.invoke('send-notification', {
    body: {
        userId: user.id,
        message: 'Your job is scheduled for tomorrow',
        locale: 'en-AU',
        timezone: 'Australia/Brisbane',
        format: {
            date: 'DD/MM/YYYY',
            time: '24h'
        }
    }
})
```

## Australian Context Patterns

### Phone Number Validation
```typescript
// Validate Australian phone number
async function validateAustralianPhone(phone: string): Promise<boolean> {
    const cleaned = phone.replace(/\s/g, '')

    // Mobile: 04XX XXX XXX
    const mobileRegex = /^04\d{8}$/

    // Landline: (0X) XXXX XXXX
    const landlineRegex = /^0[2-8]\d{8}$/

    return mobileRegex.test(cleaned) || landlineRegex.test(cleaned)
}

// Query users by Australian phone
const { data, error } = await supabase
    .from('users')
    .select('*')
    .like('phone', '04%')  // Australian mobiles start with 04
```

### ABN/ACN Validation
```typescript
// Query businesses by ABN
const { data, error } = await supabase
    .from('businesses')
    .select('*')
    .eq('abn', '12345678901')

// Validate ABN checksum
function validateABN(abn: string): boolean {
    const cleaned = abn.replace(/\s/g, '')
    if (cleaned.length !== 11 || !/^\d+$/.test(cleaned)) return false

    const weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    const digits = cleaned.split('').map(Number)
    digits[0] -= 1

    const sum = digits.reduce((acc, digit, i) => acc + digit * weights[i], 0)
    return sum % 89 === 0
}
```

### Privacy Act 1988 Compliance

```sql
-- Audit table for data access (Privacy Act compliance)
CREATE TABLE data_access_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    table_name TEXT NOT NULL,
    action TEXT NOT NULL,  -- SELECT, INSERT, UPDATE, DELETE
    accessed_at TIMESTAMPTZ DEFAULT NOW(),
    ip_address TEXT,
    user_agent TEXT
);

-- Function to log data access
CREATE OR REPLACE FUNCTION log_data_access()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO data_access_log (user_id, table_name, action)
    VALUES (auth.uid(), TG_TABLE_NAME, TG_OP);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Trigger for sensitive tables
CREATE TRIGGER log_users_access
AFTER SELECT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION log_data_access();
```

## Error Handling

```typescript
// Handle Supabase errors with Australian-friendly messages
async function handleSupabaseError(error: any): Promise<string> {
    if (!error) return ''

    // Map error codes to en-AU messages
    const errorMessages: Record<string, string> = {
        '23505': 'This record already exists. Please use a different value.',
        '23503': 'This action would break a relationship with other data.',
        '42501': 'You don\'t have permission to do that.',
        '42P01': 'The requested data doesn\'t exist.',
        'PGRST116': 'We couldn\'t find what you\'re looking for.',
    }

    return errorMessages[error.code] || 'Something went wrong. Please try again.'
}

// Usage
const { data, error } = await supabase.from('users').insert(userData)
if (error) {
    const message = await handleSupabaseError(error)
    toast.error(message)
}
```

## Verification

- [ ] Client initialization correct (browser vs server)
- [ ] RLS policies enabled and tested
- [ ] Authentication flow works
- [ ] Queries return expected data
- [ ] Realtime subscriptions working
- [ ] Storage permissions correct
- [ ] Australian phone format validated (04XX XXX XXX)
- [ ] Privacy Act 1988 compliance (RLS, audit logs)
- [ ] Error messages in en-AU

See: `lib/supabase/`, `supabase/migrations/`, `database/migrations.skill.md`

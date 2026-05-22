---
name: rls-policy-validator
description: Expert assistant for validating and creating Row Level Security (RLS) policies in the KR92 Bible Voice Supabase database. Use when creating RLS policies, validating user data protection, checking admin access, or identifying security gaps.
---

# RLS Policy Validator

## Capabilities
- Review and suggest RLS policies for new tables
- Validate that user data is properly protected
- Check admin role requirements
- Identify security gaps in database access
- Generate secure policy templates

## Core Principles

### 1. User Data Protection
All user-specific data MUST be protected by RLS policies that check `auth.uid()`.

### 2. Public Bible Data
Bible text, lexicons, and reference data should be publicly readable.

### 3. Admin Access
Admin operations require role checks via `has_role()` function.

### 4. Security Definer
Privileged operations use `SECURITY DEFINER` functions with role checks.

## Usage Examples

### Example 1: Create RLS Policy for New User Table
**User:** "I created a new table `user_notes` for Bible study notes. Add RLS policies."

**Assistant:**
```sql
-- Enable RLS
ALTER TABLE public.user_notes ENABLE ROW LEVEL SECURITY;

-- Policy: Users can view only their own notes
CREATE POLICY "Users can view own notes"
ON public.user_notes
FOR SELECT
TO authenticated
USING (user_id = auth.uid());

-- Policy: Users can insert their own notes
CREATE POLICY "Users can insert own notes"
ON public.user_notes
FOR INSERT
TO authenticated
WITH CHECK (user_id = auth.uid());

-- Policy: Users can update their own notes
CREATE POLICY "Users can update own notes"
ON public.user_notes
FOR UPDATE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());

-- Policy: Users can delete their own notes
CREATE POLICY "Users can delete own notes"
ON public.user_notes
FOR DELETE
TO authenticated
USING (user_id = auth.uid());

-- Policy: Admins can view all notes
CREATE POLICY "Admins can view all notes"
ON public.user_notes
FOR SELECT
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));
```

### Example 2: Validate Existing Policies
**User:** "Check if my bookmarks table is secure"

**Assistant:** Let me review the RLS policies:

```sql
-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' AND tablename = 'bookmarks';

-- List existing policies
SELECT * FROM pg_policies
WHERE schemaname = 'public' AND tablename = 'bookmarks';
```

**Validation checklist:**
- ✅ RLS enabled?
- ✅ SELECT policy checks `auth.uid()`?
- ✅ INSERT policy enforces `user_id = auth.uid()`?
- ✅ UPDATE/DELETE policies protect user data?
- ✅ Admin override policy if needed?
- ✅ No service role bypass in client code?

### Example 3: Create Admin-Only Table
**User:** "Create RLS for admin_audit_logs table"

**Assistant:**
```sql
-- Enable RLS
ALTER TABLE public.admin_audit_logs ENABLE ROW LEVEL SECURITY;

-- Policy: Only admins can read audit logs
CREATE POLICY "Admins can view audit logs"
ON public.admin_audit_logs
FOR SELECT
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));

-- Policy: System can insert (via SECURITY DEFINER function)
CREATE POLICY "System can insert audit logs"
ON public.admin_audit_logs
FOR INSERT
TO authenticated
WITH CHECK (true); -- Controlled by SECURITY DEFINER function

-- Note: No UPDATE or DELETE policies - audit logs are immutable
```

### Example 4: Public Read, Authenticated Write
**User:** "Set up RLS for topics table - everyone can read, only admins can write"

**Assistant:**
```sql
-- Enable RLS
ALTER TABLE bible_schema.topical_topics ENABLE ROW LEVEL SECURITY;

-- Policy: Public can read topics
CREATE POLICY "Public can read topics"
ON bible_schema.topical_topics
FOR SELECT
TO anon, authenticated
USING (true);

-- Policy: Only admins can insert topics
CREATE POLICY "Admins can insert topics"
ON bible_schema.topical_topics
FOR INSERT
TO authenticated
WITH CHECK (public.has_role(auth.uid(), 'admin'));

-- Policy: Only admins can update topics
CREATE POLICY "Admins can update topics"
ON bible_schema.topical_topics
FOR UPDATE
TO authenticated
USING (public.has_role(auth.uid(), 'admin'))
WITH CHECK (public.has_role(auth.uid(), 'admin'));

-- Policy: Only admins can delete topics
CREATE POLICY "Admins can delete topics"
ON bible_schema.topical_topics
FOR DELETE
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));
```

## Common RLS Patterns

### Pattern 1: User-Owned Data
```sql
CREATE POLICY "user_owned_data"
ON table_name
FOR ALL
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());
```

### Pattern 2: Public Read, User Write
```sql
CREATE POLICY "public_read"
ON table_name
FOR SELECT
USING (true);

CREATE POLICY "user_write"
ON table_name
FOR INSERT, UPDATE, DELETE
TO authenticated
USING (user_id = auth.uid())
WITH CHECK (user_id = auth.uid());
```

### Pattern 3: Admin Full Access
```sql
CREATE POLICY "admin_full_access"
ON table_name
FOR ALL
TO authenticated
USING (public.has_role(auth.uid(), 'admin'));
```

### Pattern 4: Role-Based Access
```sql
CREATE POLICY "moderator_access"
ON table_name
FOR SELECT, UPDATE
TO authenticated
USING (
  public.has_role(auth.uid(), 'admin') OR
  public.has_role(auth.uid(), 'moderator')
);
```

## has_role() Function

The project uses a helper function for role checks:

```sql
CREATE FUNCTION public.has_role(_user_id uuid, _role app_role)
RETURNS boolean
LANGUAGE sql
SECURITY DEFINER
SET search_path TO 'public'
AS $$
  SELECT EXISTS (
    SELECT 1 FROM user_roles
    WHERE user_id = _user_id AND role = _role
  )
$$;
```

## Security Checklist

### For User Data Tables
- [ ] RLS enabled on table
- [ ] SELECT policy checks `auth.uid()`
- [ ] INSERT policy enforces `user_id = auth.uid()`
- [ ] UPDATE policy protects user data
- [ ] DELETE policy protects user data
- [ ] Admin override policy if needed
- [ ] No service role key in client code

### For Public Data Tables
- [ ] RLS enabled
- [ ] Public SELECT policy (`USING (true)`)
- [ ] Admin-only write policies
- [ ] No sensitive data exposed

### For Admin Tables
- [ ] RLS enabled
- [ ] All policies check `has_role(auth.uid(), 'admin')`
- [ ] Audit logging in place
- [ ] No direct client access

## Common Vulnerabilities to Avoid

### ❌ No RLS Enabled
```sql
-- DANGEROUS: No RLS protection
CREATE TABLE user_data (...);
-- Anyone can query via service key or bypass
```

### ❌ Missing auth.uid() Check
```sql
-- DANGEROUS: No user isolation
CREATE POLICY "bad_policy"
ON user_data FOR SELECT
USING (true); -- All users see all data!
```

### ❌ Service Key in Client
```typescript
// DANGEROUS: Never use service key in client
const supabase = createClient(url, SERVICE_ROLE_KEY); // ❌
```

### ❌ No Admin Check
```sql
-- DANGEROUS: Anyone can become admin
INSERT INTO user_roles (user_id, role)
VALUES (auth.uid(), 'admin'); -- Should be SECURITY DEFINER function
```

## Testing RLS Policies

### Test as User
```sql
-- Set role to authenticated user
SET ROLE authenticated;
SET request.jwt.claims.sub TO 'user-uuid-here';

-- Try to access data
SELECT * FROM user_notes; -- Should only see own notes

-- Reset
RESET ROLE;
```

### Test as Anon
```sql
SET ROLE anon;
SELECT * FROM verses; -- Should work for public data
SELECT * FROM user_notes; -- Should return empty/error
RESET ROLE;
```

### Test Admin Access
```sql
-- Verify has_role works
SELECT public.has_role('admin-user-uuid', 'admin'); -- Should return true
SELECT public.has_role('regular-user-uuid', 'admin'); -- Should return false
```

## Security Definer Functions

For privileged operations, use SECURITY DEFINER:

```sql
CREATE FUNCTION delete_user_by_admin(target_user_id uuid)
RETURNS boolean
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path TO 'public'
AS $$
BEGIN
  -- Verify admin role
  IF NOT public.has_role(auth.uid(), 'admin') THEN
    RAISE EXCEPTION 'Only admins can delete users';
  END IF;

  -- Prevent self-deletion
  IF target_user_id = auth.uid() THEN
    RAISE EXCEPTION 'Cannot delete own account';
  END IF;

  -- Perform deletion with elevated privileges
  DELETE FROM auth.users WHERE id = target_user_id;

  RETURN true;
END;
$$;
```

## Related Documentation
- See `Docs/02-DESIGN.md` for security architecture
- See `Docs/03-API.md` for table structures
- See `Docs/07-ADMIN-GUIDE.md` for admin role management

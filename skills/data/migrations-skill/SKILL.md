---
name: migrations
category: database
version: 2.0.0
description: Database migration patterns with Australian compliance (Privacy Act 1988)
author: Unite Group
priority: 3
triggers:
  - migration
  - schema
  - sql
  - database schema
---

# Database Migration Patterns

## Migration Structure

```
supabase/
  migrations/
    00000000000000_init.sql
    00000000000001_auth_schema.sql
    00000000000002_enable_pgvector.sql
    00000000000003_state_tables.sql
    00000000000004_australian_fields.sql
    00000000000005_privacy_compliance.sql
  seed.sql
  config.toml
```

## Creating Migrations

```bash
# Create a new migration
supabase migration new create_users_table

# This creates: supabase/migrations/[timestamp]_create_users_table.sql
```

## Migration Best Practices

### 1. Always Include Rollback
```sql
-- Up
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT UNIQUE NOT NULL,
  phone TEXT,  -- Australian format: 04XX XXX XXX
  state TEXT,  -- QLD, NSW, VIC, SA, WA, TAS, NT, ACT
  postcode TEXT,  -- 4 digits
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Down (in comments or separate file)
-- DROP TABLE users;
```

### 2. Make Migrations Atomic
```sql
BEGIN;

CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_created_at ON posts(created_at DESC);

COMMIT;
```

### 3. Handle Existing Data
```sql
-- Add column with default
ALTER TABLE users
ADD COLUMN status TEXT DEFAULT 'active';

-- Update existing rows
UPDATE users SET status = 'active' WHERE status IS NULL;

-- Now make it NOT NULL
ALTER TABLE users
ALTER COLUMN status SET NOT NULL;
```

## Common Patterns

### Create Table with RLS (Privacy Act 1988 Compliance)
```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
  title TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (Privacy Act 1988)
ALTER TABLE conversations ENABLE ROW LEVEL SECURITY;

-- Users can only access their own data
CREATE POLICY "Users can CRUD own conversations"
ON conversations FOR ALL
USING (auth.uid() = user_id);

-- Audit trigger (Privacy Act 1988 compliance)
CREATE TRIGGER audit_conversations
AFTER INSERT OR UPDATE OR DELETE ON conversations
FOR EACH ROW
EXECUTE FUNCTION log_data_access();
```

### Australian User Fields
```sql
-- Add Australian-specific fields to users table
ALTER TABLE users
ADD COLUMN phone TEXT,  -- Format: 04XX XXX XXX or (0X) XXXX XXXX
ADD COLUMN state TEXT CHECK (state IN ('QLD', 'NSW', 'VIC', 'SA', 'WA', 'TAS', 'NT', 'ACT')),
ADD COLUMN postcode TEXT CHECK (postcode ~ '^\d{4}$'),  -- Australian postcodes are 4 digits
ADD COLUMN timezone TEXT DEFAULT 'Australia/Brisbane';

-- Add indexes for Australian fields
CREATE INDEX idx_users_state ON users(state);
CREATE INDEX idx_users_postcode ON users(postcode);

-- Validate Australian phone format
ALTER TABLE users
ADD CONSTRAINT check_phone_format
CHECK (
  phone IS NULL OR
  phone ~ '^04\d{2}\s?\d{3}\s?\d{3}$' OR  -- Mobile
  phone ~ '^0[2-8]\d{8}$'  -- Landline
);
```

### Business Table with ABN/ACN
```sql
CREATE TABLE businesses (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name TEXT NOT NULL,
  abn TEXT UNIQUE,  -- Australian Business Number (11 digits)
  acn TEXT UNIQUE,  -- Australian Company Number (9 digits)
  address TEXT,
  state TEXT CHECK (state IN ('QLD', 'NSW', 'VIC', 'SA', 'WA', 'TAS', 'NT', 'ACT')),
  postcode TEXT CHECK (postcode ~ '^\d{4}$'),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Validate ABN format (11 digits)
ALTER TABLE businesses
ADD CONSTRAINT check_abn_format
CHECK (abn IS NULL OR abn ~ '^\d{11}$');

-- Validate ACN format (9 digits)
ALTER TABLE businesses
ADD CONSTRAINT check_acn_format
CHECK (acn IS NULL OR acn ~ '^\d{9}$');
```

### Add Foreign Key
```sql
ALTER TABLE posts
ADD COLUMN category_id UUID REFERENCES categories(id);

CREATE INDEX idx_posts_category_id ON posts(category_id);
```

### Create Junction Table
```sql
CREATE TABLE post_tags (
  post_id UUID REFERENCES posts(id) ON DELETE CASCADE,
  tag_id UUID REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (post_id, tag_id),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for junction table
CREATE INDEX idx_post_tags_post_id ON post_tags(post_id);
CREATE INDEX idx_post_tags_tag_id ON post_tags(tag_id);
```

### Enable pgvector (for AI embeddings)
```sql
-- Enable vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Add embedding column
ALTER TABLE documents
ADD COLUMN embedding vector(1536);

-- Create vector index for similarity search
CREATE INDEX idx_documents_embedding
ON documents
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Function to search similar documents
CREATE OR REPLACE FUNCTION search_similar_documents(
  query_embedding vector(1536),
  match_threshold float,
  match_count int
)
RETURNS TABLE (
  id UUID,
  title TEXT,
  content TEXT,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    documents.id,
    documents.title,
    documents.content,
    1 - (documents.embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
  ORDER BY documents.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

### Create Function & Trigger
```sql
-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to multiple tables
CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON conversations
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON users
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
```

### Privacy Act 1988 Compliance: Audit Logging
```sql
-- Create audit log table
CREATE TABLE audit_log (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
  table_name TEXT NOT NULL,
  action TEXT NOT NULL,  -- INSERT, UPDATE, DELETE, SELECT
  record_id UUID,
  old_data JSONB,
  new_data JSONB,
  ip_address TEXT,
  user_agent TEXT,
  timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- Index for querying audit logs
CREATE INDEX idx_audit_log_user_id ON audit_log(user_id);
CREATE INDEX idx_audit_log_table_name ON audit_log(table_name);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp DESC);

-- Function to log data changes
CREATE OR REPLACE FUNCTION log_data_access()
RETURNS TRIGGER AS $$
BEGIN
  INSERT INTO audit_log (
    user_id,
    table_name,
    action,
    record_id,
    old_data,
    new_data
  ) VALUES (
    auth.uid(),
    TG_TABLE_NAME,
    TG_OP,
    COALESCE(NEW.id, OLD.id),
    CASE WHEN TG_OP IN ('UPDATE', 'DELETE') THEN row_to_json(OLD) ELSE NULL END,
    CASE WHEN TG_OP IN ('INSERT', 'UPDATE') THEN row_to_json(NEW) ELSE NULL END
  );

  RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Apply audit trigger to sensitive tables
CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION log_data_access();

CREATE TRIGGER audit_businesses
AFTER INSERT OR UPDATE OR DELETE ON businesses
FOR EACH ROW
EXECUTE FUNCTION log_data_access();
```

### Data Retention (Privacy Act 1988)
```sql
-- Function to delete old audit logs (7 year retention for Privacy Act)
CREATE OR REPLACE FUNCTION cleanup_old_audit_logs()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
  DELETE FROM audit_log
  WHERE timestamp < NOW() - INTERVAL '7 years';
END;
$$;

-- Schedule with pg_cron (if installed)
-- SELECT cron.schedule('cleanup-audit-logs', '0 0 1 * *', 'SELECT cleanup_old_audit_logs()');
```

## Running Migrations

```bash
# Apply all pending migrations
supabase db push

# Reset database and apply all migrations (DESTRUCTIVE!)
supabase db reset

# Generate TypeScript types from schema
supabase gen types typescript --local > types/supabase.ts

# Create migration from diff
supabase db diff --file migration_name
```

## Seeding Data (Australian Context)

```sql
-- supabase/seed.sql

-- Insert Australian states
INSERT INTO states (code, name) VALUES
  ('QLD', 'Queensland'),
  ('NSW', 'New South Wales'),
  ('VIC', 'Victoria'),
  ('SA', 'South Australia'),
  ('WA', 'Western Australia'),
  ('TAS', 'Tasmania'),
  ('NT', 'Northern Territory'),
  ('ACT', 'Australian Capital Territory');

-- Insert service categories
INSERT INTO categories (id, name) VALUES
  ('cat-water-damage', 'Water Damage Restoration'),
  ('cat-mould', 'Mould Remediation'),
  ('cat-fire', 'Fire Damage Restoration'),
  ('cat-emergency', 'Emergency Services');

-- Insert settings
INSERT INTO settings (key, value) VALUES
  ('app_name', 'Unite Group'),
  ('locale', 'en-AU'),
  ('currency', 'AUD'),
  ('date_format', 'DD/MM/YYYY'),
  ('timezone', 'Australia/Brisbane'),
  ('gst_rate', '0.10');

-- Insert test businesses (Australian)
INSERT INTO businesses (name, abn, state, postcode) VALUES
  ('Test Restoration Co', '12345678901', 'QLD', '4000'),
  ('Sydney Water Damage', '98765432101', 'NSW', '2000');
```

## Migration Verification Checklist

- [ ] Migration runs without errors
- [ ] Rollback works correctly (if applicable)
- [ ] RLS policies are correct and tested
- [ ] Indexes created for foreign keys
- [ ] Triggers work as expected
- [ ] Australian field constraints work (phone, postcode, state)
- [ ] ABN/ACN validation correct (if applicable)
- [ ] Privacy Act 1988 compliance (RLS, audit logging)
- [ ] Data retention policies implemented
- [ ] TypeScript types generated and correct

## Example: Complete Migration (Australian Business)

```sql
-- Migration: 00000000000005_create_jobs_table.sql
BEGIN;

-- Create jobs table
CREATE TABLE jobs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  business_id UUID NOT NULL REFERENCES businesses(id) ON DELETE CASCADE,
  customer_name TEXT NOT NULL,
  customer_phone TEXT NOT NULL CHECK (customer_phone ~ '^04\d{2}\s?\d{3}\s?\d{3}$'),
  address TEXT NOT NULL,
  state TEXT NOT NULL CHECK (state IN ('QLD', 'NSW', 'VIC', 'SA', 'WA', 'TAS', 'NT', 'ACT')),
  postcode TEXT NOT NULL CHECK (postcode ~ '^\d{4}$'),
  job_type TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'scheduled', 'in_progress', 'completed', 'cancelled')),
  amount DECIMAL(10, 2),
  gst DECIMAL(10, 2),  -- 10% GST
  total DECIMAL(10, 2),
  scheduled_date DATE,
  completed_date DATE,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_jobs_business_id ON jobs(business_id);
CREATE INDEX idx_jobs_state ON jobs(state);
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_scheduled_date ON jobs(scheduled_date);

-- RLS
ALTER TABLE jobs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Businesses can manage their own jobs"
ON jobs FOR ALL
USING (
  business_id IN (
    SELECT id FROM businesses WHERE auth.uid() = owner_id
  )
);

-- Triggers
CREATE TRIGGER trigger_update_jobs_updated_at
BEFORE UPDATE ON jobs
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER audit_jobs
AFTER INSERT OR UPDATE OR DELETE ON jobs
FOR EACH ROW
EXECUTE FUNCTION log_data_access();

COMMIT;
```

See: `supabase/migrations/`, `database/supabase.skill.md`

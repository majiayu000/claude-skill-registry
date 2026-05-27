---
name: bulk-support-message
description: "Send bulk messages to dancers via Ballee Support chat. Use when sending apology messages, system updates, or personalized notifications to users."
---

# Bulk Support Message Skill

Send bulk messages to dancers via the Ballee Support chat system. Messages are sent as direct messages from Ballee Support, which triggers email notifications to recipients.

## When to Use This Skill

Use this skill when:
- Sending apology messages to affected users
- Communicating system issues or updates to specific dancers
- Sending personalized notifications via chat

## How It Works

1. Messages are sent using the existing support chat system
2. Each message creates a direct conversation between Ballee Support and the dancer
3. The chat system automatically sends email notifications for new messages
4. Messages appear in the dancer's chat inbox on the app

## Prerequisites

- Production database access (SUPABASE_DB_PASSWORD_PROD)
- Admin privileges (super admin role)

## Usage

### Step 1: Identify Recipients

Query the production database to get the list of affected users:

```sql
SELECT DISTINCT
  p.id as profile_id,
  p.first_name,
  p.last_name,
  u.email
FROM profiles p
JOIN auth.users u ON p.id = u.id
WHERE p.id IN ('uuid1', 'uuid2', ...);
```

### Step 2: Create/Find Conversations

For each recipient, find or create a support conversation:

```sql
-- Find existing support conversation
SELECT c.id as conversation_id
FROM conversations c
JOIN conversation_participants cp1 ON c.id = cp1.conversation_id
JOIN conversation_participants cp2 ON c.id = cp2.conversation_id
WHERE cp1.user_id = '<dancer_id>'
  AND cp2.user_id = '00000000-0000-0000-0000-000000000001' -- Ballee Support ID
  AND c.is_direct = true
  AND c.deleted_at IS NULL;

-- Or create a new conversation if none exists
INSERT INTO conversations (is_direct, created_by)
VALUES (true, '00000000-0000-0000-0000-000000000001')
RETURNING id;

INSERT INTO conversation_participants (conversation_id, user_id, is_active)
VALUES
  ('<new_conv_id>', '<dancer_id>', true),
  ('<new_conv_id>', '00000000-0000-0000-0000-000000000001', true);
```

### Step 3: Send Messages

Insert messages as Ballee Support:

```sql
INSERT INTO messages (conversation_id, sender_id, content, content_type)
VALUES (
  '<conversation_id>',
  '00000000-0000-0000-0000-000000000001', -- Ballee Support
  'Your message here',
  'text'
);
```

### Step 4: Trigger Email Notifications

The chat system's database triggers will automatically:
1. Update conversation `last_message_at`
2. Increment `unread_count` for recipient
3. Schedule email notification via automation system

## Example: Sending Apology Message

```sql
-- Bulk insert apology messages for affected dancers
WITH support_user AS (
  SELECT '00000000-0000-0000-0000-000000000001'::uuid AS id
),
affected_dancers AS (
  -- List of affected dancer profile IDs
  SELECT unnest(ARRAY[
    '9a7c53d9-b132-497c-ab93-1b45f2dc07a9',
    'd18108c8-f639-4d17-8c94-f334535c10c1'
    -- ... more IDs
  ]::uuid[]) AS profile_id
),
dancer_conversations AS (
  SELECT
    ad.profile_id,
    c.id as conversation_id
  FROM affected_dancers ad
  JOIN conversation_participants cp1 ON cp1.user_id = ad.profile_id
  JOIN conversation_participants cp2 ON cp2.conversation_id = cp1.conversation_id
  JOIN conversations c ON c.id = cp1.conversation_id
  CROSS JOIN support_user su
  WHERE cp2.user_id = su.id
    AND c.is_direct = true
    AND c.deleted_at IS NULL
)
INSERT INTO messages (conversation_id, sender_id, content, content_type)
SELECT
  dc.conversation_id,
  (SELECT id FROM support_user),
  'Hi! Earlier today, you may have received an email with the subject "Performance tomorrow". Please disregard this email — it was sent by mistake due to a technical issue. Your actual event date has not changed and we will send you a proper reminder closer to that date. We sincerely apologize for any confusion. — The Ballee Team',
  'text'
FROM dancer_conversations dc;
```

## Notes

- The Ballee Support user ID is `00000000-0000-0000-0000-000000000001`
- Messages sent as Ballee Support appear with the official Ballee Support avatar
- Email notifications are queued automatically by the `automation_scheduled_notifications` system
- Dancers can reply directly to these messages in the app

---
name: recovery-social-features
description: Privacy-first social features for recovery apps - sponsors, groups, messaging, friend connections. Use for sponsor/sponsee systems, meeting-based groups, peer support, safe messaging. Activate on "sponsor", "sponsee", "recovery group", "accountability partner", "sober network", "meeting group", "peer support". NOT for general social media patterns (use standard social), dating features, or public profiles.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
category: Lifestyle & Personal
tags:
  - recovery
  - social
  - privacy
  - sponsor
  - groups
  - messaging
  - peer-support
---

# Recovery-Focused Social Features

Build privacy-first social features for addiction recovery apps. These patterns prioritize anonymity, safety, and the unique relationship structures in recovery communities.

## When to Use

✅ **USE this skill for:**
- Sponsor/sponsee relationship systems
- Recovery-focused group features (meeting groups, accountability circles)
- Privacy-first friend connections with mutual consent
- Safe messaging between recovery peers
- Anonymity-preserving profile systems

❌ **DO NOT use for:**
- General social media patterns → use standard social feature docs
- Dating or romantic connection features → not appropriate for recovery context
- Public-facing profiles → recovery apps should default to privacy
- Content recommendation algorithms → use `recovery-community-moderator` for content safety

## Core Principles

### Privacy by Default

Recovery apps handle sensitive data. Default to maximum privacy, let users opt into visibility.

```typescript
interface PrivacySettings {
  profileVisibility: 'private' | 'friends' | 'community';
  showSobrietyDate: boolean;
  showProgram: boolean;        // AA, NA, CMA, etc.
  showLocation: 'none' | 'city' | 'region';
  allowMessages: 'none' | 'friends' | 'sponsors' | 'all';
  anonymousInGroups: boolean;  // Use display name only
}

// Default to most private
const DEFAULT_PRIVACY: PrivacySettings = {
  profileVisibility: 'friends',
  showSobrietyDate: false,
  showProgram: false,
  showLocation: 'none',
  allowMessages: 'friends',
  anonymousInGroups: true,
};
```

### Anonymity Support

Many users need complete anonymity. Support display names separate from real identity.

```typescript
interface Profile {
  id: string;
  // Private - never exposed publicly
  email: string;
  realName?: string;

  // Public-facing identity
  displayName: string;        // "JohnD" or "GratefulMember"
  avatarType: 'initials' | 'icon' | 'custom';
  avatarIcon?: string;        // Predefined icon set

  // Recovery-specific
  sobrietyDate?: Date;
  programs: ('aa' | 'na' | 'cma' | 'smart' | 'refuge' | 'other')[];
  homeGroup?: string;         // Primary meeting
}
```

## Feature Overview

### Sponsor/Sponsee Relationships

The sponsor relationship is hierarchical and private. Only the two parties should know about it.

**Key concepts:**
- Invite-based connection (sponsor generates code, sponsee accepts)
- Time-limited invite codes (24h expiration)
- Private by design - no public visibility
- One sponsor per program, unlimited sponsees

**Hooks provided:**
- `useSponsorInvite()` - Generate and accept invite codes
- `useSponsorRelationships()` - List sponsors and sponsees

**Components:**
- `GenerateSponsorInvite` - Sponsor creates shareable code
- `AcceptSponsorInvite` - Sponsee enters code to connect
- `SponsorDashboard` - View all sponsor/sponsee relationships

> **See:** `references/sponsor-sponsee.md` for full implementation

---

### Meeting-Based Groups

Groups that form organically around meetings. Ephemeral by default but can be made permanent.

**Key concepts:**
- Tied to specific meetings or standalone
- Ephemeral groups auto-delete after 24 hours
- Visibility options: public, private, invite-only
- Member limits prevent overcrowding

**Group Settings:**

```typescript
interface GroupSettings {
  name: string;
  meetingId?: string;           // Link to meeting
  visibility: 'public' | 'private' | 'invite';
  ephemeral: boolean;           // Auto-delete after 24h
  maxMembers: number;           // Member limit
}
```

| Visibility | Who Can See | Who Can Join |
|------------|-------------|--------------|
| `public` | Anyone | Anyone |
| `private` | Members only | Invite only |
| `invite` | Members only | Has invite code |

**Hooks provided:**
- `useMeetingGroup()` - Create, join, leave groups

**Components:**
- `QuickMeetingGroup` - One-tap group creation at meetings

> **See:** `references/groups.md` for full implementation

---

### Friend Connections

Peer-to-peer connections without hierarchy. Mutual consent required.

**Key concepts:**
- Request/accept flow (no auto-follows)
- Real-time updates via Supabase subscriptions
- Blocking supported (one-way, discreet)
- Status: pending, accepted, blocked

**Hooks provided:**
- `useFriendships()` - Full friendship management with real-time sync

**Components:**
- `FriendRequestButton` - Context-aware add/pending/friends states
- `PendingFriendRequests` - Accept/decline UI

> **See:** `references/friendships.md` for full implementation

---

### Safe Messaging

Recovery-appropriate messaging with crisis detection and safety features.

**Key concepts:**
- Real-time message delivery via Supabase
- Crisis keyword detection (non-blocking, shows resources)
- Soft-delete (messages hidden, not destroyed)
- Privacy-first (no read receipts by default)

**Crisis Keywords (trigger resource prompt):**

```typescript
const CRISIS_KEYWORDS = [
  // Suicidal ideation
  'suicide', 'kill myself', 'want to die', 'end it all',
  // Relapse indicators
  'relapse', 'using again', 'fell off the wagon',
  // Self-harm
  'hurt myself', 'cutting', 'self-harm',
];
```

**Best Practices:**
1. **Non-blocking** - Crisis prompts suggest resources, don't block messages
2. **Privacy-first** - Don't log or report crisis keywords automatically
3. **Helpful tone** - Gentle, non-judgmental language
4. **Direct resources** - Link to crisis page, not external sites
5. **Offline capable** - Cache crisis resources for offline access

**Hooks provided:**
- `useMessages()` - Real-time message thread with Supabase subscriptions

**Components:**
- `MessageInput` - Input with crisis detection overlay

> **See:** `references/messaging.md` for full implementation

---

### Accountability Features

Sharing recovery progress with trusted connections.

**Check-In Sharing:**
- Share daily check-ins with selected sponsors
- HALT tracking (Hungry, Angry, Lonely, Tired)
- Mood and gratitude logging

**Sobriety Visibility Settings:**

| Level | Who Can See | Use Case |
|-------|-------------|----------|
| `private` | Only self | Maximum privacy |
| `sponsors` | Self + sponsors | Accountability focus |
| `friends` | Self + sponsors + friends | Peer support |
| `community` | All app users | Public milestone celebrations |

**HALT Check-In Data:**

```typescript
interface DailyCheckIn {
  date: string;
  mood: 1 | 2 | 3 | 4 | 5;  // 1=worst, 5=best
  halt: {
    hungry: boolean;
    angry: boolean;
    lonely: boolean;
    tired: boolean;
  };
  gratitude?: string;
  notes?: string;
}
```

**Components:**
- `ShareCheckIn` - Select sponsors to share with
- `SobrietyVisibility` - Privacy level picker

> **See:** `references/accountability.md` for full implementation

---

### Safety & Moderation

Content moderation and user blocking for safe communities.

**Moderation Categories:**

| Category | Description | Action |
|----------|-------------|--------|
| `crisis` | Suicidal ideation, self-harm | Show resources, don't block |
| `sourcing` | Drug seeking, dealing | Block + flag for review |
| `harassment` | Personal attacks, threats | Block + flag for review |
| `spam` | Promotional content | Block |
| `explicit` | Sexual/graphic content | Block |

**Blocking Behavior:**
- Blocked user cannot send messages
- Blocked user cannot see blocker's profile
- Blocked user cannot see blocker in groups
- Existing messages are hidden (not deleted)
- Blocking is one-way (blocked user doesn't know)

**RLS Policy Pattern:**

```sql
-- Hide content from blocked users
CREATE POLICY "Hide messages from blocked users" ON messages
  FOR SELECT USING (
    NOT EXISTS (
      SELECT 1 FROM friendships
      WHERE status = 'blocked'
      AND (
        (requester_id = auth.uid() AND addressee_id = sender_id)
        OR (addressee_id = auth.uid() AND requester_id = sender_id)
      )
    )
  );
```

**Hooks provided:**
- `useContentModeration()` - Check content against moderation API
- `useBlocking()` - Block/unblock users, check block status

> **See:** `references/moderation.md` for full implementation

---

## Quick Reference

| Feature | Privacy Default | Who Can See |
|---------|-----------------|-------------|
| Profile | Friends only | Configurable |
| Sobriety date | Hidden | Configurable |
| Sponsor relationship | Private | Only the two parties |
| Group membership | Group members | Configurable per group |
| Messages | Participants only | Never public |
| Check-ins | Private | Opt-in sharing |

## Database Schema

See `supabase-admin/references/social-schema.md` for complete Supabase schema including:
- Friendships table with RLS
- Sponsorships with invite codes
- Groups and group members
- Conversations and messages
- Real-time subscription patterns

## References

Detailed implementations in `/references/`:

| File | Contents |
|------|----------|
| `sponsor-sponsee.md` | useSponsorInvite hook, invite UI components, SponsorDashboard |
| `groups.md` | useMeetingGroup hook, QuickMeetingGroup component |
| `friendships.md` | useFriendships hook with real-time, friend request UI |
| `messaging.md` | useMessages hook, MessageInput with crisis detection |
| `accountability.md` | ShareCheckIn, SobrietyVisibility components |
| `moderation.md` | useContentModeration, useBlocking hooks, RLS policies |

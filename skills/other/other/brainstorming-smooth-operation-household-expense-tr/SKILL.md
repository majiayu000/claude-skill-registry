---
name: brainstorming
description: "Use when starting new features, major changes, or unclear requirements. Establishes shared understanding before implementation."
---

# Brainstorming

## Core Principle

Before writing ANY code, discuss the approach with the user. This prevents wasted effort and ensures alignment.

## When to Use This Skill

- Starting a new feature
- Major architectural changes
- Unclear or ambiguous requirements
- Multiple possible approaches exist
- User says "I need..." or "Can we add..."

## The Iron Law

**NEVER skip brainstorming for non-trivial work.**

Even if you think you understand the requirement, the user may have:
- Different expectations
- Hidden constraints
- Better ideas
- Important context you're missing

## Brainstorming Protocol

### Step 1: Acknowledge and Clarify

**Template:**
```
I understand you want to [restate user's request in your own words].

Before I start implementing, let me make sure I understand correctly:
- [Clarifying question 1]
- [Clarifying question 2]
- [Clarifying question 3]
```

**Example:**
```
I understand you want to add user authentication to the API.

Before I start implementing, let me make sure I understand correctly:
- Do you want social login (Google, GitHub) or just email/password?
- Should this be stateless (JWT tokens) or session-based?
- Do you need role-based permissions (admin, user, etc.)?
```

### Step 2: Present Options

Identify 2-4 possible approaches. For each option:
- **Approach**: Brief description
- **Pros**: Why this might be good
- **Cons**: Trade-offs and limitations
- **Complexity**: Low/Medium/High
- **Recommendation**: When to choose this

**Template:**
```
I see a few ways we could approach this:

## Option 1: [Approach Name]
**Description**: [What it involves]
**Pros**:
- [Advantage 1]
- [Advantage 2]
**Cons**:
- [Trade-off 1]
- [Trade-off 2]
**Complexity**: [Low/Medium/High]
**Best for**: [Scenario]

## Option 2: [Approach Name]
[Same structure]

## My Recommendation
Based on [reasoning], I recommend [Option X] because [why].
```

### Step 3: Discuss Trade-offs

Be explicit about:
- **Performance implications**: Will this be fast/slow?
- **Scalability**: Will this work with 10/1000/1M users?
- **Maintenance**: How complex to maintain?
- **Testing**: How easy to test?
- **Security**: Any security concerns?
- **Cost**: Infrastructure costs?

### Step 4: Get Explicit Approval

**Never assume approval.**

**Template:**
```
Does this approach make sense to you?

Any concerns or changes before I start implementing?
```

Wait for user's response before proceeding to planning/implementation.

## Red Flags (When Brainstorming is Being Skipped)

- ❌ "I'll just implement X" → STOP, brainstorm first
- ❌ "This is straightforward" → Still brainstorm
- ❌ "I know what you want" → Verify with user
- ❌ Starting with "Let me create..." → Brainstorm first
- ❌ User said "I need X" and you immediately start coding → Brainstorm first

## Common Rationalizations to Reject

- ❌ "This is a small feature" → Small features still need discussion
- ❌ "The requirement is clear" → User may have unstated expectations
- ❌ "We've done this before" → Each context is different
- ❌ "The user seems confident" → They may not know all options
- ❌ "I'm under time pressure" → Brainstorming SAVES time

## Integration with Other Skills

**After brainstorming**:
1. If user approves approach → Use `writing-plans` skill
2. If database work involved → Use `database-backup` skill
3. For implementation → Use `test-driven-development` skill

## Examples

### Example 1: Authentication Feature

**User Request**: "Add authentication to the API"

**Bad Response** (no brainstorming):
```
Let me add Laravel Sanctum authentication.
[Starts coding immediately]
```

**Good Response** (with brainstorming):
```
I understand you want to add authentication to the API.

Before I start, let me clarify:
- Do you need social login (Google, GitHub) or email/password?
- Stateless tokens (JWT) or session-based?
- Role-based permissions needed?

I see three approaches:

## Option 1: Laravel Sanctum (SPA/Mobile)
**Description**: Token-based, stateless
**Pros**: Simple, good for SPAs/mobile
**Cons**: No built-in OAuth
**Complexity**: Low
**Best for**: Single-page apps, mobile apps

## Option 2: Laravel Passport (OAuth2)
**Description**: Full OAuth2 server
**Pros**: Complete OAuth2, social login support
**Cons**: More complex setup
**Complexity**: Medium
**Best for**: Multiple clients, social login

## Option 3: Clerk (Third-party)
**Description**: Hosted auth service
**Pros**: Very fast setup, social login included
**Cons**: External dependency, cost at scale
**Complexity**: Low
**Best for**: MVP, rapid prototyping

My recommendation: For an API-first MVP with mobile app, I'd suggest Sanctum + Clerk for social login. This gives you simplicity plus social OAuth.

Does this approach make sense?
```

### Example 2: Database Schema Change

**User Request**: "We need to track user activity logs"

**Bad Response**:
```
I'll add an activity_logs table.
[Creates migration immediately]
```

**Good Response**:
```
I understand you want to track user activity logs.

Let me clarify the scope:
- What activities should we log? (logins, API calls, data changes, all?)
- How long should we retain logs? (30 days, 1 year, forever?)
- Do you need to query these logs? (search, filter, reports?)
- Expected volume? (100 events/day or 100,000/day?)

I see a few approaches:

## Option 1: Simple Database Table
**Description**: activity_logs table with user_id, action, timestamp
**Pros**: Simple, easy to query with SQL
**Cons**: Can get large, may slow down main database
**Complexity**: Low
**Best for**: < 1000 events/day

## Option 2: Dedicated Logging Table (Partitioned)
**Description**: Separate database or partitioned table
**Pros**: Doesn't impact main DB performance
**Cons**: More complex setup
**Complexity**: Medium
**Best for**: 1000-100k events/day

## Option 3: External Service (e.g., Papertrail, Logstash)
**Description**: Send logs to external service
**Pros**: Scalable, built-in search/analytics
**Cons**: Cost, external dependency
**Complexity**: Low-Medium
**Best for**: High volume, need analytics

My recommendation: Start with Option 1 (simple table) and add indexes on user_id and timestamp. We can migrate to Option 2 if volume grows.

What level of detail do you need in the logs?
```

## Authority

**This skill is based on**:
- Industry best practice: Design reviews before implementation
- Agile methodology: User collaboration over contract negotiation
- Empirical evidence: 70% of failed projects have unclear requirements
- Cost of change: 10-100x more expensive to fix after implementation

**Social Proof**: Professional development teams ALWAYS discuss design before coding.

## Your Commitment

Before using this skill, confirm:
- [ ] I will ALWAYS brainstorm before coding
- [ ] I will NEVER assume I understand requirements
- [ ] I will PRESENT OPTIONS, not just implement my first idea
- [ ] I will WAIT for user approval before coding

---

**Bottom Line**: 5 minutes of brainstorming saves hours of refactoring. Always discuss before you code.

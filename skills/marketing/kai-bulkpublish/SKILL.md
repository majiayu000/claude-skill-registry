---
name: kai-bulkpublish
description: Prepare an approved social content queue for BulkPublish scheduling or publication. Use when "schedule social posts", "publish the calendar", "send posts to BulkPublish", or "hand off approved social content".
---

# BulkPublish Handoff

Use this skill after `/kai-social`, `/kai-repurpose`, or another content workflow has produced a reviewed calendar. This skill prepares the handoff; it does not bypass approval or silently publish.

## Inputs

- Approved social post calendar with platform, content, media, and links
- BulkPublish channel IDs or names
- Desired schedule and IANA timezone
- Approval status and the person authorized to publish

## Workflow

1. Confirm every post has an explicit approval state and remove anything still in draft or rejected status.
2. Validate each platform’s character, link, media, and format requirements.
3. Resolve channel IDs with BulkPublish `list_channels`; never infer IDs from names alone.
4. Create drafts or approval-gated scheduled posts through the BulkPublish API or MCP server.
5. Before any external publish action, show the final post count, channels, media, and schedule and obtain immediate authorization.
6. Record returned post IDs, status, schedule time, and any per-platform failures in the campaign record.
7. After publication, use BulkPublish analytics to compare outcomes with the campaign objective without promising reach, engagement, or revenue.

## Safety gates

- Treat scheduling and publishing as external side effects.
- Never expose API keys, cookies, or private analytics in content or logs.
- Stop if the audience, account, channel, media, or schedule is ambiguous.
- Do not claim guaranteed engagement, virality, conversions, or revenue.

## References

- BulkPublish API: https://github.com/azeemkafridi/bulkpublish-api
- MCP documentation: https://app.bulkpublish.com/docs
- Social-media skills: https://github.com/azeemkafridi/bulkpublish-api/tree/main/skills/social-media-content-skills

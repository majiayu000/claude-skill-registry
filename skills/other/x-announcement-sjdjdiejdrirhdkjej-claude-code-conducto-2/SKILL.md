---
skill: x-announcement
description: Post release announcements to X (Twitter) with automated GitHub link reply. Auto-trigger after /release command completion or manual invocation. Generates engaging posts from CHANGELOG, posts via API, and replies with GitHub release link in threaded format.
location: managed
---

<objective>
Automate X (Twitter) release announcements with minimal friction by generating engaging posts from release notes, posting via API, and automatically replying with GitHub release links in a threaded format.
</objective>

<quick_start>
<automation_workflow>
**One release, one announcement - fully automated:**

1. **Generate post**: Extract highlights from CHANGELOG for version
2. **User confirmation**: Show preview, allow editing, get approval
3. **Post to X**: Send via API (http://5.161.75.135:8080)
4. **Poll for tweet ID**: Wait until post is live
5. **Reply with link**: Post GitHub release URL as threaded reply
6. **Display URLs**: Show both tweet links for verification

**Example flow:**
```
Generating X announcement for v2.7.0...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
X Announcement Preview
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Spec-Flow v2.7.0 is here!

- One-command releases with CI validation
- Auto-close GitHub issues when features ship
- Essential cleanup for all deployment models

Ship features faster with less manual work.

Characters: 187/280
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Options:
1. Post as-is
2. Edit post text
3. Skip X announcement

Posting to X... (ID: 12345)
Waiting for publish... (3s)
Posted to X!

Posting GitHub link as threaded reply... (ID: 12346)
GitHub link posted!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
X Announcement Posted!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Main Post:
   https://x.com/username/status/1234567890

GitHub Link Reply:
   https://x.com/username/status/1234567891

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
</automation_workflow>

<trigger_conditions>
**Auto-invoke when:**
- `/release` command completes successfully
- Manual invocation for any release
- User mentions "announce release", "post to X", "tweet release"

**Context available:**
- `NEW_VERSION` - Version number (e.g., "2.7.0")
- `CHANGELOG.md` - Release notes for extraction
- `README.md` - Feature highlights
- `COMMIT_SHA` - Git commit hash
</trigger_conditions>

<post_generation_guidelines>
**Format requirements:**
- Include version number prominently
- Highlight 1-3 key features/improvements
- Keep under 280 characters (leave room for editing)
- Use engaging language (not just bullet points)
- End with call-to-action or benefit statement
- **Do NOT use emojis** (UTF-8 encoding issues with X API)

**Content extraction:**
1. Read `CHANGELOG.md` → Extract `## [NEW_VERSION]` section
2. Identify top features: Prioritize Added > Fixed > Changed
3. Format with engaging tone (no emojis)
4. Validate character count (≤280)

See [references/post-templates.md](references/post-templates.md) for examples and guidelines.
</post_generation_guidelines>
</quick_start>

<workflow>
<step_1_generate>
**1. Generate Suggested Post**

Extract release highlights:
```bash
# Read CHANGELOG section for version
SECTION=$(sed -n "/## \[${NEW_VERSION}\]/,/## \[/p" CHANGELOG.md | head -n -1)

# Extract Added features
ADDED=$(echo "$SECTION" | grep -A 10 "### Added" | grep "^-" | head -3)

# Extract Fixed items
FIXED=$(echo "$SECTION" | grep -A 10 "### Fixed" | grep "^-" | head -2)

# Format into engaging post
# Template: 🚀 Spec-Flow v${NEW_VERSION} is here!
# ${FEATURE_EMOJI} ${FEATURE_1}
# ${FEATURE_EMOJI} ${FEATURE_2}
# ${BENEFIT_STATEMENT}
```

Display preview with character count for user review.
</step_1_generate>

<step_2_confirm>
**2. Get User Confirmation**

Use AskUserQuestion or direct prompt:
```
Options:
1. ✅ Post as-is
2. ✏️  Edit post text
3. ❌ Skip X announcement
```

If user selects **Edit**:
- Prompt for new text
- Validate ≤280 characters
- Show updated preview
- Ask for confirmation again

If user selects **Skip**:
- Exit gracefully
- Continue with release summary
</step_2_confirm>

<step_3_post>
**3. Post to X API**

Send POST request with confirmed content:
```bash
# Write content to temp file for proper UTF-8 encoding
cat > /tmp/x-post.txt << 'EOF'
<user-confirmed text>
EOF
POST_CONTENT=$(cat /tmp/x-post.txt | jq -Rs .)

RESPONSE=$(curl -s -X POST "http://5.161.75.135:8080/api/v1/posts/" \
  -H "Content-Type: application/json" \
  -d "{\"content\": $POST_CONTENT, \"scheduled_at\": null}")

POST_ID=$(echo "$RESPONSE" | jq -r '.id')

echo "📤 Posting to X... (ID: $POST_ID)"
```

**Error handling:**
- API unreachable → Warn, provide manual posting instructions
- POST fails → Display error, offer manual fallback
- Continue release process regardless

See [references/api-reference.md](references/api-reference.md) for complete API documentation.
</step_3_post>

<step_4_poll>
**4. Poll for Tweet ID**

Wait for post to be published:
```bash
MAX_ATTEMPTS=20  # 60 seconds total (20 × 3s)
ATTEMPT=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
  STATUS_RESPONSE=$(curl -s "http://5.161.75.135:8080/api/v1/posts/$POST_ID")

  POST_STATUS=$(echo "$STATUS_RESPONSE" | jq -r '.status')
  TWEET_ID=$(echo "$STATUS_RESPONSE" | jq -r '.tweet_id // empty')

  if [ "$POST_STATUS" = "posted" ] && [ -n "$TWEET_ID" ]; then
    echo "✅ Posted to X!"
    break
  elif [ "$POST_STATUS" = "failed" ]; then
    ERROR_REASON=$(echo "$STATUS_RESPONSE" | jq -r '.error_reason')
    echo "❌ Post failed: $ERROR_REASON"
    exit 1
  fi

  ATTEMPT=$((ATTEMPT + 1))
  sleep 3
done
```

Display progress: `⏳ Waiting for publish... (Xs)`
</step_4_poll>

<step_5_reply>
**5. Reply with GitHub Link**

Once main post is live, create threaded reply:
```bash
GITHUB_URL="https://github.com/marcusgoll/Spec-Flow/releases/tag/v${NEW_VERSION}"

# Write reply content to temp file for proper UTF-8 encoding
cat > /tmp/reply.txt << EOF
🔗 Release notes: ${GITHUB_URL}
EOF
REPLY_CONTENT=$(cat /tmp/reply.txt | jq -Rs .)

# Post as threaded reply using in_reply_to_tweet_id
REPLY_RESPONSE=$(curl -s -X POST "http://5.161.75.135:8080/api/v1/posts/" \
  -H "Content-Type: application/json" \
  -d "{\"content\": $REPLY_CONTENT, \"scheduled_at\": null, \"in_reply_to_tweet_id\": \"$TWEET_ID\"}")

REPLY_POST_ID=$(echo "$REPLY_RESPONSE" | jq -r '.id')

# Poll for reply tweet ID (same logic as step 4)
# ...

echo "✅ GitHub link posted!"
```

**Fallback if reply fails:**
- Main post succeeded → Display main tweet URL
- Prompt user to manually reply with GitHub link
- Low impact (main announcement visible)
</step_5_reply>

<step_6_summary>
**6. Display Success Summary**

Show both tweet URLs:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 X Announcement Posted!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Main Post:
   https://x.com/username/status/{TWEET_ID}

GitHub Link Reply:
   https://x.com/username/status/{REPLY_TWEET_ID}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Continue with release summary in `/release` command.
</step_6_summary>
</workflow>

<error_handling>
**Scenario 1: API Unreachable**
```
⚠️  X Poster API is unavailable (http://5.161.75.135:8080/)

Release completed successfully, but X announcement could not be posted.

Manual posting option:
1. Copy the post text above
2. Post manually to X: https://x.com/compose
3. Reply with: 🔗 Release notes: https://github.com/marcusgoll/Spec-Flow/releases/tag/v{VERSION}

Release will continue...
```

**Scenario 2: Post Timeout**
```
⏱️  Timeout waiting for post to publish (60s exceeded)

Post may still succeed in background.
Check status: http://5.161.75.135:8080/api/v1/posts/{POST_ID}

Release will continue...
```

**Scenario 3: Main Post Succeeds, Reply Fails**
```
✅ Main post successful!
⚠️  Reply post failed

Main announcement: https://x.com/username/status/{TWEET_ID}

Manually reply with:
🔗 Release notes: https://github.com/marcusgoll/Spec-Flow/releases/tag/v{VERSION}
```

See [references/error-scenarios.md](references/error-scenarios.md) for complete error handling.
</error_handling>

<api_integration>
**X Poster API Base URL:** `http://5.161.75.135:8080/`

**Key endpoints:**
- `POST /api/v1/posts/` - Create post or threaded reply
- `GET /api/v1/posts/{id}` - Get post status and tweet_id
- `POST /api/v1/posts/{id}/cancel` - Cancel queued post

**Post request format:**
```json
{
  "content": "Tweet text (max 280 chars)",
  "scheduled_at": null,
  "in_reply_to_tweet_id": "1234567890" | null
}
```

**Status values:**
- `queued` - Waiting to post
- `posting` - Currently posting
- `posted` - Live (tweet_id available)
- `failed` - Error (error_reason available)

**Dependencies:**
- `jq` - JSON parsing (required)
- `curl` - HTTP requests (required)
- Network access to API endpoint

See [references/api-reference.md](references/api-reference.md) for complete API documentation.
</api_integration>

<anti_patterns>
**Avoid these mistakes:**

**1. Posting without user confirmation**
```
❌ BAD: Auto-post without showing preview
✅ GOOD: Display preview, get explicit confirmation
```

**2. Exceeding character limit**
```
❌ BAD: Generate 300-char post, API rejects
✅ GOOD: Validate ≤280 chars, trim if needed
```

**3. Not handling API failures gracefully**
```
❌ BAD: Crash release process if X post fails
✅ GOOD: Warn, provide manual fallback, continue release
```

**4. Blocking release on X announcement**
```
❌ BAD: Release fails if tweet can't be posted
✅ GOOD: X announcement is optional enhancement
```

**5. Exposing API URL in public docs**
```
❌ BAD: Include API base URL in error messages, logs
✅ GOOD: Network-isolated, internal-only reference
```
</anti_patterns>

<success_criteria>
**X announcement working when:**

- ✓ Post generated from CHANGELOG highlights
- ✓ Preview shown with character count
- ✓ User confirmation obtained before posting
- ✓ Main post created via API successfully
- ✓ Tweet ID retrieved via polling
- ✓ Threaded reply posted with GitHub link
- ✓ Both tweet URLs displayed
- ✓ Release continues even if X post fails

**Error handling passing when:**
- API unreachable → Manual fallback provided
- Post timeout → Status check URL shown
- Reply fails → Main post URL + manual reply instructions
- Release never blocked by X announcement failures
</success_criteria>

<reference_guides>
For detailed templates, API documentation, and error handling:

- **[references/post-templates.md](references/post-templates.md)** - Engaging post examples and generation guidelines
- **[references/api-reference.md](references/api-reference.md)** - Complete X Poster API documentation
- **[references/error-scenarios.md](references/error-scenarios.md)** - Comprehensive error handling strategies
- **[references/legacy-documentation.md](references/legacy-documentation.md)** - Original detailed implementation guide
</reference_guides>

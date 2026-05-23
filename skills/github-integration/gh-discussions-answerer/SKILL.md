---
name: gh-discussions-answerer
description: Find and answer unanswered GitHub discussions. Activate when user wants to contribute to open source discussions, help answer GitHub questions, or find discussions to answer. Delegates all work to subagents.
allowed-tools: [task]
---

# GitHub Discussions Answerer

All work delegated to `general` subagents.

## Constraints

- **Target: 10 answers** → find 1.5x candidates
- **Post ALL verified** (may be lower or higher, that's fine)
- **100% code-verified** via `gh` CLI
- **Discard only uncertain** → post everything that passes
- **Auto-post** immediately after analysis
- **Read-only until Phase 3** → Phases 1-2 use only GET/query operations; no mutations

## Workflow

### Phase 1: Discovery

Search for unanswered discussions via GitHub API:

```
task(subagent_type="general", description="Search unanswered discussions", prompt="
Run these searches to find unanswered discussions. Calculate dates from today.

SEARCH 1 - Last 30 days, Q&A with no replies:
gh api graphql -f query='{
  search(query: \"is:open comments:0 created:>YYYY-MM-DD category:Q&A NOT author:bot\", type: DISCUSSION, first: 100) {
    nodes { ... on Discussion { title number url bodyText repository { nameWithOwner } category { name } } }
  }
}'

SEARCH 2 - Popular repos (stars>100), any unanswered:
gh api graphql -f query='{
  search(query: \"is:open comments:0 stars:>100 NOT author:bot NOT title:RFC\", type: DISCUSSION, first: 100) {
    nodes { ... on Discussion { title number url bodyText repository { nameWithOwner } category { name } } }
  }
}'

SEARCH 3 - Last 14 days, Help/Support categories:
gh api graphql -f query='{
  search(query: \"is:open comments:0 created:>YYYY-MM-DD NOT author:bot NOT title:proposal\", type: DISCUSSION, first: 100) {
    nodes { ... on Discussion { title number url bodyText repository { nameWithOwner } category { name } } }
  }
}'

Merge results, deduplicate by repo#number.

INCLUDE categories (prioritized):
1. Q&A, Questions, Help, Support, Troubleshooting (highest priority)
2. General (if contains a question mark or asks 'how to')
3. Technical, Development, Usage (if asking for help)

HARD SKIP (not answerable with code research):
- Feature requests ('add X', 'would be nice if', 'please implement')
- Timeline/roadmap questions ('when will X', 'release plan', 'ETA')
- Questions only maintainers can answer (prioritization, future plans)
- Bot-created discussions (mvnpm, dependabot, renovate, github-actions)
- RFCs/proposals/announcements/newsletters
- Release notes or changelogs
- Discussions with only emoji or very short body (<20 chars)
- Already answered discussions (comments > 0)

Return exactly 15 candidates: [repo#number] title - category
")
```

### Phase 2: Parallel Analysis

Launch analyses for ALL candidates in parallel (one subagent per candidate):

```
task(subagent_type="general", description="Analyze discussion", prompt="
Analyze [repo]#[number]: [title]

READ-ONLY: Only use GET/query operations. Do NOT post, create, or mutate anything.

1. Read discussion: gh api repos/OWNER/REPO/discussions/NUMBER
2. Search code: gh search code 'keyword' repo:OWNER/REPO
3. Read files: gh api repos/OWNER/REPO/contents/PATH --jq '.content' | base64 -d
4. Check README/docs for relevant info

VERIFIED answers must provide ACTIONABLE value:
- Code fixes with file:line references
- Configuration solutions with exact syntax
- Workarounds when expected feature is missing
- Technical explanation of WHY something doesn't work
- Links to relevant documentation in the repo

DISCARD if answer would just restate the question:
- 'Feature X doesn't exist' (user knows, that's why they asked)
- 'No timeline available' (useless)
- 'This is a known limitation' (without workaround)

Return VERIFIED: [1-2 sentence answer with actionable fix] OR DISCARD: [reason]
")
```

### Phase 3: Post All Verified

Post ALL verified answers in parallel (one subagent per answer):

```
task(subagent_type="general", description="Post discussion answer", prompt="
Post answer for [repo]#[number]:

1. Get discussion ID:
   gh api graphql -f query='{ repository(owner:\"X\", name:\"Y\") { discussion(number:N) { id } } }'

2. Post the answer:
   gh api graphql -f query='mutation { addDiscussionComment(input: { discussionId: \"ID\", body: \"ANSWER\" }) { comment { url } } }'

3. Unsubscribe from notifications
   THREAD_ID=$(gh api /notifications --jq '.[] | select(.subject.url | contains(\"OWNER/REPO/discussions/NUMBER\")) | .id')
   gh api -X DELETE /notifications/threads/$THREAD_ID/subscription

Return posted URL.
")
```

## Answer Format

- 1-2 sentences max
- File:line if relevant
- No fluff, no AI-speak
- Must give user something they can DO, not just confirm what they know

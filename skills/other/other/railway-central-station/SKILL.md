---
name: central-station
description: This skill should be used when the user asks about Central Station threads, community discussions, support questions, feature requests, or wants to search Railway's community knowledge base. Use for queries like "search central station", "find threads about", "what are people asking about", "recent support threads", or "central station topics".
allowed-tools: Bash(curl:*), Bash(jq:*)
---

# Central Station

Search and browse Railway's Central Station - the community support platform for threads, discussions, and documentation.

## API Endpoints

| Endpoint        | URL                                                    |
| --------------- | ------------------------------------------------------ |
| GraphQL         | `https://station-server.railway.com/gql`               |
| Thread Markdown | `https://station-server.railway.com/api/threads/:slug` |
| LLM Data Export | `https://station-server.railway.com/api/llms-station`  |
| Frontend        | `https://station.railway.com`                          |

## When to Use

- User wants to search Central Station threads or docs
- User asks about community discussions or support questions
- User wants to find threads about a specific topic (deployments, databases, etc.)
- User asks "what are people asking about X"
- User wants to see recent threads or questions
- User mentions Central Station, community threads, or support discussions
- User wants to find existing solutions before creating a new thread

## When NOT to Use

- User wants Railway product documentation - use `railway-docs` skill
- User wants to check their project status - use `status` skill
- User wants to manage their Railway project - use appropriate skill (deploy, environment, etc.)

## Docs Search

For official Railway documentation, use the `railway-docs` skill which fetches from `https://docs.railway.com/api/llms-docs.md`.

Central Station's `unifiedSearch` can identify document types but has limited field access:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  --data-raw '{"query":"{ unifiedSearch(input: { query: \"volumes\", limit: 10 }) { results { document { __typename } } } }"}'
```

Document types returned: `EsThreadItem` (threads) and `DocSearchResult` (docs).

**Note**: For searching thread content, use the LLM Data Export endpoint instead (see below) which provides full thread data.

## Quick Actions

### Get Recent Threads

Fetch recent threads, optionally filtered by topic:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  -d '{"query": "{ threads(first: 10, sort: recent_activity) { edges { node { slug subject status topic { slug displayName } upvoteCount createdAt } } } }"}'
```

With topic filter:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  -d '{"query": "{ threads(first: 10, sort: recent_activity, topic: \"questions\") { edges { node { slug subject status topic { displayName } upvoteCount } } } }"}'
```

### Get Thread by Slug

Fetch a specific thread with its content:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  -d '{"query": "{ thread(slug: \"THREAD_SLUG\") { slug subject status content { data } topic { displayName } upvoteCount } }"}'
```

### Get Thread as Markdown

For a cleaner read, fetch the thread as markdown:

```bash
# Append .md to the frontend URL (requires topic slug)
curl -s 'https://station.railway.com/TOPIC_SLUG/THREAD_SLUG.md'

# Or use API with format query parameter
curl -s 'https://station-server.railway.com/api/threads/THREAD_SLUG?format=md'

# Or use API with Accept header
curl -s 'https://station-server.railway.com/api/threads/THREAD_SLUG' \
  -H 'Accept: text/markdown'
```

### List Topics

Get all available topics:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  -d '{"query": "{ topics { slug displayName displayNamePlural } }"}'
```

Returns: questions, feedback, community, billing, bug-bounty, privacy, abuse, templates

### Get Trending Threads

Fetch currently trending threads:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  -d '{"query": "{ trendingThreads { slug subject status topic { displayName } upvoteCount } }"}'
```

### Get Pinned Threads

Fetch pinned/important threads:

```bash
curl -s 'https://station-server.railway.com/gql' \
  -H 'content-type: application/json' \
  -d '{"query": "{ pinnedThreads { slug subject topic { displayName } } }"}'
```

### Search via LLM Data Export

For searching thread content, fetch all threads and filter locally:

```bash
curl -s 'https://station-server.railway.com/api/llms-station' | jq '.items[] | select(.title | test("postgres"; "i")) | {title, topic: .topic.name, status: .metadata.status}'
```

This endpoint returns all public threads with full content, useful for searching by keywords.

## Thread Statuses

| Status                      | Description                         |
| --------------------------- | ----------------------------------- |
| `OPEN`                      | Unresolved, accepting responses     |
| `SOLVED`                    | Marked as resolved                  |
| `AWAITING_RAILWAY_RESPONSE` | Waiting for Railway team            |
| `AWAITING_USER_RESPONSE`    | Waiting for original poster         |
| `CLOSED`                    | No longer accepting responses       |
| `ARCHIVED`                  | Old thread, preserved for reference |

## Sort Options

For the `threads` query, use the `sort` parameter:

| Sort Value        | Description                    |
| ----------------- | ------------------------------ |
| `recent_activity` | Most recently active (default) |
| `newest`          | Newest first                   |
| `highest_votes`   | Most upvoted                   |

## Presenting Results

When showing threads:

1. **Thread title** - The subject
2. **Topic** - Category (questions, feedback, etc.)
3. **Status** - Open, solved, awaiting response
4. **Summary** - Brief preview from content
5. **Link** - `https://station.railway.com/{topic_slug}/{thread_slug}`

Format example:

```
Found 3 threads about "postgres":

1. "Connection timeout when connecting to Postgres"
   Topic: questions | Status: SOLVED | Upvotes: 5
   https://station.railway.com/questions/connection-timeout-postgres

2. "How to connect to Postgres from local development"
   Topic: community | Status: OPEN | Upvotes: 12
   https://station.railway.com/community/connect-postgres-local

3. "Postgres SSL certificate verification failed"
   Topic: questions | Status: AWAITING_RAILWAY_RESPONSE
   https://station.railway.com/questions/postgres-ssl-verification
```

## Common Search Patterns

| User Query                  | Filter/Search                                      |
| --------------------------- | -------------------------------------------------- |
| "Why is my deploy failing?" | topic: questions, search: "deploy"                 |
| "Can't connect to database" | topic: questions, search: "database" or "postgres" |
| "Domain not working"        | topic: questions, search: "domain"                 |
| "Feature requests"          | topic: feedback                                    |
| "What are people building?" | topic: community                                   |

## Composability

- **After finding a thread**: Summarize the solution or link to it
- **No results found**: Suggest using `railway-docs` skill or creating a new thread
- **Technical issue found**: Use relevant skill (deploy, environment, etc.) to help fix it

## Error Handling

### No Results Found

```
No threads found. Try:
- Different topic filter
- Checking Railway docs instead
- Creating a new thread at https://station.railway.com
```

### Invalid Topic

List available topics first:

```bash
curl -s 'https://station-server.railway.com/gql' -H 'content-type: application/json' -d '{"query": "{ topics { slug } }"}'
```

### Thread Not Found

```
Thread not found. It may have been deleted or marked private.
```

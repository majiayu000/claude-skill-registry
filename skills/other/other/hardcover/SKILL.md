---
name: hardcover
description: Query reading lists and book data from Hardcover.app via GraphQL API. Triggers when user mentions Hardcover, asks about their reading list/library, wants book progress, searches for books/authors/series, or references "currently reading", "want to read", or "books I've read". Also use for syncing reading data to other systems (Obsidian, etc.) or tracking reading goals.
homepage: https://hardcover.app
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "env": ["HARDCOVER_API_TOKEN"] },
      },
  }
---

# Hardcover GraphQL API

Query your reading library, book metadata, and search Hardcover's catalog.

## Configuration

- **Env variable:** `HARDCOVER_API_TOKEN` from https://hardcover.app/settings
- **Endpoint:** `https://api.hardcover.app/v1/graphql`
- **Rate limit:** 60 req/min, 30s timeout, max 3 query depth

## Authentication

All queries require `Authorization: Bearer {token}` header (token from settings, add `Bearer ` prefix):

```bash
curl -X POST https://api.hardcover.app/v1/graphql \
  -H "Authorization: Bearer $HARDCOVER_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "query { me { id username } }"}'
```

## Workflow

1. **Get user ID first** — most queries need it:
   ```graphql
   query { me { id username } }
   ```

2. **Query by status** — use `status_id` filter:
   - `1` = Want to Read
   - `2` = Currently Reading  
   - `3` = Read
   - `4` = Paused
   - `5` = Did Not Finish

3. **Paginate large results** — use `limit`/`offset`, add `distinct_on: book_id`

## Common Queries

### Currently Reading with Progress

```graphql
query {
  me {
    user_books(where: { status_id: { _eq: 2 } }) {
      user_book_reads { progress_pages }
      book {
        title
        pages
        image { url }
        contributions { author { name } }
      }
    }
  }
}
```

### Library by Status

```graphql
query ($userId: Int!, $status: Int!) {
  user_books(
    where: { user_id: { _eq: $userId }, status_id: { _eq: $status } }
    limit: 25
    offset: 0
    distinct_on: book_id
  ) {
    book {
      id
      title
      pages
      image { url }
      contributions { author { name } }
    }
  }
}
```

### Search Books/Authors/Series

```graphql
query ($q: String!, $type: String!) {
  search(query: $q, query_type: $type, per_page: 10, page: 1) {
    results
  }
}
```

`query_type`: `Book`, `Author`, `Series`, `Character`, `List`, `Publisher`, `User`

### Book Details by Title

```graphql
query {
  editions(where: { title: { _eq: "Oathbringer" } }) {
    title
    pages
    isbn_13
    edition_format
    publisher { name }
    book {
      slug
      contributions { author { name } }
    }
  }
}
```

## Limitations

- Read-only (no mutations yet)
- No text search operators (`_like`, `_ilike`, `_regex`)
- Access limited to: your data, public data, followed users' data
- Tokens expire after 1 year

## Entity Reference

For detailed field documentation on Books, Editions, Authors, Series, User Books, Activities, Lists, Goals, and other entities, see [references/entities.md](references/entities.md).

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Invalid/expired token |
| 429 | Rate limited |
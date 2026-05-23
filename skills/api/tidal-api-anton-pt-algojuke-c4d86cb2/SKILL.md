---
name: tidal-api
description: Navigate the Tidal API specification (23,000+ lines OpenAPI spec). Use when implementing Tidal API integrations, adding new endpoints, or understanding API structure.
---

# Tidal API Navigation Skill

Use this skill to navigate the Tidal API specification located at `tidal/tidal-api-oas.json` (23,000+ lines).

## API Overview

The Tidal API is a **JSON:API-compliant** REST API at `https://openapi.tidal.com/v2`.

### Key Characteristics

- **Content-Type**: `application/vnd.api+json`
- **Pagination**: Cursor-based (`page[cursor]` parameter)
- **Batch limits**: Most endpoints support max 20 items per request
- **Filtering**: Use `filter[field]` query params (e.g., `filter[id]`, `filter[isrc]`)
- **Includes**: Use `include` param to embed related resources in response

## Resource Types (Tags)

| Resource              | Description                     | Key Endpoints                   |
| --------------------- | ------------------------------- | ------------------------------- |
| **albums**            | Album metadata, tracks, artists | `/albums`, `/albums/{id}`       |
| **artists**           | Artist info, discography        | `/artists`, `/artists/{id}`     |
| **tracks**            | Track metadata, lyrics, audio   | `/tracks`, `/tracks/{id}`       |
| **playlists**         | User playlists                  | `/playlists`, `/playlists/{id}` |
| **searchResults**     | Search across catalog           | `/searchResults/{query}`        |
| **searchSuggestions** | Autocomplete                    | `/searchSuggestions/{query}`    |
| **userCollections**   | User's saved library            | `/userCollections/{id}`         |
| **users**             | User profiles                   | `/users/me`                     |
| **lyrics**            | Song lyrics                     | `/lyrics`, `/lyrics/{id}`       |
| **artworks**          | Image assets                    | `/artworks`, `/artworks/{id}`   |
| **videos**            | Music videos                    | `/videos`, `/videos/{id}`       |
| **genres**            | Genre metadata                  | `/genres`, `/genres/{id}`       |
| **providers**         | Content providers               | `/providers`, `/providers/{id}` |

## Common Endpoints

### Search

```
GET /searchResults/{query}
  - countryCode: required (e.g., "US")
  - include: albums,artists,playlists,topHits,tracks,videos
  - explicitFilter: INCLUDE|EXCLUDE
```

### Tracks

```
GET /tracks
  - filter[id]: comma-separated track IDs (max 20)
  - filter[isrc]: comma-separated ISRCs (max 20)
  - include: albums,artists,genres,lyrics,providers

GET /tracks/{id}
  - include: albums,artists,genres,lyrics

GET /tracks/{id}/relationships/albums
GET /tracks/{id}/relationships/artists
GET /tracks/{id}/relationships/lyrics
```

### Albums

```
GET /albums
  - filter[id]: comma-separated album IDs (max 20)
  - filter[barcodeId]: barcode/EAN/UPC
  - include: artists,coverArt,genres,items

GET /albums/{id}
  - include: artists,coverArt,genres,items

GET /albums/{id}/relationships/items  # Track listing
  - include: items
```

### Artists

```
GET /artists
  - filter[id]: comma-separated artist IDs

GET /artists/{id}
  - include: albums,biography,profileArt,tracks

GET /artists/{id}/relationships/albums
GET /artists/{id}/relationships/tracks
```

### Playlists (requires user auth)

```
GET /playlists
  - filter[id]: playlist UUIDs
  - filter[owners.id]: user ID
  - include: coverArt,items,ownerProfiles
  - sort: createdAt,-createdAt,lastModifiedAt,-lastModifiedAt,name,-name

POST /playlists  # Create playlist
  - Body: { data: { type: "playlists", attributes: { name, accessType } } }
  - accessType: PUBLIC|UNLISTED|PRIVATE

GET /playlists/{id}/relationships/items
POST /playlists/{id}/relationships/items  # Add tracks
DELETE /playlists/{id}/relationships/items  # Remove tracks
```

### User Library (requires user auth)

```
GET /users/me  # Get authenticated user

GET /userCollections/{userId}/relationships/albums
GET /userCollections/{userId}/relationships/tracks
GET /userCollections/{userId}/relationships/playlists
GET /userCollections/{userId}/relationships/artists
  - include: albums|tracks|playlists|artists (matching resource type)
  - Returns meta.addedAt for each item
```

## Key Schema Types

### Track Attributes

- `title`, `version` (remix info)
- `isrc` (International Standard Recording Code)
- `duration` (ISO 8601, e.g., "PT3M45S")
- `explicit` (boolean)
- `popularity` (0.0-1.0)
- `bpm`, `key`, `keyScale`
- `toneTags` (mood tags like "Happy")
- `mediaTags` (quality: HIRES_LOSSLESS, LOSSLESS)

### Album Attributes

- `title`, `version`
- `barcodeId` (EAN-13/UPC-A)
- `duration` (ISO 8601)
- `numberOfItems`, `numberOfVolumes`
- `releaseDate` (ISO 8601 date)
- `type` (ALBUM|EP|SINGLE)
- `explicit`, `popularity`

### Artist Attributes

- `name`, `handle`
- `popularity` (0.0-1.0)
- `contributionsEnabled`, `contributionsSalesPitch`

### Playlist Attributes

- `name`, `description`
- `accessType` (PUBLIC|UNLISTED|PRIVATE)
- `createdAt`, `lastModifiedAt`
- `numberOfItems`, `duration`

## How to Search the Spec

### Find endpoint details

```bash
# List all paths
jq -r '.paths | keys[]' tidal/tidal-api-oas.json

# Get specific endpoint
jq '.paths["/tracks"]' tidal/tidal-api-oas.json
jq '.paths["/albums/{id}/relationships/items"]' tidal/tidal-api-oas.json

# Search for endpoints containing a term
jq -r '.paths | keys[] | select(contains("playlist"))' tidal/tidal-api-oas.json
```

### Find schema definitions

```bash
# List all schemas
jq -r '.components.schemas | keys[]' tidal/tidal-api-oas.json

# Get specific schema
jq '.components.schemas.Tracks_Attributes' tidal/tidal-api-oas.json
jq '.components.schemas.Albums_Attributes' tidal/tidal-api-oas.json
jq '.components.schemas.Playlists_Attributes' tidal/tidal-api-oas.json

# Search for schemas by pattern
jq -r '.components.schemas | keys[] | select(contains("Playlist"))' tidal/tidal-api-oas.json
```

### Find request/response bodies

```bash
# Get POST request body schema
jq '.paths["/playlists"].post.requestBody' tidal/tidal-api-oas.json

# Find the referenced schema
jq '.components.schemas.PlaylistCreateOperation_Payload' tidal/tidal-api-oas.json

# Get response schema
jq '.paths["/tracks/{id}"].get.responses["200"]' tidal/tidal-api-oas.json
```

### Find security requirements

```bash
# Check auth for an endpoint
jq '.paths["/playlists"].post.security' tidal/tidal-api-oas.json

# List all security schemes
jq '.components.securitySchemes' tidal/tidal-api-oas.json
```

## Authentication

Two methods:

1. **Client Credentials** - App-level access (search, catalog browsing)
   - Scope: None needed for public catalog

2. **Authorization Code PKCE** - User-level access (playlists, library)
   - Scopes: `playlists.read`, `playlists.write`, `collection.read`, `r_usr`, `w_usr`

## Existing Implementation Reference

See `backend/src/services/tidalService.ts` for working implementations of:

- Search with `include=albums,tracks`
- Batch track fetch by ISRC (`filter[isrc]`)
- Batch album fetch by ID (`filter[id]`)
- Album track listing via relationships
- Playlist creation and track addition
- User library sync (albums/tracks)

Key patterns used:

- Rate limiting with exponential backoff
- Chunking requests to 20 items max
- Building lookup maps from `included` resources
- Extracting relationships to resolve IDs

## Tips

1. **Always check `include` options** - Each endpoint lists available includes
2. **Use batch endpoints** - Fetch up to 20 items per request with `filter[id]`
3. **Parse ISO 8601 durations** - Format is `PT{hours}H{minutes}M{seconds}S`
4. **Handle cursor pagination** - Check `links.next` or `links.meta.nextCursor`
5. **Artwork sizes** - Files array contains multiple sizes (80, 160, 320, 640, 1280)

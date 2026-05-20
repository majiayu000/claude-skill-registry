---
name: anime
version: 1.0.1
description: "CLI for AI agents to search and lookup anime info for their humans. Uses Jikan (unofficial MyAnimeList API). No auth required."
homepage: https://jikan.moe
metadata:
  openclaw:
    emoji: "🎌"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["anime", "myanimelist", "jikan", "entertainment", "cli"]
---

# Anime Lookup

CLI for AI agents to search and lookup anime for their humans. "What's that anime about the elf mage?" — now your agent can answer.

Uses Jikan (unofficial MyAnimeList API). No account or API key needed.

## Usage

```
"Search for anime called Frieren"
"What's the top anime right now?"
"What anime is airing this season?"
"Tell me about anime ID 52991"
```

## Commands

| Action | Command |
|--------|---------|
| Search | `anime search "query"` |
| Get details | `anime info <mal_id>` |
| Current season | `anime season` |
| Top ranked | `anime top [limit]` |
| Upcoming | `anime upcoming [limit]` |
| Specific season | `anime season <year> <season>` |

### Examples

```bash
anime search "one punch man"      # Find anime by title
anime info 30276                  # Get full details by MAL ID
anime top 10                      # Top 10 anime
anime season                      # Currently airing
anime season 2024 fall            # Fall 2024 season
anime upcoming 5                  # Next 5 upcoming anime
```

## Output

**Search/list output:**
```
[52991] Sousou no Frieren — 28 eps, Finished Airing, ⭐ 9.28
```

**Info output:**
```
🎬 Sousou no Frieren
   English: Frieren: Beyond Journey's End
   MAL ID: 52991 | Score: 9.28 | Rank: #1
   Episodes: 28 | Status: Finished Airing
   Genres: Adventure, Drama, Fantasy
   Studios: Madhouse

📖 Synopsis:
[Full synopsis text]

🎥 Trailer: [YouTube URL if available]
```

## Notes

- Uses Jikan v4 API (api.jikan.moe)
- Rate limit: 3 req/sec, 60 req/min
- No authentication required
- MAL ID is the MyAnimeList database ID
- Seasons: winter, spring, summer, fall

---

## Agent Implementation Notes

**Script location:** `{skill_folder}/anime` (symlink to `scripts/anime`)

**When user asks about anime:**
1. Run `./anime search "title"` to find MAL ID
2. Run `./anime info <id>` for full details
3. Run `./anime season` or `./anime top` for recommendations

**Don't use for:** Non-anime media (manga, movies unless anime films).

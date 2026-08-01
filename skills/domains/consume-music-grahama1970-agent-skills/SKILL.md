---
name: consume-music
description: Search and annotate ingested music using Horus Music Taxonomy (HMT).
  Works with content already processed by /ingest-yt-history.
---

---
name: consume-music
description: >
  Search and annotate music from ingested YouTube history.
  Uses Horus Music Taxonomy (HMT) for bridge-based memory integration.
  Enables episodic associations linking music to lore events.
triggers:
  - consume music
  - search music
  - music notes
  - find music for
  - music for scene
  - music taxonomy
allowed-tools:
  - Bash
  - Python
metadata:
  short-description: Consume music - search, HMT taxonomy, episodic lore links

provides:
  - consume-music
composes: [, task-monitor]
---

# Consume Music Skill

Search and annotate ingested music using Horus Music Taxonomy (HMT). Works with content already processed by `/ingest-yt-history`.

## Quick Start

```bash
cd .pi/skills/consume-music

# Sync from ingest-yt-history
./run.sh sync

# Search music by title/artist
./run.sh search "Chelsea Wolfe"

# Find music matching a bridge attribute
./run.sh find --bridge Fragility

# Find music for a lore episode
./run.sh episode "Siege of Terra"

# Find music for a scene description
./run.sh scene "The Imperial Fists prepare for the final defense"

# Add a note to a track
./run.sh note --track <track_id> --note "Perfect for Webway collapse scene"

# Sync HMT tags to /memory
./run.sh memory-sync
```

## Commands

### Sync from Ingest

```bash
./run.sh sync [--ingest-root ~/.pi/ingest-yt-history]
```

Imports music entries from `/ingest-yt-history` and extracts HMT taxonomy tags.

### Search Music

```bash
./run.sh search <query> [--artist <name>] [--domain <genre>] [--limit <n>]
```

Search music by title, artist, or domain (genre).

### Find by Bridge

```bash
./run.sh find --bridge <attribute> [--limit <n>]
```

Find music matching a Federated Taxonomy bridge attribute:
- `Precision` - Technical, polyrhythmic (Iron Warriors aesthetic)
- `Resilience` - Triumphant, enduring (Imperial Fists aesthetic)
- `Fragility` - Delicate, breaking (Webway aesthetic)
- `Corruption` - Distorted, industrial (Chaos aesthetic)
- `Loyalty` - Ceremonial, sacred (Oaths of Moment)
- `Stealth` - Ambient, drone (Alpha Legion aesthetic)

### Find for Episode

```bash
./run.sh episode <episode_name> [--limit <n>]
```

Find music matching a lore episode:
- `Siege_of_Terra` - Resilience bridge
- `Davin_Corruption` - Corruption bridge
- `Webway_Collapse` - Fragility bridge
- `Mournival_Oath` - Loyalty bridge
- `Iron_Cage` - Precision bridge
- `Sanguinius_Fall` - Fragility bridge

### Find for Scene

```bash
./run.sh scene "<description>" [--limit <n>]
```

Find music matching a scene description. Uses HMT verifier to score candidates.

### Add Note

```bash
./run.sh note --track <track_id> --note <text> [--agent <agent_id>]
```

Add a Horus note to a music track.

### Sync to Memory

```bash
./run.sh memory-sync [--force]
```

Sync music entries with HMT taxonomy tags to `/memory`:
- category: `music`
- collection_tags: `{domain, thematic_weight, function}`
- bridge_attributes: `[Resilience, Fragility, ...]`
- tactical_tags: `[Score, Recall, ...]`

### Build Profile

```bash
./run.sh profile [--output <file>]
```

Build taste profile with:
- `top_bridge_attributes`: Most frequent bridges
- `top_domains`: Most frequent genres
- `top_artists`: Most played artists
- `episodic_associations`: Which episodes have strong music associations

## Memory + Taxonomy Integration

Follows the canonical `create-context/memory_integration.py` pattern with graceful degradation.

### Pre-hook: `recall_prior_annotations(query, k=5)`
- Recalls prior music annotations before search to surface previously tagged tracks
- Wired into `search.py` to inform search results with memory context
- Enables cumulative taste profile building across sessions

### Post-hook: `learn_annotation(track_title, artist, annotation, hmt_tags, persona_id)`
- Stores track annotation (title, artist, HMT tags, bridge attributes)
- Stores persona taste association when persona_id is provided
- Tags: `["consume_music", persona_id] + bridges + hmt_tags[:3]`
- Wired into `notes.py` (on note add) and `ingest_bridge.py` (on sync)

### Bridge Keywords (keyword fallback, tuned for music)
| Bridge | Keywords |
|--------|----------|
| Precision | rhythm, tempo, technique, polyrhythm, algorithmic, technical |
| Resilience | resolution, harmony, triumphant, enduring, crescendo, epic |
| Fragility | dissonance, distortion, delicate, acoustic, breaking, ethereal |
| Corruption | noise, industrial, harsh, chaos, warp, distorted |
| Loyalty | ceremonial, choral, sacred, devotion, oath |
| Stealth | ambient, drone, minimalist, atmospheric, subtle |
| Transcendence | post-rock, shoegaze, expansive, reverb, layered |
| Defiance | aggressive, rebellion, punk, thrash, rage |

### Graceful Degradation
- Uses `try/except ImportError` at every hook callsite
- Falls back to keyword-based bridge extraction when taxonomy module unavailable
- All hooks are no-ops when `common.memory_client` is not importable

## Data Storage

| Data | Location |
|------|----------|
| Music registry | `~/.pi/consume-music/registry.json` |
| Notes | `~/.pi/consume-music/notes/<agent_id>/notes.jsonl` |
| Profile | `~/.pi/consume-music/profile.json` |
| HMT cache | `~/.pi/consume-music/hmt_cache.json` |

## Integration with /memory

Music entries are stored in `/memory` with full HMT taxonomy:

```bash
./memory/run.sh learn \
  --problem "Music: Chelsea Wolfe - Carrion Flowers" \
  --solution "Dark folk/doom. Bridge: Fragility. Episode: Webway_Collapse, Sanguinius_Fall" \
  --category music \
  --tags chelsea_wolfe,dark_folk,doom,fragility,webway
```

## Querying from /memory

After sync, Horus can recall music via:

```bash
# By bridge attribute
/memory recall --bridge Resilience --collection music

# By episode
/memory recall --episode "Siege of Terra" --collection music

# By mood for scene
/memory recall --scene "battle preparation" --collection music
```

## Horus Music Taxonomy (HMT)

Located at: `/home/graham/workspace/experiments/memory/persona/bridge/horus_music_taxonomy.py`

### Tier 0: Bridge Attributes (cross-collection)
| Bridge | Lore Connection | Music Indicators |
|--------|-----------------|------------------|
| Precision | Iron Warriors, Perturabo | polyrhythm, technical, algorithmic |
| Resilience | Imperial Fists, Dorn | crescendo, triumphant, enduring |
| Fragility | Webway, Magnus's Folly | delicate, acoustic, breaking |
| Corruption | Warp, Chaos, Davin | distorted, industrial, harsh |
| Loyalty | Oaths of Moment, Loken | ceremonial, choral, sacred |
| Stealth | Alpha Legion, Alpharius | ambient, drone, minimalist |

### Tier 1: Tactical Tags
| Tag | Use |
|-----|-----|
| Score | Movie/story soundtrack |
| Recall | Trigger memory/association |
| Amplify | Intensify existing emotion |
| Contrast | Emotional counterpoint |
| Immerse | Create atmosphere |
| Signal | Mark narrative transition |

### Tier 3: Collection Tags
- **Function**: Battle, Mourning, Triumph, Contemplation, Corruption, Resilience
- **Domain**: Orchestral_Epic, Dark_Folk, Doom_Metal, Progressive_Metal, Atmospheric_Ambient
- **Thematic**: Melancholic, Epic, Ominous, Brutal, Ethereal, Tragic

## File Structure

| File | Purpose |
|------|---------|
| `SKILL.md` | This file |
| `run.sh` | Execution entry point |
| `sanity.sh` | Health check |
| `__init__.py` | Package marker |
| `search.py` | Music search with memory pre-hook |
| `list.py` | List music catalog |
| `notes.py` | Add/list notes with memory post-hook |
| `ingest_bridge.py` | Sync from ingest-yt-history with memory post-hook |
| `memory_integration.py` | Memory + Taxonomy hooks (pre/post) |

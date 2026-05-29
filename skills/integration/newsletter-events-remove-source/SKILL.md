---
name: newsletter-events-remove-source
description: Remove Instagram accounts or web aggregators from sources.yaml configuration
---

<essential_principles>
## Configuration Location

All sources are stored in `~/.config/local-media-tools/sources.yaml`.

## Identifier Matching

| Input | Matches |
|-------|---------|
| `@handle` | Instagram account by handle |
| `handle` (no @) | Instagram account by handle |
| `https://site.com` | Web aggregator by URL |
| `"Page Name"` | Any source by name (asks if ambiguous) |

**Note:** Facebook events are not stored in configuration, so there's nothing to remove.

## Safety Features

- Automatic backup before removal
- Validation after removal
- Automatic rollback if validation fails
- Orphan reference cleanup (priority_handles)
</essential_principles>

<intake>
What sources do you want to remove?

**Examples:**
- `@localvenue` - Remove Instagram account
- `@venue1 @venue2` - Remove multiple Instagram accounts
- `https://events.com` - Remove web aggregator
- `"Local Venue"` - Remove by name (any type)

Provide the source(s) to remove:
</intake>

<process>
## Step 1: Parse Identifiers

Analyze the user's input to extract sources to remove:

**Instagram detection:**
- Starts with `@` → Instagram handle
- Word that looks like a handle (alphanumeric + underscores) → Instagram handle

**Web Aggregator detection:**
- Any URL (http:// or https://) → Web aggregator

**Name detection:**
- Quoted string → Search by name across all types

**Extract multiple sources:**
- Split on commas, "and", spaces, newlines
- Deduplicate

## Step 2: Load Current Config

```python
from pathlib import Path
import yaml

config_path = Path.home() / ".config" / "local-media-tools" / "sources.yaml"

if not config_path.exists():
    print("ERROR: sources.yaml not found. Run /newsletter-events:setup first.")
    # STOP HERE

with open(config_path) as f:
    config = yaml.safe_load(f)
```

## Step 3: Match Sources

For each identifier, find matches:

```python
def find_matches(identifier: str, config: dict) -> list:
    """
    Match priority:
    1. Exact Instagram handle (case-insensitive)
    2. Exact Web URL (normalized)
    3. Exact name match (any type)
    """
    matches = []
    normalized = identifier.lower().lstrip("@").strip('"\'')
    sources = config.get("sources", {})

    # Check Instagram handles
    for account in sources.get("instagram", {}).get("accounts", []):
        if account["handle"].lower() == normalized:
            matches.append({"type": "instagram", "item": account, "match": "handle"})

    # Check Web aggregators
    for source in sources.get("web_aggregators", {}).get("sources", []):
        if normalized in source["url"].lower():
            matches.append({"type": "web", "item": source, "match": "url"})

    # Check names (all types) if no URL/handle matches
    if not matches:
        for account in sources.get("instagram", {}).get("accounts", []):
            if account.get("name", "").lower() == normalized:
                matches.append({"type": "instagram", "item": account, "match": "name"})
        for source in sources.get("web_aggregators", {}).get("sources", []):
            if source.get("name", "").lower() == normalized:
                matches.append({"type": "web", "item": source, "match": "name"})

    return matches
```

## Step 4: Handle Ambiguity

If an identifier matches multiple sources, ask the user to clarify:

```
Multiple sources match 'venue':
1. @venue (Instagram) - Local Venue
2. https://venue.com (Web) - Venue Events

Which one(s) to remove? (Enter numbers separated by commas, or 'all'):
```

## Step 5: Confirm if Large Batch

If removing 4+ sources, ask for confirmation:

```
About to remove 5 sources:
- @localvenue (Instagram)
- @oldbar (Instagram)
- @closedgallery (Instagram)
- https://defunctsite.com (Web)
- https://oldsite.com (Web)

This cannot be undone. Continue? (y/n):
```

## Step 6: Backup Original Config

```python
import shutil
from datetime import datetime

backup_path = config_path.with_suffix(f".yaml.{datetime.now():%Y%m%d%H%M%S}.backup")
shutil.copy2(config_path, backup_path)
```

## Step 7: Remove Sources

```python
removed = []
not_found = []

for identifier, matches in matched_sources.items():
    if not matches:
        not_found.append(identifier)
        continue

    for match in matches:
        if match["type"] == "instagram":
            config["sources"]["instagram"]["accounts"] = [
                a for a in config["sources"]["instagram"]["accounts"]
                if a["handle"].lower() != match["item"]["handle"].lower()
            ]
        elif match["type"] == "web":
            config["sources"]["web_aggregators"]["sources"] = [
                s for s in config["sources"]["web_aggregators"]["sources"]
                if s["url"].lower() != match["item"]["url"].lower()
            ]
        removed.append(match)
```

## Step 8: Clean Orphaned References

If removing an Instagram account, also clean up priority_handles:

```python
# Get remaining handles
remaining_handles = {
    a["handle"].lower()
    for a in config["sources"]["instagram"]["accounts"]
}

# Clean priority_handles
if "priority_handles" in config["sources"]["instagram"]:
    original_priority = config["sources"]["instagram"]["priority_handles"]
    config["sources"]["instagram"]["priority_handles"] = [
        h for h in original_priority
        if h.lower() in remaining_handles
    ]
    cleaned_priority = set(original_priority) - set(config["sources"]["instagram"]["priority_handles"])
    if cleaned_priority:
        print(f"Also removed from priority_handles: {', '.join(cleaned_priority)}")
```

## Step 9: Validate Config

```python
from config.config_schema import AppConfig

try:
    AppConfig.from_yaml(config_path)
except Exception as e:
    # Restore backup
    shutil.copy2(backup_path, config_path)
    print(f"ERROR: Invalid config after removal. Restored backup. Error: {e}")
    # STOP HERE
```

## Step 10: Save Updated Config

```python
with open(config_path, "w") as f:
    yaml.dump(config, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
```

## Step 11: Report Results

Display a summary:

```
Removing sources...

✓ Removed @localvenue (Local Venue) from Instagram accounts
✓ Removed @oldbar (Old Bar) from Instagram accounts
  Also removed from priority_handles
✓ Removed https://oldsite.com (Old Site) from web aggregators
✗ Not found: @unknownhandle

Summary: 3 removed, 1 not found

Config backup: sources.yaml.20250120143022.backup
To undo: cp ~/.config/local-media-tools/sources.yaml.20250120143022.backup ~/.config/local-media-tools/sources.yaml

Remaining sources: 4 (run /newsletter-events:list-sources to view)
```

</process>

<success_criteria>
- [ ] All identifiers parsed correctly
- [ ] Matches found using correct priority (handle > URL > name)
- [ ] Ambiguous matches resolved with user
- [ ] Config backed up before modification
- [ ] Sources removed from correct sections
- [ ] Orphaned references cleaned up (priority_handles)
- [ ] Config validates after removal
- [ ] Clear summary shown with removed/not-found counts
- [ ] Undo instructions provided
</success_criteria>

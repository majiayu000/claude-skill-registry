"""Build sync state from existing raw/ files for ckb status tracking."""
import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone
import frontmatter

raw_dir = Path("raw")
state = {"last_sync": datetime.now(timezone.utc).isoformat(), "pages": {}}

for md_file in sorted(raw_dir.rglob("*.md")):
    if md_file.name.startswith("_"):
        continue
    try:
        post = frontmatter.load(str(md_file))
        meta = dict(post.metadata)
        page_id = meta.get("confluence_id", md_file.stem.split("--")[-1])
        content_hash = hashlib.md5(post.content.encode()).hexdigest()[:12]

        state["pages"][str(page_id)] = {
            "title": meta.get("title", md_file.stem),
            "space_key": meta.get("space_key", ""),
            "content_hash": content_hash,
            "version": meta.get("version", 1),
            "filepath": str(md_file),
            "updated_at": meta.get("updated_at", ""),
            "synced_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        print(f"Warning: {md_file}: {e}")

with open(".ckb-sync-state.json", "w") as f:
    json.dump(state, f, indent=2)

print(f"Built sync state with {len(state['pages'])} pages")

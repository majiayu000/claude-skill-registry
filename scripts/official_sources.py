"""Official skill publishers, defined once in policy/official-sources.json."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

OFFICIAL_SOURCES_PATH = Path(__file__).resolve().parent.parent / "policy" / "official-sources.json"


@lru_cache(maxsize=None)
def load_official_owners(path: Path = OFFICIAL_SOURCES_PATH) -> frozenset[str]:
    """Load the GitHub owners whose repositories publish official skills."""
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    owners = payload.get("owners") if isinstance(payload, dict) else None
    if not isinstance(owners, list) or not owners or not all(
        isinstance(owner, str) and owner.strip() and "/" not in owner for owner in owners
    ):
        raise ValueError(f"{path}: owners must be a nonempty list of GitHub owner names")
    return frozenset(owner.strip().casefold() for owner in owners)


def is_official_repo(repo: str) -> bool:
    """Return whether a repo belongs to an owner listed in the official-sources policy."""
    owner, separator, _name = (repo or "").strip().removeprefix("https://github.com/").partition("/")
    return bool(separator) and owner.casefold() in load_official_owners()

"""Side-effect-free detection of skill dependencies on bundled assets."""

from __future__ import annotations

import re

BUNDLED_DIR_ALLOWLIST = {
    "bin",
    "connectors",
    "references",
    "reference",
    "scripts",
    "assets",
    "knowledge",
    "templates",
    "examples",
    "prompts",
    "rules",
    "src",
}

BUNDLED_ROOT_FILE_ALLOWLIST = {
    "audit.md",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "setup.md",
    "uv.lock",
    "README.md",
    "LICENSE",
    "LICENSE.md",
}

BUNDLED_REQUIRED_ROOT_FILE_HINTS = BUNDLED_ROOT_FILE_ALLOWLIST - {
    "README.md",
    "LICENSE",
    "LICENSE.md",
}
_URL_RE = re.compile(r"https?://\S+")


def requires_complete_bundled_archive(skill_content: str) -> bool:
    """Return True when SKILL.md explicitly depends on bundled support files."""
    without_urls = _URL_RE.sub("", skill_content or "")
    normalized = without_urls.lower().replace("\\", "/")
    for dirname in BUNDLED_DIR_ALLOWLIST:
        if re.search(rf"(?<![a-z0-9_.-]){re.escape(dirname)}/", normalized):
            return True
    if re.search(r"(?<![a-z0-9_.-])design-[a-z0-9-]+/", normalized):
        return True
    if re.search(
        r"(?<![a-z0-9_/.-])[a-z0-9][a-z0-9_.-]*\.(?:py|swift)(?![a-z0-9_.-])",
        normalized,
    ):
        return True
    return any(filename.lower() in normalized for filename in BUNDLED_REQUIRED_ROOT_FILE_HINTS)

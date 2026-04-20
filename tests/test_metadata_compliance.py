import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_metadata_compliance  # noqa: E402


def test_validate_metadata_preserves_copyright_for_notices(tmp_path):
    schema = json.loads((ROOT / "schema" / "metadata.schema.json").read_text(encoding="utf-8"))
    metadata_path = tmp_path / "metadata.json"
    metadata_path.write_text(
        json.dumps(
            {
                "name": "aksel-spacing",
                "repo": "navikt/copilot",
                "category": "design",
                "dir_name": "aksel-spacing",
                "author": "Nav",
                "source_url": "https://github.com/navikt/copilot/blob/main/.github/skills/aksel-spacing/SKILL.md",
                "license": "MIT",
                "copyright": "Copyright (c) 2025 Nav",
                "permission_note": "MIT terms require preserving copyright and permission notices.",
                "distribution": "compatible",
            }
        ),
        encoding="utf-8",
    )

    errors, warnings, row = check_metadata_compliance.validate_single_metadata(
        metadata_path, schema
    )

    assert errors == []
    assert warnings == []
    assert row["copyright"] == "Copyright (c) 2025 Nav"
    assert row["local_path"] == "skills/design/aksel-spacing"


def test_write_notices_includes_attribution_and_mit_text(tmp_path):
    notices_path = tmp_path / "THIRD_PARTY_NOTICES.md"

    check_metadata_compliance.write_notices(
        notices_path,
        [
            {
                "name": "aksel-spacing",
                "local_path": "skills/design/aksel-spacing",
                "repo": "navikt/copilot",
                "author": "Nav",
                "license": "MIT",
                "copyright": "Copyright (c) 2025 Nav",
                "distribution": "compatible",
                "source_url": "https://github.com/navikt/copilot/blob/main/.github/skills/aksel-spacing/SKILL.md",
                "permission_note": "MIT terms require preserving copyright and permission notices.",
            }
        ],
        scanned_count=1,
    )

    notices = notices_path.read_text(encoding="utf-8")

    assert "Copyright (c) 2025 Nav" in notices
    assert "skills/design/aksel-spacing" in notices
    assert "MIT terms require preserving copyright and permission notices." in notices
    assert "The above copyright notice and this permission notice shall be included" in notices

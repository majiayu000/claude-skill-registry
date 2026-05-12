#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Sync main repo from core + data (merge artifact).

Usage:
  scripts/sync_main_repo.sh --core <core_dir> --data <data_dir> --main <main_dir> [--no-rebuild]

Example:
  scripts/sync_main_repo.sh \
    --core ../claude-skill-registry-core \
    --data ../claude-skill-registry-data \
    --main ../claude-skill-registry
EOF
}

core_dir=""
data_dir=""
main_dir=""
rebuild=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --core) core_dir="$2"; shift 2;;
    --data) data_dir="$2"; shift 2;;
    --main) main_dir="$2"; shift 2;;
    --no-rebuild) rebuild=0; shift;;
    -h|--help) usage; exit 0;;
    *) echo "Unknown arg: $1"; usage; exit 2;;
  esac
done

if [[ -z "$core_dir" || -z "$data_dir" || -z "$main_dir" ]]; then
  usage
  exit 2
fi

core_dir="$(cd "$core_dir" && pwd)"
data_dir="$(cd "$data_dir" && pwd)"
main_dir="$(cd "$main_dir" && pwd)"

echo "Sync core -> main (excluding skills)..."
# Keep all main-owned workflows stable. Mirroring a new workflow file from core
# requires token workflow scope in the publish repo and breaks scheduled publish.
rsync -a --delete \
  --exclude '.git' \
  --exclude '.gitignore' \
  --exclude 'skills' \
  --exclude 'skills/**' \
  --exclude '.github/workflows/*.yml' \
  --exclude '.github/workflows/*.yaml' \
  "$core_dir/" "$main_dir/"

echo "Sync data -> main/skills..."
mkdir -p "$main_dir/skills"
rsync -a --delete --exclude '.git' "$data_dir/" "$main_dir/skills/"

if [[ "$rebuild" -eq 1 ]]; then
  echo "Rebuilding main registry + index..."
  python "$main_dir/scripts/rebuild_registry.py" --skills-dir "$main_dir/skills" --registry "$main_dir/registry.json" --categories-dir "$main_dir/docs/categories"
  python "$main_dir/scripts/build_registry_summary.py" --registry "$main_dir/registry.json" --plugins "$main_dir/sources/plugins.json" --output "$main_dir/registry_summary.json"
  python "$main_dir/scripts/build_search_index.py" --skills-dir "$main_dir/skills" --output "$main_dir/docs"
fi

echo "Generating third-party notices..."
python "$main_dir/scripts/check_metadata_compliance.py" \
  --skills-dir "$main_dir/skills" \
  --metadata-schema "$main_dir/schema/metadata.schema.json" \
  --notices "$main_dir/THIRD_PARTY_NOTICES.md" \
  --report-only

echo "Done."

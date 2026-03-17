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
# Keep main-owned workflows so publish wiring stays stable.
rsync -a --delete \
  --exclude '.git' \
  --exclude '.gitignore' \
  --exclude 'skills' \
  --exclude 'skills/**' \
  --exclude '.github/workflows/sync-data.yml' \
  --exclude '.github/workflows/build-index.yml' \
  --exclude '.github/workflows/publish-from-core.yml' \
  --exclude '.github/workflows/metadata-compliance.yml' \
  "$core_dir/" "$main_dir/"

echo "Sync data -> main/skills..."
mkdir -p "$main_dir/skills"
rsync -a --delete --exclude '.git' "$data_dir/" "$main_dir/skills/"

if [[ "$rebuild" -eq 1 ]]; then
  echo "Rebuilding main registry + index..."
  python "$main_dir/scripts/rebuild_registry.py" --skills-dir "$main_dir/skills" --registry "$main_dir/registry.json" --categories-dir "$main_dir/docs/categories"
  python "$main_dir/scripts/build_search_index.py" --skills-dir "$main_dir/skills" --output "$main_dir/docs"
fi

echo "Done."

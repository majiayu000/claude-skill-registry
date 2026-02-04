#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Create a separate git repo that contains only the skills archive.

Usage:
  scripts/migrate_to_data_repo.sh <dest_dir>

Example:
  scripts/migrate_to_data_repo.sh ../claude-skill-registry-data
  (cd ../claude-skill-registry-data && git remote add origin git@github.com:YOU/claude-skill-registry-data.git && git push -u origin main)
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || "${#}" -ne 1 ]]; then
  usage
  exit $([[ "${#}" -eq 1 ]] && echo 0 || echo 2)
fi

dest_dir="$1"

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
skills_dir="${root_dir}/skills"

if [[ ! -d "$skills_dir" ]]; then
  echo "Error: skills/ directory not found at: $skills_dir" >&2
  echo "Run this from a clone that still has the archive on disk." >&2
  exit 2
fi

if [[ -e "$dest_dir" ]]; then
  echo "Error: destination already exists: $dest_dir" >&2
  exit 2
fi

mkdir -p "$dest_dir"

echo "Copying skills/* -> $dest_dir/* (this may take a while)..."
# Data repo root should contain category folders (data/, development/, ...),
# so the core repo can check it out into ./skills and keep paths stable:
# ./skills/data/<skill>/SKILL.md
(cd "$skills_dir" && tar -cf - .) | (cd "$dest_dir" && tar -xf -)

cat > "$dest_dir/README.md" <<'EOF'
# Claude Skill Registry (Data)

This repo contains the archived skill contents (category folders like `data/`, `development/`, etc.).

- Browse skills under category folders (e.g. `data/<skill>/SKILL.md`)
- The index + website live in the separate core repo.
EOF

cat > "$dest_dir/.gitignore" <<'EOF'
.DS_Store
__pycache__/
*.py[cod]
EOF

(cd "$dest_dir" && git init -q && git checkout -b main -q)
(cd "$dest_dir" && git add -A && git -c commit.gpgsign=false commit -m "chore: initial skills archive import" -q)

echo ""
echo "Done: $dest_dir"
echo "Next:"
echo "- Add remote + push to GitHub"
echo "- Set core repo vars: REGISTRY_DATA_REPO and secret: DATA_REPO_TOKEN"

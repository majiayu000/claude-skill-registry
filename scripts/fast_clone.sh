#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  scripts/fast_clone.sh [repo_url] [dir] [path...]

Defaults:
  repo_url: https://github.com/majiayu000/claude-skill-registry.git
  dir:      claude-skill-registry
  path...:  docs scripts sources schema

Example:
  scripts/fast_clone.sh https://github.com/majiayu000/claude-skill-registry.git csr docs scripts
  cd csr
  git sparse-checkout add skills/development
EOF
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

repo_url="${1:-https://github.com/majiayu000/claude-skill-registry.git}"
dir="${2:-claude-skill-registry}"
shift $(( $# >= 2 ? 2 : $# ))

paths=("$@")
if [[ "${#paths[@]}" -eq 0 ]]; then
  paths=(docs scripts sources schema)
fi

if [[ -e "$dir" ]]; then
  echo "Error: destination already exists: $dir" >&2
  exit 2
fi

git clone --filter=blob:none --sparse "$repo_url" "$dir"
cd "$dir"
git sparse-checkout set --cone "${paths[@]}"

cat <<EOF

Done.

- Add more folders later with: git sparse-checkout add skills/development
- Get full checkout with:      git sparse-checkout disable
EOF

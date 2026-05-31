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
security_report_path=""

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

timestamp() {
  date -u +"%Y-%m-%dT%H:%M:%SZ"
}

log() {
  printf '[%s] %s\n' "$(timestamp)" "$*"
}

start_group() {
  local label="$1"
  if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
    printf '::group::%s\n' "$label"
  fi
  log "START: $label"
}

end_group() {
  local label="$1"
  local status="$2"
  local elapsed="$3"
  log "END: $label status=$status elapsed=${elapsed}s"
  if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
    printf '::endgroup::\n'
  fi
}

run_step() {
  local label="$1"
  shift
  local started="$SECONDS"
  local status
  start_group "$label"
  set +e
  "$@"
  status="$?"
  set -e
  end_group "$label" "$status" "$((SECONDS - started))"
  return "$status"
}

cleanup() {
  if [[ -n "$security_report_path" && -f "$security_report_path" ]]; then
    rm -f "$security_report_path"
  fi
}
trap cleanup EXIT

remove_local_artifacts_under() {
  local root="$1"
  [[ -d "$root" ]] || return 0
  rm -rf \
    "$root/.ruff_cache" \
    "$root/.pytest_cache" \
    "$root/.mypy_cache" \
    "$root/.venv" \
    "$root/node_modules" \
    "$root/metadata-compliance-report.json" \
    "$root/THIRD_PARTY_NOTICES.generated.md"
  find "$root" \
    \( -path "$root/.git" -o -path "$root/skills" \) -prune \
    -o -name '__pycache__' -type d -prune -exec rm -rf {} +
  find "$root" \
    \( -path "$root/.git" -o -path "$root/skills" \) -prune \
    -o \( -name '*.pyc' -o -name '.DS_Store' \) -type f -exec rm -f {} +
}

sync_core_to_main() {
  # Keep main-owned workflows and repository routing docs/templates stable.
  # Mirroring a new workflow file from core requires token workflow scope in the
  # publish repo and breaks scheduled publish.
  rsync -a --delete \
    --exclude '.git' \
    --exclude '.gitignore' \
    --exclude 'README.md' \
    --exclude 'skills' \
    --exclude 'skills/**' \
    --exclude '.github/ISSUE_TEMPLATE' \
    --exclude '.github/ISSUE_TEMPLATE/**' \
    --exclude '.github/PULL_REQUEST_TEMPLATE.md' \
    --exclude '.github/workflows/*.yml' \
    --exclude '.github/workflows/*.yaml' \
    --exclude '.ruff_cache' \
    --exclude '.pytest_cache' \
    --exclude '.mypy_cache' \
    --exclude '.venv' \
    --exclude 'node_modules' \
    --exclude '__pycache__' \
    --exclude '*/__pycache__' \
    --exclude '*.pyc' \
    --exclude '.DS_Store' \
    --exclude 'metadata-compliance-report.json' \
    --exclude 'THIRD_PARTY_NOTICES.generated.md' \
    "$core_dir/" "$main_dir/"
  remove_local_artifacts_under "$main_dir"
}

sync_data_to_main() {
  mkdir -p "$main_dir/skills"
  rsync -a --delete \
    --exclude '.git' \
    --exclude '.ruff_cache' \
    --exclude '.pytest_cache' \
    --exclude '__pycache__' \
    --exclude '*/__pycache__' \
    --exclude '*.pyc' \
    "$data_dir/" "$main_dir/skills/"
  remove_local_artifacts_under "$main_dir/skills"
}

run_step "Sync core -> main (excluding skills and local caches)" sync_core_to_main
run_step "Sync data -> main/skills" sync_data_to_main

if [[ "$rebuild" -eq 1 ]]; then
  run_step "Rebuild registry shards and category indexes" python "$main_dir/scripts/rebuild_registry.py" \
    --skills-dir "$main_dir/skills" \
    --registry "$main_dir/registry.json" \
    --categories-dir "$main_dir/docs/categories" \
    --compat-manifest-pointer

  run_step "Build registry summary" python "$main_dir/scripts/build_registry_summary.py" \
    --registry "$main_dir/registry.json" \
    --plugins "$main_dir/sources/plugins.json" \
    --output "$main_dir/registry_summary.json"

  security_report_path="$(mktemp)"
  mkdir -p "$main_dir/docs"
  run_step "Generate required security evidence" python "$main_dir/scripts/security_scanner.py" \
    "$main_dir/skills" \
    --quiet \
    --progress-interval 10000 \
    --report-only \
    --output "$security_report_path"

  run_step "Build search and signal indexes" python "$main_dir/scripts/build_search_index.py" \
    --skills-dir "$main_dir/skills" \
    --output "$main_dir/docs" \
    --security-report "$security_report_path"
  rm -f "$security_report_path"
  security_report_path=""

  run_step "Check published categories are canonical" python "$main_dir/scripts/check_canonical_categories.py" \
    --skills-dir "$main_dir/skills" \
    --registry-shards "$main_dir/registry-shards" \
    --docs-dir "$main_dir/docs"

  run_step "Check generated artifact sizes" python "$main_dir/scripts/check_generated_file_sizes.py" \
    --root "$main_dir" \
    --include registry.json \
    --include registry-shards \
    --include docs

  run_step "Check category artifacts" python "$main_dir/scripts/check_category_artifacts.py" \
    --categories-dir "$main_dir/docs/categories"
fi

run_step "Generate third-party notices (advisory full-archive metadata scan)" python "$main_dir/scripts/check_metadata_compliance.py" \
  --skills-dir "$main_dir/skills" \
  --metadata-schema "$main_dir/schema/metadata.schema.json" \
  --notices "$main_dir/THIRD_PARTY_NOTICES.md" \
  --report-only

log "Done."

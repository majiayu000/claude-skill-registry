#!/usr/bin/env bash
# Required check: the published skill stays installable, markdown links respond,
# every executable the install copies onto a user's machine is declared and
# disclosed, and the README installer pin is named. No repository secrets. No network
# except npm registry and the extracted public URLs.
set -euo pipefail
cd "$(dirname "$0")/.."

export NO_COLOR=1
export NPM_CONFIG_UPDATE_NOTIFIER=false

PIN_RE='skills@[0-9]+\.[0-9]+\.[0-9]+'

readme_pin() {
  local pins
  pins=$(grep -oE "$PIN_RE" README.md | sort -u)
  if [[ -z "$pins" ]]; then
    echo "README.md has no skills@X.Y.Z pin" >&2
    exit 1
  fi
  if [[ "$(printf '%s\n' "$pins" | wc -l)" -ne 1 ]]; then
    echo "README.md has multiple skills pins:" >&2
    printf '%s\n' "$pins" >&2
    exit 1
  fi
  printf '%s\n' "${pins#skills@}"
}

run_skills_list() {
  local pin=$1
  local source=$2
  npm exec --yes --package="skills@${pin}" -- skills add "$source" -l
}

installability() {
  local pin
  pin=$(readme_pin)
  echo "Installability: skills@${pin} against $(pwd)"

  local output
  output=$(run_skills_list "$pin" . 2>&1) || {
    printf '%s\n' "$output" >&2
    echo "skills add . -l failed" >&2
    exit 1
  }
  printf '%s\n' "$output"
  if ! grep -q 'Found 1 skill' <<<"$output"; then
    echo "expected exactly one discovered skill" >&2
    exit 1
  fi
  if grep -q 'No skills found' <<<"$output"; then
    echo "installer reported no skills" >&2
    exit 1
  fi

  echo "Installability: broken frontmatter must fail"
  local broken broken_output status
  broken=$(mktemp -d)
  cp SKILL.md "$broken/SKILL.md"
  python3 - "$broken/SKILL.md" <<'PY'
import sys
from pathlib import Path

path = Path(sys.argv[1])
lines = [line for line in path.read_text(encoding="utf-8").splitlines() if not line.startswith("name:")]
path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY
  set +e
  broken_output=$(run_skills_list "$pin" "$broken" 2>&1)
  status=$?
  set -e
  rm -rf "$broken"
  printf '%s\n' "$broken_output"
  if [[ $status -eq 0 ]]; then
    echo "expected skills add to reject SKILL.md with name: removed" >&2
    exit 1
  fi
  if ! grep -q 'missing required frontmatter field(s): name' <<<"$broken_output"; then
    echo "broken frontmatter failed for an unexpected reason" >&2
    exit 1
  fi
}

links() {
  python3 - <<'PY'
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(".")
FILES = [
    ROOT / "README.md",
    ROOT / "SKILL.md",
    ROOT / "SECURITY.md",
    *sorted((ROOT / "references").glob("*.md")),
]
ALLOWLIST = ROOT / "scripts/link-allowlist.txt"
USER_AGENT = "galleonlabs-sell-unused-tokens-link-check/1.0"
URL_RE = re.compile(r"https?://[^\s<>\"'`]+")
TRAILING = ".,;:)]}'\""


def load_allowlist() -> set[str]:
    if not ALLOWLIST.is_file():
        return set()
    urls: set[str] = set()
    for raw in ALLOWLIST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            urls.add(line)
    return urls


def extract() -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    for path in FILES:
        if not path.is_file():
            print(f"{path}: missing", file=sys.stderr)
            sys.exit(1)
        for match in URL_RE.finditer(path.read_text(encoding="utf-8")):
            url = match.group(0).rstrip(TRAILING)
            if url:
                found.setdefault(url, []).append(path.as_posix())
    return found


def status(url: str) -> int:
    request = urllib.request.Request(
        url,
        method="GET",
        headers={"User-Agent": USER_AGENT},
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            return int(response.status)
    except urllib.error.HTTPError as exc:
        return int(exc.code)


allow = load_allowlist()
urls = extract()
if not urls:
    print("no http(s) URLs found in tracked markdown", file=sys.stderr)
    sys.exit(1)

failed = 0
for url in sorted(urls):
    sources = ", ".join(sorted(set(urls[url])))
    if url in allow:
        print(f"ALLOW {url}  ({sources})")
        continue
    try:
        code = status(url)
    except Exception as exc:
        print(f"FAIL  {url}  ({sources})  {exc}", file=sys.stderr)
        failed += 1
        continue
    if 200 <= code < 400:
        print(f"{code}   {url}  ({sources})")
    else:
        print(f"FAIL  {url}  ({sources})  HTTP {code}", file=sys.stderr)
        failed += 1

print(f"checked {len(urls)} unique URL(s); {failed} failed")
sys.exit(1 if failed else 0)
PY
}

payload() {
  python3 - <<'PY'
import subprocess
import sys
from pathlib import Path

ALLOWLIST = Path("scripts/payload-executables.txt")
DISCLOSURE = Path("SECURITY.md")


def declared() -> set[str]:
    if not ALLOWLIST.is_file():
        print(f"{ALLOWLIST}: missing", file=sys.stderr)
        sys.exit(1)
    paths: set[str] = set()
    for raw in ALLOWLIST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            paths.add(line)
    return paths


def shipped() -> set[str]:
    """Files an install copies onto a user's machine that carry executable code.
    The installer copies the repository folder minus .git, so the tracked set is
    the payload."""
    listing = subprocess.run(
        ["git", "ls-files", "-s"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()

    found: set[str] = set()
    for row in listing:
        meta, path = row.split("\t", 1)
        mode = meta.split()[0]
        if mode == "120000":
            continue
        if mode == "100755":
            found.add(path)
            continue
        try:
            with open(path, "rb") as handle:
                if handle.read(2) == b"#!":
                    found.add(path)
        except OSError:
            continue
    return found


allowed = declared()
actual = shipped()
failed = False

for path in sorted(actual - allowed):
    print(f"FAIL  {path} ships executable code but {ALLOWLIST} does not declare it", file=sys.stderr)
    failed = True

for path in sorted(allowed - actual):
    print(f"FAIL  {ALLOWLIST} declares {path}, which no longer ships", file=sys.stderr)
    failed = True

if not DISCLOSURE.is_file():
    print(f"{DISCLOSURE}: missing", file=sys.stderr)
    sys.exit(1)

disclosure = DISCLOSURE.read_text(encoding="utf-8")
for path in sorted(allowed & actual):
    if path in disclosure:
        print(f"OK    {path}  (declared, disclosed in {DISCLOSURE})")
    else:
        print(f"FAIL  {path} ships but {DISCLOSURE} does not name it", file=sys.stderr)
        failed = True

print(f"payload carries {len(actual)} executable file(s); every one must be declared and disclosed")
sys.exit(1 if failed else 0)
PY
}

pin_freshness() {
  local pin latest
  pin=$(readme_pin)
  latest=$(npm view skills version)
  echo "README pin skills@${pin}; npm latest ${latest}"
  if [[ "$pin" != "$latest" ]]; then
    local message="README pins skills@${pin}; npm latest is ${latest}. Deliberate pin; not a build failure."
    if [[ "${GITHUB_ACTIONS:-}" == "true" ]]; then
      echo "::warning title=Installer pin::${message}"
    else
      echo "WARNING: ${message}"
    fi
  fi
}

cmd=${1:-all}
case "$cmd" in
  installability) installability ;;
  links) links ;;
  payload) payload ;;
  pin) pin_freshness ;;
  all)
    installability
    links
    payload
    pin_freshness
    ;;
  *)
    echo "usage: $0 [all|installability|links|payload|pin]" >&2
    exit 2
    ;;
esac

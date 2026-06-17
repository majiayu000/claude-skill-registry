#!/usr/bin/env bash
source "$(dirname "$0")/_common.sh"

# Long-running poll loop for in-session Monitor / `tail -f`-style
# consumption. Emits one compact JSON object (CommentDto / CommentReplyDto
# shape) per new non-self comment on stdout, then sleeps and polls again.
# Exits on SIGINT / SIGTERM.
#
# Usage:
#   comments-stream.sh --artifact <shortId>
#                      [--interval <seconds>]   (default 30)
#                      [--status open|all]       (default all; `resolved`
#                                                 is supported but rarely
#                                                 useful — resolved threads
#                                                 don't tend to grow new
#                                                 replies)
#                      [--sentinel <prefix>]     (default
#                                                 ${DISPLAYDEV_REPLY_SENTINEL:-[claude-bot] };
#                                                 pass "" to disable the
#                                                 self-loop fuse)
#                      [--seen-file <path>]      (default tempfile cleaned
#                                                 on exit; pass a persistent
#                                                 path to dedupe across
#                                                 invocations, e.g. the
#                                                 Pattern-B `stream
#                                                 --exit-after 1` loop)
#                      [--exit-after <N>]        (exit 0 after N emissions
#                                                 instead of running
#                                                 forever; the Pattern-B
#                                                 idiom passes 1)
#
# Self-loop fuse: comments whose body begins with the sentinel are
# dropped before emission. `comment-reply.sh` reads the same default via
# DISPLAYDEV_REPLY_SENTINEL so the two helpers always agree on the
# fuse — override that env var to change it for the whole watch session
# instead of remembering to pass --sentinel to every helper.
#
# Cursor model: the server's `since` query is thread-level — it returns
# whole threads with any activity at-or-after the cursor, which includes
# old comments inside active threads. Client-side dedupe via the `seen`
# ID set is what guarantees each comment id is emitted at most once
# across the lifetime of this state (process for a tempfile; across
# invocations for a persistent --seen-file). NOW is captured *before*
# each fetch and used as the NEXT cursor on success — this closes the
# race where a comment committed between the API snapshot and the
# `date` call would otherwise be skipped.
#
# When --seen-file mode resumes from a prior invocation (header marker
# present), the *first* fetch deliberately omits --since so the API
# returns the full thread set: any comment created between invocations
# is older than this process's startup time and would be excluded by a
# tight --since filter, but the seen-set still dedupes everything else.
# Subsequent ticks use NOW as the cursor, so we only pay the "fetch
# everything" cost once per resume.
#
# Requires `jq`. Without `jq` we'd have to roll a comment-shaped JSON
# parser in bash — refusing is the saner default.

# Header marker written to the top of a --seen-file on first init.
# Subsequent invocations detect the marker to know "this file has been
# primed, don't re-prime from current state." Header-write happens
# *before* the priming fetch, so a crash anywhere after this point
# (including during the network call or the id append) still leaves a
# valid resume-state marker — the next invocation skips priming and
# the at-least-once seen-set dedupe handles recovery. The tradeoff: a
# priming-fetch failure (e.g. not signed in) leaves the file primed,
# so the subsequent successful run treats every existing comment as
# new. That's preferable to silently swallowing downtime comments.
SEEN_HEADER="# dsp-comments-seen v1"

ARTIFACT=""; INTERVAL="30"; STATUS="all"
SENTINEL="${DISPLAYDEV_REPLY_SENTINEL-[claude-bot] }"
SEEN_FILE=""; EXIT_AFTER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --artifact)
      if [[ $# -lt 2 ]]; then echo "comments-stream.sh: --artifact requires a value" >&2; exit 1; fi
      ARTIFACT="$2"; shift 2 ;;
    --interval)
      if [[ $# -lt 2 ]]; then echo "comments-stream.sh: --interval requires a value" >&2; exit 1; fi
      INTERVAL="$2"; shift 2 ;;
    --status)
      if [[ $# -lt 2 ]]; then echo "comments-stream.sh: --status requires a value" >&2; exit 1; fi
      STATUS="$2"; shift 2 ;;
    --sentinel)
      if [[ $# -lt 2 ]]; then echo "comments-stream.sh: --sentinel requires a value (use \"\" to disable)" >&2; exit 1; fi
      SENTINEL="$2"; shift 2 ;;
    --seen-file)
      if [[ $# -lt 2 ]]; then echo "comments-stream.sh: --seen-file requires a value" >&2; exit 1; fi
      SEEN_FILE="$2"; shift 2 ;;
    --exit-after)
      if [[ $# -lt 2 ]]; then echo "comments-stream.sh: --exit-after requires a value" >&2; exit 1; fi
      EXIT_AFTER="$2"; shift 2 ;;
    *) echo "comments-stream.sh: unrecognized arg: $1" >&2; exit 1 ;;
  esac
done

if [[ -z "$ARTIFACT" ]]; then
  echo "comments-stream.sh: --artifact is required" >&2; exit 1
fi
if ! printf '%s' "$INTERVAL" | LC_ALL=C grep -qE '^[0-9]+$'; then
  echo "comments-stream.sh: --interval must be a non-negative integer (seconds)" >&2; exit 1
fi
case "$STATUS" in
  open|resolved|all) ;;
  *) echo "comments-stream.sh: --status must be open|resolved|all" >&2; exit 1 ;;
esac
if [[ -n "$EXIT_AFTER" ]] && ! printf '%s' "$EXIT_AFTER" | LC_ALL=C grep -qE '^[1-9][0-9]*$'; then
  echo "comments-stream.sh: --exit-after must be a positive integer" >&2; exit 1
fi
require_jq_or_exit

LIST="$(dirname "$0")/comments-list.sh"

# Seen-state file. Two modes:
#   - --seen-file <path>: persistent across invocations. Header marker
#     distinguishes "already primed" from "fresh path that user just
#     created with touch."
#   - default: tempfile cleaned on EXIT/INT/TERM. Always primes.
PRIME_NEEDED=1
if [[ -n "$SEEN_FILE" ]]; then
  SEEN="$SEEN_FILE"
  # `touch` on an existing directory succeeds (updates mtime), so we
  # need an explicit guard before any grep/append against the path.
  if [[ -d "$SEEN" ]]; then
    echo "comments-stream.sh: --seen-file '$SEEN' is a directory" >&2; exit 1
  fi
  mkdir -p "$(dirname "$SEEN")"
  touch "$SEEN"
  # Header presence (not file size) is the "already primed" signal.
  # An empty file or one without the header gets primed once; the
  # header is written *before* the prime body, so a mid-prime crash
  # still produces a valid resume state.
  if grep -qxF "$SEEN_HEADER" "$SEEN" 2>/dev/null; then
    PRIME_NEEDED=0
  fi
else
  SEEN=$(mktemp -t dsp-comments-stream)
  # shellcheck disable=SC2064
  trap "rm -f '$SEEN'" EXIT INT TERM
fi

START_ISO=$(date -u +%Y-%m-%dT%H:%M:%SZ)

if [[ $PRIME_NEEDED -eq 1 ]]; then
  # Header first — before the network fetch, before any id append.
  # The window between `touch` and this write is microseconds, so a
  # crash there is the only case where downtime comments can be
  # swallowed on rerun. A crash anywhere *after* this point leaves the
  # header in place; the next invocation enters resume mode and
  # at-least-once delivery catches the gap. Trade: priming-fetch
  # failure (not signed in / invalid artifact) marks the file primed
  # too, so the next successful run emits every existing comment as
  # the agent's "backlog" — preferred over silent drops.
  if [[ -n "$SEEN_FILE" ]]; then
    printf '%s\n' "$SEEN_HEADER" > "$SEEN"
  fi
  # Run the priming call un-suppressed so genuine setup errors surface
  # as a loud startup failure instead of an infinite silent loop.
  if ! INIT_BODY=$("$LIST" --artifact "$ARTIFACT" --status all); then
    echo "comments-stream.sh: priming call failed; cannot watch artifact=$ARTIFACT" >&2
    exit 1
  fi
  printf '%s' "$INIT_BODY" \
    | "$JQ" -r '.data[]? | (., (.replies // [])[]) | .id' >> "$SEEN" || true
fi

echo "comments-stream.sh: watching artifact=$ARTIFACT since=$START_ISO interval=${INTERVAL}s sentinel=\"$SENTINEL\" seen=$SEEN${EXIT_AFTER:+ exit-after=$EXIT_AFTER}" >&2

# Initial cursor. In resume mode (PRIME_NEEDED=0) start empty so the
# first fetch returns everything — anything not in the loaded seen-set
# is something we missed between invocations and should emit. In fresh
# mode start at process startup so existing comments don't fire.
if [[ $PRIME_NEEDED -eq 0 ]]; then
  SINCE=""
else
  SINCE="$START_ISO"
fi

EMITTED=0
while true; do
  # Capture NOW *before* the fetch so the next cursor advances to a
  # point that can't be earlier than the comments we're about to read.
  # Anything created between this `date` and the API's snapshot is
  # picked up on the next tick.
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)
  if BODY=$("$LIST" --artifact "$ARTIFACT" ${SINCE:+--since "$SINCE"} --status "$STATUS" 2>/dev/null); then
    # Flatten root + replies into individual comment objects, drop
    # self-replies via the sentinel filter, emit as compact JSON.
    # Downstream dedupe is on `id`.
    while IFS= read -r line; do
      [[ -z "$line" ]] && continue
      # Extract id with a regex rather than re-invoking jq per line —
      # comment ids are quoted strings with no internal `"`, so a
      # straight grep is safe and avoids spawning a process per row.
      id=$(printf '%s' "$line" | grep -oE '"id":"[^"]+"' | head -n 1 | cut -d'"' -f4 || printf '')
      [[ -z "$id" ]] && continue
      if ! grep -qxF "$id" "$SEEN"; then
        # Echo first, append second. If the consumer closes the pipe
        # mid-tick (e.g. an external `| head -n 1`) the next `printf`
        # SIGPIPEs *before* the id is appended, so the comment isn't
        # marked seen and re-emits on the next invocation. With
        # append-first the comment would be silently dropped.
        printf '%s\n' "$line"
        printf '%s\n' "$id" >> "$SEEN"
        EMITTED=$((EMITTED + 1))
        if [[ -n "$EXIT_AFTER" && $EMITTED -ge $EXIT_AFTER ]]; then
          exit 0
        fi
      fi
    done < <(printf '%s' "$BODY" | "$JQ" -c --arg sentinel "$SENTINEL" '
      .data[]? | (., (.replies // [])[])
      | select($sentinel == "" or (.body | startswith($sentinel) | not))
    ' 2>/dev/null || true)
    # Advance the cursor only on a successful tick. Transient failures
    # (network, server hiccup) leave SINCE unchanged so the next tick
    # backfills automatically.
    SINCE="$NOW"
  fi
  sleep "$INTERVAL"
done

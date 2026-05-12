#!/usr/bin/env python3
"""Find the Claude Code transcript that produced a given commit and extract reasoning excerpts.

Usage:
  python3 scripts/find_transcript.py --commit <sha>
  python3 scripts/find_transcript.py --file <path>[:<line>]
  python3 scripts/find_transcript.py --file <path>:<line> --window-days 14

Resolves a commit SHA (directly or via `git blame`), locates the Claude Code project
transcript directory (~/.claude/projects/<encoded-cwd>/), ranks candidate transcripts
by time overlap and file/tool-use references, and extracts relevant user prompts and
assistant text messages from the top candidate.

Output: JSON on stdout with commit metadata, candidate list, and excerpts.
Exit codes: 0 on success (even if no transcripts found), 1 on usage errors, 2 on git failures.
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


def run_git(args, cwd=None):
    result = subprocess.run(
        ['git', *args],
        cwd=cwd,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout


def resolve_commit(commit, file_ref, repo_root):
    """Return commit SHA, resolving via git blame if needed."""
    if commit:
        sha = run_git(['rev-parse', commit], cwd=repo_root)
        if sha is None:
            return None
        return sha.strip()

    if file_ref:
        path, _, line = file_ref.partition(':')
        line = line or '1'
        blame = run_git(['blame', '-L', f'{line},{line}', '--porcelain', path], cwd=repo_root)
        if blame is None:
            return None
        blame_lines = blame.splitlines()
        first_line = blame_lines[0] if blame_lines else ''
        sha = first_line.split(' ', 1)[0] if first_line else ''
        if not sha or sha == '0000000000000000000000000000000000000000':
            return None
        return sha

    return None


def get_commit_meta(sha, repo_root):
    """Return dict with sha, timestamp (ISO), message, files touched."""
    info = run_git(
        ['show', '-s', '--format=%H%n%cI%n%s%n%b', sha],
        cwd=repo_root,
    )
    if info is None:
        return None
    lines = info.splitlines()
    if len(lines) < 3:
        return None
    files = run_git(['show', '--name-only', '--format=', sha], cwd=repo_root) or ''
    return {
        'sha': lines[0],
        'timestamp': lines[1],
        'subject': lines[2],
        'body': '\n'.join(lines[3:]).strip(),
        'files': [f for f in files.splitlines() if f],
    }


def project_transcript_dir(repo_root):
    """Derive ~/.claude/projects/<encoded>/ from an absolute project path.

    Claude Code encodes the cwd by replacing both '/' and '.' with '-'.
    """
    encoded = re.sub(r'[/.]', '-', str(repo_root))
    return Path.home() / '.claude' / 'projects' / encoded


def iter_transcripts(project_dir):
    if not project_dir.is_dir():
        return []
    return sorted(
        project_dir.glob('*.jsonl'),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def parse_timestamp(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None


def load_transcript_records(path, max_records=20000):
    """Stream-load a transcript JSONL file, capping records to avoid runaway memory."""
    records = []
    try:
        with path.open('r', encoding='utf-8', errors='replace') as f:
            for i, line in enumerate(f):
                if i >= max_records:
                    break
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
    except OSError:
        return []
    return records


def transcript_time_range(records):
    timestamps = []
    for r in records:
        ts = parse_timestamp(r.get('timestamp'))
        if ts is not None:
            timestamps.append(ts)
    if not timestamps:
        return (None, None)
    return (min(timestamps), max(timestamps))


def extract_text(message_content):
    """Pull plain text out of assistant or user message content (string or list of parts)."""
    if message_content is None:
        return ''
    if isinstance(message_content, str):
        return message_content
    if isinstance(message_content, list):
        parts = []
        for p in message_content:
            if not isinstance(p, dict):
                continue
            t = p.get('type')
            if t == 'text' and p.get('text'):
                parts.append(p['text'])
            elif t == 'tool_use':
                name = p.get('name', '')
                inp = p.get('input') or {}
                parts.append(f'[tool_use:{name} {json.dumps(inp)[:500]}]')
        return '\n'.join(parts)
    return ''


def score_transcript(records, commit_ts, touched_files):
    """Return (score, reasons, relevant_record_indices) for how well this transcript matches the commit."""
    score = 0
    reasons = []
    relevant_indices = []

    # Time overlap
    start, end = transcript_time_range(records)
    if start is not None and end is not None and commit_ts is not None:
        # Session must have had activity before the commit
        if start <= commit_ts:
            score += 2
            reasons.append('session active before commit')
        if start <= commit_ts <= end + timedelta(hours=2):
            score += 3
            reasons.append('commit within session window')

    file_hits = {}
    tool_hits = {}

    for idx, r in enumerate(records):
        is_relevant = False
        text_blob = ''
        msg = r.get('message') or {}
        content = msg.get('content')
        if content is not None:
            text_blob = extract_text(content)

        # Full-path text mentions only. Basename-only matching would false-positive on common filenames
        # (e.g., index.ts, main.py) appearing across unrelated transcripts in the time window.
        for full_path in touched_files:
            if full_path and full_path in text_blob:
                file_hits[full_path] = file_hits.get(full_path, 0) + 1
                is_relevant = True

        # Tool uses referencing touched files
        if isinstance(content, list):
            for part in content:
                if not isinstance(part, dict) or part.get('type') != 'tool_use':
                    continue
                name = part.get('name', '')
                if name not in ('Edit', 'Write', 'MultiEdit', 'NotebookEdit'):
                    continue
                inp = part.get('input') or {}
                fp = inp.get('file_path', '')
                for f in touched_files:
                    # Match full equality or a proper path suffix; plain endswith would
                    # false-match (e.g., '/src/foobar.py'.endswith('bar.py') is True).
                    if f and (fp == f or fp.endswith('/' + f)):
                        tool_hits[f] = tool_hits.get(f, 0) + 1
                        is_relevant = True
                        break

        if is_relevant:
            relevant_indices.append(idx)

    score += sum(file_hits.values())
    score += 3 * sum(tool_hits.values())

    if file_hits:
        reasons.append(f'mentions {len(file_hits)} touched file(s): {", ".join(sorted(file_hits))[:200]}')
    if tool_hits:
        reasons.append(f'edits {len(tool_hits)} touched file(s)')

    return score, reasons, relevant_indices


NOISE_PREFIXES = (
    '<command-message>',
    '<command-name>',
    '<command-args>',
    '<local-command-stdout>',
    '<local-command-caveat>',
    '<bash-input>',
    '<bash-stdout>',
    '<bash-stderr>',
    '<system-reminder>',
    'Base directory for this skill:',
    'Called the ',
    'Caveat: The messages below were generated',
)


def clean_text(content, rtype):
    """Extract and clean message text, returning None for non-reasoning content."""
    text = extract_text(content).strip()
    if not text:
        return None
    if rtype == 'user' and isinstance(content, list):
        if all(isinstance(p, dict) and p.get('type') == 'tool_result' for p in content):
            return None
    if any(text.startswith(p) for p in NOISE_PREFIXES):
        return None
    if rtype == 'assistant' and '[tool_use:' in text:
        lines = [l for l in text.split('\n') if not l.startswith('[tool_use:')]
        text = '\n'.join(lines).strip()
    return text or None


def extract_excerpts(records, relevant_indices, commit_ts, max_excerpts=40):
    """Return reasoning-relevant excerpts.

    Always captures every non-sidechain user prompt in the session (the intent is gold),
    plus substantive assistant text near relevant tool calls (filters out short transitions).
    """
    excerpts = []
    seen = set()

    interesting = set()
    for idx in relevant_indices:
        for j in range(max(0, idx - 2), min(len(records), idx + 3)):
            interesting.add(j)

    for idx, r in enumerate(records):
        if r.get('type') == 'user' and not r.get('isSidechain'):
            interesting.add(idx)

    for idx in sorted(interesting):
        if idx in seen:
            continue
        seen.add(idx)
        r = records[idx]
        rtype = r.get('type')
        if rtype not in ('user', 'assistant'):
            continue
        if r.get('isSidechain'):
            continue
        msg = r.get('message') or {}
        text = clean_text(msg.get('content'), rtype)
        if text is None:
            continue
        # Assistant: skip short transitional messages unless they sit directly at a relevant tool call
        if rtype == 'assistant' and len(text) < 80 and idx not in relevant_indices:
            continue
        excerpts.append({
            'index': idx,
            'role': rtype,
            'timestamp': r.get('timestamp'),
            'text': text[:2000],
        })
        if len(excerpts) >= max_excerpts:
            break

    return excerpts


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument('--commit', help='commit SHA to look up (overrides --file)')
    parser.add_argument('--file', help='file path, optionally FILE:LINE to use git blame')
    parser.add_argument('--window-days', type=int, default=14,
                        help='max days between commit and transcript mtime (default 14)')
    parser.add_argument('--limit', type=int, default=3,
                        help='max candidate transcripts to report (default 3)')
    parser.add_argument('--cwd', default=os.getcwd(),
                        help='project directory (default: current working directory)')
    args = parser.parse_args()

    if not args.commit and not args.file:
        print('error: --commit or --file is required', file=sys.stderr)
        return 1

    repo_root_raw = run_git(['rev-parse', '--show-toplevel'], cwd=args.cwd)
    if repo_root_raw is None:
        print('error: not a git repository', file=sys.stderr)
        return 2
    repo_root = Path(repo_root_raw.strip()).resolve()

    sha = resolve_commit(args.commit, args.file, repo_root)
    if sha is None:
        print(json.dumps({
            'status': 'no-commit',
            'error': 'could not resolve a commit (blame returned no author, or commit not found)',
        }))
        return 0

    meta = get_commit_meta(sha, repo_root)
    if meta is None:
        print(json.dumps({'status': 'no-commit', 'error': f'commit {sha} not found'}))
        return 0

    commit_ts = parse_timestamp(meta['timestamp'])
    project_dir = project_transcript_dir(repo_root)

    result = {
        'status': 'ok',
        'commit': meta,
        'project_dir': str(project_dir),
        'candidates': [],
    }

    if not project_dir.is_dir():
        result['status'] = 'no-transcripts'
        result['error'] = f'no Claude Code transcript dir for {repo_root}'
        print(json.dumps(result, indent=2))
        return 0

    touched = meta['files']
    window = timedelta(days=args.window_days)
    scored = []
    for path in iter_transcripts(project_dir):
        # Coarse pre-filter: skip files whose mtime is far from the commit to avoid
        # loading and parsing every historical transcript. score_transcript() uses
        # the precise in-file timestamps for the final time-overlap check.
        mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
        if commit_ts is not None and abs(mtime - commit_ts) > window:
            continue
        records = load_transcript_records(path)
        if not records:
            continue
        score, reasons, rel_idx = score_transcript(records, commit_ts, touched)
        if score <= 0:
            continue
        excerpts = extract_excerpts(records, rel_idx, commit_ts)
        scored.append({
            'session_id': path.stem,
            'jsonl_path': str(path),
            'mtime': mtime.isoformat(),
            'score': score,
            'match_reasons': reasons,
            'excerpt_count': len(excerpts),
            'excerpts': excerpts,
        })

    scored.sort(key=lambda c: c['score'], reverse=True)
    result['candidates'] = scored[: args.limit]

    if not result['candidates']:
        result['status'] = 'no-match'
        result['error'] = 'no transcript in the window matched the touched files'

    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())

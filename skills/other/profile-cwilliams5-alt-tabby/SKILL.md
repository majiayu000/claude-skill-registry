---
name: profile
description: Analyze speedscope profiles from Alt-Tabby's built-in profiler
user-invocable: true
disable-model-invocation: true
argument-hint: "[speedscope file or profile targeting]"
---
Analyze a profiling session captured by Alt-Tabby's `--profile` build. The user may provide additional context (specific file, focus area, comparison instructions, or multiple files to analyze together).

## File Resolution

Resolve the profile file(s) using the argument (if any):

1. **No argument**: Use `release/recorder/`, pick the newest `profile_*.speedscope.json` by modification time
2. **Count** (e.g., "3 newest", "last 2"): Load that many newest profiles from `release/recorder/`
3. **Exact filename** (no path separators): Search `release/recorder/` for a matching file
4. **Full path**: Use as-is
5. **"today"** or **"from today"**: All `profile_*.speedscope.json` files from today in `release/recorder/`

Use `ls -t release/recorder/profile_*.speedscope.json` to find files. Confirm the resolved file path(s) to the user before analyzing.

## Analysis Steps

Run these via `python tools/query_profile.py <file>`:

1. **Summary** (no flags) — always run first. Show the table to the user.
2. **Reentrancy check** (`--reentrant`) — always run. Flag any reentrant calls as potential bugs.
3. **Deep dive** — based on the summary, pick the top 2-3 functions by total time and run `--function <name>` on each. Use `query_timers.ps1` to check if hot functions are timer callbacks — this helps interpret high call counts (timer-driven vs event-driven). Focus on:
   - Unexpected caller chains (who is triggering this function and should they be?)
   - High call counts relative to session activity
   - Large max vs avg gaps (outliers worth investigating)

4. **User focus** — if the user specified a focus area (e.g., "investigate animation draw times", "look at komorebi processing"), prioritize functions related to that area in the deep dive.

## Multi-Profile Comparison

When analyzing multiple profiles:
- Run summary on each, present side-by-side
- Highlight differences: functions that appear in one but not others, significant count/time changes
- If the user described what varies between recordings (e.g., "different workspace switch types"), correlate the differences with the described scenarios

## Reporting

Present findings as:
- **Session overview**: duration, CPU%, key activity counts (switches, Alt-Tab cycles, etc.)
- **Hot spots**: top functions with actionable observations
- **Anomalies**: reentrancy, outlier calls, unexpected callers
- **Comparison**: if multiple profiles or the user mentions a previous profile, compare before/after metrics

Keep it concise — tables over prose. The user knows the codebase.

<!-- SOURCE-OF-TRUTH: shared/references/monitor_integration_pattern.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Monitor Integration Pattern

Claude Code `Monitor` tool (2.1.98+) for streaming background shell command output.

## When to Use

Use Monitor instead of `Bash` or `Bash(run_in_background=true)` when:
- Command expected duration >30 seconds
- Real-time error detection is valuable (test suites, builds)
- Multiple runs in sequence (profiling, benchmarking, keep/discard loops)

## Canonical Patterns

| Use Case | Command Pattern | timeout_ms | persistent |
|----------|----------------|------------|------------|
| Test suite | `{test_command} 2>&1 \| grep --line-buffered -E 'FAIL\|Error\|✗'` | match test timeout | false |
| Build | `{build_command} 2>&1 \| grep --line-buffered -iE 'error\|failed\|warning'` | 300000 | false |
| Container health | `docker compose logs -f 2>&1 \| grep --line-buffered -iE 'ready\|listening\|healthy'` | healthTimeout | false |
| Install + verify | `{install_command} && {verify_command} 2>&1` | 300000 | false |
| Multi-run loop | `{command} 2>&1 \| grep --line-buffered -E 'run\|result\|error'` | 600000 | false |
| Log streaming | `docker compose logs -f 2>&1 \| grep --line-buffered -E 'ERROR\|CRITICAL'` | 300000 | true |
| Agent wait (external review agent) | `tail -f {agent_log} \| grep --line-buffered -E 'Phase\|ERROR\|DONE'` | 120000 | false |

## Rules

- Use `grep --line-buffered` when piping — without it, buffering delays events by minutes
- Handle transient failures with `|| true` in poll loops
- Be selective with stdout — every line becomes a conversation message; unfiltered streams auto-stop
- Set `timeout_ms` from the skill's timeout option when available
- Fallback: if Monitor is unavailable (Bedrock/Vertex/Foundry), use `Bash(run_in_background=true)`

## Anti-patterns

- Streaming unfiltered output from verbose builds (auto-terminates)
- Using Monitor for commands that complete in <10 seconds
- Using Monitor instead of `Bash` when you need the exit code immediately

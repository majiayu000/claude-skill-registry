---
name: debug-e2e
description: Interactive debugging for failed e2e tests. Orchestrates the debugging session but delegates log reading to subagents to keep the main conversation clean. Use for ping-pong debugging sessions where you want to form and test hypotheses together with the user.
argument-hint: <hash, PR, URL, or test name>
---

# E2E Test Debugging

Interactive debugging for failed e2e tests. This skill orchestrates the debugging session but **never reads logs directly** - it delegates to subagents to keep the conversation context clean.

## Invocation

The user can invoke this skill with:
- **CI log hash**: `/debug-e2e 343c52b17688d2cd`
- **PR number**: `/debug-e2e #19783` or `/debug-e2e 19783`
- **CI URL**: `/debug-e2e http://ci.aztec-labs.com/...`
- **Test name**: `/debug-e2e epochs_l1_reorgs` (for general investigation)
- **No argument**: `/debug-e2e` then ask the user what they want to debug

## When to Use

- Debugging flaky or failing e2e tests
- Investigating CI failures that need deep analysis
- When you want to collaborate with the user on forming hypotheses
- When comparing failed and successful runs

## When NOT to Use

- **Obvious assertion failures**: If the test output clearly shows `expected 5, got 3`, just investigate the code directly
- **Build/compilation errors**: Use standard debugging, not log analysis
- **Simple configuration issues**: Missing env vars, wrong paths, etc.
- **When user just wants a quick answer**: This skill is for interactive ping-pong debugging sessions

## Key Principle

**Never read logs directly in this conversation.** Logs can be 50k+ lines and would pollute the context. Instead:
1. Use `identify-ci-failures` subagent to find failures and download logs
2. Use `analyze-logs` subagent to deep-dive specific logs
3. Work with the summaries they return

## Workflow

### Step 1: Identify Failures

Spawn the `identify-ci-failures` subagent:

```
Use Task tool with subagent_type: "identify-ci-failures"
Prompt: "Identify CI failures for [PR number / CI URL / hash]"
```

This returns:
- List of failures with types
- Local file paths for downloaded logs (e.g., `/tmp/<hash>.log`)
- History URL for finding successful runs

### Step 2: Discuss with User

Present findings to the user:
- What tests failed?
- What type of failure (timeout, assertion, error)?
- Form initial hypotheses together

### Step 3: Deep Dive with analyze-logs

Spawn the `analyze-logs` subagent with the **local file path**:

```
Use Task tool with subagent_type: "analyze-logs"
Prompt: "Analyze /tmp/<hash>.log focusing on test '<test_name>'. Look for [specific thing based on hypothesis]"
```

For comparison:
```
Prompt: "Compare /tmp/<failed>.log with /tmp/<success>.log for test '<test_name>'. Find divergence points."
```

### Step 4: Refine Hypothesis

Based on the summary:
- Does the evidence support the hypothesis?
- What contradicts it?
- What new questions arise?

Discuss with user, then spawn another `analyze-logs` if needed.

### Step 5: Investigate Codebase

Once you have a theory, search the codebase:
- Use Grep to find where specific log messages are generated
- Read the code context around log emission points
- Trace execution paths

### Step 6: Suggest Fix or Local Test

Either:
- Propose a code fix based on findings
- Suggest running the test locally to verify:
  ```bash
  yarn workspace @aztec/end-to-end test:e2e <file>.test.ts -t '<test name>'
  ```

## Hypothesis Formation

Take time to think deeply before proposing theories.

For each hypothesis:
1. **Clearly state the theory**: "The test fails because X happens when Y"
2. **Identify expected evidence**: "If this is correct, we should see log entries for Z"
3. **Ask analyze-logs to verify**: Spawn subagent to look for specific evidence
4. **Look for contradictions**: What would disprove this theory?
5. **Assign confidence**: high / medium / low based on evidence

Formulate multiple competing hypotheses when the cause is unclear.

## Investigation Principles

- **Be systematic**: Follow the workflow, don't jump to conclusions
- **Be evidence-based**: Every theory must be backed by log entries or code
- **Be critical**: Actively seek to disprove your own hypotheses
- **Be thorough**: Check timing, sequence, missing events, code context
- **Be clear**: Use specific timestamps and quotes from summaries
- **Be practical**: Suggest fixes that address root causes

## History Investigation

To understand when a test started failing:

1. Look for the `history:` marker at the **beginning** of the log file (first few lines)
2. The history shows recent runs of this exact test with PASSED/FAILED/FLAKED status:
   ```
   01-23 17:10:11: PASSED (2614d91ec48f4047): ... (Author: commit message (#PR))
   01-23 17:08:30: FLAKED (10d5f47f04025f1c): ... (code: 1) group:e2e-p2p-epoch-flakes (Author: commit message (#PR))
   01-23 16:51:21: FLAKED (512e978edff9e471): ... (code: 1) group:e2e-p2p-epoch-flakes (Author: commit message (#PR))
   ```
3. Identify the transition point where test started failing/flaking
4. Check the PR mentioned in the commit message to understand what changed
5. Download logs from both passing and failing runs to compare:
   - Use hash from history (e.g., `2614d91ec48f4047` for passed, `10d5f47f04025f1c` for failed)
   - `yarn ci dlog <hash> > /tmp/<hash>.log 2>&1` downloads the log to a local tmp file

**Important**: Do NOT use `gh run list` - the history in the log file is more accurate for this specific test.

## Local Test Running

To run tests locally for verification:

```bash
# Run specific test
yarn workspace @aztec/end-to-end test:e2e <file>.test.ts -t '<test name>'

# With verbose logging
LOG_LEVEL=verbose yarn workspace @aztec/end-to-end test:e2e <file>.test.ts -t '<test name>'

# With debug logging (very detailed)
LOG_LEVEL=debug yarn workspace @aztec/end-to-end test:e2e <file>.test.ts -t '<test name>'

# With specific module logging
LOG_LEVEL='info; debug:sequencer,p2p' yarn workspace @aztec/end-to-end test:e2e <file>.test.ts -t '<test name>'
```

## Log Structure

### Timestamp Format
Logs use ISO timestamps: `2024-01-23T17:08:30.123Z` - useful for correlating events across nodes.

### Log Levels
- `ERROR` - Failures, exceptions
- `WARN` - Potential issues, recoverable problems
- `INFO` - Key events, state transitions
- `VERBOSE` - Detailed operational info
- `DEBUG` - Fine-grained debugging (very noisy)

### Component Prefixes
Log lines are prefixed with the component name (e.g., `aztec:sequencer`, `aztec:p2p`, `aztec:archiver`). These map to the **Key Packages** section in CLAUDE.md - use that as a reference for understanding what each component does.

## Multi-Node Debugging

E2E tests often spawn multiple nodes. Key tips:

### Identifying Nodes
- Look for node identifiers in log prefixes: `node-0`, `node-1`, `validator-0`, etc.
- Each node has its own log stream but they're interleaved in the combined output
- Ask `analyze-logs` to filter by node when needed

### Cross-Node Correlation
- Use timestamps to correlate events across nodes
- Look for message propagation: "Node A sends X" → "Node B receives X"
- Check for missing events: if Node A sent but Node B never received, that's a clue

### Common Multi-Node Issues
- **Network partition**: Nodes can't reach each other
- **Clock skew**: Timestamps don't align, causing validation failures
- **Split brain**: Nodes have divergent views of state
- **Message ordering**: Events arrive in unexpected order

## Common Failure Patterns

### Timeout Failures
- Action executed, expected reaction didn't occur
- Ask analyze-logs to find: what was the last action? What was expected?
- Check for blocked operations, missing events, stuck processes

### Assertion Failures
- Test expectation not met
- Compare actual vs expected values
- Trace back to find where the wrong value originated

### State Pollution
- Previous test left system in bad state
- Compare logs from the failing test with the same test in isolation
- Check `beforeEach`/`afterEach` hooks

### Race Conditions
- Timing-dependent failures
- Look for operations completing in different order
- Check for missing synchronization

## Example Session

```
User: Debug this flaky test: 343c52b17688d2cd

Claude: [Spawns identify-ci-failures subagent]
        Returns: epochs_l1_reorgs.test.ts failed with timeout after 383s
        Log downloaded to /tmp/343c52b17688d2cd.log
        History shows test started flaking recently

Claude: The test "handles reorgs spanning epoch boundaries" timed out. Looking at
        the history, this test has been flaking since yesterday. The failures correlate
        with PR #19783 "adding MAXIMUM_GOSSIP_CLOCK_DISPARITY for p2p validation".

        Let me check a passing run to compare. [Spawns analyze-logs for both]

User: What do you see as differences?

Claude: [Spawns analyze-logs with comparison prompt]
        Summary shows: In failed run, node-2 never received epoch proof notification.
        In passing run, all nodes received it within 2s of each other.

        Hypothesis: The new clock disparity check may be rejecting valid messages
        during epoch transitions when clocks drift slightly.

User: Can you check if there are any logs about clock validation?

Claude: [Spawns analyze-logs with specific prompt]
        Found: "Rejecting gossip message: clock disparity 3.2s exceeds maximum 2s"
        This confirms the hypothesis.

Claude: [Searches codebase for MAXIMUM_GOSSIP_CLOCK_DISPARITY]
        Found in p2p/config.ts, default is 2 seconds. The PR added this validation
        but epoch proofs can take longer to propagate. Recommend increasing the
        disparity threshold for epoch-related messages.
```

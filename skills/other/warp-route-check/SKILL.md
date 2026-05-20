---
name: warp-route-check
description: A skill that allows a user to validate that a warp route deployment will be in the expected state after applying some configuration
---

# Warp Route Deployment Checker

You are a specialized agent for checking warp route deployments and updates using the Hyperlane CLI and Heimdall CLI.

## Prerequisites

This skill requires the following tools and setup:

### Required Tools

1. **Hyperlane CLI**: `npm install -g @hyperlane-xyz/cli`
2. **Heimdall**: Ethereum transaction decoder
3. **Foundry (cast)**: `curl -L https://foundry.paradigm.xyz | bash && foundryup`
4. **jq**: JSON processor (`brew install jq` or `apt-get install jq`)
5. **Python 3**: With standard library
6. **pnpm**: Package manager

### Required Setup

1. **Hyperlane Registry** cloned (default location: `$HOME/hyperlane-registry`):

   ```bash
   git clone https://github.com/hyperlane-xyz/hyperlane-registry.git $HOME/hyperlane-registry
   ```

2. **Hyperlane Monorepo** cloned (required for http-registry):

   ```bash
   git clone https://github.com/hyperlane-xyz/hyperlane-monorepo.git
   export HYPERLANE_MONOREPO="/path/to/hyperlane-monorepo"
   ```

3. **Optional: http_registry shell function** (add to ~/.zshrc or ~/.bashrc):
   ```bash
   function http_registry() {
     pnpm -C $HYPERLANE_MONOREPO/typescript/infra start:http-registry
   }
   ```

### Environment Variables (Optional)

```bash
export HYPERLANE_REGISTRY="$HOME/hyperlane-registry"  # Custom registry location
export HYPERLANE_MONOREPO="/path/to/monorepo"        # Monorepo location
```

---

## Your Task

Follow these steps to verify a warp route deployment:

### Step 0: Verify Environment

**Verify all required tools and paths before proceeding:**

```bash
# Check required CLI tools
command -v hyperlane >/dev/null 2>&1 || { echo "❌ hyperlane CLI not installed. Run: npm install -g @hyperlane-xyz/cli"; exit 1; }
command -v heimdall >/dev/null 2>&1 || { echo "❌ heimdall not installed"; exit 1; }
command -v cast >/dev/null 2>&1 || { echo "❌ foundry not installed. Run: curl -L https://foundry.paradigm.xyz | bash"; exit 1; }
command -v jq >/dev/null 2>&1 || { echo "❌ jq not installed"; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "❌ python3 not installed"; exit 1; }

echo "✅ All required tools installed"
```

```bash
# Determine registry location (configurable via env var)
REGISTRY_PATH="${HYPERLANE_REGISTRY:-$HOME/hyperlane-registry}"

# Verify registry exists
if [ ! -d "$REGISTRY_PATH" ]; then
  echo "❌ Registry not found at $REGISTRY_PATH"
  echo "Clone it: git clone https://github.com/hyperlane-xyz/hyperlane-registry.git $REGISTRY_PATH"
  exit 1
fi

echo "✅ Registry found at $REGISTRY_PATH"
```

```bash
# Determine HTTP registry start command
if type http_registry >/dev/null 2>&1; then
  HTTP_REGISTRY_CMD="http_registry"
elif [ -n "$HYPERLANE_MONOREPO" ] && [ -d "$HYPERLANE_MONOREPO/typescript/infra" ]; then
  HTTP_REGISTRY_CMD="pnpm -C $HYPERLANE_MONOREPO/typescript/infra start:http-registry"
else
  echo "❌ Cannot start HTTP registry. Please either:"
  echo "  1. Set HYPERLANE_MONOREPO env var pointing to monorepo, OR"
  echo "  2. Define http_registry function in your shell"
  exit 1
fi

echo "✅ HTTP registry command available"
```

### Step 1: Get Warp Route ID

- Ask the user for the warp route ID if not provided
- The warp route ID should be in the format used by the Hyperlane registry

**Common Chain IDs Reference** (for parsing transactions):

```
1 = ethereum          8453 = base
10 = optimism         42161 = arbitrum
56 = bsc              43114 = avalanche
88 = viction          59144 = linea
130 = unichain        137 = polygon
```

_Check fork output for complete mappings_

### Step 2: Verify Registry Branch

- **CRITICAL**: The hyperlane-registry location is in `$REGISTRY_PATH` (default: `$HOME/hyperlane-registry`)
- Confirm with the user that the registry is pointing to the correct branch
- The registry should contain the expected final configuration
- Ask the user to specify the branch name if not already confirmed
- Verify the current branch with `git -C "$REGISTRY_PATH" branch --show-current`
- If not on the correct branch, ask the user to switch branches first
- **Remember the original branch** - you'll need to switch back to `main` at the end

### Step 3: Start HTTP Registry (Background)

- Run the HTTP registry command determined in Step 0 in the background
- Use `run_in_background=true` parameter for Bash tool
- **CRITICAL**: Check the output to find the ACTUAL port (commonly 3333, but may vary)
- Look for "Server running" message with port number in the background task output
- Note the registry URL (e.g., http://localhost:3333 or http://localhost:XXXX)
- **DO NOT assume port 3333** - always verify from output

```bash
# Use command determined in Step 0
$HTTP_REGISTRY_CMD > /tmp/http-registry.log 2>&1 &
```

### Step 4: Fork the Warp Route (Background)

- **IMPORTANT**: `hyperlane warp fork` also blocks - it runs a server for the forked registry
- Use the installed `hyperlane` command
- Run `hyperlane warp fork` with the provided warp route ID **in the background**
- This creates local forked chains (anvil instances) and serves the forked registry
- Use the registry URL from step 3 as the source
- **CRITICAL**: Check the output to find the ACTUAL forked registry port (commonly 8535, but may vary)
- Look for "Server running" message with port number (e.g., `{ port: 8535 } Server running`)
- Note the forked registry URL: `http://localhost:<actual-port>`
- Wait for the fork server to be ready (check output for "Server running")
- **IMPORTANT**: Each chain in the warp route gets its own anvil instance on sequential ports starting at 8545
- **CRITICAL**: Check the fork output for ACTUAL port assignments per chain - DO NOT use example ports

```bash
# Use ACTUAL registry URL from Step 3
hyperlane warp fork --id <warp-route-id> --registry <actual-registry-url-from-step-3>
```

**Read fork output carefully** to extract:

1. Forked registry server port (e.g., "{ port: 8535 } Server running")
2. Chain-specific anvil ports (e.g., "Successfully started Anvil node for chain ethereum at http://127.0.0.1:YYYY")

**Create a port mapping** from the fork output for later use.

### Step 5: Analyze Transactions File (CRITICAL - Multiple Owners Detection)

**IMPORTANT**: Before submitting transactions, you MUST analyze the transaction file to detect if it targets multiple owners per chain.

#### 5a. Identify Chains and Contracts with Transactions

```bash
# Get all unique chain IDs
jq -r '.[].chainId' <transactions-file> | sort -u

# Get all unique contract addresses per chain
jq -r '.[] | "\(.chainId)|\(.to)"' <transactions-file> | sort -u
```

**Map chain IDs to names** using the fork output (don't assume - verify actual chain names).

#### 5b. Query Owners for ALL Contract Addresses

**CRITICAL**: For EACH unique contract address being targeted, query its current owner from the forked chain.

```bash
# For each contract on each chain (use ACTUAL ports from fork output):
cast call <contract-address> "owner()(address)" --rpc-url http://localhost:<ACTUAL-PORT-FOR-CHAIN>
```

**Example workflow** (ports shown are examples - use ACTUAL ports from YOUR fork output):

```bash
# Example assumes fork output showed: ethereum at port 8548, arbitrum at port 8545
# YOUR ports may differ - always check YOUR fork output

# Query ethereum contracts (use YOUR actual port from fork output)
cast call 0xe1De... "owner()(address)" --rpc-url http://localhost:<YOUR-ETH-PORT>
cast call 0xcf4ec... "owner()(address)" --rpc-url http://localhost:<YOUR-ETH-PORT>

# Query arbitrum contracts (use YOUR actual port from fork output)
cast call 0xAd435... "owner()(address)" --rpc-url http://localhost:<YOUR-ARB-PORT>
```

**Create complete owner mapping**:

```json
{
  "<chainId>_<contractAddress>": "<actual-owner-address>",
  "1_0xe1De9910fe71cC216490AC7FCF019e13a34481D7": "0x3965...",
  "1_0xcf4ecA86606372B975FaF04a97e8eE3AfeA5a02D": "0x8Ff4..."
}
```

**Note**: Owners may be contract addresses (multisigs, timelocks) - this is OK, anvil can impersonate them.

#### 5c. Detect Multiple Owners Per Chain

Group transactions by chain and owner to detect if splitting is needed:

```python
# Pseudocode logic
for each chain:
    unique_owners = set of owners for contracts on this chain
    if len(unique_owners) > 1:
        # Chain has multiple owners - splitting required
        splitting_needed = True
```

**If ANY chain has multiple owners**: Proceed to Step 5d (split transactions)
**If all chains have single owner**: Skip to Step 5e (create single strategy)

#### 5d. Split Transactions by Owner (If Multiple Owners Detected)

**When to do this**: If Step 5c detected multiple owners per chain.

**How to split**:

1. Create owner-to-contract mapping from Step 5b
2. Group transactions by the owner of their target contract
3. Create separate transaction files for each unique owner
4. Each file contains only transactions targeting contracts owned by that owner

```python
# Split transactions by owner
owner_groups = group_by(transactions, lambda tx: owner_map[f"{tx.chainId}_{tx.to}"])

for owner, txs in owner_groups:
    write_file(f"/tmp/transactions-owner-{owner}.json", txs)
```

**Example**: If 171 transactions target 17 different owners across 6 chains, create 17 separate transaction files.

**Proceed to Step 5f** for each split file.

#### 5e. Create Single Strategy File (If Single Owner Per Chain)

**When to do this**: If Step 5c found no multiple owners per chain.

Create one strategy file with one owner per chain:

```yaml
<chain-name>:
  submitter:
    chain: <chain-name>
    type: impersonatedAccount
    userAddress: '<actual-owner-from-step-5b>'
```

Save to `/tmp/<route>-strategy.yaml`

**Proceed to Step 5g**.

#### 5f. Create Multiple Strategy Files (If Transactions Were Split)

**When to do this**: If Step 5d split transactions.

For each split transaction file, create a corresponding strategy file:

1. Identify which chains are in that transaction file
2. For each chain, use the owner that matches the split group
3. Create chain-specific strategy with that owner

```yaml
<chain-name>:
  submitter:
    chain: <chain-name>
    type: impersonatedAccount
    userAddress: '<owner-for-this-split>'
```

Save each as `/tmp/strategy-owner-<owner>.yaml`

#### 5g. Fund All Owner Accounts

Use `anvil_setBalance` to fund ALL unique owner addresses on their respective chains (use ACTUAL ports from fork output):

```bash
BALANCE="0x56BC75E2D63100000"  # 100 ETH

# For each owner on each chain (use YOUR ACTUAL port from fork output):
cast rpc anvil_setBalance <owner-address> $BALANCE --rpc-url http://localhost:<YOUR-ACTUAL-PORT>
```

**Example** (ports shown are examples - use YOUR actual ports from fork output):

```bash
# Example assumes fork output showed ethereum at port 8548
# YOUR port may differ - use YOUR actual port from fork output

cast rpc anvil_setBalance 0x3965... $BALANCE --rpc-url http://localhost:<YOUR-ETH-PORT>
cast rpc anvil_setBalance 0x8Ff4... $BALANCE --rpc-url http://localhost:<YOUR-ETH-PORT>
```

**Fund ALL unique owners** you identified in Step 5b.

### Step 6: Submit Transactions

#### 6a. Determine Submission Approach

- **Single strategy**: Submit once with one transaction file (from Step 5e)
- **Multiple strategies**: Submit multiple times, once per split file (from Step 5f)

#### 6b. Submit Each Transaction File

For each transaction file and its corresponding strategy:

```bash
# Set dummy HYP_KEY (required even with impersonation)
HYP_KEY="0x0000000000000000000000000000000000000000000000000000000000000001"

# Submit transactions using installed hyperlane command with ACTUAL forked registry URL
hyperlane submit \
  --transactions <transactions-file> \
  --strategy <corresponding-strategy-file> \
  --registry <YOUR-ACTUAL-forked-registry-url-from-step-4> \
  --yes
```

**CRITICAL**:

- Use the installed `hyperlane` command
- **No need for --id parameter** - submit auto-detects chains from transactions file
- Use **YOUR ACTUAL forked registry URL** from Step 4 (NOT the source registry URL from Step 3)
- Dummy HYP_KEY is required even with impersonation

**Track submission results**:

- Count successful submissions
- Count failed submissions
- Note any error messages

**If using split files**: Submit all files sequentially, tracking success/failure for each.

### Step 7: Decode Transactions with Heimdall

**IMPORTANT**: After submission, decode ALL transactions using Heimdall for the final report.

```python
# For each transaction in the original combined file:
for tx in transactions:
    decoded = run_command(f"heimdall decode {tx.data} --default")
    store_decoded(tx.chainId, tx.to, tx.annotation, decoded)
```

**Save decoded output** as JSON for inclusion in final report:

```json
[
  {
    "index": 1,
    "chain": "ethereum",
    "to": "0x...",
    "annotation": "...",
    "decoded": "..."
  }
]
```

Save to `/tmp/decoded-transactions.json`

### Step 8: Run Warp Check

Execute `hyperlane warp check` against the forked registry (use YOUR ACTUAL URL from Step 4):

```bash
hyperlane warp check \
  --id <warp-route-id> \
  --registry <YOUR-ACTUAL-forked-registry-url-from-step-4> \
  --yes
```

**Capture full output** to `/tmp/warp-check.log` for the final report.

**NOTE**: Warp check may show provider errors for newly added chains - this is expected.

### Step 9: Interpret Results

Analyze the warp check output carefully:

**CRITICAL**: Focus on violations for chains that have transactions. Violations on other chains are expected since those chains aren't being modified.

#### Expected Violations (✅ These are OK)

**1. Violations on chains WITHOUT transactions**: ALWAYS EXPECTED

```yaml
avalanche: # ← No transactions for this chain
  proxyAdmin:
    owner:
      EXPECTED: '0x...'
      ACTUAL: '0x...'
```

**Why**: Chains not in the transactions file are not being modified. Their violations show the gap between current and target state.

**2. Ownership mismatches on chains WITH transactions**: EXPECTED if transactions don't include ownership transfers

```yaml
ethereum: # ← Has transactions, but ownership not transferred yet
  proxyAdmin:
    owner:
      EXPECTED: '0x...'
      ACTUAL: '0x...'
```

**Why**: The registry shows TARGET state after full deployment. If transactions configure functionality but don't transfer ownership, ownership differences are expected.

**3. Fee configuration differences**: MAY BE EXPECTED

```yaml
ethereum:
  tokenFee:
    maxFee:
      ACTUAL: '115792...'
      EXPECTED: ''
```

**Why**: Transactions may SET fee values that aren't in the registry config yet.

#### Real Violations (❌ These are problems)

These indicate actual configuration issues **on chains WITH transactions**:

```yaml
ethereum: # ← Has transactions but missing expected config
  remoteRouters:
    42161: # arbitrum domain
      ACTUAL: ''
      EXPECTED: '0x...'
```

**Real problems to look for**:

- Missing ISM configurations that should have been set
- Missing remote router enrollments that transactions should have added
- Missing destination gas settings that transactions should have configured
- Incorrect xERC20 limits (except for new chains showing 0.0)

**Key**: Only violations on chains that have transactions AND should have been fixed by those transactions are real problems.

### Step 10: Generate Final Report

Create a comprehensive markdown report with the following sections:

#### Report Structure

````markdown
# <WARP_ROUTE_ID> Validation Report

**Date:** <timestamp>
**Branch:** <registry-branch>
**Transaction File:** <filename>

## Executive Summary

[Overall pass/fail verdict]
[Key metrics: total transactions, chains modified, success rate]

## Port Detection (Dynamic)

[List all ports extracted from fork output]

- HTTP Registry: <actual-port>
- Forked Registry: <actual-port>
- Chain Ports: [chain: port mapping]

## Transaction Breakdown

[Table showing chains with transactions, counts, owners]

## Submission Results

[Detailed results of transaction submission]

- Split files created (if applicable)
- Submission success/failure counts
- Any errors encountered

## Warp Check Results

### Chains WITH Transactions

[Analysis of functional configuration]

- Routers: [status]
- Destination gas: [status]
- ISM: [status]
- Bridge allowances: [status]

### Chains WITHOUT Transactions

[List of chains not modified and their expected violations]

## Decoded Transactions (Heimdall Output)

```json
[Full decoded transaction output from /tmp/decoded-transactions.json]
```
````

## Warp Check Output (Raw)

```
[Full warp check output from /tmp/warp-check.log]
```

## Conclusion

[Final verdict with supporting rationale]

````

**Save report** to `/tmp/<route>-validation-report.md`

### Step 11: Cleanup

- Clean up **both** background processes:
  - Stop the `hyperlane warp fork` server
  - Stop the `http_registry` server
- **Switch registry branch back to main**: `git -C "$REGISTRY_PATH" checkout main`
- Confirm cleanup is complete

```bash
# Kill background processes
pkill -f "hyperlane warp fork"
pkill -f "http_registry"

# Switch back to main (use $REGISTRY_PATH variable)
git -C "$REGISTRY_PATH" checkout main
````

## Common Issues & Solutions

### "Ownable: caller is not the owner"

- **Cause**: Using wrong owner address or single-owner strategy with multi-owner transactions
- **Solution**: Always query actual owners (Step 5b) and split transactions if multiple owners detected (Step 5d)

### "Insufficient funds for intrinsic transaction cost"

- **Cause**: Impersonated accounts have no balance on forked chains
- **Solution**: Use `anvil_setBalance` (Step 5g) for ALL unique owners

### Multiple owners per chain causing submission failure

- **Cause**: Transaction file targets contracts with different owners on same chain
- **Solution**: Automatically detect in Step 5c and split transactions in Step 5d

### Port connection errors

- **Cause**: Using example ports instead of actual ports from fork output
- **Solution**: ALWAYS parse fork output for actual port assignments, never hardcode

### "http_registry: command not found"

- **Cause**: http_registry function not defined
- **Solution**: Set HYPERLANE_MONOREPO env var or define function in shell profile

### "Registry not found"

- **Cause**: Registry not at expected location
- **Solution**: Set HYPERLANE_REGISTRY env var or clone to $HOME/hyperlane-registry

### Warp check shows provider errors for newly added chains

- **Cause**: Newly added chains may cause provider errors
- **Expected**: This is often normal for new chain additions
- **Solution**: Use `hyperlane warp read` as fallback validation if needed

## Key Learnings

1. **Never use config owners for impersonation** - always query actual on-chain owners
2. **Always check for multiple owners per chain** - split transactions if detected
3. **Never hardcode ports** - always extract from fork output
4. **Ownership violations are usually expected** - they show current vs future state
5. **Decode transactions with Heimdall** - include in final report
6. **Generate comprehensive report** - include interpretation + raw outputs
7. **Distinguish functional from ownership violations** - only functional violations on chains with transactions are problems
8. **Fund ALL unique owners** - not just warp route owners
9. **Both servers must run in background** - HTTP registry AND warp fork
10. **Always cleanup and switch back to main** - leave environment clean
11. **Verify prerequisites before starting** - check tools and paths exist
12. **Use environment variables for paths** - makes skill portable across machines

## Port Detection Best Practices

**CRITICAL**: Never assume port numbers. Always extract from actual output.

```bash
# ❌ WRONG - Hardcoded port
cast call <addr> "owner()" --rpc-url http://localhost:8550

# ✅ CORRECT - Use actual port from YOUR fork output
# First: Extract port from YOUR fork output file
PORT=$(grep "Successfully started Anvil node for chain ethereum" /tmp/warp-fork.log | \
  grep -oE "http://127.0.0.1:([0-9]+)" | cut -d: -f3)
cast call <addr> "owner()" --rpc-url http://localhost:$PORT
```

Build a port mapping dictionary from YOUR fork output and reference it throughout.

## Environment Variable Reference

| Variable             | Default                    | Purpose                             |
| -------------------- | -------------------------- | ----------------------------------- |
| `HYPERLANE_REGISTRY` | `$HOME/hyperlane-registry` | Registry location                   |
| `HYPERLANE_MONOREPO` | (required)                 | Monorepo location for http-registry |
| `REGISTRY_PATH`      | `$HYPERLANE_REGISTRY`      | Used internally by skill            |
| `HTTP_REGISTRY_CMD`  | (auto-detected)            | Command to start HTTP registry      |

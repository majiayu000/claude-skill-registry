---
name: deploy-contracts
description:
  "Safely deploys Move contracts to Aptos networks (devnet, testnet, mainnet) with pre-deployment verification. Triggers
  on: 'deploy contract', 'publish to testnet', 'deploy to mainnet', 'how to deploy', 'publish module', 'deployment
  checklist', 'deploy to devnet'."
license: MIT
metadata:
  author: aptos-labs
  version: "1.0"
  category: move
  tags: ["deployment", "devnet", "testnet", "mainnet", "publishing"]
  priority: high
---

# Deploy Contracts Skill

## Overview

This skill guides safe deployment of Move contracts to Aptos networks. **Always deploy to testnet before mainnet.**

## Pre-Deployment Checklist

Before deploying, verify ALL items:

### Security Audit ⭐ CRITICAL - See [SECURITY.md](../../../patterns/move/SECURITY.md)

- [ ] Security audit completed (use `security-audit` skill)
- [ ] All critical vulnerabilities fixed
- [ ] All security patterns verified (arithmetic safety, storage scoping, reference safety, business logic)
- [ ] Access control verified (signer checks, object ownership)
- [ ] Input validation implemented (minimum thresholds, fee validation)
- [ ] No unbounded iterations (per-user storage, not global vectors)
- [ ] Atomic operations (no front-running opportunities)
- [ ] Randomness security (if applicable - entry functions, gas balanced)

### Testing

- [ ] 100% test coverage achieved: `aptos move test --coverage`
- [ ] All tests passing: `aptos move test`
- [ ] Coverage report shows 100.0%
- [ ] Edge cases tested

### Code Quality

- [ ] Code compiles without errors: `aptos move compile`
- [ ] No hardcoded addresses (use named addresses)
- [ ] Error codes clearly defined
- [ ] Functions properly documented

### Configuration

- [ ] Move.toml configured correctly
- [ ] Named addresses set up: `my_addr = "_"`
- [ ] Dependencies specified with correct versions
- [ ] Network URLs configured

## Object Deployment (Modern Pattern)

### CRITICAL: Use Correct Deployment Command

There are TWO ways to deploy contracts. For modern object-based contracts, use `deploy-object`:

**✅ CORRECT: Object Deployment (Modern Pattern)**

```bash
aptos move deploy-object \
    --address-name my_addr \
    --profile devnet \
    --assume-yes
```

**What this does:**

1. Creates an object to host your contract code
2. Deploys the package to that object's address
3. Returns the object address (deterministic, based on deployer + package name)
4. Object address becomes your contract address

**❌ WRONG: Using Regular Publish for Object Contracts**

```bash
# ❌ Don't use this for object-based contracts
aptos move publish \
    --named-addresses my_addr=<address>
```

**When to use each:**

- `deploy-object`: Modern contracts using objects (RECOMMENDED)
- `publish`: Legacy account-based deployment (older pattern)

**How to tell if you need object deployment:**

- Your contract creates named objects in `init_module`
- Your contract uses `object::create_named_object()`
- You want a deterministic contract address
- Documentation says "deploy as object"

### Alternative Object Deployment Commands

**Option 1: `deploy-object` (Recommended - Simplest)**

```bash
aptos move deploy-object --address-name my_addr --profile devnet
```

- Automatically creates object and deploys code
- Object address is deterministic
- Best for most use cases

**Option 2: `create-object-and-publish-package` (Advanced)**

```bash
aptos move create-object-and-publish-package \
    --address-name my_addr \
    --named-addresses my_addr=default
```

- More complex command with more options
- Use only if you need specific object configuration
- Generally not needed

**Recommendation:** Always use `deploy-object` unless you have a specific reason to use the alternative.

## Deployment Workflow

### Step 1: Test Locally

```bash
# Ensure all tests pass
aptos move test

# Verify 100% coverage
aptos move test --coverage
aptos move coverage summary
# Expected output: "coverage: 100.0%"
```

### Step 2: Compile

```bash
# Compile contract
aptos move compile --named-addresses my_addr=<your_address>

# Verify compilation succeeds
echo $?
# Expected: 0 (success)
```

### Step 3: Deploy to Devnet (Optional)

**Devnet is for quick testing and experimentation. Account is auto-funded on `aptos init`.**

Check if a profile exists before initializing:

```bash
# Check if default profile exists (look for "default" in output)
aptos config show-profiles

# If no profile exists, initialize one (auto-funds on devnet)
aptos init --network devnet --assume-yes
```

```bash
# Deploy as object (modern pattern)
aptos move deploy-object \
    --address-name my_addr \
    --profile default \
    --assume-yes

# Save the object address from output for future upgrades
# Output: "Code was successfully deployed to object address 0x..."

# Verify deployment
aptos account list --account <object_address> --profile default
```

### Step 4: Deploy to Testnet (REQUIRED)

**Testnet is for final testing before mainnet.**

Check if a profile exists before initializing:

```bash
# Check if default profile exists
aptos config show-profiles

# If no profile exists, initialize one
aptos init --network testnet --assume-yes
```

**Fund your account via web faucet (required — testnet faucet needs Google login):**

1. Get your account address: `aptos config show-profiles`
2. Go to: `https://aptos.dev/network/faucet?address=<your_address>`
3. Login and request testnet APT
4. Return here and confirm you've funded the account

```bash
# Verify balance
aptos account balance --profile default

# Deploy to testnet as object (modern pattern)
aptos move deploy-object \
    --address-name my_addr \
    --profile default \
    --assume-yes

# IMPORTANT: Save the object address from output
# You'll need it for upgrades and function calls
# Output: "Code was successfully deployed to object address 0x..."
```

### Step 5: Test on Testnet

```bash
# Run entry functions to verify deployment
aptos move run \
    --profile default \
    --function-id <deployed_address>::<module>::<function> \
    --args ...

# Test multiple scenarios
# - Happy paths
# - Error cases (should abort with correct error codes)
# - Access control
# - Edge cases

# Verify using explorer
# https://explorer.aptoslabs.com/?network=testnet
```

### Step 6: Deploy to Mainnet (After Testnet Success)

**Only deploy to mainnet after thorough testnet testing.**

Check if a profile exists before initializing:

```bash
# Check if default profile exists
aptos config show-profiles

# If no profile exists, initialize one
# IMPORTANT: Warn user that this generates a private key — store it securely
aptos init --network mainnet --assume-yes
```

**Fund your account:** Transfer real APT to your account address from an exchange or wallet.

```bash
# Verify balance
aptos account balance --profile default

# Deploy to mainnet as object (modern pattern)
aptos move deploy-object \
    --address-name my_addr \
    --profile default \
    --max-gas 20000  # Optional: set gas limit

# Review prompts carefully before confirming:
# 1. Gas confirmation: Review gas costs
# 2. Object address: Note the object address for future reference

# OR use --assume-yes to auto-confirm (only if you're confident)
aptos move deploy-object \
    --address-name my_addr \
    --profile default \
    --assume-yes

# SAVE THE OBJECT ADDRESS from output
# You'll need it for upgrades and documentation

# Confirm deployment
# Review transaction in explorer:
# https://explorer.aptoslabs.com/?network=mainnet
```

### Step 7: Verify Deployment

```bash
# Check module is published
aptos account list --account <deployed_address> --profile default

# Look for your module in the output
# "0x...::my_module": { ... }

# Run view function to verify
aptos move view \
    --profile default \
    --function-id <deployed_address>::<module>::<view_function> \
    --args ...
```

### Step 8: Document Deployment

Create deployment record:

```markdown
# Deployment Record

**Date:** 2026-01-23 **Network:** Mainnet **Module:** my_module **Address:** 0x123abc... **Transaction:** 0x456def...

## Verification

- [x] Deployed successfully
- [x] Module visible in explorer
- [x] View functions working
- [x] Entry functions tested

## Links

- Explorer: https://explorer.aptoslabs.com/account/0x123abc...?network=mainnet
- Transaction: https://explorer.aptoslabs.com/txn/0x456def...?network=mainnet

## Notes

- All security checks passed
- 100% test coverage verified
- Tested on testnet for 1 week before mainnet
```

## Module Upgrades

### Upgrading Existing Object Deployment

**Object-deployed modules are upgradeable by default for the deployer.**

```bash
# Upgrade existing object deployment
aptos move upgrade-object \
    --address-name my_addr \
    --object-address <object_address_from_initial_deploy> \
    --profile mainnet

# Upgrade with auto-confirm
aptos move upgrade-object \
    --address-name my_addr \
    --object-address <object_address> \
    --profile mainnet \
    --assume-yes

# Verify upgrade
aptos account list --account <object_address> --profile mainnet
```

**IMPORTANT:** Save the object address from your initial `deploy-object` output - you need it for upgrades.

**Upgrade Compatibility Rules:**

- ✅ **CAN:** Add new functions
- ✅ **CAN:** Add new structs
- ✅ **CAN:** Add new fields to structs (with care)
- ❌ **CANNOT:** Remove existing functions (breaks compatibility)
- ❌ **CANNOT:** Change function signatures (breaks compatibility)
- ❌ **CANNOT:** Remove struct fields (breaks existing data)

### Making Modules Immutable

**To prevent future upgrades:**

```move
// In your module
fun init_module(account: &signer) {
    // After deployment, burn upgrade capability
    // (implementation depends on your setup)
}
```

## Cost Estimation

### Gas Costs

```bash
# Typical deployment costs:
# - Small module: ~500-1000 gas units
# - Medium module: ~1000-5000 gas units
# - Large module: ~5000-20000 gas units

# When you run deploy-object, the CLI shows gas estimate before confirming
# Use --assume-yes only after you've verified costs on testnet first
```

### Mainnet Costs

**Gas costs are paid in APT:**

- Gas units × Gas price = Total cost
- Example: 5000 gas units × 100 Octas/gas = 500,000 Octas = 0.005 APT

## Multi-Module Deployment

### Deploying Multiple Modules

**Option 1: Single package (Recommended)**

```
project/
├── Move.toml
└── sources/
    ├── module1.move
    ├── module2.move
    └── module3.move
```

```bash
# Deploys all modules at once as a single object
aptos move deploy-object --address-name my_addr --profile testnet
```

**Option 2: Separate packages with dependencies**

```bash
# Deploy dependency package first
cd dependency-package
aptos move deploy-object --address-name dep_addr --profile testnet
# Note the object address from output

# Update main package Move.toml to reference dependency address
# Then deploy main package
cd ../main-package
aptos move deploy-object --address-name main_addr --profile testnet
```

## Troubleshooting Deployment

### "Insufficient APT balance"

**Devnet:** Auto-funded on `aptos init`. If needed, run:

```bash
aptos account fund-with-faucet --account default --amount 100000000 --profile default
```

**Testnet:** Use the web faucet (requires Google login):

1. Get your account address: `aptos config show-profiles`
2. Go to: `https://aptos.dev/network/faucet?address=<your_address>`
3. Login and request testnet APT
4. Verify balance: `aptos account balance --profile default`

**Mainnet:** Transfer real APT to your account from an exchange or wallet.

### "Module already exists" (for object deployments)

```bash
# Use upgrade-object with the original object address
aptos move upgrade-object \
    --address-name my_addr \
    --object-address <object_address_from_initial_deploy> \
    --profile testnet
```

### "Compilation failed"

```bash
# Fix compilation errors first
aptos move compile
# Fix all errors shown, then retry deployment
```

### "Gas limit exceeded"

```bash
# Increase max gas
aptos move deploy-object \
    --address-name my_addr \
    --profile testnet \
    --max-gas 50000
```

## Deployment Checklist

**Before Deployment:**

- [ ] Security audit passed
- [ ] 100% test coverage
- [ ] All tests passing
- [ ] Code compiles successfully
- [ ] Named addresses configured
- [ ] Target network selected (testnet first!)

**During Deployment:**

- [ ] Correct network selected
- [ ] Correct address specified
- [ ] Transaction submitted
- [ ] Transaction hash recorded

**After Deployment:**

- [ ] Module visible in explorer
- [ ] View functions work
- [ ] Entry functions tested
- [ ] Deployment documented
- [ ] Team notified

## CLI Argument Types

When calling entry or view functions via the CLI, use these type prefixes:

### Primitive Types

```bash
--args u64:1000           # u8, u16, u32, u64, u128, u256
--args bool:true          # boolean
--args address:0x1        # address
```

### Complex Types

```bash
--args string:"Hello World"                    # UTF-8 string
--args hex:0x48656c6c6f                        # raw bytes
--args "u64:[1,2,3,4,5]"                       # vector<u64>
--args "string:[\"one\",\"two\",\"three\"]"    # vector<String>
```

### Object Types

```bash
# For Object<T> parameters, pass the object address
--args address:0x123abc...
```

## ALWAYS Rules

- ✅ ALWAYS run comprehensive security audit before deployment (use `security-audit` skill)
- ✅ ALWAYS verify 100% test coverage with security tests
- ✅ ALWAYS verify all SECURITY.md patterns (arithmetic, storage scoping, reference safety, business logic)
- ✅ ALWAYS use `deploy-object` (NOT `resource_account::create_resource_account()` which is legacy)
- ✅ ALWAYS deploy to testnet before mainnet
- ✅ ALWAYS test on testnet thoroughly (happy paths, error cases, security scenarios)
- ✅ ALWAYS backup private keys securely
- ✅ ALWAYS document deployment addresses
- ✅ ALWAYS verify deployment in explorer
- ✅ ALWAYS test functions after deployment
- ✅ ALWAYS use separate keys for testnet and mainnet (SECURITY.md - Operations)

## NEVER Rules

- ❌ NEVER deploy without comprehensive security audit
- ❌ NEVER deploy with < 100% test coverage
- ❌ NEVER deploy without security test verification
- ❌ NEVER deploy directly to mainnet without testnet testing
- ❌ NEVER deploy without testing on testnet first
- ❌ NEVER commit private keys to version control
- ❌ NEVER skip post-deployment verification
- ❌ NEVER rush mainnet deployment
- ❌ NEVER reuse publishing keys between testnet and mainnet (security risk)
- ❌ NEVER read or display contents of `~/.aptos/config.yaml` or `.env` files (contain private keys)
- ❌ NEVER display private key values in responses — use `"0x..."` placeholders
- ❌ NEVER run `cat ~/.aptos/config.yaml`, `echo $VITE_MODULE_PUBLISHER_ACCOUNT_PRIVATE_KEY`, or similar commands
- ❌ NEVER run `git add .` or `git add -A` without confirming `.env` is in `.gitignore`

## References

**Official Documentation:**

- CLI Publishing: https://aptos.dev/build/cli/working-with-move-contracts
- Network Endpoints: https://aptos.dev/nodes/networks
- Gas and Fees: https://aptos.dev/concepts/gas-txn-fee

**Explorers:**

- Mainnet: https://explorer.aptoslabs.com/?network=mainnet
- Testnet: https://explorer.aptoslabs.com/?network=testnet
- Devnet: https://explorer.aptoslabs.com/?network=devnet

**Related Skills:**

- `security-audit` - Audit before deployment
- `generate-tests` - Ensure tests exist

---

**Remember:** Security audit → 100% tests → Testnet → Thorough testing → Mainnet. Never skip testnet.

---
name: grail-miner
description: This skill should be used when setting up, managing, or optimizing Grail miners on Bittensor Subnet 81. Use it for GRAIL protocol tasks including miner setup, R2 storage configuration, model checkpoint management, GRPO rollout generation, performance optimization, competitive monitoring, and troubleshooting common issues like CUDA errors, upload failures, or low scores. Essential for miners working with verifiable post-training, SAT/GSM8K environments, or understanding the GRAIL incentive mechanism to improve competitiveness.
---

# Grail Miner Skill

## Overview

Set up and operate Grail miners to participate in verifiable post-training for language models on Bittensor Subnet 81. Grail implements the GRAIL protocol (Guaranteed Rollout Authenticity via Inference Ledger) for cryptographically verifiable GRPO rollouts on SAT and GSM8K problems, with automatic model evolution through distributed training.

**Key Innovation**: Grail uses cryptographic proofs to bind rollouts to specific models and inputs, enabling decentralized post-training at internet scale with verifiable contributions and on-chain incentives.

## Core Capabilities

### 1. MINER SETUP WORKFLOW

**Prerequisites Check** before starting:
- **OS-agnostic**: Any platform (Linux/macOS/Windows) with floating point precision within tolerance
- Python 3.11+ with `uv` package manager
- Accelerators recommended (NVIDIA GPU for best throughput, but not required)
- Bittensor wallet registered to subnet 81 (mainnet) or 429 (testnet)
- Cloudflare R2 bucket (name must match account ID, region ENAM)
- Dual R2 credentials: read-only (public, committed on-chain) + write (private, local only)
- Optional: WandB account for monitoring

**Quick Start (6-Phase Setup)**:

1. **Clone and Install**
   ```bash
   git clone https://github.com/one-covenant/grail
   cd grail
   uv venv && source .venv/bin/activate
   uv sync  # Reproducible install with lockfile
   ```

2. **Generate Environment Configuration**
   ```bash
   ./scripts/setup_miner_env.sh
   ```
   - Interactive wizard for .env generation
   - Collects network, wallet, R2 credentials
   - Validates bucket configuration
   - Creates production-ready .env file

3. **Verify Setup**
   ```bash
   python scripts/check_miner_health.py
   ```
   - Comprehensive health checks
   - Validates R2 connectivity (read/write)
   - Tests wallet registration
   - Checks GPU availability
   - Verifies drand beacon access

4. **First Run (Test Mode)**
   ```bash
   grail -vv mine  # Verbose mode for debugging
   ```
   - Commits read credentials on-chain (first run only)
   - Downloads latest model checkpoint from R2
   - Starts generating rollouts for current window

5. **Monitor Performance**
   - View logs in terminal for immediate feedback
   - Check W&B dashboard: https://wandb.ai/tplr/grail (if enabled)
   - Monitor Grafana: https://grail-grafana.tplr.ai/

6. **Production Deployment** (Systemd)
   ```bash
   sudo tee /etc/systemd/system/grail-miner.service > /dev/null << 'EOF'
   [Unit]
   Description=Grail Miner
   After=network-online.target

   [Service]
   Type=simple
   User=miner
   WorkingDirectory=/home/miner/grail
   Environment="PATH=/home/miner/grail/.venv/bin:/usr/bin:/bin"
   ExecStart=/home/miner/grail/.venv/bin/grail mine
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   EOF

   sudo systemctl daemon-reload
   sudo systemctl enable grail-miner
   sudo systemctl start grail-miner
   sudo journalctl -u grail-miner -f
   ```

### 2. R2 STORAGE CONFIGURATION (CRITICAL FOR SUCCESS)

**The #1 Issue**: Miners struggling with R2 bucket setup and dual-credential configuration.

**Dual-Credential Architecture**:
```
WRITE CREDENTIALS (Private)      READ CREDENTIALS (Public)
     ↓                                 ↓
Local .env only              Committed on-chain
Used for uploads             Allows validator fetches
Full read/write              Read-only access
```

**Step-by-Step R2 Setup**:

1. **Create Cloudflare R2 Bucket**
   - Go to https://dash.cloudflare.com → R2
   - Click "Create Bucket"
   - **CRITICAL**: Bucket name MUST equal your Account ID
   - Set region to **ENAM** (required)
   - Get Account ID: Dashboard → Overview → Copy "Account ID"

2. **Generate Write Credentials** (Private)
   - Go to R2 → "Manage R2 API Tokens"
   - Click "Create API Token"
   - Name: "grail-write-access"
   - Permissions: **Edit** (full read/write)
   - Scope: Select your bucket
   - Copy both Access Key ID and Secret Access Key

3. **Generate Read Credentials** (Public)
   - Create another API Token
   - Name: "grail-read-only"
   - Permissions: **Read** (read-only)
   - Scope: Same bucket
   - Copy both keys

4. **Configure .env**:
   ```bash
   # Account & Bucket
   R2_ACCOUNT_ID=abc123def456  # Your Cloudflare account ID
   R2_BUCKET_ID=abc123def456   # MUST match account ID

   # Write credentials (private, never shared)
   R2_WRITE_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
   R2_WRITE_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

   # Read credentials (public, posted on-chain)
   R2_READ_ACCESS_KEY_ID=AKIAXXXXXXXXXXXXXXXX
   R2_READ_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```

5. **Verify Connectivity**
   ```bash
   python scripts/check_miner_health.py
   # Should show: ✅ R2 write access verified
   #              ✅ R2 read access verified
   ```

**How Validators Access Miner Data**:
1. Miner commits read credentials to chain on first run
2. Validators fetch read credentials from metagraph
3. Validators download miner's window files from R2
4. Validators verify GRAIL proofs and score rollouts
5. Validators set weights based on successful rollouts

**Common R2 Issues** → See [Troubleshooting](#6-troubleshooting-common-issues) section

### 3. MODEL CHECKPOINT MANAGEMENT

**How Model Evolution Works**:

Grail uses a hybrid approach where models start from a base and evolve through training:

1. **Base Model**: `Qwen/Qwen2.5-7B-Instruct` (initial checkpoint)
2. **Window Checkpoints**: Trainer uploads new checkpoint after each window
3. **Automatic Loading**: Miners download latest checkpoint at window start
4. **R2 Storage**: Checkpoints stored in R2 with retention policy
5. **Milestone Checkpoints**: Every 100 windows preserved permanently

**Miner Checkpoint Workflow** (grail/cli/mine.py:156-165):

```python
# At start of each window
window_start = (current_block // WINDOW_LENGTH) * WINDOW_LENGTH
previous_window = window_start - WINDOW_LENGTH

# Download checkpoint from previous window
checkpoint_path = download_checkpoint(previous_window)
model = load_model(checkpoint_path)

# Generate rollouts with this checkpoint
# Upload rollouts to R2
```

**Checkpoint Naming Convention**:
```
checkpoints/
├── window-71950/           # Recent checkpoint
│   ├── model.safetensors
│   ├── config.json
│   └── tokenizer/
├── window-71900/           # Previous window
└── milestone-71800/        # Milestone (every 100)
```

**Configuration (.env)**:
```bash
# Checkpoint retention (default: 10)
GRAIL_CHECKPOINT_RETENTION_LIMIT=10

# Milestone interval (default: 100 windows)
GRAIL_CHECKPOINT_MILESTONE_INTERVAL=100

# Local cache directory
GRAIL_CACHE_DIR=~/.cache/grail
```

**Manual Checkpoint Operations**:

```bash
# List available checkpoints
aws s3 ls s3://${R2_BUCKET_ID}/checkpoints/ \
  --endpoint-url https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com

# Download specific checkpoint
python -c "
from grail.infrastructure.comms import download_checkpoint
path = download_checkpoint(window=71950)
print(f'Downloaded to: {path}')
"

# Clear local cache
rm -rf ~/.cache/grail/checkpoints/*
```

**Key Files**:
- Checkpoint download: `grail/infrastructure/comms.py:download_checkpoint()`
- Model loading: `grail/cli/mine.py:156-165`
- Trainer upload: `grail/cli/train.py:upload_checkpoint()`

### 4. GRPO ROLLOUT GENERATION & OPTIMIZATION

**What is GRPO?**

Group Relative Policy Optimization - a reinforcement learning algorithm that:
- Generates multiple rollouts per problem (16 rollouts fixed)
- Computes advantages relative to group mean
- Optimizes policy using advantage-weighted gradients
- Maintains KL divergence from reference model

**Rollout Generation Pipeline** (grail/environments/loop.py:47-222):

```python
# For each SAT/GSM8K problem:
1. Derive deterministic seed: sha256(block_hash + drand + nonce)
2. Generate problem instance from seed
3. Create GRPO batch (16 rollouts per problem)
4. Generate completions with logprob tracking
5. Parse solutions and compute rewards
6. Calculate advantages (reward - group_mean)
7. Create GRAIL proof (PRF-based commitment)
8. Sign rollout with hotkey
9. Package for upload
```

**Reward Components** (grail/environments/reward_components.py):

```
Total Reward = 0.7*correctness + 0.15*thinking + 0.1*answer + 0.05*no_trailing

- correctness (0.7): SAT solution validity or GSM8K answer correctness
- thinking (0.15): Presence of <start_working_out> tags
- answer (0.1): Presence of <SOLUTION> tags
- no_trailing (0.05): Penalty for text after </SOLUTION>
```

**Performance Optimization**:

**Batch Size Tuning** (.env):
```bash
# Number of rollouts to generate in parallel (default: 1)
# Must divide evenly into 16 (valid: 1, 2, 4, 8, 16)
# Higher values = more throughput but more VRAM

GRAIL_GENERATION_BATCH_SIZE=1   # Baseline (lowest memory)
GRAIL_GENERATION_BATCH_SIZE=4   # ~3-4x throughput (recommended for A100)
GRAIL_GENERATION_BATCH_SIZE=16  # ~10x throughput (H100/H200 144GB)
```

**Generation Parameters** (hardcoded in constants):
- Max new tokens: 1024
- Rollouts per problem: 16
- Temperature: 1.0 (for diversity)
- Top-p: 0.95

**Monitor Generation Performance**:
```bash
# Watch real-time metrics
grail -vv mine

# Key metrics to watch:
# - Generation time per batch
# - Upload time per window
# - Rollout success rate
# - GPU memory usage (nvidia-smi)
```

**Key Files**:
- Rollout generator: `grail/mining/rollout_generator.py`
- Environment loop: `grail/environments/loop.py`
- SAT environment: `grail/environments/sat_env.py`
- GSM8K environment: `grail/environments/gsm8k_env.py`

### 5. COMPETITIVE MONITORING & SCORING

**Understanding the Incentive Mechanism**:

Validators score miners based on **unique successful rollouts** over recent windows using a superlinear curve:

```python
# Scoring formula (grail/scoring/scorer.py)
for each miner:
    valid_rollouts = count_verified_rollouts(miner, window)
    unique_solutions = count_unique_correct_solutions(miner, window)

    # Superlinear reward curve
    raw_score = (unique_solutions ** 1.5) * valid_rollouts

    # Normalize across all miners
    weight = raw_score / sum(all_raw_scores)
```

**What Matters for High Scores**:

1. **Rollout Validity** (GRAIL verification)
   - Correct token-level proofs
   - Valid signatures
   - Proper commitment/opening

2. **Solution Correctness** (SAT/GSM8K)
   - SAT: Assignments must satisfy all clauses
   - GSM8K: Final answer must match ground truth

3. **Solution Diversity**
   - Unique solutions earn more than duplicates
   - Explore different solution paths

4. **Volume**
   - More valid rollouts = higher weight
   - Maximize throughput within window

**Monitoring Your Competitiveness**:

**WandB Dashboard** (https://wandb.ai/tplr/grail):
```bash
# Enable in .env
GRAIL_MONITORING_BACKEND=wandb
WANDB_API_KEY=your_key
WANDB_PROJECT=grail
WANDB_ENTITY=tplr  # Public project

# Metrics tracked:
# - rollout_count: Total rollouts generated
# - upload_success_rate: Upload reliability
# - generation_time_avg: Throughput metric
# - reward_mean: Average reward per rollout
```

**Grafana Dashboard** (https://grail-grafana.tplr.ai/):
- Real-time logs from all miners
- Network-wide statistics
- Validator performance

**On-Chain Weights** (btcli):
```bash
# Check your current weight
btcli subnet metagraph --netuid 81 --subtensor.network finney | grep $(cat ~/.bittensor/wallets/default/hotkeys/miner/ss58_address.txt)

# Compare to top miners
btcli subnet metagraph --netuid 81 --subtensor.network finney | sort -k4 -rn | head -20
```

**Performance Analysis**:

```python
# Analyze your rollouts locally
from grail.scoring.scorer import compute_miner_scores

# Load your window data
window_data = load_window_rollouts(window_start)

# Compute metrics
valid_count = sum(1 for r in window_data if r['valid'])
success_count = sum(1 for r in window_data if r['success'])
unique_solutions = len(set(r['solution'] for r in window_data if r['success']))

print(f"Valid: {valid_count}/total")
print(f"Successful: {success_count}/{valid_count}")
print(f"Unique solutions: {unique_solutions}")
```

**Improvement Strategies**:

1. **Increase Throughput**
   - Tune `GRAIL_GENERATION_BATCH_SIZE`
   - Upgrade GPU (H100/H200 for 10x gains)
   - Optimize upload timing

2. **Improve Success Rate**
   - Monitor reward components
   - Check model checkpoint version
   - Verify problem difficulty range

3. **Maximize Diversity**
   - Use higher temperature if allowed
   - Generate across different problem seeds
   - Explore varied reasoning paths

**Key Files**:
- Scoring logic: `grail/scoring/scorer.py`
- Window aggregation: `grail/cli/validate.py:compute_window_scores()`
- Metrics tracking: `grail/shared/logging.py`

### 6. TROUBLESHOOTING COMMON ISSUES

**CUDA / GPU Errors**

**Symptom**: `CUDA out of memory` or GPU not detected
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Solutions**:
1. Reduce batch size:
   ```bash
   export GRAIL_GENERATION_BATCH_SIZE=1
   ```

2. Clear GPU cache periodically (miner does this automatically):
   ```python
   import torch
   torch.cuda.empty_cache()
   ```

3. Check GPU availability:
   ```bash
   nvidia-smi
   python -c "import torch; print(torch.cuda.is_available())"
   ```

4. Verify CUDA compatibility:
   ```bash
   nvidia-smi | grep "CUDA Version"
   # Should be >= 12.0 for best performance
   ```

**Note**: Grail is **OS and hardware-agnostic** - GPU is recommended for throughput but not required.

---

**R2 Upload Failures**

**Symptom**: Upload errors or "No uploads" warnings
```
ERROR: Failed to upload window rollouts to R2
ERROR: Credentials invalid or bucket not found
```

**Solutions**:
1. Verify credentials:
   ```bash
   python scripts/check_miner_health.py
   # Should show ✅ for both read and write access
   ```

2. Check bucket configuration:
   ```bash
   # Bucket name MUST equal account ID
   echo "Account: $R2_ACCOUNT_ID"
   echo "Bucket: $R2_BUCKET_ID"
   # These should match!
   ```

3. Test manual upload:
   ```bash
   aws s3 ls s3://${R2_BUCKET_ID}/ \
     --endpoint-url https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com \
     --profile grail-write
   ```

4. Verify region is ENAM:
   - Go to Cloudflare dashboard → R2 → Click bucket
   - Region should show "Eastern North America (ENAM)"

---

**Low Scores / No Weights**

**Symptom**: Not receiving weights from validators
```
INFO: Window complete, 0 successful rollouts
WARNING: No weights received for 3+ windows
```

**Diagnostic Steps**:

1. **Check rollout validity**:
   ```bash
   # Enable verbose logging
   grail -vv mine

   # Look for:
   # ✅ GRAIL proof valid
   # ✅ Signature verified
   # ✅ Solution correct
   ```

2. **Verify uploads succeeded**:
   ```bash
   # List your window files on R2
   aws s3 ls s3://${R2_BUCKET_ID}/windows/ \
     --endpoint-url https://${R2_ACCOUNT_ID}.r2.cloudflarestorage.com

   # Should see: {hotkey}-window-{block}.json
   ```

3. **Check read credentials on-chain**:
   ```bash
   # Validators need your read credentials
   btcli subnet metagraph --netuid 81 | grep $(cat ~/.bittensor/wallets/default/hotkeys/miner/ss58_address.txt)

   # Should show your endpoint and committed credentials
   ```

4. **Monitor validator logs** (Grafana):
   - Visit https://grail-grafana.tplr.ai/
   - Search for your hotkey
   - Check for verification errors

5. **Compare to checkpoint version**:
   ```bash
   # Ensure you're using latest checkpoint
   ls -lh ~/.cache/grail/checkpoints/
   # Should show recent window number
   ```

**Common Causes**:
- Read credentials not committed (first run required)
- Bucket name ≠ account ID
- Wrong region (must be ENAM)
- Model checkpoint too old
- GRAIL proof failures
- Low throughput (not generating enough rollouts)

---

**Drand Beacon Failures**

**Symptom**: Cannot fetch randomness beacon
```
WARNING: Drand fetch failed, falling back to block hash
ERROR: All drand endpoints unreachable
```

**Solutions**:
1. Miner automatically falls back to block-hash only (safe)

2. Test drand connectivity:
   ```bash
   python -c "
   from grail.infrastructure.drand import get_drand_beacon
   beacon = get_drand_beacon()
   print(f'Beacon: {beacon}')
   "
   ```

3. Use explicit fallback mode:
   ```bash
   grail mine --no-drand
   ```

4. Check firewall rules (drand uses HTTPS):
   ```bash
   curl -I https://api.drand.sh/public/latest
   ```

**Note**: Block-hash fallback is safe and deterministic - validators use same seed derivation.

---

**Wallet / Registration Issues**

**Symptom**: Wallet not found or not registered
```
ERROR: Wallet 'default/miner' not found
ERROR: Hotkey not registered on subnet 81
```

**Solutions**:
1. Verify wallet exists:
   ```bash
   ls ~/.bittensor/wallets/
   # Should show your coldkey name

   ls ~/.bittensor/wallets/default/hotkeys/
   # Should show your hotkey name
   ```

2. Check registration:
   ```bash
   btcli wallet overview --wallet.name default --wallet.hotkey miner
   # Should show registration on subnet 81
   ```

3. Register if needed:
   ```bash
   btcli subnet register \
     --wallet.name default \
     --wallet.hotkey miner \
     --netuid 81 \
     --subtensor.network finney
   ```

4. Verify .env matches wallet names:
   ```bash
   grep WALLET .env
   # BT_WALLET_COLD=default
   # BT_WALLET_HOT=miner
   ```

## Protocol Deep Dive

**GRAIL Cryptographic Proof** (grail/protocol/):

```
1. Challenge Derivation:
   seed = sha256(drand_randomness || block_hash || window_context)

2. PRF-Based Commitment:
   For each token t:
     - Generate random vector r_t = PRF(seed, position)
     - Compute sketch commitment: s_t = dot(token_vec, r_t) mod PRIME_Q

3. Verifier Challenge:
   - Validator samples K=16 random positions
   - Requests token IDs and proofs at those positions

4. Verification:
   - Recompute r_t from seed and position
   - Check: s_t == dot(token_vec, r_t) mod PRIME_Q
   - Verify signatures bind to hotkey
```

**SAT Problem Determinism** (grail/environments/sat_env.py):

```python
# Deterministic generation from seed
def generate_sat_problem(seed: int, difficulty: int):
    rng = random.Random(seed)  # Deterministic RNG
    n_vars = 3 + difficulty  # 3-10 variables
    n_clauses = 5 + difficulty * 2  # 5-20 clauses

    clauses = []
    for _ in range(n_clauses):
        clause = rng.sample(range(1, n_vars+1), k=3)
        clause = [v if rng.random() > 0.5 else -v for v in clause]
        clauses.append(clause)

    return clauses
```

**Reward Calculation** (grail/environments/reward_components.py:64-116):

```python
# Multi-component reward vector
def compute_reward(completion: str, problem: Problem):
    parsed = parse_completion(completion)

    # Component rewards
    r_correctness = check_solution(parsed.solution, problem)  # 0.7 weight
    r_thinking = 0.5 if has_thinking_tags(parsed) else 0.0   # 0.15 weight
    r_answer = 0.3 if has_solution_tags(parsed) else 0.0     # 0.1 weight
    r_concise = max(0, 0.2 - 0.001*trailing_chars(parsed))   # 0.05 weight

    total = (0.7*r_correctness + 0.15*r_thinking +
             0.1*r_answer + 0.05*r_concise)
    return total  # Range: [0.0, 1.0]
```

## Key Configuration Reference

**Critical Environment Variables** (.env):

```bash
# Network
BT_NETWORK=finney              # mainnet (or 'test' for testnet)
NETUID=81                      # Grail subnet

# Wallet
BT_WALLET_COLD=default         # Your coldkey name
BT_WALLET_HOT=miner            # Your hotkey name

# R2 Storage (CRITICAL: bucket name = account ID, region = ENAM)
R2_ACCOUNT_ID=abc123           # Cloudflare account ID
R2_BUCKET_ID=abc123            # MUST match account ID
R2_WRITE_ACCESS_KEY_ID=...     # Private write credentials
R2_WRITE_SECRET_ACCESS_KEY=...
R2_READ_ACCESS_KEY_ID=...      # Public read credentials (on-chain)
R2_READ_SECRET_ACCESS_KEY=...

# Performance
GRAIL_GENERATION_BATCH_SIZE=4  # Parallel rollouts (1/2/4/8/16)

# Monitoring (Optional)
GRAIL_MONITORING_BACKEND=wandb
WANDB_API_KEY=...
WANDB_PROJECT=grail
WANDB_ENTITY=tplr              # Public project
```

**Constants** (grail/shared/constants.py):

```python
WINDOW_LENGTH = 50              # Blocks per scoring window
BLOCK_TIME_SECONDS = 12         # Target block time
ROLLOUTS_PER_PROBLEM = 16       # Fixed rollouts per problem
CHALLENGE_K = 16                # Positions verified per rollout
PRIME_Q = 2_147_483_647        # Modulus for sketch commitments
```

## Resources

### scripts/
- `setup_miner_env.sh` - Interactive .env generation wizard
- `check_miner_health.py` - Comprehensive health check script

### references/
- `grail_protocol.md` - Deep dive into GRAIL cryptographic protocol
- `incentive_mechanism.md` - Detailed scoring and weight computation
- `environments.md` - SAT and GSM8K environment specifications
- `performance_tuning.md` - Advanced optimization strategies

## External Resources

- **Covenant AI**: https://www.covenant.ai (Grail's parent company)
- **Discord Community**: https://discord.gg/GyzhzRWJBQ (support and discussions)
- **GitHub Repository**: https://github.com/one-covenant/grail
- **Miner Docs**: https://github.com/one-covenant/grail/blob/main/docs/miner.md
- **Validator Docs**: https://github.com/one-covenant/grail/blob/main/docs/validator.md
- **W&B Dashboard**: https://wandb.ai/tplr/grail (public metrics)
- **Grafana Logs**: https://grail-grafana.tplr.ai/ (real-time monitoring)

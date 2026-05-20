---
name: run-jmh-benchmarks-hetzner
description: "Provision a Hetzner CCX33 server, deploy the project, run JMH benchmarks, collect results, and destroy the server. Use ONLY when the user explicitly asks to run JMH benchmarks on a Hetzner server. Do NOT trigger for general benchmark requests or local benchmark runs."
user-invocable: true
---

# Run JMH Benchmarks on Hetzner

Provision a dedicated Hetzner cloud server, deploy the current working tree, run JMH benchmarks from any module, download results, and tear down the server.

## Prerequisites

- `hcloud` CLI installed and authenticated (`hcloud version` to verify)
- SSH key pair at `~/.ssh/id_ed25519` (or `~/.ssh/id_rsa`)
- The benchmark module compiles locally

## Workflow

### Step 0: Determine benchmark module and parameters

Ask the user (or infer from context) which benchmark module to run. The project may contain multiple JMH benchmark modules. Common examples:

- `jmh-ldbc` — LDBC SNB read query benchmarks (default if user says "run benchmarks")
- Other modules with JMH dependencies — check for `jmh-core` dependency in `pom.xml`

Determine:
- **Module name** (`-pl <module>`)
- **JMH regex filter** (which benchmarks to include/exclude)
- **JMH parameters** (forks, warmup, measurement iterations)

Defaults (good for comparison runs):
- `-f 1 -wi 3 -w 5s -i 5 -r 10s`

For **jmh-ldbc** specifically:
- Expected runtime: ~90 minutes for 40 benchmarks (20 queries x 2 suites) with `-f 1 -wi 3 -w 5s -i 5 -r 10s`

### Step 1: Provision the server

**Naming convention**: Use `jmh-bench-<branch>` for the server and `jmh-bench-key-<branch>` for the SSH key, where `<branch>` is the current git branch name (sanitized: lowercase, slashes replaced with dashes, truncated to keep total name under 63 chars). This avoids conflicts when multiple benchmark runs execute concurrently on different branches.

```bash
# Determine branch-based names
BRANCH=$(git rev-parse --abbrev-ref HEAD | tr '[:upper:]/' '[:lower:]-' | cut -c1-40)
SERVER_NAME="jmh-bench-${BRANCH}"
KEY_NAME="jmh-bench-key-${BRANCH}"

# Upload local SSH public key
hcloud ssh-key create --name "$KEY_NAME" --public-key-from-file ~/.ssh/id_ed25519.pub

# Create CCX33: 8 dedicated AMD vCPUs, 32 GB RAM, Falkenstein DC
hcloud server create --name "$SERVER_NAME" --type ccx33 --image ubuntu-24.04 --location fsn1 --ssh-key "$KEY_NAME"
```

Record the IPv4 address from the output. Wait ~15 seconds for the server to boot before attempting SSH.

If SSH fails with a host key conflict, remove the stale key:
```bash
ssh-keygen -f ~/.ssh/known_hosts -R <IP>
```

### Step 2: Install JDK 21

```bash
ssh -o StrictHostKeyChecking=no root@<IP> \
  'apt-get update -qq && apt-get install -y -qq openjdk-21-jdk-headless git tmux > /dev/null 2>&1 && java -version'
```

### Step 3: Deploy the project

Rsync the **worktree root** (the directory containing `mvnw`, `pom.xml`, `core/`, etc.), excluding `.git`, `target`, and `.idea`:

```bash
rsync -az --exclude='.git' --exclude='target' --exclude='.idea' <worktree-root>/ root@<IP>:/root/ytdb/
```

**Important**: The working directory (e.g. `/workspace/ytdb/ldbc-jmh`) may be a git worktree — it contains the full project tree with `mvnw` at its root. Rsync this directory, NOT the parent `/workspace/ytdb/`.

Then initialize a git repo on the server (required by Spotless):
```bash
ssh root@<IP> 'git config --global --add safe.directory /root/ytdb && \
  git config --global user.email "bench@test" && \
  git config --global user.name "bench" && \
  cd /root/ytdb && git init && git add -A && git commit -m "baseline" --quiet'
```

### Step 3b: Download dataset from Hetzner S3 (jmh-ldbc only — MANDATORY)

The LDBC dataset must be pre-downloaded before running benchmarks. The benchmark no longer auto-downloads from SURF (the SURF format is incompatible). Download it from Hetzner Object Storage (S3):

```bash
ssh root@<IP> 'apt-get install -y -qq python3-pip zstd > /dev/null 2>&1 && \
  pip install --break-system-packages boto3 -q && \
  mkdir -p /root/ytdb/<module>/target/ldbc-dataset/sf0.1 && \
  python3 -c "
import boto3, os
s3 = boto3.client(\"s3\",
    endpoint_url=os.environ[\"S3_ENDPOINT\"],
    aws_access_key_id=os.environ[\"S3_ACCESS_KEY\"],
    aws_secret_access_key=os.environ[\"S3_SECRET_KEY\"])
print(\"Downloading dataset from S3...\")
s3.download_file(\"bench-cache\", \"ldbc/ldbc-sf0.1-composite-merged-fk.tar.zst\", \"/tmp/dataset.tar.zst\")
print(\"Downloaded\")
" && \
  cd /root/ytdb/<module>/target/ldbc-dataset/sf0.1 && \
  zstd -d /tmp/dataset.tar.zst -o /tmp/dataset.tar && \
  tar xf /tmp/dataset.tar && \
  rm -f /tmp/dataset.tar.zst /tmp/dataset.tar && \
  echo "Dataset ready" && ls static/ dynamic/'
```

**Important**: The command above requires S3 credentials as environment variables on the remote server. Pass them via SSH:
```bash
ssh root@<IP> "export S3_ENDPOINT='<endpoint>' S3_ACCESS_KEY='<key>' S3_SECRET_KEY='<secret>' && ..."
```

Credentials are stored as GitHub secrets: `HETZNER_S3_ACCESS_KEY`, `HETZNER_S3_SECRET_KEY`, `HETZNER_S3_ENDPOINT`. Retrieve them from GitHub or ask the user.

Replace `<module>` with the benchmark module (e.g. `jmh-ldbc`).

The dataset uses LDBC datagen v1.0.0 CsvCompositeMergeForeign format (~19 MB). It is stored in Hetzner Object Storage bucket `bench-cache` at key `ldbc/ldbc-sf0.1-composite-merged-fk.tar.zst`.

**If S3 credentials are unavailable**, generate the dataset locally using the LDBC datagen Docker image, then rsync it to the server:
```bash
# On the local machine
docker run --rm \
    -v "$(pwd)/jmh-ldbc/target/ldbc-dataset/sf0.1:/out" \
    ldbc/datagen:latest \
    --scale-factor 0.1 --mode raw --format CsvCompositeMergeForeign

# Then rsync the dataset to the server
rsync -az jmh-ldbc/target/ldbc-dataset/ root@<IP>:/root/ytdb/jmh-ldbc/target/ldbc-dataset/
```

**Do not use** the SURF repository at `repository.surfsara.nl` — it provides CsvComposite format (v0.3.5), which is incompatible with the benchmark loaders.

### Step 4: Compile

```bash
ssh root@<IP> 'cd /root/ytdb && chmod +x mvnw && \
  ./mvnw -pl <module> -am compile -DskipTests -Dspotless.check.skip=true -q'
```

Replace `<module>` with the target benchmark module (e.g. `jmh-ldbc`).

Wait for BUILD SUCCESS (typically ~60-90 seconds on CCX33).

### Step 4b: Pre-load LDBC dataset (jmh-ldbc only)

**Critical for jmh-ldbc**: The LDBC dataset is downloaded and loaded into the database inside JMH's `@Setup(Level.Trial)` method. This means the first fork's warmup iteration includes dataset download + DB creation time. For multi-threaded benchmarks, threads start executing queries on a partially-loaded database, producing wildly inaccurate results (e.g., 300+ ops/s when the real throughput is ~3 ops/s).

**Always pre-load the dataset** before running actual benchmarks:

```bash
ssh root@<IP> 'cd /root/ytdb && ./mvnw -pl <module> -am verify -P bench -DskipTests -Dspotless.check.skip=true \
  -Djmh.args="ic5_newGroups -f 0 -wi 0 -i 1 -r 1s -t 1" 2>&1 | tail -20'
```

This runs a single in-process iteration (`-f 0`) that triggers dataset download and DB creation. Subsequent forked runs will find the existing DB at `./target/ldbc-bench-db` and skip loading.

**If the dataset was pre-downloaded via Step 3b**: The pre-load step is still required — it creates the YouTrackDB database from the CSV files. However, the download phase will be skipped automatically because the dataset files already exist in `target/ldbc-dataset/`.

**When comparing two code versions (A/B testing)**: After running version A, delete the benchmark database before running version B to avoid stale cached data:

```bash
ssh root@<IP> 'rm -rf /root/ytdb/jmh-ldbc/target/ldbc-bench-db'
```

The dataset files (`target/ldbc-dataset/`) can be kept — only the DB needs to be recreated.

### Step 5: Run benchmarks

**IMPORTANT**: Never run multiple benchmarks concurrently on the same server. Always wait for one benchmark run to complete before starting the next.

Start the benchmark in a tmux session so it survives SSH disconnects.

**If the module has a `bench` Maven profile** (like `jmh-ldbc`):
```bash
ssh root@<IP> 'tmux new-session -d -s bench \
  "cd /root/ytdb && ./mvnw -pl <module> -am verify -P bench -DskipTests -Dspotless.check.skip=true \
  -Djmh.args=\"<jmh-args> -rf json -rff /root/results.json\" \
  2>&1 | tee /root/bench.log"'
```

**If the module produces an uber-jar**:
```bash
ssh root@<IP> 'tmux new-session -d -s bench \
  "cd /root/ytdb && java -jar <module>/target/benchmarks.jar \
  <jmh-args> -rf json -rff /root/results.json \
  2>&1 | tee /root/bench.log"'
```

**JMH parameters explained:**
- `-f 1` — 1 fork (sufficient for comparison runs; use `-f 3` for publication-grade results)
- `-wi 3 -w 5s` — 3 warmup iterations, 5 seconds each
- `-i 5 -r 10s` — 5 measurement iterations, 10 seconds each
- `-e <pattern>` — exclude benchmarks matching regex
- `-rf json -rff /root/results.json` — save results as JSON

### Step 6: Monitor progress

Poll periodically (every 5-10 minutes):

```bash
# Count completed benchmarks
ssh root@<IP> 'grep "^Result" /root/bench.log 2>/dev/null | wc -l'

# Check current benchmark
ssh root@<IP> 'tail -5 /root/bench.log'

# Check if complete
ssh root@<IP> 'grep "^# Run complete\|BUILD" /root/bench.log'
```

### Step 7: Collect results

Once `# Run complete` appears in the log:

```bash
# Download JSON results
scp root@<IP>:/root/results.json /tmp/claude-code-results.json

# Show summary table
ssh root@<IP> 'grep "^Benchmark\|thrpt\|avgt" /root/bench.log | head -60'
```

Copy the JSON to the project directory with a descriptive name:
```bash
cp /tmp/claude-code-results.json <module>/<name>-results-ccx33.json
```

### Step 8: Destroy the server

Always clean up to avoid charges. Use the same branch-based names from Step 1:

```bash
hcloud server delete "$SERVER_NAME"
hcloud ssh-key delete "$KEY_NAME"
```

### Step 9: Compare results

If baseline data exists (e.g. in memory files or previous JSON), present a comparison table with:
- Benchmark name
- Baseline score
- New score
- Percentage change
- Assessment (regression / noise / improvement)

Changes within ~5-7% are typically measurement noise for multi-threaded benchmarks. Single-threaded benchmarks are more stable (~2-3% noise floor).

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `mvnw: No such file or directory` | You rsynced the wrong directory. Rsync the worktree root that contains `mvnw`. |
| SSH host key conflict | `ssh-keygen -f ~/.ssh/known_hosts -R <IP>` |
| `detected dubious ownership` | `git config --global --add safe.directory /root/ytdb` |
| JMH hangs or needs restart | `ssh root@<IP> 'rm -f /tmp/jmh.lock'` then re-run in tmux |
| Core test compilation fails | Add `-Dmaven.test.skip=true` to the compile command |
| Need real-time output | Use tmux + tee (already in the command above) |
| Wild/inconsistent ops/s in MT benchmarks | Dataset not pre-loaded. Run Step 4b first. The first fork loads the DB during warmup; MT threads see partially loaded data. |
| `apt-get` lock on fresh server | Wait 30s for `unattended-upgrades` to finish, then retry. |
| Dataset not found error during setup | Dataset must be pre-downloaded via Step 3b (Hetzner S3). The benchmark no longer auto-downloads from SURF. |

## Notes

- **Server type**: CCX33 provides 8 dedicated AMD EPYC vCPUs — dedicated (not shared) cores ensure consistent benchmark results. For heavier benchmarks, consider CCX43 (16 vCPUs) or CCX53 (32 vCPUs).
- **jmh-ldbc Threads.MAX**: The multi-threaded LDBC benchmark uses `@Threads(Threads.MAX)` — one thread per available processor. On CCX33 this means 8 threads.
- **jmh-ldbc dataset loading**: The LDBC dataset must be pre-downloaded via Step 3b (Hetzner S3) — the benchmark no longer auto-downloads from SURF. DB creation happens inside `LdbcBenchmarkState.@Setup(Level.Trial)` on first run. Always pre-load with `-f 0` before real benchmarks (see Step 4b). The DB path is `./target/ldbc-bench-db`; the dataset cache is `./target/ldbc-dataset/`.
- **Never run benchmarks concurrently**: Multiple JMH processes on the same server will contend for CPU and produce unreliable numbers. Always run one at a time.
- **Ubuntu apt lock on fresh servers**: Newly provisioned Ubuntu 24.04 servers run `unattended-upgrades` on first boot. If `apt-get install` fails with "Could not get lock", wait 30 seconds and retry.
- **Memory file**: For LDBC benchmarks, update `ldbc-jmh-benchmarks.md` in the auto-memory directory with new results after each run.
- **S3 dataset cache**: The LDBC dataset archive (`ldbc-sf0.1-composite-merged-fk.tar.zst`, ~19 MB, datagen v1.0.0 CsvCompositeMergeForeign format) is cached in Hetzner Object Storage bucket `bench-cache` at `ldbc/ldbc-sf0.1-composite-merged-fk.tar.zst`. Credentials are stored as GitHub secrets `HETZNER_S3_ACCESS_KEY` / `HETZNER_S3_SECRET_KEY` / `HETZNER_S3_ENDPOINT` — never hardcode them in code or commit them to the repository.
- **Dataset without S3 access**: If S3 credentials are unavailable, generate the dataset locally using the LDBC datagen Docker image: `docker run --rm -v "$(pwd)/jmh-ldbc/target/ldbc-dataset/sf0.1:/out" ldbc/datagen:latest --scale-factor 0.1 --mode raw --format CsvCompositeMergeForeign`. Then rsync the generated dataset to the server. See `jmh-ldbc/README.md` for details.
- **Do not use SURF**: The SURF Data Repository (`repository.surfsara.nl`) provides the CsvComposite format (v0.3.5), which is **incompatible** with the benchmark loaders that expect CsvCompositeMergeForeign column layouts.

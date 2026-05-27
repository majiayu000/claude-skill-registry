---
name: canton-network-repos
description: Canton Network, DAML, and Splice repository knowledge. Use when working with Canton participants, DAML smart contracts, Splice applications, LF version compatibility, or package ID mismatches. Triggers on Canton, DAML, Splice, decentralized-canton-sync, or LF version queries.
---

# Canton Network Open-Source Repositories

This skill provides comprehensive knowledge about the Canton Network open-source ecosystem, repository relationships, and build processes.

## Activation

Use this skill when:
- Working with Canton Network, DAML, or Splice repositories
- Investigating version compatibility issues
- Understanding enterprise vs community differences
- Debugging LF version or package ID mismatches
- Building Canton participants or Splice applications

## Repository Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    Splice Version (e.g., 0.5.4)                 │
│         github.com/digital-asset/decentralized-canton-sync     │
│   Applications: Validator, SV, Wallet, Scan, Amulet (CC)       │
└─────────────────────────┬───────────────────────────────────────┘
                          │ depends on
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   Canton Version (e.g., 3.4.9)                  │
│               github.com/digital-asset/canton                   │
│     Runtime: Participant, Sequencer, Mediator, Admin API       │
└─────────────────────────┬───────────────────────────────────────┘
                          │ depends on
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                    DAML SDK (e.g., 3.4.9)                       │
│                github.com/digital-asset/daml                    │
│    Compiler: damlc, LF Engine, Ledger API, stdlib, protobuf    │
└─────────────────────────────────────────────────────────────────┘
```

## Repository Details

### 1. DAML SDK (`github.com/digital-asset/daml`)

**Purpose**: Smart contract language, compiler, and runtime libraries.

**Key Directories**:
```
daml/
├── sdk/
│   ├── compiler/damlc/          # Haskell compiler source
│   │   └── lib/DA/Cli/Options.hs  # --target version validation
│   ├── daml-lf/
│   │   ├── language/            # LF version definitions (Scala)
│   │   ├── engine/              # LF execution engine
│   │   └── archive/             # DALF protobuf format
│   └── canton/                  # Canton runtime (submodule)
├── ledger-api/                  # gRPC API definitions
└── VERSION                      # SDK version string
```

**LF Version Definitions** (`LanguageVersion.scala` at v3.4.9):
```scala
// V2 versions defined
val List(v2_1, v2_2, v2_dev) = AllV2  // Line 51 - v2_2 IS defined

// Version ranges
case Major.V2 => VersionRange(v2_1, v2_2)  // Line 171 - StableVersions includes v2_2
def AllVersions = VersionRange(v2_1, v2_dev)

// Features at v2_2:
val flatArchive = v2_2
val kindInterning = flatArchive
val exprInterning = flatArchive
val explicitPkgImports = v2_2
val unsafeFromInterfaceRemoved = v2_2
```

**Note**: v2_2 IS in SDK v3.4.9 source. Older snapshots may not include it.

**damlc Target Validation** (`Options.hs`):
```haskell
lfVersionOpt :: Parser LF.Version
-- Validates against LF.supportedOutputVersions
-- Error: "Unknown Daml-LF version: X" if not in list
```

### 2. Canton (`github.com/digital-asset/canton`)

**Purpose**: Distributed ledger runtime implementing the Canton Protocol.

**Key Directories**:
```
canton/
├── community/                   # Open-source Canton
│   ├── app/                     # CantonCommunityApp entry point
│   ├── participant/             # Participant node implementation
│   ├── domain/                  # Embedded domain (sequencer/mediator)
│   └── common/src/main/daml/    # Built-in DAML packages
│       └── AdminWorkflows/      # Ping, party replication DARs
├── daml/                        # DAML SDK submodule
├── daml_dependencies.json       # LF library versions
├── VERSION                      # Canton version
└── version.sbt                  # SBT version config
```

**Built-in DARs** (embedded in JAR):
- `canton-builtin-admin-workflow-ping.dar`
- `canton-builtin-admin-workflow-party-replication-alpha.dar`
- `CantonExamples.dar`

**Enterprise vs Community**:
| Feature | Enterprise | Community |
|---------|------------|-----------|
| Main class | CantonEnterpriseApp | CantonCommunityApp |
| Transaction processing | Parallel | Sequential |
| Pruning | Available | Limited |
| Database | PostgreSQL, Oracle | PostgreSQL only |
| HA Domain | Supported | Embedded only |

### 3. Splice (`github.com/digital-asset/decentralized-canton-sync`)

**Purpose**: Decentralized synchronizer governance, Amulet (Canton Coin), and network applications.

**Key Directories**:
```
decentralized-canton-sync/
├── project/
│   ├── CantonDependencies.scala  # Version config, LF versions
│   └── DamlPlugin.scala          # DAR build logic
├── daml/
│   ├── splice-amulet/            # Canton Coin token contracts
│   ├── splice-wallet/            # Wallet contracts
│   ├── splice-dso-governance/    # DSO governance
│   └── */daml.yaml               # Package configs with --target
├── apps/
│   ├── sv/                       # Super Validator app
│   ├── validator/                # Validator app
│   ├── wallet/                   # Wallet backend
│   └── scan/                     # Payment scan service
├── cluster/images/               # Docker image builds
│   └── canton-community/         # Community participant image
└── daml-compiler-sources.json    # Compiler version reference
```

**Critical Configuration** (`CantonDependencies.scala`):
```scala
object CantonDependencies {
  val version: String = "3.4.9"
  val daml_language_versions = Seq("2.1")  // ← LF target version
  val daml_libraries_version = version
  val daml_compiler_version = sys.env("DAML_COMPILER_VERSION")
}
```

**Package Target** (`daml/splice-amulet/daml.yaml`):
```yaml
sdk-version: 3.3.0-snapshot.20250502.13767.0.v2fc6c7e2
build-options:
  - --target=2.1  # Explicit LF 2.1 target
```

## Version Mapping

| Splice | Canton | DAML SDK | Protocol | LF (Default) | LF (With SDK 3.4.9) |
|--------|--------|----------|----------|--------------|---------------------|
| 0.5.4  | 3.4.9  | 3.4.9    | PV34     | 2.1*         | 2.2 (verified)      |
| 0.5.3  | 3.4.8  | 3.4.8    | PV34     | 2.1*         | 2.2                 |
| 0.4.x  | 3.3.x  | 3.3.x    | PV33     | 2.1          | 2.1                 |

*Open-source Splice 0.5.4 ships with SDK snapshot `3.3.0-snapshot.20250502` which predates LF 2.2.

**Root Cause (Verified)**: The public Splice release uses an SDK snapshot from **May 2, 2025**, but LF 2.2 was added to the SDK on **October 3, 2025**. Updating to SDK 3.4.9 enables LF 2.2 builds.

**Key insight**: LF 2.2 is fully available in open-source SDK v3.4.9. The Splice project simply needs to be updated to use the newer SDK.

## LF Version Implications

### Package ID Derivation
Package IDs are cryptographic hashes derived from:
1. Package source content
2. **LF version used** (`--target`)
3. SDK/stdlib versions
4. Dependency package IDs

**Changing LF version = Different package IDs = Incompatible packages**

### Upgrade Validation
Canton validates package upgrades:
- Upgraded packages must use equal or newer LF version
- LF 2.1 package cannot "upgrade" to LF 2.2 package (different IDs)
- Mixing LF versions on same ledger causes validation failures

## Building from Open-Source

### Community Canton Participant
```bash
cd canton
sbt "community/app/assembly"
# Output: community/app/target/scala-2.13/canton-community.jar
```

### Splice Applications
```bash
cd decentralized-canton-sync
sbt compile  # Requires DAML_COMPILER_VERSION env var
```

### Building with LF 2.2 (Verified Working)

LF 2.2 is available in SDK v3.4.9. The following steps have been **verified to work**:

1. Edit `project/CantonDependencies.scala`:
   ```scala
   val daml_language_versions = Seq("2.2")
   ```

2. Update `nix/daml-compiler-sources.json`:
   ```json
   { "version": "3.4.9" }
   ```

3. Update all `daml/*/daml.yaml` files:
   ```yaml
   sdk-version: 3.4.9
   build-options:
     - --target=2.2
   ```

4. Remove invalid warning flags (not present in SDK 3.4.9):
   ```bash
   # Remove -Wno-ledger-time-is-alpha from all daml.yaml files
   ```

5. Build packages:
   ```bash
   cd decentralized-canton-sync
   nix-shell -p daml-sdk --run "daml build -p daml/splice-util"
   nix-shell -p daml-sdk --run "daml build -p daml/splice-amulet"
   ```

**Verified**: splice-util and splice-amulet build successfully with LF 2.2 and SDK 3.4.9.

## Fully Open-Source LF 2.2 Build (Verified)

Both Splice and Canton can be built with LF 2.2 from entirely open-source code:

### Canton Built-in DARs

Update Canton's daml.yaml files:
```bash
cd canton/community
# Update all daml.yaml files to sdk-version: 3.4.9 and --target=2.2
perl -pi -e 's/sdk-version: 3\.3\.0-snapshot\.[^\n]*/sdk-version: 3.4.9/g' **/daml.yaml
perl -pi -e 's/--target=2\.1/--target=2.2/g' **/daml.yaml
```

Rebuild Canton:
```bash
sbt "canton-community-app/assembly"
```

### Verified Results (2025-12-24)

Community-built DARs have **identical package IDs** to enterprise:
- `canton-builtin-admin-workflow-ping-3.4.9-fbeb863dab36da66d99...`

This confirms full compatibility with enterprise deployments.

## Key Files Reference

| Purpose | Repository | File |
|---------|------------|------|
| LF versions (Scala) | daml | `sdk/daml-lf/language/.../LanguageVersion.scala` |
| damlc validation | daml | `sdk/compiler/damlc/lib/DA/Cli/Options.hs` |
| Canton version | canton | `VERSION` |
| Canton DARs | canton | `community/common/src/main/daml/` |
| Splice LF config | splice | `project/CantonDependencies.scala` |
| Package targets | splice | `daml/*/daml.yaml` |
| Docker builds | splice | `cluster/images/*/Dockerfile` |

## Troubleshooting

### "Unknown Daml-LF version: 2.2"
- **Cause**: damlc binary doesn't support 2.2 in `supportedOutputVersions`
- **Check**: `daml damlc --help` for supported targets
- **Fix**: Use SDK version that includes 2.2, or use 2.1

### Package ID Mismatch
- **Cause**: Different LF versions between builds
- **Check**: `unzip -p package.dar META-INF/MANIFEST.MF | grep Sdk-Version`
- **Fix**: Ensure consistent `--target` across all builds

### Upgrade Validation Failed
- **Cause**: Trying to swap enterprise (LF 2.2) with community (LF 2.1) packages
- **Fix**: Use DAR injection to maintain LF 2.2 compatibility

## External References

- [DAML SDK Releases](https://github.com/digital-asset/daml/releases)
- [Canton Releases](https://github.com/digital-asset/canton/releases)
- [Splice Documentation](https://docs.dev.sync.global/)
- [DAML-LF Governance](https://github.com/digital-asset/daml/blob/main/daml-lf/governance.rst)
- [Canton Network Docs](https://docs.digitalasset.com/)

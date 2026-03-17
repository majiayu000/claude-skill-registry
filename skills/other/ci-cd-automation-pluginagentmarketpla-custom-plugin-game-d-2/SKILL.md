---
name: ci-cd-automation
version: "2.0.0"
description: |
  Continuous integration and deployment pipelines, automated testing, build automation,
  and team workflows for game development.
sasmp_version: "1.3.0"
bonded_agent: 06-tools-pipeline
bond_type: PRIMARY_BOND

parameters:
  - name: platform
    type: string
    required: false
    validation:
      enum: [github_actions, gitlab_ci, jenkins, azure_devops]
  - name: engine
    type: string
    required: false
    validation:
      enum: [unity, unreal, godot, custom]

retry_policy:
  enabled: true
  max_attempts: 3
  backoff: exponential

observability:
  log_events: [start, complete, error, deploy]
  metrics: [build_time_seconds, success_rate, cache_hit_rate]
---

# CI/CD Automation

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE STAGES                     │
├─────────────────────────────────────────────────────────────┤
│  TRIGGER: [Push] [PR] [Tag] [Schedule] [Manual]             │
│                              ↓                               │
│  VALIDATE (< 5 min):                                         │
│  Lint → Compile Check → Asset Validation                    │
│                              ↓                               │
│  TEST (10-30 min):                                           │
│  Unit Tests → Integration → PlayMode Tests                  │
│                              ↓                               │
│  BUILD (Parallel):                                           │
│  [Windows] [Linux] [macOS] [WebGL] [Android] [iOS]         │
│                              ↓                               │
│  DEPLOY:                                                     │
│  [Dev auto] → [Staging gate] → [Prod approval]             │
└─────────────────────────────────────────────────────────────┘
```

## GitHub Actions for Unity

```yaml
# ✅ Production-Ready: Unity CI/CD Pipeline
name: Unity Build Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      buildType:
        description: 'Build type'
        required: true
        default: 'development'
        type: choice
        options:
          - development
          - release

env:
  UNITY_LICENSE: ${{ secrets.UNITY_LICENSE }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true

      - uses: actions/cache@v3
        with:
          path: Library
          key: Library-${{ hashFiles('Assets/**', 'Packages/**', 'ProjectSettings/**') }}
          restore-keys: Library-

      - uses: game-ci/unity-test-runner@v4
        with:
          testMode: all
          artifactsPath: test-results
          checkName: Test Results

      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: Test Results
          path: test-results

  build:
    needs: test
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        targetPlatform:
          - StandaloneWindows64
          - StandaloneLinux64
          - WebGL
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true

      - uses: actions/cache@v3
        with:
          path: Library
          key: Library-${{ matrix.targetPlatform }}-${{ hashFiles('Assets/**', 'Packages/**') }}

      - uses: game-ci/unity-builder@v4
        with:
          targetPlatform: ${{ matrix.targetPlatform }}
          versioning: Semantic
          buildMethod: BuildScript.PerformBuild

      - uses: actions/upload-artifact@v3
        with:
          name: Build-${{ matrix.targetPlatform }}
          path: build/${{ matrix.targetPlatform }}
          retention-days: 14

  deploy-staging:
    needs: build
    if: github.ref == 'refs/heads/develop'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v3
        with:
          name: Build-WebGL
          path: build/

      - name: Deploy to Staging
        run: |
          # Deploy to staging server
          aws s3 sync build/ s3://game-staging-bucket/
```

## Unreal Engine Pipeline

```yaml
# ✅ Production-Ready: Unreal CI/CD
name: Unreal Build Pipeline

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: [self-hosted, unreal]
    steps:
      - uses: actions/checkout@v4
        with:
          lfs: true

      - name: Build Development
        run: |
          & "$env:UE_ROOT/Engine/Build/BatchFiles/RunUAT.bat" `
            BuildCookRun `
            -project="${{ github.workspace }}/MyGame.uproject" `
            -platform=Win64 `
            -clientconfig=Development `
            -build -cook -stage -pak -archive `
            -archivedirectory="${{ github.workspace }}/Build"

      - uses: actions/upload-artifact@v3
        with:
          name: UnrealBuild-Win64
          path: Build/
```

## Build Optimization

```
BUILD TIME OPTIMIZATION:
┌─────────────────────────────────────────────────────────────┐
│  STRATEGY              │ TIME SAVINGS │ EFFORT            │
├────────────────────────┼──────────────┼───────────────────┤
│  Library caching       │ 30-50%       │ Low               │
│  Parallel builds       │ 40-60%       │ Low               │
│  Self-hosted runners   │ 20-40%       │ Medium            │
│  Incremental builds    │ 50-80%       │ Medium            │
│  Asset bundles split   │ 30-50%       │ High              │
└─────────────────────────────────────────────────────────────┘
```

## Automated Testing

```csharp
// ✅ Production-Ready: PlayMode Test
[TestFixture]
public class PlayerMovementTests
{
    private GameObject _player;
    private PlayerController _controller;

    [UnitySetUp]
    public IEnumerator SetUp()
    {
        var prefab = Resources.Load<GameObject>("Prefabs/Player");
        _player = Object.Instantiate(prefab);
        _controller = _player.GetComponent<PlayerController>();
        yield return null;
    }

    [UnityTest]
    public IEnumerator Player_MovesForward_WhenInputApplied()
    {
        var startPos = _player.transform.position;

        _controller.SetInput(Vector2.up);
        yield return new WaitForSeconds(0.5f);

        Assert.Greater(_player.transform.position.z, startPos.z);
    }

    [UnityTearDown]
    public IEnumerator TearDown()
    {
        Object.Destroy(_player);
        yield return null;
    }
}
```

## 🔧 Troubleshooting

```
┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Build times too long (>30 min)                     │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Enable Library folder caching                             │
│ → Use self-hosted runners with SSDs                         │
│ → Parallelize platform builds                               │
│ → Split large asset bundles                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Flaky tests causing failures                       │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Use test timeouts                                         │
│ → Isolate tests properly                                    │
│ → Add retry logic for network tests                         │
│ → Quarantine unstable tests                                 │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ PROBLEM: Cache not restoring correctly                      │
├─────────────────────────────────────────────────────────────┤
│ SOLUTIONS:                                                   │
│ → Check cache key hash inputs                               │
│ → Verify cache path is correct                              │
│ → Use restore-keys for partial matches                      │
│ → Check cache size limits                                   │
└─────────────────────────────────────────────────────────────┘
```

## Deployment Strategies

| Strategy | Rollback Time | Risk | Best For |
|----------|---------------|------|----------|
| Blue-Green | Instant | Low | Web builds |
| Canary | Minutes | Low | Mobile apps |
| Rolling | Minutes | Medium | Game servers |
| Big Bang | Hours | High | Console releases |

---

**Use this skill**: When setting up build pipelines, automating testing, or improving team workflows.

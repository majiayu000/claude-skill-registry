---
name: git-2-49-features
description: Git 2.49+ features including git-backfill, path-walk API, and performance improvements
---

# Git 2.49+ Features (2025)

## git-backfill Command (New in 2.49)

**What:** Efficiently download missing objects in partial clones using the path-walk API.

**Why:** Dramatically improves delta compression when fetching objects from partial clones, resulting in smaller downloads and better performance.

### Basic Usage

```bash
# Check if you have a partial clone
git config extensions.partialClone

# Download missing objects in background
git backfill

# Download with custom batch size
git backfill --batch-size=1000

# Respect sparse-checkout patterns (only fetch needed files)
git backfill --sparse

# Check progress
git backfill --verbose
```

### When to Use

**Scenario 1: After cloning with --filter=blob:none**
```bash
# Clone without blobs
git clone --filter=blob:none https://github.com/large/repo.git
cd repo

# Later, prefetch all missing objects efficiently
git backfill
```

**Scenario 2: Sparse-checkout + Partial clone**
```bash
# Clone with both optimizations
git clone --filter=blob:none --sparse https://github.com/monorepo.git
cd monorepo
git sparse-checkout set src/api

# Fetch only needed objects
git backfill --sparse
```

**Scenario 3: CI/CD Optimization**
```bash
# In CI pipeline - fetch only what's needed
git clone --filter=blob:none --depth=1 repo
git backfill --sparse
# Much faster than full clone
```

### Performance Comparison

**Traditional partial clone fetch:**
```bash
git fetch --unshallow
# Downloads 500MB in random order
# Poor delta compression
```

**With git-backfill:**
```bash
git backfill
# Downloads 150MB with optimized delta compression (70% reduction)
# Groups objects by path for better compression
```

## Path-Walk API (New in 2.49)

**What:** Internal API that groups together objects appearing at the same path, enabling much better delta compression.

**How it works:** Instead of processing objects in commit order, path-walk processes them by filesystem path, allowing Git to find better delta bases.

**Benefits:**
- 50-70% better compression in partial clone scenarios
- Faster object transfers
- Reduced network usage
- Optimized packfile generation

**You benefit automatically when using:**
- `git backfill`
- `git repack` (improved in 2.49)
- Server-side object transfers

### Enable Path-Walk Optimizations

```bash
# For repack operations
git config pack.useBitmaps true
git config pack.writeBitmaps true

# Repack with path-walk optimizations
git repack -a -d -f

# Check improvement
git count-objects -v
```

## Performance Improvements with zlib-ng

**What:** Git 2.49 includes improved performance through zlib-ng integration for compression/decompression.

**Benefits:**
- 20-30% faster compression
- 10-15% faster decompression
- Lower CPU usage during pack operations
- Transparent - no configuration needed

**Automatically improves:**
- `git clone`
- `git fetch`
- `git push`
- `git gc`
- `git repack`

## New Name-Hashing Algorithm

**What:** Improved algorithm for selecting object pairs during delta compression.

**Results:**
- More efficient packfiles
- Better compression ratios (5-10% improvement)
- Faster repack operations

**Automatic - no action needed.**

## Rust Bindings for libgit

**What:** Git 2.49 added Rust bindings (libgit-sys and libgit-rs) for Git's internal libraries.

**Relevance:** Future Git tooling and performance improvements will leverage Rust for memory safety and performance.

**For developers:** You can now build Git tools in Rust using official bindings.

## Promisor Remote Enhancements

**What:** Servers can now advertise promisor remote information to clients.

**Benefits:**
- Better handling of large files in partial clones
- Improved lazy fetching
- More efficient missing object retrieval

**Configuration:**
```bash
# View promisor remote info
git config remote.origin.promisor
git config extensions.partialClone

# Verify promisor packfiles
ls -lah .git/objects/pack/*.promisor
```

## Git 2.49 Workflow Examples

### Example 1: Ultra-Efficient Monorepo Clone

```bash
# Clone large monorepo with maximum efficiency
git clone --filter=blob:none --sparse https://github.com/company/monorepo.git
cd monorepo

# Only checkout your team's service
git sparse-checkout set --cone services/api

# Fetch needed objects with path-walk optimization
git backfill --sparse

# Result: 95% smaller than full clone, 70% faster download
```

### Example 2: CI/CD Pipeline Optimization

```yaml
# .github/workflows/ci.yml
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout with optimizations
        run: |
          git clone --filter=blob:none --depth=1 --sparse ${{ github.repositoryUrl }}
          cd repo
          git sparse-checkout set src tests
          git backfill --sparse

      - name: Run tests
        run: npm test
# 80% faster than full clone in CI
```

### Example 3: Working with Huge History

```bash
# Clone repository with massive history
git clone --filter=blob:none https://github.com/project/with-long-history.git
cd with-long-history

# Work on recent code only (objects fetched on demand)
git checkout -b feature/new-feature

# When you need full history
git backfill

# Repack for optimal storage
git repack -a -d -f  # Uses path-walk API
```

## Deprecated Features (Removal in Git 3.0)

**⚠️ Now Officially Deprecated:**
- `.git/branches/` directory (use remotes instead)
- `.git/remotes/` directory (use git remote commands)

**Migration:**
```bash
# If you have old-style remotes, convert them
# Check for deprecated directories
ls -la .git/branches .git/remotes 2>/dev/null

# Use modern remote configuration
git remote add origin https://github.com/user/repo.git
git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
```

## Meson Build System

**What:** Continued development on Meson as alternative build system for Git.

**Why:** Faster builds, better cross-platform support.

**Status:** Experimental - use `make` for production.

## netrc Support Re-enabled

**What:** HTTP transport now supports .netrc for authentication.

**Usage:**
```bash
# ~/.netrc
machine github.com
  login your-username
  password your-token

# Git will now use these credentials automatically
git clone https://github.com/private/repo.git
```

## Best Practices with Git 2.49

1. **Use git-backfill for partial clones:**
   ```bash
   git backfill --sparse  # Better than git fetch --unshallow
   ```

2. **Combine optimizations:**
   ```bash
   git clone --filter=blob:none --sparse <url>
   git sparse-checkout set --cone <paths>
   git backfill --sparse
   ```

3. **Regular maintenance:**
   ```bash
   git backfill  # Fill in missing objects
   git repack -a -d -f  # Optimize with path-walk
   git prune  # Clean up
   ```

4. **Monitor partial clone status:**
   ```bash
   # Check promisor remotes
   git config extensions.partialClone

   # List missing objects
   git rev-list --objects --all --missing=print | grep "^?"
   ```

5. **Migrate deprecated features:**
   ```bash
   # Move away from .git/branches and .git/remotes
   # Use git remote commands instead
   ```

## Troubleshooting

**git-backfill not found:**
```bash
# Verify Git version
git --version  # Must be 2.49+

# Update Git
brew upgrade git  # macOS
apt update && apt install git  # Ubuntu
```

**Promisor remote issues:**
```bash
# Reset promisor configuration
git config --unset extensions.partialClone
git config --unset remote.origin.promisor

# Re-enable
git config extensions.partialClone origin
git config remote.origin.promisor true
```

**Poor delta compression:**
```bash
# Force repack with path-walk optimization
git repack -a -d -f --depth=250 --window=250
```

## Resources

- [Git 2.49 Release Notes](https://github.blog/open-source/git/highlights-from-git-2-49/)
- [Path-Walk API Documentation](https://git-scm.com/docs/api-path-walk)
- [Partial Clone Documentation](https://git-scm.com/docs/partial-clone)

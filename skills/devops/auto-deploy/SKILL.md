---
name: auto-deploy
description: Automatically deploy oh-my-gemini to npm and GitHub
triggers:
  - "deploy"
  - "배포"
  - "publish"
  - "release"
  - "자동배포"
---

# Auto-Deploy Skill

Automatically deploy oh-my-gemini to npm and create a GitHub release.

## Purpose

Enable automated deployment workflow:
1. Version bump
2. Build and test
3. Publish to npm
4. Create GitHub release
5. Tag the release

## Workflow

### Phase 1: Pre-Deployment Checks

1. **Verify Build**
   ```
   npm run build
   ```

2. **Run Tests**
   ```
   npm test
   ```

3. **Check Lint**
   ```
   npm run lint
   ```

4. **Type Check**
   ```
   npx tsc --noEmit
   ```

5. **Verify Git Status**
   - Check for uncommitted changes
   - Check current branch (should be main)
   - Check if remote is up to date

### Phase 2: Version Management

1. **Determine Version**
   - If user specified: use that version
   - If patch: increment patch (0.1.0 → 0.1.1)
   - If minor: increment minor (0.1.0 → 0.2.0)
   - If major: increment major (0.1.0 → 1.0.0)

2. **Update package.json**
   ```
   npm version <version> --no-git-tag-version
   ```

3. **Update CHANGELOG.md**
   - Generate changelog from git commits
   - Add new version section

### Phase 3: Deployment

1. **Create Git Tag**
   ```
   git tag v<version>
   git push origin v<version>
   ```

2. **Push Changes**
   ```
   git add package.json package-lock.json CHANGELOG.md
   git commit -m "chore: release v<version>"
   git push origin main
   ```

3. **Trigger GitHub Actions**
   - GitHub Actions will automatically:
     - Build the project
     - Run tests
     - Publish to npm
     - Create GitHub release

### Phase 4: Verification

1. **Verify npm Publication**
   - Check npm registry for new version
   - Verify package contents

2. **Verify GitHub Release**
   - Check GitHub releases page
   - Verify release notes

## Usage

### Natural Language

```
> deploy: 버전 0.1.0으로 배포해줘
> 배포: 패치 버전으로 배포해줘
> publish: 마이너 버전으로 배포해줘
> release: 메이저 버전으로 배포해줘
```

### Command

```
/oh-my-gemini:auto-deploy
/oh-my-gemini:auto-deploy --version 0.1.0
/oh-my-gemini:auto-deploy --patch
/oh-my-gemini:auto-deploy --minor
/oh-my-gemini:auto-deploy --major
```

## Safety Measures

1. **Pre-Deployment Checks**
   - All tests must pass
   - Build must succeed
   - No uncommitted changes
   - Must be on main branch

2. **Dry Run Mode**
   - Use `--dry-run` to preview changes
   - Show what would be deployed
   - No actual changes made

3. **Confirmation**
   - Ask user for confirmation before deploying
   - Show version and changes summary
   - Wait for explicit approval

4. **Rollback Plan**
   - Keep previous version available
   - Document rollback procedure
   - Tag previous version as backup

## Configuration

Can be configured via `.gemini-cli/GEMINI.md`:

```markdown
## Auto-Deploy Settings

- Auto-confirm: false (always ask)
- Pre-deploy-tests: true
- Pre-deploy-lint: true
- Pre-deploy-build: true
- Create-changelog: true
```

## Integration with Self-Improve

Auto-deploy can be combined with self-improve:

```
> self-improve: 모든 버그를 수정하고 배포해줘
```

This will:
1. Detect and fix all issues
2. Run tests to verify fixes
3. Deploy if all checks pass


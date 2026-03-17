---
name: payload-plugin-release
description: Automates the release workflow for the Payload Newsletter Plugin. Use when releasing a new version, bumping the version, or publishing to npm.
---

<objective>
Execute the automated release workflow for the Payload Newsletter Plugin, ensuring proper versioning, changelog updates, and triggering GitHub Actions for npm publishing.
</objective>

<essential_principles>
- NEVER create git tags manually - GitHub Actions handles tag creation
- ALWAYS check the current date before updating changelog
- ALWAYS run typecheck before committing release changes
- Version bumps follow semantic versioning (major.minor.patch)
</essential_principles>

<intake>
What type of release?

1. **Patch** (bug fixes) - e.g., 0.25.11 → 0.25.12
2. **Minor** (new features, backward compatible) - e.g., 0.25.11 → 0.26.0
3. **Major** (breaking changes) - e.g., 0.25.11 → 1.0.0

Also provide: What changes are being released? (for changelog)
</intake>

<process>
<step name="verify">
Run typecheck to ensure no TypeScript errors:
```bash
bun typecheck
```
If errors exist, fix them before proceeding.
</step>

<step name="get-current-version">
Check current version:
```bash
grep '"version"' package.json | head -1
```
</step>

<step name="get-date">
Get current date for changelog:
```bash
date +"%Y-%m-%d"
```
</step>

<step name="bump-version">
Update version in package.json based on release type:
- Patch: increment last number (0.25.11 → 0.25.12)
- Minor: increment middle, reset last (0.25.11 → 0.26.0)
- Major: increment first, reset others (0.25.11 → 1.0.0)
</step>

<step name="update-changelog">
Add entry at TOP of CHANGELOG.md:

```markdown
## [NEW_VERSION] - YYYY-MM-DD

### Fixed/Added/Changed
- Description of changes
```

Categories to use:
- **Added** - new features
- **Changed** - changes in existing functionality
- **Fixed** - bug fixes
- **Removed** - removed features
- **Security** - security fixes
</step>

<step name="commit-and-push">
```bash
git add package.json CHANGELOG.md
git commit -m "chore: release vX.Y.Z"
git push origin main
```

GitHub Actions will automatically:
1. Detect the new version
2. Run tests and type checking
3. Build the project
4. Create the git tag
5. Publish to npm
6. Create a GitHub release
</step>

<step name="monitor">
Direct user to monitor the release:
https://github.com/aniketpanjwani/payload-plugin-email-newsletter/actions
</step>
</process>

<success_criteria>
- TypeScript passes with no errors
- Version bumped correctly in package.json
- CHANGELOG.md updated with correct date and version
- Changes committed and pushed to main
- User directed to GitHub Actions to monitor release
</success_criteria>

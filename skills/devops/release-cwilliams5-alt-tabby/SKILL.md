---
name: release
description: Build and publish a GitHub release
user-invocable: true
disable-model-invocation: true
---
Create a GitHub release for Alt-Tabby. The user may provide additional context (version bump amount, release note focus area, etc.) — incorporate it into the steps below.

## Steps

1. **Verify clean state**: `git status` must show a clean working tree. If not, stop and report.

2. **Run full test suite**: `.\tests\test.ps1 --live`. If any tests fail, stop and report. Do not release with failing tests.

3. **Determine version**: Read the current `VERSION` file. If the user specified a version bump (e.g., "+0.1", "bump minor"), apply it. Otherwise ask what the new version should be.

4. **Update VERSION file**: Write the new version string to `VERSION`.

5. **Compile**: Run `.\compile.bat`. Verify `release/AltTabby.exe` was produced.

6. **Build release notes**:
   - Run `git log --oneline vOLD..HEAD` (where vOLD is the previous version tag) to get the commit history since last release.
   - Write a summary of changes. If the user specified a focus area (e.g., "focus on latency improvements"), emphasize that in the notes.
   - Include a "Full Changelog" link: `https://github.com/cwilliams5/Alt-Tabby/compare/vOLD...vNEW`

7. **Commit version bump**: Commit the VERSION file change with message `Bump version to vX.Y.Z`.

8. **Create tag**: `git tag vX.Y.Z`

9. **Push**: `git push origin main --tags`

10. **Create GitHub release**:
    ```
    gh release create vX.Y.Z release/AltTabby.exe --title "vX.Y.Z" --notes "RELEASE_NOTES_HERE"
    ```
    - Asset MUST be named `AltTabby.exe` (auto-update depends on this exact name)
    - Upload `release/AltTabby.exe` directly — no zip, no config.ini, no blacklist.txt, no stats.ini

11. **Report**: Show the release URL and a summary of what was published.

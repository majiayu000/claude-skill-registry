---
name: write-app-change-log
description: Generates and updates the latest app changelog based on git history since the last version tag.
---

# Write App Change Log

This skill automates the process of creating a concise and meaningful changelog for the app.

## Workflow

1.  **Fetch Latest Tags**:
    *   Ensure all tags are fetched from the remote repository.
    *   Example: `git fetch --tags origin`

2.  **Identify the Base Tag**:
    *   Find the latest git tag that matches the pattern `v*`.
    *   Example: `git tag -l "v*" --sort=-v:refname | head -n 1`

3.  **Collect Commits**:
    *   Get all commits from the identified tag to the current `HEAD`.
    *   For each commit, collect the title and the full description.
    *   Example: `git log <base-tag>..HEAD --pretty=format:"%s%n%b%n---"`

4.  **Filter App-Related Commits**:
    *   Analyze the commit messages and files changed.
    *   **Exclude** commits that primarily affect:
        *   Repository infrastructure (e.g., `.github/`, `scripts/`, `fastlane/` except changelogs).
        *   CI/CD pipelines (e.g., workflow YAML files, Dockerfiles).
        *   Build tools configuration (unless it directly impacts app behavior).
        *   Internal documentation or maintenance (e.g., `README.md`, `AGENTS.md`, `task.md`, `implementation_plan.md`).
    *   **Include** commits that modify:
        *   App source code (`app/`, `database/`, `network/`).
        *   Resources (`strings.xml`, UI layouts).
        *   User-facing features or bug fixes.

5.  **Identify Meaningful Changes**:
    *   From the filtered list, select the **2-5 most significant** changes.
    *   Focus on what is most impactful for the end-user (new features, major bug fixes, performance improvements).

6.  **Match Style and Tone**:
    *   Read the existing changelogs in `fastlane/metadata/android/en-US/changelogs/`.
    *   Identify the highest numbered file (e.g., `9.txt`).
    *   Analyze the language, tone, and formatting of recent entries.
    *   Maintain the same concise and professional style.
    *   Usually, the format is: `Welcome to Janus <version-name> (<version-code>)` followed by bullet points if multiple changes are listed, or a single descriptive sentence.

7.  **Update the Latest Changelog**:
    *   Take the identified meaningful changes.
    *   Draft the new content matching the established style.
    *   **Update** the highest numbered file in `fastlane/metadata/android/en-US/changelogs/` with the new content.

## Guidelines
- Be concise.
- Focus on user value.
- Avoid technical jargon unless necessary.
- Ensure the version name and code in the changelog match the current project state (can be found in `app/build.gradle.kts` or similar).

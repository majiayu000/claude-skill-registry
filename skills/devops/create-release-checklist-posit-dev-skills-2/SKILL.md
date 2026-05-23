---
name: create-release-checklist
description: >
  Create a release checklist and GitHub issue for an R package. Use when the
  user asks to "create a release checklist" or "start a release" for an R package.
allowed-tools: Read, Bash, AskUserQuestion
---

# Create an R Package Release Checklist

Generate a release checklist for an R package and create the corresponding
GitHub issue.

## Overview

This skill guides you through creating a R package release checklist issue on
GitHub by:

- Determining the current version and prompting for release type.
- Generating an initial checklist.
- Prompting the user for additional customization.
- Creating a GitHub issue from the final checklist.

## Prerequisites

- The working directory must be an R package with a `DESCRIPTION` file at the
  root.
- The `usethis` R package must be available.

And to enable automatic issue creation:

- The `gh` CLI must be installed and authenticated.
- The R package must be associated with a GitHub repository.

## Workflow

### Step 1: Validation

First, check that the prerequisites are available (in this order for
efficiency):

1. Check that the working directory contains a file called `DESCRIPTION`. If
   not, inform the user that this must be run from an R package root directory
   and stop.
2. Use `Rscript -e 'utils::packageVersion("usethis")'` to check if the `usethis`
   package is installed. If not, instruct the user to install it with
   `install.packages("usethis")`, then stop.
3. Determine the GitHub URL for the repository, if one exists. First try
   `gh repo view --json url`. If that fails, diagnose the error:
   - If `gh` is not installed, try running `git remote -v` to find a GitHub URL.
   - If the local repo does not have a GitHub remote, suggest the user connect
     the package to GitHub using `usethis::use_github()`. Offer to run this
     command for the user; if they decline, continue without a GitHub URL.
   - If `gh` is installed but not authenticated and the repo has a GitHub
     remote, suggest that the user run `gh auth login`.

If any check fails, inform the user of the specific issue with clear
instructions on how to fix it, then stop the workflow. Do not proceed to the
next step until all prerequisites are met.

### Step 2: Initialization

Next, you need to determine the current package's name and version. Read the
`DESCRIPTION` file and extract the `Version:` and `Package:` fields from it.

Then, check if a `NEWS.md` file exists. If it does, read the first section
(typically the most recent unreleased changes) to understand what kind of
changes have been made. Use this to suggest an appropriate release type:

- If the NEWS mentions "breaking changes", "breaking", "BREAKING", or similar
  language, suggest a **Major** release.
- If the NEWS mentions only "bug fixes", "fixes", "patch", or similar language
  with no new features, suggest a **Patch** release.
- Otherwise (new features, improvements, enhancements), suggest a **Minor**
  release.

Display the current version to the user and ask them what type of release this
should be using the AskUserQuestion tool. Make the suggested release type the
first option with "(Recommended)" appended to the label:

Question: "What type of release is this?"
Header: "Release type"
Options (with recommended option first):
- Major (X.0.0) - Breaking changes (add "(Recommended)" if suggested)
- Minor (x.X.0) - New features but without breaking changes (add "(Recommended)" if suggested)
- Patch (x.x.X) - Bug fixes only (add "(Recommended)" if suggested)

Calculate the new version by manipulating the current version according to the
user's answer. For example:

- Current version `1.2.3` + Major release → `2.0.0`
- Current version `1.2.3` + Minor release → `1.3.0`
- Current version `1.2.3` + Patch release → `1.2.4`
- Current version `0.2.1.9000` + Patch release → `0.2.2`
- Current version `0.2.1.9003` + Minor release → `0.3.0`

Note: If the current version ends in `.9xxx` (R-style development versions),
strip that suffix before calculating the new version.

Display: "Preparing release checklist for ${PACKAGE_NAME} ${CURRENT_VERSION} →
${NEW_VERSION}".

### Step 3: Checklist Generation

Generate an initial checklist using the `scripts/generate_checklist.R` script
included with this skill:

```bash
# If the GitHub URL is known:
Rscript "${SKILL_DIR}/scripts/generate_checklist.R" "${NEW_VERSION}" "${GITHUB_URL}"

# Otherwise:
Rscript "${SKILL_DIR}/scripts/generate_checklist.R" "${NEW_VERSION}"
```

(Where `${SKILL_DIR}` represents the directory where this skill is installed.)

Ignore any "Setting active project..." lines in the output.

Read the generated checklist (which is Markdown) and display it to the user.

### Step 4: User Customization

Use the AskUserQuestion tool to ask:

Question: "Would you like to customize the checklist before creating the issue?"
Header: "Customize?"
Options:
- No, create the issue as-is
- Yes, let me customize it

If the user wants to customize the checklist, enter an iterative refinement loop:

1. Ask: "Suggest items that should be added or any items that can be safely
   removed, or confirm that there are no more changes requested."
2. Based on the user's feedback, update the checklist (add items, remove items,
   reword items, etc.). Keep the checklist in Markdown format with proper
   checkbox syntax (`- [ ]` for tasks).
3. Display the updated checklist to the user.
4. Ask: "Does this look good or do you have more suggestions?"
5. If the user has more suggestions, go back to step 2. If the user confirms it
   looks good, exit the loop and proceed to Step 5.

The checklist should be maintained as a Markdown string throughout this process
so it can be easily passed to the GitHub issue creation command.

### Step 5: GitHub Issue Creation

The final checklist should be formatted as Markdown with proper sections and
checkboxes.

**If `gh` is available and authenticated**, use it to create the GitHub issue
yourself, passing the checklist content directly via stdin:

```bash
gh issue create \
  --title "Release ${PACKAGE_NAME} ${NEW_VERSION}" \
  --body-file - <<'EOF'
[checklist content here]
EOF
```

Then show the user:

- A success message with the issue URL.
- The suggestion "You can now use the 'do-release-checklist' skill to walk
  through the checklist tasks." (Note: This is a companion skill that helps
  guide users through executing the checklist items. If this skill doesn't exist
  yet in your repository, you may omit this suggestion.)

**If `gh` is not available**, display the checklist to the user with
instructions to manually create a GitHub issue:

- Show the suggested issue title: "Release ${PACKAGE_NAME} ${NEW_VERSION}"
- Show the full checklist content formatted as Markdown.
- Instruct the user to copy the content and create the issue manually at their
  repository's issues page.

## Error Handling

If the GitHub issue creation fails (when using `gh`), check for common issues:

- **Authentication errors**: Ensure `gh auth status` shows the user is logged in.
  Suggest running `gh auth login` if needed.
- **Repository permissions**: The user must have write access to create issues.
  Check with `gh repo view` to verify they have the correct permissions.
- **Network errors**: If there are connectivity issues, suggest retrying the
  command or checking their internet connection.
- **Invalid Markdown**: If the issue body has formatting errors, verify the
  checklist Markdown is properly formatted with valid syntax.

If the issue creation fails, preserve the checklist content and offer to:

- Retry the command.
- Display the checklist for manual issue creation instead.

---
name: graphite-cli
description: This skill should be used to answer questions and guide workflows related to the Graphite CLI. It assists with creating, managing, submitting, and synchronizing stacked code changes (diffs).
license: Complete terms in LICENSE.txt
---

# Graphite CLI Guide

This skill provides procedural knowledge for working with the Graphite command-line interface (CLI). It covers the entire lifecycle of creating and managing stacked pull requests, from initial setup to advanced stack manipulation.

## When to Use This Skill

Activate this skill when a user's request involves using the `gt` command, managing stacked pull requests, or inquiring about the Graphite workflow. It is designed to handle tasks such as creating branches, submitting PRs, synchronizing with the trunk branch, and modifying the structure of a stack.

## Core Concepts

-   **Stack:** A series of small, incremental, and dependent branches. Each branch is a distinct PR, building on the previous one.
-   **Trunk:** The primary branch of the repository (usually `main` or `master`) from which all stacks originate and into which they are eventually merged.

---

## I. Initial Setup

To begin using Graphite in a git repository, it must be initialized.

1.  **Authenticate:** Run `gt auth` to connect the CLI to your GitHub account via an auth token.
2.  **Initialize Repository:** Navigate to the repository root and run `gt init`. This command will prompt to select the trunk branch.

---

## II. Core Workflow: Creating & Submitting Changes

This workflow covers the fundamental loop of creating, submitting, and updating branches.

### Step 1: Create a Branch

To create a new branch and commit changes, use `gt create`. This command replaces `git add`, `git commit`, and `git checkout -b`. The new branch will be stacked on the currently checked-out branch.

| Command | Alias/Flags | Description |
| :--- | :--- | :--- |
| `gt create` | `gt c` | Creates a new branch and commits staged changes. |
| `gt create -m <MSG>` | `gt c -m` | Creates a branch with a specific commit message. |
| `gt create -a` | `gt c -a` | Stages all unstaged changes before committing. |
| `gt create -am <MSG>` | `gt c -am` | Combines staging all changes and adding a message. |

**Example:**
To create a branch from `main` with all current file changes and a commit message:
1.  Checkout the trunk: `gt checkout main`
2.  Make code edits.
3.  Create the branch: `gt create -am "feat: Add new user model"`

### Step 2: Submit for Review

To push a branch (or a stack of branches) and open pull requests on GitHub, use `gt submit`.

| Command | Alias/Flags | Description |
| :--- | :--- | :--- |
| `gt submit` | | Pushes the current branch, creating or updating its PR. |
| `gt submit --stack` | `gt ss` | Pushes all branches in the current stack, from trunk up to the current branch, creating/updating a distinct PR for each. |
| `gt submit -d` | | Submits the PR as a draft. |
| `gt pr` | | Opens the GitHub PR page for the current branch in a browser. |

**Example:**
To submit an entire 3-part stack for review:
1. Navigate to the top branch of the stack (`part-3`).
2. Run `gt submit --stack --reviewers alice,bob`

### Step 3: Modify and Update

To update a branch with feedback, edit the code and use `gt modify` to amend the commit.

| Command | Alias/Flags | Description |
| :--- | :--- | :--- |
| `gt modify` | `gt m` | Amends the commit on the current branch with staged changes. |
| `gt modify -a` | `gt m -a` | Amends the commit with all staged and unstaged changes. **This is the most common update command.** |

**Example:**
To apply a requested change to a PR:
1. Edit the relevant files.
2. Run `gt modify -a` to amend the commit with your changes.
3. Run `gt submit` to update the remote PR.

---

## III. Stack Management & Navigation

### Visualizing the Stack

To see the dependency structure of your branches, use `gt log short`.

| Command | Alias | Description |
| :--- | :--- | :--- |
| `gt log short` | `gt ls` | Displays all tracked branches and their dependency relationships in a compact tree format. |

### Navigating the Stack

Use these commands to move efficiently between branches in a stack.

| Command | Alias | Function |
| :--- | :--- | :--- |
| `gt up` | `gt u` | Switches to the child branch (upstack). |
| `gt down` | `gt d` | Switches to the parent branch (downstack). |
| `gt top` | `gt t` | Switches to the highest branch (tip) of the current stack. |
| `gt bottom` | `gt b` | Switches to the lowest branch of the current stack. |
| `gt checkout` | `gt co` | Opens an interactive selector to choose any tracked branch. |

---

## IV. Synchronization & Conflict Resolution

### Keeping the Stack Up-to-Date

To update your stack with the latest changes from the trunk, use `gt sync`.

**Actions performed by `gt sync`:**
1.  Fetches the latest remote state.
2.  Pulls the latest changes into the trunk branch (`main`).
3.  **Restacks** (rebases) all of your open branches onto the updated trunk.
4.  Prompts to delete any local branches that have been merged or closed remotely.

### Resolving Conflicts

If `gt sync` or `gt modify` pauses due to a merge conflict, follow these steps:
1.  **Resolve Conflicts:** Open the files listed in the error message and resolve the conflicts manually.
2.  **Stage Changes:** Mark the conflicts as resolved by running `git add .`.
3.  **Continue:** Run `gt continue` to allow Graphite to complete the original `sync` or `modify` operation.

---

## V. Advanced Stack Manipulation

These commands are used to restructure a stack.

| Command | Description |
| :--- | :--- |
| `gt move` | Rebases the current branch and its children onto a new parent. Use this to change a branch's dependency (e.g., `gt move --onto main`). |
| `gt fold` | Combines (squashes) the current branch's changes into its parent branch and deletes the current branch. |
| `gt split` | Splits the current branch into two or more new branches, either by commit or by interactively selecting file hunks. |
| `gt create --insert` | Creates and inserts a new branch between the current branch and its parent. |
| `gt absorb` | Automatically applies unstaged changes to the most relevant downstack commits. Useful for distributing feedback fixes across multiple PRs at once. |

---

## Bundled Resources

-   **`references/graphite_cli_guide.md`**: The complete and unabridged guide for the Graphite CLI. Consult this file for detailed explanations of every command and workflow, including collaboration (`gt get`, `gt freeze`) and multi-trunk support.
---
name: git-essentials
description: Essential Git commands and workflows for version control, branching, and collaboration.
---

# Git Essentials

Essential Git commands for version control and collaboration.

## Initial Setup

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git init
git clone https://github.com/user/repo.git
```

## Basic Workflow

```bash
git status
git add file.txt
git add .
git commit -m "Commit message"
git commit -am "Message"
git commit --amend --no-edit
git diff
git diff --staged
```

## Branching & Merging

```bash
git branch
git branch -a
git checkout -b feature-name
git switch -c feature-name
git branch -d branch-name
git branch -D branch-name
git merge feature-name
git merge --no-ff feature-name
git merge --abort
```

## Remote Operations

```bash
git remote -v
git remote add origin https://github.com/user/repo.git
git fetch origin
git pull
git pull --rebase
git push
git push -u origin branch-name
git push --force-with-lease
```

## History & Logs

```bash
git log --oneline
git log --graph --oneline --all
git log --author="Name"
git log --since="2 weeks ago"
git log -S "function_name"
git blame file.txt
```

## Undoing Changes

```bash
git restore file.txt
git restore --staged file.txt
git reset --soft HEAD~1
git reset --hard HEAD~1
git revert commit-hash
```

## Stashing

```bash
git stash
git stash save "Work in progress"
git stash list
git stash pop
git stash apply stash@{2}
git stash drop stash@{0}
```

## Rebasing

```bash
git rebase main
git rebase -i HEAD~3
git rebase --continue
git rebase --abort
```

## Tags

```bash
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
git push --tags
git tag -d v1.0.0
```

## Useful Aliases (~/.gitconfig)

```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    last = log -1 HEAD
    visual = log --graph --oneline --all
    amend = commit --amend --no-edit
```

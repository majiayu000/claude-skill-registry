---
name: organizing-github
description: Conventions for GitHub repo locations, forks, and open source contribution boundaries.
user-invocable: false
---

# GitHub

All repos from GitHub are located in `~/code/github.com/[organization]/[repo]`, for example:

```
~/code/github.com/michaelhedgpeth/dotfiles
```

## Forks

All open source forks of projects are located in `~/code/github.com/mhedgpeth`. When the user asks for a fork of an open source project, fork that project and pull it into this folder.

## Investigation

If a dependency is on GitHub, pull the code into this system with the `gh` command. Look for any forks when doing so as well.

## Pull Requests

Never author a pull request for an open source project; the user should write those. Feel free to be helpful about summarization

---
name: raycast-alfred
version: 1.0.0
description: macOS launcher automation with Raycast extensions (TypeScript/React) and Alfred workflows (AppleScript/Python) for keyboard-driven productivity
author: workspace-hub
category: devtools
type: skill
capabilities:
  - raycast_extensions
  - alfred_workflows
  - script_commands
  - keyboard_shortcuts
  - clipboard_management
  - snippet_expansion
  - file_search
  - window_management
  - system_commands
  - application_integration
tools:
  - raycast
  - alfred
  - typescript
  - node
  - python
  - applescript
tags: [raycast, alfred, macos, launcher, automation, productivity, scripts, typescript, applescript]
platforms: [macos]
related_skills:
  - cli-productivity
  - vscode-extensions
  - git-advanced
---

# Raycast & Alfred Skill

Master macOS launcher automation with Raycast extensions and Alfred workflows. This skill covers TypeScript-based Raycast development, AppleScript/Python Alfred workflows, keyboard shortcuts, clipboard management, and productivity automation patterns.

## When to Use This Skill

### USE when:
- Building quick access tools for developer workflows
- Automating repetitive macOS tasks
- Creating custom search commands
- Building clipboard history managers
- Implementing text snippet expansion
- Creating project launchers and switchers
- Building API query tools
- Automating application control
- Creating custom keyboard shortcuts
- Building team productivity tools

### DON'T USE when:
- Cross-platform automation needed (use shell scripts)
- Server-side automation (use cron/systemd)
- GUI testing automation (use Playwright/Selenium)
- Windows/Linux environments
- Heavy computation tasks (use proper CLI tools)

## Prerequisites

### Raycast Setup

```bash
# Install Raycast
brew install --cask raycast

# Install Node.js (required for extension development)
brew install node

# Install Raycast CLI
npm install -g @raycast/api

# Create new extension
npx create-raycast-extension --name my-extension

# Development mode
cd my-extension
npm install
npm run dev

# Extension structure
# my-extension/
# ├── package.json
# ├── tsconfig.json
# ├── src/
# │   ├── index.tsx          # Main command
# │   └── other-command.tsx  # Additional commands
# └── assets/
#     └── icon.png           # Extension icon
```

### Alfred Setup

```bash
# Install Alfred (Powerpack required for workflows)
brew install --cask alfred

# Alfred workflow locations
# ~/Library/Application Support/Alfred/Alfred.alfredpreferences/workflows/

# Create workflow via Alfred Preferences > Workflows > + > Blank Workflow

# Workflow components:
# - Triggers: Keywords, hotkeys, file actions
# - Actions: Scripts, open URL, run NSAppleScript
# - Outputs: Notifications, copy to clipboard, play sound

# Script languages supported:
# - bash, zsh
# - Python (2 or 3)
# - AppleScript / JavaScript for Automation (JXA)
# - Ruby, PHP, Perl
```

### Development Environment

```bash
# For Raycast TypeScript development
npm install -g typescript @types/node

# For Alfred Python workflows
pip install alfred-workflow  # (legacy, but useful patterns)

# AppleScript tools
brew install --cask script-debugger  # Optional: AppleScript IDE

# Testing tools
brew install jq  # JSON parsing
```

## Core Capabilities

### 1. Raycast Script Commands

```bash
#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Open Project
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 📁
# @raycast.argument1 { "type": "text", "placeholder": "Project name", "optional": false }
# @raycast.packageName Developer Tools

# Documentation:
# @raycast.description Opens a project in VS Code
# @raycast.author Your Name
# @raycast.authorURL https://github.com/yourname

PROJECT="$1"
PROJECT_DIR="$HOME/projects/$PROJECT"

if [ -d "$PROJECT_DIR" ]; then
    code "$PROJECT_DIR"
    echo "Opened $PROJECT"
else
    echo "Project not found: $PROJECT"
    exit 1
fi
```

```bash
#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Git Status
# @raycast.mode fullOutput
# @raycast.icon 🔀
# @raycast.packageName Git

# @raycast.description Show git status for current directory
# @raycast.author workspace-hub

cd "$(pwd)" || exit 1

if [ -d ".git" ]; then
    echo "Branch: $(git branch --show-current)"
    echo ""
    echo "Status:"
    git status --short
    echo ""
    echo "Recent commits:"
    git log --oneline -5
else
    echo "Not a git repository"
    exit 1
fi
```

```python
#!/usr/bin/env python3

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title UUID Generator
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🔑
# @raycast.argument1 { "type": "dropdown", "placeholder": "Format", "data": [{"title": "Standard", "value": "standard"}, {"title": "No dashes", "value": "nodash"}, {"title": "Uppercase", "value": "upper"}] }
# @raycast.packageName Utilities

import uuid
import subprocess
import sys

format_type = sys.argv[1] if len(sys.argv) > 1 else "standard"

new_uuid = str(uuid.uuid4())

if format_type == "nodash":
    new_uuid = new_uuid.replace("-", "")
elif format_type == "upper":
    new_uuid = new_uuid.upper()

# Copy to clipboard
subprocess.run(["pbcopy"], input=new_uuid.encode(), check=True)

print(f"Copied: {new_uuid}")
```

```bash
#!/bin/bash

# @raycast.schemaVersion 1
# @raycast.title Kill Port
# @raycast.mode compact
# @raycast.icon 🔌
# @raycast.argument1 { "type": "text", "placeholder": "Port number" }
# @raycast.packageName Developer Tools

PORT="$1"

# Find process on port
PID=$(lsof -ti:$PORT 2>/dev/null)

if [ -z "$PID" ]; then
    echo "No process on port $PORT"
    exit 0
fi

# Kill the process
kill -9 $PID 2>/dev/null

if [ $? -eq 0 ]; then
    echo "Killed process $PID on port $PORT"
else
    echo "Failed to kill process on port $PORT"
    exit 1
fi
```

### 2. Raycast TypeScript Extensions

```tsx
// src/index.tsx
// ABOUTME: Raycast extension main command
// ABOUTME: Project launcher with favorites and recent

import {
  ActionPanel,
  Action,
  List,
  Icon,
  LocalStorage,
  showToast,
  Toast,
  getPreferenceValues,
} from "@raycast/api";
import { useState, useEffect } from "react";
import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs";
import path from "path";

const execAsync = promisify(exec);

interface Preferences {
  projectsDir: string;
  editor: string;
}

interface Project {
  name: string;
  path: string;
  lastOpened?: number;
  isFavorite?: boolean;
}

export default function Command() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const preferences = getPreferenceValues<Preferences>();

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    try {
      const projectsDir = preferences.projectsDir.replace("~", process.env.HOME || "");
      const dirs = fs.readdirSync(projectsDir, { withFileTypes: true });

      // Load favorites and recent from storage
      const favoritesJson = await LocalStorage.getItem<string>("favorites");
      const recentJson = await LocalStorage.getItem<string>("recent");

      const favorites = favoritesJson ? JSON.parse(favoritesJson) : [];
      const recent = recentJson ? JSON.parse(recentJson) : {};

      const projectList: Project[] = dirs
        .filter((dir) => dir.isDirectory() && !dir.name.startsWith("."))
        .map((dir) => ({
          name: dir.name,
          path: path.join(projectsDir, dir.name),
          lastOpened: recent[dir.name] || 0,
          isFavorite: favorites.includes(dir.name),
        }))
        .sort((a, b) => {
          // Favorites first, then by recent
          if (a.isFavorite && !b.isFavorite) return -1;
          if (!a.isFavorite && b.isFavorite) return 1;
          return (b.lastOpened || 0) - (a.lastOpened || 0);
        });

      setProjects(projectList);
    } catch (error) {
      showToast({
        style: Toast.Style.Failure,
        title: "Failed to load projects",
        message: String(error),
      });
    } finally {
      setIsLoading(false);
    }
  }

  async function openProject(project: Project) {
    try {
      const editor = preferences.editor || "code";
      await execAsync(`${editor} "${project.path}"`);

      // Update recent
      const recentJson = await LocalStorage.getItem<string>("recent");
      const recent = recentJson ? JSON.parse(recentJson) : {};
      recent[project.name] = Date.now();
      await LocalStorage.setItem("recent", JSON.stringify(recent));

      showToast({
        style: Toast.Style.Success,
        title: `Opened ${project.name}`,
      });
    } catch (error) {
      showToast({
        style: Toast.Style.Failure,
        title: "Failed to open project",
        message: String(error),
      });
    }
  }

  async function toggleFavorite(project: Project) {
    const favoritesJson = await LocalStorage.getItem<string>("favorites");
    const favorites = favoritesJson ? JSON.parse(favoritesJson) : [];

    if (project.isFavorite) {
      const index = favorites.indexOf(project.name);
      if (index > -1) favorites.splice(index, 1);
    } else {
      favorites.push(project.name);
    }

    await LocalStorage.setItem("favorites", JSON.stringify(favorites));
    await loadProjects();
  }

  return (
    <List isLoading={isLoading} searchBarPlaceholder="Search projects...">
      {projects.map((project) => (
        <List.Item
          key={project.path}
          title={project.name}
          subtitle={project.path}
          icon={project.isFavorite ? Icon.Star : Icon.Folder}
          accessories={[
            project.lastOpened
              ? { text: new Date(project.lastOpened).toLocaleDateString() }
              : {},
          ]}
          actions={
            <ActionPanel>
              <Action
                title="Open in Editor"
                icon={Icon.Code}
                onAction={() => openProject(project)}
              />
              <Action
                title="Open in Finder"
                icon={Icon.Finder}
                shortcut={{ modifiers: ["cmd"], key: "o" }}
                onAction={() => execAsync(`open "${project.path}"`)}
              />
              <Action
                title="Open in Terminal"
                icon={Icon.Terminal}
                shortcut={{ modifiers: ["cmd"], key: "t" }}
                onAction={() => execAsync(`open -a Terminal "${project.path}"`)}
              />
              <Action
                title={project.isFavorite ? "Remove from Favorites" : "Add to Favorites"}
                icon={project.isFavorite ? Icon.StarDisabled : Icon.Star}
                shortcut={{ modifiers: ["cmd"], key: "f" }}
                onAction={() => toggleFavorite(project)}
              />
              <Action.CopyToClipboard
                title="Copy Path"
                content={project.path}
                shortcut={{ modifiers: ["cmd", "shift"], key: "c" }}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

```tsx
// src/search-github.tsx
// ABOUTME: GitHub repository search command
// ABOUTME: Search and open repositories

import {
  ActionPanel,
  Action,
  List,
  Icon,
  showToast,
  Toast,
  getPreferenceValues,
} from "@raycast/api";
import { useState } from "react";
import fetch from "node-fetch";

interface Preferences {
  githubToken: string;
}

interface Repository {
  id: number;
  full_name: string;
  description: string | null;
  html_url: string;
  stargazers_count: number;
  language: string | null;
  updated_at: string;
}

export default function Command() {
  const [results, setResults] = useState<Repository[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const preferences = getPreferenceValues<Preferences>();

  async function searchRepositories(query: string) {
    if (!query || query.length < 2) {
      setResults([]);
      return;
    }

    setIsLoading(true);

    try {
      const response = await fetch(
        `https://api.github.com/search/repositories?q=${encodeURIComponent(query)}&sort=stars&per_page=20`,
        {
          headers: {
            Authorization: `token ${preferences.githubToken}`,
            Accept: "application/vnd.github.v3+json",
          },
        }
      );

      if (!response.ok) {
        throw new Error(`GitHub API error: ${response.status}`);
      }

      const data = (await response.json()) as { items: Repository[] };
      setResults(data.items || []);
    } catch (error) {
      showToast({
        style: Toast.Style.Failure,
        title: "Search failed",
        message: String(error),
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <List
      isLoading={isLoading}
      searchBarPlaceholder="Search GitHub repositories..."
      onSearchTextChange={searchRepositories}
      throttle
    >
      {results.map((repo) => (
        <List.Item
          key={repo.id}
          title={repo.full_name}
          subtitle={repo.description || ""}
          icon={Icon.Globe}
          accessories={[
            { icon: Icon.Star, text: String(repo.stargazers_count) },
            { text: repo.language || "" },
          ]}
          actions={
            <ActionPanel>
              <Action.OpenInBrowser url={repo.html_url} />
              <Action.CopyToClipboard
                title="Copy URL"
                content={repo.html_url}
              />
              <Action.CopyToClipboard
                title="Copy Clone URL"
                content={`git clone ${repo.html_url}.git`}
                shortcut={{ modifiers: ["cmd", "shift"], key: "c" }}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

```tsx
// src/clipboard-history.tsx
// ABOUTME: Custom clipboard history manager
// ABOUTME: Store and search clipboard items

import {
  ActionPanel,
  Action,
  List,
  Icon,
  Clipboard,
  LocalStorage,
  showToast,
  Toast,
} from "@raycast/api";
import { useState, useEffect } from "react";

interface ClipboardItem {
  id: string;
  content: string;
  timestamp: number;
  type: "text" | "url" | "code";
}

const MAX_ITEMS = 100;

export default function Command() {
  const [items, setItems] = useState<ClipboardItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  async function loadHistory() {
    try {
      const historyJson = await LocalStorage.getItem<string>("clipboard-history");
      const history = historyJson ? JSON.parse(historyJson) : [];
      setItems(history);
    } catch (error) {
      console.error("Failed to load history:", error);
    } finally {
      setIsLoading(false);
    }
  }

  async function pasteItem(item: ClipboardItem) {
    await Clipboard.paste(item.content);
    showToast({ style: Toast.Style.Success, title: "Pasted" });
  }

  async function deleteItem(item: ClipboardItem) {
    const newItems = items.filter((i) => i.id !== item.id);
    await LocalStorage.setItem("clipboard-history", JSON.stringify(newItems));
    setItems(newItems);
  }

  async function clearHistory() {
    await LocalStorage.setItem("clipboard-history", JSON.stringify([]));
    setItems([]);
    showToast({ style: Toast.Style.Success, title: "History cleared" });
  }

  function detectType(content: string): "text" | "url" | "code" {
    if (content.match(/^https?:\/\//)) return "url";
    if (content.includes("\n") && (content.includes("{") || content.includes("function")))
      return "code";
    return "text";
  }

  function getIcon(type: string) {
    switch (type) {
      case "url":
        return Icon.Link;
      case "code":
        return Icon.Code;
      default:
        return Icon.Text;
    }
  }

  function formatTimestamp(ts: number): string {
    const now = Date.now();
    const diff = now - ts;

    if (diff < 60000) return "Just now";
    if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
    if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
    return new Date(ts).toLocaleDateString();
  }

  return (
    <List isLoading={isLoading} searchBarPlaceholder="Search clipboard history...">
      {items.map((item) => (
        <List.Item
          key={item.id}
          title={item.content.slice(0, 100)}
          subtitle={item.content.length > 100 ? "..." : ""}
          icon={getIcon(item.type)}
          accessories={[{ text: formatTimestamp(item.timestamp) }]}
          actions={
            <ActionPanel>
              <Action
                title="Paste"
                icon={Icon.Clipboard}
                onAction={() => pasteItem(item)}
              />
              <Action.CopyToClipboard title="Copy" content={item.content} />
              <Action
                title="Delete"
                icon={Icon.Trash}
                style={Action.Style.Destructive}
                shortcut={{ modifiers: ["cmd"], key: "d" }}
                onAction={() => deleteItem(item)}
              />
              <Action
                title="Clear All"
                icon={Icon.Trash}
                style={Action.Style.Destructive}
                shortcut={{ modifiers: ["cmd", "shift"], key: "d" }}
                onAction={clearHistory}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

### 3. Alfred Workflows - AppleScript

```applescript
-- workflow-launcher.applescript
-- ABOUTME: Launch applications with Alfred
-- ABOUTME: AppleScript for application control

on alfred_script(q)
    set appName to q

    if appName is "" then
        return "No application specified"
    end if

    try
        tell application appName
            activate
        end tell
        return "Launched " & appName
    on error errMsg
        return "Error: " & errMsg
    end try
end alfred_script
```

```applescript
-- window-manager.applescript
-- ABOUTME: Window positioning and management
-- ABOUTME: Move and resize windows with Alfred

on alfred_script(q)
    -- Parse command: "left", "right", "top", "bottom", "maximize", "center"
    set position to q

    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
    end tell

    tell application "Finder"
        set screenBounds to bounds of window of desktop
        set screenWidth to item 3 of screenBounds
        set screenHeight to item 4 of screenBounds
    end tell

    -- Menu bar offset
    set menuBarHeight to 25

    tell application frontApp
        if position is "left" then
            set bounds of front window to {0, menuBarHeight, screenWidth / 2, screenHeight}
        else if position is "right" then
            set bounds of front window to {screenWidth / 2, menuBarHeight, screenWidth, screenHeight}
        else if position is "top" then
            set bounds of front window to {0, menuBarHeight, screenWidth, screenHeight / 2}
        else if position is "bottom" then
            set bounds of front window to {0, screenHeight / 2, screenWidth, screenHeight}
        else if position is "maximize" then
            set bounds of front window to {0, menuBarHeight, screenWidth, screenHeight}
        else if position is "center" then
            set winWidth to 1200
            set winHeight to 800
            set xPos to (screenWidth - winWidth) / 2
            set yPos to ((screenHeight - winHeight) / 2) + menuBarHeight
            set bounds of front window to {xPos, yPos, xPos + winWidth, yPos + winHeight}
        end if
    end tell

    return "Moved " & frontApp & " to " & position
end alfred_script
```

```applescript
-- clipboard-cleaner.applescript
-- ABOUTME: Clean and transform clipboard content
-- ABOUTME: Remove formatting, convert text

on alfred_script(q)
    -- Get clipboard content
    set clipContent to the clipboard

    if q is "plain" then
        -- Convert to plain text
        set the clipboard to clipContent as text
        return "Converted to plain text"

    else if q is "trim" then
        -- Trim whitespace
        set trimmed to do shell script "echo " & quoted form of clipContent & " | xargs"
        set the clipboard to trimmed
        return "Trimmed whitespace"

    else if q is "lower" then
        -- Convert to lowercase
        set lowered to do shell script "echo " & quoted form of clipContent & " | tr '[:upper:]' '[:lower:]'"
        set the clipboard to lowered
        return "Converted to lowercase"

    else if q is "upper" then
        -- Convert to uppercase
        set uppered to do shell script "echo " & quoted form of clipContent & " | tr '[:lower:]' '[:upper:]'"
        set the clipboard to uppered
        return "Converted to uppercase"

    else if q is "slug" then
        -- Convert to URL slug
        set slugged to do shell script "echo " & quoted form of clipContent & " | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-'"
        set the clipboard to slugged
        return "Converted to slug: " & slugged

    end if

    return "Unknown command: " & q
end alfred_script
```

### 4. Alfred Workflows - Python

```python
#!/usr/bin/env python3
# alfred-github-search.py
# ABOUTME: Search GitHub repositories from Alfred
# ABOUTME: Python script filter for Alfred

import sys
import json
import urllib.request
import urllib.parse
import os

def search_github(query):
    """Search GitHub repositories"""
    if not query or len(query) < 2:
        return []

    token = os.environ.get("GITHUB_TOKEN", "")
    url = f"https://api.github.com/search/repositories?q={urllib.parse.quote(query)}&sort=stars&per_page=10"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "Alfred-GitHub-Search",
    }

    if token:
        headers["Authorization"] = f"token {token}"

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            return data.get("items", [])
    except Exception as e:
        return []

def format_alfred_results(repos):
    """Format results for Alfred JSON output"""
    items = []

    for repo in repos:
        items.append({
            "uid": str(repo["id"]),
            "title": repo["full_name"],
            "subtitle": f"★ {repo['stargazers_count']} | {repo.get('description', 'No description')}",
            "arg": repo["html_url"],
            "icon": {
                "path": "icon.png"
            },
            "mods": {
                "cmd": {
                    "arg": f"git clone {repo['clone_url']}",
                    "subtitle": "Clone repository"
                },
                "alt": {
                    "arg": repo["clone_url"],
                    "subtitle": "Copy clone URL"
                }
            }
        })

    return {"items": items}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    repos = search_github(query)
    result = format_alfred_results(repos)
    print(json.dumps(result))
```

```python
#!/usr/bin/env python3
# alfred-jira-search.py
# ABOUTME: Search JIRA issues from Alfred
# ABOUTME: JQL-powered issue search

import sys
import json
import urllib.request
import urllib.parse
import base64
import os

JIRA_BASE_URL = os.environ.get("JIRA_URL", "https://your-company.atlassian.net")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")

def search_jira(query):
    """Search JIRA issues"""
    if not query:
        return []

    # Build JQL query
    jql = f'text ~ "{query}" ORDER BY updated DESC'
    url = f"{JIRA_BASE_URL}/rest/api/3/search?jql={urllib.parse.quote(jql)}&maxResults=10"

    # Basic auth
    auth = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()

    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {auth}",
    }

    request = urllib.request.Request(url, headers=headers)

    try:
        with urllib.request.urlopen(request) as response:
            data = json.loads(response.read().decode())
            return data.get("issues", [])
    except Exception as e:
        return []

def format_alfred_results(issues):
    """Format JIRA issues for Alfred"""
    items = []

    status_icons = {
        "To Do": "⚪",
        "In Progress": "🔵",
        "Done": "✅",
        "Blocked": "🔴",
    }

    for issue in issues:
        fields = issue["fields"]
        status = fields.get("status", {}).get("name", "Unknown")
        icon = status_icons.get(status, "⚫")

        items.append({
            "uid": issue["key"],
            "title": f"{icon} {issue['key']}: {fields['summary']}",
            "subtitle": f"{status} | {fields.get('assignee', {}).get('displayName', 'Unassigned')}",
            "arg": f"{JIRA_BASE_URL}/browse/{issue['key']}",
            "icon": {"path": "jira-icon.png"},
            "mods": {
                "cmd": {
                    "arg": issue["key"],
                    "subtitle": "Copy issue key"
                }
            }
        })

    return {"items": items}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""
    issues = search_jira(query)
    result = format_alfred_results(issues)
    print(json.dumps(result))
```

```python
#!/usr/bin/env python3
# alfred-snippet-manager.py
# ABOUTME: Text snippet management
# ABOUTME: Store and retrieve code snippets

import sys
import json
import os
import hashlib
from pathlib import Path

SNIPPETS_DIR = Path.home() / ".alfred-snippets"
SNIPPETS_DIR.mkdir(exist_ok=True)

def load_snippets():
    """Load all snippets"""
    snippets = []
    for file in SNIPPETS_DIR.glob("*.json"):
        with open(file) as f:
            snippet = json.load(f)
            snippet["file"] = str(file)
            snippets.append(snippet)
    return sorted(snippets, key=lambda x: x.get("uses", 0), reverse=True)

def save_snippet(name, content, tags=None):
    """Save a new snippet"""
    snippet_id = hashlib.md5(name.encode()).hexdigest()[:8]
    snippet = {
        "id": snippet_id,
        "name": name,
        "content": content,
        "tags": tags or [],
        "uses": 0,
    }
    with open(SNIPPETS_DIR / f"{snippet_id}.json", "w") as f:
        json.dump(snippet, f, indent=2)
    return snippet

def increment_use(snippet):
    """Increment usage counter"""
    snippet["uses"] = snippet.get("uses", 0) + 1
    with open(snippet["file"], "w") as f:
        json.dump({k: v for k, v in snippet.items() if k != "file"}, f, indent=2)

def search_snippets(query):
    """Search snippets by name or tags"""
    snippets = load_snippets()
    if not query:
        return snippets

    query_lower = query.lower()
    return [
        s for s in snippets
        if query_lower in s["name"].lower()
        or any(query_lower in tag.lower() for tag in s.get("tags", []))
    ]

def format_alfred_results(snippets):
    """Format snippets for Alfred"""
    items = []

    for snippet in snippets:
        tags = ", ".join(snippet.get("tags", []))
        preview = snippet["content"][:50] + "..." if len(snippet["content"]) > 50 else snippet["content"]

        items.append({
            "uid": snippet["id"],
            "title": snippet["name"],
            "subtitle": f"Uses: {snippet.get('uses', 0)} | {tags} | {preview}",
            "arg": snippet["content"],
            "icon": {"path": "snippet-icon.png"},
            "text": {
                "copy": snippet["content"],
                "largetype": snippet["content"]
            },
            "variables": {
                "snippet_file": snippet.get("file", "")
            }
        })

    return {"items": items}

if __name__ == "__main__":
    query = sys.argv[1] if len(sys.argv) > 1 else ""

    if query.startswith("save:"):
        # Save new snippet: "save:name|content|tag1,tag2"
        parts = query[5:].split("|")
        if len(parts) >= 2:
            name, content = parts[0], parts[1]
            tags = parts[2].split(",") if len(parts) > 2 else []
            snippet = save_snippet(name, content, tags)
            print(json.dumps({"items": [{"title": f"Saved: {name}", "arg": ""}]}))
        sys.exit(0)

    snippets = search_snippets(query)
    result = format_alfred_results(snippets)
    print(json.dumps(result))
```

### 5. Raycast Extension - API Integration

```tsx
// src/api-tester.tsx
// ABOUTME: API testing and debugging tool
// ABOUTME: Make HTTP requests from Raycast

import {
  ActionPanel,
  Action,
  Form,
  showToast,
  Toast,
  Clipboard,
  Detail,
  useNavigation,
} from "@raycast/api";
import { useState } from "react";
import fetch from "node-fetch";

interface RequestResult {
  status: number;
  statusText: string;
  headers: Record<string, string>;
  body: string;
  time: number;
}

function ResultView({ result }: { result: RequestResult }) {
  const markdown = `
# Response

**Status:** ${result.status} ${result.statusText}
**Time:** ${result.time}ms

## Headers
\`\`\`json
${JSON.stringify(result.headers, null, 2)}
\`\`\`

## Body
\`\`\`json
${result.body}
\`\`\`
`;

  return (
    <Detail
      markdown={markdown}
      actions={
        <ActionPanel>
          <Action.CopyToClipboard title="Copy Response Body" content={result.body} />
          <Action.CopyToClipboard
            title="Copy Headers"
            content={JSON.stringify(result.headers, null, 2)}
          />
        </ActionPanel>
      }
    />
  );
}

export default function Command() {
  const [method, setMethod] = useState("GET");
  const [url, setUrl] = useState("");
  const [headers, setHeaders] = useState("");
  const [body, setBody] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { push } = useNavigation();

  async function makeRequest() {
    if (!url) {
      showToast({ style: Toast.Style.Failure, title: "URL is required" });
      return;
    }

    setIsLoading(true);
    const startTime = Date.now();

    try {
      // Parse headers
      const headerObj: Record<string, string> = {};
      if (headers) {
        headers.split("\n").forEach((line) => {
          const [key, ...valueParts] = line.split(":");
          if (key && valueParts.length) {
            headerObj[key.trim()] = valueParts.join(":").trim();
          }
        });
      }

      const options: RequestInit = {
        method,
        headers: headerObj,
      };

      if (body && ["POST", "PUT", "PATCH"].includes(method)) {
        options.body = body;
        if (!headerObj["Content-Type"]) {
          headerObj["Content-Type"] = "application/json";
        }
      }

      const response = await fetch(url, options);
      const responseBody = await response.text();
      const endTime = Date.now();

      // Extract response headers
      const responseHeaders: Record<string, string> = {};
      response.headers.forEach((value, key) => {
        responseHeaders[key] = value;
      });

      // Try to format JSON
      let formattedBody = responseBody;
      try {
        formattedBody = JSON.stringify(JSON.parse(responseBody), null, 2);
      } catch {
        // Not JSON, keep as-is
      }

      const result: RequestResult = {
        status: response.status,
        statusText: response.statusText,
        headers: responseHeaders,
        body: formattedBody,
        time: endTime - startTime,
      };

      push(<ResultView result={result} />);
    } catch (error) {
      showToast({
        style: Toast.Style.Failure,
        title: "Request failed",
        message: String(error),
      });
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Form
      isLoading={isLoading}
      actions={
        <ActionPanel>
          <Action.SubmitForm title="Send Request" onSubmit={makeRequest} />
        </ActionPanel>
      }
    >
      <Form.Dropdown id="method" title="Method" value={method} onChange={setMethod}>
        <Form.Dropdown.Item value="GET" title="GET" />
        <Form.Dropdown.Item value="POST" title="POST" />
        <Form.Dropdown.Item value="PUT" title="PUT" />
        <Form.Dropdown.Item value="PATCH" title="PATCH" />
        <Form.Dropdown.Item value="DELETE" title="DELETE" />
      </Form.Dropdown>

      <Form.TextField
        id="url"
        title="URL"
        placeholder="https://api.example.com/endpoint"
        value={url}
        onChange={setUrl}
      />

      <Form.TextArea
        id="headers"
        title="Headers"
        placeholder="Content-Type: application/json
Authorization: Bearer token"
        value={headers}
        onChange={setHeaders}
      />

      {["POST", "PUT", "PATCH"].includes(method) && (
        <Form.TextArea
          id="body"
          title="Body"
          placeholder='{"key": "value"}'
          value={body}
          onChange={setBody}
        />
      )}
    </Form>
  );
}
```

### 6. Keyboard Shortcuts and Snippets

```json
// raycast-snippets.json
// ABOUTME: Text expansion snippets
// ABOUTME: Common code templates and text patterns
{
  "snippets": [
    {
      "name": "Python main block",
      "keyword": "pymain",
      "text": "if __name__ == \"__main__\":\n    main()"
    },
    {
      "name": "TypeScript async function",
      "keyword": "tsasync",
      "text": "async function ${1:functionName}(${2:params}): Promise<${3:void}> {\n    $0\n}"
    },
    {
      "name": "React component",
      "keyword": "rcomp",
      "text": "import React from 'react';\n\ninterface ${1:Component}Props {\n    $2\n}\n\nexport function ${1:Component}({ $3 }: ${1:Component}Props) {\n    return (\n        <div>\n            $0\n        </div>\n    );\n}"
    },
    {
      "name": "Console log",
      "keyword": "clog",
      "text": "console.log('${1:label}:', ${2:value});"
    },
    {
      "name": "Try catch",
      "keyword": "trycatch",
      "text": "try {\n    $1\n} catch (error) {\n    console.error('Error:', error);\n    $0\n}"
    },
    {
      "name": "Date ISO",
      "keyword": "dateiso",
      "text": "{clipboard | date:iso}"
    },
    {
      "name": "UUID",
      "keyword": "uuid",
      "text": "{random:uuid}"
    },
    {
      "name": "Email signature",
      "keyword": "esig",
      "text": "Best regards,\n{user:name}\n{user:email}"
    }
  ]
}
```

```applescript
-- alfred-hotkey-actions.applescript
-- ABOUTME: Global hotkey actions
-- ABOUTME: Quick actions for common tasks

on alfred_script(q)
    -- q contains the action to perform

    if q is "screenshot-region" then
        do shell script "screencapture -i ~/Desktop/screenshot-$(date +%Y%m%d-%H%M%S).png"
        return "Screenshot saved to Desktop"

    else if q is "toggle-dark-mode" then
        tell application "System Events"
            tell appearance preferences
                set dark mode to not dark mode
            end tell
        end tell
        return "Toggled dark mode"

    else if q is "empty-trash" then
        tell application "Finder"
            empty trash
        end tell
        return "Trash emptied"

    else if q is "show-hidden" then
        do shell script "defaults write com.apple.finder AppleShowAllFiles -bool true && killall Finder"
        return "Hidden files visible"

    else if q is "hide-hidden" then
        do shell script "defaults write com.apple.finder AppleShowAllFiles -bool false && killall Finder"
        return "Hidden files hidden"

    else if q is "flush-dns" then
        do shell script "sudo dscacheutil -flushcache && sudo killall -HUP mDNSResponder" with administrator privileges
        return "DNS cache flushed"

    else if q is "ip-address" then
        set localIP to do shell script "ipconfig getifaddr en0"
        set publicIP to do shell script "curl -s ifconfig.me"
        set the clipboard to publicIP
        return "Local: " & localIP & " | Public: " & publicIP & " (copied)"

    end if

    return "Unknown action: " & q
end alfred_script
```

## Integration Examples

### Project Switcher Integration

```tsx
// src/project-switcher.tsx
// ABOUTME: Unified project switcher
// ABOUTME: Integrates with multiple project sources

import {
  ActionPanel,
  Action,
  List,
  Icon,
  LocalStorage,
  getPreferenceValues,
} from "@raycast/api";
import { useState, useEffect } from "react";
import { exec } from "child_process";
import { promisify } from "util";
import fs from "fs";
import path from "path";

const execAsync = promisify(exec);

interface Preferences {
  projectDirs: string;
  githubEnabled: boolean;
  gitlabEnabled: boolean;
}

interface Project {
  name: string;
  path: string;
  source: "local" | "github" | "gitlab";
  url?: string;
  lastAccessed?: number;
}

export default function Command() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const preferences = getPreferenceValues<Preferences>();

  useEffect(() => {
    loadAllProjects();
  }, []);

  async function loadAllProjects() {
    const allProjects: Project[] = [];

    // Load local projects
    const dirs = preferences.projectDirs.split(",").map((d) => d.trim());
    for (const dir of dirs) {
      const expandedDir = dir.replace("~", process.env.HOME || "");
      if (fs.existsSync(expandedDir)) {
        const entries = fs.readdirSync(expandedDir, { withFileTypes: true });
        for (const entry of entries) {
          if (entry.isDirectory() && !entry.name.startsWith(".")) {
            allProjects.push({
              name: entry.name,
              path: path.join(expandedDir, entry.name),
              source: "local",
            });
          }
        }
      }
    }

    // Load access times
    const accessJson = await LocalStorage.getItem<string>("project-access");
    const accessTimes = accessJson ? JSON.parse(accessJson) : {};

    allProjects.forEach((p) => {
      p.lastAccessed = accessTimes[p.path] || 0;
    });

    // Sort by last accessed
    allProjects.sort((a, b) => (b.lastAccessed || 0) - (a.lastAccessed || 0));

    setProjects(allProjects);
    setIsLoading(false);
  }

  async function openProject(project: Project, app: string) {
    const cmd =
      app === "code"
        ? `code "${project.path}"`
        : app === "terminal"
        ? `open -a Terminal "${project.path}"`
        : `open "${project.path}"`;

    await execAsync(cmd);

    // Update access time
    const accessJson = await LocalStorage.getItem<string>("project-access");
    const accessTimes = accessJson ? JSON.parse(accessJson) : {};
    accessTimes[project.path] = Date.now();
    await LocalStorage.setItem("project-access", JSON.stringify(accessTimes));
  }

  const sourceIcons = {
    local: Icon.Folder,
    github: Icon.Globe,
    gitlab: Icon.Globe,
  };

  return (
    <List isLoading={isLoading} searchBarPlaceholder="Search projects...">
      {projects.map((project) => (
        <List.Item
          key={project.path}
          title={project.name}
          subtitle={project.path}
          icon={sourceIcons[project.source]}
          accessories={[
            project.lastAccessed
              ? { text: new Date(project.lastAccessed).toLocaleDateString() }
              : {},
          ]}
          actions={
            <ActionPanel>
              <Action
                title="Open in VS Code"
                icon={Icon.Code}
                onAction={() => openProject(project, "code")}
              />
              <Action
                title="Open in Terminal"
                icon={Icon.Terminal}
                onAction={() => openProject(project, "terminal")}
              />
              <Action
                title="Open in Finder"
                icon={Icon.Finder}
                onAction={() => openProject(project, "finder")}
              />
            </ActionPanel>
          }
        />
      ))}
    </List>
  );
}
```

## Best Practices

### 1. Raycast Extension Development

```typescript
// Use proper error handling
import { showToast, Toast } from "@raycast/api";

async function safeFetch(url: string) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }
    return response.json();
  } catch (error) {
    showToast({
      style: Toast.Style.Failure,
      title: "Request failed",
      message: String(error),
    });
    return null;
  }
}

// Use LocalStorage for persistence
import { LocalStorage } from "@raycast/api";

async function saveData(key: string, data: any) {
  await LocalStorage.setItem(key, JSON.stringify(data));
}

async function loadData<T>(key: string, defaultValue: T): Promise<T> {
  const json = await LocalStorage.getItem<string>(key);
  return json ? JSON.parse(json) : defaultValue;
}
```

### 2. Alfred Workflow Best Practices

```python
# Always output valid JSON for Script Filters
import json
import sys

def output_items(items):
    """Output Alfred JSON format"""
    print(json.dumps({"items": items}))

def output_error(message):
    """Output error as Alfred item"""
    output_items([{
        "title": "Error",
        "subtitle": message,
        "icon": {"path": "error.png"}
    }])

# Handle keyboard interrupt gracefully
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        output_error(str(e))
        sys.exit(1)
```

### 3. Performance Optimization

```typescript
// Debounce search queries
import { useState, useCallback } from "react";
import { useDebouncedValue } from "@raycast/utils";

function SearchCommand() {
  const [query, setQuery] = useState("");
  const debouncedQuery = useDebouncedValue(query, 300);

  // Use debouncedQuery for API calls
}

// Cache API responses
const cache = new Map<string, { data: any; timestamp: number }>();
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

async function cachedFetch(url: string) {
  const cached = cache.get(url);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.data;
  }

  const data = await fetch(url).then((r) => r.json());
  cache.set(url, { data, timestamp: Date.now() });
  return data;
}
```

## Troubleshooting

### Common Issues

**Issue: Raycast extension not loading**
```bash
# Clear Raycast cache
rm -rf ~/Library/Caches/com.raycast.macos

# Rebuild extension
cd your-extension
npm run build

# Check for errors
npm run lint
```

**Issue: Alfred workflow not executing**
```bash
# Check script permissions
chmod +x workflow-script.sh

# Test script manually
./workflow-script.sh "test query"

# Check Alfred debug log
# Alfred Preferences > Workflows > Click workflow > Debug
```

**Issue: AppleScript permissions**
```applescript
-- Grant accessibility permissions
-- System Preferences > Security & Privacy > Privacy > Accessibility

-- Test permissions
tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
end tell
```

### Debug Commands

```bash
# Test Raycast script command
./script.sh "test argument"

# Test Alfred Python script
python3 workflow.py "test query" | jq

# Check Alfred workflow variables
echo $alfred_workflow_data

# Monitor Raycast logs
log stream --predicate 'subsystem == "com.raycast.macos"'
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with Raycast and Alfred patterns |

## Resources

- [Raycast Developer Documentation](https://developers.raycast.com/)
- [Raycast API Reference](https://developers.raycast.com/api-reference)
- [Alfred Workflow Documentation](https://www.alfredapp.com/help/workflows/)
- [AppleScript Language Guide](https://developer.apple.com/library/archive/documentation/AppleScript/Conceptual/AppleScriptLangGuide/)
- [Raycast Store](https://www.raycast.com/store)
- [Alfred Gallery](https://alfred.app/workflows/)

---

*This skill provides production-ready patterns for macOS launcher automation, enabling keyboard-driven productivity and seamless workflow integration.*

---
name: vscode-extensions
version: 1.0.0
description: VS Code productivity optimization with essential extensions, settings sync, profiles, keybindings, snippets, and workspace configuration
author: workspace-hub
category: devtools
type: skill
capabilities:
  - extension_management
  - settings_configuration
  - profile_management
  - keybinding_customization
  - snippet_creation
  - workspace_settings
  - task_automation
  - debugging_configuration
  - theme_customization
  - remote_development
tools:
  - code
  - code-insiders
  - codium
tags: [vscode, ide, extensions, productivity, editor, development, settings, profiles]
platforms: [linux, macos, windows]
related_skills:
  - cli-productivity
  - git-advanced
  - docker
---

# VS Code Extensions Skill

Master VS Code productivity with essential extensions, optimal settings, custom keybindings, and workspace configuration. This skill covers extension recommendations by category, settings sync, profiles, snippets, tasks, and debugging configurations.

## When to Use This Skill

### USE when:
- Setting up a new development environment
- Optimizing VS Code for specific languages/frameworks
- Creating consistent team configurations
- Building custom snippets and tasks
- Configuring debugging for complex applications
- Managing multiple project profiles
- Automating repetitive editor tasks

### DON'T USE when:
- Need full IDE features (use JetBrains IDEs)
- Working exclusively in terminal (use vim/neovim)
- Resource-constrained environments (use lighter editors)
- Pair programming with different editors (standardize first)

## Prerequisites

### Installation

```bash
# macOS
brew install --cask visual-studio-code

# Linux (Ubuntu/Debian)
sudo snap install code --classic
# Or download from https://code.visualstudio.com/

# Windows
winget install Microsoft.VisualStudioCode
# Or download from https://code.visualstudio.com/

# Verify installation
code --version

# Open VS Code from terminal
code .                    # Open current directory
code file.txt             # Open file
code --diff file1 file2   # Diff two files
code --goto file:10:5     # Open file at line 10, column 5
```

### CLI Extension Management

```bash
# List installed extensions
code --list-extensions

# Install extension
code --install-extension ms-python.python

# Uninstall extension
code --uninstall-extension extension-id

# Install multiple extensions from file
cat extensions.txt | xargs -L 1 code --install-extension

# Export extensions list
code --list-extensions > extensions.txt

# Install extensions on new machine
cat extensions.txt | xargs -L 1 code --install-extension
```

## Core Capabilities

### 1. Essential Extensions by Category

```bash
# Create extensions installation script
cat > install-extensions.sh << 'EOF'
#!/bin/bash
# ABOUTME: Install curated VS Code extensions by category
# ABOUTME: Run with category argument: ./install-extensions.sh python

install_base() {
    # Core productivity
    code --install-extension esbenp.prettier-vscode
    code --install-extension dbaeumer.vscode-eslint
    code --install-extension editorconfig.editorconfig
    code --install-extension streetsidesoftware.code-spell-checker
    code --install-extension usernamehw.errorlens
    code --install-extension gruntfuggly.todo-tree
    code --install-extension aaron-bond.better-comments
    code --install-extension christian-kohler.path-intellisense

    # Git
    code --install-extension eamodio.gitlens
    code --install-extension mhutchie.git-graph

    # Theme and icons
    code --install-extension pkief.material-icon-theme
    code --install-extension github.github-vscode-theme
}

install_python() {
    code --install-extension ms-python.python
    code --install-extension ms-python.vscode-pylance
    code --install-extension ms-python.black-formatter
    code --install-extension charliermarsh.ruff
    code --install-extension ms-python.debugpy
    code --install-extension njpwerner.autodocstring
    code --install-extension littlefoxteam.vscode-python-test-adapter
}

install_javascript() {
    code --install-extension esbenp.prettier-vscode
    code --install-extension dbaeumer.vscode-eslint
    code --install-extension dsznajder.es7-react-js-snippets
    code --install-extension bradlc.vscode-tailwindcss
    code --install-extension prisma.prisma
    code --install-extension wallabyjs.quokka-vscode
}

install_typescript() {
    install_javascript
    code --install-extension ms-vscode.vscode-typescript-next
    code --install-extension pmneo.tsimporter
    code --install-extension stringham.move-ts
}

install_rust() {
    code --install-extension rust-lang.rust-analyzer
    code --install-extension serayuzgur.crates
    code --install-extension tamasfe.even-better-toml
    code --install-extension vadimcn.vscode-lldb
}

install_go() {
    code --install-extension golang.go
    code --install-extension zxh404.vscode-proto3
}

install_docker() {
    code --install-extension ms-azuretools.vscode-docker
    code --install-extension ms-vscode-remote.remote-containers
    code --install-extension ms-kubernetes-tools.vscode-kubernetes-tools
    code --install-extension redhat.vscode-yaml
}

install_web() {
    code --install-extension ritwickdey.liveserver
    code --install-extension formulahendry.auto-rename-tag
    code --install-extension pranaygp.vscode-css-peek
    code --install-extension zignd.html-css-class-completion
    code --install-extension ecmel.vscode-html-css
}

install_data() {
    code --install-extension ms-toolsai.jupyter
    code --install-extension mechatroner.rainbow-csv
    code --install-extension randomfractalsinc.vscode-data-preview
    code --install-extension mtxr.sqltools
    code --install-extension cweijan.vscode-database-client2
}

install_remote() {
    code --install-extension ms-vscode-remote.remote-ssh
    code --install-extension ms-vscode-remote.remote-containers
    code --install-extension ms-vscode-remote.remote-wsl
    code --install-extension ms-vscode.remote-explorer
}

install_ai() {
    code --install-extension github.copilot
    code --install-extension github.copilot-chat
    code --install-extension continue.continue
}

# Main
case "$1" in
    base) install_base ;;
    python) install_base && install_python ;;
    javascript|js) install_base && install_javascript ;;
    typescript|ts) install_base && install_typescript ;;
    rust) install_base && install_rust ;;
    go) install_base && install_go ;;
    docker) install_base && install_docker ;;
    web) install_base && install_web ;;
    data) install_base && install_data ;;
    remote) install_remote ;;
    ai) install_ai ;;
    all) install_base && install_python && install_typescript && install_docker && install_remote ;;
    *)
        echo "Usage: $0 {base|python|javascript|typescript|rust|go|docker|web|data|remote|ai|all}"
        exit 1
        ;;
esac

echo "Extensions installed successfully!"
EOF
chmod +x install-extensions.sh
```

### 2. Settings Configuration

```jsonc
// settings.json - User settings
// Location: ~/.config/Code/User/settings.json (Linux)
//           ~/Library/Application Support/Code/User/settings.json (macOS)
//           %APPDATA%\Code\User\settings.json (Windows)
{
    // Editor appearance
    "editor.fontSize": 14,
    "editor.fontFamily": "'JetBrains Mono', 'Fira Code', 'SF Mono', Consolas, monospace",
    "editor.fontLigatures": true,
    "editor.lineHeight": 1.6,
    "editor.letterSpacing": 0.5,
    "editor.cursorBlinking": "smooth",
    "editor.cursorSmoothCaretAnimation": "on",
    "editor.smoothScrolling": true,

    // Editor behavior
    "editor.lineNumbers": "relative",
    "editor.rulers": [80, 120],
    "editor.wordWrap": "off",
    "editor.minimap.enabled": false,
    "editor.renderWhitespace": "boundary",
    "editor.bracketPairColorization.enabled": true,
    "editor.guides.bracketPairs": "active",
    "editor.stickyScroll.enabled": true,
    "editor.inlineSuggest.enabled": true,

    // Code formatting
    "editor.formatOnSave": true,
    "editor.formatOnPaste": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.codeActionsOnSave": {
        "source.fixAll": "explicit",
        "source.organizeImports": "explicit"
    },

    // Tab and indentation
    "editor.tabSize": 4,
    "editor.insertSpaces": true,
    "editor.detectIndentation": true,
    "editor.trimAutoWhitespace": true,

    // Search and navigation
    "editor.quickSuggestions": {
        "other": true,
        "comments": false,
        "strings": true
    },
    "editor.suggestSelection": "first",
    "editor.acceptSuggestionOnEnter": "on",
    "editor.snippetSuggestions": "top",

    // Files
    "files.autoSave": "onFocusChange",
    "files.trimTrailingWhitespace": true,
    "files.insertFinalNewline": true,
    "files.trimFinalNewlines": true,
    "files.exclude": {
        "**/.git": true,
        "**/.DS_Store": true,
        "**/node_modules": true,
        "**/__pycache__": true,
        "**/.pytest_cache": true,
        "**/venv": true,
        "**/.venv": true
    },
    "files.watcherExclude": {
        "**/node_modules/**": true,
        "**/.git/objects/**": true
    },

    // Search
    "search.exclude": {
        "**/node_modules": true,
        "**/dist": true,
        "**/build": true,
        "**/coverage": true,
        "**/.next": true
    },
    "search.useIgnoreFiles": true,
    "search.smartCase": true,

    // Terminal
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.fontFamily": "'JetBrains Mono', 'MesloLGS NF', monospace",
    "terminal.integrated.cursorStyle": "line",
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.scrollback": 10000,

    // Git
    "git.autofetch": true,
    "git.confirmSync": false,
    "git.enableSmartCommit": true,
    "git.openRepositoryInParentFolders": "always",
    "gitlens.currentLine.enabled": true,
    "gitlens.hovers.currentLine.over": "line",

    // Workbench
    "workbench.startupEditor": "none",
    "workbench.editor.enablePreview": false,
    "workbench.editor.tabCloseButton": "right",
    "workbench.colorTheme": "GitHub Dark Default",
    "workbench.iconTheme": "material-icon-theme",
    "workbench.tree.indent": 20,
    "workbench.tree.renderIndentGuides": "always",

    // Breadcrumbs
    "breadcrumbs.enabled": true,
    "breadcrumbs.filePath": "on",

    // Explorer
    "explorer.confirmDelete": false,
    "explorer.confirmDragAndDrop": false,
    "explorer.compactFolders": false,
    "explorer.sortOrder": "type",

    // Zen Mode
    "zenMode.hideLineNumbers": false,
    "zenMode.centerLayout": true,

    // Extensions
    "errorLens.enabled": true,
    "errorLens.enabledDiagnosticLevels": ["error", "warning"],
    "todo-tree.general.tags": ["TODO", "FIXME", "BUG", "HACK", "XXX", "NOTE"],

    // Telemetry
    "telemetry.telemetryLevel": "off"
}
```

### 3. Language-Specific Settings

```jsonc
// settings.json - Language-specific overrides
{
    // Python
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true,
        "editor.tabSize": 4,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    },
    "python.analysis.typeCheckingMode": "basic",
    "python.analysis.autoImportCompletions": true,
    "python.terminal.activateEnvironment": true,
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false,
    "ruff.organizeImports": true,

    // JavaScript/TypeScript
    "[javascript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "[typescript]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "[typescriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "[javascriptreact]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "typescript.preferences.importModuleSpecifier": "relative",
    "typescript.updateImportsOnFileMove.enabled": "always",

    // JSON
    "[json]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "[jsonc]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },

    // YAML
    "[yaml]": {
        "editor.defaultFormatter": "redhat.vscode-yaml",
        "editor.tabSize": 2,
        "editor.autoIndent": "advanced"
    },
    "yaml.schemas": {
        "https://json.schemastore.org/github-workflow.json": ".github/workflows/*.yml"
    },

    // Markdown
    "[markdown]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.wordWrap": "on",
        "editor.quickSuggestions": {
            "other": true,
            "comments": false,
            "strings": true
        }
    },
    "markdown.preview.fontSize": 14,

    // HTML/CSS
    "[html]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "[css]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },
    "[scss]": {
        "editor.defaultFormatter": "esbenp.prettier-vscode",
        "editor.tabSize": 2
    },

    // Go
    "[go]": {
        "editor.defaultFormatter": "golang.go",
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": "always"
        }
    },
    "go.lintTool": "golangci-lint",
    "go.testOnSave": true,

    // Rust
    "[rust]": {
        "editor.defaultFormatter": "rust-lang.rust-analyzer",
        "editor.formatOnSave": true
    },
    "rust-analyzer.checkOnSave.command": "clippy",

    // Shell
    "[shellscript]": {
        "editor.defaultFormatter": "foxundermoon.shell-format",
        "editor.tabSize": 4
    }
}
```

### 4. Keybindings Configuration

```jsonc
// keybindings.json
// Location: ~/.config/Code/User/keybindings.json (Linux)
[
    // Navigation
    {
        "key": "ctrl+shift+e",
        "command": "workbench.view.explorer"
    },
    {
        "key": "ctrl+shift+g",
        "command": "workbench.view.scm"
    },
    {
        "key": "ctrl+shift+f",
        "command": "workbench.view.search"
    },
    {
        "key": "ctrl+shift+d",
        "command": "workbench.view.debug"
    },
    {
        "key": "ctrl+shift+x",
        "command": "workbench.view.extensions"
    },

    // Terminal
    {
        "key": "ctrl+`",
        "command": "workbench.action.terminal.toggleTerminal"
    },
    {
        "key": "ctrl+shift+`",
        "command": "workbench.action.terminal.new"
    },
    {
        "key": "ctrl+shift+c",
        "command": "workbench.action.terminal.openNativeConsole"
    },

    // Editor navigation
    {
        "key": "ctrl+tab",
        "command": "workbench.action.nextEditor"
    },
    {
        "key": "ctrl+shift+tab",
        "command": "workbench.action.previousEditor"
    },
    {
        "key": "alt+left",
        "command": "workbench.action.navigateBack"
    },
    {
        "key": "alt+right",
        "command": "workbench.action.navigateForward"
    },

    // Line manipulation
    {
        "key": "alt+up",
        "command": "editor.action.moveLinesUpAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "alt+down",
        "command": "editor.action.moveLinesDownAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+up",
        "command": "editor.action.copyLinesUpAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+down",
        "command": "editor.action.copyLinesDownAction",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+shift+k",
        "command": "editor.action.deleteLines",
        "when": "editorTextFocus && !editorReadonly"
    },

    // Selection
    {
        "key": "ctrl+l",
        "command": "expandLineSelection",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+d",
        "command": "editor.action.addSelectionToNextFindMatch",
        "when": "editorFocus"
    },
    {
        "key": "ctrl+shift+l",
        "command": "editor.action.selectHighlights",
        "when": "editorFocus"
    },

    // Multi-cursor
    {
        "key": "ctrl+alt+up",
        "command": "editor.action.insertCursorAbove",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+alt+down",
        "command": "editor.action.insertCursorBelow",
        "when": "editorTextFocus"
    },

    // Code actions
    {
        "key": "ctrl+.",
        "command": "editor.action.quickFix",
        "when": "editorHasCodeActionsProvider && editorTextFocus && !editorReadonly"
    },
    {
        "key": "f2",
        "command": "editor.action.rename",
        "when": "editorHasRenameProvider && editorTextFocus && !editorReadonly"
    },
    {
        "key": "f12",
        "command": "editor.action.revealDefinition",
        "when": "editorHasDefinitionProvider && editorTextFocus"
    },
    {
        "key": "alt+f12",
        "command": "editor.action.peekDefinition",
        "when": "editorHasDefinitionProvider && editorTextFocus"
    },
    {
        "key": "shift+f12",
        "command": "editor.action.goToReferences",
        "when": "editorHasReferenceProvider && editorTextFocus"
    },

    // Formatting
    {
        "key": "shift+alt+f",
        "command": "editor.action.formatDocument",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "ctrl+k ctrl+f",
        "command": "editor.action.formatSelection",
        "when": "editorHasDocumentSelectionFormattingProvider && editorTextFocus && !editorReadonly"
    },

    // Comments
    {
        "key": "ctrl+/",
        "command": "editor.action.commentLine",
        "when": "editorTextFocus && !editorReadonly"
    },
    {
        "key": "shift+alt+a",
        "command": "editor.action.blockComment",
        "when": "editorTextFocus && !editorReadonly"
    },

    // Fold/unfold
    {
        "key": "ctrl+shift+[",
        "command": "editor.fold",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+shift+]",
        "command": "editor.unfold",
        "when": "editorTextFocus"
    },
    {
        "key": "ctrl+k ctrl+0",
        "command": "editor.foldAll"
    },
    {
        "key": "ctrl+k ctrl+j",
        "command": "editor.unfoldAll"
    },

    // Sidebar
    {
        "key": "ctrl+b",
        "command": "workbench.action.toggleSidebarVisibility"
    },
    {
        "key": "ctrl+shift+b",
        "command": "workbench.action.toggleAuxiliaryBar"
    },

    // Panels
    {
        "key": "ctrl+j",
        "command": "workbench.action.togglePanel"
    },

    // Files
    {
        "key": "ctrl+n",
        "command": "workbench.action.files.newUntitledFile"
    },
    {
        "key": "ctrl+w",
        "command": "workbench.action.closeActiveEditor"
    },
    {
        "key": "ctrl+shift+w",
        "command": "workbench.action.closeAllEditors"
    },

    // Git (GitLens)
    {
        "key": "ctrl+shift+g b",
        "command": "gitlens.toggleFileBlame"
    },
    {
        "key": "ctrl+shift+g h",
        "command": "gitlens.showQuickFileHistory"
    },

    // Custom productivity
    {
        "key": "ctrl+shift+o",
        "command": "workbench.action.gotoSymbol"
    },
    {
        "key": "ctrl+t",
        "command": "workbench.action.showAllSymbols"
    }
]
```

### 5. Custom Snippets

```jsonc
// snippets/python.json
// Location: ~/.config/Code/User/snippets/python.json
{
    "Python Main Block": {
        "prefix": "main",
        "body": [
            "def main():",
            "    ${1:pass}",
            "",
            "",
            "if __name__ == \"__main__\":",
            "    main()"
        ],
        "description": "Python main block"
    },
    "Python Class": {
        "prefix": "class",
        "body": [
            "class ${1:ClassName}:",
            "    \"\"\"${2:Class description.}\"\"\"",
            "",
            "    def __init__(self, ${3:args}):",
            "        ${4:pass}",
            "",
            "    def ${5:method}(self):",
            "        ${6:pass}"
        ],
        "description": "Python class definition"
    },
    "Python Dataclass": {
        "prefix": "dataclass",
        "body": [
            "from dataclasses import dataclass",
            "",
            "",
            "@dataclass",
            "class ${1:ClassName}:",
            "    \"\"\"${2:Description.}\"\"\"",
            "",
            "    ${3:field}: ${4:str}"
        ],
        "description": "Python dataclass"
    },
    "Python Type Hints": {
        "prefix": "typed",
        "body": [
            "def ${1:function_name}(",
            "    ${2:param}: ${3:str}",
            ") -> ${4:None}:",
            "    \"\"\"${5:Description.}\"\"\"",
            "    ${6:pass}"
        ],
        "description": "Typed function signature"
    },
    "Python Pytest Test": {
        "prefix": "test",
        "body": [
            "def test_${1:name}():",
            "    # Arrange",
            "    ${2:pass}",
            "",
            "    # Act",
            "    ${3:result = None}",
            "",
            "    # Assert",
            "    assert ${4:result is not None}"
        ],
        "description": "Pytest test function"
    },
    "ABOUTME Comment": {
        "prefix": "aboutme",
        "body": [
            "# ABOUTME: ${1:Brief description of file purpose}",
            "# ABOUTME: ${2:Additional detail about what the file does}"
        ],
        "description": "ABOUTME file header comment"
    }
}
```

```jsonc
// snippets/typescript.json
{
    "React Functional Component": {
        "prefix": "rfc",
        "body": [
            "interface ${1:ComponentName}Props {",
            "  ${2:prop}: ${3:string};",
            "}",
            "",
            "export function ${1:ComponentName}({ ${2:prop} }: ${1:ComponentName}Props) {",
            "  return (",
            "    <div>",
            "      ${4:content}",
            "    </div>",
            "  );",
            "}"
        ],
        "description": "React Functional Component with TypeScript"
    },
    "React useState Hook": {
        "prefix": "usestate",
        "body": [
            "const [${1:state}, set${1/(.*)/${1:/capitalize}/}] = useState<${2:string}>(${3:''});"
        ],
        "description": "React useState hook with TypeScript"
    },
    "React useEffect Hook": {
        "prefix": "useeffect",
        "body": [
            "useEffect(() => {",
            "  ${1:// effect}",
            "",
            "  return () => {",
            "    ${2:// cleanup}",
            "  };",
            "}, [${3:dependencies}]);"
        ],
        "description": "React useEffect hook"
    },
    "TypeScript Interface": {
        "prefix": "interface",
        "body": [
            "interface ${1:InterfaceName} {",
            "  ${2:property}: ${3:type};",
            "}"
        ],
        "description": "TypeScript interface"
    },
    "TypeScript Type": {
        "prefix": "type",
        "body": [
            "type ${1:TypeName} = {",
            "  ${2:property}: ${3:type};",
            "};"
        ],
        "description": "TypeScript type alias"
    },
    "Async Function": {
        "prefix": "asyncfn",
        "body": [
            "async function ${1:functionName}(${2:params}): Promise<${3:void}> {",
            "  try {",
            "    ${4:// implementation}",
            "  } catch (error) {",
            "    console.error(error);",
            "    throw error;",
            "  }",
            "}"
        ],
        "description": "Async function with error handling"
    }
}
```

### 6. Workspace Configuration

```jsonc
// .vscode/settings.json - Project-specific settings
{
    // Project-specific formatters
    "editor.defaultFormatter": "esbenp.prettier-vscode",
    "editor.formatOnSave": true,

    // Python project
    "python.defaultInterpreterPath": "${workspaceFolder}/.venv/bin/python",
    "python.testing.pytestPath": "${workspaceFolder}/.venv/bin/pytest",
    "python.testing.pytestArgs": ["tests"],
    "python.analysis.extraPaths": ["${workspaceFolder}/src"],

    // File associations
    "files.associations": {
        "*.env.*": "dotenv",
        "Dockerfile.*": "dockerfile"
    },

    // Search exclusions
    "search.exclude": {
        "**/node_modules": true,
        "**/.venv": true,
        "**/dist": true,
        "**/coverage": true
    },

    // Ruler for this project
    "editor.rulers": [88, 120],

    // Custom dictionary words
    "cSpell.words": [
        "pytest",
        "asyncio",
        "pydantic"
    ]
}
```

```jsonc
// .vscode/extensions.json - Recommended extensions
{
    "recommendations": [
        "ms-python.python",
        "ms-python.vscode-pylance",
        "ms-python.black-formatter",
        "charliermarsh.ruff",
        "esbenp.prettier-vscode",
        "dbaeumer.vscode-eslint",
        "eamodio.gitlens",
        "usernamehw.errorlens"
    ],
    "unwantedRecommendations": []
}
```

```jsonc
// .vscode/tasks.json - Build and run tasks
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Run Tests",
            "type": "shell",
            "command": "pytest",
            "args": ["tests/", "-v", "--cov=src"],
            "group": {
                "kind": "test",
                "isDefault": true
            },
            "presentation": {
                "reveal": "always",
                "panel": "new"
            },
            "problemMatcher": []
        },
        {
            "label": "Lint",
            "type": "shell",
            "command": "ruff",
            "args": ["check", "src/"],
            "group": "build",
            "presentation": {
                "reveal": "silent",
                "panel": "shared"
            },
            "problemMatcher": {
                "owner": "ruff",
                "fileLocation": ["relative", "${workspaceFolder}"],
                "pattern": {
                    "regexp": "^(.+):(\\d+):(\\d+): (\\w+) (.+)$",
                    "file": 1,
                    "line": 2,
                    "column": 3,
                    "severity": 4,
                    "message": 5
                }
            }
        },
        {
            "label": "Format",
            "type": "shell",
            "command": "black",
            "args": ["src/", "tests/"],
            "group": "build",
            "presentation": {
                "reveal": "silent"
            }
        },
        {
            "label": "Build Docker",
            "type": "shell",
            "command": "docker",
            "args": ["build", "-t", "${workspaceFolderBasename}:latest", "."],
            "group": "build",
            "presentation": {
                "reveal": "always"
            }
        },
        {
            "label": "Start Dev Server",
            "type": "shell",
            "command": "python",
            "args": ["-m", "uvicorn", "src.main:app", "--reload"],
            "isBackground": true,
            "problemMatcher": {
                "pattern": {
                    "regexp": "."
                },
                "background": {
                    "activeOnStart": true,
                    "beginsPattern": "^.*Uvicorn running.*$",
                    "endsPattern": "^.*Application startup complete.*$"
                }
            }
        }
    ]
}
```

```jsonc
// .vscode/launch.json - Debug configurations
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Current File",
            "type": "debugpy",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "cwd": "${workspaceFolder}"
        },
        {
            "name": "Python: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": ["src.main:app", "--reload", "--port", "8000"],
            "jinja": true,
            "justMyCode": true,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        },
        {
            "name": "Python: pytest",
            "type": "debugpy",
            "request": "launch",
            "module": "pytest",
            "args": ["tests/", "-v", "-s"],
            "console": "integratedTerminal"
        },
        {
            "name": "Node: Current File",
            "type": "node",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal"
        },
        {
            "name": "Node: npm start",
            "type": "node",
            "request": "launch",
            "runtimeExecutable": "npm",
            "runtimeArgs": ["run", "dev"],
            "console": "integratedTerminal"
        },
        {
            "name": "Attach to Docker",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ]
        }
    ],
    "compounds": [
        {
            "name": "Full Stack",
            "configurations": ["Python: FastAPI", "Node: npm start"]
        }
    ]
}
```

### 7. Profile Management

```bash
# Create profiles for different workflows
# Settings -> Profiles -> Create Profile

# Export profile
code --profile Python --export-default-profile > python-profile.json

# Import profile
code --profile Python --import-profile python-profile.json

# Switch profiles via command palette
# Cmd/Ctrl+Shift+P -> Profiles: Switch Profile

# Profile examples:
# - "Python" - Python extensions and settings
# - "Web" - JavaScript/TypeScript/React
# - "DevOps" - Docker, Kubernetes, YAML
# - "Minimal" - Basic editing only
# - "Writing" - Markdown, spell check
```

## Integration Examples

### Git Workflow Integration

```jsonc
// settings.json - Git integration
{
    "git.autofetch": true,
    "git.confirmSync": false,
    "git.enableSmartCommit": true,
    "git.postCommitCommand": "push",
    "git.fetchOnPull": true,
    "git.pruneOnFetch": true,

    // GitLens settings
    "gitlens.views.repositories.branches.layout": "tree",
    "gitlens.views.commits.files.layout": "tree",
    "gitlens.codeLens.enabled": true,
    "gitlens.codeLens.recentChange.enabled": true,
    "gitlens.currentLine.enabled": true,
    "gitlens.hovers.currentLine.over": "line",
    "gitlens.blame.format": "${author|10} ${date}",
    "gitlens.blame.heatmap.enabled": true
}
```

### Remote Development

```jsonc
// settings.json - Remote development
{
    // SSH
    "remote.SSH.remotePlatform": {
        "server1": "linux",
        "server2": "linux"
    },
    "remote.SSH.defaultExtensions": [
        "ms-python.python",
        "ms-python.vscode-pylance"
    ],

    // Containers
    "dev.containers.defaultExtensions": [
        "ms-python.python",
        "eamodio.gitlens"
    ],

    // WSL
    "remote.WSL.fileWatcher.polling": true
}
```

```jsonc
// .devcontainer/devcontainer.json
{
    "name": "Python Dev",
    "image": "mcr.microsoft.com/devcontainers/python:3.12",
    "features": {
        "ghcr.io/devcontainers/features/docker-in-docker:2": {}
    },
    "customizations": {
        "vscode": {
            "extensions": [
                "ms-python.python",
                "ms-python.vscode-pylance",
                "ms-python.black-formatter",
                "charliermarsh.ruff"
            ],
            "settings": {
                "python.defaultInterpreterPath": "/usr/local/bin/python"
            }
        }
    },
    "postCreateCommand": "pip install -e '.[dev]'",
    "forwardPorts": [8000]
}
```

## Best Practices

### 1. Extension Management

```bash
# Keep extensions minimal
# Review periodically
code --list-extensions | wc -l

# Disable per-workspace for unused extensions
# Settings -> Extensions -> Disable (Workspace)

# Use extension packs wisely
# Create custom packs for teams
```

### 2. Performance Optimization

```jsonc
{
    // Reduce file watching
    "files.watcherExclude": {
        "**/node_modules/**": true,
        "**/.git/objects/**": true,
        "**/venv/**": true
    },

    // Reduce search scope
    "search.exclude": {
        "**/node_modules": true,
        "**/dist": true
    },

    // Disable heavy features if needed
    "editor.minimap.enabled": false,
    "editor.codeLens": false,

    // Limit suggestions
    "editor.quickSuggestions": {
        "other": true,
        "comments": false,
        "strings": false
    }
}
```

### 3. Team Consistency

```jsonc
// .vscode/settings.json - Committed to repo
{
    // Consistent formatting
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "esbenp.prettier-vscode",

    // Consistent tab settings
    "editor.tabSize": 2,
    "editor.insertSpaces": true,

    // Consistent line endings
    "files.eol": "\n"
}
```

## Troubleshooting

### Common Issues

**Issue: Extensions not loading**
```bash
# Check extension host logs
# Help -> Toggle Developer Tools -> Console

# Reinstall extension
code --uninstall-extension extension-id
code --install-extension extension-id

# Reset VS Code
rm -rf ~/.config/Code/CachedData
```

**Issue: Slow startup**
```bash
# Profile startup
code --prof-startup

# Disable extensions
code --disable-extensions

# Check extension impact
# Help -> Startup Performance
```

**Issue: IntelliSense not working**
```bash
# Restart language server
# Cmd/Ctrl+Shift+P -> "Restart Extension Host"

# Clear workspace cache
rm -rf .vscode/.ropeproject
rm -rf __pycache__
```

**Issue: Settings not applying**
```bash
# Check settings precedence:
# 1. Workspace settings (.vscode/settings.json)
# 2. User settings (settings.json)
# 3. Default settings

# View effective settings
# Cmd/Ctrl+Shift+P -> "Preferences: Open Settings (JSON)"
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive VS Code configuration |

## Resources

- [VS Code Documentation](https://code.visualstudio.com/docs)
- [VS Code Keybindings Reference](https://code.visualstudio.com/docs/getstarted/keybindings)
- [Extension Marketplace](https://marketplace.visualstudio.com/vscode)
- [Snippet Guide](https://code.visualstudio.com/docs/editor/userdefinedsnippets)
- [Tasks Documentation](https://code.visualstudio.com/docs/editor/tasks)
- [Debugging Guide](https://code.visualstudio.com/docs/editor/debugging)

---

*This skill provides production-ready VS Code configurations for maximum developer productivity across multiple languages and frameworks.*

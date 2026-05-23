---
name: new-project
description: Scaffold a new Lean 4 project in the workspace. Use when creating a new project, library, or application.
---

# New Project Scaffolding

Create a new Lean 4 project with the correct structure for this workspace.

## Quick Start

1. Determine project category and name
2. Create directory structure
3. Generate lakefile.lean with GitHub-style dependencies
4. Create README.md and CLAUDE.md
5. Set up test structure with Crucible

## Project Categories

| Category | Purpose | Directory |
|----------|---------|-----------|
| graphics | TUI, GPU, widgets, rendering | `graphics/` |
| web | HTTP, HTML, templates | `web/` |
| network | HTTP client, protocols | `network/` |
| data | Databases, data structures | `data/` |
| apps | Applications | `apps/` |
| util | Utilities, tools | `util/` |
| math | Linear algebra, units | `math/` |
| audio | Sound synthesis | `audio/` |
| testing | Test frameworks | `testing/` |

## Directory Structure

```
<category>/<project>/
├── lakefile.lean
├── README.md
├── CLAUDE.md
├── <Project>/
│   └── Basic.lean
├── <Project>.lean
└── Tests/
    └── Main.lean
```

## Template: lakefile.lean

```lean
import Lake
open Lake DSL

package «projectName» where
  leanOptions := #[
    ⟨`autoImplicit, false⟩
  ]

@[default_target]
lean_lib «ProjectName» where
  roots := #[`ProjectName]

require crucible from git "https://github.com/nathanial/crucible" @ "v0.0.1"

lean_exe tests where
  root := `Tests.Main

@[test_driver]
script test do
  let result ← IO.Process.run {
    cmd := ".lake/build/bin/tests"
    args := #[]
  }
  IO.println result
  return 0
```

## Template: Main Library (<Project>.lean)

```lean
import ProjectName.Basic
```

## Template: Basic.lean

```lean
namespace ProjectName

-- Your code here

end ProjectName
```

## Template: Tests/Main.lean

```lean
import Crucible
import ProjectName

open Crucible

def main : IO Unit := Crucible.runTests "ProjectName" do
  describe "Basic" do
    it "works" do
      assert true
```

## Template: CLAUDE.md

```markdown
# <Project Name>

Brief description.

## Build

\`\`\`bash
lake build && lake test
\`\`\`

## Usage

\`\`\`lean
import ProjectName
\`\`\`
```

## Naming Conventions

- Directory: lowercase with hyphens (e.g., `my-project`)
- Package: lowercase with hyphens in lakefile
- Library/namespace: PascalCase (e.g., `MyProject`)
- GitHub repo: matches directory name (except `chronos` → `chronos-lean`)

## After Creation

1. `lake build` to verify structure
2. `lake test` to run initial tests
3. `git init && git add -A && git commit -m "Initial commit"`
4. Create GitHub repo and push
5. Add to workspace CLAUDE.md project list

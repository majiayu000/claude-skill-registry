---
name: taskfiles
description: |
  Create, modify, and maintain Taskfiles following Task (https://taskfile.dev) best practices.

  Use when: (1) Creating new tasks or Taskfiles, (2) Modifying existing task definitions,
  (3) Adding new task includes, (4) Debugging task execution issues, (5) Questions about
  Taskfile syntax or patterns, (6) Running or understanding "task" commands,
  (7) Questions about available tasks or task namespaces.

  Triggers: "taskfile", "Taskfile.yaml", "task command", "task:", "create task",
  "add task", "task --list", "task tg:", "task inv:", "task wt:", ".taskfiles/",
  "how to run", "available tasks", "task syntax", "taskfile.dev"

  This skill covers the repository's specific conventions in .taskfiles/ and the root Taskfile.yaml.
---

# Taskfiles

## Repository Structure

```
Taskfile.yaml                    # Root: includes namespaced taskfiles
.taskfiles/
├── inventory/taskfile.yaml      # inv: IPMI host management
├── terragrunt/taskfile.yaml     # tg: Infrastructure operations
├── worktree/taskfile.yaml       # wt: Git worktree management
└── renovate/taskfile.yaml       # renovate: Config validation
```

## File Template

Always include schema and version:
```yaml
---
# yaml-language-server: $schema=https://taskfile.dev/schema.json
version: "3"

vars:
  MY_DIR: "{{.ROOT_DIR}}/path"

tasks:
  my-task:
    desc: Short description for --list output.
    cmds:
      - echo "hello"
```

## Required Patterns

### Include New Taskfiles
Add to root `Taskfile.yaml`:
```yaml
includes:
  namespace: .taskfiles/namespace
```

### Wildcard Tasks
Use for parameterized operations:
```yaml
plan-*:
  desc: Plans a specific terragrunt stack.
  vars:
    STACK: "{{index .MATCH 0}}"
  label: plan-{{.STACK}}          # Dynamic label for output
  cmds:
    - terragrunt plan --working-dir {{.INFRASTRUCTURE_DIR}}/stacks/{{.STACK}}
  preconditions:
    - which terragrunt
    - test -d "{{.INFRASTRUCTURE_DIR}}/stacks/{{.STACK}}"
```

### Dependencies and Formatting
Run dependencies before main task:
```yaml
apply-*:
  deps: [use, fmt]                # Run in parallel before cmds
  cmds:
    - terragrunt apply ...
```

### Internal Helper Tasks
Hide implementation details:
```yaml
ipmi-command:
  internal: true                  # Hidden from --list
  silent: true                    # Suppress command output
  requires:
    vars: [HOST, COMMAND]         # Validate required vars
  cmds:
    - ipmitool ... {{.COMMAND}}
```

### Preconditions
Validate before execution:
```yaml
preconditions:
  - which required-tool           # Tool must exist
  - test -d "{{.PATH}}"           # Directory must exist
  - sh: test "{{.VALUE}}" != ""
    msg: "VALUE cannot be empty"  # Custom error message
```

### Source Tracking
Skip unchanged tasks:
```yaml
fmt:
  sources:
    - "{{.DIR}}/**/*.tf"
  generates:
    - "{{.DIR}}/**/*.tf"          # Same files = format in place
  cmds:
    - tofu fmt -recursive
```

### Dynamic Variables from Files
Load from external sources:
```yaml
vars:
  VALID_HOSTS:
    sh: "cat {{.INVENTORY_FILE}} | yq -r '.hosts | keys[]'"
```

### For Loops
Iterate over lists:
```yaml
power-status:
  cmds:
    - for: { var: VALID_HOSTS }
      cmd: task inv:status-{{.ITEM}}
```

### CLI Arguments
Accept user input:
```yaml
new:
  requires:
    vars: [CLI_ARGS]              # Must provide argument
  vars:
    NAME: "{{.CLI_ARGS}}"
  cmds:
    - git worktree add ... -b "{{.NAME}}"
```

Usage: `task wt:new -- feature-branch`

## Style Rules

| Element | Convention | Example |
|---------|------------|---------|
| Variables | UPPERCASE | `STACK`, `ROOT_DIR` |
| Task names | kebab-case | `power-on-*`, `tofu-fmt` |
| Templates | No spaces | `{{.VAR}}` not `{{ .VAR }}` |
| Indentation | 2 spaces | Standard YAML |

## Common Operations

```bash
task --list              # Show available tasks
task tg:list             # List terragrunt stacks
task tg:plan-live        # Plan specific stack
task inv:power-on-node41 # IPMI power control
task wt:new -- branch    # Create worktree
```

## References

- [references/styleguide.md](references/styleguide.md) - Naming and formatting conventions
- [references/schema.md](references/schema.md) - Complete property reference
- [references/cli.md](references/cli.md) - CLI flags and options

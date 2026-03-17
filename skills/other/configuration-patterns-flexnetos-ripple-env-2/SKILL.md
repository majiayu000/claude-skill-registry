# Skills and Capabilities

## Environment Skills

### Nix Package Management
- Install/remove packages via `nix profile`
- Build derivations with `nix build`
- Enter development shells with `nix develop` / `nom develop`
- Check flake validity with `nix flake check`
- Update dependencies with `nix flake update`

### Pixi Package Management
- Add packages: `pixi add <package>`
- Remove packages: `pixi remove <package>`
- Search packages: `pixi search <pattern>`
- Update lockfile: `pixi update`
- Show environment: `pixi info`

### Shell Navigation
- Smart directory navigation with `zoxide` (`z <path>`)
- Fuzzy file finding with `fzf`
- File listing with `eza` (modern `ls`)
- File viewing with `bat` (modern `cat`)
- Ripgrep for fast searching (`rg <pattern>`)

## Development Skills

### ROS2 Development
- Build packages: `colcon build --symlink-install`
- Run tests: `colcon test`
- View results: `colcon test-result --verbose`
- Launch nodes: `ros2 launch <package> <launch_file>`
- Topic inspection: `ros2 topic list/echo/info`
- Service calls: `ros2 service call`
- Parameter management: `ros2 param`

### Git Operations
- Standard git workflow (add, commit, push, pull)
- GitHub CLI operations with `gh`
- PR creation: `gh pr create`
- Issue management: `gh issue`
- Workflow inspection: `gh run`

### Code Editing
- Helix editor with LSP support
- Language servers for: Python, C++, CMake, Nix, YAML, XML, Rust, Bash, TOML, Markdown
- Auto-completion, go-to-definition, hover docs
- Code formatting and linting

## Build Skills

### CMake Projects
- Configure: `cmake -B build -G Ninja`
- Build: `cmake --build build`
- Install: `cmake --install build`
- Test: `ctest --test-dir build`

### Python Projects
- Virtual environments via Pixi
- Package installation: `pixi add <package>`
- Running scripts: `pixi run python <script>`
- Testing: `pixi run pytest`

### C++ Projects
- Compilation with gcc/clang
- Debug builds with symbols
- Release optimization
- Static analysis with clang-tidy

### Rust Projects
- Package management with `cargo`
- Build: `cargo build` / `cargo build --release`
- Test: `cargo test`
- Format: `cargo fmt`
- Lint: `cargo clippy`
- LSP support via `rust-analyzer`

## AI/Inference Skills

### LocalAI (Local LLM Inference)
- OpenAI-compatible API server
- Start: `localai start`
- Stop: `localai stop`
- Check: `localai status`
- List models: `localai models`
- Default port: 8080

### AGiXT (AI Agent Platform)
- Docker-based agent automation
- Start: `agixt up`
- Stop: `agixt down`
- Logs: `agixt logs`
- Status: `agixt status`
- Shell: `agixt shell`
- API port: 7437, UI port: 3437

### AIOS (Agent Operating System)
- User-space agent kernel with syscalls
- Install: `aios install`
- Start: `aios start`
- Stop: `aios stop`
- Status: `aios status`
- Config: `aios config`
- Default port: 8000
- Pixi environment: `pixi run -e aios ...`

### Cerebrum (Agent SDK)
- SDK for building AIOS agents
- Install: `pip install aios-agent-sdk`
- Run agent: `run-agent --mode local --agent_path ./my_agent --task "..."`
- List agents: `list-agenthub-agents`
- Download agent: `download-agent`
- Upload agent: `upload-agents`

## DevOps Skills

### CI/CD
- GitHub Actions workflow creation
- Workflow debugging and monitoring
- Secret management
- Artifact handling

### Container Operations
- Build images with Docker/Podman
- Multi-stage builds
- Layer optimization
- Registry push/pull

### Infrastructure
- Nix-based system configuration
- Home-manager user configuration
- Cross-platform deployments
- Reproducible environments

## Automation Skills

### Shell Scripting
- Bash script creation and debugging
- Nushell for structured data
- PowerShell for Windows automation
- Cross-platform script patterns

### Task Automation
- File watching and triggers
- Scheduled tasks
- Event-driven automation
- Workflow orchestration

## Analysis Skills

### Code Analysis
- Static analysis with various linters
- Dependency scanning
- Security vulnerability detection
- Performance profiling

### Log Analysis
- Pattern matching with ripgrep
- Structured log parsing
- Error aggregation
- Trend detection

## Communication Skills

### Documentation
- Markdown formatting
- Code documentation
- API documentation
- User guides and tutorials

### Reporting
- Status summaries
- Progress reports
- Error explanations
- Recommendations

## Command Types

Commands are available from three sources - understand where they come from:

### Devshell Commands (flake.nix)
Available inside `nix develop` / `nom develop`:

| Command | Description | Definition |
|---------|-------------|------------|
| `cb` | `colcon build --symlink-install` | `flake.nix:219` |
| `ct` | `colcon test` | `flake.nix:222` |
| `ctr` | `colcon test-result --verbose` | `flake.nix:225` |
| `ros2-env` | Show ROS2 environment variables | `flake.nix:228` |
| `update-deps` | `pixi update` | `flake.nix:231` |
| `ai` | AI chat assistant (aichat) | `flake.nix:237` |
| `pair` | AI pair programming (aider) | `flake.nix:240` |
| `promptfoo` | LLM testing (npx wrapper) | `flake.nix:250` |
| `localai` | LocalAI server management | `flake.nix:256` |
| `agixt` | AGiXT Docker management | `flake.nix:293` |
| `aios` | AIOS Agent Kernel management | `flake.nix:340` |
| `vault-dev` | Vault dev server | `flake.nix:412` |

### Shell Aliases (modules/common/packages.nix)
Available in all shells via home-manager:

| Alias | Expands To |
|-------|------------|
| `gs` | `git status` |
| `ga` | `git add` |
| `gc` | `git commit` |
| `gp` | `git push` |
| `gl` | `git pull` |
| `gd` | `git diff` |
| `gco` | `git checkout` |
| `gb` | `git branch` |
| `glog` | `git log --oneline --graph --decorate` |
| `ls` | `eza` (modern ls) |
| `ll` | `eza -l` |
| `la` | `eza -la` |
| `lt` | `eza --tree` |
| `cat` | `bat` (syntax highlighting) |
| `grep` | `rg` (ripgrep) |
| `find` | `fd` (modern find) |
| `nrs` | `nom develop` |
| `nrb` | `nom build` |

### AI Assistant Aliases (modules/common/packages.nix)
Available in all shells via home-manager:

| Alias | Expands To |
|-------|------------|
| `ai` | `aichat` |
| `ai-code` | `aichat --role coder` |
| `ai-explain` | `aichat --role explain` |
| `ai-review` | `aichat --role reviewer` |
| `pair` | `aider` |
| `pair-voice` | `aider --voice` |
| `pair-watch` | `aider --watch` |

### Nix Commands (system-wide)
Available after Nix installation:

| Command | Description |
|---------|-------------|
| `nix develop` | Enter development shell |
| `nom develop` | Enter shell with progress UI |
| `nix flake check` | Validate flake |
| `nix flake update` | Update dependencies |
| `nix build .#output` | Build specific output |
| `nix profile install` | Install package |

## Tool Quick Reference

| Task | Command | Type |
|------|---------|------|
| Enter dev shell | `nom develop` | Nix |
| Build ROS packages | `cb` | Devshell |
| Run tests | `ct` | Devshell |
| Test results | `ctr` | Devshell |
| Add ROS package | `pixi add ros-humble-<name>` | Pixi |
| Search packages | `pixi search <pattern>` | Pixi |
| Check flake | `nix flake check` | Nix |
| Update deps | `update-deps` or `nix flake update` | Devshell/Nix |
| Show ROS env | `ros2-env` | Devshell |
| Git status | `gs` or `git status` | Alias/Git |
| Create PR | `gh pr create` | GitHub CLI |
| AI chat | `ai` or `aichat` | Devshell/Alias |
| AI code generation | `ai-code` | Alias |
| AI pair programming | `pair` or `aider` | Devshell/Alias |
| Start LocalAI | `localai start` | Devshell |
| Start AGiXT | `agixt up` | Devshell |
| Start AIOS | `aios start` | Devshell |
| Install AIOS | `aios install` | Devshell |
| Run AIOS agent | `pixi run -e aios run-agent ...` | Pixi/AIOS |
| Build Rust | `cargo build` | Rust |
| Test Rust | `cargo test` | Rust |

## Skill Expansion

New skills can be added by:

1. **Nix packages**: Add to `flake.nix` or `modules/common/packages.nix`
2. **Pixi packages**: Add via `pixi add <package>`
3. **Structured skills**: Add to `.claude/skills/<skill-name>/SKILL.md`
4. **Slash commands**: Add to `.claude/commands/<command>.md`
5. **Shell aliases**: Add to `modules/common/packages.nix` shellAliases
6. **Devshell commands**: Add to `flake.nix` devshells.default.commands
7. **Editor plugins**: Configure in `modules/common/editor/default.nix`

### Skill File Format

Skills use YAML frontmatter for agent discovery:

```markdown
---
name: skill-name
description: What this skill does
icon: 📦
category: development
tools:
  - tool1
  - tool2
---

# Skill Documentation
...
```

## Limitations

Current limitations to be aware of:

- GUI applications require display forwarding in WSL2
- Some ROS packages may not be available in RoboStack
- Hardware access (USB, serial) needs additional configuration
- GPU acceleration requires driver setup

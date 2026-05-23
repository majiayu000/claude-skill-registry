---
name: ai-assistants
description: AI-powered development tools configuration and usage
icon: 🤖
category: development
tools:
  - aichat
  - aider
  - ai
  - ai-code
  - ai-explain
  - ai-review
  - pair
  - pair-voice
  - pair-watch
  - localai
  - agixt
---

# AI Assistants

This environment includes AI-powered development tools to enhance your ROS2 development workflow.

## Access Methods

There are two ways to access AI tools in this environment:

| Method | Commands Available | Requires |
|--------|-------------------|----------|
| **Devshell** | `ai`, `pair` | `nom develop` or `direnv allow` |
| **Home-Manager** | All aliases (ai-code, pair-voice, etc.) | Module enablement |

**Note**: The devshell commands are always available when you enter the development environment. The extended aliases require home-manager module configuration.

## aichat - Foundation AI CLI

**aichat** is the default AI assistant - a tiny, provider-agnostic CLI that works with multiple AI providers.

### Supported Providers

| Provider | Model Examples | API Key Env Var |
|----------|---------------|-----------------|
| Anthropic | claude-3-opus, claude-3-sonnet | `ANTHROPIC_API_KEY` |
| OpenAI | gpt-4, gpt-4-turbo, gpt-3.5-turbo | `OPENAI_API_KEY` |
| Google | gemini-pro, gemini-1.5-pro | `GOOGLE_API_KEY` |
| Ollama | llama2, codellama, mistral | (local, no key) |
| Azure OpenAI | gpt-4, gpt-35-turbo | `AZURE_OPENAI_API_KEY` |

### Quick Start

```bash
# Set your API key (choose your provider)
export ANTHROPIC_API_KEY="your-key-here"
# or
export OPENAI_API_KEY="your-key-here"

# Basic usage
ai "explain what ROS2 topics are"

# Code assistance
ai-code "write a ROS2 publisher node in Python"

# Code review
ai-review "review this launch file for best practices"

# Explain code
cat src/my_node.py | ai-explain
```

### Available Aliases

| Alias | Command | Purpose |
|-------|---------|---------|
| `ai` | `aichat` | General AI chat |
| `ai-code` | `aichat --role coder` | Code generation |
| `ai-explain` | `aichat --role explain` | Code explanation |
| `ai-review` | `aichat --role reviewer` | Code review |

### Configuration

aichat stores configuration in `~/.config/aichat/config.yaml`:

```yaml
# Example configuration
model: claude                         # Short model name (aichat resolves to latest)
save: true
highlight: true
temperature: 0.7

# Custom roles
roles:
  - name: ros2-expert
    prompt: |
      You are a ROS2 expert. Help with:
      - Node development (Python/C++)
      - Launch files
      - Message/Service definitions
      - Best practices for robotics
```

**Note**: aichat uses short model names (e.g., `claude`, `gpt-4`, `gemini-pro`) and automatically resolves to the latest available version.

### Using with Ollama (Local Models)

For offline/private AI assistance:

```bash
# Install Ollama (if not already)
curl -fsSL https://ollama.com/install.sh | sh

# Pull a coding model
ollama pull codellama

# Use with aichat
aichat --model ollama:codellama "write a ROS2 subscriber"
```

### ROS2-Specific Usage

```bash
# Explain a ROS2 concept
ai "explain ROS2 QoS profiles"

# Generate a launch file
ai-code "create a launch file that starts a camera node and image processor"

# Debug an error
ai "why am I getting 'could not find package' in colcon build"

# Review code
cat src/robot_controller/robot_controller/controller.py | ai-review
```

### Tips

1. **Pipe code for context**: `cat file.py | ai "explain this"`
2. **Use roles for consistency**: `ai-code` for generation, `ai-review` for feedback
3. **Save sessions**: Use `aichat -s session-name` to continue conversations
4. **Local models**: Use Ollama for private/offline work

## Aider - AI Pair Programming

**Aider** is a Git-integrated AI pair programmer that edits code in your repo with automatic commits.

### Quick Start

```bash
# Start aider in current directory
pair

# Work on specific files
pair src/my_package/my_node.py

# Voice-to-code mode (requires portaudio)
pair-voice

# Watch mode - auto-commit on file changes
pair-watch

# Use specific model
aider --model claude-3-sonnet-20240229
aider --model gpt-4-turbo
```

### Key Features

| Feature | Description |
|---------|-------------|
| **Git Integration** | Auto-commits changes with descriptive messages |
| **Repo Mapping** | Understands your entire codebase structure |
| **Voice Mode** | Speak your coding requests |
| **Watch Mode** | Monitors files and auto-commits changes |
| **100+ Languages** | Python, C++, Rust, TypeScript, etc. |

### Available Aliases

| Alias | Command | Purpose |
|-------|---------|---------|
| `pair` | `aider` | Start AI pair programming |
| `pair-voice` | `aider --voice` | Voice-to-code mode |
| `pair-watch` | `aider --watch` | Auto-commit on changes |
| `pair-claude` | `aider --model claude-3-sonnet-20240229` | Use Claude |
| `pair-gpt4` | `aider --model gpt-4-turbo` | Use GPT-4 |

### ROS2-Specific Usage

```bash
# Edit a ROS2 node
pair src/my_robot/my_robot/controller.py
> "Add a service server that accepts velocity commands"

# Modify launch files
pair src/my_robot/launch/robot.launch.py
> "Add a parameter for robot_name"

# Update CMakeLists.txt
pair src/my_robot/CMakeLists.txt
> "Add the new action interface dependency"
```

### Configuration

Create `~/.aider.conf.yml`:

```yaml
# Default model
model: claude-3-sonnet-20240229

# Auto-commit settings
auto-commits: true
auto-lint: true

# Editor integration
edit-format: diff

# Voice settings (if using --voice)
voice-language: en

# Dark mode for terminal
dark-mode: true
```

### Environment Variables

```bash
# API keys (set in .envrc or shell profile)
export ANTHROPIC_API_KEY="sk-ant-..."  # For Claude
export OPENAI_API_KEY="sk-..."         # For GPT-4
export DEEPSEEK_API_KEY="..."          # For DeepSeek
```

### Voice Mode Requirements

Voice-to-code requires:
- `portaudio` (included in devshell)
- Microphone access
- API key for speech-to-text (uses provider's audio API)

## Environment Variables

Add to your shell profile or `.envrc`:

```bash
# Choose one provider
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."
export GOOGLE_API_KEY="..."

# Optional: Set default model
export AICHAT_MODEL="claude-3-sonnet-20240229"
```

## Home-Manager Configuration

If using home-manager, enable the AI modules to get all aliases:

```nix
{
  # Enable aichat with aliases (ai, ai-code, ai-explain, ai-review)
  programs.aichat = {
    enable = true;
    settings = {
      model = "claude";                 # Short model name
      save = true;
      highlight = true;
    };
  };

  # Enable aider with aliases (pair, pair-voice, pair-watch, pair-claude, pair-gpt4)
  programs.aider = {
    enable = true;
    settings = {
      model = "claude-3-sonnet-20240229";
      auto-commits = true;
      dark-mode = true;
    };
  };
}
```

**Module Locations**:
- `modules/common/ai/aichat.nix` - aichat configuration
- `modules/common/ai/aider.nix` - aider configuration
- `modules/common/ai/default.nix` - AI module aggregator

## LocalAI - Local LLM Inference

**LocalAI** provides an OpenAI-compatible API server for running LLMs locally. It's the recommended inference backend for this environment.

### Quick Start

```bash
# Start LocalAI server
localai start

# Check status
localai status

# List available models
localai models

# Stop server
localai stop
```

### Features

| Feature | Description |
|---------|-------------|
| **OpenAI API** | Drop-in replacement for OpenAI API |
| **P2P Federation** | Distributed inference across multiple machines |
| **Model Formats** | GGUF, GGML, Safetensors, HuggingFace |
| **GPU Support** | CUDA, ROCm, Metal acceleration |
| **No Internet** | Fully offline capable |

### Configuration

LocalAI uses the models directory at `~/.local/share/localai/models`.

```bash
# Set custom models path
export LOCALAI_MODELS_PATH="/path/to/models"

# Download a model (example)
curl -L "https://huggingface.co/TheBloke/Mistral-7B-v0.1-GGUF/resolve/main/mistral-7b-v0.1.Q4_K_M.gguf" \
  -o ~/.local/share/localai/models/mistral-7b.gguf
```

### Integration with Other Tools

```bash
# Use LocalAI with aichat
export OPENAI_API_BASE="http://localhost:8080/v1"
aichat --model local-model "Hello"

# Use LocalAI with aider
OPENAI_API_BASE=http://localhost:8080/v1 aider
```

### Port Configuration

| Port | Service |
|------|---------|
| 8080 | LocalAI API |

**Documentation**: See `docs/adr/adr-006-agixt-integration.md` for architecture decisions.

## AGiXT - AI Agent Platform

**AGiXT** is a powerful AI Agent Automation Platform that enables building and orchestrating complex AI workflows.

### Quick Start

```bash
# Ensure LocalAI is running first
localai start

# Start AGiXT services
agixt up

# Check service status
agixt status

# View logs
agixt logs

# Stop services
agixt down
```

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    AGiXT Stack                               │
├─────────────┬─────────────┬─────────────┬───────────────────┤
│  AGiXT API  │  AGiXT UI   │ PostgreSQL  │      MinIO        │
│   :7437     │   :3437     │   :5432     │    :9000/:9001    │
└──────┬──────┴──────┬──────┴──────┬──────┴─────────┬─────────┘
       │             │             │                │
       └─────────────┴─────────────┴────────────────┘
                            │
                    ┌───────┴───────┐
                    │   LocalAI     │
                    │    :8080      │
                    └───────────────┘
```

### Port Configuration

| Port | Service |
|------|---------|
| 7437 | AGiXT API |
| 3437 | AGiXT UI |
| 5432 | PostgreSQL |
| 9000 | MinIO API |
| 9001 | MinIO Console |
| 8080 | LocalAI (on host) |

### Environment Variables

```bash
# .env.agixt or exported
export AGIXT_URL="http://localhost:7437"
export AGIXT_API_KEY="agixt-dev-key"
export LOCALAI_URL="http://localhost:8080"
```

### Management Commands

```bash
# Full command reference
agixt up      # Start all services
agixt down    # Stop all services
agixt logs    # Follow logs
agixt status  # Show container status
agixt shell   # Shell into AGiXT container
```

### ROS2 Integration

The AGiXT Rust SDK bridge (`rust/agixt-bridge/`) enables ROS2 nodes to communicate with AGiXT:

```bash
# Build the bridge
cd rust/agixt-bridge
cargo build

# Run example
cargo run --example basic_chat
```

**Key files**:
- `rust/agixt-bridge/` - Rust SDK integration
- `docker-compose.agixt.yml` - Docker Compose configuration
- `.env.agixt.example` - Environment template
- `docs/adr/adr-006-agixt-integration.md` - Architecture decision record

## Related Skills

- [Distributed Systems](../distributed-systems/SKILL.md) - NATS, Temporal
- [Observability](../observability/SKILL.md) - Monitoring AI services
- [Rust Tooling](../rust-tooling/SKILL.md) - AGiXT Rust SDK development

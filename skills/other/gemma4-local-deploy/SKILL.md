---
name: gemma4-local-deploy
description: 在本机 Mac 或 Apple Silicon 上部署 Gemma 4 12B。本地安装/升级 llama.cpp，下载 GGUF 量化模型，用 llama-server 暴露 OpenAI-compatible API，或用 Ollama 暴露本地模型服务，配置 tmux 后台运行，验证健康检查、问答接口、资源占用和常见故障。当用户说部署 Gemma 4、Gemma 4 12B、本地大模型、llama-server、Ollama、GGUF、Mac 本地模型服务时使用。
allowed-tools: Bash, Read, WebSearch, WebFetch
metadata:
  argument-hint: "[模型量化/端口/是否后台运行]"
---

# Gemma 4 12B 本地部署

目标：把 `google/gemma-4-12B-it` 的 GGUF 版本部署成本机模型服务。默认用 `llama.cpp` / `llama-server` + Apple Metal + `Q4_K_M` + `tmux` 暴露 OpenAI-compatible API；用户明确要 Ollama 时，再走 Ollama 导入路径。

## 默认选择

- 模型仓库：`ggml-org/gemma-4-12B-it-GGUF`
- 默认量化：`Q4_K_M`
- 默认模型名：`gemma-4-12b-it`
- 默认端口：`127.0.0.1:8080`
- 默认上下文：`32768`
- 默认后台方式：`tmux` 会话 `gemma4-12b`
- 默认关闭 thinking：`--reasoning off`，避免 OpenAI API 的 `message.content` 为空
- Ollama 路径：只在用户明确要 Ollama、需要接 Ollama 生态，或询问 `ollama pull gemma4:12b` 时使用

如果用户明确要更高质量，优先建议 `Q6_K` 或 `Q8_0`；不要默认上 `bf16`，除非用户接受更大内存和更慢加载。

## 执行流程

### 1. 搜索并确认现状

先查已有安装、进程、端口和模型缓存，避免重复部署：

```bash
command -v llama-server || true
llama-server --version || true
tmux has-session -t gemma4-12b 2>/dev/null && tmux display-message -p -t gemma4-12b '#S #{pane_pid}' || true
lsof -nP -iTCP:8080 -sTCP:LISTEN || true
ls -lh "$HOME/Library/Caches/llama.cpp/"*gemma-4-12B-it*Q4_K_M*.gguf 2>/dev/null || true
```

On Mac, also record hardware:

```bash
system_profiler SPHardwareDataType | sed -n '1,30p'
df -h "$HOME"
```

### 2. Install or upgrade llama.cpp

Use Homebrew on macOS:

```bash
brew install llama.cpp
# If already installed, upgrade only this package when possible.
brew upgrade llama.cpp
llama-server --version
```

Gemma 4 GGUF requires a `llama.cpp` build that recognizes `general.architecture = gemma4`.
If loading fails with:

```text
unknown model architecture: 'gemma4'
```

then upgrade `llama.cpp` and retry. A verified good local build was `9430`; newer stable or HEAD is also acceptable.

### 3. Download/load the model

First-run download can be done by `llama-server -hf`:

```bash
llama-server \
  -hf ggml-org/gemma-4-12B-it-GGUF:Q4_K_M \
  --no-mmproj \
  --ctx-size 32768 \
  --gpu-layers 99 \
  --parallel 1 \
  --reasoning off \
  --host 127.0.0.1 \
  --port 8080 \
  --alias gemma-4-12b-it
```

After the model is cached, prefer starting with the local file path. Typical cache path:

```text
$HOME/Library/Caches/llama.cpp/ggml-org_gemma-4-12B-it-GGUF_gemma-4-12B-it-Q4_K_M.gguf
```

### 4. Run persistently with tmux

If port `8080` is free and no `gemma4-12b` session exists:

```bash
tmux new-session -d -s gemma4-12b 'llama-server -m "$HOME/Library/Caches/llama.cpp/ggml-org_gemma-4-12B-it-GGUF_gemma-4-12B-it-Q4_K_M.gguf" --ctx-size 32768 --gpu-layers 99 --parallel 1 --reasoning off --host 127.0.0.1 --port 8080 --alias gemma-4-12b-it'
```

If `$HOME` is not expanded inside single quotes in the target shell, use the absolute path instead.

Management commands:

```bash
tmux attach -t gemma4-12b
tmux kill-session -t gemma4-12b
```

### 5. Verify before claiming success

Run all three checks from the current session:

```bash
curl -fsS http://127.0.0.1:8080/health
curl -fsS http://127.0.0.1:8080/v1/models
curl -fsS http://127.0.0.1:8080/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"gemma-4-12b-it","messages":[{"role":"user","content":"用一句中文回答：现在可以问你问题吗？"}],"max_tokens":80,"temperature":0.2}'
```

Success requires:

- `/health` returns `{"status":"ok"}`
- `/v1/models` lists `gemma-4-12b-it`
- chat response has non-empty `choices[0].message.content`

### 6. Report resource usage

Use both process and macOS footprint views:

```bash
pid=$(pgrep -f 'llama-server .*gemma-4-12B-it-Q4_K_M.gguf' | head -1)
ps -p "$pid" -o pid,stat,%cpu,%mem,rss,vsz,etime,command
footprint -p "$pid" -summary 2>/dev/null | sed -n '1,80p'
memory_pressure | sed -n '1,20p'
```

Explain the difference clearly:

- GGUF `Q4_K_M` is a quantized model; its file is about 7GB, not 24GB full precision.
- `ps` RSS includes mapped model pages and often shows around 9-11GB for Q4 12B.
- `footprint` may show lower physical pressure because clean mmap pages can be discarded and reread.
- Apple Silicon uses unified memory; GPU work does not appear as a separate NVIDIA-style VRAM number.

### 7. Optional: Ollama route

Use this path only when the user asks for Ollama. Treat official Ollama registry state as live-changing: re-test before claiming support.

Install and start Ollama:

```bash
brew install ollama
ollama --version
lsof -nP -iTCP:11434 -sTCP:LISTEN || true
tmux new-session -d -s ollama-gemma4 'OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve'
curl -fsS http://127.0.0.1:11434/api/version
```

First try the official path:

```bash
ollama pull gemma4:12b
```

If it succeeds, run:

```bash
ollama run gemma4:12b "用一句中文回答：现在可以问你问题吗？"
```

If it fails with `pull model manifest: file does not exist`, fall back to GGUF import. Download or reuse a local GGUF:

```bash
mkdir -p "$HOME/Models/gemma4-12b"
huggingface-cli download ggml-org/gemma-4-12B-it-GGUF \
  gemma-4-12B-it-Q4_K_M.gguf \
  --local-dir "$HOME/Models/gemma4-12b"
```

Create a Modelfile:

```bash
cat > "$HOME/Models/gemma4-12b/Modelfile" <<EOF
FROM $HOME/Models/gemma4-12b/gemma-4-12B-it-Q4_K_M.gguf
EOF
```

Homebrew `ollama` builds may lack sidecar `llama-server` / `llama-quantize` binaries. If `ollama create` or `ollama run` reports either binary missing, create a stable working directory with symlinks to `llama.cpp`:

```bash
mkdir -p "$HOME/ollama-gemma4/build/lib/ollama"
ln -sf /opt/homebrew/bin/llama-server "$HOME/ollama-gemma4/build/lib/ollama/llama-server"
ln -sf /opt/homebrew/bin/llama-quantize "$HOME/ollama-gemma4/build/lib/ollama/llama-quantize"
tmux kill-session -t ollama-gemma4 2>/dev/null || true
tmux new-session -d -s ollama-gemma4 "cd '$HOME/ollama-gemma4' && OLLAMA_FLASH_ATTENTION=1 OLLAMA_KV_CACHE_TYPE=q8_0 ollama serve"
```

Import and run:

```bash
ollama create gemma4-12b-gguf-local -f "$HOME/Models/gemma4-12b/Modelfile"
ollama list
ollama run gemma4-12b-gguf-local "用一句中文回答：Ollama 能跑 Gemma 4 12B 吗？"
```

For Ollama success, report whether it was:

- official registry pull: `ollama pull gemma4:12b`
- manual GGUF import: `ollama create gemma4-12b-gguf-local`
- workaround needed: sidecar symlinks to `llama.cpp`

## Troubleshooting

| Symptom | Fix |
|---|---|
| `unknown model architecture: 'gemma4'` | Upgrade `llama.cpp`; old builds do not support Gemma 4 GGUF. |
| Port 8080 busy | Show the listener with `lsof`; either stop it or choose another port. |
| Chat `content` is empty and only reasoning appears | Restart with `--reasoning off`. |
| First-run `-hf` hangs or repeats metadata resolution | Use the cached local GGUF path with `-m`. |
| `ollama pull gemma4:12b` returns `pull model manifest: file does not exist` | Official registry tag is not ready or is temporarily inconsistent; use manual GGUF import. |
| Ollama reports `llama-server binary not found` or `llama-quantize binary not found` | Symlink those binaries from `llama.cpp` into the Ollama working directory and start `ollama serve` from there. |
| User wants image/multimodal | Remove `--no-mmproj` only after testing `mmproj`; text-only deployment is the stable default. |
| Memory too high | Lower context, use `Q4_K_M`, or reduce `--parallel` to `1`. |

## Final response shape

Answer in Chinese unless the user asks otherwise. Include:

- endpoint URL
- model id
- tmux/session management commands
- verification results from this session
- resource summary and any caveats

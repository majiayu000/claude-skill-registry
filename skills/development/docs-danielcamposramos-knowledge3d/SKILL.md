---
name: docs-danielcamposramos-knowledge3d
description: LLM Skill (Integrated, RAG‑First)
---

LLM Skill (Integrated, RAG‑First)

Goal
- Provide a first‑class LLM ability inside K3D without huge weights. It answers with grounding from the House memory (RAG) and runs in‑process.

Backends
- Transformers (HF local): set `K3D_LLM_MODEL=/path/to/model`, runs CPU/GPU depending on availability. Suggested small chat models: TinyLlama‑1.1B‑Chat.
- llama.cpp (GGUF, in‑process): load `.gguf` via `llama-cpp-python`. Good for EXAONE‑Deep 2.4B/7.8B Q4_K_M.

Commands (in chat)
- `/llm backend transformers <model>` — set local HF model path or repo id.
- `/llm backend llama_cpp <model.gguf> [n_gpu_layers] [n_ctx]` — load GGUF directly (no servers). Example: `/llm backend llama_cpp /models/EXAONE-Deep-7.8B.Q4_K_M.gguf 30 2048`
- `/llm ask <text>` — direct LLM generation.
- `/llm rag <text> [k]` — RAG: retrieves top‑k labels via TF‑IDF from the current House and injects as context to the LLM.

RAG Source
- Live server builds TF‑IDF from labels and the viewer’s `dataset_snippets` (label+text). Future: richer multimodal grounding with CLIP/CLAP.

Notes
- RPN still gates actions. The LLM is a skill within the Cranium, not a replacement for policy.
- GGUF notes: `pip install llama-cpp-python` (CPU). For CUDA, follow upstream build instructions. On RTX 3060 12 GB, 7.8B Q4_K_M works with partial GPU offload (e.g., n_gpu_layers≈30) and ctx≈2048.

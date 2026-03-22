---
id: "e30ea4d8-7921-4f14-9145-fdba7f8a8af9"
name: "py / 14 / 15"
description: "General SOP for common requests related to py, 14, 15."
version: "0.1.0"
tags:
  - "py"
  - "14"
  - "15"
triggers:
  - "Use when the user asks for a process or checklist."
  - "Use when you want to reuse a previously mentioned method/SOP."
examples:
  - input: "Break this into best-practice, executable steps."
---

# py / 14 / 15

General SOP for common requests related to py, 14, 15.

## Prompt

Follow this SOP (replace specifics with placeholders like <PROJECT>/<ENV>/<VERSION>):
1) RuntimeError: CUDA driver error: invalid argument
2) 路径：`vllm/distributed/device_communicators/symm_mem.py
3) torch_symm_mem.rendezvous
4) 这类报错通常是 **“驱动/硬件/拓扑/权限不满足 symmetric memory 要求”** 导致的，而不是模型权重或dtype的问题
5) 下面给你一个“最可能原因
6) 验证方法
7) 解决办法”的梳理
8) 1）最可能原因：GPU/驱动不支持（或不完全支持）PyTorch symmetric memory / NVSHMEM 类能力
9) vLLM 0.11.0 默认可能会启用一种更激进的 GPU 通信（`SymmMemCommunicator`），它依赖 PyTorch 里 `_symmetric_memory` 的能力；而这个能力对以下条件很敏感
10) GPU 架构**（例如部分非 H100/非新架构可能不支持或支持不完善

For each step, include: action, checks, and failure rollback/fallback plan.
Output format: for each step number, provide status/result and what to do next.

## Triggers

- Use when the user asks for a process or checklist.
- Use when you want to reuse a previously mentioned method/SOP.

## Examples

### Example 1

Input:

  Break this into best-practice, executable steps.

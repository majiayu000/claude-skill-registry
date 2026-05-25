---
name: gpu-use
description: 查看远程服务器 GPU 使用情况。SSH 连接服务器，展示每张卡的显存占用、运行进程、所属容器。当用户说查看 GPU、显卡占用、显存使用时使用
allowed-tools: Bash
metadata:
  argument-hint: '[user@host -p port] 或无参数使用默认服务器'
---

# GPU 使用情况诊断

你是一个 GPU 资源管理专家，帮助用户快速了解远程服务器上的 GPU 使用情况。

## 服务器列表

| 别名 | SSH 命令 |
|------|----------|
| 默认 | `ssh felix@124.158.103.16 -p 10022` |

用户可以传入自定义 SSH 地址，格式：`user@host -p port`。无参数时使用默认服务器。

## 诊断流程

### 第一步：采集数据

**并行执行以下命令（通过 SSH）：**

1. **GPU 卡概况**
```bash
ssh {SSH_TARGET} "nvidia-smi --query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits"
```

2. **GPU 上运行的进程**
```bash
ssh {SSH_TARGET} "nvidia-smi --query-compute-apps=pid,gpu_uuid,used_memory,name --format=csv,noheader,nounits"
```

3. **GPU UUID 到 index 的映射**
```bash
ssh {SSH_TARGET} "nvidia-smi --query-gpu=index,gpu_uuid --format=csv,noheader"
```

4. **Docker 容器列表**
```bash
ssh {SSH_TARGET} "docker ps --format '{{.ID}} {{.Names}}' 2>/dev/null"
```

5. **进程 PID 到容器的映射**（用采集到的 PID 列表）
```bash
ssh {SSH_TARGET} "for cid in \$(docker ps -q); do name=\$(docker inspect --format '{{.Name}}' \$cid | sed 's/^\///'); pids=\$(docker top \$cid -o pid 2>/dev/null | tail -n +2); for p in \$pids; do echo \"\$p \$name\"; done; done 2>/dev/null"
```

6. **容器内多实例 http_server 检测**（识别单容器多终端部署）
```bash
ssh {SSH_TARGET} "for cid in \$(docker ps -q); do name=\$(docker inspect --format '{{.Name}}' \$cid | sed 's/^\///'); servers=\$(docker exec \$cid ps aux 2>/dev/null | grep 'http_server -p' | grep -v grep | awk '{for(i=1;i<=NF;i++) if(\$i==\"-p\") print \$(i+1)}'); if [ -n \"\$servers\" ]; then echo \"\$name: \$servers\"; fi; done 2>/dev/null"
```

### 第二步：生成报告

将 GPU UUID 映射回 index，将 PID 映射回容器名，按以下格式输出：

```
## GPU 使用概况

| GPU | 型号 | 显存占用 | 空闲 | GPU 利用率 | 状态 |
|-----|------|----------|------|------------|------|
| 0 | H200 | 107 / 141 GB | 34 GB | 85% | 🔴 繁忙 |
| 1 | H200 | 12 / 141 GB | 129 GB | 10% | 🟢 空闲 |
| 2 | H200 | 0 / 141 GB | 141 GB | 0% | ⚪ 无任务 |

## 进程详情

| GPU | 显存占用 | 容器 | 进程 |
|-----|----------|------|------|
| 0 | 107 GB | vllm_qwen35 | VLLM::EngineCore |
| 0 | 2 GB | truetranslate-api-bin | truetranslate_api.bin |
| 1 | 12 GB | atlas_video | python |

## 多实例服务（单容器多终端部署）

如果检测到容器内运行多个 http_server 实例，单独列出：

| 容器 | 端口 | GPU | 状态 |
|------|------|-----|------|
| atlas_video | :5001 | GPU 2 | 运行中 |
| atlas_video | :5002 | GPU 3 | 运行中 |

## 空闲资源

可用于新服务部署的 GPU：
- GPU 4: 141 GB 完全空闲
- GPU 5: 141 GB 完全空闲
```

### 状态判定规则

| 显存占用比 | GPU 利用率 | 状态 |
|------------|------------|------|
| 0% | 0% | ⚪ 无任务 |
| < 30% | < 30% | 🟢 空闲 |
| 30-80% | any | 🟡 中等 |
| > 80% | any | 🔴 繁忙 |

### 多实例检测逻辑

当检测到一个容器内有多个 `http_server -p` 进程时：
1. 提取每个进程的端口号（`-p` 参数）
2. 通过进程的 `CUDA_VISIBLE_DEVICES` 环境变量识别绑定的 GPU：
   ```bash
   ssh {SSH_TARGET} "docker exec {CONTAINER} cat /proc/{PID}/environ 2>/dev/null | tr '\0' '\n' | grep CUDA_VISIBLE_DEVICES"
   ```
3. 在报告中用独立表格展示，标注各实例的端口、GPU 绑定和运行状态

## 注意事项

- 用中文输出
- SSH 命令设置 15 秒超时
- 如果 SSH 连接失败，提示用户检查网络和 SSH 配置
- 不执行任何写操作，纯只读诊断
- 单容器多终端是 atlas_video 的标准部署方式，注意区分容器级和进程级的 GPU 占用

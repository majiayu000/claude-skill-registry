---
name: sandbox-service
description: 安全隔离的 Docker 沙盒代码执行服务。支持 Python/Shell/Bash 多语言动态执行，内置超时与资源限制。提供信任模式用于服务间代码融合调用。
---

## 功能
安全的代码执行沙盒服务，能够：
1. 在隔离的 Docker 容器中执行代码
2. 支持 Python、Shell、Bash 多种语言
3. 自动超时控制和资源限制
4. 执行后自动销毁容器，无状态残留

## 适用场景
- Agent 需要执行代码验证结果
- 运行用户提供的代码片段
- 数据处理和计算任务
- 脚本执行和自动化

## 安全限制
- 网络隔离：`--network none`
- 内存限制：256MB
- CPU 限制：1 核
- 执行时间：最长 60 秒
- 用户权限：非 root (nobody)
- 文件系统：只读

## 调用方式
```python
from services.sandbox_service.client import SandboxClient

client = SandboxClient()

# 健康检查
status = client.health_check()

# 执行 Python 代码
result = client.execute("print(1+1)", language="python")

# 执行 Shell 命令
result = client.execute("echo Hello && date", language="shell")

# 自定义超时（秒）
result = client.execute(
    code="import time; time.sleep(5)",
    language="python",
    timeout=10
)

# 传递环境变量
result = client.execute(
    code="import os; print(os.environ.get('MY_VAR'))",
    language="python",
    env_vars={"MY_VAR": "hello"}
)

# 检查执行结果
if result["success"]:
    print(f"输出: {result['stdout']}")
else:
    print(f"错误: {result['stderr']}")
```

## 信任模式（代码融合）

使用 `trusted_mode=True` 可以在代码中调用其他服务：

```python
# 信任模式：允许访问 services 和网络
result = client.execute(
    code='''
from services.embedding_service.client import EmbeddingServiceClient
from services.rerank_service.client import RerankServiceClient

# 获取 embedding
embed_client = EmbeddingServiceClient()
vec1 = embed_client.embed_query("人工智能")
vec2 = embed_client.embed_query("机器学习")

# 计算相似度
import math
dot = sum(a*b for a,b in zip(vec1, vec2))
norm1 = math.sqrt(sum(a*a for a in vec1))
norm2 = math.sqrt(sum(b*b for b in vec2))
similarity = dot / (norm1 * norm2)

print(f"相似度: {similarity:.4f}")
''',
    language="python",
    trusted_mode=True  # 开启信任模式
)
```

**信任模式注意事项：**
- 允许访问 myagent_network 网络
- 可以调用其他服务的 Python 客户端
- 适合 Agent 代码融合场景
- 仍有内存和 CPU 限制


## 返回格式
```json
{
  "success": true,
  "stdout": "2\n",
  "stderr": "",
  "exit_code": 0,
  "execution_time": 1.058,
  "error": null
}
```

## 错误处理
```json
{
  "success": false,
  "stdout": "",
  "stderr": "执行超时（3秒）",
  "exit_code": -1,
  "execution_time": 3.05,
  "error": "Execution timeout"
}
```

## 支持的语言

| 语言 | 标识 | 基础镜像 |
|------|------|----------|
| Python | `python`, `python3`, `py` | `python:3.10-slim` |
| Shell | `shell`, `sh` | `alpine:latest` |
| Bash | `bash` | `bash:latest` |

---
name: docker_ops
description: "**Docker 底层操作接口**。直接管理容器、网络和文件。通常由 `deployment_manager` 调用，也可用于简单的容器管理。"
triggers:
- docker
- 容器
- container
- remove
- delete
- 删除
- 移除
---

# Docker Ops (容器运维)

你是一个 Docker 运维与执行工具。

## 核心能力

1.  **管理容器**: 停止、删除、查看容器。
2.  **执行命令**: 在宿主机执行 Docker 相关命令。
3.  **Compose 操作**: 在指定目录执行 docker compose up/down。

## 执行指令 (SOP)

### 参数说明

| 参数名 | 类型 | 必填 | 说明 |
| :--- | :--- | :--- | :--- |
| `action` | string | 是 | 操作类型 (见下表) |
| `name` | string | 条件 | 容器或项目名称 (stop/remove) |
| `cwd` | string | 条件 | 工作目录 (compose_up/compose_down/execute_command) |
| `command` | string | 条件 | Shell 命令 (execute_command) |
| `path` | string | 条件 | 文件路径 (edit_file) |
| `content` | string | 条件 | 文件内容 (edit_file) |
| `is_compose` | boolean | 否 | 是否为 compose 项目 (stop/remove) |
| `remove` | boolean | 否 | 是否删除容器 (stop) |
| `clean_volumes` | boolean | 否 | 是否清理卷 (stop + remove) |
| `build` | boolean | 否 | 是否 build (compose_up，默认 true) |
| `detach` | boolean | 否 | 是否后台运行 (compose_up，默认 true) |
| `volumes` | boolean | 否 | 是否删除卷 (compose_down，默认 false) |

### 可用 Action

| Action | 说明 |
| :--- | :--- |
| `list_services` | 列出运行中的服务 |
| `list_networks` | 列出网络 |
| `stop` | 停止/删除容器或项目 |
| `compose_up` | 在指定目录执行 `docker compose up -d --build` |
| `compose_down` | 在指定目录执行 `docker compose down` |
| `execute_command` | 执行 Shell 命令 (受限安全列表) |
| `edit_file` | 编辑文件 (docker-compose.yml) |

### 意图映射示例

**1. 列出容器**
- 用户输入: "查看运行中的容器"
- 提取参数:
  ```json
  { "action": "list_services" }
  ```

**2. 在目录执行 compose up**
- 用户输入: "在 uptime-kuma 项目目录启动服务"
- 提取参数:
  ```json
  { "action": "compose_up", "cwd": "/path/to/uptime-kuma" }
  ```

**注意**: `cwd` 应使用实际的宿主机绝对路径（由 `deployment_manager` 的 `clone` action 返回）。

**3. 停止并删除容器**
- 用户输入: "删除 caddy 容器"
- 提取参数:
  ```json
  { "action": "stop", "name": "caddy", "remove": true }
  ```

**4. 执行命令**
- 用户输入: "在宿主机执行 docker ps"
- 提取参数:
  ```json
  { "action": "execute_command", "command": "docker ps" }
  ```

**5. 在特定目录执行命令**
- 用户输入: "在 myapp 项目目录执行 docker compose logs"
- 提取参数:
  ```json
  { "action": "execute_command", "command": "docker compose logs --tail 50", "cwd": "/path/to/myapp" }
  ```

## 安全限制

允许执行的命令白名单：`docker`, `curl`, `netstat`, `ss`, `grep`, `cat`, `ls`, `pwd`, `sed`, `awk`, `head`, `tail`

以下操作被禁止：
- `docker inspect` (可能泄露环境变量)
- 读取 `.env`、`secret`、`password` 等敏感文件

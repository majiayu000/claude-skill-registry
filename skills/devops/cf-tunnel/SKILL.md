---
name: cf-tunnel
description: Cloudflare Tunnel 一键管理工具，支持统一 Bun CLI（share + panel 合并）、端口自动避让、状态检查与自解释文档
---

# Cloudflare Tunnel 管理技能（统一版）

目标：把“临时暴露 + 管理面板 + 端口管理”统一到一个命令入口，避免端口混乱。

## ✅ 推荐入口（统一 Bun CLI）

```bash
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts
```

### 命令总览

```bash
# 启动临时暴露（等同 share start）
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts start --dir ./demos/html

# 暴露已有端口
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts start --port 8766

# 暴露单文件
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts start --file ./demos/html/index.html --route /index.html

# 启动/停止/查看面板
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts panel start --port 8788 --host 127.0.0.1
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts panel status
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts panel stop

# 综合状态（share + panel）
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts status

# 停止（默认全停）
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts stop
# 只停 share
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts stop --share
# 只停 panel
bun ~/.pi/agent/skills/cf-tunnel/scripts/cf.ts stop --panel
```

---

## 功能特性

- 统一入口：`cf.ts` 同时管理 share / panel
- 端口自动避让：面板端口占用时自动切换到下一个可用端口
- 会话清晰：固定 tmux session 名
  - `cf-share-web`
  - `cf-share-tunnel`
  - `cf-share-panel`
- 状态聚合：一个命令看完整状态（本地服务 / tunnel / panel / 公网 URL）
- 向后兼容：`share.ts`、`panel.ts` 仍可直接使用

---

## 底层命令（兼容保留）

```bash
# share 底层
bun ~/.pi/agent/skills/cf-tunnel/scripts/share.ts start --dir ./demos/html
bun ~/.pi/agent/skills/cf-tunnel/scripts/share.ts status
bun ~/.pi/agent/skills/cf-tunnel/scripts/share.ts stop

# panel 底层
bun ~/.pi/agent/skills/cf-tunnel/scripts/panel.ts --port 8788 --host 127.0.0.1
```

> 建议优先使用 `cf.ts`，底层命令主要用于调试。

---

## API 与面板

启动面板后默认地址：

- `http://127.0.0.1:8788`（若占用会自动避让）

API：

- `GET /api/status` 当前状态
- `POST /api/start` 启动（body 支持 `port/dir/file/route`）
- `POST /api/stop` 停止
- `GET /api/logs` 日志 tail
- `GET /api/history` 历史记录
- `POST /api/history/clear` 清空历史

---

## 依赖

```bash
# Cloudflared（如未安装）
wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
sudo dpkg -i cloudflared-linux-amd64.deb
```

本地静态服务优先级：`python3 > bunx > npx`（无可用工具时直接失败）

---

## 故障排查

1. `cf.ts status` 先看三类会话是否在线
2. 如果 tunnel 无 URL：检查 `~/.cf-tunnel/share-tunnel.log`
3. 如果 panel 打不开：`cf.ts panel status` 看实际端口（可能已自动避让）
4. 彻底重置：`cf.ts stop --all` 后重新 `start`

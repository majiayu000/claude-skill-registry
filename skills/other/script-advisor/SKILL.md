---
name: script-advisor
description: "脚本工程化执行器。四层架构：原子→组合→Agent→配置。AI执行任务时优先使用脚本。"
---

# Script Advisor - 四层脚本执行

## 核心原则

**"先正常使用，token高了再用脚本"** - 智能辅助，非强制

### 四层架构

| 层级 | 类型 | Token | 示例 |
|------|------|-------|------|
| Layer 1 | 原子脚本 | 零 | `check_disk.sh` |
| Layer 2 | 组合脚本 | 低 | `deploy.sh` |
| Layer 3 | Agent接口 | 极低 | `--brief` 模式 |
| Layer 4 | 配置即代码 | 零 | `env/prod.json` |

### 决策阈值

| 条件 | 动作 |
|------|------|
| 单次 >500 token | 考虑脚本 |
| 累计 >2000 token | 积极脚本 |
| 重复 >3 次 | 必须脚本 |
| 文件操作 | 用 kimi-bridge |

---

## Kimi Bridge（文件操作首选）

```bash
kimi-bridge.sh analyze "统计ERROR" /var/log
kimi-bridge.sh edit --dry-run "修复bug" /project file.py
kimi-bridge.sh search "查找TODO" /project
kimi-bridge.sh batch --dry-run "重命名" /logs
```

| 任务 | 方案 |
|------|------|
| 分析文件 | `kimi-bridge.sh analyze` |
| 编辑文件 | `kimi-bridge.sh edit` |
| 搜索内容 | `kimi-bridge.sh search` |
| 批量操作 | `kimi-bridge.sh batch` |
| 系统操作 | 传统 Layer 1/2 |

---

## 脚本目录

```
scripts/
├── core/        # 核心系统（备份、配置）
├── monitor/     # 监控告警
├── gateway/     # Gateway管理
├── autonomous/  # 自主系统
├── ai/          # AI管理
├── document/    # 文档生命周期
├── task/        # 任务管理
├── test/        # 测试脚本
├── utils/       # 工具函数
└── registry.json
```

## 高频脚本

| 任务 | 脚本 |
|------|------|
| 系统状态 | `monitor/check-all-channels.sh --brief` |
| 配置备份 | `core/config-backup.sh --brief` |
| **安全编辑配置** | `core/openclaw-config-edit.sh "sed -i 's/old/new/' file"` |
| Gateway | `gateway/gateway-manage.sh --brief status` |
| 文件分析 | `utils/kimi-bridge.sh analyze --brief` |
| 文件编辑 | `utils/kimi-bridge.sh edit --brief` |

### 安全编辑配置（新）

修改重要配置文件时**必须**使用安全编辑工具：

```bash
# OpenClaw 配置专用
./scripts/core/openclaw-config-edit.sh \
  "sed -i 's/\"ask\": \"never\"/\"ask\": \"off\"/' ~/.openclaw/openclaw.json"

# 通用安全编辑（任何重要文件）
./scripts/core/safe-edit.sh ~/.openclaw/openclaw.json \
  "python3 fix-config.py" \
  "python3 -m json.tool ~/.openclaw/openclaw.json > /dev/null"
```

**流程**：自动备份 → 执行修改 → 验证 →（失败自动回滚）

## 禁止行为

- ❌ 直接 `openclaw status` → 用 `check-all-channels.sh`
- ❌ 直接 `cat config` → 用 `wecom-config.sh`
- ❌ 重复实现已有功能
- ❌ 问"要不要用脚本"→ 直接用

---

详细模板见 [references/](references/)

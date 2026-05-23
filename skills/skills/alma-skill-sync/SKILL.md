---
name: alma-skill-sync
description: 用于同步 Alma 技能到斜杠命令（Prompts）列表。当用户新增技能、修改技能名称或需要清理无效的快捷指令时使用。
---

# Alma Skill Sync

该技能负责将存储在 `~/.claude/skills/` 目录下的技能同步到 Alma 的斜杠命令（/）列表中，使用户可以通过输入 `/技能名` 快速调用。

## 使用场景

1. **新增技能后**：当你创建了新的技能，希望在输入框输入 `/` 就能看到它。
2. **清理无效指令**：当你删除了某些技能，希望对应的斜杠命令也一并消失。
3. **状态检查**：列出当前的同步状态。

## 工作流程

### 1. 同步技能 (Sync)

运行同步脚本，将所有现有的技能注册为 Alma 的 Prompts。

```bash
python3 /Users/douba/.claude/skills/alma-skill-sync/scripts/sync_to_alma.py
```

### 2. 清理模式 (Clean Sync)

运行同步脚本并开启清理模式，这会移除那些在技能目录中已不存在但仍在 Alma Prompt 列表中的快捷指令。

```bash
python3 /Users/douba/.claude/skills/alma-skill-sync/scripts/sync_to_alma.py --clean
```

## 注意事项

- **API 依赖**：该技能依赖于 Alma 在 `localhost:23001` 提供的 REST API。
- **匹配规则**：快捷指令的名称将与技能 `SKILL.md` 中定义的 `name` 字段严格一致。
- **触发机制**：生成的快捷指令内容为 `@技能名`，这会利用 Alma 的原生语义引擎激活对应的技能。

## 资源说明

- **脚本位置**：`/Users/douba/.claude/skills/alma-skill-sync/scripts/sync_to_alma.py`
- **参考资料**：`/Users/douba/.claude/skills/alma-skill-sync/references/api_reference.md` 包含了 Alma 的 API 规范。

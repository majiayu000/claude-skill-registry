# 删除/废弃 SKILL

> **目标**：安全地移除一个 SKILL（推荐废弃而非直接删除）
>
> **完成后**：必须执行 [SYNC_INDEX.md](./SYNC_INDEX.md) 同步索引

---

## 方式一：废弃（推荐）

保留文件但标记为不推荐使用，便于历史追溯。

### Step 1: 更新 SKILL.md frontmatter

```yaml
---
name: old-skill
description: 原有描述...
deprecated: true
deprecated_by: new-skill-name    # 替代方案（如有）
deprecated_reason: "功能已合并"  # 可选
---
```

### Step 2: 添加废弃警告

在正文顶部添加：

```markdown
> **已废弃**：此 SKILL 已被 [new-skill-name](../path/to/new-skill/SKILL.md) 替代。
> 请使用新版本。
```

### Step 3: 更新索引

执行 [SYNC_INDEX.md](./SYNC_INDEX.md)。

两种处理方式：

**A. 保留但标记废弃**（推荐）：
```markdown
| old-skill | ~~原有描述~~ (已废弃 → new-skill) | `old-skill/SKILL.md` |
```

**B. 直接从索引移除**

---

## 方式二：直接删除

适用于确定不再需要的 SKILL。

### Step 1: 更新索引

**先更新索引**，再删除文件：

执行 [SYNC_INDEX.md](./SYNC_INDEX.md)，从以下文件移除条目：
- 底层索引：`{category}/_INDEX.md`
- 上层索引：`_INDEX_STAGE_*.md`
- 全局索引：`_INDEX_ALL.md`

### Step 2: 删除目录

```bash
rm -rf spec_stage_skill/{category}/old-skill/
```

### Step 3: 验证

执行 [VALIDATE_SKILL_AND_INDEX.md](./VALIDATE_SKILL_AND_INDEX.md) 确认没有悬空引用。

---

## 方式三：归档

保留历史记录但从活跃目录移除。

```bash
# 创建归档目录
mkdir -p _archive/skill/

# 固定时间戳（避免跨午夜）
ARCHIVE_DATE=$(date +%Y%m%d)
ARCHIVE_DATE_DISPLAY=$(date +%Y-%m-%d)

# 移动废弃的 SKILL
mv spec_stage_skill/{category}/old-skill/ \
   _archive/skill/old-skill_${ARCHIVE_DATE}/

# 添加归档说明
echo "归档于 ${ARCHIVE_DATE_DISPLAY}，原因：功能已合并" \
  > _archive/skill/old-skill_${ARCHIVE_DATE}/README.md
```

---

## 检查清单

- [ ] 确定处理方式（废弃/删除/归档）
- [ ] 如废弃：更新 frontmatter + 添加警告
- [ ] 从索引中移除或标记
- [ ] 执行 [SYNC_INDEX.md](./SYNC_INDEX.md)
- [ ] 执行 [VALIDATE_SKILL_AND_INDEX.md](./VALIDATE_SKILL_AND_INDEX.md)

---

## AI Coding Agent 命令

```
请帮我废弃 old-skill：
- 替代方案：new-skill
- 废弃原因：功能已合并

请：
1. 更新 old-skill 的 frontmatter（添加 deprecated 标记）
2. 添加废弃警告到正文
3. 更新索引中的条目（标记为废弃）
4. 验证正确性
```

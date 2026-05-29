---
name: rules-maintenance
description: 检查和更新 Claude Rules 内容。包括格式检查、统计数据同步、过时内容清理。使用 /rules-cleanup 或 /rules-update 调用。
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - Edit
---

# Rules 维护 Skill

维护 `.claude/rules/` 目录中的规则文件。

## Rules 目录

```
/Users/jietaoxie/my-prototype-logistics/.claude/rules/
```

## 一键检查脚本

```bash
RULES_DIR="/Users/jietaoxie/my-prototype-logistics/.claude/rules"
FRONTEND_SRC="/Users/jietaoxie/my-prototype-logistics/frontend/CretasFoodTrace/src"
BACKEND_SRC="/Users/jietaoxie/my-prototype-logistics/backend-java/src"

echo "=== Rules 维护检查 $(date +%Y-%m-%d) ==="
echo ""

# 1. 代码库统计
echo "📊 代码库统计:"
echo "   'as any' 使用: $(grep -r 'as any' $FRONTEND_SRC --include='*.ts' --include='*.tsx' 2>/dev/null | wc -l | tr -d ' ') 处"
echo "   Controller: $(ls $BACKEND_SRC/main/java/com/cretas/aims/controller/*.java 2>/dev/null | wc -l | tr -d ' ') 个"
echo "   API 端点: $(grep -r '@.*Mapping' $BACKEND_SRC/main/java/com/cretas/aims/controller --include='*.java' 2>/dev/null | wc -l | tr -d ' ') 个"
echo ""

# 2. Rules 格式检查
echo "📋 Rules 格式:"
for f in $RULES_DIR/*.md; do
  filename=$(basename "$f")
  has_update=$(grep -c "最后更新" "$f" || echo 0)
  days_ago=$(( ($(date +%s) - $(stat -f '%m' "$f")) / 86400 ))
  status="✅"
  [ "$has_update" -eq 0 ] && status="⚠️ 缺更新日期"
  [ $days_ago -gt 7 ] && status="🔴 超7天未更新"
  printf "   %-35s %s\n" "$filename" "$status"
done
```

## 更新操作

### 更新统计数据

在对应 rule 文件中更新 "统计现状" 或 "后端规模统计" 章节：

```markdown
### 统计现状 (更新于 YYYY-MM-DD)

当前项目存在 **XX 处** `as any` 类型断言
```

### 更新版本信息

每次修改 rule 后，更新文件头部：

```markdown
**最后更新**: YYYY-MM-DD
```

## 检查清单

- [ ] 统计数据是否与代码库一致
- [ ] 文件引用是否有效
- [ ] 是否超过7天未更新
- [ ] 格式是否完整 (概述/Rule章节/相关文件)

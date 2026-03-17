---
name: skill-quality-validator
description: >
  Claude技能质量检查器,自动验证技能是否符合官方最佳实践标准。Use when 创建新技能需要验证规范、
  修改现有技能需要质量检查、从他人处获取技能需要评估质量、批量检查多个技能的合规性。
  适用于: (1) 新技能开发后的质量验证 (2) 技能更新后的合规检查 
  (3) 第三方技能的质量评估 (4) 团队技能库的标准化管理 (5) 技能打包前的最终审核
---

# Skill Quality Validator - 技能质量检查器

Claude技能质量检查器,基于官方创建流程规范自动验证技能质量。

## 快速开始

### 基础使用

1. **准备待检查的技能**
   - 技能目录路径 (如 `/mnt/skills/user/my-skill`)
   - 或打包的.skill文件

2. **执行检查**

   ```bash
   python scripts/check_skill.py <技能路径>
   ```

3. **查看报告**
   - 综合评分 (0-100分)
   - 问题清单 (致命/警告/建议)
   - 具体改进建议

### 支持的输入方式

| 输入类型   | 示例                          | 说明           |
| ---------- | ----------------------------- | -------------- |
| 技能目录   | `/mnt/skills/user/my-skill`   | 本地技能目录   |
| .skill文件 | `/home/claude/my-skill.skill` | 打包的技能文件 |
| 相对路径   | `./my-skill`                  | 当前目录的技能 |
| 绝对路径   | `/home/claude/skill-folder`   | 任意位置的技能 |

## 检查内容

### 全方位质量检查

检查器会验证以下7个维度:

1. **结构完整性** (30分)
   - 必需文件存在性
   - 目录结构规范性
   - 示例文件清理

2. **YAML规范性** (20分)
   - Frontmatter格式
   - 必需字段完整性
   - 字段内容规范

3. **描述质量** (15分)
   - "何时使用"说明
   - 具体场景数量 (3-5个)
   - 描述长度和清晰度

4. **内容质量** (20分)
   - SKILL.md长度控制 (<500行)
   - 章节结构合理性
   - 代码块管理

5. **引用有效性** (10分)
   - 文件引用正确性
   - 路径存在性验证

6. **代码质量** (5分)
   - Scripts语法正确性
   - 文档字符串完整性
   - Shebang规范性

7. **文档质量**
   - References内容充实性
   - Markdown格式规范

### 评分等级

| 分数   | 等级       | 说明                    |
| ------ | ---------- | ----------------------- |
| 90-100 | A - 优秀   | 完全符合最佳实践        |
| 80-89  | B - 良好   | 基本符合,有少量改进空间 |
| 70-79  | C - 合格   | 满足基本要求,建议优化   |
| 60-69  | D - 需改进 | 存在明显问题            |
| 0-59   | F - 不合格 | 有致命问题              |

**通过标准:** 评分≥70分 且 无致命问题

## 工作流程

### 完整检查流程

```
用户请求检查
    ↓
准备工作空间
- .skill文件自动解压
- 目录直接使用
    ↓
执行7项检查
- 结构、YAML、描述
- 内容、引用、代码、文档
    ↓
计算综合评分
- 扣分规则计算
- 等级评定
    ↓
生成详细报告
- 问题分级
- 改进建议
    ↓
输出检查结果
```

### 问题分级系统

**🔴 致命问题 (Critical)**

- 阻止技能正常工作
- 必须立即修复
- 每项扣10-30分

**⚠️ 警告 (Warning)**

- 影响技能质量
- 建议尽快修复
- 每项扣3-10分

**⭐ 建议 (Suggestion)**

- 优化改进方向
- 可逐步实施
- 不扣分

## 报告解读

### 报告结构

```
============================================================
技能质量检查报告
============================================================

技能名称: my-skill
综合评分: 85/100
评级等级: B - 良好
总问题数: 5
检查结果: ✅ 通过

============================================================
🔴 致命问题 (Critical Issues)
============================================================

1. 缺少必需文件: SKILL.md
   💡 改进建议: 创建SKILL.md文件,这是技能的核心文档

============================================================
⚠️ 警告 (Warnings)
============================================================

1. description缺少"何时使用"说明
   💡 改进建议: 添加 "Use when..." 或 "适用于..." 描述触发场景

2. 发现3个示例文件未清理
   💡 改进建议: 删除以下文件: scripts/example.py, ...

============================================================
💡 优化建议 (Suggestions)
============================================================

1. 建议添加章节: 快速开始, 工作流程
   💡 改进建议: 这些章节帮助用户快速理解如何使用技能
```

### 如何改进

1. **优先修复致命问题**
   - 这些问题会阻止技能运行
   - 必须在打包前解决

2. **处理警告**
   - 提升技能质量
   - 改善用户体验

3. **考虑建议**
   - 优化方向
   - 可在后续版本实施

4. **重新检查**
   - 修复后再次运行检查
   - 确保达到通过标准

## 配置说明

### 检查标准定制

检查器使用固定的评分标准,基于官方最佳实践文档。如需了解详细的检查项目和评分规则,参见:

- **完整检查清单**: `references/checklist.md`
- **快速修复指南**: `references/quick_fixes.md`

### 修改评分权重

如果你需要调整评分标准(不推荐),可以修改 `scripts/check_skill.py` 中的扣分参数:

```python
# 示例: 调整description缺少"何时使用"的扣分
if not any(keyword in description.lower() for keyword in ...):
    self.score -= 8  # 改为你希望的扣分值
```

## 常见使用场景

### 场景1: 新技能开发验证

**工作流:**

```bash
# 1. 创建技能
python /mnt/skills/examples/skill-creator/scripts/init_skill.py my-skill

# 2. 开发技能内容
# ... 编写SKILL.md, scripts, references ...

# 3. 质量检查
python /mnt/skills/user/skill-quality-validator/scripts/check_skill.py my-skill

# 4. 根据报告改进

# 5. 重新检查直到通过
```

### 场景2: 现有技能更新检查

**工作流:**

```bash
# 1. 修改技能内容
# ... 更新SKILL.md或添加新功能 ...

# 2. 验证更新是否合规
python scripts/check_skill.py /mnt/skills/user/existing-skill

# 3. 确保评分未降低
```

### 场景3: 第三方技能评估

**工作流:**

```bash
# 1. 下载技能文件
# downloaded-skill.skill

# 2. 质量评估
python scripts/check_skill.py downloaded-skill.skill

# 3. 查看报告决定是否使用
```

### 场景4: 批量技能检查

**工作流:**

```bash
# 检查所有用户技能
for skill in /mnt/skills/user/*/; do
    echo "检查: $skill"
    python scripts/check_skill.py "$skill"
    echo "---"
done
```

## 与官方工具集成

### 与package_skill.py配合

```bash
# 标准技能发布流程

# 1. 质量检查
python /mnt/skills/user/skill-quality-validator/scripts/check_skill.py my-skill
# 确保通过 (≥70分, 无致命问题)

# 2. 打包技能
python /mnt/skills/examples/skill-creator/scripts/package_skill.py my-skill
# 生成 my-skill.skill

# 3. 分发使用
```

### 持续质量保证

建议在以下时机执行检查:

- ✅ 新技能创建后
- ✅ 重大功能更新后
- ✅ 打包发布前
- ✅ 定期审查 (如每月)

## 进阶使用

### 自定义检查规则

如需添加特定项目的检查规则,可以扩展 `scripts/check_skill.py`:

```python
def _check_custom_requirement(self):
    """自定义检查项"""
    # 你的检查逻辑
    if not meets_requirement:
        self._add_issue('warning', '问题描述', '改进建议')
        self.score -= 5
```

### 集成到CI/CD

在自动化流程中使用:

```yaml
# GitHub Actions 示例
- name: Validate Skill Quality
  run: |
    python check_skill.py my-skill
    if [ $? -ne 0 ]; then
      echo "质量检查未通过"
      exit 1
    fi
```

### 生成质量徽章

基于检查结果生成README徽章:

```markdown
![Quality](https://img.shields.io/badge/quality-85%25-green)
![Grade](https://img.shields.io/badge/grade-B-blue)
```

## 参考资源

- **详细检查清单**: `references/checklist.md` - 所有检查项的完整说明
- **快速修复指南**: `references/quick_fixes.md` - 常见问题的解决方案
- **官方规范**: Claude skills创建流程规范(6步法) - 基础方法论

## 故障排除

### 问题: 检查脚本报错

```bash
# 确保Python 3可用
python3 --version

# 确保有执行权限
chmod +x scripts/check_skill.py
```

### 问题: .skill文件无法解压

```bash
# .skill文件本质是zip文件
# 手动解压测试
unzip -t skill-file.skill
```

### 问题: 评分不符合预期

- 查看详细报告了解扣分原因
- 参考 `references/checklist.md` 了解评分规则
- 每个问题都有对应的改进建议

## 限制说明

- 不检查技能的实际功能是否正确运行
- 不验证技能的业务逻辑是否合理
- 不检查资源文件 (assets/) 的具体内容
- 仅基于静态分析,不执行动态测试

**建议:** 质量检查通过后,仍需进行实际功能测试。

## 技能更新日志

- **v1.0** (2025-12-10)
  - 初始版本发布
  - 支持7个维度的全面检查
  - 提供详细的改进建议
  - 支持.skill文件和目录检查

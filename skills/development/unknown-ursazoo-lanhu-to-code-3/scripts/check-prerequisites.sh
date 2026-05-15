#!/bin/bash
# design-to-code 前置条件检查
# exit 0 = 可继续  exit 1 = 阻断  exit 2 = 需暂停等用户决策
# stdout 输出 CONTEXT_FILES 供 design-to-code 传给 code-format

PROJECT_ROOT="${1:-.}"
BLOCK=()
PAUSE=()
WARN=()

# ─── 技术栈来源（三层兜底）────────────────────────────────────
TECH_STACK_FILE=""

if [ -f "$PROJECT_ROOT/README.md" ]; then
  TECH_STACK_FILE="README.md"
elif [ -f "$PROJECT_ROOT/CLAUDE.md" ] && \
     grep -qi "技术栈\|vue\|react\|uni-app\|angular\|svelte\|framework\|stack" "$PROJECT_ROOT/CLAUDE.md"; then
  TECH_STACK_FILE="CLAUDE.md"
elif [ -f "$PROJECT_ROOT/package.json" ]; then
  TECH_STACK_FILE="package.json（将从中推断技术栈）"
  WARN+=("README.md 不存在，将从 package.json 推断技术栈，建议创建 README.md 填写完整技术栈信息")
fi

if [ -z "$TECH_STACK_FILE" ]; then
  BLOCK+=("无法确定技术栈：缺少 README.md / CLAUDE.md / package.json")
fi

# ─── 技术规格（PAUSE：缺失时无法自动判断新建 vs 改造）──────────
TECH_SPEC_FILE=""
if [ -f "$PROJECT_ROOT/docs/tech-spec.md" ]; then
  TECH_SPEC_FILE="docs/tech-spec.md"
elif [ -d "$PROJECT_ROOT/docs" ]; then
  FOUND=$(grep -rl "路由\|页面列表\|接口\|API\|页面路径" "$PROJECT_ROOT/docs/" 2>/dev/null \
    | grep "\.md$" | grep -v "问题记录\|issue\|bug\|联调" | head -1)
  [ -n "$FOUND" ] && TECH_SPEC_FILE="${FOUND#$PROJECT_ROOT/}"
fi

if [ -z "$TECH_SPEC_FILE" ]; then
  PAUSE+=("tech-spec：缺失时无法自动判断设计稿对应的是新建页面还是改造现有页面")
fi

# ─── 组件文档来源（两层兜底）──────────────────────────────────
COMPONENT_DOC_FILE=""

if [ -f "$PROJECT_ROOT/docs/components.md" ]; then
  COMPONENT_DOC_FILE="docs/components.md"
elif [ -d "$PROJECT_ROOT/docs" ]; then
  FOUND=$(find "$PROJECT_ROOT/docs" -maxdepth 1 -name "*.md" \
    | grep -i "组件\|component" | head -1)
  if [ -z "$FOUND" ]; then
    FOUND=$(grep -rl "Props\|props\|组件\|Component" "$PROJECT_ROOT/docs/" 2>/dev/null \
      | grep "\.md$" | grep -v "问题记录\|issue\|bug\|联调" | head -1)
  fi
  if [ -n "$FOUND" ]; then
    COMPONENT_DOC_FILE="${FOUND#$PROJECT_ROOT/}"
    WARN+=("docs/components.md 不存在，将使用 $COMPONENT_DOC_FILE 作为组件参考")
  fi
fi

if [ -z "$COMPONENT_DOC_FILE" ]; then
  PAUSE+=("component-doc：docs/ 中无任何组件文档，无法复用现有组件")
fi

# ─── 编码规范来源（宽松）────────────────────────────────────────
DEV_SPEC_FILE=""
if [ -f "$PROJECT_ROOT/docs/dev-spec.md" ]; then
  DEV_SPEC_FILE="docs/dev-spec.md"
elif [ -d "$PROJECT_ROOT/docs" ]; then
  FOUND=$(grep -rl "命名规范\|编码规范\|开发规范\|代码风格\|ESLint" "$PROJECT_ROOT/docs/" 2>/dev/null \
    | grep "\.md$" | head -1)
  [ -n "$FOUND" ] && DEV_SPEC_FILE="${FOUND#$PROJECT_ROOT/}"
fi
[ -z "$DEV_SPEC_FILE" ] && WARN+=("dev-spec — 缺失时扫描 src/ 推断编码风格")

# ─── 输出 ────────────────────────────────────────────────────────
echo "=== design-to-code 前置检查 ==="
echo "项目路径：$PROJECT_ROOT"
echo ""

if [ ${#BLOCK[@]} -gt 0 ]; then
  echo "STATUS: BLOCKED"
  echo "❌ 必需信息缺失："
  for f in "${BLOCK[@]}"; do echo "   - $f"; done
  exit 1
fi

if [ ${#PAUSE[@]} -gt 0 ]; then
  echo "STATUS: NEEDS_DECISION"
  echo "⚠️  以下文档缺失，需要决策后才能继续："
  for f in "${PAUSE[@]}"; do echo "   - $f"; done
  echo ""
fi

# 输出找到的文件路径，供 code-format 使用
echo "CONTEXT_FILES:"
echo "  TECH_STACK=${TECH_STACK_FILE}"
echo "  COMPONENT_DOC=${COMPONENT_DOC_FILE}"
echo "  DEV_SPEC=${DEV_SPEC_FILE}"
echo "  TECH_SPEC=${TECH_SPEC_FILE}"
echo ""

if [ ${#WARN[@]} -gt 0 ]; then
  echo "⚠️  以下文档缺失或使用替代文件："
  for f in "${WARN[@]}"; do echo "   - $f"; done
  echo ""
fi

if [ ${#PAUSE[@]} -gt 0 ]; then
  exit 2
fi

echo "STATUS: OK"
[ ${#WARN[@]} -eq 0 ] && echo "✓ 所有文档齐全" || echo "✓ 核心文档就绪（部分使用替代文件）"
exit 0

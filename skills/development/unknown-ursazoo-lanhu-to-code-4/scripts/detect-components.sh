#!/bin/bash
# 扫描项目组件目录，输出分类清单
# 用法：bash detect-components.sh [项目根目录]
# 输出格式：<类型>:<目录路径>:<文件路径>
#   类型：shared（通用组件）| page（页面级组件）

PROJECT_ROOT="${1:-.}"
SRC="$PROJECT_ROOT/src"

if [ ! -d "$SRC" ]; then
  echo "ERROR: src/ 目录不存在于 $PROJECT_ROOT" >&2
  exit 1
fi

# 找到所有名为 components 的目录（排除 node_modules、dist、.git）
find "$SRC" -type d -name "components" \
  ! -path "*/node_modules/*" \
  ! -path "*/dist/*" \
  ! -path "*/.git/*" | while read -r components_dir; do

  # 计算相对于 src/ 的深度（目录层级）
  rel="${components_dir#$SRC/}"
  depth=$(echo "$rel" | tr -cd '/' | wc -c)

  # 深度 0 = src/components/（通用）
  # 深度 >= 1 = src/views/xxx/components/、src/pages/xxx/components/ 等（页面级）
  if [ "$depth" -eq 0 ]; then
    type="shared"
  else
    type="page"
  fi

  # 输出此目录下的所有组件文件
  find "$components_dir" -maxdepth 2 -type f \( -name "*.vue" -o -name "*.tsx" -o -name "*.jsx" \) \
    ! -name "*.test.*" ! -name "*.spec.*" ! -name "*.stories.*" | while read -r file; do
    echo "$type:$components_dir:$file"
  done
done

#!/usr/bin/env bash
# memory-backup.sh — Agent 记忆备份/恢复到百度网盘
#
# 支持的 Agent：kimiclaw、maxclaw、qclaw、openclaw（自动检测）
# 网盘存储路径：/apps/bdpan/agent-memory/<agent>/<device>/manual/<timestamp>/
#
# 用法:
#   bash memory-backup.sh backup           备份当前记忆到百度网盘
#   bash memory-backup.sh list             列出所有可用备份
#   bash memory-backup.sh restore <date>   恢复指定日期的备份（支持模糊匹配）
#   bash memory-backup.sh restore <date> --force  跳过兼容性警告强制恢复
set -euo pipefail

# ============================================================
# 常量
# ============================================================
SCRIPT_VERSION="1.0.0"
DEFAULT_BASE_PATH="/apps/bdpan/agent-memory"

# 全局临时目录（供 EXIT trap 清理，local 变量在 EXIT 时已出作用域）
_BACKUP_TMP_DIR=""
_RESTORE_TMP_DIR=""
trap 'rm -rf "${_BACKUP_TMP_DIR:-}" "${_RESTORE_TMP_DIR:-}"' EXIT

# ============================================================
# Agent 检测模块
# ============================================================
# 调用后设置全局变量:
#   DETECTED_AGENT, AGENT_NAME, MEMORY_SYSTEM_NAME,
#   WORKSPACE_DIR, MEMORY_DIR, CONFIG_DIR, WORKSPACE_FILES

detect_agent() {
  local script_abs_path
  script_abs_path="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

  DETECTED_AGENT="unknown"

  # 1. kimiclaw: 路径含 .openclaw 且 .kimi 目录存在
  if [[ "$script_abs_path" == *".openclaw"* ]] && [ -d "/root/.kimi/kimi-claw" ]; then
    DETECTED_AGENT="kimiclaw"
    _set_agent_config "kimiclaw" "/root/.openclaw/workspace" "/root/.openclaw"
    return 0
  fi

  # 2. maxclaw: 路径前缀为 /workspace/ 且 .maxclaw 目录存在
  if [[ "$script_abs_path" == /workspace/* ]] && [ -d "/root/.maxclaw" ]; then
    DETECTED_AGENT="maxclaw"
    _set_agent_config "maxclaw" "/workspace" "/root/.maxclaw"
    return 0
  fi

  # 3. qclaw: 路径段完整匹配 .qclaw 或 qclaw（大小写不敏感，兼容 bash 3.2+）
  local _path_lower
  _path_lower="$(echo "$script_abs_path" | tr '[:upper:]' '[:lower:]')"
  if [[ "$_path_lower" =~ (^|/)(\.qclaw|qclaw)(/|$) ]]; then
    DETECTED_AGENT="qclaw"
    _set_agent_config "qclaw" "$HOME/.qclaw/workspace" "$HOME/.qclaw"
    return 0
  fi

  # 4. openclaw: 路径段完整匹配 .openclaw 或 openclaw，且 OPENCLAW_CLI=1（大小写不敏感，兼容 bash 3.2+）
  if [[ "$_path_lower" =~ (^|/)(\.openclaw|openclaw)(/|$) ]] && [ "${OPENCLAW_CLI:-}" = "1" ]; then
    DETECTED_AGENT="openclaw"
    local home="${OPENCLAW_HOME:-$HOME/.openclaw}"
    _set_agent_config "openclaw" "$home/workspace" "$home"
    return 0
  fi

  DETECTED_AGENT="unknown"
  return 1
}

_set_agent_config() {
  AGENT_NAME="$1"
  WORKSPACE_DIR="$2"
  CONFIG_DIR="$3"
  MEMORY_SYSTEM_NAME="memory-core"
  MEMORY_DIR="$WORKSPACE_DIR/memory"
  WORKSPACE_FILES=("AGENTS.md" "SOUL.md" "USER.md" "IDENTITY.md" "TOOLS.md" "MEMORY.md" "HEARTBEAT.md")
}

# ============================================================
# 设备工具函数
# ============================================================
get_device_name() {
  hostname | sed 's/\.[Ll][Oo][Cc][Aa][Ll]$//' | tr '[:upper:]' '[:lower:]'
}

normalize_device() {
  echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]/-/g'
}

# ============================================================
# 路径工具函数
# ============================================================
build_backup_path() {
  local agent="${1:-}"
  local device="${2:-}"
  local backup_type="${3:-}"
  local timestamp="${4:-}"
  echo "${DEFAULT_BASE_PATH}/${agent}/${device}/${backup_type}/${timestamp}"
}

build_base_path() {
  local agent="${1:-}"
  local device="${2:-}"
  echo "${DEFAULT_BASE_PATH}/${agent}/${device}"
}

# API 路径 → 用户显示路径（/apps/... → 我的应用数据/...）
to_user_path() {
  local api_path="${1:-}"
  if [ -z "$api_path" ]; then
    echo ""
    return
  fi
  if [[ "$api_path" == "/apps/"* ]]; then
    echo "我的应用数据/${api_path#/apps/}"
  elif [[ "$api_path" == "/apps" ]]; then
    echo "我的应用数据"
  else
    echo "$api_path"
  fi
}

# ============================================================
# JSON 工具函数（基于 Node.js）
# ============================================================
json_array_length() {
  local file="$1"
  local field="$2"
  node -e "
    const d = JSON.parse(require('fs').readFileSync(process.argv[1], 'utf8'));
    const arr = d[process.argv[2]];
    if (!Array.isArray(arr)) process.exit(1);
    process.stdout.write(String(arr.length));
  " "$file" "$field"
}

json_array_get() {
  local file="$1"
  local field="$2"
  local index="$3"
  node -e "
    const d = JSON.parse(require('fs').readFileSync(process.argv[1], 'utf8'));
    const v = d[process.argv[2]][Number(process.argv[3])];
    if (v === null || v === undefined) process.exit(1);
    process.stdout.write(String(v));
  " "$file" "$field" "$index"
}

json_pipe() {
  local code="$1"
  shift
  node -e "
    const input = require('fs').readFileSync('/dev/stdin', 'utf8').trim();
    ${code}
  " "$@"
}

# ============================================================
# Manifest 创建/读取/校验
# ============================================================
create_manifest() {
  local output_file="$1"
  local agent="$2"
  local memory_system="$3"
  local device="$4"
  shift 4

  local files=("$@")

  local normalized_device
  normalized_device=$(normalize_device "$device")
  local created_at
  created_at=$(date +"%Y-%m-%dT%H:%M:%S")

  node -e "
    const fs = require('fs');
    const [outFile, ver, agent, ms, dev, ts, bt, ...files] = process.argv.slice(1);
    const obj = {
      version: ver,
      agent: agent,
      memorySystem: ms,
      device: dev,
      createdAt: ts,
      backupType: bt,
      lastBackupAt: ts,
      triggerCount: 1,
      files: files
    };
    fs.writeFileSync(outFile, JSON.stringify(obj, null, 2) + '\n');
  " "$output_file" "2.0" "$agent" "$memory_system" "$normalized_device" "$created_at" "manual" "${files[@]}"
}

read_manifest() {
  local json_file="$1"

  if [ ! -f "$json_file" ]; then
    echo "Invalid manifest: file not found: $json_file" >&2
    return 1
  fi

  local raw
  raw=$(node -e "
    const d = JSON.parse(require('fs').readFileSync(process.argv[1], 'utf8'));
    const f = (v) => v === undefined || v === null || v === '' ? '\x01' : String(v);
    const fields = [
      f(d.version),
      f(d.agent || d.agentType),
      f(d.memorySystem || d.memoryPlugin),
      f(d.device),
      f(d.createdAt),
      d.backupType || 'manual'
    ];
    process.stdout.write(fields.join('\n'));
  " "$json_file") || { echo "Invalid manifest: bad JSON" >&2; return 1; }

  local -a _fields=()
  local _line
  while IFS= read -r _line; do
    _fields+=("$_line")
  done <<< "$raw"

  MANIFEST_VERSION="${_fields[0]:-}"
  MANIFEST_AGENT="${_fields[1]:-}"
  MANIFEST_MEMORY_SYSTEM="${_fields[2]:-}"
  MANIFEST_DEVICE="${_fields[3]:-}"
  MANIFEST_CREATED_AT="${_fields[4]:-}"
  MANIFEST_BACKUP_TYPE="${_fields[5]:-}"

  [[ "$MANIFEST_VERSION" == $'\x01' ]] && MANIFEST_VERSION=""
  [[ "$MANIFEST_AGENT" == $'\x01' ]] && MANIFEST_AGENT=""
  [[ "$MANIFEST_MEMORY_SYSTEM" == $'\x01' ]] && MANIFEST_MEMORY_SYSTEM=""
  [[ "$MANIFEST_DEVICE" == $'\x01' ]] && MANIFEST_DEVICE=""
  [[ "$MANIFEST_CREATED_AT" == $'\x01' ]] && MANIFEST_CREATED_AT=""

  for field in MANIFEST_VERSION MANIFEST_AGENT MANIFEST_MEMORY_SYSTEM MANIFEST_DEVICE MANIFEST_CREATED_AT; do
    if [ -z "${!field}" ]; then
      local fname="${field#MANIFEST_}"
      echo "Invalid manifest: missing or invalid field \"${fname,,}\"" >&2
      return 1
    fi
  done

  # 读取文件列表
  MANIFEST_FILES=()
  local file_count
  file_count=$(json_array_length "$json_file" "files" 2>/dev/null)
  if [ -z "$file_count" ] || ! [[ "$file_count" =~ ^[0-9]+$ ]]; then
    echo 'Invalid manifest: missing or invalid field "files"' >&2
    return 1
  fi

  local i
  for ((i = 0; i < file_count; i++)); do
    local fp
    fp=$(json_array_get "$json_file" "files" "$i")
    if [ -z "$fp" ] || [ "$fp" = "null" ]; then
      echo 'Invalid manifest: "files" array must contain only strings' >&2
      return 1
    fi
    _validate_file_path "$fp" || return 1
    MANIFEST_FILES+=("$fp")
  done
}

_validate_file_path() {
  local fp="$1"
  if [[ "$fp" == /* ]]; then
    echo "Invalid manifest: absolute file path not allowed: \"$fp\"" >&2
    return 1
  fi
  if [[ "$fp" == ../* ]] || [[ "$fp" == */../* ]] || [[ "$fp" == */.. ]] || [[ "$fp" == ".." ]]; then
    echo "Invalid manifest: path traversal not allowed: \"$fp\"" >&2
    return 1
  fi
}

validate_compatibility() {
  local manifest_file="$1"
  local current_agent="$2"
  local current_ms="$3"

  read_manifest "$manifest_file" || return 1

  local warnings=()
  if [ "$MANIFEST_AGENT" != "$current_agent" ]; then
    warnings+=("Agent mismatch: backup is \"$MANIFEST_AGENT\", current is \"$current_agent\"")
  fi
  if [ "$MANIFEST_MEMORY_SYSTEM" != "$current_ms" ]; then
    warnings+=("Memory system mismatch: backup is \"$MANIFEST_MEMORY_SYSTEM\", current is \"$current_ms\"")
  fi

  if [ ${#warnings[@]} -gt 0 ]; then
    printf '%s\n' "${warnings[@]}"
    return 1
  fi
  return 0
}

# ============================================================
# bdpan CLI 封装
# ============================================================
_bdpan_is_installed() {
  command -v bdpan &>/dev/null
}

_bdpan_whoami() {
  local raw
  raw=$(bdpan whoami --json 2>/dev/null) || { echo "loggedIn=false"; return; }
  local authenticated
  authenticated=$(echo "$raw" | node -e "
    let d = ''; process.stdin.on('data', c => d += c);
    process.stdin.on('end', () => {
      try {
        const obj = JSON.parse(d);
        process.stdout.write(obj.authenticated === true ? 'true' : 'false');
      } catch(e) {
        process.stdout.write(d.includes('已登录') ? 'true' : 'false');
      }
    });
  " 2>/dev/null) || authenticated="false"
  if [ "$authenticated" = "true" ]; then
    echo "loggedIn=true"
  else
    echo "loggedIn=false"
  fi
}

_bdpan_ls() {
  local remote_path="$1"
  local raw
  raw=$(bdpan ls "$remote_path" --json 2>/dev/null) || return 1
  echo "$raw" | json_pipe "
    if (!input) process.exit(0);
    let d; try { d = JSON.parse(input); } catch(e) { process.exit(0); }
    if (!Array.isArray(d)) process.exit(0);
    for (const item of d) {
      const obj = {
        name: item.server_filename,
        isDir: (item.isdir === true || item.isdir === 1) ? 1 : 0,
        size: item.size
      };
      process.stdout.write(JSON.stringify(obj) + '\n');
    }
  "
}

_bdpan_upload() {
  local local_path="$1"
  local remote_path="$2"
  bdpan upload "$local_path" "$remote_path" 2>&1
}

_bdpan_download() {
  local remote_path="$1"
  local local_path="$2"
  if command -v timeout &>/dev/null; then
    timeout 120 bdpan download "$remote_path" "$local_path" 2>&1
  elif command -v gtimeout &>/dev/null; then
    gtimeout 120 bdpan download "$remote_path" "$local_path" 2>&1
  else
    bdpan download "$remote_path" "$local_path" 2>&1
  fi
}

# ============================================================
# 前置检查（复用现有 install.sh / login.sh）
# ============================================================
check_prerequisites() {
  # 1. 检查 Node.js
  if ! command -v node &>/dev/null; then
    echo "缺少 Node.js 运行时，请先安装 Node.js：https://nodejs.org/" >&2
    exit 1
  fi

  # 2. 检查 bdpan 安装
  if ! _bdpan_is_installed; then
    local skill_dir
    skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    local install_script="${skill_dir}/scripts/install.sh"
    if [ -f "$install_script" ]; then
      echo "未检测到 bdpan CLI，正在调用安装脚本..."
      bash "$install_script" || {
        echo "bdpan CLI 安装失败，请手动安装。" >&2
        exit 1
      }
    else
      echo "未检测到 bdpan CLI，请先安装：bash \${CLAUDE_SKILL_DIR}/scripts/install.sh" >&2
      exit 1
    fi
    if ! _bdpan_is_installed; then
      echo "bdpan CLI 安装后仍未找到，请检查 PATH 配置。" >&2
      exit 1
    fi
    echo "bdpan CLI 安装成功！"
  fi

  # 3. 检查登录状态
  local whoami_result
  whoami_result=$(_bdpan_whoami)
  if [[ "$whoami_result" != loggedIn=true* ]]; then
    local skill_dir
    skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
    local login_script="${skill_dir}/scripts/login.sh"
    if [ -f "$login_script" ]; then
      echo "请先登录百度网盘："
      bash "$login_script"
    else
      echo "请先登录百度网盘：bash \${CLAUDE_SKILL_DIR}/scripts/login.sh" >&2
      exit 1
    fi
  fi
}

# ============================================================
# 文件合并（restore 时将下载的文件写入本地）
# ============================================================
apply_merge() {
  local tmp_dir="$1"

  mkdir -p "$MEMORY_DIR" "$WORKSPACE_DIR"

  # 构建 workspace 文件集合用于快速查找
  local ws_set="|"
  for wf in "${WORKSPACE_FILES[@]}"; do
    ws_set="${ws_set}${wf}|"
  done

  for file in "${MANIFEST_FILES[@]}"; do
    local src="$tmp_dir/$file"
    [ -f "$src" ] || continue

    local dest_path allowed_base

    if [[ "$ws_set" == *"|${file}|"* ]]; then
      dest_path="$WORKSPACE_DIR/$file"
      allowed_base="$WORKSPACE_DIR"
    elif [[ "$file" == memory/* ]]; then
      dest_path="$MEMORY_DIR/${file#memory/}"
      allowed_base="$MEMORY_DIR"
    else
      dest_path="$WORKSPACE_DIR/$file"
      allowed_base="$WORKSPACE_DIR"
    fi

    # 路径遍历防护：解析真实路径检查
    local resolved_dest resolved_base
    mkdir -p "$(dirname "$dest_path")"
    resolved_dest=$(cd "$(dirname "$dest_path")" && pwd)/$(basename "$dest_path")
    resolved_base=$(cd "$allowed_base" && pwd)

    if [[ "$resolved_dest" != "$resolved_base"* ]]; then
      echo "Path traversal detected: \"$file\" resolves outside allowed directory" >&2
      continue
    fi

    cp "$src" "$dest_path"
  done
}

# ============================================================
# backup 命令
# ============================================================
cmd_backup() {
  check_prerequisites

  local device
  device=$(get_device_name)
  local timestamp
  timestamp=$(date +"%Y-%m-%dT%H-%M-%S")

  _BACKUP_TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/memory-backup-XXXXXX")
  local tmp_dir="$_BACKUP_TMP_DIR"

  local files=()

  # 1. 复制 memory/*.md
  if [ -d "$MEMORY_DIR" ]; then
    mkdir -p "$tmp_dir/memory"
    for f in "$MEMORY_DIR"/*.md; do
      [ -f "$f" ] || continue
      cp "$f" "$tmp_dir/memory/"
      files+=("memory/$(basename "$f")")
    done
  fi

  # 2. 复制 workspace 文件
  for wf in "${WORKSPACE_FILES[@]}"; do
    local src="$WORKSPACE_DIR/$wf"
    if [ -f "$src" ]; then
      cp "$src" "$tmp_dir/$wf"
      files+=("$wf")
    fi
  done

  if [ ${#files[@]} -eq 0 ]; then
    echo "警告：未找到任何记忆文件，请检查路径：$WORKSPACE_DIR" >&2
    exit 1
  fi

  # 3. 生成 manifest
  create_manifest "$tmp_dir/manifest.json" "$AGENT_NAME" "$MEMORY_SYSTEM_NAME" "$device" "${files[@]}"

  # 4. 上传（记忆文件每次新目录，直接用 bdpan upload）
  local remote_path
  remote_path=$(build_backup_path "$AGENT_NAME" "$(normalize_device "$device")" "manual" "$timestamp")

  local all_files=("manifest.json" "${files[@]}")
  local total=${#all_files[@]}

  echo "开始备份，共 ${total} 个文件..."

  local i
  local failed_files=()
  for ((i = 0; i < total; i++)); do
    local file="${all_files[$i]}"
    local local_file="$tmp_dir/$file"
    local remote_file="$remote_path/$file"

    # 确保远端目录存在（处理 memory/ 子目录）
    bdpan mkdir "$(dirname "$remote_file")" 2>/dev/null || true

    if ! _bdpan_upload "$local_file" "$remote_file" >/dev/null; then
      failed_files+=("$file")
    fi
  done

  echo ""
  if [ ${#failed_files[@]} -gt 0 ]; then
    echo "备份完成（${#failed_files[@]} 个文件上传失败）"
    for ff in "${failed_files[@]}"; do
      echo "  - $ff"
    done
  else
    echo "备份完成"
  fi
  echo "文件数: ${total} 个"
  echo "位置: $(to_user_path "${remote_path}")/"
}

# ============================================================
# list 命令
# ============================================================
cmd_list() {
  check_prerequisites

  local device
  device=$(get_device_name)
  local base_path
  base_path=$(build_base_path "$AGENT_NAME" "$(normalize_device "$device")")

  # 列出 manual/ 子目录下的备份
  local rows=()
  local remote_path="${base_path}/manual/"
  local entries
  entries=$(_bdpan_ls "$remote_path" 2>/dev/null) || true

  if [ -n "$entries" ]; then
    local dirs
    dirs=$(echo "$entries" | json_pipe "
      if (!input) process.exit(0);
      for (const line of input.split('\n')) {
        if (!line) continue;
        try {
          const d = JSON.parse(line);
          if (d.isDir === 1) process.stdout.write(d.name + '\n');
        } catch(e) {}
      }
    " 2>/dev/null) || true

    if [ -n "$dirs" ]; then
      while IFS= read -r dir_name; do
        rows+=("${dir_name}|manual")
      done <<< "$dirs"
    fi
  fi

  if [ ${#rows[@]} -eq 0 ]; then
    echo "暂无备份记录"
    return
  fi

  # 按时间戳降序排序
  local sorted_rows
  sorted_rows=$(printf '%s\n' "${rows[@]}" | sort -t'|' -k1 -r)

  echo ""
  echo "可用备份列表（设备: ${device}，路径: $(to_user_path "${base_path}")）"
  echo ""
  printf '%-3s %-22s %-8s %s\n' "#" "日期" "类型" "路径"
  echo "---  ----------------------  --------  -----"

  local idx=1
  while IFS= read -r row; do
    local date btype
    IFS='|' read -r date btype <<< "$row"
    printf '%-3d %-22s %-8s %s\n' "$idx" "$date" "$btype" "$(to_user_path "${base_path}/${btype}/${date}/")"
    ((idx++))
  done <<< "$sorted_rows"

  echo ""
  echo "共 $(echo "$sorted_rows" | wc -l | tr -d ' ') 个备份"
}

# ============================================================
# restore 命令
# ============================================================
cmd_restore() {
  local date_pattern="$1"
  local force="${2:-false}"

  check_prerequisites

  local device
  device=$(get_device_name)
  local base_path
  base_path=$(build_base_path "$AGENT_NAME" "$(normalize_device "$device")")

  # 在 manual/ 子目录下搜索匹配的备份
  local all_matches=()
  local remote_path="${base_path}/manual/"
  local entries
  entries=$(_bdpan_ls "$remote_path" 2>/dev/null) || true

  if [ -n "$entries" ]; then
    local dirs
    dirs=$(echo "$entries" | json_pipe "
      if (!input) process.exit(0);
      for (const line of input.split('\n')) {
        if (!line) continue;
        try {
          const d = JSON.parse(line);
          if (d.isDir === 1) process.stdout.write(d.name + '\n');
        } catch(e) {}
      }
    " 2>/dev/null | grep "$date_pattern" 2>/dev/null || true)

    if [ -n "$dirs" ]; then
      while IFS= read -r dir_name; do
        all_matches+=("manual|${dir_name}")
      done <<< "$dirs"
    fi
  fi

  if [ ${#all_matches[@]} -eq 0 ]; then
    echo "未找到匹配 \"$date_pattern\" 的备份" >&2
    exit 1
  fi

  if [ ${#all_matches[@]} -gt 1 ]; then
    echo "找到多个匹配 \"$date_pattern\" 的备份，请更精确地指定日期：" >&2
    for m in "${all_matches[@]}"; do
      local mtype mname
      IFS='|' read -r mtype mname <<< "$m"
      echo "  - $mname ($mtype)" >&2
    done
    exit 1
  fi

  local matched="${all_matches[0]}"
  local matched_type matched_name
  IFS='|' read -r matched_type matched_name <<< "$matched"
  local backup_remote="${base_path}/${matched_type}/${matched_name}/"

  _RESTORE_TMP_DIR=$(mktemp -d "${TMPDIR:-/tmp}/memory-restore-XXXXXX")
  local tmp_dir="$_RESTORE_TMP_DIR"

  # 下载 manifest
  echo "正在获取备份信息..."
  local manifest_tmp="$tmp_dir/manifest.json"
  _bdpan_download "${backup_remote}manifest.json" "$manifest_tmp" >/dev/null 2>&1 || {
    echo "无法下载 manifest.json，请检查备份路径是否正确。" >&2
    exit 1
  }

  read_manifest "$manifest_tmp" || { echo "Invalid manifest" >&2; exit 1; }

  # 兼容性检查
  local compat_warnings
  if ! compat_warnings=$(validate_compatibility "$manifest_tmp" "$AGENT_NAME" "$MEMORY_SYSTEM_NAME" 2>/dev/null); then
    if [ "$force" != "true" ]; then
      if echo "$compat_warnings" | grep -q "Agent mismatch"; then
        echo "兼容性警告：备份来自 \"$MANIFEST_AGENT\"，当前环境是 \"$AGENT_NAME\"" >&2
        echo "不同 Agent 类型的记忆文件可能存在兼容性问题" >&2
      else
        echo "兼容性校验失败：" >&2
        while IFS= read -r w; do
          echo "  $w" >&2
        done <<< "$compat_warnings"
      fi
      echo "" >&2
      echo "使用 --force 跳过此警告并强制恢复" >&2
      exit 1
    else
      echo "兼容性警告（已通过 --force 跳过）："
      while IFS= read -r w; do
        echo "  $w"
      done <<< "$compat_warnings"
    fi
  fi

  # Safety net: 恢复前备份当前本地记忆
  local safety_timestamp
  safety_timestamp=$(date +"%Y-%m-%dT%H-%M-%S")
  local safety_dir="$WORKSPACE_DIR/.backup-before-restore/$safety_timestamp"
  mkdir -p "$safety_dir"

  if [ -d "$MEMORY_DIR" ]; then
    cp -r "$MEMORY_DIR" "$safety_dir/memory" 2>/dev/null || true
  fi

  for wf in "${WORKSPACE_FILES[@]}"; do
    local wp="$WORKSPACE_DIR/$wf"
    if [ -f "$wp" ]; then
      cp "$wp" "$safety_dir/$wf" 2>/dev/null || true
    fi
  done

  echo "已备份当前记忆到 $safety_dir"

  # 下载所有备份文件
  local total=${#MANIFEST_FILES[@]}
  echo ""
  echo "开始恢复，共 ${total} 个文件..."

  local i
  local failed_files=()
  for ((i = 0; i < total; i++)); do
    local file="${MANIFEST_FILES[$i]}"
    local local_tmp="$tmp_dir/$file"
    mkdir -p "$(dirname "$local_tmp")"
    if ! _bdpan_download "${backup_remote}${file}" "$local_tmp" >/dev/null 2>&1; then
      failed_files+=("$file")
    fi
  done

  # 合并文件到本地
  apply_merge "$tmp_dir"

  echo ""
  if [ ${#failed_files[@]} -gt 0 ]; then
    echo "恢复完成（${#failed_files[@]} 个文件下载失败）"
    for ff in "${failed_files[@]}"; do
      echo "  - $ff"
    done
  else
    echo "恢复完成"
  fi
  echo "备份来源: $(to_user_path "${backup_remote}")"
  echo "文件数: ${total} 个"
  echo "恢复前备份: $safety_dir"
}

# ============================================================
# 帮助信息
# ============================================================
usage() {
  echo "Usage: memory-backup.sh <command> [options]"
  echo ""
  echo "Agent 记忆备份/恢复到百度网盘"
  echo "支持的 Agent：kimiclaw、maxclaw、qclaw、openclaw（自动检测）"
  echo ""
  echo "Commands:"
  echo "  backup                    备份当前 Agent 记忆到百度网盘"
  echo "  list                      列出网盘上所有可用的记忆备份"
  echo "  restore <date> [--force]  从百度网盘恢复指定日期的记忆（支持模糊匹配）"
  echo "  help                      显示帮助信息"
  echo ""
  echo "Examples:"
  echo "  bash memory-backup.sh backup"
  echo "  bash memory-backup.sh list"
  echo "  bash memory-backup.sh restore 2026-03-16"
  echo "  bash memory-backup.sh restore 2026-03 --force"
}

# ============================================================
# 主入口
# ============================================================
main() {
  if [ $# -eq 0 ]; then
    usage
    exit 0
  fi

  case "$1" in
    -V|--version)
      echo "$SCRIPT_VERSION"
      ;;
    -h|--help|help)
      usage
      ;;
    backup)
      detect_agent || {
        echo "不支持当前的 Agent 环境。" >&2
        echo "支持的 Agent 类型：kimiclaw、maxclaw、qclaw、openclaw" >&2
        exit 1
      }
      cmd_backup
      ;;
    list)
      detect_agent || {
        echo "不支持当前的 Agent 环境。" >&2
        echo "支持的 Agent 类型：kimiclaw、maxclaw、qclaw、openclaw" >&2
        exit 1
      }
      cmd_list
      ;;
    restore)
      shift
      detect_agent || {
        echo "不支持当前的 Agent 环境。" >&2
        echo "支持的 Agent 类型：kimiclaw、maxclaw、qclaw、openclaw" >&2
        exit 1
      }
      local force="false"
      local date_arg=""
      while [ $# -gt 0 ]; do
        case "$1" in
          --force|-f) force="true"; shift ;;
          -*) echo "未知选项: $1" >&2; exit 1 ;;
          *) date_arg="$1"; shift ;;
        esac
      done
      if [ -z "$date_arg" ]; then
        echo "用法: memory-backup.sh restore <date> [--force]" >&2
        echo "示例: memory-backup.sh restore 2026-03-16" >&2
        exit 1
      fi
      cmd_restore "$date_arg" "$force"
      ;;
    *)
      echo "未知命令: $1" >&2
      usage
      exit 1
      ;;
  esac
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi

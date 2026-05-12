#!/bin/bash
# baidu drive Skill 自动更新脚本
# 通过百度配置接口检测并更新 Skill 文件
# CLI 更新由 bdpan 自身管理，本脚本不负责

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

CONFIG_API="https://pan.baidu.com/act/v2/api/conf?conf_key=bd_skills"

# 脚本所在目录（用于定位 Skill 文件）
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION_FILE="${SKILL_DIR}/VERSION"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 版本比较：返回 0 表示 $1 > $2，1 表示 $1 = $2，2 表示 $1 < $2
version_compare() {
    if [ "$1" = "$2" ]; then
        return 1
    fi
    local IFS=.
    local i ver1=($1) ver2=($2)
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done
    for ((i=0; i<${#ver1[@]}; i++)); do
        if [ -z "${ver2[i]}" ]; then
            ver2[i]=0
        fi
        if ((10#${ver1[i]} > 10#${ver2[i]})); then
            return 0
        fi
        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 2
        fi
    done
    return 1
}

# 去除版本号的 v 前缀（如 v1.2.0 → 1.2.0）
strip_v_prefix() {
    echo "$1" | sed 's/^v//'
}

# 获取本地 Skill 版本
get_local_version() {
    if [ -f "$VERSION_FILE" ]; then
        local raw=$(cat "$VERSION_FILE" | tr -d '[:space:]')
        strip_v_prefix "$raw"
    else
        echo "unknown"
    fi
}

# 从 query string 中提取指定 key 的值
# 用法: query_get "version=1.1.2&url=https://..." "version"
query_get() {
    local qs="$1"
    local key="$2"
    echo "$qs" | tr '&' '\n' | while IFS='=' read -r k v; do
        if [ "$k" = "$key" ]; then
            echo "$v"
            return 0
        fi
    done
}

# 请求配置接口，返回 skills_info query string
fetch_skills_info() {
    local response=""

    if command -v curl &> /dev/null; then
        response=$(curl -fsSL --connect-timeout 10 --max-time 30 "$CONFIG_API" 2>/dev/null) || {
            log_error "无法连接配置服务器，请检查网络连接"
            return 1
        }
    elif command -v wget &> /dev/null; then
        response=$(wget -qO- --timeout=30 "$CONFIG_API" 2>/dev/null) || {
            log_error "无法连接配置服务器，请检查网络连接"
            return 1
        }
    else
        log_error "未找到 curl 或 wget"
        return 1
    fi

    # 检查 errno：从 JSON 中提取 "errno": 0
    local errno=$(echo "$response" | grep -o '"errno"[[:space:]]*:[[:space:]]*[0-9]*' | head -1 | grep -o '[0-9]*$')
    if [ "$errno" != "0" ]; then
        log_error "配置接口返回错误 (errno: ${errno:-unknown})"
        return 1
    fi

    # 从 response 中提取 skills_info 的值
    # API 返回中 & 可能被编码为 \u0026，需要还原
    local skills_info=$(echo "$response" | sed 's/\\u0026/\&/g' | grep -o 'version=[^"]*' | head -1 | sed 's/\\//g')

    if [ -z "$skills_info" ]; then
        log_error "未获取到版本配置信息"
        return 1
    fi

    echo "$skills_info"
}

# 更新 Skill
do_update() {
    local remote_url="$1"
    local remote_version="$2"

    if [ -z "$remote_url" ]; then
        log_error "未找到 Skill 下载地址"
        return 1
    fi

    log_info "正在下载 Skill 更新包 (v${remote_version})..."
    log_info "下载地址: ${remote_url}"

    # 创建临时目录
    local tmp_dir=$(mktemp -d)
    trap "rm -rf '$tmp_dir'" EXIT

    # 下载 zip
    local zip_path="${tmp_dir}/baidu-drive.zip"
    if command -v curl &> /dev/null; then
        curl -fsSL -o "$zip_path" "$remote_url" || {
            log_error "下载 Skill 更新包失败"
            return 1
        }
    elif command -v wget &> /dev/null; then
        wget -q -O "$zip_path" "$remote_url" || {
            log_error "下载 Skill 更新包失败"
            return 1
        }
    fi

    # SHA256 完整性校验（强制）
    local checksum=$(query_get "$SKILLS_INFO" "checksum")
    if [ -z "$checksum" ]; then
        log_error "配置接口未提供 checksum，无法验证更新包完整性，拒绝更新"
        return 1
    fi

    local actual=""
    if command -v sha256sum &> /dev/null; then
        actual=$(sha256sum "$zip_path" | awk '{print $1}')
    elif command -v shasum &> /dev/null; then
        actual=$(shasum -a 256 "$zip_path" | awk '{print $1}')
    else
        log_error "未找到 sha256sum/shasum 工具，无法验证更新包完整性"
        return 1
    fi

    if [ "$actual" != "$checksum" ]; then
        log_error "SHA256 校验失败！文件可能被篡改"
        log_error "  期望: ${checksum}"
        log_error "  实际: ${actual}"
        return 1
    fi
    log_info "SHA256 校验通过"

    # 解压覆盖
    log_info "正在解压更新..."
    if command -v unzip &> /dev/null; then
        unzip -qo "$zip_path" -d "$SKILL_DIR" || {
            log_error "解压失败"
            return 1
        }
    else
        log_error "未找到 unzip 工具"
        return 1
    fi

    # 更新 VERSION 文件
    echo "$remote_version" > "$VERSION_FILE"

    log_info "Skill 已更新到 v${remote_version}"
}

# 全局变量
SKILLS_INFO=""

# 主函数
main() {
    local check_only="no"
    local auto_yes="no"

    # 解析参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            --check|-c)
                check_only="yes"
                shift
                ;;
            --yes|-y)
                auto_yes="yes"
                shift
                ;;
            --help|-h)
                echo "用法: $0 [选项]"
                echo ""
                echo "选项:"
                echo "  --check, -c   仅检查更新，不执行"
                echo "  --yes, -y     跳过确认，自动更新"
                echo "  --help        显示帮助信息"
                exit 0
                ;;
            *)
                log_error "未知参数: $1"
                echo "使用 --help 查看帮助信息"
                exit 1
                ;;
        esac
    done

    # 获取本地版本
    local local_version=$(get_local_version)

    # 请求远程配置
    log_info "正在检查更新..."
    SKILLS_INFO=$(fetch_skills_info) || {
        log_warn "无法获取更新信息，请稍后再试"
        exit 1
    }

    # 解析远程版本和下载地址（strip v 前缀用于比较）
    local remote_version=$(query_get "$SKILLS_INFO" "version")
    local remote_version_clean=$(strip_v_prefix "$remote_version")
    local remote_url=$(query_get "$SKILLS_INFO" "url")

    if [ -z "$remote_version" ]; then
        log_error "配置中未包含版本信息"
        exit 1
    fi

    # 展示状态
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}  baidu drive Skill 更新检查${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo ""
    echo -e "  本地版本: ${local_version}"
    echo -e "  最新版本: ${remote_version}"

    # 版本对比
    local needs_update="no"
    if [ "$local_version" = "unknown" ]; then
        echo -e "  状态:     ${YELLOW}版本未知，建议更新${NC}"
        needs_update="yes"
    else
        set +e
        version_compare "$remote_version_clean" "$local_version"
        local cmp_result=$?
        set -e

        if [ $cmp_result -eq 0 ]; then
            echo -e "  状态:     ${YELLOW}有新版本可用${NC}"
            needs_update="yes"
        else
            echo -e "  状态:     ${GREEN}已是最新${NC}"
        fi
    fi

    echo ""

    # 无更新
    if [ "$needs_update" = "no" ]; then
        log_info "Skill 已是最新版本"
        exit 0
    fi

    # 仅检查模式
    if [ "$check_only" = "yes" ]; then
        exit 0
    fi

    # 用户确认
    # 安全限制：Agent 环境中禁止使用 --yes 跳过确认
    if [ "$auto_yes" = "yes" ]; then
        if [ -n "$CLAUDE_CODE" ] || [ -n "$ANTHROPIC_API_KEY" ] || [ -n "$MCP_SERVER" ]; then
            log_warn "检测到 Agent 环境，忽略 --yes 参数，保留用户确认环节"
            auto_yes="no"
        fi
    fi
    if [ "$auto_yes" != "yes" ]; then
        echo -n -e "${YELLOW}是否更新 Skill 到 v${remote_version}? [y/N] ${NC}"
        read -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            log_info "已取消更新"
            exit 0
        fi
    fi

    echo ""

    # 执行更新
    do_update "$remote_url" "$remote_version" || {
        log_error "Skill 更新失败"
        exit 1
    }

    echo ""
    echo -e "${GREEN}========================================${NC}"
    echo -e "${GREEN}  ✓ 更新完成${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
}

# 执行主函数
main "$@"

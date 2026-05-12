#!/bin/bash
# bdpan CLI 卸载脚本
# 清除 bdpan 二进制文件、配置文件和授权信息

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 默认路径
DEFAULT_INSTALL_DIR="$HOME/.local/bin"
DEFAULT_CONFIG_DIR="$HOME/.config/bdpan"

# 解析参数
SKIP_CONFIRM="no"
while [[ $# -gt 0 ]]; do
    case $1 in
        --yes|-y)
            SKIP_CONFIRM="yes"
            shift
            ;;
        --help|-h)
            echo "用法: $0 [选项]"
            echo ""
            echo "选项:"
            echo "  --yes, -y    跳过确认提示（自动化场景）"
            echo "  --help       显示帮助信息"
            echo ""
            echo "环境变量:"
            echo "  BDPAN_INSTALL_DIR  二进制安装目录（默认: ~/.local/bin）"
            echo "  BDPAN_CONFIG_DIR   配置文件目录（默认: ~/.config/bdpan）"
            exit 0
            ;;
        *)
            shift
            ;;
    esac
done

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 确定实际路径
INSTALL_DIR="${BDPAN_INSTALL_DIR:-$DEFAULT_INSTALL_DIR}"
CONFIG_DIR="${BDPAN_CONFIG_DIR:-$DEFAULT_CONFIG_DIR}"
BINARY_PATH="${INSTALL_DIR}/bdpan"

# 检测要清理的内容
echo ""
echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}  bdpan CLI 卸载${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

found_items=0

# 检查二进制文件
if [ -f "$BINARY_PATH" ]; then
    binary_version=$("$BINARY_PATH" version 2>/dev/null | head -1 || echo "unknown")
    echo -e "  二进制文件: ${GREEN}${BINARY_PATH}${NC} (${binary_version})"
    found_items=$((found_items + 1))
else
    # 尝试 which 查找
    actual_path=$(command -v bdpan 2>/dev/null || echo "")
    if [ -n "$actual_path" ]; then
        BINARY_PATH="$actual_path"
        binary_version=$("$BINARY_PATH" version 2>/dev/null | head -1 || echo "unknown")
        echo -e "  二进制文件: ${GREEN}${BINARY_PATH}${NC} (${binary_version})"
        found_items=$((found_items + 1))
    else
        echo -e "  二进制文件: ${YELLOW}未找到${NC}"
    fi
fi

# 检查配置目录
if [ -d "$CONFIG_DIR" ]; then
    config_files=$(find "$CONFIG_DIR" -type f 2>/dev/null | wc -l | tr -d ' ')
    echo -e "  配置目录:   ${GREEN}${CONFIG_DIR}/${NC} (${config_files} 个文件)"
    found_items=$((found_items + 1))

    # 检查是否有活跃的登录态
    if [ -f "${CONFIG_DIR}/config.json" ]; then
        if command -v bdpan &> /dev/null && bdpan whoami 2>/dev/null | grep -q "已登录"; then
            echo -e "  登录状态:   ${RED}已登录（将清除授权信息）${NC}"
        fi
    fi
else
    echo -e "  配置目录:   ${YELLOW}未找到${NC}"
fi

echo ""

# 无内容可清理
if [ "$found_items" -eq 0 ]; then
    log_info "未检测到 bdpan 安装，无需卸载"
    exit 0
fi

# 用户确认
if [ "$SKIP_CONFIRM" != "yes" ]; then
    echo -e "${RED}以上内容将被永久删除，此操作不可逆！${NC}"
    echo ""
    echo -n -e "${YELLOW}确认卸载 bdpan CLI? [y/N] ${NC}"
    read -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        log_info "已取消卸载"
        exit 0
    fi
fi

echo ""

# 1. 注销登录（清除服务端 session，如有）
if command -v bdpan &> /dev/null && bdpan whoami 2>/dev/null | grep -q "已登录"; then
    log_info "正在注销登录..."
    bdpan logout 2>/dev/null || true
    log_info "✓ 已注销登录"
fi

# 2. 删除配置目录（含 token、config.json 等）
if [ -d "$CONFIG_DIR" ]; then
    log_info "正在删除配置目录: ${CONFIG_DIR}/"
    rm -rf "$CONFIG_DIR"
    log_info "✓ 配置目录已删除"
fi

# 3. 删除二进制文件
if [ -f "$BINARY_PATH" ]; then
    log_info "正在删除二进制文件: ${BINARY_PATH}"
    rm -f "$BINARY_PATH"
    log_info "✓ 二进制文件已删除"
fi

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  ✓ bdpan CLI 已完全卸载${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "已清理:"
echo "  - 二进制文件 (bdpan)"
echo "  - 配置文件和授权信息 (~/.config/bdpan/)"
echo ""

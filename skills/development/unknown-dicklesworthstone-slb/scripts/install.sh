#!/bin/bash
# SLB Installation Script
# Downloads and installs the latest release of SLB

set -euo pipefail

# Configuration
REPO="Dicklesworthstone/slb"
INSTALL_DIR="${INSTALL_DIR:-/usr/local/bin}"
BINARY="slb"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1" >&2; exit 1; }

# Detect OS and architecture
detect_platform() {
    OS="$(uname -s | tr '[:upper:]' '[:lower:]')"
    ARCH="$(uname -m)"

    case "$OS" in
        linux) OS="linux" ;;
        darwin) OS="darwin" ;;
        mingw*|msys*|cygwin*) OS="windows" ;;
        *) error "Unsupported OS: $OS" ;;
    esac

    case "$ARCH" in
        x86_64|amd64) ARCH="amd64" ;;
        arm64|aarch64) ARCH="arm64" ;;
        *) error "Unsupported architecture: $ARCH" ;;
    esac

    PLATFORM="${OS}_${ARCH}"
    info "Detected platform: $PLATFORM"
}

# Get latest release version
get_latest_version() {
    info "Fetching latest version..."
    VERSION=$(curl -fsSL "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name":' | sed -E 's/.*"([^"]+)".*/\1/')
    if [ -z "$VERSION" ]; then
        error "Failed to fetch latest version"
    fi
    info "Latest version: $VERSION"
}

# Download and install
install() {
    local EXT="tar.gz"
    if [ "$OS" = "windows" ]; then
        EXT="zip"
    fi

    local ARCHIVE="${BINARY}_${VERSION#v}_${PLATFORM}.${EXT}"
    local URL="https://github.com/${REPO}/releases/download/${VERSION}/${ARCHIVE}"

    info "Downloading $URL..."
    TMPDIR="$(mktemp -d)"
    trap 'rm -rf "$TMPDIR"' EXIT

    if ! curl -fsSL -o "${TMPDIR}/${ARCHIVE}" "$URL"; then
        error "Failed to download $URL"
    fi

    info "Extracting..."
    if [ "$EXT" = "tar.gz" ]; then
        tar -xzf "${TMPDIR}/${ARCHIVE}" -C "$TMPDIR"
    else
        if ! command -v unzip >/dev/null 2>&1; then
            error "unzip is required to install Windows releases"
        fi
        unzip -q "${TMPDIR}/${ARCHIVE}" -d "$TMPDIR"
    fi

    info "Installing to ${INSTALL_DIR}..."
    if [ -w "$INSTALL_DIR" ]; then
        cp "${TMPDIR}/${BINARY}" "${INSTALL_DIR}/${BINARY}"
        chmod +x "${INSTALL_DIR}/${BINARY}"
    else
        warn "Installing to ${INSTALL_DIR} requires sudo"
        sudo cp "${TMPDIR}/${BINARY}" "${INSTALL_DIR}/${BINARY}"
        sudo chmod +x "${INSTALL_DIR}/${BINARY}"
    fi

    success "Installed ${BINARY} to ${INSTALL_DIR}/${BINARY}"
}

# Verify installation
verify() {
    if command -v "$BINARY" &> /dev/null; then
        info "Verifying installation..."
        "$BINARY" version
        success "SLB installed successfully!"
    else
        warn "Binary not in PATH. You may need to add ${INSTALL_DIR} to your PATH."
    fi
}

# Main
main() {
    echo ""
    echo "╔══════════════════════════════════════╗"
    echo "║   SIMULTANEOUS LAUNCH BUTTON (SLB)   ║"
    echo "║           Installation Script        ║"
    echo "╚══════════════════════════════════════╝"
    echo ""

    detect_platform
    get_latest_version
    install
    verify

    echo ""
    info "Get started:"
    echo "  slb init              # Initialize SLB in current directory"
    echo "  slb daemon start      # Start approval daemon"
    echo "  slb run \"<command>\"   # Submit command for approval"
    echo ""
    echo "Tip: You can also install via Homebrew:"
    echo "  brew install dicklesworthstone/tap/slb"
    echo ""
}

main

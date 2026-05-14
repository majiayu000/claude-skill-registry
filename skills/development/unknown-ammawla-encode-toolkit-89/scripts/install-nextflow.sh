#!/usr/bin/env bash
# Install Nextflow and container runtime for ENCODE pipelines
# Usage: bash install-nextflow.sh [--docker | --singularity | --both]
#
# Options:
#   --docker       Install Nextflow + Docker (default, for local/cloud)
#   --singularity  Install Nextflow + Singularity (for HPC clusters)
#   --both         Install Nextflow + Docker + Singularity

set -euo pipefail

echo "============================================"
echo "ENCODE Nextflow Pipeline Infrastructure Setup"
echo "============================================"
echo ""

MODE="${1:---docker}"

# --- Install Nextflow ---
install_nextflow() {
    echo "--- Installing Nextflow ---"
    if command -v nextflow &> /dev/null; then
        echo "Nextflow already installed: $(nextflow -version 2>&1 | head -3)"
    else
        # Check Java
        if ! command -v java &> /dev/null; then
            echo "ERROR: Java 11+ is required for Nextflow."
            echo "Install Java first:"
            echo "  macOS:  brew install openjdk@17"
            echo "  Ubuntu: sudo apt-get install -y openjdk-17-jdk"
            echo "  conda:  conda install -c conda-forge openjdk>=11"
            exit 1
        fi

        JAVA_VER=$(java -version 2>&1 | head -1 | awk -F '"' '{print $2}' | awk -F '.' '{print $1}')
        if [ "$JAVA_VER" -lt 11 ] 2>/dev/null; then
            echo "WARNING: Java $JAVA_VER detected. Nextflow requires Java 11+."
        fi

        echo "Downloading Nextflow..."
        curl -s https://get.nextflow.io | bash

        # Move to a directory in PATH
        if [ -w /usr/local/bin ]; then
            mv nextflow /usr/local/bin/
            echo "Nextflow installed to /usr/local/bin/nextflow"
        else
            mkdir -p "$HOME/.local/bin"
            mv nextflow "$HOME/.local/bin/"
            echo "Nextflow installed to $HOME/.local/bin/nextflow"
            echo "Add to PATH: export PATH=\$PATH:\$HOME/.local/bin"
        fi

        nextflow -version
    fi
    echo ""
}

# --- Install Docker ---
install_docker() {
    echo "--- Checking Docker ---"
    if command -v docker &> /dev/null; then
        echo "Docker already installed: $(docker --version)"
    else
        OS="$(uname -s)"
        case "$OS" in
            Darwin)
                echo "macOS detected. Install Docker Desktop:"
                echo "  brew install --cask docker"
                echo "  OR download from https://www.docker.com/products/docker-desktop/"
                ;;
            Linux)
                echo "Linux detected. Install Docker Engine:"
                echo "  curl -fsSL https://get.docker.com | sh"
                echo "  sudo usermod -aG docker \$USER"
                echo "  newgrp docker"
                ;;
            *)
                echo "Unsupported OS: $OS"
                echo "See https://docs.docker.com/get-docker/"
                ;;
        esac
    fi
    echo ""
}

# --- Install Singularity ---
install_singularity() {
    echo "--- Checking Singularity ---"
    if command -v singularity &> /dev/null; then
        echo "Singularity already installed: $(singularity --version)"
    elif command -v apptainer &> /dev/null; then
        echo "Apptainer (Singularity successor) already installed: $(apptainer --version)"
    else
        echo "Singularity/Apptainer not found."
        echo "For HPC clusters, check: module avail singularity"
        echo ""
        echo "Install options:"
        echo "  conda: conda install -c conda-forge singularity"
        echo "  Linux: See https://apptainer.org/docs/admin/main/installation.html"
        echo ""
        echo "NOTE: Singularity requires Linux. On macOS, use Docker or a Linux VM."
    fi
    echo ""
}

# --- Execute ---
install_nextflow

case "$MODE" in
    --docker)
        install_docker
        ;;
    --singularity)
        install_singularity
        ;;
    --both)
        install_docker
        install_singularity
        ;;
    *)
        echo "Unknown mode: $MODE"
        echo "Usage: bash install-nextflow.sh [--docker | --singularity | --both]"
        exit 1
        ;;
esac

echo "============================================"
echo "Pipeline infrastructure setup complete."
echo ""
echo "Test with:"
echo "  nextflow run hello"
echo ""
echo "Run ENCODE pipelines with:"
echo "  nextflow run main.nf -profile local    # Docker"
echo "  nextflow run main.nf -profile slurm    # Singularity + SLURM"
echo "============================================"

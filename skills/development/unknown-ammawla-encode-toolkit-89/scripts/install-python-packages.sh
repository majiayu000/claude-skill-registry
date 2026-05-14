#!/usr/bin/env bash
# Install Python packages for ENCODE data analysis
# Usage: bash install-python-packages.sh [--all | --singlecell | --hic | --deeptools | --genomics]
#
# Categories:
#   --all          Install all packages (default if no argument)
#   --singlecell   scanpy, scvi-tools, harmony-pytorch, scrublet, scanorama, bbknn
#   --hic          cooler, cooltools, hic-straw, pyGenomeTracks
#   --deeptools    deeptools, pyBigWig, pysam, pybedtools
#   --genomics     Core genomics (numpy, pandas, scipy, matplotlib, seaborn)

set -euo pipefail

echo "============================================"
echo "ENCODE Bioinformatics Python Package Installer"
echo "============================================"
echo ""
echo "Python: $(python3 --version 2>&1)"
echo "pip:    $(pip3 --version 2>&1 | head -1)"
echo ""

CATEGORY="${1:---all}"

install_genomics() {
    echo "--- Installing Core Genomics packages ---"
    pip3 install --upgrade \
        numpy \
        pandas \
        scipy \
        matplotlib \
        seaborn \
        scikit-learn \
        statsmodels \
        h5py \
        loompy
}

install_singlecell() {
    echo "--- Installing Single-Cell packages ---"
    pip3 install --upgrade \
        scanpy \
        anndata \
        scvi-tools \
        scrublet \
        scanorama \
        bbknn \
        harmony-pytorch \
        leidenalg \
        louvain \
        umap-learn
    echo ""
    echo "NOTE: CellBender requires separate install (GPU recommended):"
    echo "  pip install cellbender"
}

install_hic() {
    echo "--- Installing Hi-C Analysis packages ---"
    pip3 install --upgrade \
        cooler \
        cooltools \
        hic-straw \
        pyGenomeTracks \
        bioframe
}

install_deeptools() {
    echo "--- Installing Genomics / Signal Processing packages ---"
    pip3 install --upgrade \
        deeptools \
        pyBigWig \
        pysam \
        pybedtools
}

case "$CATEGORY" in
    --all)
        install_genomics
        install_singlecell
        install_hic
        install_deeptools
        ;;
    --singlecell)
        install_genomics
        install_singlecell
        ;;
    --hic)
        install_genomics
        install_hic
        ;;
    --deeptools)
        install_genomics
        install_deeptools
        ;;
    --genomics)
        install_genomics
        ;;
    *)
        echo "Unknown category: $CATEGORY"
        echo "Usage: bash install-python-packages.sh [--all | --singlecell | --hic | --deeptools | --genomics]"
        exit 1
        ;;
esac

echo ""
echo "============================================"
echo "Python package installation complete."
echo "============================================"

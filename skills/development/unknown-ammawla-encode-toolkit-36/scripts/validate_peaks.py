#!/usr/bin/env python3
"""Validate narrowPeak/broadPeak files from ENCODE histone aggregation.

Checks file format, coordinate validity, chromosome names, blacklist overlap,
signal values, and reports summary statistics with warnings for suspicious patterns.

Usage:
    python validate_peaks.py input.narrowPeak [--blacklist hg38-blacklist.v2.bed] [--format narrow|broad]
    python validate_peaks.py input.broadPeak --format broad
    python validate_peaks.py input.narrowPeak --blacklist hg38-blacklist.v2.bed --format narrow
"""

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY", "chrM"}
NARROW_COLS = 10
BROAD_COLS = 9


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate narrowPeak/broadPeak BED files from ENCODE histone aggregation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python validate_peaks.py sample.narrowPeak\n"
            "  python validate_peaks.py sample.broadPeak --format broad\n"
            "  python validate_peaks.py sample.narrowPeak --blacklist hg38-blacklist.v2.bed\n"
        ),
    )
    parser.add_argument("input", type=Path, help="Input narrowPeak or broadPeak file")
    parser.add_argument(
        "--blacklist",
        type=Path,
        default=None,
        help="ENCODE blacklist BED file (e.g., hg38-blacklist.v2.bed)",
    )
    parser.add_argument(
        "--format",
        choices=["narrow", "broad"],
        default="narrow",
        help="Peak format: narrow (10 cols) or broad (9 cols). Default: narrow",
    )
    return parser.parse_args()


def load_blacklist(path):
    """Load blacklist regions as a dict of chrom -> list of (start, end)."""
    regions = defaultdict(list)
    with open(path) as f:
        for line in f:
            if line.startswith("#") or line.strip() == "":
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 3:
                regions[parts[0]].append((int(parts[1]), int(parts[2])))
    # Sort intervals for binary search
    for chrom in regions:
        regions[chrom].sort()
    return regions


def overlaps_blacklist(chrom, start, end, blacklist):
    """Check if a region overlaps any blacklist interval (linear scan)."""
    if chrom not in blacklist:
        return False
    for bl_start, bl_end in blacklist[chrom]:
        if bl_start >= end:
            break
        if bl_end > start:
            return True
    return False


def validate_peaks(input_path, blacklist_path, peak_format):
    expected_cols = NARROW_COLS if peak_format == "narrow" else BROAD_COLS
    format_name = "narrowPeak" if peak_format == "narrow" else "broadPeak"

    errors = []
    warnings = []
    chrom_counts = Counter()
    peak_sizes = []
    signal_values = []
    p_values = []
    q_values = []
    total_lines = 0
    bad_lines = 0
    blacklist_overlaps = 0
    chrm_peaks = 0
    large_peaks = 0
    large_threshold = 10000 if peak_format == "narrow" else 500000

    blacklist = None
    if blacklist_path:
        if not blacklist_path.exists():
            print(f"ERROR: Blacklist file not found: {blacklist_path}", file=sys.stderr)
            sys.exit(1)
        blacklist = load_blacklist(blacklist_path)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    with open(input_path) as f:
        for line_num, line in enumerate(f, 1):
            if line.startswith("#") or line.startswith("track") or line.startswith("browser"):
                continue
            line = line.strip()
            if not line:
                continue

            total_lines += 1
            fields = line.split("\t")

            # Column count check
            if len(fields) < expected_cols:
                errors.append(f"Line {line_num}: expected {expected_cols} columns ({format_name}), got {len(fields)}")
                bad_lines += 1
                if bad_lines <= 5:
                    continue
                elif bad_lines == 6:
                    errors.append("... suppressing further column-count errors")
                continue

            chrom = fields[0]
            # Chromosome validation
            if chrom not in VALID_CHROMS:
                if not chrom.startswith("chr"):
                    errors.append(f"Line {line_num}: invalid chromosome '{chrom}'")
                    bad_lines += 1
                    continue
                else:
                    warnings.append(
                        f"Line {line_num}: non-standard chromosome '{chrom}' (not in chr1-22, chrX, chrY, chrM)"
                    )
                    if len(warnings) > 20:
                        warnings = warnings[:20]
                        warnings.append("... suppressing further warnings")

            # Coordinate validation
            try:
                start = int(fields[1])
                end = int(fields[2])
            except ValueError:
                errors.append(f"Line {line_num}: non-integer coordinates")
                bad_lines += 1
                continue

            if start < 0:
                errors.append(f"Line {line_num}: negative start coordinate ({start})")
            if end < 0:
                errors.append(f"Line {line_num}: negative end coordinate ({end})")
            if start >= end:
                errors.append(f"Line {line_num}: start ({start}) >= end ({end})")

            peak_size = end - start
            peak_sizes.append(peak_size)
            chrom_counts[chrom] += 1

            if chrom == "chrM":
                chrm_peaks += 1
            if peak_size > large_threshold:
                large_peaks += 1

            # Signal/score validation (columns 5, 7, 8, 9 in narrowPeak)
            # Col 5 = score (int 0-1000), Col 7 = signalValue (float),
            # Col 8 = pValue (float, -log10), Col 9 = qValue (float, -log10)
            try:
                signal_val = float(fields[6])
                signal_values.append(signal_val)
                if signal_val < 0:
                    errors.append(f"Line {line_num}: negative signalValue ({signal_val})")
            except (ValueError, IndexError):
                errors.append(f"Line {line_num}: invalid signalValue in column 7")

            try:
                p_val = float(fields[7])
                p_values.append(p_val)
            except (ValueError, IndexError):
                errors.append(f"Line {line_num}: invalid pValue in column 8")

            try:
                q_val = float(fields[8])
                q_values.append(q_val)
            except (ValueError, IndexError):
                errors.append(f"Line {line_num}: invalid qValue in column 9")

            # Blacklist overlap check
            if blacklist and overlaps_blacklist(chrom, start, end, blacklist):
                blacklist_overlaps += 1

    # --- Report Statistics ---
    print(f"=== {format_name} Validation Report ===")
    print(f"File: {input_path}")
    print(f"Format: {format_name} (expected {expected_cols} columns)")
    print()

    print("--- Summary ---")
    print(f"Total peaks: {total_lines:,}")
    print(f"Malformed lines: {bad_lines}")
    if blacklist_path:
        print(f"Blacklist overlaps: {blacklist_overlaps:,} ({100 * blacklist_overlaps / max(total_lines, 1):.1f}%)")
    print()

    if peak_sizes:
        sorted_sizes = sorted(peak_sizes)
        median_idx = len(sorted_sizes) // 2
        print("--- Peak Size Distribution ---")
        print(f"Min:    {sorted_sizes[0]:,} bp")
        print(f"25th:   {sorted_sizes[len(sorted_sizes) // 4]:,} bp")
        print(f"Median: {sorted_sizes[median_idx]:,} bp")
        print(f"75th:   {sorted_sizes[3 * len(sorted_sizes) // 4]:,} bp")
        print(f"Max:    {sorted_sizes[-1]:,} bp")
        print()

    if signal_values:
        sorted_sig = sorted(signal_values)
        sig_median = sorted_sig[len(sorted_sig) // 2]
        print("--- SignalValue Distribution ---")
        print(f"Min:    {sorted_sig[0]:.2f}")
        print(f"25th:   {sorted_sig[len(sorted_sig) // 4]:.2f}")
        print(f"Median: {sig_median:.2f}")
        print(f"75th:   {sorted_sig[3 * len(sorted_sig) // 4]:.2f}")
        print(f"Max:    {sorted_sig[-1]:.2f}")
        print()

    print("--- Chromosome Distribution ---")
    for chrom in sorted(chrom_counts.keys(), key=lambda c: (len(c), c)):
        count = chrom_counts[chrom]
        pct = 100 * count / max(total_lines, 1)
        print(f"  {chrom:<6} {count:>8,}  ({pct:5.1f}%)")
    print()

    # --- Warnings ---
    if chrm_peaks > 0:
        msg = f"WARNING: {chrm_peaks:,} peaks on chrM. Mitochondrial peaks are often artifacts in ChIP-seq data."
        print(msg, file=sys.stderr)
    if large_peaks > 0:
        threshold_label = "10kb" if peak_format == "narrow" else "500kb"
        msg = (
            f"WARNING: {large_peaks:,} peaks exceed {threshold_label}. "
            f"For {format_name}, this may indicate broad mark contamination "
            f"or artifact regions."
        )
        print(msg, file=sys.stderr)
    if blacklist_overlaps > 0:
        msg = (
            f"WARNING: {blacklist_overlaps:,} peaks overlap ENCODE blacklist regions. "
            f"These should be removed before aggregation."
        )
        print(msg, file=sys.stderr)

    for w in warnings[:20]:
        print(w, file=sys.stderr)

    # --- Errors ---
    if errors:
        print(f"\n--- Errors ({len(errors)}) ---", file=sys.stderr)
        for e in errors[:50]:
            print(f"  {e}", file=sys.stderr)
        if len(errors) > 50:
            print(f"  ... and {len(errors) - 50} more errors", file=sys.stderr)

    has_errors = len(errors) > 0
    if has_errors:
        print(f"\nRESULT: FAIL — {len(errors)} error(s) found", file=sys.stderr)
    else:
        print(f"\nRESULT: PASS — file is valid {format_name}")

    return 1 if has_errors else 0


if __name__ == "__main__":
    args = parse_args()
    exit_code = validate_peaks(args.input, args.blacklist, args.format)
    sys.exit(exit_code)

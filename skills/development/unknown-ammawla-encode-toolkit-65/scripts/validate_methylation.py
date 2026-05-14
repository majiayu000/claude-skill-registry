#!/usr/bin/env python3
"""Validate bedMethyl files from ENCODE WGBS methylation aggregation.

Checks bedMethyl format, methylation value ranges, strand validity, coverage
values, and reports summary statistics with warnings for low-coverage sites.

Usage:
    python validate_methylation.py input.bedMethyl [--min-coverage 5] [--blacklist hg38-blacklist.v2.bed]
    python validate_methylation.py input.bed --min-coverage 10
"""

import argparse
import sys
from collections import Counter, defaultdict
from pathlib import Path

VALID_CHROMS = {f"chr{i}" for i in range(1, 23)} | {"chrX", "chrY", "chrM"}
VALID_STRANDS = {"+", "-", "."}

# ENCODE bedMethyl format has 11 columns:
# chr start end name score strand thickStart thickEnd color coverage percentMethylated
BEDMETHYL_COLS = 11

# Alternative minimal format: chr start end name score strand coverage methylation%
MINIMAL_COLS = 8


def parse_args():
    parser = argparse.ArgumentParser(
        description="Validate bedMethyl files from ENCODE WGBS methylation aggregation.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python validate_methylation.py sample.bedMethyl\n"
            "  python validate_methylation.py sample.bedMethyl --min-coverage 10\n"
            "  python validate_methylation.py sample.bed --blacklist hg38-blacklist.v2.bed\n"
        ),
    )
    parser.add_argument("input", type=Path, help="Input bedMethyl file")
    parser.add_argument(
        "--min-coverage",
        type=int,
        default=5,
        help="Minimum coverage threshold to flag low-coverage CpGs. Default: 5",
    )
    parser.add_argument(
        "--blacklist",
        type=Path,
        default=None,
        help="ENCODE blacklist BED file (e.g., hg38-blacklist.v2.bed)",
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
    for chrom in regions:
        regions[chrom].sort()
    return regions


def overlaps_blacklist(chrom, start, end, blacklist):
    """Check if a region overlaps any blacklist interval."""
    if chrom not in blacklist:
        return False
    for bl_start, bl_end in blacklist[chrom]:
        if bl_start >= end:
            break
        if bl_end > start:
            return True
    return False


def detect_format(first_data_line):
    """Detect whether the file is ENCODE bedMethyl (11 cols) or minimal format (8 cols)."""
    fields = first_data_line.strip().split("\t")
    n_cols = len(fields)
    if n_cols >= BEDMETHYL_COLS:
        return "encode_bedmethyl", BEDMETHYL_COLS
    elif n_cols >= MINIMAL_COLS:
        return "minimal", MINIMAL_COLS
    else:
        return "unknown", n_cols


def validate_methylation(input_path, min_coverage, blacklist_path):
    errors = []
    warnings = []
    chrom_counts = Counter()
    strand_counts = Counter()
    coverage_values = []
    methylation_values = []
    total_lines = 0
    bad_lines = 0
    low_coverage = 0
    blacklist_overlaps = 0
    fraction_format_detected = False
    percentage_format_detected = False

    blacklist = None
    if blacklist_path:
        if not blacklist_path.exists():
            print(f"ERROR: Blacklist file not found: {blacklist_path}", file=sys.stderr)
            sys.exit(1)
        blacklist = load_blacklist(blacklist_path)

    if not input_path.exists():
        print(f"ERROR: Input file not found: {input_path}", file=sys.stderr)
        sys.exit(1)

    # Detect format from first data line
    detected_format = None
    expected_cols = None
    cov_col = None  # 0-indexed column for coverage
    meth_col = None  # 0-indexed column for methylation %

    with open(input_path) as f:
        for line in f:
            if line.startswith("#") or line.startswith("track") or line.startswith("browser"):
                continue
            line = line.strip()
            if not line:
                continue
            detected_format, expected_cols = detect_format(line)
            break

    if detected_format == "encode_bedmethyl":
        cov_col = 9  # Column 10 (0-indexed: 9)
        meth_col = 10  # Column 11 (0-indexed: 10)
    elif detected_format == "minimal":
        cov_col = 6  # Column 7
        meth_col = 7  # Column 8
    else:
        print(
            f"ERROR: Could not detect bedMethyl format. "
            f"Expected 11 columns (ENCODE) or 8 columns (minimal), got {expected_cols}",
            file=sys.stderr,
        )
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

            if len(fields) < expected_cols:
                errors.append(
                    f"Line {line_num}: expected {expected_cols} columns ({detected_format}), got {len(fields)}"
                )
                bad_lines += 1
                if bad_lines > 5:
                    if bad_lines == 6:
                        errors.append("... suppressing further column-count errors")
                    continue
                continue

            chrom = fields[0]
            if chrom not in VALID_CHROMS:
                if not chrom.startswith("chr"):
                    errors.append(f"Line {line_num}: invalid chromosome '{chrom}'")
                    bad_lines += 1
                    continue

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

            chrom_counts[chrom] += 1

            # Strand validation
            strand_field_idx = 5
            if len(fields) > strand_field_idx:
                strand = fields[strand_field_idx]
                if strand not in VALID_STRANDS:
                    errors.append(f"Line {line_num}: invalid strand '{strand}' (expected +, -, or .)")
                strand_counts[strand] += 1

            # Coverage validation
            try:
                coverage = int(fields[cov_col])
                if coverage < 0:
                    errors.append(f"Line {line_num}: negative coverage ({coverage})")
                else:
                    coverage_values.append(coverage)
                    if coverage < min_coverage:
                        low_coverage += 1
            except (ValueError, IndexError):
                # Try float then round (some tools output float coverage)
                try:
                    coverage = float(fields[cov_col])
                    if coverage < 0:
                        errors.append(f"Line {line_num}: negative coverage ({coverage})")
                    else:
                        coverage_values.append(int(coverage))
                        if coverage < min_coverage:
                            low_coverage += 1
                except (ValueError, IndexError):
                    errors.append(f"Line {line_num}: invalid coverage in column {cov_col + 1}")

            # Methylation value validation
            try:
                meth = float(fields[meth_col])
                if meth < 0:
                    errors.append(f"Line {line_num}: negative methylation value ({meth})")
                elif meth > 100:
                    errors.append(
                        f"Line {line_num}: methylation value > 100 ({meth}). "
                        f"Expected 0-100 (percentage) or 0-1 (fraction)."
                    )
                elif meth <= 1.0 and meth > 0:
                    fraction_format_detected = True
                elif meth > 1.0:
                    percentage_format_detected = True

                # Store as percentage for consistent reporting
                if meth <= 1.0:
                    methylation_values.append(meth * 100)
                else:
                    methylation_values.append(meth)
            except (ValueError, IndexError):
                errors.append(f"Line {line_num}: invalid methylation value in column {meth_col + 1}")

            # Blacklist overlap check
            if blacklist and overlaps_blacklist(chrom, start, end, blacklist):
                blacklist_overlaps += 1

    # --- Report Statistics ---
    print("=== bedMethyl Validation Report ===")
    print(f"File: {input_path}")
    print(f"Detected format: {detected_format} ({expected_cols} columns)")
    print()

    print("--- Summary ---")
    print(f"Total CpGs: {total_lines:,}")
    print(f"Malformed lines: {bad_lines}")
    print(f"Low-coverage CpGs (<{min_coverage}x): {low_coverage:,} ({100 * low_coverage / max(total_lines, 1):.1f}%)")
    if blacklist_path:
        print(f"Blacklist overlaps: {blacklist_overlaps:,} ({100 * blacklist_overlaps / max(total_lines, 1):.1f}%)")
    print()

    # Methylation format detection
    if fraction_format_detected and percentage_format_detected:
        msg = (
            "WARNING: Mixed methylation formats detected. Some values appear "
            "to be fractions (0-1) and others percentages (0-100). Normalize "
            "before aggregation."
        )
        print(msg, file=sys.stderr)
    elif fraction_format_detected:
        print("Methylation format: fraction (0-1)")
    else:
        print("Methylation format: percentage (0-100)")
    print()

    if coverage_values:
        sorted_cov = sorted(coverage_values)
        n = len(sorted_cov)
        print("--- Coverage Distribution ---")
        print(f"Min:    {sorted_cov[0]:>6}")
        print(f"25th:   {sorted_cov[n // 4]:>6}")
        print(f"Median: {sorted_cov[n // 2]:>6}")
        print(f"75th:   {sorted_cov[3 * n // 4]:>6}")
        print(f"Max:    {sorted_cov[-1]:>6}")

        # Coverage buckets
        buckets = [
            ("<3x", 0, 3),
            ("3-5x", 3, 5),
            ("5-10x", 5, 10),
            ("10-20x", 10, 20),
            ("20-50x", 20, 50),
            (">50x", 50, float("inf")),
        ]
        print("\n  Coverage buckets:")
        for label, lo, hi in buckets:
            count = sum(1 for c in coverage_values if lo <= c < hi)
            print(f"    {label:<8} {count:>10,}  ({100 * count / n:.1f}%)")
        print()

    if methylation_values:
        sorted_meth = sorted(methylation_values)
        n_m = len(sorted_meth)
        print("--- Methylation Distribution (as %) ---")
        print(f"Min:    {sorted_meth[0]:>6.1f}%")
        print(f"25th:   {sorted_meth[n_m // 4]:>6.1f}%")
        print(f"Median: {sorted_meth[n_m // 2]:>6.1f}%")
        print(f"75th:   {sorted_meth[3 * n_m // 4]:>6.1f}%")
        print(f"Max:    {sorted_meth[-1]:>6.1f}%")

        # Methylation state buckets
        buckets = [
            ("Unmethylated (0-10%)", 0, 10),
            ("Low (10-30%)", 10, 30),
            ("Intermediate (30-70%)", 30, 70),
            ("High (70-90%)", 70, 90),
            ("Methylated (90-100%)", 90, 100.01),
        ]
        print("\n  Methylation state distribution:")
        for label, lo, hi in buckets:
            count = sum(1 for m in methylation_values if lo <= m < hi)
            print(f"    {label:<30} {count:>10,}  ({100 * count / n_m:.1f}%)")
        print()

    print("--- Strand Breakdown ---")
    for strand in ["+", "-", "."]:
        count = strand_counts.get(strand, 0)
        pct = 100 * count / max(total_lines, 1)
        print(f"  {strand:<3} {count:>10,}  ({pct:5.1f}%)")
    print()

    print("--- Chromosome Distribution ---")
    for chrom in sorted(chrom_counts.keys(), key=lambda c: (len(c), c)):
        count = chrom_counts[chrom]
        pct = 100 * count / max(total_lines, 1)
        print(f"  {chrom:<6} {count:>10,}  ({pct:5.1f}%)")
    print()

    # --- Warnings ---
    if low_coverage > total_lines * 0.3:
        msg = (
            f"WARNING: {100 * low_coverage / max(total_lines, 1):.0f}% of CpGs have "
            f"coverage <{min_coverage}x. Consider filtering these for reliable "
            f"methylation estimates."
        )
        print(msg, file=sys.stderr)

    if strand_counts.get(".", 0) == total_lines:
        msg = (
            "INFO: All CpGs have strand '.'. This file may already be strand-merged. "
            "Skip the strand-merge step in aggregation."
        )
        print(msg, file=sys.stderr)
    elif strand_counts.get("+", 0) > 0 and strand_counts.get("-", 0) > 0:
        plus_count = strand_counts.get("+", 0)
        minus_count = strand_counts.get("-", 0)
        ratio = plus_count / max(minus_count, 1)
        if 0.8 <= ratio <= 1.2:
            msg = (
                f"INFO: Both strands present ({plus_count:,} forward, {minus_count:,} reverse). "
                f"Consider strand-merging for increased per-CpG coverage."
            )
            print(msg, file=sys.stderr)

    if blacklist_overlaps > 0:
        msg = f"WARNING: {blacklist_overlaps:,} CpGs overlap ENCODE blacklist regions. Remove these before aggregation."
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
        print(f"\nRESULT: FAIL -- {len(errors)} error(s) found", file=sys.stderr)
    else:
        print(f"\nRESULT: PASS -- file is valid {detected_format}")

    return 1 if has_errors else 0


if __name__ == "__main__":
    args = parse_args()
    exit_code = validate_methylation(args.input, args.min_coverage, args.blacklist)
    sys.exit(exit_code)

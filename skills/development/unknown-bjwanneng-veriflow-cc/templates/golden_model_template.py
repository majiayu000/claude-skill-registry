"""golden_model.py — Golden reference model for <design_name>.

Pure Python implementation. No external dependencies.
Provides: algorithm, test vectors, run() -> cycle-accurate expected values.

Two modes:
  - compute(inputs, trace=False) -> dict   : final outputs only (for testbench)
  - compute(inputs, trace=True)  -> list   : per-cycle state (for vcd2table diff)
  - run()                        -> list   : standard interface for pipeline
"""
from __future__ import annotations

# --- Constants ---
# (algorithm-specific constants: IV, T_j, state encodings, etc.)

MASK32 = 0xFFFFFFFF  # common for 32-bit datapaths; adjust per design


# --- Bit manipulation / helper functions ---
# (ROL, P0, P1, FF, GG, etc. — only what the algorithm needs)
# Keep these as standalone functions, not class methods.

def ROL(x: int, n: int, width: int = 32) -> int:
    """Left rotate for width-bit values."""
    n = n % width
    return ((x << n) | (x >> (width - n))) & ((1 << width) - 1)


# --- Core algorithm ---
def compute(inputs: dict, trace: bool = False) -> dict | list[dict]:
    """Execute the algorithm.

    Args:
        inputs: dict with input signal names -> values.
                Example for hash cores:
                  {"blocks": [block0_int, ...], "is_last_flags": [True, ...]}
        trace:  If False (default), return dict of final output values only.
                If True, return list[dict] — one dict per clock cycle, mapping
                signal_name -> int. This is used by vcd2table.py for cycle-by-cycle
                comparison against RTL waveform.

    Returns:
        trace=False -> dict: {"output_port": value, ...}
        trace=True  -> list[dict]: [{signal: value, ...}, ...] indexed by cycle

    Trace timing convention (CRITICAL):
        Trace cycle N records the register state that cocotb reads AFTER
        `await RisingEdge(dut.clk)`.

        With cocotb + iverilog VPI, after `await RisingEdge`, cocotb reads
        values produced by the PREVIOUS posedge's NBA. Equivalently:
        at RisingEdge N, cocotb sees POST-NBA of posedge N-1 = PRE-NBA of
        posedge N.

        The practical effect: each trace entry should record register values
        AFTER the NBA of each posedge (i.e., the NEW values computed in this
        cycle). The cocotb test comparison loop reads these values at the
        NEXT RisingEdge.

        Implementation: record register values AFTER the computation step,
        so the trace captures the state AFTER the NBA fires.
        Example: computation cycle j should record A = new_value_after_computation,
        not A = value_before_computation.

    CRITICAL: Registered outputs (ready, valid, etc.):
        Signals that are registered outputs (driven by a _reg flip-flop, not
        combinational assign) have a 1-cycle delay from the FSM state that
        computes them. For example, if IDLE state sets ready_next=1 and CALC
        state sets ready_next=0, the ready_reg transitions:
        - At IDLE→CALC posedge: ready_next=1 (from IDLE), so ready_reg becomes 1
        - At next CALC posedge: ready_next=0 (from CALC), so ready_reg becomes 0

        The golden model trace must record ready_reg=1 at the IDLE→CALC
        transition cycle, NOT ready_reg=0. The "0" appears one cycle later.

        Similarly, at DONE→IDLE transition: if DONE state sets ready_next=0,
        the trace records ready_reg=0 at the DONE→IDLE cycle. ready_reg=1
        appears one cycle later when IDLE sets ready_next=1.

    SOFTWARE vs RTL timing offset (CRITICAL for testbench alignment):
        This golden model uses SOFTWARE timing — state updates are instantaneous.
        RTL has a 1-cycle delay for registered→combinational control paths:
        - Golden cycle 1: LOAD (A = IV0) happens instantly
        - RTL cycle 1: FSM transitions to CALC, load_en asserted in NBA wake
        - RTL cycle 2: A_reg = IV0 (actual load)
        The cocotb testbench compensates with DRIVE_PHASE_CYCLES, read from
        spec.json timing_convention.golden_to_rtl_offset_cycles (primary) or
        max(pipeline_delay_cycles) from module timing_contract (fallback).

    Implementation note:
        Write ONE algorithm implementation. When trace=True, record intermediate
        state at each cycle into a list. When trace=False, skip the recording
        and just return the final result. Do NOT write two separate implementations.
    """
    cycles = [] if trace else None

    # --- Algorithm implementation ---
    # For iterative/multi-cycle algorithms:
    #   for step in range(NUM_STEPS):
    #       # ... computation ...
    #       if trace:
    #           cycles.append({
    #               "output_signal": output_val,
    #               "intermediate_reg": reg_val,     # match RTL register names
    #               # IMPORTANT: include ALL registers that participate in the
    #               # computation — working regs, expansion regs,
    #               # combinational outputs. Omitting any register
    #               # creates a blind spot where bugs go undetected until final output.
    #               # Signal names should match RTL _reg names for VPI access.
    #           })
    #       # ... continue computation ...

    if trace:
        return cycles
    else:
        return {}  # {"output_port": final_value, ...}


# --- Test vectors ---
# Known correct input/output pairs from the standard specification.
TEST_VECTORS = [
    {
        "name": "<test_name>",
        "inputs": {},   # design-specific input format
        "expected": {},  # {"output_port": expected_value, ...}
    },
    # ... more vectors ...
]


# --- Standard Interface ---

def run(test_vector_index: int = 0) -> list[dict]:
    """Run a test vector and return cycle-accurate expected values.

    This is the standard interface consumed by:
      - vcd2table.py (Strategy 2: import run(), get list[dict])
      - cocotb testbench (golden_run() for per-cycle comparison)
      - Verilog TB generation (extract expected final outputs)

    Args:
        test_vector_index: index into TEST_VECTORS (default: 0)

    Returns:
        list of dicts, one per clock cycle:
        [
            {"signal_name": int_value, ...},  # cycle 0
            {"signal_name": int_value, ...},  # cycle 1
            ...
        ]
        For multi-module designs, keys are "<module>.<signal>".
    """
    tv = TEST_VECTORS[test_vector_index]
    return compute(tv["inputs"], trace=True)


def get_test_vectors() -> list[dict]:
    """Return test vectors with final expected outputs (for testbench generation).

    Returns:
        list of {"name": str, "inputs": dict, "expected": dict}
    """
    results = []
    for tv in TEST_VECTORS:
        computed = compute(tv["inputs"], trace=False)
        results.append({
            "name": tv["name"],
            "inputs": tv["inputs"],
            "expected": tv.get("expected") or computed,
        })
    return results


if __name__ == "__main__":
    # Strategy 1 for vcd2table.py: print "cycle N: signal=0xVALUE" lines
    # Also used for standalone verification.
    #
    # Hex format note: we emit unpadded hex (`0x{v:x}`) so the same template
    # works for 32-bit, 64-bit, and 256-bit datapaths without truncation or
    # excess zero-padding. The vcd2table parser at vcd2table.py accepts any
    # length of hex digits.
    import json

    # Run default test vector with cycle trace
    cycles = run()
    for i, entry in enumerate(cycles):
        if entry:
            parts = [f"{k}=0x{v:x}" if isinstance(v, int) else f"{k}={v}"
                     for k, v in entry.items()]
            print(f"cycle {i}: {' '.join(parts)}")

    # Verify final outputs against expected
    print()
    for tv in get_test_vectors():
        computed = compute(tv["inputs"], trace=False)
        ok = computed == tv["expected"]
        name = tv["name"]
        parts = [f"{k}=0x{v:x}" if isinstance(v, int) and v > 0xFFFF else f"{k}={v}"
                 for k, v in tv["expected"].items()]
        print(f"[{'PASS' if ok else 'FAIL'}] {name}: {' '.join(parts)}")

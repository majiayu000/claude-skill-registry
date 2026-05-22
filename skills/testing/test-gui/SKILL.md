---
name: test_gui
description: GUIアプリケーションの動作試験・デバッグを自動で行う
---

# Test and Debug GUI

This skill helps in testing and debugging `gwexpy.gui`.

## Instructions

1.  **Run Automated Tests**:
    *   Run tests specifically marked for GUI (usually requiring `pytest-qt`).
    *   Command: `pytest -m gui` or `pytest tests/gui/`. (Adjust based on actual markers/folders).
    *   Check `scripts/run_gui_tests.sh` if it exists and run it.

2.  **Debug Crashes**:
    *   If the GUI crashes (e.g. segmentation fault), look for logs or run with `gdb` if necessary/possible.
    *   Check typical PyQt issues: Thread safety (updating UI from background thread), signal/slot mismatches, object lifecycle (Python garbage collecting C++ objects).

3.  **Interactive Debugging**:
    *   Since this is an agent, "interactive" means adding print debugging or logging to the code and running it to capture output.
    *   Focus on `gwexpy/gui/main_window.py` or relevant widget files.

---
name: python-code
description: "Make sure to ALWAYS use this skill when working with python code! Help designing, structuring, and maintaining Python projects, including virtualenvs, packaging, SQLite (sql3) usage, documentation of bug fixes, and clear commenting practices."
---

# Python Project Skill

You are a careful Python engineering assistant. Your job is to help the user create, evolve, and maintain Python projects in a way that is robust, testable, and easy to understand later.

## When to Use This Skill
Use this skill whenever the user:
- wants to start or reorganize a Python project or package
- is editing Python code and asks about structure, style, or testing
- needs to read/write data using SQLite ("sql3") from Python
- is fixing bugs and wants to record what changed and why
- asks how much or what kind of comments or docs to add

## Operating Principles
1. **Environment first.**
   - Prefer isolated environments (virtualenv, venv, or similar).
   - Ask which Python version and tooling (pip, poetry, uv, etc.) they use before prescribing commands.
2. **Simple, standard layout.**
   - Prefer standard `src/`-layout or a minimal flat layout for small scripts.
   - Use clear, meaningful package and module names.
3. **Tests early.**
   - Encourage adding at least one test file (`tests/`) for non-trivial logic.
   - When changing behavior, suggest updating or adding tests alongside code.
4. **Data safety with SQLite.**
   - Default to parameterized queries.
   - Avoid schema changes or destructive operations without explicit user confirmation.
5. **Documentation as part of the change.**
   - When fixing a bug or adding a feature, ensure docstrings, CHANGELOG entries (if present), and/or comments reflect the new behavior.
6. **Comment only what adds signal.**
   - Prefer clear code and docstrings over dense inline comments.
   - Use comments to explain *why*, not restate *what* the code does.

---

## A) Creating a New Python Project

### 1) Decide on layout
Use one of these patterns based on project size:

- **Single script / tiny tool**
  - `project/`
    - `tool.py`
    - `README.md`
    - `requirements.txt` (optional)

- **Small to medium project (`src` layout)**
  - `project/`
    - `src/`
      - `project_name/`
        - `__init__.py`
        - `main.py` (or similar entry point)
    - `tests/`
      - `test_main.py`
    - `README.md`
    - `pyproject.toml` *or* `requirements.txt`
    - `.gitignore`

Choose a **package name** that:
- is all-lowercase with underscores if needed: `project_name`
- does not shadow standard library modules (e.g., avoid `email`, `json`, `logging`).

### 2) Set up a virtual environment
Examples (adjust to the user’s tooling):

- Built-in venv:
  - `python -m venv .venv`
  - `source .venv/bin/activate` (macOS/Linux)
- Install dependencies:
  - `pip install -r requirements.txt` *or* `pip install -e .` when using `pyproject.toml`/`setup.cfg`.

Always:
- Pin or constrain important dependencies.
- Record dependencies in `requirements.txt` *or* `pyproject.toml` (not only in memory).

### 3) Minimal `pyproject.toml` (recommended for libraries)
Use a simple, standards-based configuration (PEP 621 / `setuptools` or other modern build backend). When the user asks, generate a full example tailored to their project name and needs.

---

## B) Editing and Evolving the Project

When the user edits code:
1. **Preserve API boundaries.**
   - Avoid breaking public function/class signatures unless explicitly agreed.
   - If a change is breaking, suggest bumping version and noting it in docs.
2. **Keep modules cohesive.**
   - Group related functions/classes together.
   - Split overly large modules (> ~500 lines or many responsibilities) into submodules.
3. **Refactor with tests.**
   - Before refactoring, identify or create tests that cover existing behavior.
   - After changes, run tests; if tooling is unspecified, suggest `pytest` with a `tests/` directory.
4. **Guard scripts with a main block.**
   - For executable modules, use:
     - `if __name__ == "__main__":`
         `main()`
5. **Keep configuration separate.**
   - Avoid hardcoding secrets (API keys, passwords) in code.
   - Use environment variables or config files as appropriate.

When giving concrete suggestions, explain **why** each structural choice is beneficial (e.g., easier testing, clearer imports, safer migrations).

---

## C) Working with SQLite (sql3) from Python

### 1) Connecting safely
- Use the standard library `sqlite3` module unless there is a specific reason to use an ORM.
- Prefer context managers to ensure connections and cursors are closed:

  - `import sqlite3`
  - `with sqlite3.connect("app.db") as conn:`
      `conn.row_factory = sqlite3.Row`
      `cur = conn.cursor()`

### 2) Parameterized queries (avoid SQL injection)
Always use placeholders rather than string concatenation:

- `cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))`
- `cur.executemany("INSERT INTO items(name, price) VALUES (?, ?)", items)`

### 3) Schema management
- Encourage an explicit schema definition (DDL) checked into version control (e.g., a `schema.sql` file or simple migration scripts).
- Before running **destructive changes** (DROP/ALTER/DELETE without WHERE),
  - explain the impact
  - ask for confirmation
  - suggest backing up the database (e.g., copy `.db` file) if feasible.

### 4) Transactions
- For groups of related writes, use transactions:

  - `with sqlite3.connect("app.db") as conn:`
      `conn.execute("BEGIN")`
      `... do writes ...`
      `conn.commit()`

- Explain that `with` on the connection will auto-commit on success and rollback on exceptions, but be explicit if the user needs predictable behavior.

### 5) Debugging database issues
When the user encounters errors:
- Ask for the **exact error message** and **relevant SQL**.
- Check for common problems:
  - missing tables/columns (migration not applied)
  - type mismatches
  - locked database (concurrent writes)
- Suggest simple introspection queries (e.g., `PRAGMA table_info(table_name);`) when needed.

---

## D) Documenting Bug Fixes

Whenever the user fixes a bug, aim to produce:
1. **A minimal reproduction (if possible).**
   - describe or capture input, steps, and observed vs. expected behavior.
2. **A clear commit message.**
   - `fix: describe the user-visible bug and context`
   - Optionally reference an issue ID if their workflow uses one.
3. **Code-level explanation where non-obvious.**
   - Add or update docstrings and comments for tricky logic.
   - If a bug was due to an implicit assumption, document that assumption.
4. **Tests that guard against regression.**
   - Add a failing test that reproduces the bug.
   - Fix the code so the new test passes.
5. **Changelog / release notes entry (if present).**
   - Short, user-facing description of the impact: what broke, who it affected, and what changed.

When asked, help the user draft:
- a commit message
- a changelog entry
- a short “what was wrong and how we fixed it” note.

---

## E) Comment and Docstring Practices

### 1) When to use docstrings
Use docstrings for:
- public functions, methods, and classes
- modules that provide a clear set of behaviors

Docstrings should focus on:
- **what** the function/class does
- important parameters and return values
- side effects (I/O, DB access, external APIs)
- errors/exceptions raised in normal use

Encourage a consistent style (e.g., Google, NumPy, or reStructuredText), but adapt to the project’s existing conventions if present.

### 2) When to use comments
Use comments to explain:
- **why** something is done in a particular way (constraints, tradeoffs)
- workarounds for bugs in dependencies or platforms
- non-obvious invariants or performance-sensitive code paths

Avoid comments that:
- restate the code line-by-line
- become inaccurate easily (e.g., describing outdated behavior)

### 3) Practical guidelines
- Prefer **small, well-named functions** over long functions with many comments.
- Keep comments close to the code they refer to.
- When removing code that had an explanatory comment, consider whether that explanation belongs in the new code or commit message.

---

## F) Example Prompts

Users might say:
- "Use the Python Project skill to scaffold a small CLI tool that reads from a SQLite database."
- "I'm refactoring this module; suggest a better structure and where tests should live."
- "Help me document this bug fix with a clear commit message and a short changelog entry."
- "Advise on how much to comment this function and improve its docstring."
- "Set up a standard `pyproject.toml` and testing layout for this new library."

---

## G) Operational Guidelines

Follow these numbered guidelines when working on Python projects:

1. Always use virtual environments to isolate project dependencies
2. Pin dependency versions in requirements.txt or pyproject.toml
3. Run tests before committing changes to verify functionality
4. Use type hints for function signatures to improve code clarity
5. Follow PEP 8 style guidelines for consistent code formatting
6. Document public APIs with docstrings
7. Use logging instead of print statements for production code
8. Handle exceptions explicitly rather than using bare except clauses

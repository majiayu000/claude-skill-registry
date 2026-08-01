---
name: implementing-features
description: 'Implements new modules, agents, or features using TDD methodology. Used
  when adding any new functionality to the table2image multi-agent system. Follows
  six-phase workflow: context loading, test writi'
---

---
name: implementing-features
description: Implements new modules, agents, or features using TDD methodology. Used when adding any new functionality to the table2image multi-agent system. Follows six-phase workflow: context loading, test writing, implementation, verification, documentation, and protocol completion.
---

## Implement Features

**Parameters**:
- `feature_name`: Name of the feature or module to implement
- `spec_reference`: Optional specific spec documents to reference

**Procedure**:

1.  **🔍 Context Loading (The "Scout" Phase)**
    * **Action**: Scan the `spec/` directory.
    * **Check**: Do you understand the architectural context? If `spec_reference` is provided, read it carefully.
    * **Rule**: Never start coding without knowing the history.

2.  **🔴 TDD: Write Test First (The "Red" Phase)**
    * **Action**: Create a new test file in `tests/` (e.g., `tests/test_{feature_name}.py`).
    * **Content**: Write unit tests or integration tests that define the *expected behavior* based on the requirements.
    * **Verification**: Run `uv run pytest`.
    * **Requirement**: The tests MUST fail (or error out) initially. This proves the code doesn't exist yet.

3.  **🟢 Implementation (The "Green" Phase)**
    * **Action**: Create/Edit the source code in `src/table2image_agent/`.
    * **Constraint**: Write the *minimum* amount of code needed to make the test pass. Do not over-engineer.
    * **Type Hinting**: All function signatures must have type hints.

4.  **✅ Verification & Refactoring**
    * **Action**: Run `uv run pytest`.
    * **Loop**: If tests fail, fix the code. Repeat until ALL tests pass (100%)，after finish all test pass, you should ask me whether has any other test. if not then you could pass to next part

5.  **📝 Documentation (The "Spec" Phase)**
    * **Action**: Create or update a report in `spec/` (e.g., `spec/00X_{feature_name}_implementation.md`).
    * **Content**: Summarize what was built, key decisions made, and verify the deliverable against the initial goal.

6. 🫡 Address Protocol ("Phoenix" Exclusive Rule)
    Core Instruction: From the moment this prompt is read, the user must be uniformly addressed as **"Phoenix"** in all subsequent conversations, without any exceptions.
    Examples: "Phoenix, here's the C++ multithreading code example you requested.", "Format optimization completed, Phoenix."
---
name: scaffold-action
description: Generate a new jhelm action class and matching test file from a name
argument-hint: <ActionName>
allowed-tools: Bash(./mvnw *)
---

## Scaffold a new jhelm Action class

`$ARGUMENTS` is the action name in PascalCase **without** the `Action` suffix.
Example: `/scaffold-action Lint` → creates `LintAction.java` + `LintActionTest.java`.

Package: `org.alexmond.jhelm.core`
Source root: `jhelm-core/src/main/java/org/alexmond/jhelm/core/`
Test root: `jhelm-core/src/test/java/org/alexmond/jhelm/core/`

---

### Step 1: Determine dependencies

Ask (or infer from context) whether the action needs:
- `Engine engine` — only if it renders templates (install, upgrade, template)
- `KubeService kubeService` — only if it talks to Kubernetes (install, upgrade, uninstall, rollback, status, list, history)

Use only the fields actually required.

---

### Step 2: Create the action class

File: `jhelm-core/src/main/java/org/alexmond/jhelm/core/$ARGUMENTS${"Action"}.java`

```java
package org.alexmond.jhelm.core;

import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RequiredArgsConstructor
public class ${ARGUMENTS}Action {

	// Include only the dependencies determined in Step 1:
	private final Engine engine;           // if template rendering needed
	private final KubeService kubeService; // if Kubernetes access needed

	public <ReturnType> <methodName>(<params>) throws Exception {
		// TODO: implement
	}

}
```

Rules:
- `@RequiredArgsConstructor` — never write a constructor by hand
- `@Slf4j` — use `log.debug/info/warn/error`, never `System.out.println`
- Throw descriptive `RuntimeException` (with cause) for error cases
- For dry-run actions, skip `kubeService` calls when `dryRun == true`

---

### Step 3: Create the test class

File: `jhelm-core/src/test/java/org/alexmond/jhelm/core/${ARGUMENTS}ActionTest.java`

```java
package org.alexmond.jhelm.core;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class ${ARGUMENTS}ActionTest {

	@Mock
	private Engine engine; // include only if used

	@Mock
	private KubeService kubeService; // include only if used

	private ${ARGUMENTS}Action ${argumentsCamel}Action;

	@BeforeEach
	void setUp() {
		MockitoAnnotations.openMocks(this);
		${argumentsCamel}Action = new ${ARGUMENTS}Action(/* inject mocks */);
	}

	@Test
	void testSuccess() throws Exception {
		// Arrange
		// Act
		// Assert
	}

	@Test
	void testThrowsWhenNotFound() throws Exception {
		// cover error/not-found path
	}

	// Add dryRun test if applicable:
	@Test
	void testDryRunSkipsKube() throws Exception {
		// verify(kubeService, never()).apply(anyString(), anyString());
	}

}
```

Test rules:
- One `@BeforeEach setUp()` that calls `MockitoAnnotations.openMocks(this)`
- Use `doNothing().when(mock).voidMethod(...)` not `when(...).thenReturn(null)` for void methods
- Use `ArgumentCaptor` when you need to assert on what was passed to a mock
- Always test: success path, error/not-found path, and dry-run (if applicable)
- Prefer real data (manifest strings, release builders) over excessive mocking

---

### Step 4: Run precommit check
```bash
./mvnw spring-javaformat:apply -pl jhelm-core && ./mvnw test -pl jhelm-core 2>&1 | tail -10
```

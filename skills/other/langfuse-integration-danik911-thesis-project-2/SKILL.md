---
name: langfuse-integration
description: Replaces Phoenix observability with Langfuse Cloud (EU) traceability for pharmaceutical test generation. Adds @observe decorators to existing code, configures LlamaIndex callbacks, propagates GAMP-5 compliance attributes, and removes Phoenix dependencies. Use PROACTIVELY when implementing Task 2.3 (LangFuse setup), migrating observability systems, or ensuring ALCOA+ trace attribution. MUST BE USED for pharmaceutical compliance monitoring requiring persistent cloud storage.
allowed-tools: ["Bash", "Read", "Write", "Edit", "Grep", "Glob", "LS"]
---

# Langfuse Integration Skill

**Purpose**: Replace Phoenix observability with Langfuse Cloud (EU) for pharmaceutical-grade traceability and monitoring.

**Target Architecture**:
- **From**: Phoenix (local-only, ephemeral traces)
- **To**: Langfuse Cloud EU (persistent storage, analytics, GAMP-5 compliant)
- **Strategy**: Complete replacement (no dual observability)

---

## When to Use This Skill

✅ **Use when**:
- Implementing PRP Task 2.3 (LangFuse Integration and Dashboard)
- Migrating from Phoenix to production observability
- Adding traceability to new pharmaceutical workflows
- Ensuring ALCOA+ attributable traces for regulatory compliance
- Preparing for AWS production deployment

❌ **Do NOT use when**:
- Extracting existing traces from Langfuse (use `langfuse-extraction` skill)
- Automating dashboard interactions (use `langfuse-dashboard` skill)
- Phoenix is required for local development (conflicts with replacement strategy)

---

## Prerequisites

Before invoking this skill, verify:

1. **Langfuse Cloud (EU) Account**:
   - Project URL: `https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107`
   - API keys available (public + secret)
   - EU data residency confirmed

2. **Environment Variables**:
   ```bash
   export LANGFUSE_PUBLIC_KEY="pk-lf-..."
   export LANGFUSE_SECRET_KEY="sk-lf-..."
   export LANGFUSE_HOST="https://cloud.langfuse.com"
   ```

3. **Dependencies**:
   - `langfuse` Python package (will be installed if missing)
   - `llama-index-core>=0.12.0` (for callback handler)
   - Existing Phoenix instrumentation code identified

---

## Workflow Phases

### Phase 1: Assessment and Analysis (5-10 minutes)

**Objective**: Understand current Phoenix instrumentation and identify migration points.

**Steps**:

1. **Locate Phoenix Configuration**:
   ```bash
   # Search for Phoenix setup
   grep -r "phoenix" main/src/monitoring/ --include="*.py"
   grep -r "from phoenix" main/src/ --include="*.py"
   grep -r "import phoenix" main/src/ --include="*.py"
   ```

2. **Identify Instrumentation Points**:
   - Read `main/src/core/unified_workflow.py` - identify workflow entry points
   - Read `main/src/agents/` - identify agent methods needing tracing
   - Look for existing OpenTelemetry span creation
   - Document all files importing Phoenix

3. **Analyze Compliance Attributes**:
   - Check if GAMP-5 attributes are set (category, confidence)
   - Check if ALCOA+ attributes are set (user_id, session_id, timestamps)
   - Verify 21 CFR Part 11 metadata if applicable

4. **Generate Assessment Report**:
   ```markdown
   # Phoenix → Langfuse Migration Assessment

   ## Current Phoenix Instrumentation
   - Configuration file: <path>
   - Instrumented files: <count>
   - Span count per workflow: <number>
   - Compliance attributes: <present/missing>

   ## Migration Scope
   - Files requiring decorator addition: <list>
   - Phoenix imports to remove: <count>
   - Callback handlers to replace: <list>
   - Estimated migration time: <minutes>

   ## Risk Assessment
   - Breaking changes: <yes/no>
   - Test coverage: <percentage>
   - Rollback complexity: <low/medium/high>
   ```

**Quality Gate**: Assessment report generated with complete file inventory and attribute analysis.

---

### Phase 2: Langfuse Configuration Setup (10-15 minutes)

**Objective**: Create Langfuse configuration module and verify cloud connectivity.

**Steps**:

1. **Install Langfuse SDK**:
   ```bash
   # Add to pyproject.toml
   uv add langfuse

   # For LlamaIndex integration
   uv add llama-index-instrumentation-langfuse
   ```

2. **Create Langfuse Configuration Module**:
   - **File**: `main/src/monitoring/langfuse_config.py`
   - **Content**: See `reference/decorator-patterns.md` for template
   - **Key functions**:
     - `setup_langfuse()`: Initialize client with EU cloud config
     - `get_langfuse_client()`: Singleton accessor
     - `get_langfuse_callback_handler()`: LlamaIndex integration
     - `add_compliance_attributes()`: GAMP-5/ALCOA+ attribute helper

3. **Verify Cloud Connectivity**:
   ```python
   # Test script (temporary)
   from main.src.monitoring.langfuse_config import setup_langfuse

   client = setup_langfuse()
   client.trace(name="connectivity-test", input={"test": True})
   client.flush()

   # Verify trace appears at:
   # https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107/traces
   ```

4. **Update Environment Configuration**:
   - Add Langfuse environment variables to `.env.example`
   - Update `main/src/config.py` to load Langfuse settings
   - Add Langfuse to `ObservabilityConfig` dataclass

**Quality Gate**:
- ✅ Langfuse SDK installed
- ✅ `langfuse_config.py` created and tested
- ✅ Connectivity test trace visible in Langfuse Cloud dashboard
- ✅ Configuration variables documented

---

### Phase 3: Code Instrumentation (20-30 minutes)

**Objective**: Add `@observe` decorators and replace Phoenix callbacks with Langfuse.

**Steps**:

1. **Add Decorators to Workflow Entry Points**:

   Use the automated script for systematic instrumentation:
   ```bash
   python .claude/skills/langfuse-integration/scripts/add_instrumentation.py \
     --target main/src/core/unified_workflow.py \
     --dry-run  # Preview changes first
   ```

   Manual pattern (if script unavailable):
   ```python
   # main/src/core/unified_workflow.py
   from langfuse import observe

   class UnifiedWorkflow(Workflow):
       @observe(name="unified-workflow-run", as_type="span")
       async def run(self, ctx: Context, ev: StartEvent) -> StopEvent:
           # Existing code unchanged
           ...
   ```

2. **Instrument Agent Methods**:

   Target key agent operations:
   ```python
   # main/src/agents/categorizer.py
   from langfuse import observe

   @observe(name="gamp5-categorization", as_type="span")
   async def categorize_urs(self, urs_content: str) -> dict:
       # Add compliance attributes
       from langfuse import get_current_observation
       obs = get_current_observation()
       if obs:
           obs.update(metadata={
               "compliance.gamp5.applicable": True,
               "compliance.alcoa_plus.attributable": True
           })

       # Existing categorization logic
       result = await self._categorize(urs_content)

       # Tag with category
       if obs:
           obs.update(metadata={
               "compliance.gamp5.category": result["category"]
           })

       return result
   ```

3. **Replace LlamaIndex Callback Handler**:

   ```python
   # main/src/core/unified_workflow.py or main/main.py
   # OLD (Phoenix):
   # from phoenix.otel import register
   # tracer_provider = register()

   # NEW (Langfuse):
   from langfuse.llama_index import LlamaIndexCallbackHandler

   langfuse_handler = LlamaIndexCallbackHandler(
       public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
       secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
       host=os.getenv("LANGFUSE_HOST")
   )

   # Register with workflow
   workflow = UnifiedWorkflow(
       callbacks=[langfuse_handler],
       timeout=600
   )
   ```

4. **Propagate User/Session Attributes**:

   ```python
   # In API endpoint or workflow entry point
   from langfuse import observe, get_current_trace

   @observe()
   async def generate_test_suite(user_id: str, urs_file: str, job_id: str):
       # Set trace-level attributes
       trace = get_current_trace()
       if trace:
           trace.update(
               user_id=user_id,
               session_id=job_id,
               tags=["pharmaceutical", "gamp5"],
               metadata={
                   "compliance.alcoa_plus.attributable": True,
                   "user.clerk_id": user_id,
                   "job.id": job_id
               }
           )

       # All nested operations inherit these attributes
       result = await unified_workflow.run(urs_file)
       return result
   ```

5. **Verify Decorator Coverage**:
   ```bash
   # Check all instrumentation points have decorators
   grep -r "@observe" main/src/ --include="*.py" | wc -l
   # Compare to Phoenix span count (should match or exceed)
   ```

**Quality Gate**:
- ✅ `@observe` decorators added to all workflow entry points
- ✅ LlamaIndex callback handler replaced
- ✅ User/session attributes propagated correctly
- ✅ GAMP-5 category metadata attached to categorization spans
- ✅ No syntax errors or import failures

---

### Phase 4: Phoenix Removal (10-15 minutes)

**Objective**: Remove all Phoenix dependencies without breaking functionality.

**Steps**:

1. **Remove Phoenix Configuration File**:
   ```bash
   # Backup first (optional)
   cp main/src/monitoring/phoenix_config.py main/src/monitoring/phoenix_config.py.bak

   # Remove
   rm main/src/monitoring/phoenix_config.py
   ```

2. **Update Imports**:

   Use automated script:
   ```bash
   python .claude/skills/langfuse-integration/scripts/remove_phoenix.py \
     --target main/src/ \
     --dry-run  # Preview changes
   ```

   Manual pattern:
   ```python
   # Remove all instances of:
   # - from phoenix.otel import register
   # - from phoenix import ...
   # - import phoenix
   # - Any calls to phoenix.trace(), register(), etc.
   ```

3. **Remove Phoenix from Dependencies**:
   ```bash
   # Remove from pyproject.toml
   uv remove arize-phoenix arize-phoenix-otel
   ```

4. **Update Monitoring Module Init**:
   ```python
   # main/src/monitoring/__init__.py
   # OLD:
   # from .phoenix_config import setup_phoenix, PhoenixManager

   # NEW:
   from .langfuse_config import setup_langfuse, get_langfuse_client

   __all__ = ["setup_langfuse", "get_langfuse_client"]
   ```

5. **Remove Phoenix Server Command** (if applicable):
   ```bash
   # Check if phoenix serve is in any scripts
   grep -r "phoenix serve" . --include="*.sh" --include="*.py" --include="*.md"

   # Remove or comment out
   ```

**Quality Gate**:
- ✅ `phoenix_config.py` removed
- ✅ All Phoenix imports removed from codebase
- ✅ Phoenix packages uninstalled
- ✅ No references to Phoenix in documentation
- ✅ Codebase still imports successfully

---

### Phase 5: Validation and Testing (15-20 minutes)

**Objective**: Verify Langfuse integration works correctly and traces appear in dashboard.

**Steps**:

1. **Run Integration Health Check**:
   ```bash
   python .claude/skills/langfuse-integration/scripts/validate_integration.py
   ```

   Expected output:
   ```
   ✅ Langfuse SDK installed
   ✅ API keys configured
   ✅ Cloud connectivity successful
   ✅ Test trace created: trace_id=xxx
   ✅ @observe decorators found: 15
   ✅ Callback handler configured
   ❌ No Phoenix imports found (expected)
   ```

2. **Run End-to-End Workflow**:
   ```bash
   # Execute test workflow with real URS
   uv run python main/main.py --urs examples/test_urs_001.md
   ```

3. **Verify Trace in Dashboard**:
   - Navigate to: `https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107/traces`
   - Find most recent trace by timestamp
   - **Check**:
     - ✅ Trace appears (not 404)
     - ✅ Span count matches expected (compare to Phoenix baseline)
     - ✅ User ID populated
     - ✅ Session ID populated
     - ✅ Tags include "pharmaceutical", "gamp5"
     - ✅ GAMP-5 category metadata present
     - ✅ No errors in observations

4. **Compare Span Structure**:
   ```bash
   # If Phoenix baseline available, compare span counts
   echo "Phoenix baseline: 131 spans/workflow"
   echo "Langfuse actual: <count from dashboard>"
   # Acceptable range: 120-140 (some variation expected)
   ```

5. **Test Compliance Attributes**:
   - Click on categorization span in dashboard
   - Verify metadata contains:
     - `compliance.gamp5.category`: 1-5
     - `compliance.alcoa_plus.attributable`: true
     - `user.clerk_id`: <actual user ID>
     - `job.id`: <actual job ID>

6. **Run Existing Tests**:
   ```bash
   # Ensure no regressions
   pytest main/tests/ -v

   # Check for import errors
   mypy main/src/

   # Check for Phoenix references
   ruff check main/src/
   ```

**Quality Gate**:
- ✅ Health check passes all tests
- ✅ End-to-end workflow completes successfully
- ✅ Trace visible in Langfuse Cloud dashboard
- ✅ Span count within 10% of Phoenix baseline
- ✅ All compliance attributes present
- ✅ Existing tests pass
- ✅ No mypy/ruff errors

---

### Phase 6: Documentation and Finalization (5-10 minutes)

**Objective**: Document the migration and update project references.

**Steps**:

1. **Update Quick Start Guide**:
   - Edit `main/docs/guides/QUICK_START_GUIDE.md`
   - Replace Phoenix setup instructions with Langfuse
   - Update environment variable examples
   - Add Langfuse dashboard URL

2. **Update README**:
   - Replace Phoenix badge/link with Langfuse
   - Update observability section
   - Add Langfuse Cloud (EU) data residency note

3. **Create Migration Notes**:
   ```markdown
   # Phoenix → Langfuse Migration Summary

   **Date**: <YYYY-MM-DD>
   **Scope**: Complete Phoenix replacement

   ## Changes Made
   - Removed: phoenix_config.py, Phoenix dependencies
   - Added: langfuse_config.py, Langfuse SDK
   - Instrumented: 15 functions with @observe decorators
   - Replaced: LlamaIndex callback handler

   ## Verification
   - Trace count: 131 spans/workflow (matches Phoenix baseline)
   - Dashboard URL: https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107
   - Compliance: GAMP-5 + ALCOA+ attributes preserved

   ## Rollback (if needed)
   - Restore phoenix_config.py.bak
   - Run: uv add arize-phoenix arize-phoenix-otel
   - Remove @observe decorators
   ```

4. **Update CLAUDE.md**:
   - Replace Phoenix references in "Technology Stack" section
   - Update observability commands
   - Add Langfuse skill invocation instructions

5. **Commit Changes**:
   ```bash
   git add -A
   git status  # Review changes

   # Commit with detailed message
   git commit -m "$(cat <<'EOF'
   feat: Replace Phoenix with Langfuse Cloud (EU) observability

   - Add Langfuse SDK and LlamaIndex instrumentation
   - Add @observe decorators to 15 workflow/agent functions
   - Configure Langfuse Cloud (EU) with GAMP-5 compliance attributes
   - Remove Phoenix dependencies and configuration
   - Verify trace parity: 131 spans/workflow maintained
   - Update documentation (Quick Start, README, CLAUDE.md)

   Task: PRP 2.3 (LangFuse Integration and Dashboard)
   Validation: All tests passing, traces visible in dashboard

   🤖 Generated with Claude Code

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

**Quality Gate**:
- ✅ Quick Start Guide updated
- ✅ README updated
- ✅ Migration notes created
- ✅ CLAUDE.md reflects Langfuse
- ✅ Changes committed to Git

---

## Success Criteria

Before marking this skill complete, verify ALL criteria:

### Functional Requirements
- ✅ Langfuse SDK installed and configured for EU cloud
- ✅ API keys set in environment variables
- ✅ `langfuse_config.py` created with setup functions
- ✅ `@observe` decorators added to all critical paths
- ✅ LlamaIndex callback handler replaced
- ✅ Phoenix configuration file removed
- ✅ Phoenix imports removed from all files
- ✅ Phoenix dependencies uninstalled

### Observability Requirements
- ✅ End-to-end workflow generates traces
- ✅ Traces visible in Langfuse Cloud dashboard
- ✅ Span count matches Phoenix baseline (±10%)
- ✅ Trace structure maintains workflow visibility

### Compliance Requirements
- ✅ User ID (Clerk) propagated to all traces
- ✅ Session ID (job_id) propagated to all traces
- ✅ GAMP-5 category metadata on categorization spans
- ✅ ALCOA+ attributable=true on all traces
- ✅ Tags include ["pharmaceutical", "gamp5"]

### Quality Requirements
- ✅ No FALLBACK LOGIC introduced
- ✅ All errors throw with full stack traces
- ✅ Existing tests pass (pytest)
- ✅ Type checking passes (mypy)
- ✅ Linting passes (ruff)
- ✅ No import errors or circular dependencies

### Documentation Requirements
- ✅ Quick Start Guide updated
- ✅ README updated
- ✅ CLAUDE.md updated
- ✅ Migration notes created
- ✅ Changes committed to Git with descriptive message

---

## Troubleshooting

### Issue: Langfuse SDK Import Error

**Symptom**:
```python
ModuleNotFoundError: No module named 'langfuse'
```

**Solution**:
```bash
uv add langfuse llama-index-instrumentation-langfuse
uv sync
```

### Issue: Traces Not Appearing in Dashboard

**Symptom**: Workflow runs successfully but no traces in Langfuse Cloud.

**Diagnosis**:
1. Check API keys:
   ```python
   import os
   print(f"Public key: {os.getenv('LANGFUSE_PUBLIC_KEY')[:10]}...")
   print(f"Secret key configured: {bool(os.getenv('LANGFUSE_SECRET_KEY'))}")
   ```

2. Check flush call:
   ```python
   from langfuse import get_client
   client = get_client()
   client.flush()  # CRITICAL: Must flush before exit
   ```

3. Check network connectivity:
   ```bash
   curl -I https://cloud.langfuse.com
   ```

**Solution**:
- Verify API keys match dashboard (Settings → API Keys)
- Add `client.flush()` before process exit
- Check firewall/proxy settings

### Issue: Missing Compliance Attributes

**Symptom**: Traces appear but lack GAMP-5 metadata.

**Solution**:
```python
# Ensure get_current_observation() is called inside decorated function
from langfuse import observe, get_current_observation

@observe()
def my_function():
    obs = get_current_observation()
    if obs:  # CRITICAL: Check if obs exists
        obs.update(metadata={"compliance.gamp5.category": 5})
```

### Issue: Span Count Mismatch

**Symptom**: Langfuse shows fewer spans than Phoenix baseline.

**Diagnosis**:
- Check if all `@observe` decorators are applied
- Verify LlamaIndex callback handler is registered
- Check for early return statements before instrumented code

**Solution**:
```bash
# Find missing decorators
grep -r "async def" main/src/agents/ --include="*.py" | \
  grep -v "@observe"
```

### Issue: High Latency After Migration

**Symptom**: Workflows slower with Langfuse vs Phoenix.

**Diagnosis**:
- Langfuse batches events asynchronously (default: every 1 second)
- Network calls to EU cloud add latency

**Solution**:
```python
# Tune batch settings
from langfuse import Langfuse

client = Langfuse(
    flush_interval=5,  # Flush every 5 seconds instead of 1
    flush_at=50,       # Batch 50 events before flushing
)
```

---

## Reference Materials

### Decorator Patterns
See `reference/decorator-patterns.md` for:
- Function-level instrumentation patterns
- Async function handling
- Nested span creation
- LLM generation tracing

### Phoenix Migration Guide
See `reference/phoenix-migration-guide.md` for:
- Side-by-side comparison of Phoenix vs Langfuse APIs
- Import migration table
- Span structure equivalence
- Common pitfalls during migration

### Compliance Attributes
See `reference/compliance-attributes.md` for:
- GAMP-5 category metadata schema
- ALCOA+ attribute requirements
- 21 CFR Part 11 considerations
- Audit trail best practices

---

## Advanced Usage

### Context Manager Pattern (Fine-Grained Control)

For more control than decorators provide:

```python
from langfuse import get_client

langfuse = get_client()

def complex_workflow():
    with langfuse.start_as_current_span(
        name="complex-workflow",
        as_type="span"
    ) as span:
        span.update(input={"mode": "batch"})

        # Manual sub-span creation
        with langfuse.start_as_current_span(
            name="data-validation",
            as_type="span"
        ) as sub_span:
            validate_data()
            sub_span.update(output={"valid": True})

        # Main logic
        result = process_data()

        span.update(output=result)
```

### Custom Event Tracking

For discrete events (not spans):

```python
from langfuse import get_current_observation

obs = get_current_observation()
if obs:
    obs.event(
        name="gamp5-category-assigned",
        metadata={
            "category": 5,
            "confidence": 0.95,
            "timestamp": datetime.now().isoformat()
        }
    )
```

### Multi-Tenant Attribution

For pharmaceutical companies with multiple users:

```python
from langfuse import observe, get_current_trace

@observe()
async def multi_tenant_workflow(org_id: str, user_id: str):
    trace = get_current_trace()
    if trace:
        trace.update(
            user_id=user_id,
            tags=[f"org:{org_id}", "gamp5"],
            metadata={
                "organization.id": org_id,
                "organization.name": get_org_name(org_id),
                "compliance.data_residency": "EU"
            }
        )

    # Workflow logic
    ...
```

---

## Skill Completion Checklist

Before reporting success to the user, verify:

- [ ] Phase 1: Assessment report generated
- [ ] Phase 2: Langfuse configured and connectivity verified
- [ ] Phase 3: Decorators added, callback handler replaced
- [ ] Phase 4: Phoenix removed completely
- [ ] Phase 5: Validation passes all tests
- [ ] Phase 6: Documentation updated and committed
- [ ] All success criteria met (see above)
- [ ] No FALLBACK LOGIC violations
- [ ] User confirmation obtained: "Did you see traces in the dashboard?"

**IMPORTANT**: NEVER claim success without user verification. Always ask: "Can you confirm you see traces appearing in the Langfuse dashboard at https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107/traces?"

---

## Post-Migration: Next Steps

After successful migration:

1. **Use langfuse-extraction skill** to:
   - Extract traces for debugging
   - Generate audit trails for compliance
   - Export data to pandas for analysis

2. **Use langfuse-dashboard skill** to:
   - Capture dashboard screenshots for documentation
   - Automate metric extraction for alerting
   - Investigate specific traces interactively

3. **Proceed with PRP tasks**:
   - Task 3.1: FastAPI backend development
   - Task 4.3: Bedrock model integration
   - Task 5.1: Production deployment validation

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-01-17
**Compatibility**: LlamaIndex 0.12.0+, Langfuse SDK 3.0+
**Data Residency**: EU (cloud.langfuse.com)
**Compliance**: GAMP-5, ALCOA+, 21 CFR Part 11 ready

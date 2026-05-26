---
name: ai-ad-api-automation-test
version: "1.3"
status: beta
layer: skill
owner: wade
last_reviewed: 2025-12-01
last_updated: 2025-12-01
baseline: AI_CODE_FACTORY_DEV_GUIDE_v2.4, SoT Freeze v2.8, SUPERCLAUDE_INTEGRATION_GUIDE_v2.2, AUTOMATION_TEST_SPEC_v1.4.md
---

<skill>
<name>ai-ad-api-automation-test</name>
<version>1.3</version>
<domain>AI_AD_SYSTEM / API Automation Testing</domain>
<profile>API-Test-Orchestrator / Newman-Integration / pytest-Generation</profile>

<!-- ======================================================
     0. Core Mission
====================================================== -->
<mission>
  API 自动化测试编排与执行 Skill，负责：
  - 生成符合 AUTOMATION_TEST_SPEC_v1.4 规范的 pytest 测试代码
  - 支持 Newman/Postman Collection 集成（契约测试扩展）
  - 执行 L2 API 层测试并生成报告
  - 确保测试用例与 SoT 文档对齐

  参考来源：
  - https://github.com/jfrelis/sanbercode-api-automation-boilerplate
  - Newman + Postman Collection 模式
  - 项目内 AUTOMATION_TEST_SPEC_v1.4.md 规范
</mission>


<!-- ======================================================
     1. Upstream Dependencies
====================================================== -->
<dependencies>
  <sot_documents>
    | Priority | Document | Version | Purpose |
    |----------|----------|---------|---------|
    | P0 | STATE_MACHINE.md | v2.8 | State enums, transitions, terminal states |
    | P0 | DATA_SCHEMA.md | v5.6 | Data structures, field constraints |
    | P1 | API_SOT.md | v9.4 | API endpoints, request/response contracts |
    | P1 | ERROR_CODES_SOT.md | v2.2 | Error code definitions |
    | P2 | DAILY_REPORT_SOT.md | v1.0 | Daily report 8-state machine |
    | P2 | BUSINESS_RULES.md | v4.7 | Business constraints |
    | P3 | AUTH_SPEC.md | v2.1 | Role permission matrix |
  </sot_documents>

  <external_references>
    | Reference | URL | Purpose | Status |
    |-----------|-----|---------|--------|
    | sanbercode-api-automation-boilerplate | https://github.com/jfrelis/sanbercode-api-automation-boilerplate | Newman/Postman patterns | Reference Only |
    | Newman | https://www.npmjs.com/package/newman | Postman CLI runner | Active |
    | newman-reporter-htmlextra | https://www.npmjs.com/package/newman-reporter-htmlextra | HTML report generation | Active |

    Note: External URLs are reference-only and may change. The patterns and practices
    have been internalized in this skill and AUTOMATION_TEST_SPEC_v1.4.md.
  </external_references>
</dependencies>


<!-- ======================================================
     2. Input Contract
====================================================== -->
<input_contract>
  Minimum Input:
  {
    mode: "GENERATE" | "RUN" | "NEWMAN" | "REPORT"
  }

  Optional Input:
  - target_module: string
    Valid values:
      - "daily_report" - DailyReport 8 状态机相关测试
      - "topup_request" - 充值申请状态机相关测试
      - "reconciliation" - 对账状态机相关测试
      - "ledger" - 账本分录相关测试
      - "ad_accounts" - 广告账户管理相关测试
      - "suppliers" - 供应商管理相关测试
      - "settlements" - 结算管理相关测试
      - "projects" - 项目管理相关测试
      - "auth" - 认证授权相关测试
      - "all" - 全模块测试（默认）
  - test_level: "L0" | "L1" | "L2" | "L3" (default: "L2")
  - collection_path: string (Postman collection JSON path, for NEWMAN mode)
  - environment_path: string (Postman environment JSON path)
  - output_format: "cli" | "html" | "json" (for reports)
  - dry_run: boolean (default: false) - 预览模式，不实际写入文件或执行命令
  - output_dir: string (default: "backend/tests/<level>/") - 测试文件输出目录
  - overwrite: boolean (default: false) - 是否覆盖已存在的文件

  Mode Behaviors:

  - GENERATE
    - Generate pytest test code for specified module
    - Output follows AUTOMATION_TEST_SPEC_v1.4 structure
    - Include SoT references in docstrings
    - Use common/ utilities (factories, asserts)

  - RUN
    - Execute pytest tests for specified level/module
    - Generate coverage report
    - Output test results summary

  - NEWMAN
    - Execute Newman runner with Postman collection
    - Support environment variables
    - Generate HTML report via newman-reporter-htmlextra

  - REPORT
    - Generate comprehensive test report
    - Include coverage metrics
    - SoT alignment verification

  Missing mode -> Output <halt>Missing: mode</halt> and stop.
</input_contract>


<!-- ======================================================
     3. Project Scope & Constraints
====================================================== -->
<project_scope>
  Target Directories:
  - Test code: backend/tests/
  - Test config: backend/tests/pytest.ini
  - Test fixtures: backend/tests/conftest.py
  - Common utilities: backend/tests/common/
  - Newman scripts: scripts/newman/ (optional)
  - Postman collections: collections/ (optional)

  Test Levels (from AUTOMATION_TEST_SPEC_v1.4):
  - L0 Unit: backend/tests/unit/ (@pytest.mark.unit)
  - L1 Integration: backend/tests/integration/ (@pytest.mark.integration)
  - L2 API: backend/tests/api/ (@pytest.mark.api)
  - L3 E2E: backend/tests/e2e/ (@pytest.mark.e2e)

  Safety Constraints:
  - MUST NOT modify production database
  - MUST use test database for all operations
  - MUST NOT commit secrets or credentials
  - MUST follow SoT referee chain for business rules
</project_scope>


<!-- ======================================================
     4. Workflow Overview
====================================================== -->
<workflow_overview>
  [Phase 1: Test Generation]
    GENERATE mode
      -> Read target module source code
      -> Query relevant SoT documents
      -> Generate test classes following naming conventions
      -> Output pytest test file

  [Phase 2: Test Execution]
    RUN mode
      -> Execute pytest with specified markers
      -> Collect coverage data
      -> Output results summary

  [Phase 3: Newman Integration (Optional)]
    NEWMAN mode
      -> Load Postman collection
      -> Apply environment variables
      -> Execute via Newman CLI
      -> Generate HTML report

  [Phase 4: Reporting]
    REPORT mode
      -> Aggregate test results
      -> Generate coverage report
      -> Verify SoT alignment
</workflow_overview>


<!-- ======================================================
     5. GENERATE Phase
====================================================== -->
<phase id="GENERATE">
  <description>
    Generate pytest test code following AUTOMATION_TEST_SPEC_v1.4 standards.
  </description>

  <prerequisites>
    - Target module exists in backend/
    - Relevant SoT documents identified
    - common/ utilities available
  </prerequisites>

  <naming_conventions>
    File naming: test_<module>.py or test_<module>_flow.py
    Class naming: Test<Module> or Test<Module>Flow
    Function naming: test_<condition>__<expected_result>

    Examples:
    - test_create_user__success
    - test_invalid_email__raises_validation_error
    - test_submit_raw__status_becomes_trend_pending
    - test_media_buyer_approve__returns_403
    - test_negative_amount__returns_BIZ_100
  </naming_conventions>

  <test_class_structure>
    Required test classes for L2 API tests:

    1. Test<Module>HappyPath
       - Complete successful flow from start to terminal state
       - Reference: STATE_MACHINE.md transitions

    2. Test<Module>Permissions
       - Permission boundary tests for each role
       - Reference: AUTH_SPEC.md permission matrix

    3. Test<Module>StateMachineViolations
       - Illegal state transition tests
       - Reference: STATE_MACHINE.md whitelist

    4. Test<Module>ErrorCodes
       - Error code validation tests
       - Reference: ERROR_CODES_SOT.md definitions
  </test_class_structure>

  <docstring_template>
    ```python
    """
    <Brief description>

    SoT References:
    - docs/sot/STATE_MACHINE.md v2.8 Section X.X (specific rule)
    - docs/sot/ERROR_CODES_SOT.md v2.2 (error code prefix)
    - docs/sot/API_SOT.md v9.4 (API endpoint)
    """
    ```
  </docstring_template>

  <output_template>
    ```python
    # backend/tests/api/test_<module>_flow.py
    """
    <Module> API Flow Tests

    SoT References:
    - docs/sot/STATE_MACHINE.md v2.8 Section X (state machine)
    - docs/sot/ERROR_CODES_SOT.md v2.2 (error codes)
    - docs/sot/API_SOT.md v9.4 (API contracts)
    - docs/sot/AUTH_SPEC.md v2.1 (permissions)
    """

    import pytest
    from decimal import Decimal
    from datetime import date

    from backend.tests.common.factories import create_user, create_<entity>
    from backend.tests.common.state_asserts import (
        assert_status_transition,
        assert_valid_transition,
        assert_terminal_state
    )
    from backend.tests.common.error_helpers import (
        assert_error_response,
        assert_success_response
    )
    from backend.tests.api.conftest import auth_header


    @pytest.mark.api
    class Test<Module>HappyPath:
        """
        Happy Path: Complete successful flow

        SoT Reference: STATE_MACHINE.md v2.8 Section X.X
        """

        def test_full_flow__start_to_terminal(self, client, db_session, *_tokens):
            """Complete happy path test"""
            # Arrange
            # Act
            # Assert
            pass


    @pytest.mark.api
    class Test<Module>Permissions:
        """
        Permission boundary tests

        SoT Reference: AUTH_SPEC.md v2.1 Section 3
        """

        def test_unauthorized_role__returns_403(self, client, db_session, token):
            """Role X cannot perform action Y"""
            pass


    @pytest.mark.api
    class Test<Module>StateMachineViolations:
        """
        Illegal state transition tests

        SoT Reference: STATE_MACHINE.md v2.8 Section X.X (whitelist)
        """

        def test_illegal_transition__returns_STATE_001(self, client, db_session):
            """<from_state> cannot directly transition to <to_state>"""
            pass


    @pytest.mark.api
    class Test<Module>ErrorCodes:
        """
        Error code validation tests

        SoT Reference: ERROR_CODES_SOT.md v2.2
        """

        def test_invalid_input__returns_VALIDATION_001(self, client):
            """Missing required field"""
            pass
    ```
  </output_template>
</phase>


<!-- ======================================================
     6. RUN Phase
====================================================== -->
<phase id="RUN">
  <description>
    Execute pytest tests with specified markers and generate reports.
  </description>

  <prerequisites>
    Python Dependencies (requirements-test.txt):
    | Package | Version | Purpose |
    |---------|---------|---------|
    | pytest | >=7.0.0 | Test framework |
    | pytest-cov | >=4.0.0 | Coverage reporting |
    | pytest-asyncio | >=0.21.0 | Async test support |
    | pytest-timeout | >=2.2.0 | Test timeout enforcement |
    | httpx | >=0.25.0 | Async HTTP client for API tests |
    | factory_boy | >=3.3.0 | Test data factories (optional) |

    Install: pip install -r backend/requirements-test.txt
  </prerequisites>

  <commands>
    | Scenario | Command | Description |
    |----------|---------|-------------|
    | All tests | pytest backend/tests | Full test suite |
    | Unit only | pytest -m unit | L0 tests |
    | Integration | pytest -m integration | L1 tests |
    | API only | pytest -m api | L2 tests |
    | E2E only | pytest -m e2e | L3 tests |
    | Quick CI | pytest -m "not e2e" | Exclude E2E |
    | Coverage | pytest --cov=backend --cov-report=html | With coverage |
    | With timeout | pytest --timeout=5 | Per-test 5s timeout |
    | Specific file | pytest backend/tests/api/test_X.py | Single file |
  </commands>

  <thresholds>
    Coverage Thresholds (% of code covered):
    | Level | Coverage Target | CI Blocking | Description |
    |-------|-----------------|-------------|-------------|
    | L0 Unit | 90% | Yes | Core business logic |
    | L1 Integration | 70% | Yes | State machine flows |
    | L2 API | 60% | Yes | Core API endpoints |
    | Overall | 80% | Yes | Combined threshold |

    Execution Time Limits (per test case, AUTOMATION_TEST_SPEC_v1.4.md 第 2 章):
    | Level | Max Time | Timeout Action | Description |
    |-------|----------|----------------|-------------|
    | L0 Unit | < 100ms | Fail | No external dependencies |
    | L1 Integration | < 500ms | Fail | Uses test database |
    | L2 API | < 1s | Warn | HTTP interface tests |
    | L3 E2E | < 5s | Warn | Complete business flows |

    Note: Coverage thresholds and execution time limits are independent metrics.
    - Coverage: Measured via pytest-cov, enforced by --cov-fail-under
    - Execution time: Measured per test, enforced by pytest-timeout
  </thresholds>

  <output_format>
    ```markdown
    ## Test Execution Report

    **Timestamp**: YYYY-MM-DD HH:MM:SS
    **Mode**: RUN
    **Target**: <module or level>

    ### Results Summary
    | Metric | Value |
    |--------|-------|
    | Total Tests | N |
    | Passed | X |
    | Failed | Y |
    | Skipped | Z |
    | Coverage | XX% |

    ### Failed Tests
    - test_module.py::TestClass::test_function
      - Error: <error message>
      - Location: <file>:<line>

    ### Coverage by Module
    | Module | Coverage |
    |--------|----------|
    | backend/services/ | XX% |
    | backend/api/ | XX% |

    ### SoT Alignment Check
    - [x] STATE_MACHINE.md transitions covered
    - [x] ERROR_CODES_SOT.md codes validated
    - [ ] Missing: <specific coverage gaps>
    ```
  </output_format>
</phase>


<!-- ======================================================
     7. NEWMAN Phase (Contract Testing Extension)
====================================================== -->
<phase id="NEWMAN">
  <description>
    Execute Postman collections via Newman CLI for contract testing.
    Reference: sanbercode-api-automation-boilerplate patterns.
  </description>

  <prerequisites>
    - Node.js installed
    - Newman package: npm install -g newman
    - HTML reporter: npm install -g newman-reporter-htmlextra
    - Postman collection exported as JSON
    - Environment file (optional)
  </prerequisites>

  <directory_structure>
    ```
    project_root/
    ├── collections/                    # Postman collections
    │   ├── daily_report_api.json
    │   ├── topup_api.json
    │   └── ledger_api.json
    ├── environments/                   # Environment configs
    │   ├── local.json
    │   ├── staging.json
    │   └── production.json
    └── scripts/
        └── newman/
            ├── run_api_tests.js        # Newman runner script
            └── package.json            # Dependencies
    ```
  </directory_structure>

  <newman_runner_template>
    ```javascript
    // scripts/newman/run_api_tests.js
    /**
     * Newman API Test Runner
     *
     * Reference: sanbercode-api-automation-boilerplate
     * SoT: API_SOT.md v9.4
     */

    const newman = require("newman");
    const path = require("path");

    // Configuration
    const config = {
      collection: path.join(__dirname, "../../collections/api_collection.json"),
      environment: path.join(__dirname, "../../environments/local.json"),
      reporters: ["cli", "htmlextra"],
      reporter: {
        htmlextra: {
          export: path.join(__dirname, "../../reports/api_test_report.html"),
          title: "AI Ad Spend API Test Report",
          browserTitle: "API Tests",
          showOnlyFails: false,
          noSyntaxHighlighting: false,
          testPaging: true,
          logs: true,
          omitRequestBodies: false,
          omitResponseBodies: false,
        },
      },
      // Environment variables override
      envVar: [
        { key: "BASE_URL", value: process.env.API_BASE_URL || "http://localhost:8000" },
        { key: "API_VERSION", value: "v1" },
      ],
      // Timeout settings
      timeout: {
        request: 30000,
        script: 30000,
      },
    };

    // Run Newman
    newman.run(config, function (err, summary) {
      if (err) {
        console.error("Newman run failed:", err);
        process.exit(1);
      }

      // Output summary
      console.log("\n=== Test Summary ===");
      console.log(`Total: ${summary.run.stats.tests.total}`);
      console.log(`Passed: ${summary.run.stats.tests.total - summary.run.stats.tests.failed}`);
      console.log(`Failed: ${summary.run.stats.tests.failed}`);

      // Exit with error code if any tests failed
      if (summary.run.stats.tests.failed > 0) {
        process.exit(1);
      }
    });
    ```
  </newman_runner_template>

  <package_json_template>
    ```json
    {
      "name": "ai-ad-spend-api-tests",
      "version": "1.0.0",
      "description": "API automation tests for AI Ad Spend system",
      "scripts": {
        "test:api": "node run_api_tests.js",
        "test:api:local": "API_BASE_URL=http://localhost:8000 npm run test:api",
        "test:api:staging": "API_BASE_URL=https://staging.example.com npm run test:api"
      },
      "devDependencies": {
        "newman": "^6.0.0",
        "newman-reporter-htmlextra": "^1.22.11"
      }
    }
    ```
  </package_json_template>

  <postman_collection_template>
    ```json
    {
      "info": {
        "name": "AI Ad Spend API Tests",
        "description": "API contract tests - SoT: API_SOT.md v9.4",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
      },
      "variable": [
        {
          "key": "base_url",
          "value": "{{BASE_URL}}/api/{{API_VERSION}}"
        }
      ],
      "item": [
        {
          "name": "Daily Reports",
          "description": "Daily Report API tests - STATE_MACHINE.md v2.8 Section 8",
          "item": [
            {
              "name": "Create Daily Report",
              "request": {
                "method": "POST",
                "header": [
                  {
                    "key": "Authorization",
                    "value": "Bearer {{access_token}}"
                  },
                  {
                    "key": "Content-Type",
                    "value": "application/json"
                  }
                ],
                "url": {
                  "raw": "{{base_url}}/daily-reports/",
                  "host": ["{{base_url}}"],
                  "path": ["daily-reports", ""]
                },
                "body": {
                  "mode": "raw",
                  "raw": "{\n  \"ad_account_id\": \"test-account-001\",\n  \"report_date\": \"{{$isoTimestamp}}\",\n  \"conversions_raw\": 100,\n  \"raw_spend\": \"1000.00\"\n}"
                }
              },
              "event": [
                {
                  "listen": "test",
                  "script": {
                    "exec": [
                      "// Contract test: API_SOT.md v9.4",
                      "pm.test('Status code is 201', function() {",
                      "    pm.response.to.have.status(201);",
                      "});",
                      "",
                      "pm.test('Response has success=true', function() {",
                      "    const json = pm.response.json();",
                      "    pm.expect(json.success).to.be.true;",
                      "});",
                      "",
                      "pm.test('Status is raw_submitted (STATE_MACHINE.md)', function() {",
                      "    const json = pm.response.json();",
                      "    pm.expect(json.data.status).to.equal('raw_submitted');",
                      "});",
                      "",
                      "// Store report_id for subsequent tests",
                      "const json = pm.response.json();",
                      "pm.environment.set('report_id', json.data.id);"
                    ]
                  }
                }
              ]
            }
          ]
        }
      ]
    }
    ```
  </postman_collection_template>

  <execution_commands>
    | Command | Description |
    |---------|-------------|
    | npm run test:api | Run API tests with default config |
    | npm run test:api:local | Run against local server |
    | npm run test:api:staging | Run against staging |
    | newman run collection.json -e env.json | Direct Newman command |
    | newman run collection.json -r htmlextra | With HTML report |
  </execution_commands>
</phase>


<!-- ======================================================
     8. REPORT Phase
====================================================== -->
<phase id="REPORT">
  <description>
    Generate comprehensive test report with coverage and SoT alignment.
  </description>

  <report_structure>
    ```markdown
    # API Automation Test Report

    **Generated**: YYYY-MM-DD HH:MM:SS
    **Project**: AI Ad Spend System
    **Baseline**: AUTOMATION_TEST_SPEC_v1.4

    ## Executive Summary

    | Metric | Value | Status |
    |--------|-------|--------|
    | Total Tests | N | - |
    | Pass Rate | XX% | OK/WARN/FAIL |
    | Coverage | XX% | OK/WARN/FAIL |
    | SoT Alignment | XX% | OK/WARN/FAIL |

    ## Test Results by Level

    ### L0 Unit Tests
    - Total: N
    - Passed: X
    - Failed: Y
    - Coverage: XX%

    ### L1 Integration Tests
    - Total: N
    - Passed: X
    - Failed: Y
    - Coverage: XX%

    ### L2 API Tests
    - Total: N
    - Passed: X
    - Failed: Y
    - Coverage: XX%

    ## SoT Alignment Matrix

    | SoT Document | Coverage | Missing |
    |--------------|----------|---------|
    | STATE_MACHINE.md | XX/YY transitions | [list] |
    | ERROR_CODES_SOT.md | XX/YY codes | [list] |
    | API_SOT.md | XX/YY endpoints | [list] |
    | AUTH_SPEC.md | XX/YY permissions | [list] |

    ## Failed Test Details

    ### test_module::test_function
    - **Status**: FAILED
    - **Error**: <error message>
    - **Location**: <file>:<line>
    - **SoT Reference**: <relevant SoT>
    - **Suggested Fix**: <recommendation>

    ## Coverage Gaps

    1. **Missing Happy Path**: <module> lacks complete flow test
    2. **Missing Permission Test**: <role> + <action> combination
    3. **Missing Error Code**: <code> not validated

    ## Recommendations

    1. [ ] Add test for <specific scenario>
    2. [ ] Increase coverage for <module>
    3. [ ] Update test to align with SoT v<new_version>
    ```
  </report_structure>
</phase>


<!-- ======================================================
     9. Module Mapping Configuration
====================================================== -->
<module_mapping>
  <description>
    Complete module definitions for all supported API modules.
    Each module includes router, service, SoT documents, and test output paths.
  </description>

  <supported_modules>
    | Module | Router Path | Service Path | SoT Documents | State Machine | Test Output Path |
    |--------|------------|--------------|---------------|---------------|------------------|
    | daily_report | backend/routers/daily_reports.py | backend/services/daily_report_service.py | docs/sot/DAILY_REPORT_SOT.md v1.0, docs/sot/STATE_MACHINE.md v2.8 Section 8 | STATE_MACHINE.md v2.8 Section 8 (8-state machine) | backend/tests/api/test_daily_report_flow_generated.py |
    | topup_request | backend/routers/topup.py | backend/services/topup_service.py | docs/sot/TOPUP_SOT.md v1.0, docs/sot/STATE_MACHINE.md v2.8 Section 9 | STATE_MACHINE.md v2.8 Section 9 (7-state machine) | backend/tests/api/test_topup_request_flow_generated.py |
    | reconciliation | backend/routers/reconciliation.py | backend/services/reconciliation_service.py | docs/sot/RECONCILIATION_SOT.md v1.0, docs/sot/STATE_MACHINE.md v2.8 Section 11 | STATE_MACHINE.md v2.8 Section 11 (5-state machine) | backend/tests/api/test_reconciliation_flow_generated.py |
    | ledger | backend/routers/ledger.py | backend/services/ledger_service.py | docs/sot/DATA_SCHEMA.md v5.11 §3.4.4, docs/sot/DATA_SCHEMA.md v5.6 | N/A (no state machine) | backend/tests/api/test_ledger_flow_generated.py |
    | ad_accounts | backend/routers/ad_accounts.py | backend/services/ad_account_service.py | docs/sot/API_SOT.md v9.4 Section 7, docs/sot/STATE_MACHINE.md v2.8 Section 7.1 | STATE_MACHINE.md v2.8 Section 7.1 (ad_accounts.status) | backend/tests/api/test_ad_accounts_flow_generated.py |
    | suppliers | backend/routers/suppliers.py | backend/services/supplier_service.py | docs/sot/API_SOT.md v9.4, docs/sot/DATA_SCHEMA.md v5.6 | N/A (no state machine) | backend/tests/api/test_suppliers_flow_generated.py |
    | settlements | backend/routers/settlements.py | backend/services/settlement_service.py | docs/sot/API_SOT.md v9.4, docs/sot/DATA_SCHEMA.md v5.11 §3.4.4 | N/A (no state machine) | backend/tests/api/test_settlements_flow_generated.py |
    | projects | backend/routers/projects.py | backend/services/project_service.py | docs/sot/API_SOT.md v9.4 Section 6, docs/sot/STATE_MACHINE.md v2.8 Section 5 | STATE_MACHINE.md v2.8 Section 5 (projects.status) | backend/tests/api/test_projects_flow_generated.py |
    | auth | backend/routers/authentication.py | backend/services/supabase_auth_service.py | docs/sot/AUTH_SPEC.md v2.1, docs/sot/API_SOT.md v9.4 | N/A (no state machine) | backend/tests/api/test_auth_flow_generated.py |
  </supported_modules>

  <module_details>
    <module name="daily_report">
      <router>backend/routers/daily_reports.py</router>
      <service>backend/services/daily_report_service.py</service>
      <sot_documents>
        - docs/sot/DAILY_REPORT_SOT.md v1.0
        - docs/sot/STATE_MACHINE.md v2.8 Section 8
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/API_SOT.md v9.4
      </sot_documents>
      <state_machine>STATE_MACHINE.md v2.8 Section 8 (8-state: raw_submitted → trend_pending → trend_ok/trend_flagged → final_pending → final_confirmed → final_locked)</state_machine>
      <test_path>backend/tests/api/test_daily_report_flow_generated.py</test_path>
    </module>

    <module name="topup_request">
      <router>backend/routers/topup.py</router>
      <service>backend/services/topup_service.py</service>
      <sot_documents>
        - docs/sot/TOPUP_SOT.md v1.0
        - docs/sot/STATE_MACHINE.md v2.8 Section 9
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/API_SOT.md v9.4
      </sot_documents>
      <state_machine>STATE_MACHINE.md v2.8 Section 9 (7-state: draft → pending_review → finance_approve → paid → completed)</state_machine>
      <test_path>backend/tests/api/test_topup_request_flow_generated.py</test_path>
    </module>

    <module name="reconciliation">
      <router>backend/routers/reconciliation.py</router>
      <service>backend/services/reconciliation_service.py</service>
      <sot_documents>
        - docs/sot/RECONCILIATION_SOT.md v1.0
        - docs/sot/STATE_MACHINE.md v2.8 Section 11
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/API_SOT.md v9.4
      </sot_documents>
      <state_machine>STATE_MACHINE.md v2.8 Section 11 (5-state: draft → pending_review → approved/needs_adjustment → completed)</state_machine>
      <test_path>backend/tests/api/test_reconciliation_flow_generated.py</test_path>
    </module>

    <module name="ledger">
      <router>backend/routers/ledger.py</router>
      <service>backend/services/ledger_service.py</service>
      <sot_documents>
        - docs/sot/DATA_SCHEMA.md v5.11 §3.4.4
        - docs/sot/DATA_SCHEMA.md v5.6
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/API_SOT.md v9.4
      </sot_documents>
      <state_machine>N/A (no state machine, ledger entries are immutable records)</state_machine>
      <test_path>backend/tests/api/test_ledger_flow_generated.py</test_path>
    </module>

    <module name="ad_accounts">
      <router>backend/routers/ad_accounts.py</router>
      <service>backend/services/ad_account_service.py</service>
      <sot_documents>
        - docs/sot/API_SOT.md v9.4 Section 7
        - docs/sot/STATE_MACHINE.md v2.8 Section 7.1
        - docs/sot/DATA_SCHEMA.md v5.6
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/AUTH_SPEC.md v2.1
      </sot_documents>
      <state_machine>STATE_MACHINE.md v2.8 Section 7.1 (ad_accounts.status: new → testing → active → suspended → dead → archived)</state_machine>
      <test_path>backend/tests/api/test_ad_accounts_flow_generated.py</test_path>
    </module>

    <module name="suppliers">
      <router>backend/routers/suppliers.py</router>
      <service>backend/services/supplier_service.py</service>
      <sot_documents>
        - docs/sot/API_SOT.md v9.4
        - docs/sot/DATA_SCHEMA.md v5.6
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/AUTH_SPEC.md v2.1
        - docs/sot/DATA_SCHEMA.md v5.11 §3.4.4 (SUPPLIER ledger)
      </sot_documents>
      <state_machine>N/A (no state machine, suppliers.status is simple active/inactive)</state_machine>
      <test_path>backend/tests/api/test_suppliers_flow_generated.py</test_path>
    </module>

    <module name="settlements">
      <router>backend/routers/settlements.py</router>
      <service>backend/services/settlement_service.py</service>
      <sot_documents>
        - docs/sot/API_SOT.md v9.4
        - docs/sot/DATA_SCHEMA.md v5.11 §3.4.4 (ledger integration)
        - docs/sot/DATA_SCHEMA.md v5.6
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/AUTH_SPEC.md v2.1
      </sot_documents>
      <state_machine>N/A (no state machine, settlements may have approval workflow but not defined in STATE_MACHINE.md)</state_machine>
      <test_path>backend/tests/api/test_settlements_flow_generated.py</test_path>
    </module>

    <module name="projects">
      <router>backend/routers/projects.py</router>
      <service>backend/services/project_service.py</service>
      <sot_documents>
        - docs/sot/API_SOT.md v9.4 Section 6
        - docs/sot/STATE_MACHINE.md v2.8 Section 5
        - docs/sot/DATA_SCHEMA.md v5.6
        - docs/sot/ERROR_CODES_SOT.md v2.2
        - docs/sot/AUTH_SPEC.md v2.1
      </sot_documents>
      <state_machine>STATE_MACHINE.md v2.8 Section 5 (projects.status: draft → active → suspended → archived)</state_machine>
      <test_path>backend/tests/api/test_projects_flow_generated.py</test_path>
    </module>

    <module name="auth">
      <router>backend/routers/authentication.py</router>
      <service>backend/services/supabase_auth_service.py</service>
      <sot_documents>
        - docs/sot/AUTH_SPEC.md v2.1
        - docs/sot/API_SOT.md v9.4
        - docs/sot/ERROR_CODES_SOT.md v2.2
      </sot_documents>
      <state_machine>N/A (no state machine, authentication is stateless)</state_machine>
      <test_path>backend/tests/api/test_auth_flow_generated.py</test_path>
    </module>
  </module_details>
</module_mapping>


<!-- ======================================================
     10. Common Utilities Integration
====================================================== -->
<common_utilities>
  <factories>
    Location: backend/tests/common/factories.py
    SoT Ref: DATA_SCHEMA.md v5.6, STATE_MACHINE.md v2.6

    Available factories (all use keyword-only arguments):
    - create_test_project(*, name, owner_id, status, **kwargs) → Dict
    - create_test_channel(*, name, channel_type, **kwargs) → Dict
    - create_test_ad_account(*, project_id, channel_id, account_name, platform_account_id, balance, **kwargs) → Dict
    - create_test_daily_report(*, ad_account_id, report_date, status, spend, impressions, clicks, conversions, **kwargs) → Dict
    - create_test_topup_request(*, ad_account_id, amount, status, requested_by, **kwargs) → Dict

    Usage:
    ```python
    from backend.tests.common.factories import create_test_daily_report
    report = create_test_daily_report(status="raw_submitted", spend=Decimal("100.00"))
    ```

    MUST use factories instead of ad-hoc data creation.
  </factories>

  <state_asserts>
    Location: backend/tests/common/state_asserts.py
    SoT Ref: STATE_MACHINE.md v2.6

    Available assertions:
    - assert_daily_report_state(entity, expected_state, msg=None) - DailyReport 8 状态机
    - assert_topup_state(entity, expected_state, msg=None) - Topup 状态机
    - assert_reconciliation_state(entity, expected_state, msg=None) - Reconciliation 状态机
    - assert_state_transition_valid(entity_type, from_state, to_state, msg=None) - 验证状态转换合法性

    State whitelist constants:
    - DAILY_REPORT_STATES, DAILY_REPORT_TRANSITIONS, DAILY_REPORT_TERMINAL_STATES
    - TOPUP_STATES, TOPUP_TRANSITIONS, TOPUP_TERMINAL_STATES
    - RECONCILIATION_STATES, RECONCILIATION_TRANSITIONS, RECONCILIATION_TERMINAL_STATES

    Usage:
    ```python
    from backend.tests.common.state_asserts import (
        assert_daily_report_state,
        assert_state_transition_valid,
        DAILY_REPORT_TRANSITIONS
    )
    assert_daily_report_state(report, "trend_pending")
    assert_state_transition_valid("daily_report", "raw_submitted", "trend_pending")
    ```
  </state_asserts>

  <error_helpers>
    Location: backend/tests/common/error_helpers.py
    SoT Ref: ERROR_CODES_SOT.md v2.2

    Available helpers:
    - assert_error_code(response, expected_code, msg=None) - 断言特定错误码
    - assert_validation_error(response, expected_code=None, msg=None) - 断言 VAL-xxx 错误
    - assert_auth_error(response, expected_code=None, msg=None) - 断言 AUTH-xxx 错误
    - assert_business_error(response, expected_code=None, msg=None) - 断言 BIZ-xxx 错误

    Error code constants:
    - ERROR_CODE_PREFIXES: {"VAL", "AUTH", "PERM", "BIZ", "SYS", "DATA", "EXT", "LED", "RPT", "TOP", "REC"}
    - VALIDATION_ERROR_CODES: {"VAL-001", "VAL-002", "VAL-003", "VAL-004", "VAL-005"}
    - AUTH_ERROR_CODES: {"AUTH-001", "AUTH-002", "AUTH-003", "AUTH-004", "AUTH-005"}
    - BUSINESS_ERROR_CODES: {"BIZ-001", "BIZ-002", "BIZ-003", "BIZ-004", "BIZ-005"}

    Usage:
    ```python
    from backend.tests.common.error_helpers import assert_error_code, assert_validation_error
    assert_error_code(response, "VAL-001")
    assert_validation_error(response)  # Any VAL-xxx error
    ```
  </error_helpers>
</common_utilities>


<!-- ======================================================
     10. Safety Constraints
====================================================== -->
<safety_constraints>
  <sot_policy>
    **SoT Read-Only Policy (MANDATORY)**

    This skill operates in READ-ONLY mode for all SoT documents:
    - ✅ MAY read SoT documents for reference and validation
    - ✅ MAY generate test code that references SoT documents
    - ✅ MAY validate test results against SoT specifications
    - ❌ MUST NOT modify any files in docs/sot/*
    - ❌ MUST NOT propose changes to SoT documents
    - ❌ MUST NOT add/remove/rename SoT definitions

    If SoT inconsistencies are detected:
    1. Log the inconsistency with exact SoT reference
    2. Report to user for manual SoT governance process
    3. Continue test execution with current SoT values
  </sot_policy>

  <file_permissions>
    | Directory | Permission | Reason |
    |-----------|------------|--------|
    | docs/sot/* | READ-ONLY | SoT governance |
    | backend/services/* | READ-ONLY | Business logic immutable |
    | backend/api/* | READ-ONLY | API layer immutable |
    | backend/tests/* | READ-WRITE | Test code generation target |
    | collections/* | READ-WRITE | Newman collection output |
    | reports/* | READ-WRITE | Test report output |
  </file_permissions>

  <dry_run_mode>
    When dry_run=true:
    - Generate test code but do not write files
    - Show commands but do not execute
    - Preview report structure without data
  </dry_run_mode>
</safety_constraints>


<!-- ======================================================
     11. Usage Examples
====================================================== -->
<usage>
  Example 1: Generate L2 API tests for Daily Report module
  ```
  Use ai-ad-api-automation-test,
  mode = GENERATE,
  target_module = "daily_report",
  test_level = "L2".

  Generate complete test file following AUTOMATION_TEST_SPEC_v1.4.
  ```

  Example 1b: Generate L2 API tests for Ad Accounts module
  ```
  Use ai-ad-api-automation-test,
  mode = GENERATE,
  target_module = "ad_accounts",
  test_level = "L2".

  Generate complete test file for ad_accounts module.
  ```

  Example 1c: Generate L2 API tests for Suppliers module
  ```
  Use ai-ad-api-automation-test,
  mode = GENERATE,
  target_module = "suppliers",
  test_level = "L2".

  Generate complete test file for suppliers module.
  ```

  Example 2: Run all L2 API tests
  ```
  Use ai-ad-api-automation-test,
  mode = RUN,
  test_level = "L2",
  output_format = "cli".

  Execute pytest -m api and report results.
  ```

  Example 3: Execute Newman with Postman collection
  ```
  Use ai-ad-api-automation-test,
  mode = NEWMAN,
  collection_path = "collections/daily_report_api.json",
  environment_path = "environments/local.json",
  output_format = "html".

  Run Newman and generate HTML report.
  ```

  Example 4: Generate comprehensive test report
  ```
  Use ai-ad-api-automation-test,
  mode = REPORT,
  output_format = "html".

  Generate full report with coverage and SoT alignment.
  ```
</usage>


<!-- ======================================================
     11. Error Handling
====================================================== -->
<error_handling>
  Scenario 1: Target module not found
  - Report: "Error: Module '<name>' not found in backend/"
  - Suggest: List available modules from valid values enumeration
  - Action: Abort operation

  Scenario 2: SoT document not found
  - Report: "Warning: SoT document '<path>' not found"
  - Fallback: Continue with available SoT references
  - Action: Log warning, proceed with caution

  Scenario 3: Test execution fails
  - Report: Detailed error with stack trace
  - Include: Failed assertion details, SoT reference
  - Suggest: Potential fixes based on error type
  - Action: Mark test as FAILED, continue suite

  Scenario 4: Newman collection invalid
  - Report: "Error: Invalid Postman collection format"
  - Suggest: Validate JSON structure against Postman schema
  - Action: Abort Newman execution

  Scenario 5: Coverage below threshold
  - Report: "Warning: Coverage XX% below threshold YY%"
  - List: Uncovered modules/functions
  - Action: Mark build as FAILED if CI blocking

  Scenario 6: Output directory not writable
  - Report: "Error: Cannot write to '<output_dir>'"
  - Suggest: Check directory permissions, use alternative path
  - Action: Abort operation

  Scenario 7: File already exists (overwrite=false)
  - Report: "Warning: File '<path>' already exists"
  - Suggest: Set overwrite=true or use different output_dir
  - Action: Skip file, continue with next

  Scenario 8: Newman/Node.js not available
  - Report: "Error: Newman CLI not found"
  - Suggest: Run 'npm install -g newman newman-reporter-htmlextra'
  - Action: Abort NEWMAN mode

  Scenario 9: Execution timeout exceeded
  - Report: "Error: Test '<name>' exceeded timeout limit"
  - Include: Test level, configured timeout, actual duration
  - Action: Mark test as TIMEOUT, continue suite

  Scenario 10: Environment variables missing
  - Report: "Error: Required environment variable '<var>' not set"
  - Suggest: Check environments/*.json or set via shell
  - Action: Abort operation
</error_handling>


<!-- ======================================================
     12. Version Notes
====================================================== -->
<VERSION_NOTES>

  ### v1.3 (2025-12-01)

  **Module Mapping Enhancement - Status: beta**

  P0 Enhancements:
  - Added complete module mapping configuration section (Section 9)
  - Extended target_module valid values from 5 to 9 modules:
    - Added: ad_accounts, suppliers, settlements, projects
    - Existing: daily_report, topup_request, reconciliation, ledger, auth
  - Added comprehensive module definitions table with router/service/SoT/test paths
  - Added detailed module_details XML blocks for each of 9 modules

  Module Coverage:
  - All 9 modules now have complete configuration:
    - Router file paths (backend/routers/*.py)
    - Service file paths (backend/services/*_service.py)
    - SoT document references (docs/sot/*.md)
    - State machine references (STATE_MACHINE.md sections)
    - Test output paths (backend/tests/api/test_*_flow_generated.py)

  Configuration Alignment:
  - All module names consistent across:
    - target_module valid values enumeration
    - supported_modules table
    - module_details XML blocks
    - Usage examples

  ---

  ### v1.2 (2025-12-01)

  **P0/P1 Pre-Launch Remediation - Status: beta**

  P0 Fixes:
  - Fixed version inconsistency (YAML/XML both v1.2)
  - Added Safety Constraints section with SoT read-only declaration
  - Fixed coverage_thresholds to include execution time limits
  - Aligned thresholds with AUTOMATION_TEST_SPEC_v1.4.md 第 2 章

  P1 Fixes:
  - Added target_module valid values enumeration
  - Added dry_run, output_dir, overwrite parameters
  - Added pytest prerequisites/dependencies section
  - Updated common_utilities to match actual implementations:
    - factories.py: create_test_* functions
    - state_asserts.py: assert_*_state, assert_state_transition_valid
    - error_helpers.py: assert_error_code, assert_*_error
  - Extended error_handling from 5 to 10 scenarios

  ---

  ### v1.1 (2025-12-01)

  **P0/P1/P2 Audit Fixes - Status: beta**

  Infrastructure Created:
  - Created backend/tests/common/ directory with utility files:
    - factories.py: Test data factory functions
    - state_asserts.py: State machine assertion helpers
    - error_helpers.py: Error code validation helpers
  - Created test layer directories:
    - backend/tests/unit/ (L0)
    - backend/tests/integration/ (L1)
    - backend/tests/api/ (L2)
    - backend/tests/e2e/ (L3)
  - Created Newman directories:
    - scripts/newman/
    - collections/
    - environments/

  Configuration Updates:
  - Updated pytest.ini with e2e and smoke markers
  - Created .github/workflows/test-coverage.yml for CI
  - Added coverage thresholds per test level

  Status Changes:
  - Changed status from ready_for_production to beta
  - Added Status column to external_references table
  - Added external URL availability note

  ---

  ### v1.0 (2025-12-01)

  **Initial Release**
  - Created skill based on sanbercode-api-automation-boilerplate patterns
  - Integrated with AUTOMATION_TEST_SPEC_v1.4.md standards
  - Support for 4 modes: GENERATE, RUN, NEWMAN, REPORT
  - pytest test generation with SoT alignment
  - Newman/Postman collection integration for contract testing
  - HTML report generation via newman-reporter-htmlextra
  - Common utilities integration (factories, state_asserts, error_helpers)

  **Reference Projects**
  - https://github.com/jfrelis/sanbercode-api-automation-boilerplate
  - Newman v6.0.0+
  - newman-reporter-htmlextra v1.22.11+

  **Alignment**
  - MASTER.md v4.6
  - SoT Freeze v2.8
  - AUTOMATION_TEST_SPEC_v1.4.md

</VERSION_NOTES>

</skill>

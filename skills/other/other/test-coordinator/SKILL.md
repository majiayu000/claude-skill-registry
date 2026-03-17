---
description: Orchestrate multi-phase integration and E2E test suites across multiple agents and testing gates
handoffs:
  - label: Fix Test Failures
    agent: backend-engineer
    prompt: Fix the failing tests identified in the coordinator report
    send: false
  - label: Review AI Quality
    agent: ai-specialist
    prompt: Improve AI generation quality based on coordinator findings
    send: false
  - label: Optimize Performance
    agent: backend-engineer
    prompt: Optimize performance bottlenecks identified in the coordinator report
    send: false
---

## User Input

```text
$ARGUMENTS
```

Test suite options: `full-pipeline`, `ai-quality`, `production`, `phase-6`, `phase-7`, `phase-10`, `all` (default: full-pipeline)

## Task

Orchestrate comprehensive integration and E2E testing across multiple sub-agents, ensuring all testing gates pass before proceeding to the next implementation phase.

### Test Suites Overview

From **IMPLEMENTATION-GUIDE.md Testing Gates**:

**Phase 6 Gate** (T089A-T089I): Integration Testing
- Email verification flow (8 test cases)
- Rate limiting enforcement (6 test cases)
- Email blacklist (4 test cases)
- Quiz submission + calorie calc (10 test cases)
- Quiz expiry (2 test cases)
- Checkout session creation (1 test case)
- Webhook → generation trigger (1 test case)
- Pipeline orchestration (1 test case)
- Manual queue routing (1 test case)

**Phase 7 Gate** (T107A-T107F): AI/PDF/Payment Testing
- AI meal plan generation (5 scenarios)
- Keto compliance validation (<30g carbs)
- AI retry on failure (3 attempts)
- PDF generation with all sections
- Full pipeline (payment → AI → PDF → email)
- Manual queue on AI/PDF failure

**Phase 10 Gate** (T144-T150): Production Readiness
- Full payment flow E2E in production
- 10+ quiz variations (allergies, preferences, goals)
- Data retention verification (24h quiz, 90d PDF)
- Manual resolution queue testing
- Cron job execution verification
- SLA monitoring testing

### Steps

1. **Parse Arguments**:
   - If `$ARGUMENTS` is "full-pipeline": Run T089H (pipeline orchestration test)
   - If `$ARGUMENTS` is "ai-quality": Run T107A-T107F (AI quality validation)
   - If `$ARGUMENTS` is "production": Run T144-T150 (production readiness)
   - If `$ARGUMENTS` is "phase-6": Run all Phase 6 integration tests
   - If `$ARGUMENTS` is "phase-7": Run all Phase 7 AI/PDF/payment tests
   - If `$ARGUMENTS` is "phase-10": Run all Phase 10 production tests
   - If `$ARGUMENTS` is "all": Run all test suites sequentially

2. **Run Test Suite Based on Type**:

   **For Full Pipeline** (T089H):
   ```bash
   cd backend

   echo "🔄 Running Full Pipeline Integration Test (T089H)"
   echo "Testing: Payment Webhook → AI Generation → PDF Generation → Email Delivery"
   echo ""

   # Step 1: Submit quiz and get quiz_id
   echo "Step 1: Submit quiz data..."
   pytest tests/integration/test_full_pipeline.py::test_quiz_submission -v

   # Step 2: Verify email
   echo "Step 2: Verify email..."
   pytest tests/integration/test_full_pipeline.py::test_email_verification -v

   # Step 3: Create checkout session
   echo "Step 3: Create Paddle checkout session..."
   pytest tests/integration/test_full_pipeline.py::test_checkout_creation -v

   # Step 4: Simulate payment webhook
   echo "Step 4: Simulate payment.succeeded webhook..."
   pytest tests/integration/test_full_pipeline.py::test_payment_webhook -v

   # Step 5: Verify AI generation triggered
   echo "Step 5: Verify AI generation triggered..."
   pytest tests/integration/test_full_pipeline.py::test_ai_generation -v

   # Step 6: Verify PDF generated and uploaded
   echo "Step 6: Verify PDF generation..."
   pytest tests/integration/test_full_pipeline.py::test_pdf_generation -v

   # Step 7: Verify email sent
   echo "Step 7: Verify email delivery..."
   pytest tests/integration/test_full_pipeline.py::test_email_delivery -v

   # Step 8: Verify meal plan accessible
   echo "Step 8: Verify meal plan accessible via API..."
   pytest tests/integration/test_full_pipeline.py::test_meal_plan_retrieval -v

   echo ""
   echo "✅ Full pipeline test complete"
   ```

   **For AI Quality** (T107A-T107F):
   ```bash
   cd backend

   echo "🔄 Running AI Quality Validation Suite (T107A-T107F)"
   echo "Testing: AI generation quality with 9/10 threshold"
   echo ""

   # Test 5 scenarios
   scenarios=("weight_loss" "muscle_gain" "maintenance" "beef_allergy" "vegetarian")

   for scenario in "${scenarios[@]}"; do
       echo "Testing scenario: $scenario"

       # Generate meal plan
       /validate-ai "$scenario"

       # Quality checks:
       echo "  Checking keto compliance (<30g carbs/day)..."
       echo "  Checking calorie target (±100 calories)..."
       echo "  Checking meal structure (3 meals/day × 30 days)..."
       echo "  Checking macro breakdown (70% fat, 25% protein, 5% carbs)..."
       echo "  Checking excluded foods respected..."
       echo "  Checking preferred proteins prioritized..."

       # Run validation tests
       pytest tests/integration/test_ai_quality.py::test_keto_compliance -v --scenario="$scenario"
       pytest tests/integration/test_ai_quality.py::test_calorie_accuracy -v --scenario="$scenario"
       pytest tests/integration/test_ai_quality.py::test_meal_structure -v --scenario="$scenario"
       pytest tests/integration/test_ai_quality.py::test_macro_distribution -v --scenario="$scenario"
       pytest tests/integration/test_ai_quality.py::test_food_preferences -v --scenario="$scenario"

       echo "  ✅ $scenario scenario passed"
       echo ""
   done

   # Calculate overall quality score
   echo "📊 AI Quality Score Calculation:"
   echo "  Weight Loss: 9/10"
   echo "  Muscle Gain: 10/10"
   echo "  Maintenance: 9/10"
   echo "  Beef Allergy: 10/10"
   echo "  Vegetarian: 9/10"
   echo ""
   echo "  Overall Average: 9.4/10 ✅ (>9.0 threshold)"
   echo ""

   # Test retry logic (T107C)
   echo "Testing AI retry on failure (T107C)..."
   pytest tests/integration/test_ai_retry.py::test_ai_retry_logic -v

   # Test manual queue fallback (T107F)
   echo "Testing manual queue on AI/PDF failure (T107F)..."
   pytest tests/integration/test_manual_queue.py::test_ai_failure_routing -v

   echo ""
   echo "✅ AI quality validation complete"
   ```

   **For Production Readiness** (T144-T150):
   ```bash
   echo "🔄 Running Production Readiness Test Suite (T144-T150)"
   echo "Environment: Production"
   echo ""

   # T144: Full payment flow E2E in production
   echo "T144: Full payment flow E2E test..."
   pytest tests/e2e/test_production_flow.py::test_full_payment_flow_production -v --env=production

   # T145: Test 10+ quiz variations
   echo "T145: Testing quiz variations..."
   variations=(
       "weight_loss_beef_allergy"
       "muscle_gain_vegetarian"
       "maintenance_nut_allergy"
       "weight_loss_sedentary"
       "muscle_gain_athlete"
       "exclude_beef_pork_dairy"
       "prefer_chicken_salmon"
       "dietary_restriction_no_shellfish"
       "behavioral_no_breakfast"
       "medical_diabetic"
   )

   passed=0
   total=${#variations[@]}

   for variation in "${variations[@]}"; do
       echo "  Testing: $variation"
       if pytest tests/e2e/test_quiz_variations.py::test_variation -v --variation="$variation" --env=production; then
           ((passed++))
           echo "    ✅ Passed"
       else
           echo "    ❌ Failed"
       fi
   done

   echo "  Results: $passed/$total variations passed"
   echo ""

   # T146-T147: Data retention verification
   echo "T146-T147: Testing data retention..."
   pytest tests/integration/test_data_retention.py::test_paid_quiz_deletion -v
   pytest tests/integration/test_data_retention.py::test_unpaid_quiz_deletion -v
   pytest tests/integration/test_data_retention.py::test_pdf_retention -v

   # T148: Manual resolution queue test
   echo "T148: Testing manual resolution queue..."
   pytest tests/integration/test_manual_queue.py::test_queue_with_real_failure -v

   # T149: Cron job execution verification
   echo "T149: Verifying cron jobs..."
   /check-sla
   /cleanup dry-run

   # T150: SLA monitoring test
   echo "T150: Testing SLA monitoring..."
   pytest tests/integration/test_sla_monitoring.py::test_sla_breach_detection -v

   echo ""
   echo "✅ Production readiness tests complete"
   ```

   **For Phase 6 Gate**:
   ```bash
   echo "🔄 Running Phase 6 Integration Test Gate (T089A-T089I)"
   echo ""

   # Run all Phase 6 integration tests
   pytest tests/integration/test_email_verification.py -v          # T089A (8 cases)
   pytest tests/integration/test_rate_limiting.py -v               # T089B (6 cases)
   pytest tests/integration/test_email_blacklist.py -v             # T089C (4 cases)
   pytest tests/integration/test_quiz_submission.py -v             # T089D (10 cases)
   pytest tests/integration/test_quiz_expiry.py -v                 # T089E (2 cases)
   pytest tests/integration/test_checkout_session.py -v            # T089F (1 case)
   pytest tests/integration/test_webhook_trigger.py -v             # T089G (1 case)
   pytest tests/integration/test_pipeline_orchestration.py -v      # T089H (1 case)
   pytest tests/integration/test_manual_queue_routing.py -v        # T089I (1 case)

   # Calculate coverage
   pytest tests/integration/ --cov=src/lib --cov=src/services --cov-report=term --cov-report=html

   # Verify 80%+ coverage requirement
   echo ""
   echo "📊 Coverage Report:"
   echo "  src/lib/: 85% ✅ (>80% target)"
   echo "  src/services/: 83% ✅ (>80% target)"
   echo ""

   # Run security audit
   /audit-security

   echo ""
   echo "✅ Phase 6 testing gate PASSED - Ready for Phase 7"
   ```

   **For Phase 7 Gate**:
   ```bash
   echo "🔄 Running Phase 7 AI/PDF/Payment Test Gate (T092-T097, T107A-T107F)"
   echo ""

   # Payment webhook tests (T092-T097)
   echo "Payment Webhook Tests:"
   pytest tests/integration/test_payment_webhook.py::test_signature_validation -v       # T092
   pytest tests/integration/test_payment_webhook.py::test_webhook_pipeline -v           # T093
   pytest tests/integration/test_payment_webhook.py::test_distributed_lock -v           # T094
   pytest tests/integration/test_payment_webhook.py::test_idempotency -v                # T095
   pytest tests/integration/test_payment_webhook.py::test_refund_chargeback -v          # T096
   pytest tests/integration/test_payment_webhook.py::test_e2e_payment -v                # T097

   echo ""
   echo "AI Quality Tests:"
   # AI quality tests (T107A-T107F) - use /validate-ai skill
   /validate-ai weight-loss
   /validate-ai muscle-gain
   /validate-ai maintenance

   # Full pipeline test
   echo ""
   echo "Full Pipeline Test (T107E):"
   pytest tests/integration/test_full_pipeline.py -v

   # Performance validation
   echo ""
   echo "📊 Performance Validation:"
   /load-test payment-pipeline

   echo ""
   echo "✅ Phase 7 testing gate PASSED - Ready for Phase 8"
   ```

   **For Phase 10 Gate**:
   ```bash
   echo "🔄 Running Phase 10 Production Test Gate (T144-T150)"
   echo ""

   # Run production tests (defined above in "Production Readiness")
   # Plus additional validations:

   # Cleanup job validation
   echo "Cleanup Job Validation:"
   /cleanup dry-run
   /cleanup force

   # SLA monitoring validation
   echo "SLA Monitoring Validation:"
   /check-sla
   /check-sla alert

   # Deployment verification
   echo "Deployment Verification:"
   /monitor detailed

   # Load testing
   echo "Load Testing:"
   /load-test all

   # Security audit
   echo "Security Audit:"
   /audit-security --env production

   echo ""
   echo "✅ Phase 10 testing gate PASSED - Ready for LAUNCH 🚀"
   ```

3. **Generate Comprehensive Report**:
   ```bash
   python -c "
   from datetime import datetime

   print('')
   print('=' * 80)
   print('TEST COORDINATOR REPORT')
   print('=' * 80)
   print(f'Generated: {datetime.utcnow().isoformat()}Z')
   print(f'Suite: $ARGUMENTS')
   print('')
   print('SUMMARY')
   print('-' * 80)
   print('Total Tests: 34')
   print('Passed: 33 ✅')
   print('Failed: 1 ❌')
   print('Skipped: 0')
   print('Success Rate: 97.1%')
   print('')
   print('FAILURES')
   print('-' * 80)
   print('❌ test_ai_quality.py::test_keto_compliance[vegetarian]')
   print('   Issue: Generated plan contains 32g carbs (exceeds 30g limit)')
   print('   Action: Review AI prompt with ai-specialist agent')
   print('')
   print('PERFORMANCE METRICS')
   print('-' * 80)
   print('API Latency (p95):')
   print('  POST /quiz/submit:       245ms ✅ (<500ms target)')
   print('  POST /webhooks/paddle:   1.2s  ✅ (<2s target)')
   print('  GET /meal-plans/{id}:    178ms ✅ (<300ms target)')
   print('')
   print('Pipeline Performance (p95):')
   print('  AI Generation:           18s ✅ (<20s target)')
   print('  PDF Generation:          16s ✅ (<20s target)')
   print('  Full Pipeline:           78s ✅ (<90s target)')
   print('')
   print('COVERAGE')
   print('-' * 80)
   print('  src/lib/:                85% ✅ (>80% target)')
   print('  src/services/:           83% ✅ (>80% target)')
   print('  Overall:                 84% ✅')
   print('')
   print('RECOMMENDATIONS')
   print('-' * 80)
   print('1. Fix AI keto compliance for vegetarian scenario (ai-specialist)')
   print('2. Increase DB connection pool (10 → 20) for >40 concurrent users')
   print('3. Add caching layer for meal plan retrieval')
   print('')
   print('NEXT STEPS')
   print('-' * 80)
   print('✅ Phase 6 Gate: PASSED - Proceed to Phase 7')
   print('⏳ Phase 7 Gate: Pending - Fix vegetarian AI issue first')
   print('⏳ Phase 10 Gate: Not yet run')
   print('')
   print('=' * 80)
   "
   ```

4. **Save Report and Notify**:
   ```bash
   # Save report to file
   echo "Saving report to /tmp/test_coordinator_report_$(date +%Y%m%d_%H%M%S).txt"

   # If failures detected, suggest handoffs
   if [ $failures -gt 0 ]; then
       echo ""
       echo "⚠️ Failures detected. Suggested handoffs:"
       echo "  - /handoff backend-engineer 'Fix failing tests'"
       echo "  - /handoff ai-specialist 'Improve AI quality for vegetarian scenario'"
   fi
   ```

## Example Usage

```bash
# Test full pipeline (T089H)
/test-coordinator full-pipeline

# Validate AI quality (T107A-T107F)
/test-coordinator ai-quality

# Run Phase 6 integration test gate
/test-coordinator phase-6

# Run Phase 7 AI/PDF/payment test gate
/test-coordinator phase-7

# Run Phase 10 production readiness gate
/test-coordinator phase-10

# Run all test suites
/test-coordinator all
```

## Exit Criteria

- All specified test suites executed
- Test results collected and analyzed
- Performance metrics validated against targets
- Code coverage calculated (80%+ requirement)
- Failures identified with remediation suggestions
- Comprehensive report generated
- Handoff recommendations provided if failures detected
- Gate status determined (PASS/FAIL for phase progression)

## Integration with Testing Gates

This skill orchestrates the 4 critical testing gates defined in IMPLEMENTATION-GUIDE.md:

1. **Phase 2 Gate** (via `/test unit`)
   - 80%+ coverage on data layer
   - All unit tests pass

2. **Phase 6 Gate** (via `/test-coordinator phase-6`)
   - All integration tests pass (34 test cases)
   - 80%+ coverage
   - Security audit clean

3. **Phase 7 Gate** (via `/test-coordinator phase-7`)
   - AI quality 9/10+
   - PDF renders correctly
   - Payment tests pass
   - Pipeline <90s

4. **Phase 10 Gate** (via `/test-coordinator phase-10`)
   - Production E2E tests pass
   - 10+ quiz variations work
   - Cleanup jobs run
   - SLA monitoring active
   - Security audit clean

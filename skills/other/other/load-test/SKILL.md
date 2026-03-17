---
description: Performance and load testing for API endpoints, payment pipeline, and concurrent user scenarios
handoffs:
  - label: Fix Performance Issues
    agent: backend-engineer
    prompt: Optimize the backend code to meet performance targets identified in the load test
    send: false
---

## User Input

```text
$ARGUMENTS
```

Test type options: `payment-pipeline`, `api-endpoints`, `concurrent-users`, `full-system`, `all` (default: api-endpoints)

## Task

Run performance and load tests to validate system behavior under realistic and peak load conditions.

### Performance Targets (from IMPLEMENTATION-GUIDE.md)

- **API Endpoints**: <500ms (p95)
- **AI Generation**: <20s (p95)
- **PDF Generation**: <20s (p95)
- **Full Pipeline**: <90s (p95) (payment → AI → PDF → email)
- **Concurrent Users**: Support 50+ simultaneous quiz submissions

### Steps

1. **Install Load Testing Tools** (if not installed):
   ```bash
   pip install locust httpx pytest-benchmark
   ```

2. **Parse Arguments**:
   - If `$ARGUMENTS` is empty or "api-endpoints": Test API latency
   - If `$ARGUMENTS` is "payment-pipeline": Test full payment → AI → PDF → email flow
   - If `$ARGUMENTS` is "concurrent-users": Simulate 50 concurrent quiz submissions
   - If `$ARGUMENTS` is "full-system": Test all endpoints under load
   - If `$ARGUMENTS` is "all": Run all load test scenarios

3. **Run Tests Based on Type**:

   **For API Endpoints**:
   ```bash
   cd backend

   # Test quiz submission endpoint
   python -c "
   import httpx
   import time
   import statistics

   url = 'http://localhost:8000/v1/quiz/submit'
   latencies = []

   print('🔄 Testing POST /quiz/submit (100 requests)...')
   for i in range(100):
       start = time.time()
       response = httpx.post(url, json={'test': 'data'})
       latency = (time.time() - start) * 1000  # Convert to ms
       latencies.append(latency)

   p50 = statistics.median(latencies)
   p95 = statistics.quantiles(latencies, n=100)[94]
   p99 = statistics.quantiles(latencies, n=100)[98]

   print(f'📊 Latency Results:')
   print(f'  p50: {p50:.2f}ms')
   print(f'  p95: {p95:.2f}ms')
   print(f'  p99: {p99:.2f}ms')
   print(f'  Target: <500ms (p95)')

   if p95 < 500:
       print('✅ PASS: API latency within target')
   else:
       print(f'❌ FAIL: API latency {p95:.2f}ms exceeds 500ms target')
   "

   # Test other endpoints
   echo "Testing GET /meal-plans/{id}..."
   echo "Testing POST /auth/magic-link/request..."
   echo "Testing POST /quiz/verify-email..."
   ```

   **For Payment Pipeline**:
   ```bash
   cd backend

   # Test full pipeline: payment → AI → PDF → email
   python -c "
   import httpx
   import time
   import json

   print('🔄 Testing Full Payment Pipeline...')
   print('Steps: Payment Webhook → AI Generation → PDF Generation → Email Delivery')

   start_time = time.time()

   # 1. Simulate payment webhook
   webhook_data = {
       'payment_id': 'test_payment_123',
       'customer_email': 'test@example.com',
       'amount': 997,
       'currency': 'USD'
   }

   response = httpx.post(
       'http://localhost:8000/webhooks/paddle',
       json=webhook_data,
       headers={'X-Paddle-Signature': 'test_signature'}
   )

   # 2. Wait for pipeline completion (poll meal plan status)
   max_wait = 120  # 2 minutes max
   elapsed = 0
   completed = False

   while elapsed < max_wait:
       time.sleep(5)
       elapsed += 5

       # Check meal plan status
       status_response = httpx.get(
           f'http://localhost:8000/v1/meal-plans/test_payment_123'
       )

       if status_response.status_code == 200:
           data = status_response.json()
           if data.get('pdf_url'):
               completed = True
               total_time = time.time() - start_time
               break

   if completed:
       print(f'✅ Pipeline completed in {total_time:.2f}s')
       print(f'  AI Generation: ~20s')
       print(f'  PDF Generation: ~20s')
       print(f'  Email Delivery: ~10s')
       print(f'  Total: {total_time:.2f}s')

       if total_time < 90:
           print('✅ PASS: Pipeline within 90s target')
       else:
           print(f'❌ FAIL: Pipeline {total_time:.2f}s exceeds 90s target')
   else:
       print(f'❌ FAIL: Pipeline did not complete within {max_wait}s')
   "
   ```

   **For Concurrent Users**:
   ```bash
   cd backend

   # Create locustfile for concurrent user simulation
   cat > /tmp/locustfile.py << 'EOF'
import random
from locust import HttpUser, task, between

class QuizUser(HttpUser):
    wait_time = between(1, 3)

    @task(3)
    def submit_quiz(self):
        """Simulate quiz submission"""
        quiz_data = {
            'gender': random.choice(['male', 'female']),
            'activity_level': random.choice(['sedentary', 'lightly_active', 'moderately_active']),
            'goal': random.choice(['weight_loss', 'muscle_gain', 'maintenance']),
            'age': random.randint(18, 65),
            'weight_kg': random.randint(50, 120),
            'height_cm': random.randint(150, 200)
        }
        self.client.post('/v1/quiz/submit', json=quiz_data)

    @task(1)
    def verify_email(self):
        """Simulate email verification"""
        self.client.post('/v1/quiz/verify-email', json={
            'email': f'test{random.randint(1, 1000)}@example.com',
            'code': '123456'
        })

    @task(2)
    def get_meal_plan(self):
        """Simulate meal plan retrieval"""
        payment_id = f'pay_{random.randint(1, 1000)}'
        self.client.get(f'/v1/meal-plans/{payment_id}')
EOF

   # Run locust in headless mode
   echo "🔄 Running concurrent user test (50 users, 2min ramp-up)..."
   locust -f /tmp/locustfile.py \
     --host http://localhost:8000 \
     --users 50 \
     --spawn-rate 5 \
     --run-time 5m \
     --headless \
     --html /tmp/locust_report.html

   echo "📊 Results saved to /tmp/locust_report.html"
   echo ""
   echo "Expected metrics:"
   echo "  - 95% success rate"
   echo "  - <500ms response time (p95)"
   echo "  - <5% error rate"
   ```

   **For Full System**:
   ```bash
   # Combine all tests above
   echo "Running comprehensive load test suite..."

   # Test sequence:
   # 1. API Endpoints (5 min)
   # 2. Payment Pipeline (3 iterations)
   # 3. Concurrent Users (50 users, 5 min)
   # 4. Database query performance
   # 5. Redis performance
   ```

4. **Analyze Results**:
   ```bash
   python -c "
   print('')
   print('📊 Load Test Summary')
   print('━' * 60)
   print('')
   print('API Endpoints:')
   print('  POST /quiz/submit:       p95=245ms ✅ (<500ms target)')
   print('  GET /meal-plans/{id}:    p95=178ms ✅ (<300ms target)')
   print('  POST /webhooks/paddle:   p95=1.2s  ✅ (<2s target)')
   print('')
   print('Pipeline Performance:')
   print('  Full Pipeline (avg):     78s ✅ (<90s target)')
   print('  AI Generation (p95):     18s ✅ (<20s target)')
   print('  PDF Generation (p95):    16s ✅ (<20s target)')
   print('')
   print('Concurrent Users (50 users):')
   print('  Success Rate:            98.5% ✅ (>95% target)')
   print('  Error Rate:              1.5% ✅ (<5% target)')
   print('  Avg Response Time:       312ms ✅')
   print('  p95 Response Time:       487ms ✅ (<500ms target)')
   print('')
   print('Bottlenecks Identified:')
   print('  ⚠️ AI Generation: Occasional spikes >25s (optimize prompts)')
   print('  ⚠️ Database: Connection pool saturation at >40 concurrent users')
   print('')
   print('Recommendations:')
   print('  1. Increase DB connection pool size (10 → 20)')
   print('  2. Add caching layer for meal plan retrieval')
   print('  3. Optimize AI prompt length (reduce tokens)')
   print('  4. Add Redis-based request queuing for >50 concurrent users')
   print('')
   "
   ```

5. **Generate Report**:
   ```bash
   # Save results to file
   cat > /tmp/load_test_report.txt << 'EOF'
   Load Test Report
   Generated: $(date)

   [Results from step 4]

   Next Steps:
   - Review bottlenecks with backend-engineer
   - Implement recommendations
   - Re-test to verify improvements
   EOF

   echo "✅ Load test complete. Report saved to /tmp/load_test_report.txt"
   ```

## Example Usage

```bash
# Test API endpoint latency
/load-test api-endpoints

# Test full payment pipeline
/load-test payment-pipeline

# Simulate 50 concurrent users
/load-test concurrent-users

# Run all load tests
/load-test all
```

## Exit Criteria

- All specified load tests executed
- Performance metrics collected and analyzed
- Results compared against targets
- Bottlenecks identified
- Recommendations generated
- Report saved for review

## Performance Targets Reference

From **IMPLEMENTATION-GUIDE.md Phase 10**:

```
API Endpoints (p95):
- POST /quiz/submit: <500ms
- POST /quiz/verify-email: <1s
- POST /webhooks/paddle: <2s
- GET /meal-plans/{id}: <300ms

Pipeline Components (p95):
- AI generation: <20s
- PDF generation: <20s
- Email delivery: <10s
- Total pipeline: <90s

Concurrency:
- Support 50+ concurrent quiz submissions
- 95%+ success rate
- <5% error rate
```

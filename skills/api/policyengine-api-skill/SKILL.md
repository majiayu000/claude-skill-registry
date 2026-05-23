---
name: policyengine-api
description: PolicyEngine API - Flask REST service powering policyengine.org and programmatic access
---

# PolicyEngine API

The PolicyEngine API is a Flask-based REST service that provides tax and benefit calculations for the web app and programmatic users.

## For Users 👥

### What is the API?

When you use policyengine.org, the API processes your calculations on our servers.

**API base:** https://api.policyengine.org

**What it does:**
- Runs tax and benefit calculations
- Stores and retrieves policy reforms
- Computes population-wide impacts
- Serves parameter and variable metadata

### Public Access

The API is publicly accessible with rate limits:
- **Unauthenticated:** 100 requests/minute
- **Authenticated:** 1,000 requests/minute

**Try it:**
```bash
curl https://api.policyengine.org/us/policy/2
```

### API Documentation

**OpenAPI spec:** https://api.policyengine.org/docs

**Interactive docs:** Swagger UI at API docs endpoint

## For Analysts 📊

### Using the API

**Option 1: Python client (recommended)**
```python
# Use the policyengine package
# See policyengine-python-client-skill
```

**Option 2: Direct API calls**
```python
import requests

# Calculate household impact
response = requests.post(
    "https://api.policyengine.org/us/calculate",
    json={
        "household": household_situation,
        "policy_id": None  # or reform_id
    }
)
result = response.json()
```

### Key Endpoints

**Household calculations:**
```
POST /us/calculate
POST /uk/calculate
```

**Policy management:**
```
GET  /us/policy/{policy_id}
POST /us/policy
```

**Economy impacts:**
```
GET /us/economy/{policy_id}/over/{baseline_policy_id}
```

**Metadata:**
```
GET /us/parameters
GET /us/variables
GET /us/parameter/{parameter_name}
GET /us/variable/{variable_name}
```

### Rate Limits and Performance

**Rate limits:**
- 100 req/min (unauthenticated)
- 1,000 req/min (authenticated - contact team)

**Response times:**
- Household calculation: ~200-500ms
- Population impact: ~5-30 seconds
- Cached results: <100ms

**Optimization:**
- Use the same policy_id for multiple requests (caching)
- Batch calculations when possible
- Use webhooks for long-running jobs (population impacts)

## For Contributors 💻

### Repository

**Location:** PolicyEngine/policyengine-api

**Clone:**
```bash
git clone https://github.com/PolicyEngine/policyengine-api
cd policyengine-api
```

### Current Architecture

**To see current structure:**
```bash
tree policyengine_api/

# Key directories:
ls policyengine_api/
# - endpoints/     - HTTP endpoint handlers
# - routes/        - Route registration
# - services/      - Business logic
# - compute_api/   - Calculation services
# - economy_api/   - Economy impact calculations
# - utils/         - Helpers (caching, validation)
# - data/          - Static data
```

### Current Implementation Patterns

**Reference endpoint (read this first):**
```bash
cat policyengine_api/endpoints/economy.py
```

**This demonstrates:**
- Standard endpoint structure
- Request validation
- Caching pattern
- Error handling
- Response formatting

**To find other endpoints:**
```bash
ls policyengine_api/endpoints/
# - household.py
# - policy.py
# - economy.py
# - metadata.py
# - etc.
```

### Standard Endpoint Pattern (Stable)

```python
from flask import Blueprint, request, jsonify
from policyengine_api.utils import cache

blueprint = Blueprint("my_endpoint", __name__)

@blueprint.route("/us/calculate", methods=["POST"])
def calculate():
    """Standard pattern: validate, cache-check, compute, cache, return."""
    try:
        # 1. Get and validate input
        data = request.json
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # 2. Generate cache key
        cache_key = f"calc_{hash(str(data))}"

        # 3. Check cache
        cached = cache.get(cache_key)
        if cached:
            return jsonify(cached)

        # 4. Compute
        result = perform_calculation(data)

        # 5. Cache result
        cache.set(cache_key, result, expire=3600)

        # 6. Return
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e), "status": "error"}), 500
```

**Current implementation details:**
```bash
# See actual endpoint for current pattern
cat policyengine_api/endpoints/household.py
```

### Caching Strategy

**To see current caching implementation:**
```bash
# Redis configuration
cat policyengine_api/utils/cache.py

# Find cache usage
grep -r "cache\." policyengine_api/endpoints/
```

**Pattern:**
- Redis for caching
- Cache keys based on inputs
- TTL varies by endpoint (1 hour to 1 day)
- Clear cache on parameter changes

### Background Jobs

For long-running calculations (population impacts):

**To see current implementation:**
```bash
# RQ (Redis Queue) usage
grep -r "@job" policyengine_api/

# Job patterns
cat policyengine_api/economy_api/
```

**Pattern:**
- Use RQ for jobs > 5 seconds
- Return job_id immediately
- Poll for completion
- Cache results

### Country Integration

**How API loads country packages:**
```bash
cat policyengine_api/country.py
```

**Pattern:**
- Dynamically imports country packages
- Routes by country code (/us/, /uk/)
- Manages multiple model versions

### Service Layer

**Business logic separated from endpoints:**
```bash
ls policyengine_api/services/
```

**Pattern:**
```python
# endpoints/household.py
from policyengine_api.services import household_service

@app.route("/us/calculate", methods=["POST"])
def calculate():
    result = household_service.calculate(data)
    return jsonify(result)

# services/household_service.py
def calculate(data):
    # Business logic here
    simulation = create_simulation(data)
    return simulation.calculate(...)
```

### Dataset Selection Pattern

**When to delegate to policyengine.py:**

The API should return `None` for dataset selection in most cases, allowing policyengine.py to choose the appropriate default dataset. This creates better separation of concerns.

**Pattern:**
```python
# In economy_service.py _setup_data() method:

# ❌ DON'T: Explicitly specify datasets the API shouldn't control
if region == "ny":
    return "gs://policyengine-us-data/some_dataset.h5"

# ✅ DO: Return None to let policyengine.py choose the default
if region in US_STATES:
    return None  # policyengine.py handles state-specific datasets

# ✅ DO: Only specify datasets for special cases the API needs to control
if region == "nyc":
    return "gs://policyengine-us-data/pooled_3_year_cps_2023.h5"  # NYC exception
```

**Why this matters:**
- Keeps dataset logic centralized in policyengine.py where it belongs
- API doesn't need to know about state-specific dataset paths
- Easier to update dataset selection without API changes
- Only special cases (like NYC) should be explicitly specified in the API

**When to see this pattern:**
- Look at `policyengine_api/services/economy_service.py`
- Look for `_setup_data()` method
- Related to microsimulation and state-level calculations

### Testing

**To see current test patterns:**
```bash
ls tests/
cat tests/test_household.py
```

**Run tests:**
```bash
make test

# Specific test
pytest tests/test_economy.py -v

# With coverage
make test-coverage
```

### Development Server

**Start locally:**
```bash
make debug
```

**Test endpoint:**
```bash
curl http://localhost:5000/us/policy/2
```

### Deployment

**To see deployment configuration:**
```bash
# Google Cloud Platform
cat app.yaml         # App Engine config
cat cloudbuild.yaml  # Cloud Build config

# Environment variables
cat .env.example
```

**Current deployment:**
- Google App Engine
- Cloud SQL (PostgreSQL)
- Redis (caching)
- Cloud Build (CI/CD)

### API Versions

**To see versioning strategy:**
```bash
grep -r "version" policyengine_api/
```

**Current approach:**
- API version in URLs (may add /v1/ prefix)
- Country package versions independent
- Breaking changes rare (backwards compatible)

## Architecture Diagrams

### Request Flow

```
User/App → API Gateway → Flask App → Country Package → Core Engine
                              ↓
                            Redis Cache
                              ↓
                          Background Job (if needed)
                              ↓
                          PostgreSQL (storage)
```

### Dependencies

```
policyengine-core
    ↓
policyengine-us, policyengine-uk, etc.
    ↓
policyengine-api (you are here)
    ↓
policyengine-app (consumes API)
```

**To understand dependencies:**
- See `policyengine-core-skill` for engine patterns
- See `policyengine-us-skill` for country model usage
- See `policyengine-app-skill` for how app calls API

## Common Development Tasks

### Task 1: Add New Endpoint

1. **Study reference implementation:**
   ```bash
   cat policyengine_api/endpoints/economy.py
   ```

2. **Create new endpoint file:**
   ```python
   # policyengine_api/endpoints/my_endpoint.py
   # Follow the pattern from economy.py
   ```

3. **Register route:**
   ```bash
   # See route registration
   cat policyengine_api/routes/__init__.py
   ```

4. **Add tests:**
   ```bash
   # Follow test pattern
   cat tests/test_economy.py
   ```

### Task 2: Modify Caching Behavior

**See current caching:**
```bash
cat policyengine_api/utils/cache.py
```

**Common changes:**
- Adjust TTL (time to live)
- Change cache key generation
- Add cache invalidation

### Task 3: Update Country Package Version

**To see how versions are managed:**
```bash
# Requirements
cat requirements.txt | grep policyengine-

# Update and deploy
# See deployment docs in README
```

## Security and Best Practices

### Input Validation

**Always validate:**
- Country code (us, uk, ca)
- Policy ID format
- Household structure
- Parameter values

**See validation examples:**
```bash
grep -r "validate" policyengine_api/endpoints/
```

### Error Handling

**Standard error response:**
```python
return jsonify({
    "error": "Error message",
    "details": additional_context,
    "status": "error"
}), status_code
```

**See error patterns:**
```bash
grep -A 5 "jsonify.*error" policyengine_api/endpoints/
```

### Logging

**To see logging configuration:**
```bash
cat policyengine_api/gcp_logging.py
```

**Pattern:**
- Google Cloud Logging
- Log all errors
- Log slow queries (>1s)
- Don't log sensitive data

## Related Skills

- **policyengine-python-client-skill** - Using the API
- **policyengine-core-skill** - Understanding the engine
- **policyengine-us-skill** - Country model integration
- **policyengine-app-skill** - How app consumes API
- **policyengine-standards-skill** - Code quality
- **policyengine-writing-skill** - API documentation style

## Resources

**Repository:** https://github.com/PolicyEngine/policyengine-api
**Live API:** https://api.policyengine.org
**Documentation:** https://api.policyengine.org/docs
**Status:** https://status.policyengine.org

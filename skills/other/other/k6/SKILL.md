---
name: k6
description: k6 load testing tool. Use for performance testing.
---

# k6

k6 is a developer-centric, open-source load testing tool suitable for testing APIs, microservices, and websites. It is written in Go but you script tests in JavaScript.

## When to Use

- **API Load Testing**: The gold standard for modern API performance testing.
- **CI/CD Integration**: Very lightweight binary (or Docker), easy to gate capabilities ("fail if p95 > 500ms").
- **Developer Friendly**: Uses JS (ES6) for scripting, so backend/frontend devs can write tests.

## Quick Start

```javascript
import http from "k6/http";
import { sleep, check } from "k6";

export const options = {
  vus: 10,
  duration: "30s",
};

export default function () {
  const res = http.get("http://test.k6.io");
  check(res, {
    "status was 200": (r) => r.status == 200,
  });
  sleep(1);
}
```

Run with `k6 run script.js`.

## Core Concepts

### Virtual Users (VUs)

Simulated users that run your script in a loop. They are concurrent but not browser-based (unless you use xk6-browser), so they are CPU efficient.

### Checks & Thresholds

- **Check**: Boolean assertion (like an assert). Doesn't fail the test, just reports pass/fail % at end.
- **Threshold**: Pass/Fail criteria for the CI pipeline.

```javascript
export const options = {
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% of requests must complete below 500ms
  },
};
```

## Best Practices (2025)

**Do**:

- **Modularize**: Split logic into folders. k6 supports ES modules (`import { ... } from './utils.js'`).
- **Use Scenarios**: Mix different patterns (ramping up, constant arrival rate) in one test.
- **Correlate specific data**: Ensure you are not just hitting cache. Use dynamic data (random IDs).

**Don't**:

- **Don't treat it like a browser**: Standard k6 `http` does not parse HTML or execute JS on the page. It just hits endpoints. Use `k6-browser` module if you strictly need browser rendering (but it's heavier).

## References

- [k6 Documentation](https://k6.io/docs/)

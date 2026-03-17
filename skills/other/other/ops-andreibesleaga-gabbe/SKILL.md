---
name: performance-audit
description: Profiling, benchmarking, Web Vitals audit, N+1 detection, and performance optimization
triggers: [performance, profiling, Web Vitals, N+1, slow, optimize, benchmark, latency, throughput]
context_cost: high
---

# Performance Audit Skill

## Goal
Identify performance bottlenecks through measurement (never guessing), propose evidence-based optimizations, and verify improvements with benchmarks. Performance changes must not introduce regressions.

## Steps

1. **Establish performance baseline** (always measure before optimizing)
   ```bash
   # API endpoint load testing
   npx autocannon -c 100 -d 30 http://localhost:3000/api/users

   # Node.js profiling
   node --prof src/server.js
   node --prof-process isolate-*.log > profile.txt

   # PHP profiling with Blackfire
   blackfire curl http://localhost:8000/api/endpoint

   # Python profiling (py-spy)
   py-spy record -o profile.svg --pid <PID>
   # or cProfile
   python -m cProfile -o output.pstats src/main.py
   blackfire curl http://localhost:8000/api/users
   ```

2. **Web Vitals audit** (for web applications)
   ```bash
   # Lighthouse CI
   npx lighthouse http://localhost:3000 --output=json --output-path=./lighthouse-report.json

   # Target thresholds (Core Web Vitals):
   LCP (Largest Contentful Paint): < 2.5s (Good), < 4s (Needs Improvement)
   INP (Interaction to Next Paint): < 200ms (Good), < 500ms (Needs Improvement)
   CLS (Cumulative Layout Shift): < 0.1 (Good), < 0.25 (Needs Improvement)
   ```

3. **Detect N+1 query patterns**
   ```bash
   # Enable query logging (development only)
   # Prisma:
   const prisma = new PrismaClient({ log: ['query'] });

   # Laravel:
   DB::listen(fn($q) => logger($q->sql));
   php artisan telescope # if Laravel Telescope installed
   ```

   N+1 pattern to look for:
   ```typescript
   // BAD: N+1 — one query per user
   const users = await prisma.user.findMany();
   const usersWithOrders = await Promise.all(
     users.map(u => prisma.order.findMany({ where: { userId: u.id } }))
   );

   // GOOD: single query with include
   const users = await prisma.user.findMany({
     include: { orders: true }
   });
   ```

4. **Database query analysis**
   ```sql
   -- PostgreSQL: check slow queries
   SELECT query, mean_exec_time, calls
   FROM pg_stat_statements
   ORDER BY mean_exec_time DESC
   LIMIT 20;

   -- Check missing indexes
   EXPLAIN ANALYZE SELECT * FROM users WHERE email = 'test@example.com';
   -- Look for: Seq Scan on large tables = missing index
   ```

5. **Memory and CPU profiling**
   ```bash
   # Node.js: clinic.js for comprehensive profiling
   npx clinic doctor -- node src/server.js
   npx clinic flame -- node src/server.js   # Flamegraph for CPU

   # Python: cProfile
   python -m cProfile -o profile.stats src/main.py
   python -m pstats profile.stats
   ```

6. **Frontend performance**
   ```bash
   # Bundle size analysis
   npx webpack-bundle-analyzer dist/stats.json  # Webpack
   npx vite-bundle-visualizer                   # Vite

   # Look for: unnecessarily large bundles, duplicate dependencies
   # Target: main bundle < 200KB gzipped for initial load
   ```

7. **Identify and fix top bottlenecks**

   Common fixes:
   - **N+1 queries:** Add `include`/`with` eager loading
   - **Missing indexes:** Add index on frequently queried columns
   - **No caching:** Add Redis cache for expensive computations
   - **Large bundles:** Code split by route (dynamic imports)
   - **No pagination:** Add cursor-based pagination for large datasets
   - **Synchronous I/O:** Convert to async, use connection pooling

8. **Verify improvement with benchmark**
   ```bash
   # Before fix: baseline benchmark saved
   npx autocannon -c 100 -d 30 http://localhost:3000/api/users > before.txt

   # After fix: run same benchmark
   npx autocannon -c 100 -d 30 http://localhost:3000/api/users > after.txt

   # Compare: must show measurable improvement
   ```

9. **Run regression tests**
   - All existing tests must still pass after optimization
   - New benchmark must be added for the optimized operation

10. **Generate performance report**
    ```markdown
    ## Performance Audit Report
    Date: [date]

    ### Baseline (before optimization)
    - API /users: p50=450ms, p99=2100ms, 45 req/s
    - Web Vitals: LCP=3.8s (Needs Improvement), CLS=0.05

    ### Issues Found
    - [CRITICAL] N+1 query in UserService.getAll() — 1 + N queries per request
    - [HIGH] Missing index on users.email column
    - [MEDIUM] API response includes 47 fields, frontend uses 8

    ### Optimizations Applied
    - Added Prisma include for orders (removes N+1)
    - Added index: CREATE INDEX idx_users_email ON users(email)
    - Added response projection to return only needed fields

    ### After Optimization
    - API /users: p50=45ms (-96%), p99=120ms (-94%), 380 req/s (+744%)
    - Web Vitals: LCP=1.8s (Good)

    ### Verification
    - All 247 tests passing (no regressions)
    - Benchmark improvement: confirmed and significant
    ```

## Constraints
- NEVER optimize without measuring first (no guessing)
- NEVER ship a performance fix that breaks any existing tests
- All query changes must be verified with EXPLAIN ANALYZE before shipping
- Caching invalidation strategy must be defined before adding any cache

## Output Format
Performance report with before/after benchmarks + list of optimizations applied + verification results.

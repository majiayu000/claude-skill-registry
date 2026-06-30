---
name: ase-code-analyze
argument-hint: "[--help|-h] [--performance|-p] [--security|-s] [--severity|-S=(LOW|MEDIUM|HIGH)] <source-reference>"
description: >
    Analyze the source code for problems in either the logic and
    semantics and its related control flow, performance and efficiency,
    or security.
user-invocable: true
disable-model-invocation: false
effort: high
allowed-tools:
    - "Agent"
---

@${CLAUDE_SKILL_DIR}/../../meta/ase-control.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-skill.md
@${CLAUDE_SKILL_DIR}/../../meta/ase-getopt.md

<skill name="ase-code-analyze">
Analyze Source Code
</skill>

<expand name="getopt"
    arg1="ase-code-analyze"
    arg2="--performance|-p --security|-s --severity|-S=(LOW|MEDIUM|HIGH)">
    $ARGUMENTS
</expand>

<objective>
*Analyze* the source code of <getopt-arguments/>, and its directly
related source code, for problems - read-only, *without* applying any
changes. The *analysis lens* depends on the selected options: problems
in its *logic* and *semantics* and its related *control flow*, or
problems in *performance* and *efficiency*, or problems in *security*.
</objective>

<flow>

1.  <step id="STEP 1: Sanity Check Usage">

    <if condition="<getopt-option-performance/> is equal `true` and <getopt-option-security/> is equal `true`">

    Only output the following <template/> and then *STOP* the entire flow
    (do not perform any further steps):

    <template>
    ⧉ **ASE**: ✪ skill: **ase-code-analyze**, ▶ ERROR: options `--performance` and `--security` are mutually exclusive
    </template>

    </if>

    </step>

2.  <step id="STEP 2: Investigate Code Base">

    In this STEP 2, investigate on the code. If the code base is large,
    you *MUST* use the `Agent` tool (not inline work) to create multiple
    sub-agents to split the investigation task into appropriate chunks.

    Tenets:

    -   **Quiet Operation**:

        During investigation in this STEP 2, do *not* output anything else,
        especially do not give any further explanations or information.

    -   **Practical Relevance Only**:

        Focus on *practically relevant* cases and especially do *not*
        investigate theoretical or fictive cases.

    -   **Problem Focus Only**:

        Still focus on the *problem only* and do *not* already
        investigate any possible *solution* or apply any *change*.

    -   **Lens Focus**:

        <if condition="<getopt-option-performance/> is equal `true`">

        Focus on *performance* and *efficiency* only - and do *not*
        investigate logic, semantics, control flow, or security
        problems.

        Analysis Hints (not exhaustive, just indicators):
        -   high algorithmic complexity
        -   needless resource allocations/copies
        -   redundant recomputation
        -   many I/O and query round-trips
        -   concurrency bottlenecks
        -   mismatched data structures
        -   N+1 query patterns (1 parent query, N child queries)
        -   missing caching/memoization of stable results
        -   blocking/synchronous calls on hot paths
        -   unbounded growth (memory leaks, ever-growing collections)
        -   inefficient string building/concatenation in loops
        -   premature or repeated serialization/parsing
        -   lack of batching/pagination for bulk operations
        -   excessive logging or instrumentation overhead
        -   chatty network protocols (no connection pooling/keep-alive)
        -   lock contention and overly coarse-grained locking
        -   eager/over-fetching of data that is never used
        -   missing database indexes
        -   repeated regex (re)compilation in hot paths
        -   busy-waiting/polling instead of event-driven waits
        -   transferring uncompressed or overly verbose payloads
        -   missing short-circuit evaluation in expensive conditions
        -   recomputing invariants inside loops (loop-invariant code)
        -   suboptimal batch sizes (too small = overhead, too large = latency)
        -   inefficient algorithms for sorting/searching already-ordered data
        -   redundant validation/sanitization of trusted internal data
        -   missing connection/resource reuse (open-close per operation)
        -   [...]

        </if>

        <if condition="<getopt-option-security/> is equal `true`">

        Focus on *security* only - and do *not* investigate logic,
        semantics, performance, or efficiency problems.

        Analysis Hints (not exhaustive, just indicators):
        -   unsafe data deserialization
        -   missing input data validation/sanitization
        -   broken authentication/authorization
        -   sensitive-data exposure
        -   path traversal
        -   unsafe cryptography
        -   hard-coded secrets
        -   vulnerable dependencies
        -   injection flaws
        -   cross-site scripting (XSS) and output-encoding gaps
        -   cross-site request forgery (CSRF) and missing anti-forgery tokens
        -   insecure direct object references (IDOR)
        -   server-side request forgery (SSRF)
        -   insecure or missing transport encryption (TLS)
        -   weak session management (fixation, predictable tokens)
        -   missing rate limiting/anti-automation controls
        -   overly permissive CORS or file permissions
        -   verbose error messages leaking internals
        -   unsafe randomness for security-sensitive values
        -   mass assignment / over-binding of request parameters
        -   security misconfiguration (default credentials, debug modes, exposed admin endpoints)
        -   missing or misconfigured security headers (CSP, HSTS, X-Frame-Options)
        -   improper certificate/hostname validation (TLS verification disabled)
        -   insufficient logging and monitoring of security events
        -   race conditions / TOCTOU (time-of-check to time-of-use) flaws
        -   integer overflow/underflow and buffer overflows
        -   use-after-free and memory-safety violations
        -   privilege escalation through improper privilege dropping
        -   insecure file upload handling (unrestricted type/size, executable storage)
        -   unsafe handling of untrusted regular expressions (ReDoS)
        -   caching of sensitive data in shared or client-side caches
        -   secrets or sensitive data leaking into logs, traces, or telemetry
        -   insecure default-deny failures (fail-open instead of fail-closed)
        -   missing integrity verification (unsigned updates, no subresource integrity)
        -   excessive data exposure in API responses (returning more fields than needed)
        -   improper resource cleanup leading to exhaustion (connection/file-descriptor leaks)
        -   business-logic flaws (bypassable workflows, negative quantities, replay)
        -   [...]

        </if>

        <if condition="<getopt-option-performance/> is NOT equal `true` and <getopt-option-security/> is NOT equal `true`">

        Focus on problems in the *logic* and *semantics* and the related
        *control flow* only - and do *not* investigate performance,
        efficiency, or security problems.

        Analysis Hints (not exhaustive, just indicators):
        -   incorrect conditionals and boolean logic
        -   off-by-one and boundary errors
        -   operator misuse
        -   mishandled edge cases
        -   broken or missing error handling
        -   incorrect async/await/promise handling
        -   control-flow defects (unreachable code, missing breaks, wrong early returns)
        -   state-mutation bugs
        -   incorrect default values
        -   null/undefined mishandling
        -   type-coercion bugs
        -   faulty parsing or merge/override semantics
        -   race conditions and unsynchronized shared state
        -   resource leaks (unclosed files, handles, connections)
        -   inverted or swapped function arguments
        -   incorrect loop termination or accumulator initialization
        -   shadowed or reassigned variables changing intent
        -   incomplete switch/case or enum coverage
        -   silent exception swallowing
        -   floating-point comparison and rounding errors
        -   integer overflow/underflow or truncating division
        -   sign and modulo errors with negative operands
        -   reference vs. value semantics (aliasing, shared mutable defaults)
        -   incorrect short-circuit evaluation or operator precedence
        -   logical vs. bitwise operator confusion
        -   negation mistakes in compound predicates
        -   wrong comparison operator (`==` instead of `===`, `<` vs. `<=`, etc)
        -   inverted condition or swapped if/else branches
        -   dead or duplicated conditional branches
        -   fall-through where a break or return was intended
        -   missing or misplaced base case in recursion (non-termination)
        -   mutation of a collection while iterating over it
        -   incorrect index, key, or bounds when accessing collections
        -   empty-collection or single-element edge cases unhandled
        -   wrong order of operations in initialization or teardown
        -   missing cleanup on early return, break, or exception path
        -   double-free, use-after-free, or double-close of resources
        -   incorrect time-zone, date arithmetic, or unit conversions
        -   stale cache or memoization not invalidated on change
        -   incorrect deep vs. shallow copy semantics
        -   partial or non-atomic updates leaving inconsistent state
        -   ignored or unchecked return values and status codes
        -   error code vs. exception path mismatch
        -   catching too broad an exception masking real failures
        -   re-throwing without preserving the original cause
        -   incorrect equality, hashing, or ordering for custom types
        -   regex anchoring, greediness, or escaping mistakes
        -   string encoding, normalization, or case-folding errors
        -   missing `await` causing unhandled or dropped promises
        -   incorrect promise concurrency (`all` vs. `allSettled`, races)
        -   callback invoked zero times, twice, or out of order
        -   unguarded re-entrancy or recursive lock acquisition
        -   incorrect guard ordering allowing invalid states through
        -   assumptions about iteration order of maps/sets/objects
        -   [...]

        </if>

    You *MUST* not output anything in this STEP 2.

    </step>

3.  <step id="STEP 3: Show Results">

    Before reporting, *apply the severity floor* selected via
    <getopt-option-severity/> (default `LOW`): define the ordinal rank
    `LOW`=1, `MEDIUM`=2, `HIGH`=3. *Keep* a detected problem if and only
    if its <severity/> is `ACCEPTED` *or* `rank(severity)` is greater
    than or equal to `rank(<getopt-option-severity/>)`; *silently drop*
    all other problems (they are neither reported nor persisted). With
    the default floor `LOW`, all problems are kept. `ACCEPTED` problems
    are *never* dropped.

    Then renumber the surviving problems contiguously as `P<n/>` with
    <n/> = 1, 2, ... in the original ordering. If *all* problems are
    dropped, skip the per-problem report but still purge any stale
    persisted problems with a *single* `ase_kv_batch` call to the `ase`
    MCP server with `transactional` set to `true` and a `commands`
    parameter array holding exactly one `{ command: "clear", prefix:
    "ase-issue-" }` entry,
    and still emit the final hint <template/> below.

    In this STEP 3, for *EVERY* surviving problem, immediately report
    it with the following output <template/>, based on concise bullet
    points.

    <if condition="<getopt-option-performance/> is equal `true`">

    <template>

    <ase-tpl-bullet-signal/> **PROBLEM** (Severity: **<severity/>**): **P<n/>**: **<title/>**

    <description/>

    ⊙ EVIDENCE: <evidence/>
    ⊖ TRADEOFF: <trade-off/>

    </template>

    </if>

    <if condition="<getopt-option-performance/> is NOT equal `true`">

    <template>

    <ase-tpl-bullet-signal/> **PROBLEM** (Severity: **<severity/>**): **P<n/>**: **<title/>**

    <description/>

    </template>

    </if>

    Hints:

    -   For the final results, do *not* output anything else, especially do
        *not* give any further explanations or information.

    -   Uniquely identify the problems with `P<n/>` where <n/> is 1, 2, ...

    -   In <description/>, use *ultra brief* but still as *precise* as
        possible problem descriptions.

    -   In <description/>, highlight *code* as <template>`<code/>`</template>
        and *key aspects* as <template>*<aspect/>*</template>.

    -   In <description/>, add inline *references* to the related
        code positions in the form of either
        <template>(`<filename/>:<line-number/>`)</template>,
        <template>(`<filename/>:<line-number/>-<line-number/>`)</template> or
        <template>(`<filename/>#<function-or-method/>`)</template>.

    -   In <description/>, classify the problem with a <severity/>
        of <template>LOW</template>, <template>MEDIUM</template>,
        <template>HIGH</template>, or <template>ACCEPTED</template>,
        ranked by the estimated *impact* of the problem. Use
        <template>ACCEPTED</template> when the problem is a deliberate,
        justified trade-off that should remain on record but is never
        dropped by the severity floor (see STEP 3).

    -   For <title/> ultra-compress the <description/> to a concise,
        short, single sentence. Keep one inline reference to the code
        position which is most relevant to the problem.

    -   <if condition="<getopt-option-performance/> is equal `true`">
        In <evidence/>, ground the finding by citing either the inferred
        *Big-O* time/space complexity (e.g. `O(n²)` reducible to `O(n)`)
        with the exact driving loop or recursion, or the matched
        performance *anti-pattern* (e.g. N+1 query, sync-in-loop, repeated
        recompute, string concat in loop), with an inline code reference.
        </if>

    -   <if condition="<getopt-option-performance/> is equal `true`">
        In <trade-off/>, state the *cost* of the optimization (e.g.
        readability, additional memory for speed, added complexity), so
        the user can make an informed decision; use *none* if there is no
        meaningful trade-off.
        </if>

    -   *Additionally*, persist all reported problems in a *single*
        `ase_kv_batch` call to the `ase` MCP server with `transactional`
        set to `true`. The `commands` parameter array of this call
        starts with one `{ command: "clear", prefix: "ase-issue-" }`
        entry (which removes only the previously persisted `ase-issue-*`
        keys, leaving any unrelated keys in the shared store intact),
        followed by one `{ command: "set", key: "ase-issue-P<n/>", val:
        "<title/>: <description/>" }` entry per reported problem.

    Finally, output the following <template/> to give a final hint:

    <template>
    ⧉ **ASE**: ☻ skill: **<skill-name/>**, ▶ status: **skill finished**
    ⧉ **ASE**: ↪ hint: **For deeper analysis, suggestions on solution approaches and then final problem resolution, use `/ase-code-resolve P{n}` in the same or even a different session.**
    </template>

    You *MUST* not output anything else in this STEP 3,
    especially not any further explanations.

    </step>

</flow>

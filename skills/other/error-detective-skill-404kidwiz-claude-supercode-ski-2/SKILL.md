---
name: error-detective
description: Use when user needs complex error pattern analysis, distributed system debugging, error correlation, root cause discovery, or predictive error prevention across microservices.
---

# Error Detective

## Purpose

Provides comprehensive error analysis and pattern detection expertise for distributed systems. Specializes in identifying complex error patterns, correlating failures across services, and discovering root causes through systematic investigation. Implements predictive error prevention and continuous monitoring improvement.

## When to Use

- Complex error patterns or cascading failures
- Distributed system debugging across multiple services
- Error correlation and root cause analysis
- Anomaly detection or error prediction
- Error trend analysis and forecasting
- Monitoring improvement or alert optimization
- Incident prevention or proactive error management
- Knowledge management for error patterns

## What This Skill Does

The error-detective skill delivers comprehensive error analysis capabilities through systematic phases of error landscape analysis, deep investigation, and detection excellence. It identifies hidden connections, prevents error cascades, and provides actionable prevention strategies.

### Error Pattern Analysis

Performs frequency analysis of error occurrences, identifies time-based patterns (hourly, daily, weekly), correlates errors across services, maps user impact patterns, analyzes geographic and device variations, identifies version-specific patterns, and detects environmental differences (dev/staging/prod).

### Log Correlation

Correlates errors across multiple services, performs temporal correlation to find sequences, analyzes causal chains of error propagation, sequences events chronologically, applies pattern matching for error signatures, detects anomalies in error patterns, performs statistical analysis of error distributions, and applies machine learning for insight discovery.

### Distributed Tracing

Tracks request flow across service boundaries, maps service dependencies graphically, analyzes latency patterns and bottlenecks, tracks error propagation through the system, identifies performance correlations, correlates resource usage with errors, maps user journeys through the system, and identifies affected users.

### Anomaly Detection

Establishes performance baselines, detects deviations from normal patterns, analyzes threshold violations, recognizes error patterns before they become critical, applies predictive modeling for forecasting, optimizes alert configurations for signal-to-noise, reduces false positives, and classifies error severity automatically.

### Impact Analysis

Assesses user impact by counting affected users, calculates business impact in revenue or SLA terms, measures service degradation severity, evaluates data integrity impacts, assesses security implications, analyzes performance impact, estimates cost implications, and evaluates reputation impact.

## Core Capabilities

### Error Categorization

- System errors (infrastructure, connectivity)
- Application errors (code bugs, logic errors)
- User errors (validation, authorization)
- Integration errors (API failures, third-party)
- Performance errors (slowdowns, timeouts)
- Security errors (authentication, authorization)
- Data errors (corruption, inconsistency)
- Configuration errors (misconfigurations, conflicts)

### Root Cause Techniques

- Five whys analysis for deep understanding
- Fishbone diagrams for systematic analysis
- Fault tree analysis for failure modes
- Event correlation across time and services
- Timeline reconstruction for incident sequence
- Hypothesis testing for cause validation
- Elimination process for narrowing causes
- Pattern synthesis for identifying commonalities

### Prevention Strategies

- Error prediction based on patterns
- Proactive monitoring before errors occur
- Circuit breaker implementation
- Graceful degradation patterns
- Error budget management
- Chaos engineering for resilience testing
- Load testing for capacity planning
- Failure injection for preparation

### Forensic Analysis

- Collects evidence from logs and metrics
- Constructs detailed timelines
- Identifies actors and triggers
- Reconstructs error sequences
- Measures actual impact
- Analyzes recovery effectiveness
- Extracts lessons learned
- Generates comprehensive reports

### Visualization Techniques

- Error heat maps for geographic or temporal visualization
- Dependency graphs for service relationships
- Time series charts for trends
- Correlation matrices for error relationships
- Flow diagrams for error propagation
- Impact radius visualization
- Trend analysis for forecasting
- Predictive model visualization

### Error Correlation Techniques

- Time-based correlation (temporal proximity)
- Service correlation (service dependencies)
- User correlation (shared user sessions)
- Geographic correlation (regional issues)
- Version correlation (deployment-related)
- Load correlation (traffic-related)
- Change correlation (configuration or code changes)
- External correlation (third-party dependencies)

### Predictive Analysis

- Trend detection for forecasting
- Pattern prediction for anticipation
- Anomaly forecasting for prevention
- Capacity prediction for planning
- Failure prediction for preparation
- Impact estimation for prioritization
- Risk scoring for triage
- Alert optimization for early warning

### Cascade Analysis

- Failure propagation tracking
- Service dependency mapping
- Circuit breaker gap identification
- Timeout chain analysis
- Retry storm detection
- Queue backup analysis
- Resource exhaustion identification
- Domino effect prevention

## Tool Restrictions

The error-detective skill uses standard file operations for configuration and script generation. It requires log aggregation tools (ELK, Splunk, Loki), monitoring platforms (Prometheus, Grafana, CloudWatch), and tracing systems (Jaeger, Zipkin, Honeycomb). Does not perform application code fixes—coordinate with appropriate development skills for remediation.

## Integration with Other Skills

- Collaborates with debugger for specific issue investigation
- Supports qa-expert for test scenario design
- Works with performance-engineer for performance error analysis
- Guides security-auditor for security pattern analysis
- Helps devops-incident-responder for incident investigation
- Assists sre-engineer for reliability improvements
- Partners with monitoring specialists for tool integration
- Coordinates with backend-developer for application errors

## Example Interactions

### Scenario 1: Cascading Failure Investigation

User: "We're seeing failures across multiple services"

Response:
1. Aggregate error logs from all affected services
2. Correlate errors temporally to identify propagation sequence
3. Trace root cause through distributed tracing
4. Map service dependencies and identify failure points
5. Analyze cascade mechanisms (timeouts, retries, queues)
6. Implement circuit breakers and monitoring improvements
7. Prevent recurrence with predictive alerts

### Scenario 2: Error Pattern Discovery

User: "Find patterns in our error logs"

Response:
1. Analyze 15,420 errors across system
2. Identify 23 distinct error patterns
3. Correlate patterns across services and time
4. Determine 7 root causes for patterns
5. Assess impact and severity for each pattern
6. Design monitoring and alerting for key patterns
7. Implement prevention strategies reducing errors by 67%

### Scenario 3: Anomaly Detection Setup

User: "Set up predictive error monitoring"

Response:
1. Establish performance baselines from historical data
2. Configure anomaly detection for error rates
3. Implement predictive modeling for error forecasting
4. Set up alerts with optimized thresholds
5. Reduce false positives through ML-based filtering
6. Create dashboards for visualization
7. Train team on anomaly interpretation and response

## Best Practices

- Always start with symptoms and follow error chains
- Correlate errors across time and services before conclusions
- Verify hypotheses with data and evidence
- Document findings thoroughly for knowledge sharing
- Implement monitoring improvements based on discovered patterns
- Use predictive alerts for proactive prevention
- Analyze cascades to prevent domino effects
- Build knowledge base of patterns and solutions

## Output Format

Delivers comprehensive error analysis reports, pattern libraries, root cause databases, monitoring improvements, predictive alerts, and knowledge management resources. Provides dashboards for visualization and actionable prevention strategies with measurable impact.

## Included Automation Scripts

The error-detective skill includes comprehensive automation scripts located in `scripts/`:

- **error_detection_automation.py**: Automates error detection and analysis by scanning logs for error patterns, correlating errors across services, detecting anomalies in error rates, and generating error reports and alerts

## References

### Reference Documentation (`references/` directory)
- **troubleshooting.md**: Troubleshooting guide for error detection patterns, distributed system debugging, and root cause analysis
- **best_practices.md**: Best practices for error correlation, anomaly detection, predictive error prevention, and knowledge management

## Examples

### Example 1: Distributed System Failure Analysis

**Scenario:** A microservices architecture experiences intermittent failures where some requests timeout while others succeed.

**Investigation Approach:**
1. **Error Collection**: Aggregated logs from all services during failure window
2. **Correlation Analysis**: Identified temporal patterns using timestamp alignment
3. **Dependency Mapping**: Traced request flow through all services
4. **Root Cause**: Database connection pool exhaustion in one service

**Resolution:**
- Increased connection pool size and added circuit breakers
- Implemented exponential backoff for retries
- Added connection pool monitoring alerts

### Example 2: Performance Regression Detection

**Scenario:** User-reported application slowness after a deployment, but automated tests pass.

**Detection Process:**
1. **Baseline Comparison**: Compared current performance against historical data
2. **Database Analysis**: Identified new query patterns causing table scans
3. **Code Review**: Found N+1 query pattern introduced in recent change
4. **Impact Assessment**: Quantified latency increase and affected endpoints

**Solution:**
- Optimized ORM queries with eager loading
- Added query performance tests to CI pipeline
- Implemented database query monitoring

### Example 3: Security Vulnerability Pattern Discovery

**Scenario:** Unusual patterns in authentication logs suggest potential brute force attacks.

**Analysis Steps:**
1. **Pattern Recognition**: Identified IP addresses with multiple failed attempts
2. **Rate Analysis**: Detected timing patterns indicating automated attacks
3. **Impact Assessment**: Mapped affected accounts and potential exposure
4. **Remediation**: Implemented rate limiting and CAPTCHA challenges

**Prevention Measures:**
- Added fail2ban-style automatic blocking
- Enhanced monitoring for authentication anomalies
- Implemented multi-factor authentication for sensitive operations

## Best Practices

### Investigation Methodology

- **Systematic Approach**: Follow consistent process from symptoms to root cause
- **Evidence-Based**: Base conclusions on data, not assumptions
- **Thorough Documentation**: Record all findings, even negative results
- **Cross-Reference**: Validate findings against multiple data sources
- **Collaborative Investigation**: Involve relevant teams for diverse perspectives

### Error Pattern Recognition

- **Baseline Establishment**: Define normal behavior for comparison
- **Anomaly Detection**: Use statistical methods to identify deviations
- **Trend Analysis**: Track error patterns over time
- **Correlation**: Connect errors across services and time periods
- **Prioritization**: Focus on high-impact, frequent error patterns

### Root Cause Analysis

- **5 Whys Technique**: Drill down to underlying causes
- **Fault Tree Analysis**: Map causal relationships systematically
- **Contributing Factors**: Identify systemic issues beyond immediate cause
- **Documentation**: Create actionable findings with evidence
- **Verification**: Confirm fix addresses root cause, not symptoms

### Prevention Strategy

- **Automated Monitoring**: Implement proactive error detection
- **Predictive Alerts**: Use ML for early warning systems
- **Testing Integration**: Add error scenarios to test suites
- **Knowledge Sharing**: Document patterns and solutions
- **Continuous Improvement**: Iterate on prevention based on learnings

## Anti-Patterns

### Investigation Anti-Patterns

- **Jumping to Conclusions**: Fixing symptoms without root cause analysis - resist pressure to act before understanding
- **Blame Game**: Focusing on who caused the error instead of why - use blameless postmortems
- **Over-Engineering Solutions**: Implementing complex fixes for simple problems - prefer simple, proven solutions
- **Scope Creep**: Expanding investigation beyond original symptoms - stay focused on the reported issue

### Error Pattern Anti-Patterns

- **Noise Acceptance**: Ignoring frequent low-severity errors - track all errors and their trends
- **Alert Fatigue**: Ignoring alerts that trigger too often - optimize thresholds and reduce false positives
- **Pattern Blindness**: Missing gradual degradation masked by normal variation - establish and monitor baselines
- **Siloed View**: Analyzing errors in isolation - correlate errors across services and time

### Root Cause Anti-Patterns

- **Single Point Failure Focus**: Stopping at first identified cause - continue asking "why" until systemic issues found
- **Human Error Labeling**: Blaming individuals without examining system design - human error is often system failure
- **Temporal Fallacy**: Assuming temporal proximity indicates causation - validate causal relationships
- **Confirmation Bias**: Seeking evidence for assumed causes - test alternative hypotheses

### Prevention Anti-Patterns

- **False Confidence**: Assuming fixed errors won't recur - implement monitoring and detection
- **Prevention Paralysis**: Over-investing in prevention at expense of detection - balance prevention and detection
- **One-Shot Learning**: Learning from incidents only once - build institutional knowledge and pattern recognition
- **Documentation Debt**: Failing to document error patterns and solutions - maintain searchable knowledge base

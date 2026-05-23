---
name: error-detector
description: Advanced error analysis and pattern detection specialist for identifying, analyzing, and preventing software errors
---

# Error Detector Skill

## Purpose

Provides error analysis and pattern detection expertise specializing in proactive identification of software defects, code analysis, and system behavior monitoring. Identifies, analyzes, and helps prevent software errors through static and dynamic analysis techniques.

## When to Use

- Performing static code analysis and anti-pattern detection
- Analyzing runtime errors and exception patterns
- Detecting memory leaks and performance bottlenecks
- Monitoring and analyzing error logs
- Identifying security vulnerabilities through code patterns
- Conducting proactive error prevention analysis

## Overview
Specialized in error analysis, pattern detection, and proactive identification of software defects through code analysis, log monitoring, and system behavior analysis.

## Error Detection Methodologies

### Static Analysis
- Code pattern recognition
- Anti-pattern identification
- Complexity analysis
- Security vulnerability detection
- Performance bottleneck identification

### Dynamic Analysis
- Runtime error monitoring
- Exception pattern analysis
- Memory leak detection
- Performance profiling
- Resource utilization tracking

### Log-Based Analysis
```bash
# Example patterns for error detection
grep -r "ERROR\|FATAL\|CRITICAL" logs/ --include="*.log" --include="*.txt"
grep -r "exception\|error\|failed" src/ --include="*.js" --include="*.py" --include="*.java"
grep -r "TODO\|FIXME\|HACK" src/ --include="*.*" --exclude-dir=node_modules
```

## Error Categories & Patterns

### Common Programming Errors
- Null pointer exceptions
- Array index out of bounds
- Type conversion errors
- Resource leak issues
- Concurrency problems

### Logic Errors
- Off-by-one errors
- Incorrect conditionals
- Loop termination issues
- State management problems
- Data validation failures

### Performance Errors
- Inefficient algorithms
- Memory optimization issues
- Database query problems
- Network timeout handling
- Resource contention

## Advanced Detection Techniques

### Machine Learning-Based Detection
- Anomaly detection in system behavior
- Pattern recognition in error logs
- Predictive failure modeling
- Classification of error types
- Automated root cause analysis

### Statistical Analysis
- Error frequency distribution
- Time series analysis of failures
- Correlation analysis between components
- Regression testing failure patterns
- Performance degradation detection

### Code Complexity Metrics
- Cyclomatic complexity analysis
- Cognitive complexity assessment
- Maintainability index calculation
- Technical debt quantification
- Code duplication detection

## Error Analysis Frameworks

### Root Cause Analysis (RCA)
- Five Whys methodology
- Fishbone diagram analysis
- Pareto analysis for prioritization
- Fault tree analysis
- Change impact assessment

### Error Classification Systems
- Severity categorization
- Priority assignment frameworks
- Impact assessment matrices
- Frequency-based prioritization
- Business risk evaluation

### Pattern Recognition
- Repetitive error identification
- Error clustering algorithms
- Sequence pattern analysis
- Correlation detection
- Temporal pattern analysis

## Monitoring & Alerting

### Real-Time Monitoring
- System health dashboards
- Error rate monitoring
- Performance threshold alerts
- Log aggregation and analysis
- Automated incident response

### Predictive Analysis
- Failure prediction models
- Early warning systems
- Trend analysis and forecasting
- Capacity planning alerts
- Proactive maintenance scheduling

### Logging Best Practices
- Structured logging implementation
- Log level optimization
- Sensitive data protection
- Log rotation policies
- Centralized log management

## Error Prevention Strategies

### Code Quality Improvement
- Peer review processes
- Automated testing coverage
- Static analysis tools integration
- Code style enforcement
- Documentation standards

### Development Process Optimization
- Test-driven development (TDD)
- Continuous integration practices
- Automated deployment pipelines
- Rollback procedures
- Feature flag implementation

### System Design Patterns
- Circuit breaker patterns
- Retry mechanisms
- Graceful degradation
- Fallback systems
- Redundancy implementation

## Error Detection Tools & Integration

### Static Analysis Tools
- ESLint for JavaScript/TypeScript
- Pylint for Python
- SonarQube for multi-language analysis
- Checkstyle for Java
- FxCop for C#

### Dynamic Monitoring Tools
- Application Performance Monitoring (APM)
- Error tracking services (Sentry, Bugsnag)
- Log management systems (ELK stack)
- Distributed tracing tools
- Infrastructure monitoring

### Custom Detection Scripts
- Error pattern matching
- Anomaly detection algorithms
- Automated regression testing
- Performance benchmarking
- Data validation checks

## Error Response & Resolution

### Incident Management
- Error triage procedures
- Escalation protocols
- Communication templates
- Resolution tracking
- Post-incident reviews

### Automated Recovery
- Self-healing mechanisms
- Automatic restart procedures
- Failover systems
- Data recovery processes
- Service restoration workflows

### Knowledge Management
- Error documentation databases
- Solution repositories
- Best practice libraries
- Training materials
- Lessons learned archives

## Specific Domain Expertise

### Web Application Errors
- HTTP error code analysis
- JavaScript runtime errors
- API failure patterns
- Database connection issues
- Frontend performance problems

### Mobile Application Errors
- Device-specific issues
- Network connectivity problems
- App store rejection patterns
- Battery usage optimization
- Memory management issues

### Backend System Errors
- Database transaction failures
- Message queue processing errors
- Authentication and authorization issues
- Microservices communication problems
- Resource exhaustion scenarios

## Reporting & Analytics

### Error Metrics
- Mean Time To Detection (MTTD)
- Mean Time To Resolution (MTTR)
- Error frequency trends
- Resolution effectiveness
- Preventive action impact

### Quality Dashboards
- Real-time error monitoring
- Historical trend analysis
- Team performance metrics
- System health indicators
- Compliance status tracking

## Deliverables

### Analysis Reports
- Comprehensive error analysis
- Root cause identification
- Impact assessment documentation
- Resolution recommendations
- Prevention strategies

### Implementation Plans
- Error detection system design
- Monitoring setup procedures
- Alerting configuration guides
- Automated testing frameworks
- Process improvement recommendations

### Training Materials
- Error handling best practices
- Troubleshooting guides
- Tool usage documentation
- Process workflow diagrams
- Knowledge base articles

## Examples

### Example 1: E-Commerce Platform Error Monitoring

**Scenario:** Implementing comprehensive error tracking for a high-traffic e-commerce site.

**Implementation:**
1. **Error Tracking**: Sentry integration across all services
2. **Log Aggregation**: ELK stack for centralized log management
3. **Alerting**: PagerDuty integration for critical errors
4. **Dashboard**: Custom Grafana dashboards for error metrics

**Results:**
- MTTD reduced from hours to minutes
- 40% reduction in time-to-resolution
- Proactive identification of emerging issues

### Example 2: Mobile App Crash Reporting

**Scenario:** Setting up crash reporting for iOS and Android applications.

**Approach:**
1. **Crash Reporting**: Firebase Crashlytics integration
2. **Symbolication**: Automated dSYM upload for readable stack traces
3. **Breadcrumbs**: User action tracking for context
4. **Release Tracking**: Correlation of crashes with app versions

**Key Metrics Tracked:**
- Crash-free users rate (target: 99.5%)
- Top crashers by device and OS version
- Session data with crash-free rate trends
- User feedback correlation with crashes

### Example 3: API Gateway Error Analysis

**Scenario:** Monitoring and analyzing errors at API gateway level for a SaaS platform.

**Monitoring Setup:**
1. **Request Logging**: All API requests logged with status codes
2. **Rate Tracking**: Monitoring for 429 Too Many Requests patterns
3. **Latency Analysis**: P95, P99 latency tracking by endpoint
4. **Authentication Errors**: Tracking failed auth attempts for security

**Alert Configuration:**
- Error rate spikes (> 5% for 5 minutes)
- Latency degradation (> 1s for P95)
- Authentication failures (> 100/min from single IP)
- Circuit breaker state changes

## Best Practices

### Error Detection Configuration

- **Comprehensive Coverage**: Instrument all code paths, not just critical functions
- **Context-Rich Data**: Include user IDs, request IDs, environment details
- **Sensitive Data Handling**: Scrub PII and secrets before error reporting
- **Sampling Strategy**: Balance detail collection with performance impact
- **Tagging**: Use consistent tagging for filtering and aggregation

### Alert Management

- **Threshold Tuning**: Adjust sensitivity to reduce alert fatigue
- **Escalation Paths**: Clear procedures for different severity levels
- **Business Hours**: Different expectations for on-call vs. business hours
- **Alert Fatigue Prevention**: Consolidate related alerts, avoid duplicates
- **On-Call Rotation**: Sustainable schedules with clear responsibilities

### Metrics and Reporting

- **Key Metrics**: Track MTTD, MTTR, error rate, resolution rate
- **Trend Analysis**: Weekly/monthly comparisons to identify patterns
- **SLA Reporting**: Error impact on service level agreements
- **Team Dashboards**: Custom views for different teams and roles
- **Executive Reporting**: High-level summaries for leadership

### Error Handling Best Practices

- **Defensive Programming**: Validate inputs, handle edge cases
- **Graceful Degradation**: Fallback mechanisms when dependencies fail
- **Error Recovery**: Automatic retry with exponential backoff
- **User Communication**: Meaningful error messages for end users
- **Logging**: Comprehensive logs for debugging and audit trails

### Continuous Improvement

- **Post-Incident Reviews**: Learn from every significant error
- **Pattern Analysis**: Identify recurring issues for systemic fixes
- **Knowledge Base**: Document errors and solutions for future reference
- **Tool Evolution**: Regularly evaluate and update detection tools
- **Team Training**: Ensure consistent error handling practices

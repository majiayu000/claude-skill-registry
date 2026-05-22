---
name: bug-analysis
description: Analyzes software bugs including root cause identification, severity assessment, impact analysis, reproduction steps validation, and fix recommendations. Performs bug triage, categorization, duplicate detection, and regression analysis. Use when investigating bugs, analyzing crash reports, triaging issues, debugging problems, reviewing error logs, or when users mention "analyze bug", "investigate issue", "debug problem", "bug report", "crash analysis", "root cause analysis", or "fix recommendation".
---

# Bug Analysis

## Overview

This skill provides systematic bug analysis to identify root causes, assess impact, classify severity, and generate actionable fix recommendations. It helps triage bugs efficiently and provides structured analysis for development teams.

## Core Analysis Workflow

## Step 1: Initial Triage & Information Gathering

**Collect Essential Information:**

- Bug description and symptoms
- Reproduction steps (verify they work)
- Expected vs actual behavior
- Environment details (OS, browser, version, config)
- Error messages, stack traces, logs
- Screenshots or videos
- User impact and frequency

**Quick Assessment:**

- Severity: Critical/High/Medium/Low
- Type: Functional/Performance/Security/UI/Data/Integration/Configuration/Regression
- Priority: Based on severity + business impact
- Potential duplicates: Search existing issues

### Step 2: Bug Categorization

**Severity Classification** (see [severity-guidelines.md](references/severity-guidelines.md) for detailed criteria):

**Critical (P0)** - Response: Immediate (<1 hour)

- System outage, data loss, security breach, no workaround

**High (P1)** - Response: Same day

- Major feature broken, significant user impact (>25%), difficult workaround

**Medium (P2)** - Response: Within 1 week

- Feature partially broken, moderate impact, workaround available

**Low (P3)** - Response: Backlog

- Minor issue, cosmetic problem, minimal impact

**Bug Type Categories:**

- **Functional**: Feature not working as specified
- **Performance**: Slow response, timeouts, resource issues
- **Security**: Vulnerabilities, unauthorized access
- **UI/UX**: Visual glitches, usability problems
- **Data**: Corruption, loss, incorrect processing
- **Integration**: API failures, third-party issues
- **Configuration**: Environment or deployment issues
- **Regression**: Previously working feature broken

### Step 3: Root Cause Analysis

**Investigation Process:**

1. **Review Error Evidence**
   - Parse stack traces to identify failure point
   - Map error codes to known issues
   - Check recent code changes (git blame, commit history)

2. **Reproduce the Issue**
   - Validate reproduction steps
   - Test in different environments
   - Vary inputs to identify boundaries
   - Document consistent reproduction method

3. **Trace Execution Flow**
   - Follow code path from entry to failure
   - Identify where actual diverges from expected
   - Check data transformations and control flow
   - Review relevant code sections

4. **Analyze Dependencies**
   - Verify library and framework versions
   - Check for known issues in dependencies
   - Review integration points
   - Test with different dependency versions

**Common Root Cause Patterns:**

- Logic errors (incorrect conditions, calculations)
- Null/undefined reference errors
- Race conditions and timing issues
- Memory leaks
- Boundary conditions (off-by-one, overflow)
- Configuration issues
- Dependency problems
- Integration failures

**For detailed analysis techniques**, see [analysis-techniques.md](references/analysis-techniques.md) for:

- Five Whys technique
- Stack trace analysis
- Differential analysis
- Data flow tracing
- Hypothesis testing
- Evidence collection methods

### Step 4: Impact Assessment

**Evaluate Impact Across Dimensions:**

**User Impact:**

- Number/percentage of affected users
- User workflows disrupted
- User segments affected

**Business Impact:**

- Revenue loss or risk
- SLA violations
- Customer satisfaction impact
- Reputation risk

**System Impact:**

- Performance degradation
- Resource consumption
- Cascading failures
- Data integrity risks

**Security Impact** (if applicable):

- Confidentiality: Data exposure level
- Integrity: Unauthorized modifications
- Availability: Service disruptions
- Exploit potential

**Scope Definition:**

- Affected versions/releases
- Affected platforms/browsers
- Affected features/workflows
- Regression scope

### Step 5: Fix Recommendation

**Generate Structured Fix Strategy:**

**1. Immediate Mitigation** (if not already done):

- Workarounds for users
- Configuration changes to reduce impact
- Feature flags to disable problematic code
- Rollback options if recent regression

**2. Permanent Solution:**

- Specific code changes needed
- Files to modify with line numbers
- Design changes required
- Database migrations or cleanup needed
- Configuration updates required

**3. Testing Requirements:**

- Unit tests to add
- Integration tests needed
- Regression tests to prevent recurrence
- Performance/security tests if applicable

**4. Prevention Measures:**

- Code review focus areas
- Additional validation needed
- Monitoring/alerting to add
- Documentation updates
- Process improvements

## Output Format

Provide structured analysis using these templates:

**Standard Bug Analysis**: Use template from [output-templates.md](references/output-templates.md) including:

- Bug summary with severity and priority
- Environment and reproduction steps
- Root cause analysis with evidence
- Impact assessment
- Recommended fix with testing plan

**Specialized Reports** (see [output-templates.md](references/output-templates.md)):

- **Security Vulnerability Report**: CVSS scoring, attack vectors, disclosure plan
- **Performance Bug Report**: Metrics, profiling results, optimization strategy
- **Crash Analysis Report**: Stack traces, memory state, crash triggers

## Special Analysis Scenarios

### Security Vulnerabilities

For security issues:

1. **Assess using CVSS**: Attack vector, complexity, privileges, impact
2. **Identify exploit potential**: Remote exploitation, authentication required
3. **Plan containment**: Immediate patches, access restrictions, monitoring
4. **Disclosure strategy**: Timeline, notifications, compliance (CVE, GDPR, PCI-DSS)

See [severity-guidelines.md](references/severity-guidelines.md) for security-specific triage.

### Performance Issues

For performance bugs:

1. **Establish baseline**: Expected metrics, SLA thresholds
2. **Identify bottlenecks**: CPU profiling, memory patterns, I/O, database queries
3. **Quantify degradation**: Response time increase, throughput reduction
4. **Optimization strategy**: Code optimization, caching, indexing, architecture changes

### Crash Analysis

For application crashes:

1. **Analyze crash dump**: Exception type, stack trace, thread states
2. **Identify trigger**: User action, system condition, data input, timing
3. **Assess stability impact**: Frequency, affected scenarios, data loss risk
4. **Recovery strategy**: Crash handling, graceful degradation, monitoring

## Investigation Tools & Commands

For detailed command references, see [investigation-commands.md](references/investigation-commands.md):

**Version Control:**

- `git bisect` - Find commit that introduced bug
- `git blame` - See who last modified code
- `git log -S "text"` - Find when code changed

**Log Analysis:**

- `grep -A 5 -B 5 "error" app.log` - Find errors with context
- `tail -f app.log | grep ERROR` - Monitor errors real-time
- Log parsing with awk and analysis scripts

**Database Investigation:**

- PostgreSQL: Slow query analysis, index usage
- MySQL: Process list, deadlock detection
- MongoDB: Operation profiling, collection stats

**System Monitoring:**

- Process monitoring: `top`, `ps`, `htop`
- Memory analysis: `free`, `pmap`, `valgrind`
- Network analysis: `netstat`, `tcpdump`, `curl -v`

**Application Debugging:**

- Node.js: `node --inspect`, profiling, heap snapshots
- Python: `pdb`, `cProfile`, memory profiling
- Java: `jmap`, `jstack`, flight recorder
- Docker/Kubernetes: Container logs, exec, debugging

## Best Practices

### Investigation Principles

- **Evidence-based**: Base conclusions on concrete data, not assumptions
- **Systematic**: Follow logical investigation process
- **Hypothesis-driven**: Form hypotheses, test them, verify results
- **Document everything**: Record findings, reasoning, and decisions
- **Consider multiple causes**: Don't fixate on first theory

### Effective Communication

- **Use clear language**: Avoid jargon with non-technical stakeholders
- **Provide context**: Explain why the bug matters
- **Set expectations**: Realistic timelines and complexity
- **Offer workarounds**: Help users immediately when possible
- **Follow up**: Update stakeholders on progress

### Prevention Focus

After fixing bugs:

- **Identify patterns**: Common causes across multiple bugs
- **Improve testing**: Add coverage for bug scenarios
- **Enhance monitoring**: Add alerts for similar issues
- **Update processes**: Code review checklists, deployment procedures
- **Document lessons**: Update knowledge base

## Quick Reference

### Common Root Causes Checklist

- [ ] Null/undefined reference
- [ ] Off-by-one error or boundary condition
- [ ] Race condition or timing issue
- [ ] Memory leak
- [ ] Missing validation or error handling
- [ ] Configuration issue
- [ ] Dependency version mismatch
- [ ] API contract change
- [ ] Database schema mismatch
- [ ] Incorrect permissions
- [ ] Resource exhaustion
- [ ] Caching issue
- [ ] Timezone/date handling
- [ ] Character encoding problem

### Quick Diagnosis Commands

```bash
# Service status
systemctl status service_name

# Resource usage
top -bn1 | head -20                    # CPU
ps aux --sort=-%mem | head -10         # Memory
du -sh /* | sort -rh | head -10        # Disk

# Recent changes
git log --since="1 day ago" --oneline

# Error analysis
tail -100 /var/log/app.log | grep -i error
grep ERROR /var/log/app.log | wc -l
```

## Integration with Development Workflow

**Bug Lifecycle:**

1. **New** → Report received
2. **Triage** → Analysis and prioritization (use this skill)
3. **Confirmed** → Reproduced, root cause identified
4. **Assigned** → Developer assigned
5. **In Progress** → Fix being implemented
6. **Code Review** → Fix under review
7. **Testing** → QA validation
8. **Fixed** → Deployed
9. **Closed** → Verified resolved

**Documentation Requirements:**

- Link to code: Files and line numbers
- Link to tests: Verify fix test cases
- Link to monitoring: Dashboards or alerts
- Link to related issues: Duplicates, related bugs
- Update documentation: If user-facing changes

## Reference Files

Load reference files based on analysis needs:

- **Severity Guidelines**: See [severity-guidelines.md](references/severity-guidelines.md) when:
  - Determining bug severity and priority
  - Understanding triage criteria
  - Need severity/priority matrix
  - Security vulnerability classification

- **Analysis Techniques**: See [analysis-techniques.md](references/analysis-techniques.md) when:
  - Need detailed RCA methodologies
  - Applying Five Whys or other techniques
  - Conducting hypothesis testing
  - Performing evidence collection
  - Using specific debugging strategies

- **Output Templates**: See [output-templates.md](references/output-templates.md) when:
  - Creating bug reports
  - Writing RCA documents
  - Documenting security vulnerabilities
  - Reporting performance issues
  - Analyzing crashes
  - Marking duplicates

- **Investigation Commands**: See [investigation-commands.md](references/investigation-commands.md) when:
  - Need specific command syntax
  - Working with version control (git)
  - Analyzing logs and databases
  - Monitoring system resources
  - Debugging applications
  - Using container tools (Docker, Kubernetes)

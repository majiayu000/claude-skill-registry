---
name: chaos-engineering
description: Test system resilience through controlled failures. Use when validating fault tolerance, disaster recovery, or system reliability. Covers chaos experiments.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Chaos Engineering

## Principles

1. **Build a Hypothesis**: Define expected behavior
2. **Minimize Blast Radius**: Start small
3. **Run in Production**: Real conditions matter
4. **Automate**: Make experiments repeatable
5. **Minimize Impact**: Have abort conditions

## Experiment Process

1. **Steady State**: Define normal metrics
2. **Hypothesis**: "System will maintain X under condition Y"
3. **Introduce Variables**: Inject failure
4. **Observe**: Compare to steady state
5. **Analyze**: Confirm or disprove hypothesis

## Common Experiments

### Network Failures
```bash
# Add latency
tc qdisc add dev eth0 root netem delay 100ms

# Packet loss
tc qdisc add dev eth0 root netem loss 10%

# Remove
tc qdisc del dev eth0 root
```

### Resource Exhaustion
```bash
# CPU stress
stress --cpu 4 --timeout 60s

# Memory stress
stress --vm 2 --vm-bytes 1G --timeout 60s

# Disk fill
dd if=/dev/zero of=/tmp/fill bs=1M count=1024
```

### Service Failures
- Kill processes
- Restart containers
- Terminate instances
- Block dependencies

## Chaos Tools

- **Chaos Monkey**: Random instance termination
- **Gremlin**: Comprehensive chaos platform
- **Litmus**: Kubernetes chaos engineering
- **Chaos Mesh**: Cloud-native chaos

## Experiment Template

```markdown
## Experiment: [Name]

### Hypothesis
If [condition], then [expected behavior].

### Steady State
- Metric A: [baseline value]
- Metric B: [baseline value]

### Method
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Abort Conditions
- If [condition], stop immediately

### Results
[What happened]

### Findings
[What we learned]
```

## Safety Rules

1. Start in non-production
2. Have rollback ready
3. Monitor continuously
4. Communicate with team
5. Document everything

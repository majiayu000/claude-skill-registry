---
name: gremlin-enterprise-chaos
description: Apply Gremlin's enterprise chaos engineering methodology. Emphasizes categorized failure injection, safety controls, and structured experimentation. Use when implementing chaos engineering in enterprise environments with compliance requirements.
---

# Gremlin Enterprise Chaos Engineering

## Overview

Gremlin, founded by Kolton Andrus (former Amazon/Netflix reliability engineer), productized chaos engineering for enterprise adoption. Their approach emphasizes safety, categorization, and measurable outcomes—making chaos engineering accessible to organizations that can't afford to "move fast and break things."

## The Pioneer

### Kolton Andrus

Built chaos engineering infrastructure at Amazon (Game Days) and Netflix before founding Gremlin. His insight: chaos engineering needs to be **safe, repeatable, and auditable** for enterprise adoption.

> "We basically inject a little harm in order to find weak spots and build an immunity. We proactively break things."

## References

- **Tutorials**: https://www.gremlin.com/community/tutorials/
- **Documentation**: https://www.gremlin.com/docs/
- **Talks**: QCon, Velocity, SRECon presentations

## Core Philosophy

> "Thoughtful, planned experiments that teach us something about the system."

> "The goal is not to break things—it's to build confidence."

Gremlin's approach differs from early chaos engineering by emphasizing **safety controls**, **categorized attacks**, and **enterprise readiness** (audit trails, RBAC, compliance).

## Attack Categories

Gremlin organizes chaos attacks into three categories:

### 1. Resource Attacks

```
┌─────────────────────────────────────────────────────────┐
│ Resource Attacks - Stress system resources              │
├─────────────────────────────────────────────────────────┤
│ CPU         │ Consume CPU cycles                        │
│ Memory      │ Allocate memory, cause pressure           │
│ Disk        │ Fill disk, stress I/O                     │
│ IO          │ Stress disk I/O subsystem                 │
└─────────────────────────────────────────────────────────┘
```

### 2. Network Attacks

```
┌─────────────────────────────────────────────────────────┐
│ Network Attacks - Disrupt network connectivity          │
├─────────────────────────────────────────────────────────┤
│ Latency     │ Add delay to network calls                │
│ Packet Loss │ Drop percentage of packets                │
│ Blackhole   │ Drop all traffic to targets               │
│ DNS         │ Fail DNS resolution                       │
└─────────────────────────────────────────────────────────┘
```

### 3. State Attacks

```
┌─────────────────────────────────────────────────────────┐
│ State Attacks - Modify system state                     │
├─────────────────────────────────────────────────────────┤
│ Shutdown    │ Terminate process/container               │
│ Time Travel │ Skew system clock                         │
│ Process Kill│ Kill specific processes                   │
└─────────────────────────────────────────────────────────┘
```

## When Implementing

### Always

- Start with read-only observation (no injection)
- Use built-in safety controls (halt conditions)
- Define rollback procedures before starting
- Communicate experiments to stakeholders
- Document findings and remediation
- Maintain audit trail for compliance

### Never

- Run chaos without abort mechanisms
- Skip stakeholder communication
- Experiment without monitoring
- Start with complex, multi-failure scenarios
- Ignore compliance requirements
- Chaos in production without staging validation

### Prefer

- Categorized attacks over ad-hoc failures
- Automated safety controls over manual monitoring
- Graduated complexity over big-bang tests
- Business hours for initial experiments
- Team-wide involvement over siloed testing

## Implementation Patterns

### Attack Definition Framework

```python
# attack_framework.py
# Gremlin-style categorized attack definitions

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Callable
from enum import Enum
from abc import ABC, abstractmethod

class AttackCategory(Enum):
    RESOURCE = "resource"
    NETWORK = "network"
    STATE = "state"

class AttackType(Enum):
    # Resource
    CPU = "cpu"
    MEMORY = "memory"
    DISK = "disk"
    IO = "io"
    # Network
    LATENCY = "latency"
    PACKET_LOSS = "packet_loss"
    BLACKHOLE = "blackhole"
    DNS = "dns"
    # State
    SHUTDOWN = "shutdown"
    TIME_TRAVEL = "time_travel"
    PROCESS_KILL = "process_kill"

@dataclass
class SafetyControls:
    """Built-in safety mechanisms"""
    max_duration_seconds: int = 300
    halt_on_error_rate: float = 0.05      # 5% error rate
    halt_on_latency_p99_ms: int = 5000    # 5 second p99
    excluded_hosts: List[str] = field(default_factory=list)
    require_healthy_baseline: bool = True
    business_hours_only: bool = True
    
    def check_halt_conditions(self, metrics: dict) -> bool:
        """Return True if experiment should halt"""
        if metrics.get('error_rate', 0) > self.halt_on_error_rate:
            return True
        if metrics.get('latency_p99_ms', 0) > self.halt_on_latency_p99_ms:
            return True
        return False

@dataclass
class Attack:
    """Base attack definition"""
    name: str
    category: AttackCategory
    attack_type: AttackType
    description: str
    
    # Targeting
    targets: List[str]                    # Host/container/service IDs
    target_percentage: float = 1.0        # Percentage of targets to affect
    
    # Timing
    duration_seconds: int = 60
    ramp_up_seconds: int = 0              # Gradual increase
    
    # Safety
    safety: SafetyControls = field(default_factory=SafetyControls)
    
    # Attack-specific parameters
    parameters: Dict = field(default_factory=dict)


class AttackExecutor(ABC):
    """Execute attacks safely"""
    
    @abstractmethod
    def execute(self, attack: Attack) -> dict:
        pass
    
    @abstractmethod
    def halt(self, attack_id: str) -> bool:
        pass


# Specific attack implementations
@dataclass
class CPUAttack(Attack):
    """Consume CPU resources"""
    category: AttackCategory = AttackCategory.RESOURCE
    attack_type: AttackType = AttackType.CPU
    
    def __post_init__(self):
        # CPU-specific defaults
        self.parameters.setdefault('cores', 1)
        self.parameters.setdefault('percentage', 100)


@dataclass 
class LatencyAttack(Attack):
    """Add network latency"""
    category: AttackCategory = AttackCategory.NETWORK
    attack_type: AttackType = AttackType.LATENCY
    
    def __post_init__(self):
        # Latency-specific defaults
        self.parameters.setdefault('latency_ms', 100)
        self.parameters.setdefault('jitter_ms', 0)
        self.parameters.setdefault('target_hosts', [])
        self.parameters.setdefault('target_ports', [])


@dataclass
class ShutdownAttack(Attack):
    """Terminate process or container"""
    category: AttackCategory = AttackCategory.STATE
    attack_type: AttackType = AttackType.SHUTDOWN
    
    def __post_init__(self):
        # Shutdown-specific defaults
        self.parameters.setdefault('delay_seconds', 0)
        self.parameters.setdefault('reboot', False)
```

### Safety-First Execution

```python
# safe_executor.py
# Execute chaos attacks with safety controls

import time
import threading
from typing import Optional
from datetime import datetime, timedelta

class SafeChaosExecutor:
    """
    Gremlin's key insight: chaos must be SAFE for enterprise adoption.
    Built-in halt conditions, audit trails, and rollback.
    """
    
    def __init__(self, metrics_client, notification_client):
        self.metrics = metrics_client
        self.notify = notification_client
        self.active_attacks = {}
        self.audit_log = []
    
    def execute(self, attack: Attack) -> dict:
        """Execute attack with safety controls"""
        attack_id = self._generate_id()
        
        # Pre-flight checks
        preflight = self._preflight_checks(attack)
        if not preflight['passed']:
            self._audit("BLOCKED", attack, preflight['reason'])
            return {'status': 'blocked', 'reason': preflight['reason']}
        
        # Notify stakeholders
        self.notify.send(
            f"🔬 Starting chaos experiment: {attack.name}",
            f"Duration: {attack.duration_seconds}s, "
            f"Targets: {len(attack.targets)}"
        )
        
        # Start attack in background with monitoring
        self.active_attacks[attack_id] = {
            'attack': attack,
            'started_at': datetime.now(),
            'status': 'running'
        }
        
        monitor_thread = threading.Thread(
            target=self._monitored_execution,
            args=(attack_id, attack)
        )
        monitor_thread.start()
        
        self._audit("STARTED", attack)
        
        return {
            'status': 'started',
            'attack_id': attack_id,
            'halt_url': f'/attacks/{attack_id}/halt'
        }
    
    def _preflight_checks(self, attack: Attack) -> dict:
        """Verify it's safe to proceed"""
        
        # Check business hours
        if attack.safety.business_hours_only:
            hour = datetime.now().hour
            if not (9 <= hour < 17):
                return {'passed': False, 'reason': 'Outside business hours'}
        
        # Check baseline health
        if attack.safety.require_healthy_baseline:
            current_metrics = self.metrics.get_current()
            if current_metrics.get('error_rate', 0) > 0.01:
                return {'passed': False, 'reason': 'Baseline unhealthy'}
        
        # Check excluded hosts
        for target in attack.targets:
            if target in attack.safety.excluded_hosts:
                return {'passed': False, 'reason': f'Target {target} is excluded'}
        
        return {'passed': True}
    
    def _monitored_execution(self, attack_id: str, attack: Attack):
        """Execute with continuous safety monitoring"""
        start_time = time.time()
        
        try:
            # Actually inject the failure
            self._inject_failure(attack)
            
            # Monitor until duration elapsed or halt triggered
            while time.time() - start_time < attack.duration_seconds:
                # Check halt conditions
                current = self.metrics.get_current()
                if attack.safety.check_halt_conditions(current):
                    self._emergency_halt(attack_id, "Safety threshold exceeded")
                    return
                
                # Check manual halt
                if self.active_attacks[attack_id]['status'] == 'halting':
                    self._emergency_halt(attack_id, "Manual halt requested")
                    return
                
                time.sleep(1)
            
            # Normal completion
            self._complete_attack(attack_id)
            
        except Exception as e:
            self._emergency_halt(attack_id, f"Error: {str(e)}")
    
    def _emergency_halt(self, attack_id: str, reason: str):
        """Immediately stop attack and rollback"""
        attack = self.active_attacks[attack_id]['attack']
        
        # Rollback the failure injection
        self._rollback_failure(attack)
        
        # Update status
        self.active_attacks[attack_id]['status'] = 'halted'
        self.active_attacks[attack_id]['halt_reason'] = reason
        
        # Notify
        self.notify.send(
            f"🛑 Chaos experiment HALTED: {attack.name}",
            f"Reason: {reason}"
        )
        
        self._audit("HALTED", attack, reason)
    
    def halt(self, attack_id: str) -> bool:
        """Manual halt trigger"""
        if attack_id in self.active_attacks:
            self.active_attacks[attack_id]['status'] = 'halting'
            return True
        return False
    
    def _audit(self, action: str, attack: Attack, details: str = ""):
        """Maintain audit trail for compliance"""
        self.audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'attack_name': attack.name,
            'attack_type': attack.attack_type.value,
            'targets': attack.targets,
            'details': details,
            'user': self._get_current_user()
        })
```

### Graduated Complexity

```python
# graduation.py
# Progress through attack complexity safely

from dataclasses import dataclass
from typing import List
from enum import Enum

class MaturityLevel(Enum):
    """Chaos engineering maturity levels"""
    LEVEL_1 = "Exploring"      # Simple attacks, single service
    LEVEL_2 = "Practicing"     # Multiple attack types, automation
    LEVEL_3 = "Operating"      # Cross-service, game days
    LEVEL_4 = "Optimizing"     # Continuous, production chaos

@dataclass
class ChaosMaturityAssessment:
    """Assess and guide chaos engineering maturity"""
    
    level: MaturityLevel
    
    def recommended_attacks(self) -> List[str]:
        """What attacks are appropriate for this level"""
        if self.level == MaturityLevel.LEVEL_1:
            return [
                "CPU stress (single host)",
                "Memory pressure (single host)",
                "Network latency (internal)",
                "Process restart"
            ]
        elif self.level == MaturityLevel.LEVEL_2:
            return [
                "Multi-host resource attacks",
                "Network partition (AZ simulation)",
                "Dependency latency injection",
                "Automated scheduled chaos"
            ]
        elif self.level == MaturityLevel.LEVEL_3:
            return [
                "Cross-service failure scenarios",
                "Game days with multiple teams",
                "Region failover testing",
                "Data plane chaos"
            ]
        elif self.level == MaturityLevel.LEVEL_4:
            return [
                "Continuous production chaos",
                "Chaos as code in CI/CD",
                "Automated hypothesis validation",
                "Chaos-driven architecture decisions"
            ]
    
    def prerequisites_for_next_level(self) -> List[str]:
        """What's needed to advance"""
        if self.level == MaturityLevel.LEVEL_1:
            return [
                "Basic monitoring in place",
                "On-call rotation established",
                "Runbooks for common failures",
                "5+ successful experiments completed"
            ]
        elif self.level == MaturityLevel.LEVEL_2:
            return [
                "Automated experiment execution",
                "Cross-team communication plan",
                "Defined steady-state metrics",
                "Incident response tested via chaos"
            ]
        elif self.level == MaturityLevel.LEVEL_3:
            return [
                "Chaos experiments in CI/CD pipeline",
                "Production chaos (limited blast radius)",
                "Chaos-informed architecture decisions",
                "Executive sponsorship"
            ]
        else:
            return ["You've achieved chaos mastery! 🎉"]


class GraduatedChaosProgram:
    """Guide organizations through chaos maturity"""
    
    def __init__(self):
        self.experiments_completed = []
        self.current_level = MaturityLevel.LEVEL_1
    
    def suggest_next_experiment(self) -> dict:
        """Recommend next experiment based on maturity"""
        assessment = ChaosMaturityAssessment(self.current_level)
        attacks = assessment.recommended_attacks()
        
        # Find attacks not yet completed
        completed_types = {e['type'] for e in self.experiments_completed}
        available = [a for a in attacks if a not in completed_types]
        
        if not available:
            return {
                'recommendation': 'Consider advancing to next level',
                'prerequisites': assessment.prerequisites_for_next_level()
            }
        
        return {
            'recommendation': available[0],
            'rationale': f"Appropriate for {self.current_level.value} maturity",
            'safety_notes': self._safety_notes_for_level()
        }
    
    def _safety_notes_for_level(self) -> List[str]:
        if self.current_level == MaturityLevel.LEVEL_1:
            return [
                "Start in non-production environment",
                "Single host only",
                "Business hours with team present",
                "Manual halt button ready"
            ]
        elif self.current_level == MaturityLevel.LEVEL_2:
            return [
                "Staging environment recommended",
                "Notify dependent teams",
                "Automated halt conditions required"
            ]
        else:
            return [
                "Production-ready with safeguards",
                "Stakeholder communication plan",
                "Rollback procedures documented"
            ]
```

### Game Day Framework

```python
# game_day.py
# Structured chaos game day execution

from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime, timedelta

@dataclass
class GameDayScenario:
    """A specific failure scenario to test"""
    name: str
    description: str
    attacks: List['Attack']
    expected_behavior: str
    success_criteria: List[str]
    rollback_procedure: str

@dataclass
class GameDay:
    """
    Structured chaos game day - Gremlin/Amazon style.
    Planned, communicated, and educational.
    """
    name: str
    date: datetime
    duration_hours: int
    scenarios: List[GameDayScenario]
    
    # Participants
    facilitator: str
    observers: List[str]
    responders: List[str]  # Teams expected to respond
    
    # Communication
    slack_channel: str
    video_call_link: str
    
    def generate_runbook(self) -> str:
        """Generate game day runbook"""
        runbook = f"""
# Game Day: {self.name}
Date: {self.date.strftime('%Y-%m-%d %H:%M')}
Duration: {self.duration_hours} hours

## Facilitator
{self.facilitator}

## Communication
- Slack: {self.slack_channel}
- Video: {self.video_call_link}

## Participants
**Observers**: {', '.join(self.observers)}
**Responders**: {', '.join(self.responders)}

## Timeline

### Pre-Game (30 min before)
- [ ] Verify monitoring dashboards are accessible
- [ ] Confirm all participants have joined
- [ ] Review halt procedures
- [ ] Capture baseline metrics

### Scenarios

"""
        for i, scenario in enumerate(self.scenarios, 1):
            runbook += f"""
#### Scenario {i}: {scenario.name}
**Description**: {scenario.description}

**Expected Behavior**: {scenario.expected_behavior}

**Success Criteria**:
{chr(10).join(f'- [ ] {c}' for c in scenario.success_criteria)}

**Rollback**: {scenario.rollback_procedure}

---
"""
        
        runbook += """
### Post-Game
- [ ] Restore all systems to normal
- [ ] Capture final metrics
- [ ] Conduct immediate debrief
- [ ] Schedule follow-up to review findings

## Emergency Halt
If anything goes wrong: **ANNOUNCE IN SLACK AND EXECUTE ROLLBACK**
"""
        return runbook
```

## Mental Model

Gremlin/Enterprise chaos engineering asks:

1. **Is this safe?** Built-in safeguards, halt conditions, audit trail
2. **What category of failure?** Resource, network, or state
3. **What's our maturity level?** Match experiments to capability
4. **Who needs to know?** Communication is not optional
5. **What did we learn?** Document and share findings

## Signature Gremlin Moves

- Categorized attack library (resource, network, state)
- Built-in safety controls and halt conditions
- Graduated maturity model
- Game day framework
- Enterprise features (RBAC, audit, compliance)
- Failure as a Service

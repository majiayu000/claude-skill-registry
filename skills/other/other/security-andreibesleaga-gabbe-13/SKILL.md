---
name: reliability-engineering
description: Designing failover patterns (Hot Standby, TMR), redundancy, and MTTF calculations.
role: prod-safety-engineer, eng-arch
triggers:
  - reliability
  - failover
  - redundancy
  - tmr
  - mttf
  - mtbf
---

# reliability-engineering Skill

This skill designs systems that continue to function in the presence of faults.

## 1. Redundancy Patterns
- **Active/Passive (Hot Standby)**: Primary handles load, Secondary takes over on heartbeat loss.
- **Active/Active (Load Balancing)**: Both handle load. System survives if N-1 nodes active.
- **TMR (Triple Modular Redundancy)**: 3 voters. 2/3 majority wins. Used in avionics/space.

## 2. Design for Reliability
- **Watchdog Timers**: Hardware/Software timer that resets the system if it hangs.
- **Safety Bag / Monitor**: Independent channel that monitors outputs and cuts power if limits exceeded.
- **N-Version Programming**: 3 teams write the same software in 3 languages (Python, Rust, Ada) to avoid common bugs.

## 3. Calculations
- **MTBF (Mean Time Between Failures)**: Total Time / Number of Failures.
- **Availability**: MTBF / (MTBF + MTTR). Goal: 99.999% ("Five Nines" = 5 mins downtime/year).
- **Failure Rate ($\lambda$)**: 1 / MTBF.

## 4. Stability Patterns
- **Circuit Breaker**: Stop calling a failing service to prevent cascading failure.
- **Bulkhead**: Isolate components so a crash in one doesn't sink the ship.
- **Backpressure**: Reject new work when overloaded.

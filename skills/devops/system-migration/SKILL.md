---
name: system-migration
description: Guides operating system and hardware platform migrations including Linux distribution changes, Windows to Linux migration, mainframe to x86 modernization, data center migrations (physical to virtual, P2V, V2V), hardware platform changes, system consolidation, and legacy system decommissioning. Covers OS compatibility, driver migration, system configuration transfer, and cutover procedures. Use when migrating operating systems, changing hardware platforms, moving from mainframes, or when users mention "OS migration", "Linux migration", "mainframe modernization", "P2V migration", "system upgrade", "data center migration", or "legacy system replacement".
---

# System Migration

## Overview

Provides comprehensive guidance for system-level migrations including operating system changes, hardware platform transitions, mainframe modernization, virtualization, and data center migrations. Focuses on system infrastructure that underlies applications and platforms.

**Key Points:**

- System migrations often involve multiple skills: OS + database + application coordination
- Plan for 30-50% more time than initial estimates
- Parallel run periods reduce risk but increase cost
- Mainframe migrations are typically multi-year projects
- Physical to virtual conversions rarely have issues with modern hardware
- Always validate hardware compatibility before OS migrations

## Workflow Decision Tree

Choose your migration path based on the system type:

## 1. Operating System Migration

**Use for:** Linux distribution changes, Windows to Linux, OS version upgrades
**Load:** [migration-types.md](references/migration-types.md) for detailed workflows

### 2. Hardware Platform Migration

**Use for:** Mainframe to x86, architecture changes, system consolidation
**Load:** [migration-types.md](references/migration-types.md) for platform-specific guidance

### 3. Virtualization Migration

**Use for:** Physical to Virtual (P2V), Virtual to Virtual (V2V), cloud migrations
**Load:** [migration-types.md](references/migration-types.md) for virtualization patterns

### 4. Data Center Migration

**Use for:** Facility moves, infrastructure consolidation, hybrid cloud
**Load:** [migration-types.md](references/migration-types.md) for data center procedures

## Standard Migration Workflow

### Phase 1: Assessment & Planning

1. Document current system state (OS version, kernel, packages, services, configurations)
2. Identify application and hardware compatibility requirements
3. Determine migration strategy (in-place upgrade vs fresh install)
4. Create detailed migration plan with timeline and resources

### Phase 2: Preparation

1. Complete full system backups (OS, configurations, data)
2. Set up target system environment
3. Test migration procedures in non-production
4. Prepare rollback plan and validation criteria

### Phase 3: Execution

1. Perform migration following tested procedure
2. Migrate configurations and customize for target system
3. Install and configure applications
4. Validate system functionality

### Phase 4: Validation & Cutover

1. Run validation tests (See [validation-and-testing.md](references/validation-and-testing.md))
2. Conduct parallel run period if applicable
3. Execute cutover to production
4. Monitor closely post-migration

## Core Best Practices

✅ **Thorough Testing** - Test everything in non-production environments first
✅ **Complete Backups** - Multiple backups at different stages before migration
✅ **Automation** - Script repeatable tasks to reduce errors and ensure consistency
✅ **Gradual Migration** - Migrate in phases, not all at once
✅ **Rollback Plan** - Always have a tested way to revert changes
✅ **Documentation** - Document every configuration, decision, issue, and resolution

## Reference Files

Load these reference files based on specific migration needs:

- **Migration Types**: See [migration-types.md](references/migration-types.md) when:
  - Planning OS migrations (Linux distro changes, Windows to Linux)
  - Executing hardware platform migrations (mainframe to x86)
  - Performing virtualization migrations (P2V, V2V)
  - Conducting data center migrations

- **System Configuration Migration**: See [system-configuration-migration.md](references/system-configuration-migration.md) when:
  - Migrating network configurations
  - Transferring user accounts and permissions
  - Moving system services and cron jobs
  - Replicating firewall and security settings

- **Validation and Testing**: See [validation-and-testing.md](references/validation-and-testing.md) when:
  - Designing test plans for migrations
  - Validating system functionality post-migration
  - Conducting performance benchmarking
  - Testing disaster recovery procedures

- **Rollback Procedures**: See [rollback-procedures.md](references/rollback-procedures.md) when:
  - Planning rollback strategies
  - Migration fails or encounters critical issues
  - Need to revert to original system state

- **Tools and Resources**: See [tools-and-resources.md](references/tools-and-resources.md) when:
  - Selecting migration tools (rsync, dd, clonezilla, etc.)
  - Choosing automation frameworks
  - Need monitoring and validation utilities

- **Best Practices**: See [best-practices.md](references/best-practices.md) when:
  - Need comprehensive checklist for migration execution
  - Planning communication and stakeholder management
  - Establishing monitoring and alerting strategies

- **Anti-Patterns**: See [anti-patterns.md](references/anti-patterns.md) when:
  - Need to avoid common migration mistakes
  - Reviewing migration plans for potential issues
  - Troubleshooting failed or problematic migrations

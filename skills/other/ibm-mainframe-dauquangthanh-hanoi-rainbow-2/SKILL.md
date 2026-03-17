---
name: ibm-mainframe
description: Provides comprehensive IBM Mainframe administration, development, and modernization guidance including z/OS operations, JCL scripting, COBOL/PL/I programming, CICS/IMS configuration, DB2 administration, TSO/ISPF usage, system programming, batch processing, and mainframe-to-cloud migration strategies. Covers mainframe security (RACF, ACF2), performance tuning, capacity planning, disaster recovery, and DevOps integration. Use when working with mainframe systems, z/OS, JES2/JES3, VTAM, USS, or when users mention "mainframe", "z/OS", "MVS", "TSO", "ISPF", "JCL", "CICS", "IMS", "DB2 mainframe", "VSAM", "RACF", "mainframe modernization", "legacy mainframe", or "IBM z Systems".
---

# IBM Mainframe

## Overview

Comprehensive guidance for IBM Mainframe (z/OS) administration, development, operations, and modernization. Covers system programming, application development, middleware configuration, database management, and migration strategies for mainframe environments.

## Quick Start Guide

Choose your task and load the appropriate reference:

1. **z/OS System Administration** → Load [zos-administration.md](references/zos-administration.md) for system operations, address spaces, JES2/JES3, TSO/ISPF commands, dataset management, and USS
2. **JCL Development & Batch Processing** → Load [jcl-batch-processing.md](references/jcl-batch-processing.md) for JCL syntax, utilities (IEBGENER, SORT, IDCAMS), procedures, GDG management, and job scheduling
3. **COBOL Programming** → Load [cobol-programming.md](references/cobol-programming.md) for COBOL structure, file handling, DB2/CICS integration, compile/link procedures, and debugging
4. **Mainframe Modernization** → Load [mainframe-modernization.md](references/mainframe-modernization.md) for migration strategies, assessment, rehost/replatform/refactor approaches, and cloud integration

## Core Mainframe Concepts

## z/OS Operating System

- **MVS (Multiple Virtual Storage)**: Core OS components
- **JES2/JES3**: Job Entry Subsystems for batch processing
- **TSO/ISPF**: Time Sharing Option / Interactive System Productivity Facility
- **USS**: Unix System Services (POSIX environment on z/OS)
- **Address Spaces**: Isolated execution environments (ASID)

### Key Subsystems

- **CICS**: Customer Information Control System (transaction processing)
- **IMS**: Information Management System (hierarchical DB + transaction manager)
- **DB2**: Relational database management system
- **MQ**: Message queuing middleware
- **WebSphere**: Application server for Java applications

### Data Management

- **VSAM**: Virtual Storage Access Method (indexed, sequential, relative record)
- **Sequential Files**: PS (Physical Sequential), PDS (Partitioned Data Set), PDSE
- **GDG**: Generation Data Group (versioned datasets)
- **SMS**: Storage Management Subsystem (automated data management)

### Security Systems

- **RACF**: Resource Access Control Facility (IBM)
- **ACF2**: Access Control Facility 2 (CA Technologies)
- **Top Secret**: Security system (CA Technologies)

## Common Mainframe Tasks

For detailed syntax, examples, and procedures, load the appropriate reference file:

### Administration & Operations

- **JCL job submission & monitoring**: Load [jcl-batch-processing.md](references/jcl-batch-processing.md)
- **Dataset management**: Load [zos-administration.md](references/zos-administration.md)
- **VSAM file operations**: Load [jcl-batch-processing.md](references/jcl-batch-processing.md)

### Application Development

- **COBOL programming**: Load [cobol-programming.md](references/cobol-programming.md)
- **CICS transaction management**: Load [cobol-programming.md](references/cobol-programming.md)
- **DB2 operations**: Load [cobol-programming.md](references/cobol-programming.md)

### System Management

- **Security (RACF/ACF2)**: Load [zos-administration.md](references/zos-administration.md)
- **Performance monitoring**: Load [zos-administration.md](references/zos-administration.md)

## Mainframe Development Workflow

For complete development procedures, compile JCL, version control integration, and testing strategies, load [cobol-programming.md](references/cobol-programming.md).

**Typical development cycle:**

1. Edit source code (ISPF or modern IDE)
2. Compile and link programs
3. Test in development environment
4. Version control and promotion
5. Deploy to production

**Modern development approaches:**

- Git integration via USS (Unix System Services)
- Zowe CLI for remote access and CI/CD
- DBB (Dependency Based Build) for automated builds
- Eclipse/VS Code with mainframe extensions

## Mainframe Modernization Strategies

For comprehensive migration guidance, assessment procedures, and specific migration patterns, load [mainframe-modernization.md](references/mainframe-modernization.md).

**Key approaches:**

1. **Rehost (Lift & Shift)**: Mainframe emulators on x86/cloud (fastest, minimal changes)
2. **Replatform**: Migrate to modern languages (Java, C#) with automated conversion
3. **Refactor**: Redesign as microservices with modern architecture patterns
4. **Retire/Replace**: Replace with COTS or modern SaaS alternatives

**Integration options:**

- z/OS Connect for RESTful APIs
- IBM MQ for messaging
- CDC (Change Data Capture) for data replication
- DevOps integration with Zowe, Jenkins, Git

## Best Practices

### Development

1. Use structured programming (avoid ALTER, computed GO TO)
2. Modular design with focused paragraphs/sections
3. Comprehensive error handling (EXEC CICS HANDLE, SQL SQLCODE checks)
4. Clear documentation with meaningful variable names
5. Performance optimization (minimize I/O, efficient SQL, proper indexing)

### Operations

1. Automation with JCL procedures, REXX scripts, automation tools
2. Proactive monitoring with alerts and performance baselines
3. Regular backup & recovery with DR testing
4. Capacity planning to monitor trends and forecast growth
5. Security with least privilege, regular audits, compliance

### Migration

1. Phased approach to reduce risk incrementally
2. Data integrity validation before and after migration
3. Parallel running of old and new systems
4. Maintain rollback plans
5. Extensive documentation and team training

**For detailed procedures, load the appropriate reference file.**

## Tooling Ecosystem

### IBM Native Tools

- **ISPF**: Primary development interface
- **SDSF**: Job and output management
- **RMF/SMF**: Performance monitoring and system logging
- **OMVS**: Unix shell environment on z/OS

### Modern Mainframe Tools

- **Zowe**: Open-source framework for mainframe modernization
- **DBB**: Dependency Based Build for DevOps
- **IBM Wazi**: Cloud-native development environment
- **Topaz/IBM Developer for z/OS**: Modern IDEs

### Migration Tools

- **Micro Focus Enterprise Suite**: Rehost solution
- **LzLabs/AWS Mainframe Modernization**: Cloud migration platforms
- **IBM Rational/CAST**: Application analysis tools

**For detailed tool usage, configuration, and examples, load the appropriate reference file.**

## Common Issues & Solutions

### Job Failures

- **S0C7 (Data exception)**: Invalid numeric data, uninitialized variables, data conversion errors
- **S806 (Program not found)**: Missing STEPLIB/JOBLIB, linking issues, wrong load library
- **S322 (Time out)**: Infinite loop, long-running query, insufficient TIME parameter
- **S013/S213/S413 (OPEN failure)**: Dataset allocation issues, DISP conflicts, missing dataset

### Performance Issues

- **High CPU**: Inefficient code, missing indexes, excessive I/O
- **Long response time**: Network latency, database contention, poor SQL
- **Memory constraints**: Virtual storage shortage, insufficient region size

### Security Issues

- **Access denied**: Check RACF permissions and group memberships
- **Unauthorized program**: Not in APF library or not properly authorized
- **Dataset protection**: Review UACC and specific permits

**For detailed troubleshooting procedures, load the appropriate reference file.**

## Key Concepts Glossary

- **DASD**: Direct Access Storage Device (disk storage)
- **ABEND**: Abnormal End (program crash)
- **IPL**: Initial Program Load (system boot)
- **LPAR**: Logical Partition (virtual machine)
- **SYSPLEX**: System Complex (cluster of z/OS systems)
- **Coupling Facility**: High-speed memory for parallel sysplex
- **HCD/HCM**: Hardware Configuration Dialog/Manager
- **SMP/E**: System Modification Program/Extended (maintenance)
- **ISPF**: Interactive System Productivity Facility
- **REXX**: Restructured Extended Executor (scripting language)

## Critical Considerations

### Data Integrity

- VSAM files require proper SHAREOPTIONS
- DB2 locking and isolation levels must be configured correctly
- GDG generation management for versioned datasets
- Always backup before changes

### System Performance

- Batch window constraints (limited time for batch jobs)
- Online transaction response time requirements (sub-second)
- Resource contention management (CPU, I/O, memory)
- Capacity planning for growth

### Security & Compliance

- RACF/ACF2 configuration and maintenance
- Audit trails and compliance requirements (SOX, PCI-DSS, GDPR)
- Separation of duties enforcement

### High Availability

- Parallel Sysplex for redundancy
- GDPS (Geographically Dispersed Parallel Sysplex) for disaster recovery
- Continuous availability requirements

## Output Requirements

When analyzing or documenting mainframe systems, provide:

1. **System inventory**: Operating system version, middleware, applications
2. **Architecture diagram**: LPAR layout, subsystems, connectivity
3. **Dependency mapping**: Job dependencies, program CALL trees, data flows
4. **Security assessment**: User access, dataset protection, compliance gaps
5. **Performance baseline**: CPU, I/O, response times, throughput
6. **Modernization roadmap**: Assessment results, approach, timeline, risks (load [mainframe-modernization.md](references/mainframe-modernization.md))
7. **Migration plan**: Phased approach, cutover strategy, rollback procedures
8. **Documentation**: Technical specifications, runbooks, operational procedures

**For specific output formats and templates, load the appropriate reference file.**

## Next Steps

For specific tasks, load the relevant reference file from the Quick Start Guide above. Each reference provides detailed procedures, commands, examples, and troubleshooting guidance for that specific area of mainframe operations.

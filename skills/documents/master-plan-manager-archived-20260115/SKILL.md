---
name: master-plan-manager
description: SAFE MASTER-PLAN MAINTENANCE - Intelligent master-plan file management with comprehensive analysis, backup, and validation. Reads entire file, detects changes, updates only when needed, maintains document integrity. Optimized for personal productivity app master-plans.
---

# Master Plan Manager - Intelligent Document Maintenance

**Version:** 1.0.0
**Category:** Document Management / File Operations
**Related Skills:** chief-architect, comprehensive-system-analyzer, qa-testing

## Overview

A specialized skill for safe and intelligent master-plan file management. This skill reads entire master-plan documents, analyzes current content vs. needed updates, and applies changes only when meaningful improvements are detected. Implements comprehensive safety measures including backups, validation, and rollback capabilities.

## Quick Context
- **Complexity**: Medium-High (File operations with safety validation)
- **Duration**: Variable (Based on update complexity)
- **Dependencies**: File system access, markdown parsing
- **Safety**: Comprehensive backup and validation procedures

## Activation Triggers
- **Keywords**: master-plan, plan update, documentation, file analysis, document maintenance
- **Files**: `/docs/master-plan/README.md` and related planning documents
- **Contexts**: Chief-architect delegation, post-implementation updates, architectural decision documentation

## 🚨 CRITICAL SAFETY PROTOCOLS

### **MANDATORY File Safety Standards**
**DOCUMENT INTEGRITY FIRST**: Never make changes without comprehensive analysis, backup creation, and validation procedures.

#### **Before Any File Operations - MANDATORY Steps:**
1. **Complete File Analysis**: Read entire current document before any changes
2. **Backup Creation**: Create timestamped backup before any modifications
3. **Change Detection**: Analyze if updates are actually needed
4. **Content Validation**: Verify markdown structure and integrity
5. **Safety Check**: Confirm changes won't damage existing content
6. **Rollback Preparation**: Ensure quick restoration capability
7. **Integrity Verification**: Validate document after changes

#### **CRITICAL: No Blind Updates Protocol**
- **MANDATORY**: Never make changes without reading complete current file
- **MANDATORY**: Always check if content already exists before adding
- **MANDATORY**: Validate updates are meaningful improvements
- **BACKUP LOCATION**: All backups stored with timestamps in `/docs/master-plan/backups/`

## Core Capabilities

### 1. Intelligent Document Analysis
- **Complete File Reading**: Parse entire master-plan before any operations
- **Content Structure Analysis**: Understand existing sections and format
- **Change Detection**: Identify outdated, missing, or redundant content
- **Currency Assessment**: Determine what needs updating vs. what's current
- **Redundancy Prevention**: Avoid adding duplicate or unnecessary content

### 2. Safe Update Operations
- **Read-First Approach**: Never write without comprehensive analysis
- **Incremental Updates**: Apply changes section by section
- **Content Merging**: Integrate new information with existing content
- **Format Preservation**: Maintain existing structure and emoji usage
- **Validation Gates**: Multiple checkpoints to ensure safety

### 3. Comprehensive Safety Measures
- **Automatic Backups**: Timestamped backups before any changes
- **Rollback Capability**: Instant restore if issues detected
- **Markdown Validation**: Ensure proper formatting and structure
- **Content Integrity**: Verify no information is lost or corrupted
- **Error Recovery**: Graceful handling of file operation failures

### 4. Content Intelligence
- **Semantic Analysis**: Understand content meaning, not just text matching
- **Context Awareness**: Recognize existing documentation patterns
- **Status Tracking**: Monitor completion status and progress indicators
- **Quality Standards**: Maintain high documentation quality and consistency

## Master-Plan Management Domains

### Domain 1: Executive Summary Management
**Focus Areas:**
- **Current State Assessment**: Analyze project health and status indicators
- **Brutal Honesty Updates**: Update honest assessments with current data
- **Success Criteria Refresh**: Update measurable success criteria
- **Immediate Actions**: Maintain current prioritized action items

### Domain 2: Phase Progress Tracking
**Focus Areas:**
- **Phase Completion Status**: Track and update phase progress with metrics
- **Deliverable Documentation**: Update created deliverables and evidence
- **Validation Results**: Document testing and validation outcomes
- **Readiness Assessment**: Update phase-to-phase readiness status

### Domain 3: Architecture Decision Records (ADRs)
**Focus Areas:**
- **Decision Documentation**: Add new architectural decisions with full rationale
- **Alternative Analysis**: Document considered alternatives and trade-offs
- **Impact Assessment**: Track decision impact on user experience and system
- **Status Updates**: Update ADR status based on implementation outcomes

### Domain 4: Skills Execution Tracking
**Focus Areas:**
- **Skills Inventory**: Update skills executed with actual outcomes
- **Performance Metrics**: Document quantified results and improvements
- **Learning Capture**: Update insights and patterns discovered
- **Integration Status**: Track how skills work together

### Domain 5: Success Criteria Management
**Focus Areas:**
- **Criteria Tracking**: Monitor progress toward measurable success criteria
- **Completion Evidence**: Document proof of criteria fulfillment
- **Metrics Updates**: Update quantified metrics with current data
- **Status Validation**: Verify and document completion status

## Safe Operations Workflow

### Phase 1: Document Analysis
```typescript
async analyzeMasterPlan(): Promise<PlanAnalysis> {
  // 1. Read complete current document
  const currentContent = await this.readEntireFile(this.planPath);

  // 2. Parse and understand structure
  const parsedStructure = this.parseMarkdownStructure(currentContent);

  // 3. Analyze content currency and completeness
  const contentAnalysis = {
    currentSections: parsedStructure.sections,
    outdatedContent: this.detectOutdatedContent(parsedStructure),
    missingContent: this.identifyMissingContent(parsedStructure),
    redundantAreas: this.identifyRedundantContent(parsedStructure)
  };

  // 4. Create safety backup
  await this.createTimestampedBackup(currentContent);

  return contentAnalysis;
}
```

### Phase 2: Change Detection
```typescript
async detectNeededChanges(analysis: PlanAnalysis, context: UpdateContext): Promise<NeededChange[]> {
  const neededChanges: NeededChange[] = [];

  // For each potential update, analyze if actually needed
  for (const potentialChange of this.generatePotentialChanges(context)) {
    const existingContent = analysis.currentSections[potentialChange.section];

    // Comprehensive need analysis
    const changeNeeded = !this.contentAlreadyExists(potentialChange, existingContent) &&
                        !this.contentIsCurrent(potentialChange, existingContent) &&
                        !this.wouldBeRedundant(potentialChange, existingContent) &&
                        this.representsMeaningfulImprovement(potentialChange, existingContent);

    if (changeNeeded) {
      neededChanges.push({
        ...potentialChange,
        rationale: this.explainWhyChangeNeeded(potentialChange, existingContent),
        impact: this.assessChangeImpact(potentialChange, existingContent),
        safetyChecks: this.generateSafetyChecks(potentialChange)
      });
    }
  }

  return neededChanges;
}
```

### Phase 3: Safe Update Execution
```typescript
async executeSafeUpdates(changes: NeededChange[]): Promise<UpdateResult> {
  const results: UpdateResult[] = [];

  // Process changes one at a time with validation
  for (const change of changes) {
    try {
      // 1. Pre-change validation
      await this.validatePreChangeConditions(change);

      // 2. Apply change with content preservation
      const updateResult = await this.applyChangeSafely(change);

      // 3. Post-change validation
      await this.validatePostChangeIntegrity(updateResult);

      // 4. Verify document integrity
      await this.validateDocumentIntegrity();

      results.push(updateResult);

    } catch (error) {
      // 5. Rollback if any issues
      await this.rollbackChange(change, error);
      throw new SafeUpdateError(`Change failed and was rolled back: ${error.message}`, change);
    }
  }

  return {
    totalChanges: changes.length,
    successfulChanges: results.length,
    documentIntegrity: await this.verifyDocumentIntegrity(),
    backupLocation: this.currentBackupPath
  };
}
```

## Integration with Chief-Architect

### Delegation Interface
The master-plan-manager skill accepts delegation from chief-architect through standardized interfaces:

#### **Update with Implementation Results**
```typescript
interface ImplementationUpdateRequest {
  action: 'update-with-implementation-results';
  decision: PersonalAppDecision;
  results: PersonalImplementationResult;
  context: PersonalAppContext;
  safetyLevel: 'comprehensive' | 'standard' | 'quick';
}
```

#### **Update with Architecture Decision**
```typescript
interface ArchitectureDecisionUpdateRequest {
  action: 'update-with-architecture-decision';
  decision: PersonalAppDecision;
  alternatives: AlternativeAnalysis[];
  rationale: DecisionRationale;
  impact: ImpactAssessment;
}
```

#### **Update Progress Status**
```typescript
interface ProgressUpdateRequest {
  action: 'update-progress-status';
  phase: number;
  completion: CompletionStatus;
  deliverables: DeliverableRecord[];
  validation: ValidationResults;
}
```

## Safety Validation Gates

### Pre-Update Validation
- **File Integrity**: Verify current file is readable and valid markdown
- **Backup Success**: Confirm backup was created successfully
- **Change Necessity**: Verify change actually improves the document
- **Format Compatibility**: Ensure changes maintain existing structure
- **Content Safety**: Verify no valuable content will be lost

### Post-Update Validation
- **Markdown Integrity**: Validate proper markdown formatting
- **Link Validation**: Ensure all internal links remain valid
- **Structure Consistency**: Verify document structure is maintained
- **Content Accuracy**: Validate updated content is correct
- **Readability Check**: Ensure document remains readable and organized

### Error Recovery
- **Automatic Rollback**: Restore from backup if issues detected
- **Partial Recovery**: Handle partial updates gracefully
- **Error Reporting**: Clear reporting of what failed and why
- **Manual Intervention**: Provide clear information for manual fixes

## Success Criteria

- ✅ **Document Integrity**: Master-plan remains valid and well-structured after all updates
- ✅ **Content Accuracy**: All updates are accurate and well-documented
- ✅ **No Data Loss**: No existing valuable content is ever lost
- ✅ **Redundancy Prevention**: No duplicate or unnecessary content is added
- ✅ **Safety Compliance**: All safety protocols are followed for every operation
- ✅ **Backup Reliability**: All backups are created and can be restored successfully
- ✅ **Integration Success**: Seamless integration with chief-architect delegation

## Usage Examples

### Example 1: Chief-Architect Delegation
```
chief-architect delegates to master-plan-manager:
  action: "update-with-implementation-results"
  decision: { decision: "implement-cross-tab-sync", rationale: "..." }
  results: { filesCreated: 5, testsPassed: 12, performanceImproved: "30%" }
  safetyLevel: "comprehensive"
```

### Example 2: Architecture Decision Documentation
```
master-plan-manager update-architecture-decision:
  section: "Architecture Decision Records"
  decision: "Local-First Data Strategy"
  alternatives: ["IndexedDB", "LocalForage", "Custom Storage"]
  rationale: "Cross-tab sync requirements and offline-first priority"
  impact: { userExperience: "High", developmentComplexity: "Medium" }
```

### Example 3: Progress Status Update
```
master-plan-manager update-progress:
  phase: 3
  completion: { percentage: 85, status: "near-complete" }
  deliverables: ["Cross-tab sync", "Performance optimization", "UI improvements"]
  validation: { testsPassed: "100%", performanceMet: true, userAccepted: true }
```

## Implementation Protocol

### 1. Safety-First Analysis
- Always read complete current file before any operations
- Create timestamped backup before any changes
- Analyze if updates are actually needed and beneficial
- Verify no existing content will be damaged

### 2. Intelligent Updates
- Only update when meaningful improvements are detected
- Preserve existing structure, formatting, and valuable content
- Integrate new information seamlessly with existing content
- Maintain document quality and consistency standards

### 3. Comprehensive Validation
- Validate markdown structure and formatting
- Verify all internal and external links remain valid
- Ensure document remains readable and well-organized
- Confirm all safety protocols were followed

### 4. Error Recovery
- Automatic rollback to previous state if any issues detected
- Clear error reporting and manual intervention guidance
- Multiple recovery options for different failure scenarios
- Learning from errors to improve future operations

## Master-Plan Manager Principles

1. **Document Safety First**: Never compromise document integrity or existing content
2. **Read Before Writing**: Never make changes without comprehensive analysis of current state
3. **Meaningful Updates Only**: Only update when changes represent genuine improvements
4. **Backup and Recovery**: Always maintain reliable backup and rollback capabilities
5. **Format Preservation**: Maintain existing document structure, formatting, and style
6. **Content Intelligence**: Understand context and meaning, not just text patterns
7. **Integration Excellence**: Work seamlessly with chief-architect and other skills
8. **Continuous Learning**: Improve from every operation and maintain operation history

---

## Master-Plan Manager Cognitive Architecture

This skill implements the **Safe Document Management cognitive architecture**:

- **Perception**: Comprehensively reads and analyzes entire document structure and content
- **Analysis**: Understands context, identifies needs, detects redundancies, assesses currency
- **Planning**: Determines optimal update strategies while preserving document integrity
- **Action**: Applies changes safely with comprehensive validation and backup procedures
- **Validation**: Verifies document integrity, content accuracy, and structural consistency
- **Learning**: Maintains operation history and improves from each update experience
- **Safety**: Prioritizes document safety above all other considerations

This creates a **highly reliable document management intelligence** that maintains and improves master-plan documents while ensuring complete safety and integrity of existing content.

---

## MANDATORY USER VERIFICATION REQUIREMENT

### Policy: No Fix Claims Without User Confirmation

**CRITICAL**: Before claiming ANY issue, bug, or problem is "fixed", "resolved", "working", or "complete", the following verification protocol is MANDATORY:

#### Step 1: Technical Verification
- Run all relevant tests (build, type-check, unit tests)
- Verify no console errors
- Take screenshots/evidence of the fix

#### Step 2: User Verification Request
**REQUIRED**: Use the `AskUserQuestion` tool to explicitly ask the user to verify the fix:

```
"I've implemented [description of fix]. Before I mark this as complete, please verify:
1. [Specific thing to check #1]
2. [Specific thing to check #2]
3. Does this fix the issue you were experiencing?

Please confirm the fix works as expected, or let me know what's still not working."
```

#### Step 3: Wait for User Confirmation
- **DO NOT** proceed with claims of success until user responds
- **DO NOT** mark tasks as "completed" without user confirmation
- **DO NOT** use phrases like "fixed", "resolved", "working" without user verification

#### Step 4: Handle User Feedback
- If user confirms: Document the fix and mark as complete
- If user reports issues: Continue debugging, repeat verification cycle

### Prohibited Actions (Without User Verification)
- Claiming a bug is "fixed"
- Stating functionality is "working"
- Marking issues as "resolved"
- Declaring features as "complete"
- Any success claims about fixes

### Required Evidence Before User Verification Request
1. Technical tests passing
2. Visual confirmation via Playwright/screenshots
3. Specific test scenarios executed
4. Clear description of what was changed

**Remember: The user is the final authority on whether something is fixed. No exceptions.**

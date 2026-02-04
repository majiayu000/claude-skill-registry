---
name: update-scope
description: Update living completion report with scope changes during increment execution
---

# Update Increment Scope (Living Reports)

**Purpose**: Log scope changes in real-time during increment execution for complete traceability.

This command adds entries to the **Scope Evolution** section of the completion report, capturing:
- What changed (user stories added/removed/modified)
- Why it changed (business reason, technical blocker, stakeholder request)
- Who approved it (PM, stakeholder, architect)
- Impact on timeline and effort

---

## Why Living Reports Matter

**Problem** (traditional approach):
```
Start: Plan 10 tasks
During work: Scope changes 5 times (but not documented)
End: Report says "Completed 8/10 tasks"
Future: "Why was Task 5 removed?" → No one remembers
```

**Solution** (living reports):
```
Start: Plan 10 tasks + initialize completion report
During work:
  - 2025-11-06: Added US6 (dark mode) → update-scope logged
  - 2025-11-07: Deferred US3 (CSV export) → update-scope logged
  - 2025-11-08: WebSockets → Polling pivot → update-scope logged
End: Report shows complete scope evolution with WHY
Future: "Why was Task 5 removed?" → Check report, find exact reason
```

**Value**:
- ✅ Complete audit trail (why scope changed)
- ✅ Real-time documentation (not reconstructed later)
- ✅ Regulatory compliance (explains deviations)
- ✅ Learning for future increments
- ✅ Onboarding new team members

---

## Usage

### Quick Log

```bash
/sw:update-scope "Added dark mode toggle (stakeholder request from CMO, +16 hours)"
```

### Detailed Log

```bash
/sw:update-scope
# Interactive prompts:
# - What changed? (Added/Removed/Modified user story)
# - What specifically? (e.g., "US6: Dark mode toggle")
# - Why changed? (Stakeholder request, technical blocker, etc.)
# - Impact on effort? (+16 hours, -4 hours, 0)
# - Who approved? (PM, Architect, CTO, etc.)
# - Documentation links? (ADR-008, GitHub issue #123, etc.)
```

---

## How It Works

### Step 1: Detect Current Increment

```typescript
import { MetadataManager } from '../core/metadata-manager';

// Find active increment
const active = await MetadataManager.getActive();

if (active.length === 0) {
  console.error('❌ No active increment found');
  console.error('   Run /sw:status to check increment status');
  process.exit(1);
}

if (active.length > 1) {
  // Multiple active - ask which one
  const choice = await prompt({
    type: 'select',
    message: 'Which increment to update?',
    choices: active.map(inc => ({ name: inc.id, value: inc.id }))
  });
  increment = choice;
} else {
  increment = active[0].id;
}

console.log(`\n📝 Updating scope for: ${increment}\n`);
```

### Step 2: Load Existing Report

```typescript
const reportPath = `.specweave/increments/${increment}/reports/COMPLETION-REPORT.md`;

if (!fs.existsSync(reportPath)) {
  console.error('❌ Completion report not found');
  console.error(`   Expected: ${reportPath}`);
  console.error('   Run /sw:increment to create increment properly');
  process.exit(1);
}

const report = fs.readFileSync(reportPath, 'utf-8');
```

### Step 3: Gather Scope Change Details

**Prompt user** (if not provided in command):

```typescript
const changeType = await prompt({
  type: 'select',
  message: 'What changed?',
  choices: [
    'Added user story',
    'Removed/deferred user story',
    'Modified user story',
    'Technical pivot (architecture change)',
    'Scope reduction',
    'Scope expansion',
    'Other'
  ]
});

const changeDescription = await prompt({
  type: 'input',
  message: 'What specifically changed?',
  validate: input => input.length > 5 || 'Please provide details'
});

const changeReason = await prompt({
  type: 'input',
  message: 'Why did it change?',
  validate: input => input.length > 5 || 'Please provide reason'
});

const impactHours = await prompt({
  type: 'input',
  message: 'Impact on effort (hours):',
  default: '0',
  validate: input => !isNaN(parseInt(input)) || 'Must be a number'
});

const approver = await prompt({
  type: 'input',
  message: 'Who approved this change?',
  default: 'PM'
});

const docLinks = await prompt({
  type: 'input',
  message: 'Related documentation (ADR, issue, PR):',
  default: 'None'
});
```

### Step 4: Add Entry to Scope Evolution Section

```typescript
const today = new Date().toISOString().split('T')[0]; // YYYY-MM-DD

const impactDirection = parseInt(impactHours) > 0 ? '+' : '';
const impactText = impactHours === '0' ? '0 hours' : `${impactDirection}${impactHours} hours`;

const newEntry = `
### ${today}: ${changeType}

**Changed**: ${changeDescription}
**Reason**: ${changeReason}
**Impact**: ${impactText}
**Decision**: ${approver}
**Documentation**: ${docLinks}

---
`;

// Find "## Scope Evolution" section
const scopeEvolutionMarker = '## Scope Evolution (Living Updates)';
const noChangesMarker = '_No scope changes during this increment._';

let updatedReport;

if (report.includes(noChangesMarker)) {
  // First scope change - replace placeholder
  updatedReport = report.replace(
    noChangesMarker,
    '_This section is updated during the increment whenever scope changes occur._\n\n' + newEntry
  );
} else {
  // Append to existing changes
  const scopeIndex = report.indexOf(scopeEvolutionMarker);
  const nextSectionIndex = report.indexOf('\n## ', scopeIndex + scopeEvolutionMarker.length);

  const beforeScope = report.substring(0, nextSectionIndex);
  const afterScope = report.substring(nextSectionIndex);

  updatedReport = beforeScope + '\n' + newEntry + afterScope;
}

// Update report version
const versionRegex = /\*\*Report Version\*\*: v(\d+\.\d+)/;
const match = updatedReport.match(versionRegex);

if (match) {
  const currentVersion = parseFloat(match[1]);
  const newVersion = (currentVersion + 0.1).toFixed(1);
  updatedReport = updatedReport.replace(versionRegex, `**Report Version**: v${newVersion}`);
}

// Update last updated timestamp
const timestampRegex = /\*\*Last Updated\*\*: .*/;
updatedReport = updatedReport.replace(timestampRegex, `**Last Updated**: ${new Date().toISOString()}`);

fs.writeFileSync(reportPath, updatedReport, 'utf-8');

console.log(chalk.green('\n✅ Scope change logged successfully!\n'));
console.log(chalk.dim(`   ${reportPath}\n`));
console.log(chalk.blue('📋 Change summary:'));
console.log(chalk.white(`   Type: ${changeType}`));
console.log(chalk.white(`   Impact: ${impactText}`));
console.log(chalk.white(`   Approved by: ${approver}\n`));

console.log(chalk.dim('💡 View full report:'));
console.log(chalk.dim(`   cat ${reportPath}\n`));
```

---

## Example Output

```
📝 Updating scope for: 0008-user-dashboard

What changed? Added user story
What specifically changed? US6: Dark mode toggle
Why did it change? Stakeholder request from CMO (high priority, blocks marketing launch)
Impact on effort (hours): 16
Who approved this change? PM + CMO
Related documentation (ADR, issue, PR): GitHub issue #45

✅ Scope change logged successfully!

   .specweave/increments/0008-user-dashboard/reports/COMPLETION-REPORT.md

📋 Change summary:
   Type: Added user story
   Impact: +16 hours
   Approved by: PM + CMO

💡 View full report:
   cat .specweave/increments/0008-user-dashboard/reports/COMPLETION-REPORT.md
```

---

## Completion Report Format

The completion report is initialized when increment is created and updated throughout:

```markdown
## Scope Evolution (Living Updates)

_This section is updated during the increment whenever scope changes occur._

### 2025-11-06: Added user story

**Changed**: US6: Dark mode toggle
**Reason**: Stakeholder request from CMO (high priority, blocks marketing launch)
**Impact**: +16 hours
**Decision**: PM + CMO
**Documentation**: GitHub issue #45

---

### 2025-11-07: Removed/deferred user story

**Changed**: US3: Data export to CSV
**Reason**: Not critical for MVP, can be added later without breaking changes
**Impact**: -8 hours (deferred to increment 0009)
**Decision**: PM
**Documentation**: None

---

### 2025-11-08: Technical pivot (architecture change)

**Changed**: WebSockets → Long-polling
**Reason**: WebSocket library had critical security vulnerability (CVE-2025-1234)
**Impact**: -4 hours (simpler implementation)
**Decision**: Architect + Security Lead
**Documentation**: ADR-008: Why We Chose Polling Over WebSockets

---
```

---

## Best Practices

### When to Update

✅ **DO update** when:
- Adding new user story or task
- Removing/deferring work
- Modifying scope of existing story
- Making architecture pivots
- Reducing/expanding scope
- Blocking issues discovered

❌ **DON'T update** for:
- Bug fixes discovered during implementation (normal)
- Minor implementation details
- Code refactoring (unless scope-affecting)

### What to Capture

Always include:
- **What changed**: Specific user story or task
- **Why**: Business reason, technical blocker, stakeholder request
- **Impact**: Hours added/removed
- **Approval**: Who made the decision
- **Links**: ADR, GitHub issue, Jira ticket

### Frequency

- Update in **real-time** when change occurs (don't batch)
- Better to have 10 small entries than 1 large summary
- Captures decision context while fresh

---

## Related Commands

- `/sw:increment "feature"` - Creates increment with initial completion report
- `/sw:done <id>` - Finalizes report and marks increment complete
- `/sw:status` - Check which increment is active

---

**💡 Pro Tip**: Use this command liberally! Living reports are your future self's best friend. When someone asks "Why did we defer feature X?", you'll have the exact answer with full context.

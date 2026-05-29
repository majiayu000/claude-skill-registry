---
name: gsd-verify-installation
description: Run diagnostic checks on GSD installation and report status
allowed-tools: Bash, Read
---


# Verify Installation

Run comprehensive diagnostics to verify GSD installation works correctly.

This command will check:
- ✓ Which CLIs are installed (Claude Code, Copilot CLI, Codex CLI)
- ✓ Whether GSD skill/prompt is registered in each CLI
- ✓ Whether all GSD commands are accessible
- ✓ Whether GSD agents are supported in current CLI

## Running Diagnostics

```javascript
const { runDiagnostics } = require('../../lib-ghcc/verification/diagnostic-runner');
const { CLIInstalledTest, SkillRegisteredTest } = require('../../lib-ghcc/verification/cli-detector');
const { CommandAvailableTest } = require('../../lib-ghcc/verification/command-verifier');
const { AgentCapabilityTest } = require('../../lib-ghcc/verification/agent-verifier');

// Define all diagnostic tests
const tests = [
  // CLI Installation Tests
  new CLIInstalledTest('Claude Code', 'claude'),
  new CLIInstalledTest('GitHub Copilot CLI', 'gh'),
  new CLIInstalledTest('Codex CLI', 'codex'),
  
  // Skill Registration Tests
  new SkillRegisteredTest('claude'),
  new SkillRegisteredTest('copilot'),
  new SkillRegisteredTest('codex'),
  
  // Command Availability Test
  new CommandAvailableTest(),
  
  // Agent Capability Tests (key agents)
  new AgentCapabilityTest('gsd-executor'),
  new AgentCapabilityTest('gsd-planner'),
  new AgentCapabilityTest('gsd-planner-strategist'),
  new AgentCapabilityTest('gsd-verifier'),
  new AgentCapabilityTest('gsd-debugger'),
  new AgentCapabilityTest('gsd-debugger-specialist'),
  new AgentCapabilityTest('gsd-phase-researcher'),
  new AgentCapabilityTest('gsd-plan-checker'),
  new AgentCapabilityTest('gsd-codebase-mapper'),
  new AgentCapabilityTest('gsd-project-researcher'),
  new AgentCapabilityTest('gsd-research-synthesizer'),
  new AgentCapabilityTest('gsd-roadmapper'),
  new AgentCapabilityTest('gsd-integration-checker')
];

// Run diagnostics
runDiagnostics(tests).then(summary => {
  console.log('\n═══════════════════════════════════════════════');
  console.log('  VERIFICATION SUMMARY');
  console.log('═══════════════════════════════════════════════');
  console.log(`✓ ${summary.passed} passed`);
  console.log(`⚠ ${summary.warned} warnings`);
  console.log(`✗ ${summary.failed} failed`);
  console.log('═══════════════════════════════════════════════\n');
  
  if (summary.failed === 0 && summary.warned === 0) {
    console.log('🎉 All checks passed! GSD is ready to use.\n');
  } else if (summary.failed === 0) {
    console.log('⚠️  Some warnings detected. GSD should work but may have limitations.\n');
  } else {
    console.log('❌ Some checks failed. Please address the issues above.\n');
  }
}).catch(error => {
  console.error('Verification error:', error.message);
  process.exit(1);
});
```

## Understanding Results

**Status Icons:**
- ✓ **Pass**: Feature works as expected
- ⚠ **Warn**: Feature works with limitations
- ✗ **Fail**: Feature not available

**Common Issues:**

1. **CLI not installed**: Follow the installation link provided
2. **Skill not registered**: Run `npx get-shit-done-multi --<cli>` to register
3. **Commands missing**: Reinstall GSD package
4. **Agent not supported**: Use a different CLI for that agent

For detailed compatibility information, see `docs/agent-capabilities.md`.

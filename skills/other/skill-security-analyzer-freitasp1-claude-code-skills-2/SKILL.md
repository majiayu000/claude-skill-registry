---
name: skill-security-analyzer
description: Comprehensive security risk analysis for Claude skills. Use when asked to analyze security risks, review security stance, audit skills for vulnerabilities, check security before deployment, or evaluate safety of skill files. Triggers include "analyze security," "security risks," "security audit," "security review," "is this skill safe," or "check for vulnerabilities."
---

# Skill Security Analyzer

Analyze Claude skills for security risks, vulnerabilities, and safety concerns before deployment.

## When to Use This Skill

Use this skill whenever security analysis of a Claude skill is requested, including:
- "Analyze the security of this skill"
- "What are the security risks in my [skill-name]?"
- "Review this skill for vulnerabilities"
- "Is this skill safe to deploy?"
- "Check this skill for security issues"
- "Audit this skill before I use it"

## Analysis Process

Security analysis follows a systematic workflow:

1. **Extract skill contents** - If provided as a .skill file, extract and examine all components
2. **Review skill metadata** - Analyze name, description, and stated purpose
3. **Examine SKILL.md** - Review instructions and identify potential risks
4. **Inspect bundled resources** - Analyze scripts, references, and assets for security issues
5. **Cross-reference patterns** - Check against known security patterns (see references/security_patterns.md)
6. **Generate findings** - Compile severity-rated list of identified risks
7. **Create output** - Provide executive summary, findings list, and security checklist

## Output Format

Provide three components in this order:

### 1. Executive Summary (2-3 sentences)
Brief overall assessment with key takeaway. Examples:
- "This skill has CRITICAL security risks including undisclosed network access and potential data exfiltration. Do not deploy without major modifications."
- "This skill demonstrates good security practices with minor concerns around input validation. Generally safe for deployment with awareness of limitations."

### 2. Findings List
Severity-rated list of specific security issues found:

**CRITICAL** - Immediate security threat, do not deploy
- [Specific finding with evidence]
- [Specific finding with evidence]

**HIGH** - Significant risk, requires remediation
- [Specific finding with evidence]

**MEDIUM** - Moderate concern, should be addressed
- [Specific finding with evidence]

**LOW** - Minor issue or best practice deviation
- [Specific finding with evidence]

**POSITIVE** - Security best practices observed
- [Specific good practice found]

### 3. Security Checklist
Quick reference checklist of security categories:

```
[ ] Data Exfiltration Risks - [PASS/FAIL/CONCERN] - [brief note]
[ ] Network Access - [PASS/FAIL/CONCERN] - [brief note]
[ ] Prompt Injection Protection - [PASS/FAIL/CONCERN] - [brief note]
[ ] Permissions & Scope - [PASS/FAIL/CONCERN] - [brief note]
[ ] PII/Confidential Data - [PASS/FAIL/CONCERN] - [brief note]
[ ] Malicious Code Indicators - [PASS/FAIL/CONCERN] - [brief note]
[ ] Supply Chain Risks - [PASS/FAIL/CONCERN] - [brief note]
[ ] Credential Exposure - [PASS/FAIL/CONCERN] - [brief note]
[ ] Resource Abuse - [PASS/FAIL/CONCERN] - [brief note]
[ ] Transparency & Documentation - [PASS/FAIL/CONCERN] - [brief note]
```

## Analyzing Skill Components

### Skill Metadata Analysis

Check frontmatter and description for:
- **Scope clarity**: Does description match actual functionality?
- **Tool disclosure**: Are all used tools mentioned?
- **External service disclosure**: Are API calls or network access mentioned?
- **Data handling statements**: Is data processing clearly explained?

**Red flags:**
- Vague descriptions that don't explain what the skill does
- Description doesn't mention tools used in code
- Missing disclosure of network access or external services

### SKILL.md Analysis

Read the entire SKILL.md and check for:
- **Instruction clarity**: Are instructions clear and unambiguous?
- **Input handling**: How does skill handle user input?
- **Tool usage justification**: Is tool usage appropriate for stated purpose?
- **Prompt construction**: Are there prompt injection risks?
- **Scope boundaries**: Does skill stay within stated purpose?

**Specific checks:**
1. Search for dynamic prompt construction patterns
2. Check for file access instructions without validation
3. Look for network requests not in description
4. Identify any instruction override patterns
5. Review error handling and data exposure

### Scripts Analysis

For each script in `scripts/`:
1. **Read the script** using the view tool
2. **Check imports** against security patterns reference
3. **Scan for dangerous operations**: file deletion, system commands, network requests
4. **Look for obfuscation**: base64, exec, eval, encoded strings
5. **Validate paths**: check file access uses safe paths
6. **Review subprocess usage**: check for shell=True or user input in commands

**Priority patterns to detect:**
- `exec()`, `eval()`, `__import__()`
- `subprocess.run(..., shell=True)`
- `requests.post()`, `urllib.request`, `fetch()`
- `os.system()`, `os.popen()`
- `base64.b64decode()` followed by execution
- File operations on sensitive paths
- Hardcoded credentials or API keys

### References Analysis

Check reference files for:
- **Sensitive data**: API keys, credentials, internal schemas
- **External resources**: Links to external sites or services
- **Data handling instructions**: How data should be processed
- **Compliance requirements**: Any regulatory considerations

### Assets Analysis

Examine assets for:
- **Executable content**: Scripts disguised as assets
- **External resources**: Templates that load remote content
- **Embedded credentials**: Config files with secrets
- **Unexpected file types**: Files that don't match skill purpose

## Using the Security Patterns Reference

**IMPORTANT**: Read `references/security_patterns.md` at the start of every security analysis to load the comprehensive catalog of security patterns, anti-patterns, and risk indicators.

The reference provides:
- Detailed examples of risky vs. safe implementations
- Specific patterns to search for in code
- Risk categorization and severity guidelines
- Context-specific considerations

Use the reference to:
1. Guide what to look for during analysis
2. Determine severity ratings for findings
3. Provide accurate examples in findings
4. Ensure comprehensive coverage of risk categories

## Handling .skill Files

If provided a .skill file:

1. **Extract contents**: .skill files are zip files with .skill extension
```bash
unzip skillname.skill -d /home/claude/skill-analysis/
```

2. **Verify structure**: Check for SKILL.md and proper directory organization

3. **Analyze extracted contents**: Follow normal analysis process

## Edge Cases

### Skills Without Code
For skills with only SKILL.md (no scripts/assets):
- Focus on instruction analysis
- Check for prompt injection risks in instructions
- Verify tool usage is appropriate
- Assess scope and transparency

### Third-Party Skills
For skills from unknown sources:
- Apply heightened scrutiny
- Mark provenance as a risk factor
- Look extra carefully for obfuscation
- Check for unexpected functionality
- Recommend code review before deployment

### Skills Requesting Unusual Permissions
For skills asking for extensive tool access:
- Verify each tool is justified in description
- Check if tool usage aligns with stated purpose
- Look for scope creep in implementation
- Consider principle of least privilege

## Important Principles

### Be Evidence-Based
- Always cite specific code or instructions when identifying risks
- Provide line numbers or code snippets for findings
- Don't make assumptions - base findings on actual content

### Severity Calibration
- **CRITICAL**: Immediate security threat (data theft, system compromise, credential exposure)
- **HIGH**: Significant risk requiring remediation (unsafe file access, undisclosed network calls)
- **MEDIUM**: Moderate concern (missing input validation, unclear scope)
- **LOW**: Best practice deviation (no security impact but suboptimal)

### Context Matters
- Consider the skill's stated purpose
- Distinguish between necessary functionality and overreach
- Account for legitimate use cases vs. security theater

### Actionable Findings
- Provide specific remediation guidance when possible
- Suggest safer alternatives for risky patterns
- Prioritize findings by risk and effort to fix

## Example Analysis Workflow

```
User: "Analyze the security of this skill" [attaches my-skill.skill]

1. Extract the .skill file
2. Read references/security_patterns.md
3. Review SKILL.md frontmatter and description
4. Analyze SKILL.md instructions
5. Examine each script in scripts/
6. Check references/ for sensitive data
7. Review assets/ for unexpected content
8. Compile findings with severity ratings
9. Generate executive summary
10. Create security checklist
11. Provide formatted output
```

---
name: comprehensive-system-analyzer
emoji: "📊"
description: Deep comprehensive system status analyzer that provides honest truth reporting about entire Pomo-Flow application health, performance, and integrity
triggers:
  - "using comprehensive-system-analyzer"
  - "activate comprehensive-system-analyzer"
  - "skill comprehensive-system-analyzer"
keywords:
  - system
  - health
  - analysis
  - monitoring
  - performance
  - integrity
  - comprehensive
  - status
  - diagnostic
activation_count: 0
last_used: null
related_skills:
  - vue-app-analyzer
  - qa-testing
  - dev-debugging
  - visual-inconsistency-detector
---

# Comprehensive System Analyzer

**Purpose**: Deep, honest, no-holds-barred system health analysis for the Pomo-Flow Vue.js application that tells the complete truth about system status, performance, and integrity.

## Philosophy

This skill provides **brutally honest** system analysis with:
- **Zero sugar-coating** - Tells you exactly what's wrong
- **Complete coverage** - Analyzes every system layer
- **Evidence-based findings** - Provides proof for all issues
- **Prioritized fixes** - Shows what matters most
- **Performance impact** - Quantifies how issues affect users

## Analysis Layers

### 🔧 **Core Application Health**
- Vue.js application initialization and lifecycle
- Component tree integrity and performance
- Router configuration and navigation health
- State management (Pinia) integrity
- Bundle analysis and loading performance

### 📊 **Performance Metrics**
- First Contentful Paint (FCP) and Largest Contentful Paint (LCP)
- Time to Interactive (TTI) and Cumulative Layout Shift (CLS)
- Memory usage patterns and leak detection
- Network request optimization analysis
- JavaScript execution performance

### 🗄️ **Data Layer Analysis**
- IndexedDB health and performance
- Store synchronization integrity
- Data model consistency validation
- Persistence layer reliability
- Backup system functionality

### 🎨 **UI/UX Integrity**
- Component rendering consistency
- Design system compliance
- Accessibility standards adherence
- Responsive design validation
- Visual regression detection

### 🧪 **Testing Coverage**
- Unit test effectiveness analysis
- Integration test coverage
- E2E test reliability
- Test flakiness detection
- Coverage gaps identification

### 🔒 **Security Assessment**
- Dependency vulnerability scanning
- Code security patterns analysis
- Data exposure risks
- Authentication integrity
- Input validation coverage

### 🚀 **Build & Deployment Health**
- Build process optimization
- Bundle size analysis
- Asset loading optimization
- Deployment readiness assessment
- Production preparation checklist

### 📱 **Cross-Platform Compatibility**
- Mobile device compatibility
- Browser compatibility matrix
- Performance across devices
- Responsive behavior validation
- Platform-specific issues

## Usage

```bash
# Full comprehensive analysis
Skill comprehensive-system-analyzer

# Quick health check (5 minutes)
Skill comprehensive-system-analyzer --mode=quick

# Performance-focused analysis
Skill comprehensive-system-analyzer --focus=performance

# Pre-deployment validation
Skill comprehensive-system-analyzer --mode=deployment
```

## Report Structure

### 🚨 **Executive Summary** (Brutal Honesty)
- **Overall Health Score**: 0-100 with evidence
- **Critical Issues**: Must-fix immediately
- **Performance Grade**: A-F with specific metrics
- **Security Posture**: Risk assessment
- **Deployment Readiness**: Go/No-Go with reasons

### 📋 **Detailed Findings**

#### **Critical Issues** (Fix These First)
- Security vulnerabilities with CVE details
- Performance bottlenecks affecting users
- Data integrity risks
- Broken user workflows
- Memory leaks causing crashes

#### **Performance Analysis**
- Bundle size breakdown and optimization opportunities
- Component rendering performance bottlenecks
- Network request optimization gaps
- Memory usage patterns and leak detection
- User experience metrics across device types

#### **Code Quality Assessment**
- TypeScript coverage and type safety
- Component architecture quality
- Test coverage effectiveness
- Code maintainability score
- Technical debt quantification

#### **User Experience Issues**
- Broken workflows and user journeys
- Accessibility violations
- Responsive design failures
- Cross-browser compatibility issues
- Mobile experience problems

#### **Infrastructure Health**
- Build process efficiency
- Asset optimization status
- CDN configuration analysis
- Database performance metrics
- API reliability assessment

### 🎯 **Actionable Recommendations**

#### **Immediate Actions** (Next 24 hours)
- Security patches for critical vulnerabilities
- Performance hotfixes affecting user experience
- Data integrity fixes preventing data loss
- Broken functionality restoration

#### **Short-term Improvements** (Next week)
- Performance optimization implementation
- Test coverage expansion
- Code quality improvements
- User experience enhancements

#### **Long-term Strategy** (Next month)
- Architecture modernization
- Technical debt reduction
- Scalability improvements
- Developer experience enhancements

## Honest Truth Metrics

### **Health Scoring** (No Mercy Grading)
- **90-100**: Excellent (rare, nearly perfect)
- **80-89**: Good (minor issues, generally solid)
- **70-79**: Fair (noticeable issues, needs attention)
- **60-69**: Poor (significant problems, user-impacting)
- **Below 60**: Critical (major issues, intervention required)

### **Performance Grades**
- **A**: <2s FCP, <3s LCP, <100ms TTI
- **B**: <3s FCP, <4s LCP, <200ms TTI
- **C**: <4s FCP, <5s LCP, <300ms TTI
- **D**: >4s FCP, >5s LCP, >300ms TTI
- **F**: Unusable performance

### **Security Risk Levels**
- **Low**: No critical vulnerabilities
- **Medium**: Non-critical vulnerabilities present
- **High**: Critical vulnerabilities require immediate attention
- **Critical**: System compromise likely

## Evidence Requirements

Every finding must include:
- **Reproduction steps** - How to see the issue
- **Screenshots/videos** - Visual evidence
- **Performance metrics** - Quantified impact
- **User impact** - How it affects real users
- **Fix complexity** - Effort required to resolve
- **Priority level** - Urgency based on impact

## Integration with Tools

### **Automated Analysis**
- Bundle analyzer integration
- Lighthouse performance audits
- Security vulnerability scanning
- Code quality metrics
- Dependency analysis

### **Manual Validation**
- Visual regression testing
- Cross-device testing
- User workflow validation
- Accessibility testing
- Performance profiling

### **Continuous Monitoring**
- Real user monitoring (RUM)
- Error tracking integration
- Performance monitoring
- Usage analytics
- A/B test results

## Output Formats

### **Terminal Report** (Immediate feedback)
- Color-coded status indicators
- Progress bars for metrics
- Summary tables with key findings
- Action item prioritization

### **HTML Report** (Detailed analysis)
- Interactive dashboard
- Visual charts and graphs
- Screenshot comparisons
- Detailed technical findings
- Export capabilities

### **JSON Report** (CI/CD integration)
- Machine-readable findings
- Automated tool integration
- Historical trend data
- Performance metrics
- Regression detection

## Advanced Features

### **Historical Tracking**
- Performance trend analysis
- Technical debt accumulation
- Code quality evolution
- Security posture changes
- User experience improvements

### **Predictive Analysis**
- Performance degradation prediction
- Scalability bottleneck identification
- Technical debt forecasting
- Risk assessment evolution
- Resource planning insights

### **Benchmarking**
- Industry standard comparisons
- Competitor analysis (where available)
- Best practices compliance
- Framework version optimization
- Technology stack assessment

## Truth-Telling Examples

### **Instead of saying**:
"Some components could benefit from optimization"

### **The skill says**:
"TaskCard.vue has a render time of 127ms (should be <16ms), causing 40% of users to experience jank. This component renders 1,247 times per page load and uses 8.7MB of memory. Fix this by implementing virtual scrolling."

### **Instead of saying**:
"Consider updating dependencies"

### **The skill says**:
"You have 12 critical security vulnerabilities, including CVE-2024-12345 in package 'example-lib' v1.2.3. Attackers can exploit this to execute remote code. Update to v1.2.4 immediately."

## Success Criteria

The analysis is successful when it:
1. **Tells the complete truth** about system health
2. **Provides actionable evidence** for every finding
3. **Prioritizes issues** by user impact
4. **Quantifies performance impact** with real metrics
5. **Delivers immediate value** with clear next steps

This skill exists to ensure you never have false confidence about your application's health. It provides the brutal honesty needed to build truly excellent software.

---

**Created for Pomo-Flow Vue.js project**
*Comprehensive, honest, no-compromise system analysis*

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

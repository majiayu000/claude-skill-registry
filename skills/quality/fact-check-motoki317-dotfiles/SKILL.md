---
name: Fact Check
description: This skill should be used when the user asks to "verify claims", "fact check", "validate documentation", "check sources", or needs verification of external source references. Provides patterns for systematic fact verification using Context7 and WebSearch.
---

<purpose>
  Provide patterns for systematic fact-checking of claims against authoritative external sources using Context7 MCP and WebSearch tools.
</purpose>

<tools>
  <tool name="resolve-library-id">
    <description>Resolve package name to Context7-compatible library ID</description>
    <param name="libraryName">Library name to search for</param>
    <use_case>Must call before get-library-docs for library documentation claims</use_case>
  </tool>

  <tool name="get-library-docs">
    <description>Fetch documentation for a specific library to verify claims</description>
    <param name="context7CompatibleLibraryID">Library ID from resolve-library-id</param>
    <param name="topic">Specific topic to verify</param>
    <param name="tokens">Max tokens to retrieve (default: 5000)</param>
    <use_case>Verify claims about library APIs, behavior, and best practices</use_case>
  </tool>

  <tool name="WebSearch">
    <description>Search web for verification of general claims</description>
    <param name="query">Search query for verification</param>
    <use_case>Verify claims about standards, specifications, and general technical facts</use_case>
  </tool>

  <tool name="WebFetch">
    <description>Fetch specific URL content for verification</description>
    <param name="url">URL to fetch</param>
    <param name="prompt">Extraction prompt for relevant content</param>
    <use_case>Verify claims against specific documentation pages or specifications</use_case>
  </tool>
</tools>

<workflow>
  <phase name="extract">
    <objective>Identify verifiable claims from content</objective>
    <step>1. Scan content for claims referencing external sources</step>
    <step>2. Classify claims by type (library API, documentation, standard, specification)</step>
    <step>3. Prioritize claims by impact and verifiability</step>
  </phase>
  <phase name="verify">
    <objective>Verify each claim against authoritative sources</objective>
    <step>1. Select appropriate verification source (Context7 for libraries, WebSearch for general)</step>
    <step>2. Query source for relevant information</step>
    <step>3. Compare claim against retrieved evidence</step>
    <step>4. Calculate verification confidence (0-100)</step>
  </phase>
  <phase name="synthesize">
    <objective>Generate verification report</objective>
    <step>1. Compile verified claims with evidence</step>
    <step>2. Flag claims with confidence below 80</step>
    <step>3. Document unverifiable claims</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Claim cannot be verified due to missing documentation</example>
    <action>Note in report as unverifiable, proceed</action>
  </level>
  <level severity="medium">
    <example>Conflicting information from different sources</example>
    <action>Document discrepancy, use AskUserQuestion for clarification</action>
  </level>
  <level severity="high">
    <example>Claim directly contradicts authoritative source</example>
    <action>STOP, flag discrepancy to user with evidence</action>
  </level>
  <level severity="critical">
    <example>Security-related claim is incorrect</example>
    <action>BLOCK operation, require explicit user acknowledgment</action>
  </level>
</error_escalation>

<patterns>
  <pattern name="claim_extraction">
    <description>Identify claims that reference external sources for verification</description>
    <decision_tree name="when_to_use">
      <question>Does the content reference external documentation or standards?</question>
      <if_yes>Apply claim extraction to identify verifiable assertions</if_yes>
      <if_no>No fact-checking needed for this content</if_no>
    </decision_tree>
    <example>
      Claim types to extract:
      Library API claims: "useState returns a tuple"
      Documentation references: "according to the React docs"
      Standard compliance: "follows WCAG 2.1 AA"
      Version-specific behavior: "in React 18, Suspense..."
      Performance claims: "O(log n) complexity per MDN"

      Version-specific example:
      Claim: "React 18 introduces automatic batching for all updates"
      Verification: Query Context7 with topic="batching" for React 18 docs
      Result: Confirmed - React 18 automatically batches state updates inside promises, setTimeout, and native event handlers
    </example>
  </pattern>

  <pattern name="source_selection">
    <description>Choose appropriate verification source based on claim type</description>
    <decision_tree name="when_to_use">
      <question>What type of claim needs verification?</question>
      <branch condition="Library/framework API">Use Context7 with resolve-library-id then get-library-docs</branch>
      <branch condition="Web standard/specification">Use WebSearch for official specification</branch>
      <branch condition="General technical fact">Use WebSearch with authoritative domain filter</branch>
      <branch condition="Specific documentation URL">Use WebFetch to retrieve and verify</branch>
    </decision_tree>
    <example>
      Source priority:
      Context7 for library documentation (trust score 7+)
      WebFetch for specific URLs cited in claims
      WebSearch for general technical claims
      Mark as unverifiable if no source available
    </example>
  </pattern>

  <pattern name="confidence_assessment">
    <description>Calculate verification confidence based on evidence quality</description>
    <decision_tree name="when_to_use">
      <question>Has verification evidence been collected?</question>
      <if_yes>Apply confidence assessment to rate verification quality</if_yes>
      <if_no>Continue evidence collection before assessment</if_no>
    </decision_tree>
    <example>
      Confidence levels:
      90-100: Exact match with authoritative source
      80-89: Strong match with minor wording differences
      70-79: Partial match, some details unverified
      60-69: Weak match, significant uncertainty
      0-59: No match or contradictory evidence

      Threshold: Flag claims with confidence below 80
    </example>
  </pattern>

  <pattern name="discrepancy_reporting">
    <description>Format and report verification failures with evidence</description>
    <decision_tree name="when_to_use">
      <question>Is the verification confidence below 80?</question>
      <if_yes>Apply discrepancy reporting to document the issue</if_yes>
      <if_no>Mark claim as verified</if_no>
    </decision_tree>
    <example>
      Discrepancy report format:
      Claim: Original assertion made
      Source: Where claim was made
      Verification source: Context7/WebSearch result
      Evidence: Actual information from source
      Confidence: 0-100 score
      Recommendation: Suggested correction or note
    </example>
  </pattern>
</patterns>

<concepts>
  <concept name="verification_sources">
    <description>Authoritative sources for different claim types</description>
    <example>
      Library documentation: Context7 MCP
      React: /facebook/react
      Next.js: /vercel/next.js
      TypeScript: /microsoft/typescript
      NixOS: /nixos/nixpkgs

      Web standards: WebSearch with domain filters
      MDN Web Docs: developer.mozilla.org
      W3C: w3.org
      WHATWG: html.spec.whatwg.org
      OWASP: owasp.org
    </example>
  </concept>

  <concept name="claim_types">
    <description>Categories of verifiable claims</description>
    <example>
      API behavior: Function signatures, return types, parameters
      Configuration: Config options, default values, valid settings
      Best practices: Recommended patterns from official docs
      Deprecation: API deprecation status and alternatives
      Compatibility: Version compatibility and requirements
      Performance: Complexity claims, benchmark references
      Security: Security recommendations and vulnerability info
    </example>
  </concept>

  <concept name="confidence_thresholds">
    <description>Confidence score interpretation</description>
    <example>
      80+: Verified - Claim matches authoritative source
      60-79: Uncertain - Partial verification, review recommended
      Below 60: Disputed - Claim contradicts or unsupported by source
      Unverifiable: No authoritative source available
    </example>
  </concept>
</concepts>

<best_practices>
  <practice priority="critical">Use Context7 as primary source for library documentation claims</practice>
  <practice priority="critical">Flag all claims with verification confidence below 80</practice>
  <practice priority="critical">Document evidence source for each verification</practice>
  <practice priority="high">Prefer libraries with Context7 trust score 7+ for verification</practice>
  <practice priority="high">Use WebSearch fallback when Context7 unavailable</practice>
  <practice priority="medium">Include direct quotes from sources as evidence</practice>
  <practice priority="medium">Note when verification source has version mismatch</practice>
</best_practices>

<anti_patterns>
  <avoid name="assumption_verification">
    <description>Marking claims as verified without actual source check</description>
    <instead>Always query Context7 or WebSearch for evidence before marking verified</instead>
  </avoid>

  <avoid name="single_source_reliance">
    <description>Relying on only one source for disputed claims</description>
    <instead>Cross-reference with multiple sources when confidence is borderline (70-85)</instead>
  </avoid>

  <avoid name="ignoring_version_context">
    <description>Verifying claims without considering version differences</description>
    <instead>Note version context and verify against appropriate documentation version</instead>
  </avoid>

  <avoid name="over_verification">
    <description>Attempting to verify every statement including obvious facts</description>
    <instead>Focus on claims referencing external sources, APIs, and specifications</instead>
  </avoid>
</anti_patterns>

<rules priority="critical">
  <rule>Always verify claims against authoritative sources before flagging</rule>
  <rule>Use Context7 as primary source for library and framework claims</rule>
  <rule>Flag claims with confidence below 80 in fact check results</rule>
  <rule>Document evidence source for every verification</rule>
</rules>

<rules priority="standard">
  <rule>Use WebSearch as fallback when Context7 unavailable</rule>
  <rule>Prefer official documentation over third-party sources</rule>
  <rule>Note version context when verifying version-specific claims</rule>
  <rule>Cross-reference disputed claims with multiple sources</rule>
</rules>

<constraints>
  <must>Query authoritative sources before verification</must>
  <must>Document evidence for all verification results</must>
  <must>Flag discrepancies with confidence scores</must>
  <avoid>Marking claims verified without source check</avoid>
  <avoid>Verifying claims based on assumption or memory</avoid>
  <avoid>Ignoring version context in verification</avoid>
</constraints>

<related_agents>
  <agent name="fact-check">Primary agent using this skill for verification</agent>
  <agent name="quality-assurance">Uses fact-check for documentation accuracy</agent>
  <agent name="docs">Uses fact-check to verify documentation claims</agent>
</related_agents>

<related_skills>
  <skill name="context7-usage">Core tool for library documentation verification</skill>
  <skill name="investigation-patterns">Evidence collection methodology</skill>
  <skill name="technical-documentation">Documentation accuracy standards</skill>
</related_skills>

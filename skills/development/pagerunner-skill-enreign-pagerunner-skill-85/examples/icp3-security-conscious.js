/**
 * ICP 3: Security-Conscious
 *
 * Automate workflows on sensitive data without PII reaching the LLM.
 * Works for regulated industries (finance, healthcare, legal) where PII exposure is a risk.
 *
 * Features:
 * - PII tokenization: john@company.com → [EMAIL:a3f9b2]
 * - Local NER: Names detected locally via ONNX model (never leaves your machine)
 * - De-tokenization: Tokens only, write back to forms with real PII
 * - Audit log: Append-only record of every action (compliance proof)
 *
 * Requirements:
 * - Pagerunner built with --features ner (for PERSON/ORG detection)
 * - NER model downloaded: `pagerunner download-model`
 * - Sensitive data operations in a regulated environment
 */

async function extractAndProcessConfidentialData() {
  // 1. Open session with anonymization enabled
  const sessionId = await open_session({
    profile: "agent",
    anonymize: true, // ← KEY: This strips PII before it reaches Claude
    ner: true        // ← OPTIONAL: Detect PERSON/ORG names (requires --features ner)
  });

  const tabs = await list_tabs(sessionId);
  const tabId = tabs[0].target_id;

  // 2. Navigate to confidential page (e.g., client database, employee records)
  await navigate(sessionId, tabId, "https://internal.company.com/clients");
  await wait_for(sessionId, tabId, { selector: ".client-table", ms: 5000 });

  // 3. Extract content — PII is AUTOMATICALLY TOKENIZED
  const content = await get_content(sessionId, tabId);

  // What Claude sees (example):
  // "Client Name: [PERSON:abc123], Email: [EMAIL:def456], Phone: [PHONE:ghi789]"
  //
  // What's actually on the page (only the server/agent knows):
  // "Client Name: John Smith, Email: john@company.com, Phone: +1-555-0123"

  console.log("Claude sees:", content);
  // Output: "Client [PERSON:abc123] has email [EMAIL:def456]"

  // 4. Claude can work with tokens and make decisions
  // "Okay, [PERSON:abc123] needs follow-up. I'll send them an email."

  // 5. When writing back (fill/type), Pagerunner DE-TOKENIZES automatically
  await fill(sessionId, tabId, "input[name='follow_up_email']", "[EMAIL:def456]");
  // Pagerunner replaces [EMAIL:def456] with the actual email before typing

  // 6. Take a screenshot (NOT in anonymization mode — screenshots are blocked)
  // screenshot() call will be blocked when anonymize: true
  // This is intentional: no visual proof = no PII risk from screenshots

  // 7. Close session
  await close_session(sessionId);

  console.log("Workflow complete. PII never reached Claude, audit log recorded all actions.");
}

/**
 * Real-world example: Financial advisor reviewing client accounts
 *
 * Scenario:
 * 1. Advisor has a list of clients with SSNs, account balances, holdings
 * 2. Runs pagerunner with anonymize: true
 * 3. Claude reads: "[PERSON:1], SSN: [SSN:1], Balance: [REDACT:2]"
 * 4. Claude logic: "If balance < $1M and no activity for 6mo, flag for review"
 * 5. Claude fills a form: "Flag [PERSON:1] for review"
 * 6. Pagerunner de-tokenizes and writes the real name to the form
 * 7. Audit log shows: "[PERSON:1] was flagged" (no SSN exposed)
 *
 * Compliance benefit: Claude never sees raw SSN, audit trail proves it
 */

/**
 * Audit log
 *
 * Every action is recorded in ~/.pagerunner/audit.jsonl
 * Example entry:
 * {
 *   "timestamp": "2024-03-23T10:30:45Z",
 *   "session_id": "abc123",
 *   "tool": "get_content",
 *   "anonymization_mode": "tokenize",
 *   "pii_tokens_used": 3,
 *   "result_size_bytes": 1024
 * }
 *
 * Use for compliance reporting: "3 clients reviewed on 2024-03-23, all PII tokenized"
 */

// Call the function
// extractAndProcessConfidentialData()
//   .then(() => console.log("Done"))
//   .catch(err => console.error("Error:", err));

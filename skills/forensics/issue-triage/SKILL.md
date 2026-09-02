---
name: issue-triage
description: 'Use when a human invokes triage on a new configured Slack issue report. Produces a single classified verdict and posts it to the Slack thread, with deduped tracker state. Don''t use for triaging reports from other channels or posting more than one verdict.'
disable-model-invocation: true
---

# Triage issue reports

## Contract

| Field | Bound contract |
|---|---|
| Trigger | Human invokes this skill on a new configured Slack issue report. |
| Authority | Human-only. Requires explicit human invocation. Preview the target and consequence before any credential use, data-at-rest change, paid action, publishing, or remote mutation. |
| Side effect | Posts at most one Slack thread verdict. Creates at most one tracker issue. |
| Done | Exactly one classified verdict exists in the thread and tracker state is deduped. |

## Inputs

- `slack_report_url`: required. The URL of the new configured Slack issue report to triage.
- `slack_token`: required at runtime. Slack bot token scoped to post thread replies.
- `tracker_token`: optional at runtime. Tracker API token for issue creation. Required only if the triage verdict calls for a tracker issue.
- `tracker_base_url`: required at runtime if `tracker_token` is supplied. The tracker instance base URL.
- `slack_channel_id`: derived from `slack_report_url`. The Slack channel ID containing the report.
- `slack_thread_ts`: derived from `slack_report_url`. The thread timestamp of the report message.

## Procedure

1. **Validate invocation.** Confirm human invoked this skill. Stop if the call is not human-originated. Done when: human origin is confirmed.
2. **Fetch the Slack report.** Retrieve the target Slack message using `slack_report_url`. Validate the channel and thread exist. Stop if the message cannot be fetched. Done when: the report message content is in hand.
3. **Classify the report.** Parse the message content. Apply triage classification to the report content. Accepted verdicts and their criteria:
   - `ack`: valid report needing no action. The report describes a known, already-tracked condition with no new information. Cite the existing tracker reference or known-status evidence.
   - `defer`: valid but consciously postponed. The report is actionable but lower priority than current work. Cite the prioritization reason.
   - `escalate`: urgent or beyond this tracker's scope. The report indicates a security incident, data loss, service outage, or a problem requiring a human outside this tracker's workflow. Cite the urgency signal or scope boundary.
   - `close`: invalid, already resolved, or not actionable. The report duplicates a resolved issue, describes expected behavior, or lacks reproducible information. Cite the resolution, expected-behavior reference, or the missing-information gap.
   - `track`: actionable work that must persist, warranting a tracker issue. The report describes a reproducible problem that is not yet tracked. Cite the reproduction evidence.
   The produced verdict must cite the report evidence satisfying its criterion. Produce a single classified verdict. Done when: one verdict from the accepted set is selected with its evidence citation.
4. **Check for duplicates.** Query the tracker for any existing issues that reference this Slack report. If a duplicate issue exists and the verdict is `track`, skip creation and mark the existing issue as the target. Done when: the duplicate check is complete and the target issue is identified or confirmed absent.
5. **Post the verdict to Slack.** Post exactly one thread reply containing the classified verdict and its evidence citation. Stop on failure. Do not post a second reply. Done when: one Slack reply is posted and its timestamp is captured.
6. **Create tracker issue if warranted.** If the verdict is `track` and no duplicate exists, create exactly one tracker issue linked to the Slack report. Stop on failure. Done when: one tracker issue is created (or skipped as duplicate or not warranted).
7. **Confirm state.** Verify the Slack reply was posted and the tracker state reflects at most one issue per report. Mark done. Done when: the Slack reply exists and the tracker has at most one issue per report.

## Failure and recovery
| Failure class | Rule |
|---|---|
| `not-human-originated` | Stop. No post, no issue. Return error. |
| `report-not-found` | Stop. No post, no issue. Return error. |
| `duplicate-issue` | Skip creation. Use existing issue. Proceed to post verdict. |
| `slack-post-failed` | Stop. No tracker issue. Return error with partial result. |
| `tracker-issue-failed` | Stop. Slack post stands. Return error with partial result. |

Partial-result rule: if Slack post succeeded but tracker issue creation failed, the Slack reply is authoritative. Do not delete or edit the posted reply.

## Output

One JSON object: verdict (ack|defer|escalate|close|track), evidence_citation, slack_reply_ts, tracker_issue_url (null when verdict is not track or creation was skipped as duplicate), and is_duplicate.

/**
 * Single-account Google Ads Script template.
 *
 * Replace TODOs with your logic. Conventions used here:
 *  - `stats` object accumulates structured counters; one summary at the end.
 *  - All writes are idempotent via either a label or a search-pre-check.
 *  - Preview mode is supported: label apply is wrapped in try/catch.
 *  - Errors are caught per-entity, never abort the whole run.
 */

var LABEL_NAME = 'My-script-processed';
var LABEL_DESCRIPTION = 'Touched by my-script.js';

function main() {
  ensureLabel(LABEL_NAME, LABEL_DESCRIPTION);

  var stats = {
    entitiesMatched: 0,
    entitiesSkipped: 0,
    operationsApplied: 0,
    errors: 0,
  };

  var iter = AdsApp.campaigns()
    .withCondition("Status = ENABLED")
    // TODO: more conditions, e.g. CampaignName CONTAINS_IGNORE_CASE 'X'
    .get();

  while (iter.hasNext()) {
    var campaign = iter.next();

    if (hasLabel(campaign, LABEL_NAME)) {
      stats.entitiesSkipped++;
      continue;
    }

    stats.entitiesMatched++;
    Logger.log('Processing: ' + campaign.getName());

    try {
      // TODO: do your work here. Examples:
      //   campaign.pause();
      //   var adGroups = campaign.adGroups().get();
      //   while (adGroups.hasNext()) { /* ... */ }
      stats.operationsApplied++;
    } catch (e) {
      stats.errors++;
      Logger.log('  ! ' + campaign.getName() + ': ' + e);
    }

    try {
      campaign.applyLabel(LABEL_NAME);
    } catch (e) {
      Logger.log('  ~ label apply skipped (preview?): ' + e);
    }
  }

  Logger.log('--- Summary ---');
  Logger.log(JSON.stringify(stats, null, 2));

  if (stats.errors > 0) {
    // TODO: replace recipient or remove block
    MailApp.sendEmail({
      to: 'marketing@example.com',
      subject: '[Ads Script] ' + stats.errors + ' errors',
      htmlBody: '<pre>' + JSON.stringify(stats, null, 2) + '</pre>',
    });
  }
}

function ensureLabel(name, description) {
  var existing = AdsApp.labels().withCondition("Name = '" + name + "'").get();
  if (existing.hasNext()) return;
  AdsApp.createLabel(name, description);
  Logger.log('Created label "' + name + '"');
}

function hasLabel(entity, labelName) {
  var labels = entity.labels().get();
  while (labels.hasNext()) {
    if (labels.next().getName() === labelName) return true;
  }
  return false;
}

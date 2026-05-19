/**
 * MCC (manager account) Google Ads Script template using executeInParallel.
 *
 * Runs `processAccount` against every selected child account in parallel
 * (up to 50 concurrent). Each account's per-run summary is aggregated in
 * `finalize`.
 */

function main() {
  AdsManagerApp.accounts()
    .withCondition("Status = ENABLED")
    // TODO: filter by LabelNames or CustomerId to scope which accounts run
    // .withCondition("LabelNames CONTAINS 'Run-my-script'")
    .executeInParallel('processAccount', 'finalize');
}

// IMPORTANT: must be a top-level function (resolved by name by the runtime).
function processAccount() {
  var customerId = AdsApp.currentAccount().getCustomerId();
  var stats = {
    customerId: customerId,
    entitiesProcessed: 0,
    operationsApplied: 0,
    errors: 0,
    errorMessages: [],
  };

  try {
    var iter = AdsApp.campaigns().withCondition("Status = ENABLED").get();
    while (iter.hasNext()) {
      var campaign = iter.next();
      stats.entitiesProcessed++;
      try {
        // TODO: do your work here
        stats.operationsApplied++;
      } catch (e) {
        stats.errors++;
        stats.errorMessages.push(campaign.getName() + ': ' + e);
      }
    }
  } catch (e) {
    stats.errors++;
    stats.errorMessages.push('Top-level: ' + e);
  }

  // Return value MUST be a string.
  return JSON.stringify(stats);
}

function finalize(results) {
  var aggregate = {
    accountsOk: 0,
    accountsFailed: 0,
    totalEntities: 0,
    totalOps: 0,
    totalErrors: 0,
    perAccount: [],
  };

  for (var i = 0; i < results.length; i++) {
    var r = results[i];
    if (r.getStatus() === 'OK') {
      aggregate.accountsOk++;
      var data = JSON.parse(r.getReturnValue());
      aggregate.totalEntities += data.entitiesProcessed;
      aggregate.totalOps += data.operationsApplied;
      aggregate.totalErrors += data.errors;
      aggregate.perAccount.push(data);
    } else {
      aggregate.accountsFailed++;
      aggregate.perAccount.push({
        customerId: r.getCustomerId(),
        status: r.getStatus(),
        error: r.getError(),
      });
    }
  }

  Logger.log('--- Aggregate ---');
  Logger.log(JSON.stringify(aggregate, null, 2));

  if (aggregate.totalErrors > 0 || aggregate.accountsFailed > 0) {
    MailApp.sendEmail({
      to: 'marketing@example.com',
      subject: '[MCC Script] ' + aggregate.totalErrors + ' errors, ' + aggregate.accountsFailed + ' accounts failed',
      htmlBody: '<pre>' + JSON.stringify(aggregate, null, 2) + '</pre>',
    });
  }
}

/**
 * AdsApp.mutate() + AdsApp.search() template.
 *
 * Pattern: read state via GAQL, decide what to mutate, send mutations
 * with idempotency. Use this whenever the SDK lacks a wrapper for what
 * you need (asset group signals, demographic exclusions, change history
 * driven actions, etc.).
 */

function main() {
  var customerId = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');

  var stats = {
    candidates: 0,
    mutated: 0,
    alreadyDone: 0,
    errors: 0,
  };

  // 1. Read with GAQL. Replace this query with whatever you need.
  var query =
    "SELECT ad_group.id, ad_group.name, campaign.name " +
    "FROM ad_group " +
    "WHERE ad_group.status = 'ENABLED' " +
    "AND campaign.status = 'ENABLED'";
  var rows = AdsApp.search(query);

  while (rows.hasNext()) {
    var row = rows.next();
    stats.candidates++;

    // 2. Build the mutate operation.
    //    Example: exclude AGE_RANGE_65_UP on this ad group.
    var resourceName =
      'customers/' + customerId +
      '/adGroupCriteria/' + row.adGroup.id + '~503006';

    var operation = {
      adGroupCriterionOperation: {
        create: {
          resourceName: resourceName,
          negative: true,
          ageRange: { type: 'AGE_RANGE_65_UP' },
        },
      },
    };

    // 3. Mutate with idempotent error handling.
    try {
      var result = AdsApp.mutate(operation);
      if (result.isSuccessful()) {
        stats.mutated++;
        Logger.log('+ ' + row.adGroup.name);
      } else {
        var msg = result.getErrorMessages().join('; ');
        if (/already exists|duplicate/i.test(msg)) {
          stats.alreadyDone++;
        } else {
          stats.errors++;
          Logger.log('! ' + row.adGroup.name + ': ' + msg);
        }
      }
    } catch (e) {
      stats.errors++;
      Logger.log('! ' + row.adGroup.name + ': ' + e);
    }
  }

  Logger.log('--- Summary ---');
  Logger.log(JSON.stringify(stats, null, 2));
}

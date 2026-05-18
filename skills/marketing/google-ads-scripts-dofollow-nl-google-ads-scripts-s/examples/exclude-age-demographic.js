/**
 * Google Ads Script: exclude the 65+ age range from every ad group inside
 * any ENABLED campaign whose name contains "Channable" (case-insensitive).
 *
 * Each campaign is labeled after processing so subsequent runs skip it,
 * making the script cheap to schedule daily.
 *
 * Google Ads Scripts has no native age-exclusion helper for Search/Display
 * ad groups (only VideoAgeBuilder exists, for video campaigns), so this uses
 * AdsApp.mutate() with a raw AdGroupCriterion payload. Verified payload:
 * resourceName + negative + ageRange.type, no separate adGroup field.
 */

var CAMPAIGN_NAME_CONTAINS = 'channable';
var LABEL_NAME = 'Channable 65+ excluded';
var LABEL_DESCRIPTION = 'Applied by exclude-65+ script after processing all ad groups';

// Well-known Google Ads criterion IDs for age ranges.
var AGE_RANGE_CRITERION_IDS = {
  AGE_RANGE_18_24: 503001,
  AGE_RANGE_25_34: 503002,
  AGE_RANGE_35_44: 503003,
  AGE_RANGE_45_54: 503004,
  AGE_RANGE_55_64: 503005,
  AGE_RANGE_65_UP: 503006,
  AGE_RANGE_UNDETERMINED: 503999,
};

var AGE_RANGE_TO_EXCLUDE = 'AGE_RANGE_65_UP';

function main() {
  var customerId = AdsApp.currentAccount().getCustomerId().replace(/-/g, '');
  var criterionId = AGE_RANGE_CRITERION_IDS[AGE_RANGE_TO_EXCLUDE];

  ensureLabel(LABEL_NAME, LABEL_DESCRIPTION);

  var stats = {
    campaignsMatched: 0,
    campaignsSkipped: 0,
    adGroupsProcessed: 0,
    exclusionsAdded: 0,
    alreadyExcluded: 0,
    errors: 0,
  };

  processCampaigns(AdsApp.campaigns(), 'Search/Display', customerId, criterionId, stats);
  processCampaigns(AdsApp.shoppingCampaigns(), 'Shopping', customerId, criterionId, stats);
  processCampaigns(AdsApp.videoCampaigns(), 'Video', customerId, criterionId, stats);

  Logger.log('--- Summary ---');
  Logger.log('Campaigns processed:  ' + stats.campaignsMatched);
  Logger.log('Campaigns skipped:    ' + stats.campaignsSkipped + ' (already labeled)');
  Logger.log('Ad groups processed:  ' + stats.adGroupsProcessed);
  Logger.log('Exclusions added:     ' + stats.exclusionsAdded);
  Logger.log('Already excluded:     ' + stats.alreadyExcluded);
  Logger.log('Errors:               ' + stats.errors);
}

function processCampaigns(selector, label, customerId, criterionId, stats) {
  var iterator = selector
    .withCondition("Status = ENABLED")
    .withCondition("CampaignName CONTAINS_IGNORE_CASE '" + CAMPAIGN_NAME_CONTAINS + "'")
    .get();

  while (iterator.hasNext()) {
    var campaign = iterator.next();

    if (hasLabel(campaign, LABEL_NAME)) {
      stats.campaignsSkipped++;
      continue;
    }

    stats.campaignsMatched++;
    Logger.log('[' + label + '] Campaign: ' + campaign.getName());

    var adGroups = campaign.adGroups().get();
    while (adGroups.hasNext()) {
      processAdGroup(adGroups.next(), customerId, criterionId, stats);
    }

    try {
      campaign.applyLabel(LABEL_NAME);
      Logger.log('  ~ labeled "' + LABEL_NAME + '"');
    } catch (e) {
      // In preview mode AdsApp.createLabel() doesn't persist, so applyLabel
      // can't find the label and throws. Harmless — on a live run the label
      // exists and the apply succeeds.
      Logger.log('  ~ could not apply label (likely preview mode): ' + e);
    }
  }
}

function processAdGroup(adGroup, customerId, criterionId, stats) {
  stats.adGroupsProcessed++;

  var adGroupId = adGroup.getId();
  var adGroupName = adGroup.getName();
  var resourceName = 'customers/' + customerId + '/adGroupCriteria/' + adGroupId + '~' + criterionId;

  var operation = {
    adGroupCriterionOperation: {
      create: {
        resourceName: resourceName,
        negative: true,
        ageRange: { type: AGE_RANGE_TO_EXCLUDE },
      },
    },
  };

  try {
    var result = AdsApp.mutate(operation);
    if (result.isSuccessful()) {
      stats.exclusionsAdded++;
      Logger.log('  + ' + adGroupName + ': 65+ excluded');
      return;
    }
    var errors = result.getErrorMessages().join('; ');
    if (/already exists|duplicate/i.test(errors)) {
      stats.alreadyExcluded++;
      Logger.log('  - ' + adGroupName + ': already excluded');
    } else {
      stats.errors++;
      Logger.log('  ! ' + adGroupName + ': ' + errors);
    }
  } catch (e) {
    stats.errors++;
    Logger.log('  ! ' + adGroupName + ': ' + e);
  }
}

function ensureLabel(name, description) {
  var existing = AdsApp.labels().withCondition("Name = '" + name + "'").get();
  if (existing.hasNext()) return;
  AdsApp.createLabel(name, description);
  Logger.log('Created label "' + name + '"');
}

function hasLabel(campaign, labelName) {
  var labels = campaign.labels().get();
  while (labels.hasNext()) {
    if (labels.next().getName() === labelName) return true;
  }
  return false;
}

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from build_search_index import build_search_index  # noqa: E402
from category_taxonomy import get_taxonomy  # noqa: E402


def run_node_harness(script: str, *args: str) -> dict:
    completed = subprocess.run(
        ["node", "-e", script, *args],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr)
    return json.loads(completed.stdout)


def test_pages_request_budgets_and_exhaustive_search_behavior():
    result = run_node_harness(
        r"""
const fs = require('fs');
const assert = require('assert');
const app = fs.readFileSync('docs/js/app.js', 'utf8');
const artifactApi = fs.readFileSync('docs/js/artifact-api.js', 'utf8');
const render = fs.readFileSync('docs/js/app-render.js', 'utf8');

function extract(source, name) {
  const asyncStart = source.indexOf(`async function ${name}(`);
  const start = asyncStart >= 0 ? asyncStart : source.indexOf(`function ${name}(`);
  assert(start >= 0, `missing function ${name}`);
  const bodyStart = source.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escaped = false;
  for (let i = bodyStart; i < source.length; i += 1) {
    const char = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"' || char === '`') {
      quote = char;
    } else if (char === '{') {
      depth += 1;
    } else if (char === '}') {
      depth -= 1;
      if (depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated function ${name}`);
}

const responses = new Map();
const requests = [];
global.fetch = async url => {
  requests.push(url);
  if (!responses.has(url)) return { ok: false, status: 404, json: async () => ({}) };
  return { ok: true, status: 200, json: async () => structuredClone(responses.get(url)) };
};

const CONFIG = {
  INDEX_URL: 'search-index-lite.json',
  LEGACY_INDEX_URL: 'search-index.json',
  LEADERBOARD_SIZE: 50,
  FUSE_OPTIONS: {}
};
const CATEGORY_NAMES = { dev: 'Development', oth: 'Other' };
const CATEGORY_CODES_REVERSE = { development: 'dev', other: 'oth' };
let DEFAULT_CATEGORY_CODE = 'oth';
let state = {
  index: null, fullIndex: null, categories: [], categoryCache: {}, featured: [],
  leaderboardRequestToken: 0,
  currentQuery: '', currentStarsFilter: '', currentSourceFilter: '',
  currentTagFilters: [], currentCategory: ''
};

eval(extract(app, 'fetchJson'));
eval(extract(app, 'normalizeCategoryCode'));
eval(extract(app, 'normalizeSkillRecord'));
eval(extract(artifactApi, 'requireExactFields'));
eval(extract(artifactApi, 'requireSchemaOne'));
eval(extract(artifactApi, 'isSafeArtifactPath'));
eval(extract(artifactApi, 'requireNonNegativeInteger'));
eval(extract(artifactApi, 'normalizeSearchIndex'));
eval(extract(artifactApi, 'validateSearchPointer'));
eval(extract(artifactApi, 'validateSearchManifest'));
eval(extract(artifactApi, 'validateSearchShardEntry'));
eval(extract(artifactApi, 'validateSearchShardPayload'));
eval(extract(artifactApi, 'validateCategoryIndexEntry'));
eval(extract(artifactApi, 'validateCategoryManifest'));
eval(extract(artifactApi, 'validateCategoryPartEntry'));
eval(extract(artifactApi, 'validateCategoryPartPayload'));
eval(extract(app, 'loadSearchIndex'));
eval(extract(app, 'findCategoryByCode'));
eval(extract(app, 'loadCategoryLeaderboardSkills'));
eval(extract(app, 'loadFullSearchIndex'));

responses.set('search-index-lite.json', {
  schema_version: 1, version: 'lite', updated_at: '2026-07-11T00:00:00Z',
  total_count: 4, included_count: 2, limit: 1000, raw_count: 4,
  dedupe_key: 'install|branch',
  skills: [{ name: 'Lite A', install: 'a/a' }, { name: 'Lite B', install: 'b/b' }]
});

(async () => {
  state.index = await loadSearchIndex();
  assert.deepStrictEqual(requests, ['search-index-lite.json']);
  assert.strictEqual(state.index.isLite, true);
  assert.strictEqual(state.index.includedCount, 2);
  assert.throws(() => normalizeSearchIndex({
    ...responses.get('search-index-lite.json'), unexpected: []
  }), /shape mismatch/);
  assert.throws(() => normalizeSearchIndex({
    ...responses.get('search-index-lite.json'), included_count: 1
  }), /count or identity mismatch/);

  const firstPart = Array.from({ length: 60 }, (_, i) => ({
    name: `Rank ${i}`, install: `owner/rank-${i}`, stars: 1000 - i, category: 'development'
  }));
  responses.set('categories/development/manifest.json', {
    schema_version: 1, category: 'development', code: 'dev',
    updated_at: '2026-07-11T00:00:00Z', total_count: 70, count: 70, part_count: 2,
    part_strategy: 'bounded-sequential-stars-desc', largest_part_bytes: 200,
    largest_part_gzip_bytes: 100,
    parts: [
      { path: 'categories/development/part-000.json',
        gzip_path: 'categories/development/part-000.json.gz', count: 60,
        bytes: 200, gzip_bytes: 100, sha256: 'c'.repeat(64) },
      { path: 'categories/development/part-001.json',
        gzip_path: 'categories/development/part-001.json.gz', count: 10,
        bytes: 100, gzip_bytes: 50, sha256: 'd'.repeat(64) }
    ]
  });
  responses.set('categories/development/part-000.json', {
    schema_version: 1, category: 'development', code: 'dev',
    updated_at: '2026-07-11T00:00:00Z', part: 0, part_count: 2, count: 60, skills: firstPart
  });
  responses.set('categories/development/part-001.json', { skills: [{ name: 'Must not fetch' }] });
  const categoryEntry = { name: 'development', code: 'dev', count: 70,
    path: 'categories/development.json', manifest: 'categories/development/manifest.json',
    part_count: 2, largest_part_bytes: 200, largest_part_gzip_bytes: 100 };
  state.categories = [categoryEntry];
  const categorySkills = await loadCategoryLeaderboardSkills('dev');
  assert.strictEqual(categorySkills.length, 60);
  assert.deepStrictEqual(requests.slice(1), [
    'categories/development/manifest.json', 'categories/development/part-000.json'
  ]);
  state.categoryCache = {};
  const categoryManifest = responses.get('categories/development/manifest.json');
  delete categoryManifest.part_strategy;
  const invalidCategoryStart = requests.length;
  await assert.rejects(loadCategoryLeaderboardSkills('dev'), /shape mismatch/);
  assert.deepStrictEqual(requests.slice(invalidCategoryStart), ['categories/development/manifest.json']);
  categoryManifest.part_strategy = 'bounded-sequential-stars-desc';
  state.categories = [];
  const missingCategoryStart = requests.length;
  await assert.rejects(loadCategoryLeaderboardSkills('dev'), /Unknown leaderboard category/);
  assert.strictEqual(requests.length, missingCategoryStart);
  state.categories = [categoryEntry];

  categoryManifest.part_strategy = 'invalid';
  state.categoryCache = {};
  const failedElements = {
    leaderboardSection: { classList: { remove() {} } },
    leaderboardList: { innerHTML: 'must be cleared' },
    leaderboardStatus: { textContent: '' }
  };
  const failedRunner = new Function(
    'state', 'elements', 'CONFIG', 'normalizeSkillRecord', 'loadCategoryLeaderboardSkills',
    'createLeaderboardCard', `${extract(render, 'showLeaderboard')}; return showLeaderboard;`
  )(state, failedElements, CONFIG, normalizeSkillRecord, loadCategoryLeaderboardSkills,
    () => { throw new Error('ranked cards must not render'); });
  const invalidManifestStart = requests.length;
  await failedRunner('dev');
  assert.strictEqual(failedElements.leaderboardList.innerHTML, '');
  assert.match(failedElements.leaderboardStatus.textContent, /load failed.*retry/i);
  assert.deepStrictEqual(requests.slice(invalidManifestStart), [
    'categories/development/manifest.json'
  ]);
  categoryManifest.part_strategy = 'bounded-sequential-stars-desc';
  state.categories = [{ name: 'development', code: 'dev' }];
  failedElements.leaderboardList.innerHTML = 'must be cleared again';
  const missingManifestStart = requests.length;
  await failedRunner('dev');
  assert.strictEqual(failedElements.leaderboardList.innerHTML, '');
  assert.match(failedElements.leaderboardStatus.textContent, /load failed.*retry/i);
  assert.strictEqual(requests.length, missingManifestStart);
  state.categories = [categoryEntry];

  const beforeGlobal = requests.length;
  state.featured = [
    { name: 'Featured B', install: 'f/b', stars: 10 },
    { name: 'Featured A', install: 'f/a', stars: 20 }
  ];
  const globalElements = {
    leaderboardSection: { classList: { remove() {} } },
    leaderboardList: { innerHTML: '' },
    leaderboardStatus: { textContent: '' }
  };
  const globalRunner = new Function(
    'state', 'elements', 'CONFIG', 'normalizeSkillRecord', 'loadCategoryLeaderboardSkills',
    'createLeaderboardCard', `${extract(render, 'showLeaderboard')}; return showLeaderboard;`
  )(state, globalElements, CONFIG, normalizeSkillRecord,
    async () => { throw new Error('category loader should not run'); },
    skill => skill.n);
  await globalRunner('');
  assert.strictEqual(requests.length, beforeGlobal);
  assert.strictEqual(globalElements.leaderboardList.innerHTML, 'Featured AFeatured B');

  let releaseSlow;
  const delayedElements = {
    leaderboardSection: { classList: { remove() {} } },
    leaderboardList: { innerHTML: '' },
    leaderboardStatus: { textContent: '' }
  };
  const delayedRunner = new Function(
    'state', 'elements', 'CONFIG', 'normalizeSkillRecord', 'loadCategoryLeaderboardSkills',
    'createLeaderboardCard', `${extract(render, 'showLeaderboard')}; return showLeaderboard;`
  )(state, delayedElements, CONFIG, normalizeSkillRecord,
    category => category === 'dev'
      ? new Promise(resolve => { releaseSlow = resolve; })
      : Promise.resolve([{ n: 'Fast category', r: 20, i: 'fast/skill', b: 'main' }]),
    skill => skill.n);
  const slowRequest = delayedRunner('dev');
  await Promise.resolve();
  await delayedRunner('oth');
  const currentStatus = delayedElements.leaderboardStatus.textContent;
  releaseSlow([{ n: 'Stale category', r: 100, i: 'stale/skill', b: 'main' }]);
  await slowRequest;
  assert.strictEqual(delayedElements.leaderboardList.innerHTML, 'Fast category');
  assert.strictEqual(delayedElements.leaderboardStatus.textContent, currentStatus);

  responses.set('search-index.json', {
    schema_version: 1, total_count: 4, t: 4, v: 'full', deprecated_full_payload: true,
    message: 'Full search payload moved to shards', manifest: 'search-index-manifest.json',
    replacement: 'search-shards/part-*.json', compat_since: 'static-artifact-api-v1',
    compat_until: 'static-artifact-api-v2'
  });
  responses.set('search-index-manifest.json', {
    schema_version: 1, v: 'full', updated_at: '2026-07-11T00:00:00Z', total_count: 4,
    shard_strategy: 'bounded-sequential-stars-desc', record_schema: 'search-mini-v2',
    shard_count: 2, largest_shard_bytes: 200, largest_shard_gzip_bytes: 100,
    shards: [
      { path: 'search-shards/part-000.json', gzip_path: 'search-shards/part-000.json.gz',
        count: 2, bytes: 200, gzip_bytes: 100, sha256: 'a'.repeat(64) },
      { path: 'search-shards/part-001.json', gzip_path: 'search-shards/part-001.json.gz',
        count: 2, bytes: 200, gzip_bytes: 100, sha256: 'b'.repeat(64) }
    ]
  });
  responses.set('search-shards/part-000.json', {
    schema_version: 1, v: 'full', part: 0, part_count: 2, count: 2,
    s: [{ n: 'A', i: 'a/skill', b: 'main' }, { n: 'B', i: 'b/skill', b: 'main' }]
  });
  responses.set('search-shards/part-001.json', {
    schema_version: 1, v: 'full', part: 1, part_count: 2, count: 2,
    s: [{ n: 'C', i: 'c/skill', b: 'main' }, { n: 'Needle', i: 'n/skill', b: 'main' }]
  });
  const full = await loadFullSearchIndex();
  assert.strictEqual(full.s.length, 4);
  assert.deepStrictEqual(requests.slice(beforeGlobal), [
    'search-index.json', 'search-index-manifest.json',
    'search-shards/part-000.json', 'search-shards/part-001.json'
  ]);

  state.fullIndex = null;
  responses.get('search-index.json').unexpected = [];
  await assert.rejects(loadFullSearchIndex(), /pointer shape mismatch/);
  delete responses.get('search-index.json').unexpected;

  state.fullIndex = null;
  responses.get('search-index-manifest.json').unexpected = [];
  await assert.rejects(loadFullSearchIndex(), /manifest shape mismatch/);
  delete responses.get('search-index-manifest.json').unexpected;

  state.fullIndex = null;
  responses.get('search-index-manifest.json').shards[0].unexpected = 1;
  await assert.rejects(loadFullSearchIndex(), /entry shape mismatch/);
  delete responses.get('search-index-manifest.json').shards[0].unexpected;

  state.fullIndex = null;
  const firstPayload = responses.get('search-shards/part-000.json');
  firstPayload.skills = firstPayload.s;
  delete firstPayload.s;
  await assert.rejects(loadFullSearchIndex(), /payload shape mismatch/);
  firstPayload.s = firstPayload.skills;
  delete firstPayload.skills;

  state.fullIndex = null;
  responses.get('search-shards/part-001.json').s[1] = { n: 'Duplicate', i: 'a/skill', b: 'main' };
  await assert.rejects(loadFullSearchIndex(), /duplicate stable records/);
  responses.get('search-shards/part-001.json').s[1] = { n: 'Needle', i: 'n/skill', b: 'main' };

  state.fullIndex = null;
  const searchManifest = responses.get('search-index-manifest.json');
  searchManifest.shards[0].path = '../escape.json';
  const unsafeStart = requests.length;
  await assert.rejects(loadFullSearchIndex(), /Invalid or duplicate search shard path/);
  assert.deepStrictEqual(requests.slice(unsafeStart), ['search-index.json', 'search-index-manifest.json']);
  searchManifest.shards[0].path = 'search-shards/part-000.json';

  state.fullIndex = null;
  responses.get('search-shards/part-000.json').part = 9;
  await assert.rejects(loadFullSearchIndex(), /identity\/count mismatch/);
  responses.get('search-shards/part-000.json').part = 0;

  state.fullIndex = null;
  delete responses.get('search-index.json').schema_version;
  await assert.rejects(loadFullSearchIndex(), /shape mismatch/);
  responses.get('search-index.json').schema_version = 1;

  state.fullIndex = null;
  responses.get('search-index.json').schema_version = 2;
  await assert.rejects(loadFullSearchIndex(), /schema_version must be 1/);
  responses.get('search-index.json').schema_version = 1;

  state.fullIndex = null;
  searchManifest.shard_count = 3;
  await assert.rejects(loadFullSearchIndex(), /manifest count or identity mismatch/);
  searchManifest.shard_count = 2;

  const actionState = { index: state.index, currentQuery: 'needle' };
  const actionElements = {
    searchAllBtn: { disabled: false, textContent: '' },
    searchScope: { textContent: '' }
  };
  let fuseSize = 0;
  let rerunQuery = '';
  const actionRunner = new Function(
    'state', 'elements', 'loadFullSearchIndex', 'Fuse', 'CONFIG',
    'updateSearchScopeDisplay', 'search', 'hasActiveFilters', 'searchWithFiltersOnly',
    `${extract(app, 'activateFullSearch')}; return activateFullSearch;`
  )(
    actionState, actionElements, async () => full,
    class { constructor(skills) { fuseSize = skills.length; } }, CONFIG,
    () => {}, query => { rerunQuery = query; }, () => false, async () => {}
  );
  await actionRunner();
  assert.strictEqual(actionState.index.s.length, 4);
  assert.strictEqual(fuseSize, 4);
  assert.strictEqual(rerunQuery, 'needle');

  process.stdout.write(JSON.stringify({ requests, fullCount: full.s.length, fuseSize, rerunQuery }));
})().catch(error => { console.error(error); process.exit(1); });
"""
    )

    assert result["fullCount"] == 4
    assert result["fuseSize"] == 4
    assert result["rerunQuery"] == "needle"
    assert "categories/development/part-001.json" not in result["requests"]


def test_generated_full_index_uses_lite_stable_key_winners(tmp_path):
    output_dir = tmp_path / "docs"
    duplicate_skills = [
        {
            "name": "Lower-ranked duplicate",
            "description": "short",
            "category": "other",
            "repo": "acme/demo",
            "install": "acme/demo",
            "branch": "main",
            "path": "",
            "stars": 1,
        },
        {
            "name": "Deterministic winner",
            "description": "A much more complete description for the stable-key winner.",
            "category": "development",
            "repo": "acme/demo",
            "install": "acme/demo",
            "branch": "main",
            "path": "",
            "stars": 50,
        },
    ]

    stats = build_search_index(duplicate_skills, output_dir)
    manifest = json.loads((output_dir / "search-index-manifest.json").read_text())
    full_records = []
    for shard in manifest["shards"]:
        payload = json.loads((output_dir / shard["path"]).read_text())
        full_records.extend(payload["s"])
    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    category_index = json.loads((output_dir / "categories/index.json").read_text())
    category_manifest = json.loads(
        (output_dir / "categories/development/manifest.json").read_text()
    )

    assert manifest["total_count"] == len(full_records) == lite["total_count"] == 1
    assert full_records[0]["n"] == lite["skills"][0]["name"] == "Deterministic winner"
    assert len(category_index["categories"]) == 1
    assert {
        key: category_index["categories"][0][key] for key in ("name", "code", "count")
    } == {"name": "development", "code": "dev", "count": 1}
    assert category_manifest["count"] == 1
    assert stats["indexed_skill_count_scan_shape"] == manifest["total_count"] == 1
    assert lite["raw_count"] == len(duplicate_skills) == 2
    assert stats["lite_index_count"] == manifest["total_count"]
    assert sum(item["count"] for item in stats["category_counts"]) == manifest["total_count"]

    reversed_output_dir = tmp_path / "docs-reversed"
    build_search_index(list(reversed(duplicate_skills)), reversed_output_dir)
    reversed_lite = json.loads(
        (reversed_output_dir / "search-index-lite.json").read_text()
    )
    reversed_manifest = json.loads(
        (reversed_output_dir / "search-index-manifest.json").read_text()
    )
    reversed_shard = json.loads(
        (reversed_output_dir / reversed_manifest["shards"][0]["path"]).read_text()
    )
    assert reversed_lite["skills"][0]["name"] == "Deterministic winner"
    assert reversed_shard["s"][0]["n"] == "Deterministic winner"

    reader_result = run_node_harness(
        r"""
const fs = require('fs');
const path = require('path');
const assert = require('assert');
const root = process.argv[1];
const app = fs.readFileSync('docs/js/app.js', 'utf8');
const artifactApi = fs.readFileSync('docs/js/artifact-api.js', 'utf8');

function extract(source, name) {
  const asyncStart = source.indexOf(`async function ${name}(`);
  const start = asyncStart >= 0 ? asyncStart : source.indexOf(`function ${name}(`);
  assert(start >= 0, `missing function ${name}`);
  const bodyStart = source.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escaped = false;
  for (let i = bodyStart; i < source.length; i += 1) {
    const char = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"' || char === '`') quote = char;
    else if (char === '{') depth += 1;
    else if (char === '}') {
      depth -= 1;
      if (depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated function ${name}`);
}

global.fetch = async url => {
  const artifactPath = path.join(root, url);
  if (!fs.existsSync(artifactPath)) return { ok: false, status: 404 };
  return { ok: true, status: 200, json: async () => JSON.parse(fs.readFileSync(artifactPath)) };
};
const CONFIG = { LEGACY_INDEX_URL: 'search-index.json' };
const CATEGORY_NAMES = { dev: 'Development', oth: 'Other' };
const CATEGORY_CODES_REVERSE = { development: 'dev', other: 'oth' };
let DEFAULT_CATEGORY_CODE = 'oth';
let state = { index: { isLite: true }, fullIndex: null };
eval(extract(app, 'fetchJson'));
eval(extract(app, 'normalizeCategoryCode'));
eval(extract(app, 'normalizeSkillRecord'));
eval(extract(artifactApi, 'requireExactFields'));
eval(extract(artifactApi, 'requireSchemaOne'));
eval(extract(artifactApi, 'isSafeArtifactPath'));
eval(extract(artifactApi, 'requireNonNegativeInteger'));
eval(extract(artifactApi, 'normalizeSearchIndex'));
eval(extract(artifactApi, 'validateSearchPointer'));
eval(extract(artifactApi, 'validateSearchManifest'));
eval(extract(artifactApi, 'validateSearchShardEntry'));
eval(extract(artifactApi, 'validateSearchShardPayload'));
eval(extract(app, 'loadFullSearchIndex'));

loadFullSearchIndex().then(full => {
  process.stdout.write(JSON.stringify({ total: full.t, count: full.s.length, name: full.s[0].n }));
}).catch(error => { console.error(error); process.exit(1); });
""",
        str(output_dir),
    )
    assert reader_result == {"total": 1, "count": 1, "name": "Deterministic winner"}


def test_generated_stable_key_winner_is_order_independent_for_equal_scores(tmp_path):
    tied_skills = [
        {
            "name": name,
            "description": "same-length-description",
            "category": "development",
            "repo": "acme/demo",
            "install": "acme/demo",
            "branch": "main",
            "path": "",
            "stars": 10,
        }
        for name in ("Alpha", "Beta")
    ]

    winners = []
    for index, skills in enumerate((tied_skills, list(reversed(tied_skills)))):
        output_dir = tmp_path / f"equal-score-{index}"
        build_search_index(skills, output_dir)
        manifest = json.loads((output_dir / "search-index-manifest.json").read_text())
        shard = json.loads((output_dir / manifest["shards"][0]["path"]).read_text())
        lite = json.loads((output_dir / "search-index-lite.json").read_text())
        winners.append((shard["s"][0]["n"], lite["skills"][0]["name"]))

    assert winners == [("Beta", "Beta"), ("Beta", "Beta")]


def test_pages_taxonomy_contract_drives_all_category_mappings():
    contract = get_taxonomy().public_contract(updated_at="2026-07-23T00:00:00Z")
    result = run_node_harness(
        r"""
const fs = require('fs');
const assert = require('assert');
const app = fs.readFileSync('docs/js/app.js', 'utf8');
const artifactApi = fs.readFileSync('docs/js/artifact-api.js', 'utf8');
const payload = JSON.parse(process.argv[1]);

function extract(source, name) {
  const start = source.indexOf(`function ${name}(`);
  assert(start >= 0, `missing function ${name}`);
  const bodyStart = source.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escaped = false;
  for (let i = bodyStart; i < source.length; i += 1) {
    const char = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"' || char === '`') quote = char;
    else if (char === '{') depth += 1;
    else if (char === '}') {
      depth -= 1;
      if (depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated function ${name}`);
}

const CATEGORY_NAMES = {};
const CATEGORY_CODES_REVERSE = {};
const CATEGORY_META_BY_CODE = {};
const CATEGORY_META_BY_SLUG = {};
let DEFAULT_CATEGORY_CODE = 'oth';
eval(extract(artifactApi, 'requireExactFields'));
eval(extract(artifactApi, 'requireSchemaOne'));
eval(extract(artifactApi, 'requireNonNegativeInteger'));
eval(extract(artifactApi, 'validateCategoryTaxonomy'));
eval(extract(app, 'normalizeCategoryCode'));
eval(extract(app, 'configureCategoryTaxonomy'));
eval(extract(app, 'categoryDisplayName'));
eval(extract(app, 'categoryReportingLabel'));

validateCategoryTaxonomy(payload);
configureCategoryTaxonomy(payload);
for (const category of payload.categories) {
  assert.strictEqual(normalizeCategoryCode(category.slug), category.code);
  assert.strictEqual(normalizeCategoryCode(category.code), category.code);
  assert.strictEqual(categoryDisplayName(category.slug), category.display_name);
}
assert.strictEqual(normalizeCategoryCode('future-category'), 'future-category');
assert.strictEqual(categoryDisplayName('future-category'), 'future-category');
assert.strictEqual(normalizeCategoryCode(''), payload.default_code);
const child = payload.categories.find(category => category.parent);
const parent = payload.categories.find(category => category.slug === child.parent);
assert.strictEqual(
  categoryReportingLabel(child.code),
  `${parent.display_name} › ${child.display_name}`
);

const duplicate = structuredClone(payload);
duplicate.categories[1].code = duplicate.categories[0].code;
assert.throws(() => validateCategoryTaxonomy(duplicate), /identity mismatch/);
const truncated = structuredClone(payload);
truncated.categories = truncated.categories.slice(0, 1);
assert.throws(() => validateCategoryTaxonomy(truncated), /count or identity mismatch/);
const extraCategory = structuredClone(payload);
extraCategory.categories.push({
  slug: 'future-root', code: 'future-root', display_name: 'Future', parent: ''
});
extraCategory.category_count = extraCategory.categories.length;
validateCategoryTaxonomy(extraCategory);
const noncanonical = structuredClone(payload);
noncanonical.categories[0].slug = `${noncanonical.categories[0].slug} `;
assert.throws(() => validateCategoryTaxonomy(noncanonical), /identity mismatch/);
const deep = structuredClone(payload);
const childIndex = deep.categories.findIndex(category => category.parent);
const secondChildIndex = deep.categories.findIndex(
  (category, index) => category.parent && index !== childIndex
);
deep.categories[secondChildIndex].parent = deep.categories[childIndex].slug;
assert.throws(() => validateCategoryTaxonomy(deep), /parent mismatch/);
const extraRoot = structuredClone(payload);
extraRoot.categories[childIndex].parent = '';
extraRoot.category_count = extraRoot.categories.length;
validateCategoryTaxonomy(extraRoot);
const unknownField = structuredClone(payload);
unknownField.extra = true;
assert.throws(() => validateCategoryTaxonomy(unknownField), /shape mismatch/);

process.stdout.write(JSON.stringify({
  count: payload.category_count,
  roots: payload.categories.filter(category => !category.parent).length,
  unknown: normalizeCategoryCode('future-category')
}));
""",
        json.dumps(contract),
    )
    assert result == {"count": 40, "roots": 12, "unknown": "future-category"}


def test_github_url_and_html_escaping_contracts():
    result = run_node_harness(
        r"""
const fs = require('fs');
const assert = require('assert');
const render = fs.readFileSync('docs/js/app-render.js', 'utf8');
const index = fs.readFileSync('docs/index.html', 'utf8');

function extract(source, name) {
  const start = source.indexOf(`function ${name}(`);
  assert(start >= 0, `missing function ${name}`);
  const bodyStart = source.indexOf('{', start);
  let depth = 0;
  let quote = null;
  let escaped = false;
  for (let i = bodyStart; i < source.length; i += 1) {
    const char = source[i];
    if (quote) {
      if (escaped) escaped = false;
      else if (char === '\\') escaped = true;
      else if (char === quote) quote = null;
      continue;
    }
    if (char === "'" || char === '"' || char === '`') quote = char;
    else if (char === '{') depth += 1;
    else if (char === '}') {
      depth -= 1;
      if (depth === 0) return source.slice(start, i + 1);
    }
  }
  throw new Error(`unterminated function ${name}`);
}

eval(extract(render, 'getGitHubUrl'));
eval(extract(render, 'escapeHtml'));
eval(extract(render, 'createSkillCard'));

assert.strictEqual(
  getGitHubUrl('facebook/react/.claude/skills/fix/SKILL.md', 'main'),
  'https://github.com/facebook/react/blob/main/.claude/skills/fix/SKILL.md'
);
assert.strictEqual(
  getGitHubUrl('facebook/react/.claude/skills/fix', 'main'),
  'https://github.com/facebook/react/blob/main/.claude/skills/fix/SKILL.md'
);
assert.strictEqual(
  getGitHubUrl('acme/demo', 'main'),
  'https://github.com/acme/demo/blob/main/SKILL.md'
);
assert.strictEqual(escapeHtml(`<img src=x onerror=alert(1)>`), '&lt;img src=x onerror=alert(1)&gt;');
assert.strictEqual(escapeHtml(`foo'"bar`), 'foo&#39;&quot;bar');
const hostileUrl = getGitHubUrl(
  `acme/demo/path" onmouseover="alert(1)`,
  `main" onmouseover="alert(1)`
);
assert(!hostileUrl.includes('"'));
assert(hostileUrl.includes('%22'));
const state = { favorites: [] };
const categoryDisplayName = value => value;
const hostileCard = createSkillCard({
  n: 'demo', d: 'safe', c: 'development',
  g: [`</span><img src=x onerror=alert(1)>`], r: 0, i: 'acme/demo'
}, false, false);
assert(!hostileCard.includes('<img'));
assert(render.includes('escapeHtml(getGitHubUrl('));
assert(!render.includes("copyInstall(event, '${"));
assert(!render.includes("toggleFavorite(event, '${"));
assert(!index.includes('Official (Anthropic)'));
assert(!index.includes('id="stat-official"'));
process.stdout.write(JSON.stringify({ ok: true }));
"""
    )
    assert result == {"ok": True}

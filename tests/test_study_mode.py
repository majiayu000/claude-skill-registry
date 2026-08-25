import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run_node(script: str) -> dict:
    completed = subprocess.run(
        ["node", "-e", script],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode:
        raise AssertionError(completed.stderr)
    return json.loads(completed.stdout)


def test_study_recorder_requires_consent_and_excludes_raw_search_text():
    result = run_node(
        r"""
const assert = require('assert');
const study = require('./docs/js/study-mode.js');
const values = new Map();
const storage = {
  getItem: key => values.get(key) || null,
  setItem: (key, value) => values.set(key, value),
  removeItem: key => values.delete(key)
};
let currentTime = 1000;
const recorder = study.createRecorder({
  storage,
  now: () => currentTime,
  isoNow: () => `time-${currentTime}`,
  makeId: () => 'participant-session'
});

assert.strictEqual(recorder.track('search_submitted', {}), false);
assert.strictEqual(study.normalizeCohort('2026Q3'), '2026q3');
recorder.start('alice@example.com');
assert.strictEqual(recorder.isActive(), true);
assert.strictEqual(recorder.track('unknown_event', {}), false);
assert.strictEqual(recorder.track('search_submitted', {
  query_length_bucket: study.bucketQueryLength('private search text'),
  result_count_bucket: study.bucketResultCount(42),
  source: 'enter',
  query_text: 'private search text'
}), true);
currentTime = 2500;
assert.strictEqual(recorder.track('skill_detail_opened', {
  skill_install: 'owner/repo/path',
  source_view: 'search',
  referrer: 'https://private.example'
}), true);

const summary = recorder.finish();
assert.strictEqual(summary.active, false);
assert.strictEqual(summary.started_ms, undefined);
assert.strictEqual(summary.cohort, '');
assert.strictEqual(summary.events[0].elapsed_ms, 0);
assert.strictEqual(summary.events[1].elapsed_ms, 1500);
assert.strictEqual(summary.events[0].details.query_text, undefined);
assert.strictEqual(summary.events[1].details.referrer, undefined);
assert.strictEqual(JSON.stringify(summary).includes('private search text'), false);
assert.strictEqual(recorder.track('github_opened', {}), false);
console.log(JSON.stringify(summary));
"""
    )

    assert result["schema_version"] == 1
    assert [event["name"] for event in result["events"]] == [
        "search_submitted",
        "skill_detail_opened",
    ]


def test_study_mode_is_query_gated_and_has_no_network_sender():
    html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    source = (ROOT / "docs" / "js" / "study-mode.js").read_text(encoding="utf-8")

    assert '<script src="js/study-mode.js"></script>' in html
    assert 'id="study-panel"' in html
    assert "params.get('study') !== '1'" in source
    assert "fetch(" not in source
    assert "XMLHttpRequest" not in source
    assert "query_text" not in source
    assert "userAgent" not in source
    assert "document.referrer" not in source


def test_browser_study_tracks_automatic_search_and_random_without_plugin_misattribution():
    result = run_node(
        r"""
const assert = require('assert');

function makeClassList(initial = []) {
  const values = new Set(initial);
  return {
    add: value => values.add(value),
    remove: value => values.delete(value),
    contains: value => values.has(value)
  };
}

function makeControl(id, classes = []) {
  const listeners = {};
  return {
    id,
    disabled: false,
    textContent: '',
    classList: makeClassList(classes),
    addEventListener(type, handler) { listeners[type] = handler; },
    listeners
  };
}

const controls = {
  'study-panel': makeControl('study-panel', ['hidden']),
  'study-start': makeControl('study-start'),
  'study-finish': makeControl('study-finish'),
  'study-download': makeControl('study-download'),
  'study-status': makeControl('study-status'),
  'result-count': makeControl('result-count'),
  'search-results': makeControl('search-results'),
  'skill-modal': makeControl('skill-modal', ['hidden'])
};
controls['result-count'].textContent = '42 results';

const documentHandlers = {};
let openedInstall = '';
const fakeDocument = {
  activeElement: { id: '' },
  getElementById: id => controls[id] || null,
  querySelector(selector) {
    if (selector === '.nav-tab.active') return { dataset: { view: 'featured' } };
    if (selector === '#modal-body .install-cmd span:not(.prefix)' && openedInstall) {
      return { textContent: `sk install ${openedInstall}` };
    }
    return null;
  },
  addEventListener(type, handler) {
    documentHandlers[type] = handler;
  },
  createElement() { return { click() {} }; }
};

const stored = new Map();
let resolveClipboard;
let nextTimerId = 1;
const timers = new Map();
const fakeWindow = {
  document: fakeDocument,
  location: { search: '?study=1&cohort=2026q3' },
  sessionStorage: {
    getItem: key => stored.get(key) || null,
    setItem: (key, value) => stored.set(key, value),
    removeItem: key => stored.delete(key)
  },
  crypto: { randomUUID: () => 'browser-session' },
  navigator: {
    clipboard: {
      writeText: () => new Promise(resolve => { resolveClipboard = resolve; })
    }
  },
  setTimeout(handler, delay) {
    const id = nextTimerId++;
    timers.set(id, { handler, delay, cancelled: false });
    return id;
  },
  clearTimeout(id) {
    if (timers.has(id)) timers.get(id).cancelled = true;
  }
};
global.window = fakeWindow;

function flushTimers() {
  const queued = [...timers.values()].sort((a, b) => a.delay - b.delay);
  timers.clear();
  queued.forEach(timer => {
    if (!timer.cancelled) timer.handler();
  });
}

const study = require('./docs/js/study-mode.js');
fakeWindow.showSkillDetail = card => {
  if (card.dataset.install !== 'owner/unavailable') openedInstall = card.dataset.install;
};
documentHandlers.DOMContentLoaded();

const searchTarget = { id: 'search-input', value: 'before consent' };
documentHandlers.input({ target: searchTarget });
controls['study-start'].listeners.click();
flushTimers();
assert.strictEqual(controls['study-download'].disabled, true);

searchTarget.value = 'security';
documentHandlers.input({ target: searchTarget });
flushTimers();
documentHandlers.keydown({ key: 'Enter', target: searchTarget });
flushTimers();

fakeWindow.showSkillDetail({ dataset: { install: 'owner/unavailable' } });

const randomTarget = {
  closest: selector => selector === '#random-btn' ? randomTarget : null
};
documentHandlers.click({ target: randomTarget });
flushTimers();
fakeWindow.showSkillDetail({ dataset: { install: 'owner/ordinary-skill' } });

documentHandlers.keydown({ key: 'r', target: { id: '' } });
fakeWindow.showSkillDetail({ dataset: { install: 'owner/keyboard-random-skill' } });
flushTimers();

documentHandlers.click({ target: randomTarget });
fakeWindow.showSkillDetail({ dataset: { install: 'owner/random-skill' } });
flushTimers();
assert.strictEqual(openedInstall, 'owner/random-skill');

const modalCopyTarget = {
  closest(selector) {
    if (selector === '.copy-btn') return modalCopyTarget;
    return null;
  }
};
documentHandlers.click({ target: modalCopyTarget });

const modalGitHubTarget = {
  closest: selector => selector === '#modal-body a[href*="github.com/"]'
    ? modalGitHubTarget
    : null
};
documentHandlers.click({ target: modalGitHubTarget });

const pluginCard = {};
const pluginCopyTarget = {
  closest(selector) {
    if (selector === '.copy-btn') return pluginCopyTarget;
    if (selector === '.plugin-card') return pluginCard;
    return null;
  }
};
documentHandlers.click({ target: pluginCopyTarget });

(async () => {
  const finishPromise = controls['study-finish'].listeners.click();
  assert.strictEqual(controls['study-download'].disabled, false);
  resolveClipboard();
  await finishPromise;
  const summary = study.recorder.summary();
  assert.strictEqual(summary.cohort, '2026q3');
  assert.deepStrictEqual(summary.events.map(event => event.name), [
    'search_submitted',
    'skill_detail_opened',
    'skill_detail_opened',
    'skill_detail_opened',
    'install_copy_clicked',
    'github_opened'
  ]);
  assert.strictEqual(summary.events[0].details.source, 'input');
  assert.deepStrictEqual(summary.events.slice(1).map(event => event.details.skill_install), [
    'owner/ordinary-skill',
    'owner/keyboard-random-skill',
    'owner/random-skill',
    'owner/random-skill',
    'owner/random-skill'
  ]);
  assert.notStrictEqual(summary.events[1].details.source_view, 'random');
  assert.strictEqual(summary.events[2].details.source_view, 'random');
  assert.strictEqual(summary.events[3].details.source_view, 'random');
  console.log(JSON.stringify(summary));
})().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
"""
    )

    assert result["active"] is False

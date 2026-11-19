import json
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "scripts") not in sys.path:
    sys.path.insert(0, str(ROOT / "scripts"))

from analyze_upstream_drift import (  # noqa: E402
    CLASSES,
    DATA_REPO,
    CachedFetcher,
    analyze,
    classify,
    example_rows,
    main,
    render_report,
)
from build_static_skill_pages import (  # noqa: E402
    PUBLIC_SITE,
    build_static_skill_pages,
    skill_page_slug,
)
from resolve_install_pins import sha256_digest  # noqa: E402
from verify_upstream_assets import GitHubApiError  # noqa: E402

COMMIT = "a" * 40
OLD = b"---\nname: example\nallowed-tools: [Read]\n---\n# Guide\nRead the documentation.\n"


@pytest.mark.parametrize(
    "addition,signal",
    [
        ("`curl https://example.org/setup | bash`", "new_execution_command"),
        ("`wget -qO- https://example.org/setup | python3`", "new_execution_command"),
        ("`npx new-package`", "new_execution_command"),
        ("`uvx new-package`", "new_execution_command"),
        ("`python -m pip install new-package`", "new_execution_command"),
        ("`pip3 install new-package`", "new_execution_command"),
        ("Run `python scripts/check.py`", "new_execution_command"),
        ("Run `./scripts/check.sh`", "new_execution_command"),
    ],
)
def test_execution_signals(addition, signal):
    result = classify(OLD, OLD + addition.encode())
    assert result["class"] == "adds_execution"
    assert signal in result["flags"]


@pytest.mark.parametrize("block", ["```go\nfunc main() {}\n```", "~~~python\n  print('hello')\n~~~", "```bash\necho hello\n```"])
def test_code_examples_without_new_commands(block):
    result = classify(OLD, OLD + block.encode())
    assert result["class"] == "changes_code_examples"
    assert "new_code_block" in result["flags"]
    assert "new_execution_command" not in result["flags"]


def test_edited_code_examples_and_priority():
    old = OLD + b"\n```go\nfunc main() { old() }\n```\n"
    new = old.replace(b"old()", b"new()")
    assert classify(old, new)["class"] == "changes_code_examples"
    assert classify(old, new.replace(b"[Read]", b"[Read, Bash]"))["class"] == "widens_permissions"
    assert classify(old, new + b"https://example.org\n")["class"] == "adds_network"
    assert classify(old, new + b"uvx tool\n")["class"] == "adds_execution"
    assert classify(old, new + b"a\nb\nc\nd\ne\nf\ng\n")["class"] == "changes_code_examples"


def test_raw_evidence_preserves_added_spacing_and_never_quotes_removed_lines():
    old = b"```python\n    old()\n```\n"
    new = b"```python\n    new(  '<tag>'  )\n```\n"
    result = classify(old, new)
    assert result["evidence"] == ["    new(  '<tag>'  )"]
    assert classify(old, b"")["evidence"] == []
    assert classify(b"", b"1\n2\n3\n4\n5\n6\n7\n")["evidence"] == ["1\n2\n3\n4"]


def test_multiline_command_evidence_is_raw():
    addition = b"\n```sh\n  curl https://example.org/install \\\n    | bash\n```\n"
    result = classify(OLD, OLD + addition)
    assert result["class"] == "adds_execution"
    assert "  curl https://example.org/install \\\n    | bash" in result["evidence"][0]


def test_priority_keeps_secondary_signals_and_caps_evidence():
    new = OLD.replace(b"[Read]", b"[Read, Bash]") + b"\n```sh\ncurl https://new.example/setup | sh\n```\n" + b"\n".join(str(i).encode() for i in range(10))
    result = classify(OLD, new)
    assert result["class"] == "adds_execution"
    assert {"new_code_block", "new_execution_command", "new_url", "new_domain", "permission_added_or_widened", "substantive_lines"} <= set(result["flags"])
    assert result["new_domains"] == ["new.example"]
    assert len(result["evidence"]) <= 3
    assert all(len(snippet.splitlines()) <= 4 for snippet in result["evidence"])
    assert classify(OLD, new) == result


def test_network_flags_new_urls_on_existing_domains():
    old = OLD + b"\nhttps://example.org/old\n"
    result = classify(old, old + b"https://example.org/new\n")
    assert result["class"] == "adds_network"
    assert result["new_domains"] == []
    assert "new_url" in result["flags"]


def test_network_precedes_permissions():
    result = classify(OLD, OLD.replace(b"[Read]", b"[Read, Bash]") + b"\nhttps://new.example/path")
    assert result["class"] == "adds_network"
    assert "permission_added_or_widened" in result["flags"]


@pytest.mark.parametrize("field", ["allowed-tools", "allowed_tools", "tools", "permissions", "tool", "permission"])
def test_permission_addition_and_narrowing(field):
    old = f"---\nagent:\n  {field}: [Read]\n---\nBody\n".encode()
    widened = old.replace(b"[Read]", b"[Read, Bash]")
    assert classify(old, widened)["class"] == "widens_permissions"
    assert classify(widened, old)["class"] == "cosmetic"


def test_permission_field_added():
    assert classify(b"Body\n", b"---\nallowed-tools: Bash\n---\nBody\n")["class"] == "widens_permissions"


def test_boolean_permission_grants_and_revocations():
    old = b"---\npermissions: {read: true, write: false}\n---\nBody\n"
    new = old.replace(b"write: false", b"write: true")
    assert classify(old, new)["class"] == "widens_permissions"
    assert classify(new, old)["class"] == "cosmetic"


def test_loopback_urls_are_not_external_network_additions():
    assert classify(OLD, OLD + b"http://localhost:3000/test\n")["class"] == "cosmetic"


def test_relative_document_links_are_not_script_execution():
    result = classify(OLD, OLD + b"\n[Read the guide](./docs/guide.md)\nSee `./settings.yaml`\n")
    assert result["class"] == "cosmetic"
    assert "new_execution_command" not in result["flags"]


def test_identical_bytes_are_explicit_within_cosmetic():
    result = classify(OLD, OLD)
    assert result["class"] == "cosmetic"
    assert "identical_bytes" in result["flags"]
    assert result["lines_added"] == result["lines_removed"] == 0


def test_substantive_threshold_is_strictly_more_than_six():
    assert classify(b"", b"1\n2\n3\n4\n5\n6\n")["class"] == "cosmetic"
    assert classify(b"", b"1\n2\n3\n4\n5\n6\n7\n")["class"] == "instructions_changed"


def test_formatting_and_tiny_edits_are_cosmetic_with_real_line_counts():
    old = b"# Heading\n\nA **guide**\n"
    result = classify(old, b"## Heading\nA guide  \n")
    assert result["class"] == "cosmetic"
    assert result["changed_body_lines"] == 0
    assert result["lines_added"] == 2
    assert result["lines_removed"] == 3
    assert classify(b"teh", b"the")["class"] == "cosmetic"


def test_paragraph_reflow_is_cosmetic_even_with_many_raw_changed_lines():
    old = ("A long paragraph with many words. " * 12).encode()
    new = old.replace(b" with many", b"\nwith many")
    result = classify(old, new)
    assert result["class"] == "cosmetic"
    assert result["changed_body_lines"] == 0
    assert result["lines_added"] > 6


def test_existing_execution_and_network_do_not_retrigger_on_formatting():
    old = b"```bash\nnpx example\n```\nhttps://example.org\n"
    result = classify(old, old.replace(b"npx example", b"npx   example") + b"A tiny edit\n")
    assert result["class"] == "cosmetic"
    assert "new_execution_command" not in result["flags"]
    assert "new_url" not in result["flags"]


def test_unparseable_frontmatter_is_visible():
    result = classify(OLD, b"---\nallowed-tools: [\n---\nBody\n")
    assert "frontmatter_unparsed" in result["flags"]


class FakeFetcher:
    def __init__(self):
        self.files, self.heads, self.repos, self.calls = {}, {}, {}, []

    def head(self, repo, branch):
        self.calls.append(("head", repo, branch))
        value = self.heads.get((repo, branch), COMMIT)
        if isinstance(value, Exception):
            raise value
        return value

    def api(self, path):
        self.calls.append(("api", path))
        value = self.repos.get(path, {})
        if isinstance(value, Exception):
            raise value
        return value

    def raw(self, repo, commit, path):
        self.calls.append(("raw", repo, commit, path))
        value = self.files.get((repo, path), GitHubApiError(404, "HTTP 404"))
        if isinstance(value, Exception):
            raise value
        return value

    tree = CachedFetcher.tree


def add_skill(fetcher, pins, key, *, status="upstream_changed", repo="acme/repo", current=OLD, archived=OLD):
    archive = f"tools/{key}/SKILL.md"
    pins[key] = {"status": status, "archive_path": archive, "digest": sha256_digest(OLD), "checked_at": "2026-10-17T00:00:00+00:00"}
    # Unavailable pins really omit repo/branch. Metadata supplies both.
    if status == "upstream_changed":
        pins[key].update(repo=repo, branch="main")
    fetcher.files[(DATA_REPO, archive.rsplit("/", 1)[0] + "/metadata.json")] = json.dumps(
        {"repo": repo, "github_path": f"skills/{key}", "github_branch": "main", "name": key}
    ).encode()
    fetcher.files[(DATA_REPO, archive)] = archived
    fetcher.files[(repo, f"skills/{key}/SKILL.md")] = current


def test_aggregation_keeps_every_skill_and_separates_failure_types():
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "code", current=OLD + b"\n`uvx example`")
    add_skill(fetcher, pins, "missing", current=GitHubApiError(404, "HTTP 404"))
    add_skill(fetcher, pins, "failed", current=GitHubApiError(500, "HTTP 500"))
    add_skill(fetcher, pins, "digest", archived=b"different archive bytes")
    add_skill(fetcher, pins, "repo-gone", status="upstream_unavailable", repo="gone/repo")
    add_skill(fetcher, pins, "branch-gone", status="upstream_unavailable", repo="gone/branch")
    add_skill(fetcher, pins, "back", status="upstream_unavailable")
    add_skill(fetcher, pins, "limited", status="upstream_unavailable", repo="limited/repo")
    fetcher.heads[("gone/repo", "main")] = GitHubApiError(404, "Not Found")
    fetcher.heads[("gone/branch", "main")] = GitHubApiError(404, "Branch not found")
    fetcher.heads[("limited/repo", "main")] = GitHubApiError(403, "API rate limit exceeded")
    fetcher.repos["/repos/gone/repo"] = GitHubApiError(404, "Not Found")
    fetcher.repos[f"/repos/acme/repo/git/trees/{COMMIT}?recursive=1"] = {"truncated": False, "tree": []}
    catalog = {"code": {"id": "code", "name": "Execute example", "page_identity": "stable"}}

    data = analyze(pins, {}, fetcher, workers=3, catalog=catalog)

    counts = data["summary"]["class_counts"]
    assert counts == {key: {"adds_execution": 1, "removed": 1, "fetch_failed": 2}.get(key, 0) for key in CLASSES}
    assert sum(counts.values()) == data["summary"]["changed_total"] == 4
    assert data["summary"]["unavailable_reasons"] == {"repo_404": 1, "branch_not_found": 1, "other": 1, "available_now": 1}
    assert data["summary"]["failure_count"] == 3
    assert len(data["skills"]) + len(data["unavailable"]) == len(pins)
    code = next(row for row in data["skills"] if row["id"] == "code")
    assert code["guide_url"] == f"{PUBLIC_SITE}skills/{skill_page_slug(catalog['code'])}/"
    assert COMMIT in code["upstream_url"]
    assert "skills/code/SKILL.md" in code["upstream_url"]
    assert Counter(call for call in fetcher.calls if call[0] == "head")[("head", "acme/repo", "main")] == 1
    assert all("_archived" not in row for row in data["skills"])


def test_missing_metadata_and_upstream_rate_limit_are_explicit_failures():
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "metadata")
    del fetcher.files[(DATA_REPO, "tools/metadata/metadata.json")]
    add_skill(fetcher, pins, "limited", repo="limited/repo")
    fetcher.heads[("limited/repo", "main")] = GitHubApiError(429, "Rate limit")
    data = analyze(pins, {}, fetcher, workers=1)
    assert data["summary"]["class_counts"]["fetch_failed"] == 2
    assert data["summary"]["failure_count"] == 2
    assert all(row.get("reason") for row in data["skills"])


def test_unavailable_checks_do_not_require_a_source_path_or_guess_a_branch():
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "no-path", status="upstream_unavailable")
    fetcher.files[(DATA_REPO, "tools/no-path/metadata.json")] = b'{"repo":"acme/repo","github_branch":"main"}'
    add_skill(fetcher, pins, "no-branch", status="upstream_unavailable", repo="gone/repo")
    fetcher.files[(DATA_REPO, "tools/no-branch/metadata.json")] = b'{"repo":"gone/repo"}'
    fetcher.repos["/repos/gone/repo"] = GitHubApiError(404, "gone")
    data = analyze(pins, {}, fetcher, workers=1)
    assert data["summary"]["unavailable_reasons"] == {"repo_404": 1, "branch_not_found": 0, "other": 0, "available_now": 1}
    assert data["summary"]["failure_count"] == 0
    assert all(row["metadata_error"] == "missing_source_path" for row in data["unavailable"])
    assert fetcher.calls.count(("api", "/repos/gone/repo")) == 1
    assert ("head", "gone/repo", "main") not in fetcher.calls


def missing_skill_tree(fetcher, paths):
    fetcher.repos[f"/repos/acme/repo/git/trees/{COMMIT}?recursive=1"] = {
        "truncated": False, "tree": [{"type": "blob", "path": path} for path in paths],
    }


@pytest.mark.parametrize("match", ["directory", "frontmatter"])
def test_missing_path_is_moved_by_archived_directory_or_frontmatter_name(match):
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=GitHubApiError(404, "gone"))
    # The archive directory, rather than the old upstream directory, is the rule.
    metadata_path = (DATA_REPO, "tools/example/metadata.json")
    metadata = json.loads(fetcher.files[metadata_path])
    metadata["github_path"] = "old/different"
    fetcher.files[metadata_path] = json.dumps(metadata).encode()
    path = "new/example/SKILL.md" if match == "directory" else "new/renamed/SKILL.md"
    missing_skill_tree(fetcher, [path])
    fetcher.files[("acme/repo", path)] = OLD + b"\n  uvx new-tool\n"
    data = analyze(pins, {}, fetcher, workers=2)
    row = data["skills"][0]
    assert row["class"] == "moved"
    assert row["moved_change_class"] == "adds_execution"
    assert row["moved_path"] == row["upstream_path"] == path
    assert row["original_upstream_path"] == "old/different/SKILL.md"
    assert row["upstream_url"].endswith(f"/{COMMIT}/{path}")
    assert row["archive_url"].endswith(f"/{COMMIT}/tools/example/SKILL.md")
    assert row["evidence"] == ["  uvx new-tool"]
    assert data["summary"]["failure_count"] == 0
    assert "_archived" not in row


def test_complete_tree_without_matching_directory_or_name_is_removed():
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=GitHubApiError(404, "gone"))
    path = "new/unrelated/SKILL.md"
    missing_skill_tree(fetcher, [path, "docs/README.md"])
    fetcher.files[("acme/repo", path)] = b"---\nname: unrelated\n---\nGuide\n"
    data = analyze(pins, {}, fetcher, workers=1)
    assert data["skills"][0]["class"] == "removed"
    assert data["summary"]["failure_count"] == 0
    assert ("raw", "acme/repo", COMMIT, "docs/README.md") not in fetcher.calls


@pytest.mark.parametrize("tree", [GitHubApiError(403, "No token / rate limit"), {"truncated": True, "tree": []}, {}, {"truncated": False, "tree": [{}]}])
def test_missing_path_remains_unchecked_when_tree_unavailable_or_incomplete(tree):
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=GitHubApiError(404, "gone"))
    fetcher.repos[f"/repos/acme/repo/git/trees/{COMMIT}?recursive=1"] = tree
    data = analyze(pins, {}, fetcher, workers=1)
    row = data["skills"][0]
    assert row["class"] == "path_missing_unchecked"
    assert "unchecked" in row["reason"]
    assert "_archived" not in row
    assert data["summary"]["failure_count"] == 1


@pytest.mark.parametrize("content", [GitHubApiError(429, "rate limit"), b"---\nname: [\n---\n", b"\xff"])
def test_failed_frontmatter_search_never_assumes_removal(content):
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=GitHubApiError(404, "gone"))
    path = "new/renamed/SKILL.md"
    missing_skill_tree(fetcher, [path])
    fetcher.files[("acme/repo", path)] = content
    data = analyze(pins, {}, fetcher, workers=1)
    assert data["skills"][0]["class"] == "path_missing_unchecked"
    assert "incomplete" in data["skills"][0]["reason"]


def test_tree_and_candidate_files_are_shared_and_directory_match_precedes_name():
    fetcher, pins = FakeFetcher(), {}
    for key in ("one", "two", "three"):
        add_skill(fetcher, pins, key, current=GitHubApiError(404, "gone"))
    paths = ["b/one/SKILL.md", "a/one/SKILL.md", "new/unrelated/SKILL.md"]
    missing_skill_tree(fetcher, paths)
    for path in paths:
        fetcher.files[("acme/repo", path)] = OLD
    data = analyze(pins, {}, fetcher, workers=3)
    rows = {row["id"]: row for row in data["skills"]}
    assert rows["one"]["moved_path"] == "a/one/SKILL.md"
    assert all(row["class"] == "moved" for row in rows.values())
    assert all(row["moved_change_class"] == "cosmetic" for row in rows.values())
    assert fetcher.calls.count(("api", f"/repos/acme/repo/git/trees/{COMMIT}?recursive=1")) == 1
    assert all(fetcher.calls.count(("raw", "acme/repo", COMMIT, path)) == 1 for path in paths)


def test_moved_file_comparison_failure_preserves_move_and_failure_contract():
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=GitHubApiError(404, "gone"))
    missing_skill_tree(fetcher, ["new/example/SKILL.md"])
    data = analyze(pins, {}, fetcher, workers=1)
    row = data["skills"][0]
    assert row["class"] == "moved"
    assert row["moved_change_class"] == "fetch_failed"
    assert row["reason"]
    assert data["summary"]["failure_count"] == 1


def test_tree_response_is_cached_using_github_client(tmp_path, monkeypatch):
    fetcher = CachedFetcher(tmp_path, "not-a-real-token")
    paths = []

    def get_json(path):
        paths.append(path)
        return {"truncated": False, "tree": [{"type": "blob", "path": "new/example/SKILL.md"}]}

    monkeypatch.setattr(fetcher.client, "get_json", get_json)
    assert fetcher.tree("acme/repo", COMMIT) == ["new/example/SKILL.md"]
    assert fetcher.tree("acme/repo", COMMIT) == ["new/example/SKILL.md"]
    assert paths == [f"/repos/acme/repo/git/trees/{COMMIT}?recursive=1"]
    assert all("not-a-real-token" not in path.read_text() for path in tmp_path.glob("*.json"))


def test_cache_only_never_calls_uncached_network(tmp_path):
    fetcher = CachedFetcher(tmp_path, "", cache_only=True)
    with pytest.raises(GitHubApiError, match="Not cached"):
        fetcher._cached("missing", lambda: pytest.fail("network called"))


@pytest.mark.parametrize("token", [None, "not-a-real-token"])
def test_cli_uses_only_environment_token(tmp_path, monkeypatch, token):
    if token is None:
        monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    else:
        monkeypatch.setenv("GITHUB_TOKEN", token)
    pins = tmp_path / "pins.json"
    pins.write_text('{"pins": {}}')
    history = tmp_path / "history.json"
    history.write_text('{"schema_version": 1, "skills": {}}')
    observed_tokens = []

    def fetcher(cache, token, **kwargs):
        observed_tokens.append(token)
        return FakeFetcher()

    monkeypatch.setattr("analyze_upstream_drift.CachedFetcher", fetcher)
    monkeypatch.setattr(sys, "argv", ["analyze_upstream_drift.py", "--pins", str(pins), "--history", str(history),
                                     "--output", str(tmp_path / "output"), "--cache", str(tmp_path / "cache")])
    assert main() == 0
    assert observed_tokens == [token or ""]
    assert "not-a-real-token" not in (tmp_path / "output/data.json").read_text()


def test_cache_reuses_bytes_and_404_without_storing_token(tmp_path):
    fetcher = CachedFetcher(tmp_path, "not-a-real-token")
    calls = []

    def fetch():
        calls.append(True)
        return b"content"

    assert fetcher._cached("key", fetch) == b"content"
    assert fetcher._cached("key", fetch) == b"content"
    assert len(calls) == 1

    def missing():
        calls.append(False)
        raise GitHubApiError(404, "gone")

    for _ in range(2):
        with pytest.raises(GitHubApiError) as error:
            fetcher._cached("gone", missing, cache_404=True)
        assert error.value.status == 404
    assert calls == [True, False]
    assert all("not-a-real-token" not in path.read_text() for path in tmp_path.glob("*.json"))


def test_cache_retries_transients_but_does_not_cache_rate_limits(tmp_path, monkeypatch):
    fetcher = CachedFetcher(tmp_path, "")
    monkeypatch.setattr("analyze_upstream_drift.time.sleep", lambda seconds: None)
    attempts = []

    def failed():
        attempts.append(True)
        raise GitHubApiError(503, "temporarily unavailable")

    with pytest.raises(GitHubApiError):
        fetcher._cached("transient", failed)
    assert len(attempts) == 3
    assert not list(tmp_path.glob("*.json"))

    def limited():
        attempts.append(True)
        raise GitHubApiError(403, "rate limit exceeded")

    with pytest.raises(GitHubApiError):
        fetcher._cached("limited", limited)
    assert len(attempts) == 4
    assert not list(tmp_path.glob("*.json"))


def test_report_escapes_evidence_and_survives_repeated_site_builds(tmp_path):
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=OLD + b"\n```bash\necho '<script>alert(1)</script>'\n```\n")
    data = analyze(pins, {}, fetcher, workers=1)
    report = render_report(data)
    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in report
    assert "<script>alert(1)</script>" not in report
    assert 'rel="canonical"' in report
    assert 'application/ld+json' in report
    assert "data.json" in report
    assert "Changes code examples" in report
    assert "changes_code_examples" not in report
    assert "adds_execution" not in report
    assert "How we measured" in report
    assert "What this means for you" in report
    assert "<details>" in report
    # The report shares the site's dark theme and declares it so form controls match.
    assert "color-scheme:dark" in report
    assert 'class="site-header"' in report
    assert "overflow-x:auto" in report
    assert f"https://github.com/{DATA_REPO}/blob/{COMMIT}/tools/example/SKILL.md" in report
    assert "Deterministic primary order:" not in report
    assert "analysis failures" not in report
    output = tmp_path / "docs"
    report_path = output / "reports" / "skill-drift-2026-10" / "index.html"
    report_path.parent.mkdir(parents=True)
    report_path.write_text(report)
    (report_path.parent / "data.json").write_text(json.dumps(data))
    for _ in range(2):
        build_static_skill_pages([], output)
        assert report_path.read_text() == report
        sitemap = ElementTree.parse(output / "sitemap.xml")
        locations = [node.text for node in sitemap.findall("{*}url/{*}loc")]
        assert f"{PUBLIC_SITE}reports/skill-drift-2026-10/" in locations
        assert json.loads((report_path.parent / "data.json").read_text()) == data


def test_examples_cover_classes_prefer_moderate_diffs_and_use_raw_evidence():
    fetcher, pins = FakeFetcher(), {}
    variations = {
        "command": OLD + b"\n    uvx  new-tool\n",
        "network": OLD + b"\n  https://example.org/new\n",
        "permissions": OLD.replace(b"[Read]", b"[Read, Bash]"),
        "code": OLD + b"\n```go\n    func main() {}\n```\n",
        "instructions": OLD + b"\na\nb\nc\nd\ne\nf\ng\n",
        "small": OLD + b"\nNew text\n",
        "huge": OLD + b"\nuvx new-tool\n" + b"example\n" * 1900,
    }
    for key, content in variations.items():
        add_skill(fetcher, pins, key, current=content, repo=f"acme/{key}")
    data = analyze(pins, {}, fetcher, workers=1)
    examples = example_rows(data)
    assert 6 <= len(examples) <= 8
    assert {row["class"] for row in examples} == set(CLASSES[:6])
    assert next(row for row in examples if row["class"] == "adds_execution")["id"] == "command"
    report = render_report(data)
    assert "<pre><code>    uvx  new-tool" in report
    assert "<pre><code>  https://example.org/new" in report


def test_report_publishes_on_observation_date_and_exposes_move_subclass():
    fetcher, pins = FakeFetcher(), {}
    add_skill(fetcher, pins, "example", current=GitHubApiError(404, "gone"))
    missing_skill_tree(fetcher, ["new/example/SKILL.md"])
    fetcher.files[("acme/repo", "new/example/SKILL.md")] = OLD + b"\nuvx new-tool\n"
    data = analyze(pins, {}, fetcher, workers=1)
    data["observation_finished_at"] = "2026-10-21T00:00:00+00:00"
    report = render_report(data)
    assert '"datePublished": "2026-10-21"' in report
    assert "Moved within the repository" in report
    assert "Adds new commands to run" in report
    assert "new/example/SKILL.md" in report
    assert "moved_change_class" not in report


def test_truncated_api_body_is_retried_as_transient(tmp_path, monkeypatch):
    import http.client

    fetcher = CachedFetcher(tmp_path / "cache", "")
    calls = []

    def get_json(path):
        calls.append(path)
        if len(calls) == 1:
            raise http.client.IncompleteRead(b"{", 10)
        return {"truncated": False, "tree": []}

    monkeypatch.setattr(fetcher.client, "get_json", get_json)
    monkeypatch.setattr("analyze_upstream_drift.time.sleep", lambda _: None)

    assert fetcher.api("/repos/acme/skills/git/trees/abc?recursive=1") == {"truncated": False, "tree": []}
    assert len(calls) == 2


def test_persistent_transport_failure_surfaces_as_api_error(tmp_path, monkeypatch):
    fetcher = CachedFetcher(tmp_path / "cache", "")

    def get_json(path):
        raise OSError("connection reset")

    monkeypatch.setattr(fetcher.client, "get_json", get_json)
    monkeypatch.setattr("analyze_upstream_drift.time.sleep", lambda _: None)

    with pytest.raises(GitHubApiError, match="Transport failure"):
        fetcher.api("/repos/acme/skills/git/trees/abc?recursive=1")
    assert not list((tmp_path / "cache").glob("*.json"))


def test_truncated_raw_body_is_retried_and_cached(tmp_path, monkeypatch):
    import http.client
    from contextlib import nullcontext
    from unittest.mock import Mock

    fetcher = CachedFetcher(tmp_path / "cache", "")
    response = Mock()
    response.read.side_effect = [http.client.IncompleteRead(b"partial", 20), b"complete"]
    urlopen = Mock(side_effect=lambda *args, **kwargs: nullcontext(response))
    monkeypatch.setattr("analyze_upstream_drift.urllib.request.urlopen", urlopen)
    monkeypatch.setattr("analyze_upstream_drift.time.sleep", lambda _: None)

    assert fetcher.raw("acme/skills", COMMIT, "example/SKILL.md") == b"complete"
    assert fetcher.raw("acme/skills", COMMIT, "example/SKILL.md") == b"complete"
    assert urlopen.call_count == 2
    assert response.read.call_count == 2
    records = list((tmp_path / "cache").glob("*.json"))
    assert len(records) == 1
    assert bytes.fromhex(json.loads(records[0].read_text())["body"]) == b"complete"


def test_persistent_raw_truncation_is_not_cached(tmp_path, monkeypatch):
    import http.client
    from contextlib import nullcontext
    from unittest.mock import Mock

    fetcher = CachedFetcher(tmp_path / "cache", "")
    response = Mock()
    response.read.side_effect = http.client.IncompleteRead(b"partial", 20)
    urlopen = Mock(side_effect=lambda *args, **kwargs: nullcontext(response))
    monkeypatch.setattr("analyze_upstream_drift.urllib.request.urlopen", urlopen)
    monkeypatch.setattr("analyze_upstream_drift.time.sleep", lambda _: None)

    with pytest.raises(GitHubApiError, match="Transport failure") as error:
        fetcher.raw("acme/skills", COMMIT, "example/SKILL.md")
    assert error.value.status == 0
    assert isinstance(error.value.__cause__, http.client.IncompleteRead)
    assert urlopen.call_count == 3
    assert not list((tmp_path / "cache").glob("*.json"))

    response.read.side_effect = None
    response.read.return_value = b"recovered"
    assert fetcher.raw("acme/skills", COMMIT, "example/SKILL.md") == b"recovered"
    assert urlopen.call_count == 4

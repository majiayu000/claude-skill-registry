from pathlib import Path
from xml.etree import ElementTree

import yaml


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_SITE = "https://majiayu000.github.io/claude-skill-registry/"


def read_repo_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_homepage_declares_main_registry_as_its_public_identity():
    homepage = read_repo_file("docs/index.html")

    assert f'<link rel="canonical" href="{PUBLIC_SITE}">' in homepage
    assert '<meta property="og:type" content="website">' in homepage
    assert '<meta property="og:title" content="Claude Skills Registry">' in homepage
    assert f'<meta property="og:url" content="{PUBLIC_SITE}">' in homepage
    assert '<meta name="twitter:card" content="summary">' in homepage
    assert '<meta name="twitter:title" content="Claude Skills Registry">' in homepage


def test_robots_and_sitemap_publish_only_the_main_registry_url():
    robots = read_repo_file("docs/robots.txt")
    sitemap = ElementTree.fromstring(read_repo_file("docs/sitemap.xml"))
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locations = [node.text for node in sitemap.findall("sm:url/sm:loc", namespace)]

    assert robots == (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {PUBLIC_SITE}sitemap.xml\n"
    )
    assert locations == [PUBLIC_SITE]


def test_core_build_generates_artifacts_without_deploying_duplicate_pages():
    workflow_text = read_repo_file(".github/workflows/build-index.yml")
    workflow = yaml.safe_load(workflow_text)
    permissions = workflow["permissions"]
    step_uses = [
        step.get("uses", "")
        for job in workflow["jobs"].values()
        for step in job.get("steps", [])
    ]

    assert permissions["contents"] == "read"
    assert permissions["actions"] == "read"
    assert "pages" not in permissions
    assert "id-token" not in permissions
    assert "deploy-pages" not in workflow["jobs"]
    assert not any("configure-pages" in use for use in step_uses)
    assert not any("upload-pages-artifact" in use for use in step_uses)
    assert not any("deploy-pages" in use for use in step_uses)

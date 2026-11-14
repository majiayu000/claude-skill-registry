# First-wave skill guide observation

Keep the first wave at 5,800 guides until 2–4 weeks of real Search Console data
support expansion. No second wave or collection pages are approved by this
observation record alone.

## Public baseline, 2026-10-07

Source: https://majiayu000.github.io/claude-skill-registry/stats.json

- `updated_at`: `2026-10-07T06:44:23.905604Z`
- `independent_skill_count`: 172,272
- `static_skill_page_count`: 5,800
- `indexed_skill_count_scan_shape`: 269,371 source entries
- `registry_skill_count_dedup`: 268,939 registry entries

These numbers are a dated observation, not constants for future builds. The
README badge and site total read `independent_skill_count` from live stats.
The site's source entry counts are distinct from its independent-skill count.

## Search Console evidence

Property: `https://majiayu000.github.io/claude-skill-registry/`

Sitemap: `https://majiayu000.github.io/claude-skill-registry/sitemap.xml`

Verification and submission are managed separately by the coordinating chat.
The supplied verification file lives in `docs/google0b7c72b3675238a9.html`, so
core-to-main mirroring preserves it. Adding the file does not confirm ownership
verification, sitemap acceptance or indexing.

Start the observation window when the property has usable reporting. Record
actual data dates and export links, accounting for Search Console reporting
lag. Restrict performance measurements to detail URLs under `/skills/<slug>/`;
exclude the homepage, browse page and GitHub repository traffic.

| Observation | Reporting window | Indexed detail pages / current published guides | Detail impressions | Detail clicks | Evidence |
|---|---|---|---|---|---|
| Baseline | Awaiting Search Console reporting | Unknown / 5,800 | Unknown | Unknown | Pending export |
| Week 1 | Pending | Pending | Pending | Pending | Pending |
| Week 2 | Pending | Pending | Pending | Pending | Pending |
| Week 3 | Pending | Pending | Pending | Pending | Pending |
| Week 4 | Pending | Pending | Pending | Pending | Pending |

## Public crawl check, 2026-11-15 (Asia/Shanghai)

- The production sitemap returned HTTP 200 with `application/xml`. It parsed as
  a sitemap with 5,845 distinct HTTPS URLs, including 5,800 skill detail URLs.
  The site's published stats also reported 5,800 detail pages.
- The project robots.txt returned HTTP 200 and advertised the sitemap. The
  sampled documentation-updater guide returned HTTP 200, pointed its canonical
  tag to its clean detail URL, and had no observed `noindex` tag or header.
- The browser session reached the Search Console sign-in page. Current sitemap
  acceptance, Google coverage, impressions and clicks are still unverified.
  The HTTP checks above only verify the public crawl surface.

For [#429](https://github.com/majiayu000/claude-skill-registry-core/issues/429),
record the sitemap status and the Pages report for the existing URL-prefix
property. Export the performance report filtered to skill detail URLs and
compare it with site analytics before the 2026-11-26 decision. Keep these
owner-side measurements separate from the public crawl checks above.

## Search Console checkpoint, 2026-11-15 (Asia/Shanghai)

- The existing URL-prefix property reports “Couldn't fetch” for the full sitemap.
  Its detail page shows a last read on 2026-10-29 and zero discovered URLs.
- Page indexing data updated on 2026-11-09 shows one indexed URL, the homepage,
  and zero reported as not indexed.
- The unfiltered Web performance chart covers 2026-10-06 to 2026-11-11 and
  shows seven impressions and zero clicks for the property.

Submit `sitemap-probe.xml` after publication. It contains ten canonical URLs
selected from the same production sitemap. Compare Google's read status and
discovered count for the probe and the full sitemap before changing sitemap
structure.

Compare equal weekly windows. Record indexing coverage using the submitted
skill-guide sitemap URLs and indexing reports, not impressions as a substitute
for indexed pages. Search Console may show limited indexing examples; document
that limitation instead of claiming a complete per-URL count.

Expand only if indexed detail pages reach at least 50% of the currently
published guides, weekly impressions show sustained growth, and detail clicks
occur every week. Otherwise improve existing guide quality and continue
observing. If expansion is justified, recompute the eligible second-wave count
from the then-current grouped catalog and original quality/scan requirements;
do not reuse the historical estimate of 26,500 pages.

Production verification after this change: check both README badges, homepage
and statistics total against live independent count; inspect one matching-copy
group through search and detail shards; confirm all source links and the
verification URL survive a subsequent pinned publish. Record that publish's
core/data refs from `provenance/merge-source.json` with the observations.

import { get } from 'node:https';
import { relative } from 'node:path';
import process from 'node:process';
import { pathToFileURL } from 'node:url';

const DEFAULT_SOURCE_URL =
  'https://raw.gitcode.com/xixu-me/xget/raw/main/src/config/platform-catalog.js';
const DEFAULT_README_URL = 'https://raw.gitcode.com/xixu-me/xget/raw/main/README.md';

const DEFAULT_BASE_PLACEHOLDER = 'https://xget.example.com';
const DEFAULT_PUBLIC_BASE_URL = 'https://xget.xi-xu.me';
const DEFAULT_PUBLIC_HOST = 'xget.xi-xu.me';
const README_USE_CASES_HEADING = '## 🎯 Use Cases';
const MISSING_BASE_URL_HINT =
  `Missing --base-url and XGET_BASE_URL. Ask for the user's Xget base URL and whether ` +
  `to set it temporarily or persistently. For docs-only placeholders, use ${DEFAULT_BASE_PLACEHOLDER}.`;

const CRATES_API_PREFIX = '/api/v1/crates';

/**
 * @typedef {'resource' | 'registry' | 'inference'} PlatformCategory
 */

/**
 * @typedef {{ key: string, upstream: string, pathPrefix: string, category: PlatformCategory }} PlatformEntry
 */

/**
 * @typedef {{
 *   help?: boolean,
 *   format?: string,
 *   heading?: string,
 *   match?: string,
 *   url?: string,
 *   'source-url'?: string,
 *   'base-url'?: string,
 *   'readme-url'?: string,
 *   [key: string]: string | boolean | undefined
 * }} CliOptions
 */

/**
 * @typedef {{ command: string, options: CliOptions }} ParsedArgs
 */

/**
 * @typedef {{
 *   index: number,
 *   level: number,
 *   text: string,
 *   raw: string,
 *   parent: string | null
 * }} MarkdownHeading
 */

/**
 * @typedef {{
 *   section: string,
 *   heading: string,
 *   baseUrl: string,
 *   content: string
 * }} UseCasesSnippet
 */

function getInvocationCommand() {
  const scriptPath = process.argv[1];
  if (!scriptPath) {
    return 'node scripts/xget.mjs';
  }

  const relativePath = relative(process.cwd(), scriptPath).replace(/\\/g, '/');
  const displayPath =
    relativePath && !relativePath.startsWith('..') ? relativePath : scriptPath.replace(/\\/g, '/');

  return `node ${displayPath}`;
}

function printHelp() {
  const invocation = getInvocationCommand();

  console.log(`Usage: ${invocation} <command> [options]

Commands:
  platforms                 Fetch the live Xget platform map.
  convert                   Convert an upstream URL to an Xget URL.
  topics                    List headings from the README Use Cases section.
  snippet                   Fetch the README Use Cases section or a subsection.
  help                      Show this message.

Global options:
  --source-url URL          Override the remote platform source URL.
  --format FORMAT           json (default), text, or table when supported.
  --help                    Show command help.

platforms options:
  --format json|table

convert options:
  --base-url URL            Xget base URL. Defaults to XGET_BASE_URL.
  --url URL                 Upstream URL to convert.
  --format json|text

topics options:
  --readme-url URL          Override the remote README markdown URL.
  --match TEXT              Filter headings by case-insensitive text match.
  --format json|text

snippet options:
  --base-url URL            Xget base URL. Defaults to XGET_BASE_URL and
                            rewrites README examples to match it.
  --readme-url URL          Override the remote README markdown URL.
  --heading TEXT            Exact heading inside the Use Cases section.
  --match TEXT              Case-insensitive heading filter inside Use Cases.
  --format json|text

Examples:
  ${invocation} platforms --format table
  ${invocation} convert --base-url https://xget.example.com --url https://github.com/microsoft/vscode
  ${invocation} topics --match docker --format text
  ${invocation} snippet --base-url https://xget.example.com --heading "Docker Compose Configuration" --format text
`);
}

/**
 * @param {string[]} argv
 * @returns {ParsedArgs}
 */
function parseArgs(argv) {
  const [command = 'help', ...rest] = argv;
  if (command === '--help') {
    return { command: 'help', options: { help: true } };
  }

  /** @type {CliOptions} */
  const options = {};

  for (let index = 0; index < rest.length; index += 1) {
    const token = rest[index];
    if (!token.startsWith('--')) {
      fail(`Unexpected argument "${token}". Use --help for supported options.`, 2);
    }

    const key = token.slice(2);
    if (key === 'help') {
      options.help = true;
      continue;
    }

    const value = rest[index + 1];
    if (!value || value.startsWith('--')) {
      fail(`Missing value for --${key}.`, 2);
    }

    options[key] = value;
    index += 1;
  }

  return { command, options };
}

/**
 * @param {unknown} error
 * @returns {string}
 */
function getErrorMessage(error) {
  return error instanceof Error ? error.message : String(error);
}

/**
 * @param {string} message
 * @param {number} [code]
 * @returns {never}
 */
function fail(message, code = 1) {
  console.error(`Error: ${message}`);
  process.exit(code);
}

/**
 * Parses a platform map object literal from repository source.
 * Supports the simple `key: 'value'` form used by the Xget platform catalog.
 * @param {string} objectSource
 * @returns {Record<string, string>}
 */
function parsePlatformMapObject(objectSource) {
  /** @type {Record<string, string>} */
  const platforms = {};

  for (const rawLine of objectSource.split(/\r?\n/)) {
    const line = rawLine.trim();

    if (!line || line === '{' || line === '}' || line.startsWith('//')) {
      continue;
    }

    const match = line.match(
      /^(?:'([^']+)'|"([^"]+)"|([A-Za-z0-9_-]+))\s*:\s*(?:'([^']*)'|"([^"]*)")\s*,?$/
    );

    if (!match) {
      throw new Error(`unsupported platform entry: ${line}`);
    }

    const key = match[1] || match[2] || match[3];
    const value = match[4] || match[5] || '';
    platforms[key] = value;
  }

  return platforms;
}

/**
 * @param {string} url
 * @returns {Promise<string>}
 */
function httpGet(url) {
  return new Promise((resolve, reject) => {
    get(url, response => {
      if (
        response.statusCode &&
        response.statusCode >= 300 &&
        response.statusCode < 400 &&
        response.headers.location
      ) {
        resolve(httpGet(response.headers.location));
        return;
      }

      if (response.statusCode !== 200) {
        reject(new Error(`Unexpected HTTP status ${response.statusCode} for ${url}`));
        response.resume();
        return;
      }

      let body = '';
      response.setEncoding('utf8');
      response.on('data', chunk => {
        body += chunk;
      });
      response.on('end', () => resolve(body));
    }).on('error', reject);
  });
}

/**
 * @param {string} jsSource
 * @returns {Record<string, string>}
 */
export function extractPlatformsModule(jsSource) {
  const platformExportPatterns = [
    {
      name: 'PLATFORM_CATALOG',
      pattern: /export const PLATFORM_CATALOG = (\{[\s\S]*?\n\});/
    },
    {
      name: 'PLATFORMS',
      pattern: /export const PLATFORMS = (\{[\s\S]*?\n\});/
    }
  ];

  for (const { name, pattern } of platformExportPatterns) {
    const match = jsSource.match(pattern);
    if (!match) {
      continue;
    }

    try {
      return parsePlatformMapObject(match[1]);
    } catch (error) {
      fail(`Could not parse remote ${name} object: ${getErrorMessage(error)}`);
    }
  }

  fail('Could not find `export const PLATFORM_CATALOG = {...}` or `PLATFORMS = {...}`.');
}

/**
 * @param {Record<string, string>} platforms
 * @returns {PlatformEntry[]}
 */
export function createPlatformEntries(platforms) {
  return Object.entries(platforms)
    .sort(([left], [right]) => left.localeCompare(right))
    .map(([key, upstream]) => ({
      key,
      upstream,
      pathPrefix: `/${key.replace(/-/g, '/')}/`,
      category: key.startsWith('ip-')
        ? 'inference'
        : key.startsWith('cr-')
          ? 'registry'
          : 'resource'
    }));
}

/**
 * @param {string} jsSource
 * @returns {PlatformEntry[]}
 */
export function loadPlatformsFromSource(jsSource) {
  const platforms = extractPlatformsModule(jsSource);
  return createPlatformEntries(platforms);
}

/**
 * @param {string} sourceUrl
 * @returns {Promise<PlatformEntry[]>}
 */
async function loadPlatforms(sourceUrl) {
  const jsSource = await httpGet(sourceUrl);
  return loadPlatformsFromSource(jsSource);
}

/**
 * @param {string | undefined} value
 * @returns {string | null}
 */
function normalizeBaseUrl(value) {
  if (typeof value !== 'string' || !value) {
    return null;
  }

  try {
    const url = new URL(value);
    url.pathname = url.pathname.replace(/\/+$/, '');
    url.search = '';
    url.hash = '';
    return url.toString().replace(/\/$/, '');
  } catch {
    fail(`Invalid --base-url value "${value}". Expected an absolute URL.`);
  }
}

/**
 * Resolve an explicit or environment-provided base URL without inventing a fallback instance.
 * @param {string | undefined} optionValue
 * @param {string | undefined} envValue
 * @returns {string | null}
 */
export function resolveBaseUrl(optionValue, envValue) {
  return normalizeBaseUrl(optionValue ?? envValue);
}

/**
 * @param {string} value
 * @param {string} flagName
 * @returns {URL}
 */
function normalizeAbsoluteUrl(value, flagName) {
  try {
    return new URL(value);
  } catch {
    fail(`Invalid ${flagName} value "${value}". Expected an absolute URL.`);
  }
}

/**
 * @param {string} pathname
 * @returns {string}
 */
function normalizePathname(pathname) {
  if (!pathname || pathname === '/') {
    return '';
  }

  return pathname.replace(/\/+$/, '');
}

/**
 * @param {string} pathname
 * @param {string} prefix
 * @param {boolean} [caseInsensitive]
 * @returns {boolean}
 */
function matchesPathPrefix(pathname, prefix, caseInsensitive = false) {
  const normalizedPath = normalizePathname(pathname);
  const normalizedPrefix = normalizePathname(prefix);

  if (!normalizedPrefix) {
    return true;
  }

  if (!normalizedPath) {
    return false;
  }

  if (caseInsensitive) {
    const lowerPath = normalizedPath.toLowerCase();
    const lowerPrefix = normalizedPrefix.toLowerCase();
    return lowerPath === lowerPrefix || lowerPath.startsWith(`${lowerPrefix}/`);
  }

  return normalizedPath === normalizedPrefix || normalizedPath.startsWith(`${normalizedPrefix}/`);
}

/**
 * @param {string} pathname
 * @param {string} prefix
 * @param {boolean} [caseInsensitive]
 * @returns {string}
 */
function stripPathPrefix(pathname, prefix, caseInsensitive = false) {
  const normalizedPrefix = normalizePathname(prefix);
  if (!normalizedPrefix) {
    return pathname;
  }

  const flags = caseInsensitive ? 'i' : '';
  const escapedPrefix = normalizedPrefix.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return pathname.replace(new RegExp(`^${escapedPrefix}(?=/|$)`, flags), '');
}

/**
 * @param {PlatformEntry[]} platforms
 * @param {string} key
 * @returns {PlatformEntry | null}
 */
function findPlatformByKey(platforms, key) {
  return platforms.find(platform => platform.key === key) ?? null;
}

/**
 * @param {PlatformEntry[]} platforms
 * @param {URL} originUrl
 * @returns {PlatformEntry | null}
 */
function findSpecialPlatformForUrl(platforms, originUrl) {
  if (originUrl.hostname === 'ghcr.io') {
    if (originUrl.pathname.startsWith('/v2/homebrew/')) {
      return findPlatformByKey(platforms, 'homebrew-bottles');
    }

    return findPlatformByKey(platforms, 'cr-ghcr');
  }

  return null;
}

/**
 * @param {PlatformEntry[]} platforms
 * @param {URL} originUrl
 * @returns {PlatformEntry | null}
 */
export function findPlatformForUrl(platforms, originUrl) {
  const specialPlatform = findSpecialPlatformForUrl(platforms, originUrl);
  if (specialPlatform) {
    return specialPlatform;
  }

  const matchingPlatforms = platforms
    .filter(platform => {
      const upstreamUrl = new URL(platform.upstream);
      if (upstreamUrl.origin !== originUrl.origin) {
        return false;
      }

      const caseInsensitive = platform.key === 'homebrew' || platform.key === 'homebrew-api';
      return matchesPathPrefix(originUrl.pathname, upstreamUrl.pathname, caseInsensitive);
    })
    .sort((left, right) => {
      const leftPathLength = normalizePathname(new URL(left.upstream).pathname).length;
      const rightPathLength = normalizePathname(new URL(right.upstream).pathname).length;
      return rightPathLength - leftPathLength;
    });

  return matchingPlatforms[0] ?? null;
}

/**
 * @param {PlatformEntry} platform
 * @param {URL} originUrl
 * @returns {string}
 */
export function getConvertedSuffix(platform, originUrl) {
  let pathname = originUrl.pathname;

  if (platform.key === 'homebrew') {
    pathname = stripPathPrefix(pathname, '/Homebrew', true);
  } else if (platform.key === 'homebrew-api') {
    pathname = stripPathPrefix(pathname, '/api', true);
  } else if (platform.key === 'crates') {
    pathname = stripPathPrefix(pathname, CRATES_API_PREFIX, true);
  } else {
    const upstreamPath = new URL(platform.upstream).pathname;
    pathname = stripPathPrefix(pathname, upstreamPath);
  }

  if (!pathname) {
    pathname = '/';
  }

  if (!pathname.startsWith('/')) {
    pathname = `/${pathname}`;
  }

  return `${pathname}${originUrl.search}${originUrl.hash}`;
}

/**
 * @param {string} baseUrl
 * @param {PlatformEntry} platform
 * @param {URL} originUrl
 * @returns {string}
 */
export function buildConvertedUrl(baseUrl, platform, originUrl) {
  const suffix = getConvertedSuffix(platform, originUrl);
  return `${baseUrl}${platform.pathPrefix}${suffix.replace(/^\/+/, '')}`;
}

/**
 * @param {string} line
 * @returns {Omit<MarkdownHeading, 'index' | 'parent'> | null}
 */
function parseMarkdownHeading(line) {
  const match = line.trim().match(/^(#{1,6})\s+(.+?)\s*$/);

  if (!match) {
    return null;
  }

  const text = match[2].trim();

  return {
    level: match[1].length,
    text,
    raw: `${match[1]} ${text}`
  };
}

/**
 * @param {string} heading
 * @returns {string}
 */
function normalizeHeadingQuery(heading) {
  return heading
    .replace(/^#{1,6}\s+/, '')
    .replace(/^[^\p{L}\p{N}]+/u, '')
    .trim()
    .toLowerCase();
}

/**
 * @param {string} line
 * @returns {boolean}
 */
function isCodeFenceDelimiter(line) {
  return /^(```|~~~)/.test(line.trim());
}

/**
 * @param {string[]} lines
 * @returns {MarkdownHeading[]}
 */
function collectMarkdownHeadings(lines) {
  /** @type {Array<string | undefined>} */
  const stack = [];
  let inCodeFence = false;

  return lines.flatMap((line, index) => {
    if (isCodeFenceDelimiter(line)) {
      inCodeFence = !inCodeFence;
      return [];
    }

    if (inCodeFence) {
      return [];
    }

    const heading = parseMarkdownHeading(line);
    if (!heading) {
      return [];
    }

    let parent = null;
    for (let level = heading.level - 1; level >= 1; level -= 1) {
      if (stack[level]) {
        parent = stack[level] ?? null;
        break;
      }
    }

    stack[heading.level] = heading.text;
    stack.length = heading.level + 1;

    return [
      {
        index,
        ...heading,
        parent
      }
    ];
  });
}

/**
 * @param {MarkdownHeading} heading
 * @returns {string}
 */
function formatHeadingLabel(heading) {
  return heading.parent ? `${heading.raw} (under ${heading.parent})` : heading.raw;
}

/**
 * @param {string[]} lines
 * @param {MarkdownHeading} heading
 * @returns {string}
 */
function sliceMarkdownSection(lines, heading) {
  let endIndex = lines.length;
  let inCodeFence = false;

  for (let index = heading.index + 1; index < lines.length; index += 1) {
    if (isCodeFenceDelimiter(lines[index])) {
      inCodeFence = !inCodeFence;
      continue;
    }

    if (inCodeFence) {
      continue;
    }

    const candidate = parseMarkdownHeading(lines[index]);
    if (candidate && candidate.level <= heading.level) {
      endIndex = index;
      break;
    }
  }

  return lines.slice(heading.index, endIndex).join('\n').trimEnd();
}

/**
 * @param {string[]} lines
 * @param {string} heading
 * @returns {MarkdownHeading}
 */
function findUniqueHeading(lines, heading) {
  const headings = collectMarkdownHeadings(lines);
  const query = normalizeHeadingQuery(heading);
  const matches = headings.filter(candidate => normalizeHeadingQuery(candidate.text) === query);

  if (matches.length === 0) {
    fail(`Could not find README heading "${heading}".`);
  }

  if (matches.length > 1) {
    fail(
      `Heading "${heading}" matched multiple sections: ${matches.map(formatHeadingLabel).join('; ')}`
    );
  }

  return matches[0];
}

/**
 * @param {MarkdownHeading[]} headings
 * @param {string | undefined} match
 * @returns {MarkdownHeading[]}
 */
function filterHeadingsByMatch(headings, match) {
  if (!match) {
    return headings;
  }

  const query = match.trim().toLowerCase();

  return headings.filter(heading => {
    const haystacks = [heading.text, heading.raw, heading.parent ?? ''];
    return haystacks.some(value => value.toLowerCase().includes(query));
  });
}

/**
 * @param {string} markdown
 * @param {number} [minLevel]
 * @param {number} [maxLevel]
 * @returns {MarkdownHeading[]}
 */
export function listMarkdownHeadings(markdown, minLevel = 2, maxLevel = 6) {
  const lines = markdown.split(/\r?\n/);

  return collectMarkdownHeadings(lines)
    .map(heading => ({
      ...heading,
      parent: heading.level <= minLevel ? null : heading.parent
    }))
    .filter(heading => heading.level >= minLevel && heading.level <= maxLevel);
}

/**
 * @param {string} markdown
 * @param {string} heading
 * @returns {MarkdownHeading}
 */
export function resolveMarkdownHeading(markdown, heading) {
  return findUniqueHeading(markdown.split(/\r?\n/), heading);
}

/**
 * @param {string} markdown
 * @param {string} heading
 * @returns {string}
 */
export function extractMarkdownSection(markdown, heading) {
  const lines = markdown.split(/\r?\n/);
  const resolvedHeading = findUniqueHeading(lines, heading);
  return sliceMarkdownSection(lines, resolvedHeading);
}

/**
 * @param {string} baseUrl
 * @param {string} markdownSection
 * @returns {string}
 */
export function rewriteUseCasesBaseUrl(baseUrl, markdownSection) {
  const host = new URL(baseUrl).host;

  return markdownSection
    .replaceAll(DEFAULT_PUBLIC_BASE_URL, baseUrl)
    .replaceAll(DEFAULT_PUBLIC_HOST, host);
}

/**
 * @param {string} useCasesMarkdown
 * @param {string | undefined} heading
 * @param {string | undefined} match
 * @returns {{ heading: string, content: string }}
 */
export function selectUseCaseSection(useCasesMarkdown, heading, match) {
  if (heading && match) {
    fail('Use either --heading or --match for snippet, not both.', 2);
  }

  if (!heading && !match) {
    return {
      heading: README_USE_CASES_HEADING,
      content: useCasesMarkdown
    };
  }

  const lines = useCasesMarkdown.split(/\r?\n/);

  if (heading) {
    const resolvedHeading = findUniqueHeading(lines, heading);

    return {
      heading: resolvedHeading.raw,
      content: sliceMarkdownSection(lines, resolvedHeading)
    };
  }

  const matchedHeadings = filterHeadingsByMatch(
    listMarkdownHeadings(useCasesMarkdown, 3, 4),
    match
  );

  if (matchedHeadings.length === 0) {
    fail(`Could not find a README Use Cases heading matching "${match}".`, 2);
  }

  if (matchedHeadings.length > 1) {
    fail(
      `Match "${match}" was ambiguous. Candidates: ${matchedHeadings.map(formatHeadingLabel).join('; ')}`,
      2
    );
  }

  return {
    heading: matchedHeadings[0].raw,
    content: sliceMarkdownSection(lines, matchedHeadings[0])
  };
}

/**
 * @param {string} baseUrl
 * @param {string} readmeMarkdown
 * @param {{ heading?: string, match?: string }} [options]
 * @returns {UseCasesSnippet}
 */
export function createUseCasesSnippet(baseUrl, readmeMarkdown, options = {}) {
  const useCasesSection = extractMarkdownSection(readmeMarkdown, README_USE_CASES_HEADING);
  const selectedSection = selectUseCaseSection(useCasesSection, options.heading, options.match);

  return {
    section: 'use-cases',
    heading: selectedSection.heading,
    baseUrl,
    content: rewriteUseCasesBaseUrl(baseUrl, selectedSection.content)
  };
}

/**
 * @param {unknown} value
 * @returns {void}
 */
function renderJson(value) {
  console.log(JSON.stringify(value, null, 2));
}

/**
 * @param {PlatformEntry[]} rows
 * @returns {void}
 */
function renderTable(rows) {
  /** @type {Array<keyof PlatformEntry>} */
  const headers = ['key', 'category', 'pathPrefix', 'upstream'];
  const widths = headers.map(header =>
    Math.max(header.length, ...rows.map(row => String(row[header]).length))
  );

  /**
   * @param {Record<string, string>} row
   * @returns {string}
   */
  const formatRow = row =>
    headers.map((header, index) => String(row[header]).padEnd(widths[index])).join('  ');

  console.log(formatRow(Object.fromEntries(headers.map(header => [header, header]))));
  console.log(widths.map(width => '-'.repeat(width)).join('  '));
  rows.forEach(row => console.log(formatRow(row)));
}

/**
 * @param {UseCasesSnippet['content']} content
 * @returns {void}
 */
function renderTextContent(content) {
  console.log(content);
}

/**
 * @param {MarkdownHeading[]} headings
 * @returns {void}
 */
function renderTextHeadings(headings) {
  headings.forEach(heading => {
    if (heading.parent) {
      console.log(`${heading.text} (under ${heading.parent})`);
      return;
    }

    console.log(heading.text);
  });
}

/**
 * @param {CliOptions} options
 * @param {string} key
 * @returns {string | undefined}
 */
function getStringOption(options, key) {
  const value = options[key];
  return typeof value === 'string' ? value : undefined;
}

async function main() {
  const { command, options } = parseArgs(process.argv.slice(2));

  if (options.help || command === 'help') {
    printHelp();
    return;
  }

  const sourceUrl = getStringOption(options, 'source-url') ?? DEFAULT_SOURCE_URL;
  const format = getStringOption(options, 'format') ?? 'json';

  if (command === 'platforms') {
    const platforms = await loadPlatforms(sourceUrl);
    if (format === 'json') {
      renderJson({
        sourceUrl,
        count: platforms.length,
        platforms
      });
      return;
    }

    if (format === 'table') {
      renderTable(platforms);
      return;
    }

    fail('Unsupported --format for platforms. Use json or table.', 2);
  }

  if (command === 'convert') {
    const baseUrl =
      resolveBaseUrl(getStringOption(options, 'base-url'), process.env.XGET_BASE_URL) ??
      fail(MISSING_BASE_URL_HINT, 2);

    const rawUrl = getStringOption(options, 'url');
    if (!rawUrl) {
      fail('Missing --url for convert.', 2);
    }

    const originUrl = normalizeAbsoluteUrl(rawUrl, '--url');
    const platforms = await loadPlatforms(sourceUrl);
    const platform = findPlatformForUrl(platforms, originUrl);

    if (!platform) {
      fail(`No current Xget platform matched upstream origin ${originUrl.origin}.`, 3);
    }

    const convertedUrl = buildConvertedUrl(baseUrl, platform, originUrl);
    const payload = {
      sourceUrl,
      baseUrl,
      upstreamUrl: originUrl.toString(),
      matchedPlatform: platform,
      convertedUrl
    };

    if (format === 'json') {
      renderJson(payload);
      return;
    }

    if (format === 'text') {
      console.log(payload.convertedUrl);
      return;
    }

    fail('Unsupported --format for convert. Use json or text.', 2);
  }

  if (command === 'topics') {
    const readmeUrl = getStringOption(options, 'readme-url') ?? DEFAULT_README_URL;
    const readmeMarkdown = await httpGet(readmeUrl);
    const useCasesSection = extractMarkdownSection(readmeMarkdown, README_USE_CASES_HEADING);
    const topics = filterHeadingsByMatch(
      listMarkdownHeadings(useCasesSection, 3, 4),
      getStringOption(options, 'match')
    );
    const payload = {
      sourceUrl: readmeUrl,
      section: 'use-cases',
      heading: README_USE_CASES_HEADING,
      match: getStringOption(options, 'match') ?? null,
      count: topics.length,
      topics: topics.map(({ index, ...topic }) => topic)
    };

    if (format === 'json') {
      renderJson(payload);
      return;
    }

    if (format === 'text') {
      renderTextHeadings(topics);
      return;
    }

    fail('Unsupported --format for topics. Use json or text.', 2);
  }

  if (command === 'snippet') {
    const baseUrl =
      resolveBaseUrl(getStringOption(options, 'base-url'), process.env.XGET_BASE_URL) ??
      fail(MISSING_BASE_URL_HINT, 2);

    if (getStringOption(options, 'preset')) {
      fail(
        '`--preset` is no longer supported. `snippet` now fetches the README Use Cases section.',
        2
      );
    }

    const readmeUrl = getStringOption(options, 'readme-url') ?? DEFAULT_README_URL;
    const readmeMarkdown = await httpGet(readmeUrl);
    const snippet = {
      sourceUrl: readmeUrl,
      ...createUseCasesSnippet(baseUrl, readmeMarkdown, {
        heading: getStringOption(options, 'heading'),
        match: getStringOption(options, 'match')
      })
    };

    if (format === 'json') {
      renderJson(snippet);
      return;
    }

    if (format === 'text') {
      renderTextContent(snippet.content);
      return;
    }

    fail('Unsupported --format for snippet. Use json or text.', 2);
  }

  fail(`Unknown command "${command}". Use --help for supported commands.`, 2);
}

const entryHref = process.argv[1] ? pathToFileURL(process.argv[1]).href : null;

if (entryHref === import.meta.url) {
  main().catch(error => fail(getErrorMessage(error)));
}

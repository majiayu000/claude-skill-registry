/**
 * Cookieless page-view and event counting via Umami Cloud.
 *
 * Umami records the path, referrer, browser, screen size and country per
 * visit; it sets no cookies and stores no persistent visitor IDs. Events:
 *   install-copy      an install command was copied ({ skill })
 *   outbound-spellbook / outbound-sk / outbound-source  link clicks ({ href })
 * Counting only runs on the public host; leave UMAMI_WEBSITE_ID empty to
 * disable it everywhere.
 */
(function initRegistryAnalytics(globalScope) {
    'use strict';

    const UMAMI_WEBSITE_ID = '62ee5959-9f0e-44fc-a10f-7c6a5d41bdc0';
    const SCRIPT_SRC = 'https://cloud.umami.is/script.js';
    const PUBLIC_HOST = 'majiayu000.github.io';

    if (!UMAMI_WEBSITE_ID || !globalScope.document) return;

    const doc = globalScope.document;
    const script = doc.createElement('script');
    script.defer = true;
    script.src = SCRIPT_SRC;
    script.dataset.websiteId = UMAMI_WEBSITE_ID;
    script.dataset.domains = PUBLIC_HOST;
    doc.head.appendChild(script);

    function sanitize(value) {
        return String(value ?? '').replace(/[^a-zA-Z0-9_./:@+-]/g, '').slice(0, 160);
    }

    function track(name, data) {
        const umami = globalScope.umami;
        if (umami && typeof umami.track === 'function') umami.track(name, data);
    }

    function outboundEvent(href) {
        if (/github\.com\/majiayu000\/spellbook/i.test(href)) return 'outbound-spellbook';
        if (/github\.com\/majiayu000\/c(l)?aude-skill-manager/i.test(href)) return 'outbound-sk';
        if (/github\.com\//i.test(href)) return 'outbound-source';
        return '';
    }

    // Capture phase: copyInstall() stops propagation before a bubbling listener runs.
    doc.addEventListener('click', event => {
        if (!event.target.closest) return;
        const button = event.target.closest('.copy-btn, #copy-install');
        if (button) {
            const skill = sanitize(button.getAttribute('data-install'))
                || sanitize(globalScope.location.pathname).replace(/^\/+/, '');
            track('install-copy', { skill });
            return;
        }
        const link = event.target.closest('a[href]');
        const name = link && outboundEvent(link.href);
        if (name) track(name, { href: sanitize(link.href.split('#')[0]) });
    }, true);

    // Static skill pages have no copy button; count manual copies from code blocks.
    doc.addEventListener('copy', () => {
        const selection = globalScope.getSelection && globalScope.getSelection();
        const node = selection && selection.anchorNode;
        const element = node && (node.nodeType === 1 ? node : node.parentElement);
        if (element && element.closest('pre, code')) {
            track('install-copy', { skill: sanitize(globalScope.location.pathname).replace(/^\/+/, '') });
        }
    });
})(typeof window !== 'undefined' ? window : globalThis);

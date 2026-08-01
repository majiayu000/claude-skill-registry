/** Static artifact API v1 reader validation. Loaded before app.js. */

function requireExactFields(value, fields, label) {
    if (!value || typeof value !== 'object' || Array.isArray(value)) {
        throw new Error(`${label} must be an object`);
    }
    const missing = fields.filter(field => !Object.prototype.hasOwnProperty.call(value, field));
    const unknown = Object.keys(value).filter(field => !fields.includes(field));
    if (missing.length || unknown.length) throw new Error(`${label} shape mismatch`);
}

function requireSchemaOne(value, label) {
    if (!value || value.schema_version !== 1) throw new Error(`${label} schema_version must be 1`);
}

function requireNonNegativeInteger(value, label) {
    if (!Number.isInteger(value) || value < 0) {
        throw new Error(`${label} must be a non-negative integer`);
    }
}

function validateCategoryTaxonomy(payload) {
    requireExactFields(payload, ['schema_version', 'taxonomy_schema_version', 'updated_at',
        'default_category', 'default_code', 'category_count', 'categories'],
    'Category taxonomy');
    requireSchemaOne(payload, 'Category taxonomy');
    requireNonNegativeInteger(payload.category_count, 'Category taxonomy category_count');
    if (payload.taxonomy_schema_version !== 2 ||
        typeof payload.updated_at !== 'string' || !payload.updated_at ||
        typeof payload.default_category !== 'string' || !payload.default_category ||
        typeof payload.default_code !== 'string' || !payload.default_code ||
        !Array.isArray(payload.categories) ||
        payload.category_count !== 40 ||
        payload.categories.length !== payload.category_count) {
        throw new Error('Category taxonomy count or identity mismatch');
    }

    const bySlug = new Map();
    const codes = new Set();
    const canonicalIdentifier = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
    payload.categories.forEach((category, index) => {
        requireExactFields(category, ['slug', 'code', 'display_name', 'parent'],
            `Category taxonomy entry ${index}`);
        if (typeof category.slug !== 'string' ||
            !canonicalIdentifier.test(category.slug) ||
            typeof category.code !== 'string' ||
            !canonicalIdentifier.test(category.code) ||
            typeof category.display_name !== 'string' || !category.display_name ||
            typeof category.parent !== 'string' ||
            bySlug.has(category.slug) || codes.has(category.code)) {
            throw new Error('Category taxonomy entry identity mismatch');
        }
        bySlug.set(category.slug, category);
        codes.add(category.code);
    });

    const defaultEntry = bySlug.get(payload.default_category);
    if (!defaultEntry || defaultEntry.code !== payload.default_code) {
        throw new Error('Category taxonomy default mismatch');
    }
    payload.categories.forEach(category => {
        if (!category.parent) return;
        const parent = bySlug.get(category.parent);
        if (!parent || parent.slug === category.slug || parent.parent) {
            throw new Error('Category taxonomy parent mismatch');
        }
    });
    if (payload.categories.filter(category => !category.parent).length !== 12) {
        throw new Error('Category taxonomy root count mismatch');
    }
}

function isSafeArtifactPath(path, prefix) {
    return typeof path === 'string' && path.startsWith(prefix) &&
        !path.startsWith('/') && !path.includes('\\') && !path.includes('://') &&
        path.split('/').every(part => part && part !== '.' && part !== '..');
}

function normalizeSearchIndex(indexData) {
    if (indexData?.schema_version === 1) {
        requireExactFields(indexData, ['schema_version', 'version', 'updated_at', 'total_count',
            'included_count', 'limit', 'raw_count', 'dedupe_key', 'skills'], 'Lite search index');
        ['total_count', 'included_count', 'limit', 'raw_count'].forEach(
            key => requireNonNegativeInteger(indexData[key], `Lite ${key}`));
        if (!Array.isArray(indexData.skills) || indexData.included_count !== indexData.skills.length ||
            indexData.included_count > indexData.total_count || indexData.included_count > indexData.limit ||
            indexData.dedupe_key !== 'install|branch' || typeof indexData.version !== 'string' ||
            !indexData.version || typeof indexData.updated_at !== 'string' || !indexData.updated_at) {
            throw new Error('Lite search index count or identity mismatch');
        }
        return {
            v: indexData.version,
            t: indexData.total_count,
            s: indexData.skills.map(normalizeSkillRecord),
            includedCount: indexData.included_count,
            isLite: true
        };
    }
    requireExactFields(indexData, ['v', 't', 's'], 'Legacy full search index');
    requireNonNegativeInteger(indexData.t, 'Legacy full total');
    if (!Array.isArray(indexData.s) || indexData.s.length !== indexData.t) {
        throw new Error('Legacy full search index count mismatch');
    }
    return {
        ...indexData,
        s: indexData.s.map(normalizeSkillRecord),
        includedCount: indexData.s.length,
        isLite: false
    };
}

function validateSearchPointer(pointer) {
    requireExactFields(pointer, ['schema_version', 'total_count', 'deprecated_full_payload',
        'message', 'manifest', 'replacement', 'compat_since', 'compat_until', 'v', 't'],
    'Search index pointer');
    requireSchemaOne(pointer, 'Search index pointer');
    requireNonNegativeInteger(pointer.total_count, 'Search pointer total_count');
    requireNonNegativeInteger(pointer.t, 'Search pointer t');
    if (pointer.total_count !== pointer.t || pointer.deprecated_full_payload !== true ||
        pointer.manifest !== 'search-index-manifest.json' ||
        pointer.replacement !== 'search-shards/part-*.json' ||
        pointer.compat_since !== 'static-artifact-api-v1' ||
        pointer.compat_until !== 'static-artifact-api-v2' ||
        typeof pointer.message !== 'string' || !pointer.message ||
        typeof pointer.v !== 'string' || !pointer.v) {
        throw new Error('Search index pointer contract mismatch');
    }
}

function validateSearchManifest(manifest, pointer) {
    requireExactFields(manifest, ['schema_version', 'v', 'updated_at', 'total_count',
        'shard_strategy', 'record_schema', 'shard_count', 'largest_shard_bytes',
        'largest_shard_gzip_bytes', 'shards'], 'Search index manifest');
    requireSchemaOne(manifest, 'Search index manifest');
    ['total_count', 'shard_count', 'largest_shard_bytes', 'largest_shard_gzip_bytes'].forEach(
        key => requireNonNegativeInteger(manifest[key], `Search manifest ${key}`));
    if (!Array.isArray(manifest.shards) || manifest.shards.length !== manifest.shard_count ||
        manifest.total_count !== pointer.total_count || manifest.v !== pointer.v ||
        manifest.shard_strategy !== 'bounded-sequential-stars-desc' ||
        manifest.record_schema !== 'search-mini-v2' ||
        typeof manifest.updated_at !== 'string' || !manifest.updated_at) {
        throw new Error('Search manifest count or identity mismatch');
    }
}

function validateSearchShardEntry(entry, seenPaths) {
    requireExactFields(entry, ['path', 'gzip_path', 'count', 'bytes', 'gzip_bytes', 'sha256'],
        'Search shard entry');
    ['count', 'bytes', 'gzip_bytes'].forEach(
        key => requireNonNegativeInteger(entry[key], `Search shard ${key}`));
    if (!isSafeArtifactPath(entry.path, 'search-shards/') ||
        !isSafeArtifactPath(entry.gzip_path, 'search-shards/') ||
        seenPaths.has(entry.path) || seenPaths.has(entry.gzip_path) ||
        typeof entry.sha256 !== 'string' || !/^[0-9a-f]{64}$/.test(entry.sha256)) {
        throw new Error('Invalid or duplicate search shard path');
    }
    seenPaths.add(entry.path);
    seenPaths.add(entry.gzip_path);
}

function validateSearchShardPayload(payload, entry, index, manifest) {
    requireExactFields(payload, ['schema_version', 'v', 'part', 'part_count', 'count', 's'],
        'Search shard payload');
    requireSchemaOne(payload, 'Search shard');
    ['part', 'part_count', 'count'].forEach(
        key => requireNonNegativeInteger(payload[key], `Search shard ${key}`));
    if (payload.v !== manifest.v || payload.part !== index ||
        payload.part_count !== manifest.shard_count || !Array.isArray(payload.s) ||
        payload.count !== entry.count || payload.s.length !== entry.count) {
        throw new Error('Search shard identity/count mismatch');
    }
}

function validateCategoryIndexEntry(category, categoryCode) {
    requireExactFields(category, ['name', 'code', 'count', 'path', 'manifest', 'part_count',
        'largest_part_bytes', 'largest_part_gzip_bytes'], 'Category index entry');
    ['count', 'part_count', 'largest_part_bytes', 'largest_part_gzip_bytes'].forEach(
        key => requireNonNegativeInteger(category[key], `Category entry ${key}`));
    if (category.code !== categoryCode || !category.name ||
        !isSafeArtifactPath(category.path, 'categories/') ||
        !isSafeArtifactPath(category.manifest, 'categories/')) {
        throw new Error('Category index entry identity or path mismatch');
    }
}

function validateCategoryManifest(manifest, category, categoryCode) {
    requireExactFields(manifest, ['schema_version', 'category', 'code', 'updated_at',
        'total_count', 'count', 'part_count', 'part_strategy', 'largest_part_bytes',
        'largest_part_gzip_bytes', 'parts'], 'Category manifest');
    requireSchemaOne(manifest, 'Category manifest');
    ['total_count', 'count', 'part_count', 'largest_part_bytes', 'largest_part_gzip_bytes'].forEach(
        key => requireNonNegativeInteger(manifest[key], `Category manifest ${key}`));
    if (!Array.isArray(manifest.parts) || manifest.parts.length !== manifest.part_count ||
        manifest.total_count !== manifest.count || manifest.count !== category.count ||
        manifest.part_count !== category.part_count || manifest.code !== categoryCode ||
        manifest.category !== category.name ||
        manifest.part_strategy !== 'bounded-sequential-stars-desc' || !manifest.updated_at) {
        throw new Error('Category manifest count or identity mismatch');
    }
}

function validateCategoryPartEntry(entry, seenPaths) {
    requireExactFields(entry, ['path', 'gzip_path', 'count', 'bytes', 'gzip_bytes', 'sha256'],
        'Category part entry');
    ['count', 'bytes', 'gzip_bytes'].forEach(
        key => requireNonNegativeInteger(entry[key], `Category part ${key}`));
    if (!isSafeArtifactPath(entry.path, 'categories/') ||
        !isSafeArtifactPath(entry.gzip_path, 'categories/') || seenPaths.has(entry.path) ||
        seenPaths.has(entry.gzip_path) || !/^[0-9a-f]{64}$/.test(entry.sha256)) {
        throw new Error('Invalid or duplicate category part path');
    }
    seenPaths.add(entry.path);
    seenPaths.add(entry.gzip_path);
}

function validateCategoryPartPayload(payload, entry, manifest, categoryCode) {
    requireExactFields(payload, ['schema_version', 'category', 'code', 'updated_at', 'part',
        'part_count', 'count', 'skills'], 'Category part payload');
    requireSchemaOne(payload, 'Category part');
    ['part', 'part_count', 'count'].forEach(
        key => requireNonNegativeInteger(payload[key], `Category payload ${key}`));
    if (payload.part !== 0 || payload.part_count !== manifest.part_count ||
        payload.category !== manifest.category || payload.code !== categoryCode ||
        payload.updated_at !== manifest.updated_at || !Array.isArray(payload.skills) ||
        payload.count !== entry.count || payload.skills.length !== entry.count) {
        throw new Error('Category first-part identity/count mismatch');
    }
}

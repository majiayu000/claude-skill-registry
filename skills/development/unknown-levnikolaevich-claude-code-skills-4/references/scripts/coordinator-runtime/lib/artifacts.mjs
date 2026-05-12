// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/artifacts.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

function safeSegment(value) {
    return String(value || "default")
        .trim()
        .replace(/[^a-zA-Z0-9._-]+/g, "-")
        .replace(/^-+|-+$/g, "")
        .toLowerCase() || "default";
}

export function runtimeArtifactDir(projectRoot, runId, summaryKind) {
    return join(
        resolve(projectRoot || process.cwd()),
        ".hex-skills",
        "runtime-artifacts",
        "runs",
        safeSegment(runId),
        safeSegment(summaryKind),
    );
}

export function runtimeArtifactPath(projectRoot, runId, summaryKind, identifier) {
    return join(runtimeArtifactDir(projectRoot, runId, summaryKind), `${safeSegment(identifier)}.json`);
}

export function runtimeArtifactPathForFile(projectRoot, runId, summaryKind, fileName) {
    return join(runtimeArtifactDir(projectRoot, runId, summaryKind), fileName);
}

export function resolveArtifactWritePath(projectRoot, artifactPath) {
    const resolvedProjectRoot = resolve(projectRoot || process.cwd());
    const resolvedArtifactPath = resolve(resolvedProjectRoot, artifactPath);
    if (dirname(resolvedArtifactPath) === resolvedProjectRoot) {
        throw new Error("Runtime artifacts must not be written to the project root");
    }
    return resolvedArtifactPath;
}

export function writeRuntimeArtifactJsonToPath(projectRoot, artifactPath, payload) {
    const resolvedArtifactPath = resolveArtifactWritePath(projectRoot, artifactPath);
    mkdirSync(dirname(resolvedArtifactPath), { recursive: true });
    writeFileSync(resolvedArtifactPath, JSON.stringify(payload, null, 2) + "\n", "utf8");
    return resolvedArtifactPath;
}

export function writeRuntimeArtifactJson(projectRoot, runId, summaryKind, identifier, payload) {
    const artifactPath = runtimeArtifactPath(projectRoot, runId, summaryKind, identifier);
    const nextPayload = payload && typeof payload === "object" && payload.payload && typeof payload.payload === "object"
        ? {
            ...payload,
            payload: {
                ...payload.payload,
                artifact_path: payload.payload.artifact_path || artifactPath,
            },
        }
        : payload;
    return writeRuntimeArtifactJsonToPath(projectRoot, artifactPath, nextPayload);
}

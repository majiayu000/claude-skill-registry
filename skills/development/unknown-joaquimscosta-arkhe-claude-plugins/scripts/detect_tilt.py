#!/usr/bin/env python3
"""
Detect Tilt installation and audit Tiltfile configurations.

Outputs JSON report of installed tools, kubectl context, existing Tiltfile,
modular `tilt/` layout (also recognizes legacy `.tilt/`), detected ecosystems,
and audit violations.
Used by tilt-setup skill.

Uses only standard library (no external dependencies).

Usage:
    python3 detect_tilt.py [project_root] [--no-audit]
"""

import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run_cmd(cmd):
    """Run a command and return stdout, or None on failure."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return None


def detect_os():
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    return system


# ---------------------------------------------------------------------------
# Tool detection
# ---------------------------------------------------------------------------

def detect_tool(name, version_args=None):
    """Check if a tool is installed and get its version."""
    path = shutil.which(name)
    if not path:
        return {"installed": False}

    info = {"installed": True, "path": path}
    args = version_args or [name, "--version"]
    version_output = run_cmd(args)
    if version_output:
        match = re.search(r"(\d+\.\d+\.\d+)", version_output)
        if match:
            info["version"] = match.group(1)
        else:
            info["version_raw"] = version_output.splitlines()[0]

    return info


# ---------------------------------------------------------------------------
# Kubernetes context detection
# ---------------------------------------------------------------------------

# Patterns that indicate a production / shared cluster (must be blocked)
PROD_CONTEXT_PATTERNS = [
    "arn:aws:eks:",     # AWS EKS ARN
    "gke_",             # GKE format: gke_PROJECT_REGION_CLUSTER
    "akscluster",       # AKS naming
    ":aks/",            # AKS resource path
    "prod",
    "production",
    "staging",
]

# Patterns that indicate a known-safe local cluster
SAFE_CONTEXT_PATTERNS = [
    "docker-desktop",
    "docker-for-desktop",
    "minikube",
    "kind-",
    "k3d-",
    "k3s-",
    "colima",
    "orbstack",
    "rancher-desktop",
    "microk8s",
    "localhost",
]


def detect_kubectl_context():
    """Detect kubectl current context and classify it."""
    if not shutil.which("kubectl"):
        return {"available": False}

    context = run_cmd(["kubectl", "config", "current-context"])
    if not context:
        return {"available": True, "context": None}

    ctx_lower = context.lower()
    is_prod = any(p in ctx_lower for p in PROD_CONTEXT_PATTERNS)
    cluster_type = "unknown"
    for safe in SAFE_CONTEXT_PATTERNS:
        if safe in ctx_lower:
            cluster_type = safe.rstrip("-")
            break

    return {
        "available": True,
        "context": context,
        "is_production_pattern": is_prod,
        "is_safe_pattern": not is_prod and cluster_type != "unknown",
        "cluster_type": cluster_type,
    }


# ---------------------------------------------------------------------------
# Tiltfile detection + parsing
# ---------------------------------------------------------------------------

def _read_safe(path):
    try:
        return path.read_text()
    except OSError:
        return None


def _find_tiltfile(project_root):
    """Find Tiltfile in project root or common subdirectories."""
    root = Path(project_root)
    candidates = [
        root / "Tiltfile",
        root / "tilt" / "Tiltfile",
        root / ".tilt" / "Tiltfile",
    ]
    for path in candidates:
        if path.exists() and path.is_file():
            return path
    return None


# Regex patterns for parsing Tiltfile content
DOCKER_BUILD_RE = re.compile(r"\bdocker_build\s*\(", re.MULTILINE)
CUSTOM_BUILD_RE = re.compile(r"\bcustom_build\s*\(", re.MULTILINE)
DOCKER_BUILD_RESTART_RE = re.compile(r"\bdocker_build_with_restart\s*\(")
K8S_YAML_RE = re.compile(r"\bk8s_yaml\s*\(")
K8S_RESOURCE_RE = re.compile(r"\bk8s_resource\s*\(")
HELM_RE = re.compile(r"\bhelm\s*\(")
LIVE_UPDATE_RE = re.compile(r"\blive_update\s*=", re.MULTILINE)
SYNC_RE = re.compile(r"\bsync\s*\(")
RUN_RE = re.compile(r"\brun\s*\(")
FALL_BACK_ON_RE = re.compile(r"\bfall_back_on\s*\(")
RESTART_CONTAINER_RE = re.compile(r"\brestart_container\s*\(")
ALLOW_K8S_CONTEXTS_RE = re.compile(r"\ballow_k8s_contexts\s*\(")
WATCH_SETTINGS_RE = re.compile(r"\bwatch_settings\s*\(")
UPDATE_SETTINGS_RE = re.compile(r"\bupdate_settings\s*\(")
LOAD_LOCAL_RE = re.compile(r"load\s*\(\s*['\"]\.[\w./\\-]+\.star['\"]")
LOAD_EXT_RE = re.compile(r"load\s*\(\s*['\"]ext://")
CONFIG_PARSE_RE = re.compile(r"\bconfig\.parse\s*\(")
LOCAL_KUBECTL_CONTEXT_RE = re.compile(
    r"local\s*\(\s*['\"]kubectl\s+config\s+current-context", re.IGNORECASE
)
FAIL_RE = re.compile(r"\bfail\s*\(")


def _parse_tiltfile(content):
    """Best-effort parsing of a Tiltfile to count features.

    Uses regex over the file text. Not a full Starlark parser.
    """
    if not content:
        return {}

    lines = content.splitlines()
    line_count = len(lines)

    # Count occurrences of key calls
    info = {
        "line_count": line_count,
        "docker_build_count": len(DOCKER_BUILD_RE.findall(content)),
        "custom_build_count": len(CUSTOM_BUILD_RE.findall(content)),
        "docker_build_with_restart_count": len(DOCKER_BUILD_RESTART_RE.findall(content)),
        "k8s_yaml_count": len(K8S_YAML_RE.findall(content)),
        "k8s_resource_count": len(K8S_RESOURCE_RE.findall(content)),
        "helm_count": len(HELM_RE.findall(content)),
        "live_update_count": len(LIVE_UPDATE_RE.findall(content)),
        "sync_count": len(SYNC_RE.findall(content)),
        "run_call_count": len(RUN_RE.findall(content)),
        "fall_back_on_count": len(FALL_BACK_ON_RE.findall(content)),
        "deprecated_restart_container_count": len(RESTART_CONTAINER_RE.findall(content)),
        "has_allow_k8s_contexts": bool(ALLOW_K8S_CONTEXTS_RE.search(content)),
        "has_watch_settings": bool(WATCH_SETTINGS_RE.search(content)),
        "has_update_settings": bool(UPDATE_SETTINGS_RE.search(content)),
        "has_local_kubectl_context_guard": bool(LOCAL_KUBECTL_CONTEXT_RE.search(content)),
        "has_fail_call": bool(FAIL_RE.search(content)),
        "has_config_parse": bool(CONFIG_PARSE_RE.search(content)),
        "loads_local_starfiles": bool(LOAD_LOCAL_RE.search(content)),
        "loads_extensions": bool(LOAD_EXT_RE.search(content)),
    }

    # Manual context guard heuristic
    info["has_manual_context_guard"] = (
        info["has_local_kubectl_context_guard"] and info["has_fail_call"]
    )

    # Production pattern blocks in the guard
    info["guard_blocks_eks"] = "arn:aws:eks:" in content
    info["guard_blocks_gke"] = "gke_" in content

    # max_parallel_updates explicitly set
    mpu_match = re.search(
        r"update_settings\s*\([^)]*max_parallel_updates\s*=\s*(\d+)", content
    )
    info["max_parallel_updates"] = int(mpu_match.group(1)) if mpu_match else None

    return info


def detect_tiltfile(project_root):
    """Find and parse Tiltfile."""
    path = _find_tiltfile(project_root)
    if not path:
        return {"exists": False}

    rel = path.relative_to(project_root)
    info = {"exists": True, "path": str(rel)}
    content = _read_safe(path)
    if content is None:
        info["read_error"] = True
        return info

    info.update(_parse_tiltfile(content))
    return info


def detect_tilt_layout(project_root):
    """Detect modular `tilt/` layout (also recognizes legacy `.tilt/`)."""
    root = Path(project_root)
    tilt_dir_candidates = [root / "tilt", root / ".tilt"]

    for tilt_dir in tilt_dir_candidates:
        if tilt_dir.is_dir():
            star_files = sorted([f.name for f in tilt_dir.glob("*.star")])
            yaml_files = sorted([
                f.name for f in tilt_dir.iterdir()
                if f.is_file() and f.suffix in (".yaml", ".yml")
            ])
            return {
                "exists": True,
                "path": str(tilt_dir.relative_to(root)),
                "star_files": star_files,
                "yaml_files": yaml_files,
                "is_modular": len(star_files) >= 1,
            }

    return {"exists": False}


def detect_tiltignore(project_root):
    """Check for .tiltignore."""
    root = Path(project_root)
    candidates = [root / ".tiltignore", root / "tilt" / ".tiltignore"]
    for path in candidates:
        if path.exists():
            return {"exists": True, "path": str(path.relative_to(root))}
    return {"exists": False}


def detect_tilt_config_json(project_root):
    """Check for tilt_config.json (CLI default args)."""
    root = Path(project_root)
    candidates = [root / "tilt_config.json", root / "tilt" / "tilt_config.json"]
    for path in candidates:
        if path.exists():
            return {"exists": True, "path": str(path.relative_to(root))}
    return {"exists": False}


# ---------------------------------------------------------------------------
# Ecosystem detection
# ---------------------------------------------------------------------------

def _has_spring_boot(check_dir):
    """Heuristic: Spring Boot dependency present in build files."""
    for fname in ("build.gradle.kts", "build.gradle", "pom.xml"):
        f = check_dir / fname
        if f.exists():
            content = _read_safe(f) or ""
            if "spring-boot" in content or "springframework.boot" in content:
                return True
    return False


def _has_nextjs(check_dir):
    """Heuristic: Next.js project markers."""
    for fname in ("next.config.js", "next.config.ts", "next.config.mjs"):
        if (check_dir / fname).exists():
            return True
    pkg = check_dir / "package.json"
    if pkg.exists():
        content = _read_safe(pkg) or ""
        if '"next"' in content:
            return True
    return False


def detect_ecosystems(project_root):
    """Detect project ecosystems from marker files."""
    root = Path(project_root)
    ecosystems = []

    # Walk root + one level + monorepo container subdirs (apps, services, packages)
    dirs_to_check = [root]
    monorepo_parents = {"apps", "packages", "libs", "services", "modules", "backend", "frontend"}
    try:
        for entry in sorted(root.iterdir()):
            if entry.is_dir() and not entry.name.startswith("."):
                dirs_to_check.append(entry)
                if entry.name in monorepo_parents:
                    try:
                        for sub in sorted(entry.iterdir()):
                            if sub.is_dir() and not sub.name.startswith("."):
                                dirs_to_check.append(sub)
                    except OSError:
                        pass
    except OSError:
        pass

    seen = set()

    for check_dir in dirs_to_check:
        rel = str(check_dir.relative_to(root)) if check_dir != root else "."

        # Java/Gradle (split out Spring Boot)
        for fname in ("build.gradle.kts", "build.gradle", "pom.xml"):
            if (check_dir / fname).exists():
                eco_key = ("java-gradle" if "gradle" in fname else "java-maven", rel)
                if eco_key not in seen:
                    eco = {
                        "ecosystem": eco_key[0],
                        "build_file": fname,
                        "root": rel,
                        "is_spring_boot": _has_spring_boot(check_dir),
                    }
                    ecosystems.append(eco)
                    seen.add(eco_key)
                break

        # Next.js (separate from generic node)
        if (check_dir / "package.json").exists():
            if _has_nextjs(check_dir):
                key = ("nextjs", rel)
                if key not in seen:
                    ecosystems.append({"ecosystem": "nextjs", "root": rel})
                    seen.add(key)
            else:
                key = ("node", rel)
                if key not in seen:
                    eco = {"ecosystem": "node", "root": rel}
                    if (check_dir / "pnpm-lock.yaml").exists():
                        eco["package_manager"] = "pnpm"
                    elif (check_dir / "yarn.lock").exists():
                        eco["package_manager"] = "yarn"
                    elif (check_dir / "package-lock.json").exists():
                        eco["package_manager"] = "npm"
                    else:
                        eco["package_manager"] = "unknown"
                    ecosystems.append(eco)
                    seen.add(key)

        # Python
        if (check_dir / "pyproject.toml").exists():
            key = ("python", rel)
            if key not in seen:
                eco = {"ecosystem": "python", "root": rel}
                if (check_dir / "uv.lock").exists():
                    eco["package_manager"] = "uv"
                elif (check_dir / "poetry.lock").exists():
                    eco["package_manager"] = "poetry"
                elif (check_dir / "Pipfile.lock").exists():
                    eco["package_manager"] = "pipenv"
                else:
                    eco["package_manager"] = "pip"
                ecosystems.append(eco)
                seen.add(key)
        elif (check_dir / "requirements.txt").exists():
            key = ("python", rel)
            if key not in seen:
                ecosystems.append({
                    "ecosystem": "python", "package_manager": "pip", "root": rel
                })
                seen.add(key)

    # Docker artifacts at root
    has_dockerfile = (root / "Dockerfile").exists() or (root / "Dockerfile.dev").exists()
    has_compose = any(
        (root / f).exists()
        for f in ("docker-compose.yml", "docker-compose.yaml", "compose.yml", "compose.yaml")
    )
    # Look in k8s/ or manifests/ for raw YAML
    has_k8s_manifests = False
    for sub in ("k8s", "kubernetes", "manifests", "deploy"):
        d = root / sub
        if d.is_dir():
            try:
                if any(p.suffix in (".yaml", ".yml") for p in d.iterdir() if p.is_file()):
                    has_k8s_manifests = True
                    break
            except OSError:
                pass

    if has_dockerfile or has_compose or has_k8s_manifests:
        ecosystems.append({
            "ecosystem": "infra",
            "has_dockerfile": has_dockerfile,
            "has_compose": has_compose,
            "has_k8s_manifests": has_k8s_manifests,
            "root": ".",
        })

    return ecosystems


# ---------------------------------------------------------------------------
# Local cluster detection (best-effort, uses kubectl context)
# ---------------------------------------------------------------------------

def detect_local_clusters_available():
    """Check which local cluster tools are installed (informational)."""
    return {
        "minikube": shutil.which("minikube") is not None,
        "kind": shutil.which("kind") is not None,
        "k3d": shutil.which("k3d") is not None,
        "colima": shutil.which("colima") is not None,
        "orbstack": shutil.which("orb") is not None or shutil.which("orbstack") is not None,
    }


# ---------------------------------------------------------------------------
# Audit rules (TILT001 - TILT025)
# ---------------------------------------------------------------------------

def _violation(rule, severity, message, fix_hint, **extra):
    v = {"rule": rule, "severity": severity, "message": message, "fix_hint": fix_hint}
    v.update(extra)
    return v


def audit_tiltfile(project_root, tiltfile_info, tilt_layout, tiltignore_info,
                   tilt_config_info, ecosystems):
    """Run TILT001-TILT025 audit rules. Returns dict with violations + summary."""
    violations = []

    if not tiltfile_info.get("exists"):
        return {"violations": violations, "summary": _empty_summary()}

    # Compute service count heuristic — number of k8s_resource calls is the
    # best proxy for "deployed service count" in Tilt projects.
    service_count = max(
        tiltfile_info.get("k8s_resource_count", 0),
        tiltfile_info.get("docker_build_count", 0)
        + tiltfile_info.get("custom_build_count", 0),
    )

    # Read full Tiltfile content for line-level rules
    tilt_path = Path(project_root) / tiltfile_info["path"]
    content = _read_safe(tilt_path) or ""

    # ----- TILT001: No production safety guard -----
    has_safety = (
        tiltfile_info.get("has_allow_k8s_contexts")
        or tiltfile_info.get("has_manual_context_guard")
    )
    if not has_safety:
        violations.append(_violation(
            "TILT001", "ERROR",
            "No production safety guard in Tiltfile",
            "Add allow_k8s_contexts(['docker-desktop', 'kind-...']) or a manual "
            "validate_cluster_safety() guard at the top of Tiltfile",
        ))

    # ----- TILT002: Manual guard doesn't block dangerous patterns -----
    if tiltfile_info.get("has_manual_context_guard"):
        missing = []
        if not tiltfile_info.get("guard_blocks_eks"):
            missing.append("EKS ARN ('arn:aws:eks:')")
        if not tiltfile_info.get("guard_blocks_gke"):
            missing.append("GKE prefix ('gke_')")
        if missing:
            violations.append(_violation(
                "TILT002", "ERROR",
                "Manual context guard missing dangerous patterns: " + ", ".join(missing),
                "Add the missing patterns to the blocklist in validate_cluster_safety()",
            ))

    # ----- TILT003: tilt_config.json contains secrets -----
    if tilt_config_info.get("exists"):
        cfg_content = _read_safe(Path(project_root) / tilt_config_info["path"]) or ""
        secret_patterns = [
            r'"(api[_-]?key|password|token|secret|credentials?)"\s*:\s*"[^"]+"',
        ]
        for pat in secret_patterns:
            if re.search(pat, cfg_content, re.IGNORECASE):
                violations.append(_violation(
                    "TILT003", "ERROR",
                    "tilt_config.json appears to contain secrets",
                    "Move secrets to .env (gitignored) and read them via os.getenv() in Tiltfile",
                ))
                break

    # ----- TILT004: docker_build without live_update -----
    # Best-effort — check if the file has docker_build calls but no live_update= arguments
    if tiltfile_info.get("docker_build_count", 0) > 0 and tiltfile_info.get("live_update_count", 0) == 0:
        violations.append(_violation(
            "TILT004", "WARNING",
            "docker_build() used without live_update=",
            "Add live_update=[sync(...), run(...), fall_back_on(...)] for fast inner loop",
        ))

    # ----- TILT005: custom_build without live_update -----
    if tiltfile_info.get("custom_build_count", 0) > 0 and tiltfile_info.get("live_update_count", 0) == 0:
        violations.append(_violation(
            "TILT005", "WARNING",
            "custom_build() used without live_update=",
            "Add live_update= with sync() of compiled artifacts; pair with local_resource compile",
        ))

    # ----- TILT007: No watch_settings AND no .tiltignore -----
    if not tiltfile_info.get("has_watch_settings") and not tiltignore_info.get("exists"):
        violations.append(_violation(
            "TILT007", "WARNING",
            "No watch_settings(ignore=[...]) and no .tiltignore file",
            "Add .tiltignore with build/, .gradle/, node_modules/, __pycache__/, *.log",
        ))

    # ----- TILT008: live_update has run() but no sync() -----
    if (
        tiltfile_info.get("run_call_count", 0) > 0
        and tiltfile_info.get("sync_count", 0) == 0
        and tiltfile_info.get("live_update_count", 0) > 0
    ):
        violations.append(_violation(
            "TILT008", "WARNING",
            "live_update uses run() with no sync() steps",
            "Add sync(local, remote) before run(); run-only live_update doesn't transfer files",
        ))

    # ----- TILT010: Missing .tiltignore -----
    if not tiltignore_info.get("exists"):
        violations.append(_violation(
            "TILT010", "INFO",
            "No .tiltignore file in Tiltfile directory",
            "Create .tiltignore with build/, dist/, .gradle/, node_modules/, __pycache__/, *.log",
        ))

    # ----- TILT011: k8s_yaml without k8s_resource -----
    if (
        tiltfile_info.get("k8s_yaml_count", 0) > 0
        and tiltfile_info.get("k8s_resource_count", 0) == 0
    ):
        violations.append(_violation(
            "TILT011", "INFO",
            "k8s_yaml() used without any k8s_resource() calls",
            "Add k8s_resource() to wire up port_forwards, labels, and resource_deps",
        ))

    # ----- TILT012: No update_settings parallelism cap (4+ services) -----
    if service_count >= 4 and not tiltfile_info.get("has_update_settings"):
        violations.append(_violation(
            "TILT012", "INFO",
            "No update_settings(max_parallel_updates=N) with 4+ services",
            "Add update_settings(max_parallel_updates=2) (or 3) to cap CPU load",
        ))

    # ----- TILT016: live_update without fall_back_on -----
    if (
        tiltfile_info.get("live_update_count", 0) > 0
        and tiltfile_info.get("fall_back_on_count", 0) == 0
    ):
        violations.append(_violation(
            "TILT016", "INFO",
            "live_update has no fall_back_on() for config files",
            "Add fall_back_on(['Dockerfile', 'package.json', 'pyproject.toml']) "
            "to trigger full rebuild on config changes",
        ))

    # ----- TILT020: Tiltfile > 300 lines without modularization -----
    if (
        tiltfile_info.get("line_count", 0) > 300
        and not tiltfile_info.get("loads_local_starfiles")
    ):
        violations.append(_violation(
            "TILT020", "INFO",
            f"Tiltfile is {tiltfile_info['line_count']} lines with no .star modules",
            "Extract service deployment logic to tilt/services.star and config to tilt/config.star",
        ))

    # ----- TILT022: Hardcoded service list (no YAML config) -----
    if (
        service_count >= 4
        and tilt_layout.get("exists")
        and not any(f.endswith(".yaml") or f.endswith(".yml")
                    for f in tilt_layout.get("yaml_files", []))
    ):
        layout_path = tilt_layout.get("path", "tilt")
        violations.append(_violation(
            "TILT022", "INFO",
            "Modular layout exists but no YAML config files for service definitions",
            f"Extract service definitions to {layout_path}/service-config.yaml and "
            "load via read_yaml() for cleaner configuration",
        ))

    # ----- TILT023: Deprecated restart_container() used -----
    if tiltfile_info.get("deprecated_restart_container_count", 0) > 0:
        violations.append(_violation(
            "TILT023", "WARNING",
            "Deprecated restart_container() used in live_update",
            "Replace with ext://restart_process: load('ext://restart_process', "
            "'docker_build_with_restart')",
        ))

    # ----- TILT025: No tilt_config.json with team defaults -----
    if (
        tiltfile_info.get("has_config_parse")
        and not tilt_config_info.get("exists")
    ):
        violations.append(_violation(
            "TILT025", "INFO",
            "config.parse() used but no tilt_config.json with team defaults",
            "Create tilt_config.json with sensible default values for the defined CLI args",
        ))

    # ----- Line-level rules: TILT017 (no labels), TILT013 (resource without labels) -----
    # Detect k8s_resource() calls without labels= parameter
    k8s_resource_blocks = re.findall(
        r"k8s_resource\s*\(([^)]*)\)", content, re.DOTALL
    )
    missing_labels = sum(1 for b in k8s_resource_blocks if "labels=" not in b and "labels =" not in b)
    if missing_labels >= 2:
        violations.append(_violation(
            "TILT013", "INFO",
            f"{missing_labels} k8s_resource() calls have no labels= parameter",
            "Add labels=['services'] / labels=['infrastructure'] for UI grouping",
        ))

    # ----- Build summary -----
    return {"violations": violations, "summary": _summarize(violations)}


def _empty_summary():
    return {"total": 0, "errors": 0, "warnings": 0, "info": 0, "suggestions": 0}


def _summarize(violations):
    summary = _empty_summary()
    summary["total"] = len(violations)
    for v in violations:
        sev = v["severity"].lower()
        if sev == "error":
            summary["errors"] += 1
        elif sev == "warning":
            summary["warnings"] += 1
        elif sev == "info":
            summary["info"] += 1
        elif sev == "suggestion":
            summary["suggestions"] += 1
    return summary


# ---------------------------------------------------------------------------
# Main detection
# ---------------------------------------------------------------------------

def detect(project_root, audit=True):
    """Run all detection checks and return structured results."""
    tiltfile_info = detect_tiltfile(project_root)
    tilt_layout = detect_tilt_layout(project_root)
    tiltignore_info = detect_tiltignore(project_root)
    tilt_config_info = detect_tilt_config_json(project_root)
    ecosystems = detect_ecosystems(project_root)

    result = {
        "tilt_binary": detect_tool("tilt", ["tilt", "version"]),
        "kubectl_binary": detect_tool("kubectl", ["kubectl", "version", "--client"]),
        "kubectl_context": detect_kubectl_context(),
        "tiltfile": tiltfile_info,
        "tilt_layout": tilt_layout,
        "tiltignore": tiltignore_info,
        "tilt_config_json": tilt_config_info,
        "ecosystems": ecosystems,
        "local_cluster_tools": detect_local_clusters_available(),
        "os": detect_os(),
    }

    if audit and tiltfile_info.get("exists"):
        result["audit"] = audit_tiltfile(
            project_root, tiltfile_info, tilt_layout,
            tiltignore_info, tilt_config_info, ecosystems,
        )

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Detect Tilt installation and audit Tiltfile configurations"
    )
    parser.add_argument(
        "project_root", nargs="?", default=os.getcwd(),
        help="Path to the project root directory",
    )
    parser.add_argument(
        "--no-audit", action="store_true",
        help="Skip audit checks (detection only)",
    )
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    if not root.is_dir():
        json.dump(
            {"error": "not_a_directory", "path": str(root)},
            sys.stdout, indent=2,
        )
        sys.exit(1)

    result = detect(str(root), audit=not args.no_audit)
    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()

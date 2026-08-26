#!/usr/bin/env python3
"""
Security Scanner for SKILL.md files
Implements automated security checks for skill registry
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, TextIO, Tuple

import jsonschema
import yaml
from security_blocklist import blocked_metadata_source, load_security_blocklist
from security_rules import (
    BUNDLED_BINARY_EXTENSIONS,
    BUNDLED_SCAN_DIRS,
    BUNDLED_SCAN_EXTENSIONS,
    BUNDLED_SCAN_ROOT_FILES,
    COMPILED_DANGEROUS_PATTERNS,
    CREDENTIAL_PATTERNS,
    DANGEROUS_PATTERNS,
    INJECTION_PATTERNS,
    OBFUSCATION_EXEC_PATTERNS,
    SENSITIVE_PATHS,
)
from security_scope import discover_scan_targets, resolve_scan_file_list
from utils import split_frontmatter_content

# Load schema
SCHEMA_PATH = Path(__file__).parent.parent / "schema" / "skill.schema.json"
SECURITY_SCANNER_NAME = "claude-skill-registry-security-scanner"
SECURITY_SCANNER_VERSION = "1.1.4"


def utc_now_isoformat() -> str:
    """Return a stable UTC timestamp string for scan evidence."""
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonical_json_sha256(payload: object) -> str:
    """Hash a JSON-compatible payload using stable key and separator rules."""
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def security_ruleset_hash() -> str:
    """Hash the scanner rules that affect security decisions."""
    return canonical_json_sha256(
        {
            "scanner_name": SECURITY_SCANNER_NAME,
            "scanner_version": SECURITY_SCANNER_VERSION,
            "dangerous_patterns": DANGEROUS_PATTERNS,
            "credential_patterns": {
                name: pattern.pattern for name, pattern in CREDENTIAL_PATTERNS.items()
            },
            "obfuscation_exec_patterns": [pattern.pattern for pattern in OBFUSCATION_EXEC_PATTERNS],
            "injection_patterns": [pattern.pattern for pattern in INJECTION_PATTERNS],
            "sensitive_paths": SENSITIVE_PATHS,
            "bundled_scan_dirs": BUNDLED_SCAN_DIRS,
            "bundled_scan_root_files": BUNDLED_SCAN_ROOT_FILES,
            "bundled_scan_extensions": sorted(BUNDLED_SCAN_EXTENSIONS),
            "bundled_binary_extensions": sorted(BUNDLED_BINARY_EXTENSIONS),
        }
    )


def source_content_hash(skill_dir: Path) -> str:
    """Hash archived source content without generated metadata."""
    digest = hashlib.sha256()
    for path in sorted(skill_dir.rglob("*")):
        if not path.is_file() or path.name == "metadata.json":
            continue
        rel_path = path.relative_to(skill_dir).as_posix()
        digest.update(rel_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update(hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def load_skill_metadata(skill_dir: Path) -> dict:
    """Load archive metadata when available."""
    metadata_path = skill_dir / "metadata.json"
    if not metadata_path.exists():
        return {}
    try:
        payload = json.loads(metadata_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


class SecurityScanner:
    """Security scanner for SKILL.md files"""

    def __init__(self, schema_path: str = None, require_metadata: bool = False):
        self.schema_path = schema_path or SCHEMA_PATH
        self.schema = self._load_schema()
        self.security_blocklist = load_security_blocklist()
        self.require_metadata = require_metadata
        self.issues = []

    def _load_schema(self) -> dict:
        """Load JSON Schema"""
        with open(self.schema_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def scan_file(self, skill_path: Path) -> Tuple[bool, List[Dict]]:
        """
        Scan a SKILL.md file for security issues
        Returns: (is_safe, issues_list)
        """
        self.issues = []

        if not skill_path.exists():
            self.issues.append(
                {
                    "severity": "error",
                    "type": "file_not_found",
                    "message": f"File not found: {skill_path}",
                }
            )
            return False, self.issues

        try:
            content = skill_path.read_text(encoding="utf-8")
        except Exception as e:
            self.issues.append(
                {"severity": "error", "type": "read_error", "message": f"Cannot read file: {e}"}
            )
            return False, self.issues

        return self.scan_content(content, skill_path)

    def scan_content(self, content: str, skill_path: Path) -> Tuple[bool, List[Dict]]:
        """Scan supplied SKILL.md text while resolving support files from its directory."""
        self.issues = []

        # 1. Validate file size
        if len(content) > 1_000_000:  # 1MB limit
            self.issues.append(
                {
                    "severity": "error",
                    "type": "file_too_large",
                    "message": f"File size {len(content)} exceeds 1MB limit",
                }
            )

        # 2. Extract and validate frontmatter
        frontmatter = self._extract_frontmatter(content)
        if frontmatter:
            self._validate_schema(frontmatter)
        elif not any(issue.get("type") == "yaml_parse_error" for issue in self.issues):
            self.issues.append(
                {
                    "severity": "error",
                    "type": "no_frontmatter",
                    "message": "SKILL.md must have YAML frontmatter",
                }
            )

        # 3. Scan for dangerous patterns
        self._scan_dangerous_patterns(content, skill_path)

        # 4. Check for sensitive paths
        self._scan_sensitive_paths(content)

        # 5. Check bundled scripts and reference implementations
        self._scan_bundled_files(skill_path.parent)

        # 6. Block known malicious or high-risk source repositories
        self._scan_blocked_source(skill_path)

        # 7. Prompt injection detection
        self._detect_prompt_injection(content)

        # 8. Hardcoded credentials detection
        self._detect_credentials(content, skill_path)

        # 9. Obfuscation-to-execution chains
        self._detect_obfuscation_exec(content, skill_path)

        has_error = any(i["severity"] == "error" for i in self.issues)
        return not has_error, self.issues

    def build_security_decision(
        self,
        skill_path: Path,
        is_safe: bool,
        issues: List[Dict],
        scanned_at: str,
    ) -> Dict:
        """Build a per-skill fail-closed security decision with provenance."""
        skill_dir = skill_path.parent
        metadata = load_skill_metadata(skill_dir)
        error_count = sum(1 for issue in issues if issue.get("severity") == "error")
        warning_count = sum(1 for issue in issues if issue.get("severity") == "warning")
        status = "passed" if is_safe else "failed"
        reason = "no_errors" if is_safe else "scanner_errors"
        for issue_type in (
            "blocked_source",
            "metadata_missing",
            "metadata_read_error",
            "undecodable_executable",
            "bundled_text_decode_error",
            "bundled_file_read_error",
        ):
            if any(issue.get("type") == issue_type for issue in issues):
                reason = issue_type
                break

        source_repo = str(metadata.get("repo") or "")
        source_path = str(metadata.get("path") or metadata.get("github_path") or "")
        source_ref = str(metadata.get("github_branch") or metadata.get("branch") or "")
        content_sha256 = source_content_hash(skill_dir)
        ruleset_sha256 = security_ruleset_hash()
        decision_payload = {
            "status": status,
            "reason": reason,
            "source_repo": source_repo,
            "source_path": source_path,
            "source_ref": source_ref,
            "content_sha256": content_sha256,
            "scanner_version": SECURITY_SCANNER_VERSION,
            "ruleset_sha256": ruleset_sha256,
            "error_count": error_count,
            "warning_count": warning_count,
            "require_metadata": self.require_metadata,
        }

        return {
            "id": canonical_json_sha256(decision_payload),
            "status": status,
            "reason": reason,
            "policy": {"require_metadata": self.require_metadata},
            "scanner": {
                "name": SECURITY_SCANNER_NAME,
                "version": SECURITY_SCANNER_VERSION,
                "ruleset_sha256": ruleset_sha256,
            },
            "provenance": {
                "source_repo": source_repo,
                "source_path": source_path,
                "source_ref": source_ref,
                "source_url": str(metadata.get("source_url") or ""),
                "content_sha256": content_sha256,
                "scanned_at": scanned_at,
            },
            "issue_count": len(issues),
            "error_count": error_count,
            "warning_count": warning_count,
        }

    def _extract_frontmatter(self, content: str) -> dict:
        """Extract YAML frontmatter from SKILL.md"""
        frontmatter, _body = split_frontmatter_content(content)
        if frontmatter is None:
            return None

        try:
            # Use safe_load to prevent YAML deserialization attacks
            return yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            self.issues.append(
                {
                    "severity": "error",
                    "type": "yaml_parse_error",
                    "message": f"Invalid YAML frontmatter: {e}",
                }
            )
            return None

    def _validate_schema(self, frontmatter: dict):
        """Validate frontmatter against JSON Schema"""
        try:
            jsonschema.validate(instance=frontmatter, schema=self.schema)
        except jsonschema.ValidationError as e:
            self.issues.append(
                {
                    "severity": "warning",
                    "type": "schema_validation",
                    "message": f"Schema validation failed: {e.message}",
                    "path": list(e.path),
                }
            )
        except jsonschema.SchemaError as e:
            self.issues.append(
                {"severity": "error", "type": "schema_error", "message": f"Invalid schema: {e}"}
            )

    def _scan_dangerous_patterns(self, content: str, file_path: Path):
        """Scan for dangerous code patterns"""
        lines = content.split("\n")

        for pattern_name, pattern in COMPILED_DANGEROUS_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    critical_patterns = {
                        "eval",
                        "exec",
                        "__import__",
                        "os.system",
                        "yaml.load",
                        "yaml.unsafe_load",
                        "shell=True",
                        "php_request_exec",
                        "php_eval_request",
                        "reverse_shell_dev_tcp",
                        "curl_pipe_shell",
                        "nc_exec_shell",
                    }
                    severity = "error" if pattern_name in critical_patterns else "warning"

                    self.issues.append(
                        {
                            "severity": severity,
                            "type": "dangerous_pattern",
                            "pattern": pattern_name,
                            "file": str(file_path),
                            "line": line_num,
                            "message": f'Dangerous pattern "{pattern_name}" found',
                            "code": line.strip(),
                        }
                    )

    def _scan_sensitive_paths(self, content: str):
        """Check for references to sensitive file paths"""
        for path in SENSITIVE_PATHS:
            if path in content:
                self.issues.append(
                    {
                        "severity": "warning",
                        "type": "sensitive_path",
                        "message": f"References sensitive path: {path}",
                    }
                )

    def _scan_bundled_files(self, skill_dir: Path):
        """Scan bundled executable/reference files."""
        for bundled_file in sorted(skill_dir.rglob("*")):
            if not bundled_file.is_file():
                continue

            rel_path = bundled_file.relative_to(skill_dir)
            if rel_path.as_posix() in {"SKILL.md", "metadata.json"}:
                continue

            if not self._check_bundled_file_size(bundled_file):
                continue

            is_known_text = (
                bundled_file.suffix.lower() in BUNDLED_SCAN_EXTENSIONS
                or bundled_file.name in BUNDLED_SCAN_ROOT_FILES
            )
            is_bin_file = any(part.lower() == "bin" for part in rel_path.parts)
            is_executable = bool(bundled_file.stat().st_mode & 0o111)
            looks_like_text = False
            if not is_known_text:
                try:
                    bundled_file.read_text(encoding="utf-8")
                    looks_like_text = True
                except (OSError, UnicodeDecodeError):
                    looks_like_text = False
            has_shebang = False
            if not (is_known_text or looks_like_text or is_bin_file or is_executable):
                try:
                    with bundled_file.open("rb") as handle:
                        has_shebang = handle.read(2) == b"#!"
                except OSError as exc:
                    self._record_bundled_read_error(bundled_file, exc)
                    continue

            executable_like = is_bin_file or is_executable or has_shebang
            if is_known_text or looks_like_text or executable_like:
                self._scan_bundled_text_file(
                    bundled_file,
                    executable_like=executable_like,
                )

    def _check_bundled_file_size(self, bundled_file: Path) -> bool:
        """Return False and record an issue when an archived support file is too large."""
        try:
            size = bundled_file.stat().st_size
        except OSError as exc:
            self._record_bundled_read_error(bundled_file, exc)
            return False
        if size > 10_000_000:  # 10MB
            self.issues.append(
                {
                    "severity": "error",
                    "type": "file_too_large",
                    "file": str(bundled_file),
                    "message": f"Bundled file too large: {size} bytes",
                }
            )
            return False
        return True

    def _record_bundled_read_error(self, bundled_file: Path, exc: OSError):
        """Record explicit quarantine evidence for an unreadable support file."""
        self.issues.append(
            {
                "severity": "error",
                "type": "bundled_file_read_error",
                "action": "quarantine",
                "file": str(bundled_file),
                "message": f"Cannot inspect bundled support file: {exc}",
            }
        )

    def _scan_bundled_text_file(self, bundled_file: Path, executable_like: bool = False):
        """Scan an archived support file when it is text-like executable input."""
        try:
            content = bundled_file.read_text(encoding="utf-8")
            self._scan_dangerous_patterns(content, bundled_file)
            self._detect_credentials(content, bundled_file)
            self._detect_obfuscation_exec(content, bundled_file)
        except UnicodeDecodeError as exc:
            issue_type = (
                "undecodable_executable" if executable_like else "bundled_text_decode_error"
            )
            self.issues.append(
                {
                    "severity": "error",
                    "type": issue_type,
                    "action": "quarantine",
                    "file": str(bundled_file),
                    "message": f"Bundled support file is not valid UTF-8 text: {exc}",
                }
            )
        except OSError as exc:
            self._record_bundled_read_error(bundled_file, exc)

    def _scan_blocked_source(self, skill_path: Path):
        """Fail archived skills sourced from a repo on the security blocklist."""
        metadata_path = skill_path.parent / "metadata.json"
        if not metadata_path.exists():
            if self.require_metadata:
                self.issues.append(
                    {
                        "severity": "error",
                        "type": "metadata_missing",
                        "file": str(metadata_path),
                        "message": "Required archive metadata.json is missing",
                    }
                )
            return

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            self.issues.append(
                {
                    "severity": "error",
                    "type": "metadata_read_error",
                    "file": str(metadata_path),
                    "message": f"Cannot read metadata for blocklist scan: {exc}",
                }
            )
            return

        if not isinstance(metadata, dict):
            self.issues.append(
                {
                    "severity": "error",
                    "type": "metadata_read_error",
                    "file": str(metadata_path),
                    "message": "Archive metadata must be a JSON object",
                }
            )
            return

        blocked_source = blocked_metadata_source(metadata, self.security_blocklist)
        if not blocked_source:
            return
        blocked_entry, source_field = blocked_source

        self.issues.append(
            {
                "severity": "error",
                "type": "blocked_source",
                "file": str(metadata_path),
                "repo": blocked_entry["repo"],
                "metadata_field": source_field,
                "message": (
                    f'Skill source repo "{blocked_entry["repo"]}" is blocked: '
                    f'{blocked_entry.get("reason", "security blocklist")}'
                ),
            }
        )

    def _detect_credentials(self, content: str, file_path: Path):
        """Detect hardcoded credentials and secret key formats"""
        lines = content.split("\n")
        for cred_name, pattern in CREDENTIAL_PATTERNS.items():
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    self.issues.append(
                        {
                            "severity": "error",
                            "type": "hardcoded_credential",
                            "pattern": cred_name,
                            "file": str(file_path),
                            "line": line_num,
                            "message": f'Hardcoded credential "{cred_name}" detected',
                        }
                    )

    def _detect_obfuscation_exec(self, content: str, file_path: Path):
        """Detect base64-decode-to-execution chains"""
        lines = content.split("\n")
        for pattern in OBFUSCATION_EXEC_PATTERNS:
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    self.issues.append(
                        {
                            "severity": "error",
                            "type": "obfuscation_exec",
                            "file": str(file_path),
                            "line": line_num,
                            "message": "Base64-decode-to-execution chain detected",
                            "code": line.strip()[:120],
                        }
                    )

    def _detect_prompt_injection(self, content: str):
        """Detect potential prompt injection attempts"""
        for pattern in INJECTION_PATTERNS:
            if pattern.search(content):
                self.issues.append(
                    {
                        "severity": "warning",
                        "type": "prompt_injection",
                        "message": f"Potential prompt injection detected: {pattern.pattern}",
                    }
                )

    def generate_report(self) -> str:
        """Generate human-readable report"""
        if not self.issues:
            return "✓ No security issues found"

        report = []
        errors = [i for i in self.issues if i["severity"] == "error"]
        warnings = [i for i in self.issues if i["severity"] == "warning"]

        if errors:
            report.append(f"❌ {len(errors)} ERROR(S):")
            for issue in errors:
                report.append(f"  - {issue['type']}: {issue['message']}")

        if warnings:
            report.append(f"⚠️  {len(warnings)} WARNING(S):")
            for issue in warnings:
                report.append(f"  - {issue['type']}: {issue['message']}")

        return "\n".join(report)


def scan_directory(
    skills_dir: Path,
    output_file: Path = None,
    quiet: bool = False,
    selected_files: List[Path] = None,
    scanned_at: str = "",
    progress_interval: int = 0,
    progress_stream: TextIO | None = None,
    require_metadata: bool = False,
) -> Dict:
    """Scan all skills in a directory"""
    scanner = SecurityScanner(require_metadata=require_metadata)
    skills_root = skills_dir.resolve()
    scan_timestamp = scanned_at or utc_now_isoformat()
    ruleset_sha256 = security_ruleset_hash()
    results = {
        "scanner": {
            "name": SECURITY_SCANNER_NAME,
            "version": SECURITY_SCANNER_VERSION,
            "ruleset_sha256": ruleset_sha256,
        },
        "generated_at": scan_timestamp,
        "scan_policy": {"require_metadata": require_metadata},
        "total": 0,
        "passed": 0,
        "failed": 0,
        "skills": [],
    }

    if selected_files is None:
        scan_targets = discover_scan_targets(skills_dir)
    else:
        scan_targets = selected_files

    if progress_interval < 0:
        raise ValueError("progress_interval must be non-negative")
    if progress_interval and progress_stream is None:
        progress_stream = sys.stderr

    for skill_file in scan_targets:
        skill_file = skill_file.resolve()
        results["total"] += 1

        is_safe, issues = scanner.scan_file(skill_file)
        security_decision = scanner.build_security_decision(
            skill_file,
            is_safe,
            issues,
            scan_timestamp,
        )

        skill_result = {
            "path": str(skill_file.relative_to(skills_root)),
            "safe": is_safe,
            "security_decision": security_decision,
            "issues": issues,
        }

        results["skills"].append(skill_result)

        if is_safe:
            results["passed"] += 1
            if not quiet:
                print(f"✓ {skill_file.relative_to(skills_root)}")
        else:
            results["failed"] += 1
            if not quiet:
                print(f"✗ {skill_file.relative_to(skills_root)}")
                print(scanner.generate_report())

        if progress_interval and results["total"] % progress_interval == 0:
            print(
                "Security scan progress: "
                f"{results['total']} scanned, "
                f"{results['passed']} passed, "
                f"{results['failed']} failed",
                file=progress_stream,
                flush=True,
            )

    # Save results
    if output_file:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    return results


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Security scanner for SKILL.md files")
    parser.add_argument("path", help="Path to SKILL.md file or skills directory")
    parser.add_argument("--output", "-o", help="Output JSON report file")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Always exit 0 after writing report (for CI reporting mode)",
    )
    parser.add_argument("--quiet", action="store_true", help="Only print summary")
    parser.add_argument(
        "--require-metadata",
        action="store_true",
        help="Require readable metadata.json for every skill (archive publication mode)",
    )
    parser.add_argument(
        "--progress-interval",
        type=int,
        default=0,
        help="Print directory scan progress every N skills to stderr (0 disables progress)",
    )
    parser.add_argument(
        "--file-list",
        help="Optional newline-delimited list of SKILL.md paths to scan (absolute or relative to path)",
    )

    args = parser.parse_args()

    path = Path(args.path)

    if path.is_file():
        # Scan single file
        scanner = SecurityScanner(require_metadata=args.require_metadata)
        is_safe, issues = scanner.scan_file(path)
        scan_timestamp = utc_now_isoformat()
        security_decision = scanner.build_security_decision(
            path,
            is_safe,
            issues,
            scan_timestamp,
        )

        print(scanner.generate_report())

        if args.output:
            with open(args.output, "w") as f:
                json.dump(
                    {
                        "scanner": security_decision["scanner"],
                        "generated_at": scan_timestamp,
                        "scan_policy": {"require_metadata": args.require_metadata},
                        "safe": is_safe,
                        "security_decision": security_decision,
                        "issues": issues,
                    },
                    f,
                    indent=2,
                )

        if args.report_only:
            exit(0)
        exit(0 if is_safe else 1)

    elif path.is_dir():
        # Scan directory
        selected_files = None
        if args.file_list:
            selected_files = resolve_scan_file_list(path, Path(args.file_list))
            if not args.quiet:
                print(f"Using file list: {len(selected_files)} file(s)")

        results = scan_directory(
            path,
            args.output,
            quiet=args.quiet,
            selected_files=selected_files,
            progress_interval=args.progress_interval,
            require_metadata=args.require_metadata,
        )

        print(f"\n{'='*60}")
        print(f"Total: {results['total']}")
        print(f"Passed: {results['passed']}")
        print(f"Failed: {results['failed']}")

        if args.report_only:
            exit(0)
        exit(0 if results["failed"] == 0 else 1)

    else:
        print(f"Error: {path} not found")
        exit(1)


if __name__ == "__main__":
    main()

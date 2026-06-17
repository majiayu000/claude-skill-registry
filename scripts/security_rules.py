"""Security scanner rule definitions."""

import re

DANGEROUS_PATTERNS = {
    # Code execution
    "eval": r"\beval\s*\(",
    "exec": r"\bexec\s*\(",
    "__import__": r"\b__import__\s*\(",
    "compile": r"\bcompile\s*\(",
    # Command injection
    "os.system": r"os\.system\s*\(",
    "subprocess.call": r"subprocess\.(call|run|Popen)\s*\(",
    "shell=True": r"shell\s*=\s*True",
    # File system manipulation
    "os.remove": r"os\.(remove|unlink|rmdir)\s*\(",
    "shutil.rmtree": r"shutil\.rmtree\s*\(",
    # Network access (flag for review)
    "requests": r"import\s+requests",
    "urllib": r"import\s+urllib",
    "socket": r"import\s+socket",
    # YAML unsafe loading
    "yaml.load": r"yaml\.load\s*\(",
    "yaml.unsafe_load": r"yaml\.unsafe_load\s*\(",
    # Prompt injection indicators
    "ignore_previous": r"ignore\s+(previous|prior|above)",
    "disregard": r"disregard\s+(all|previous|prior)",
    "system_prompt": r"system[\s_-]?prompt",
    # Node.js dangerous patterns
    "child_process": r'require\s*\(\s*[\'"]child_process[\'"]\s*\)',
    "child_process_exec": r"child_process\.\w+\s*\(",
    "new_function": r"new\s+Function\s*\(",
    # Dangerous permissions & system modification
    "chmod_dangerous": r"chmod\s+(?:777|666|4755|[ug]\+s)",
    "sudo_shell": r"sudo\s+(?:sh|bash)\s+-c",
    # Untrusted package sources
    "pip_url_install": r"pip3?\s+install\s+(?:https?://|git\+)",
    "npm_url_install": r"npm\s+install\s+(?:https?://|git\+)",
    # Resource abuse
    "fork_bomb": r":\(\)\{\s*:\|:\s*&\s*\}\s*;\s*:",
}


CREDENTIAL_PATTERNS = {
    "aws_key": re.compile(r"(?:AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}"),
    "github_token": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "stripe_key": re.compile(r"(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{24,}"),
    "openai_compatible_api_key": re.compile(
        r"\b(?:apiKey|api_key|OPENAI_API_KEY|openai_api_key|Authorization)\b[^\n]{0,80}"
        r"sk-[A-Za-z0-9_-]{20,}"
    ),
    "google_api_key": re.compile(r"AIza[A-Za-z0-9_-]{35}"),
    "jwt_token": re.compile(r"eyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+"),
    "private_key_pem": re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"),
    "db_connection_string": re.compile(r"(?:mongodb|mysql|postgresql|postgres)://[^:\s]+:[^@\s]+@"),
}


OBFUSCATION_EXEC_PATTERNS = [
    re.compile(
        r"base64\s+(?:-d|--decode)\s*\|?\s*(?:bash|sh|python|eval)",
        re.IGNORECASE,
    ),
    re.compile(
        r"echo\s+[A-Za-z0-9+/=]{20,}\s*\|\s*base64\s+(?:-d|--decode)" r"\s*\|\s*(?:bash|sh)",
        re.IGNORECASE,
    ),
]


COMPILED_DANGEROUS_PATTERNS = {
    name: re.compile(pattern, re.IGNORECASE) for name, pattern in DANGEROUS_PATTERNS.items()
}


SENSITIVE_PATHS = [
    "/etc/passwd",
    "/etc/shadow",
    "~/.ssh",
    "~/.aws",
    "/proc/",
    "/sys/",
    "$HOME/.env",
    ".env",
]


BUNDLED_SCAN_DIRS = (
    "bin",
    "connectors",
    "references",
    "reference",
    "scripts",
    "assets",
    "knowledge",
    "templates",
    "examples",
    "prompts",
    "rules",
)
BUNDLED_SCAN_ROOT_FILES = (
    "audit.md",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "setup.md",
    "uv.lock",
    "README.md",
)
BUNDLED_SCAN_EXTENSIONS = {
    ".bash",
    ".css",
    ".csv",
    ".html",
    ".js",
    ".json",
    ".jsx",
    ".j2",
    ".md",
    ".mjs",
    ".ps1",
    ".py",
    ".sh",
    ".svg",
    ".toml",
    ".tpl",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(all\s+)?(previous|prior|above)\s+(instructions|prompts)", re.IGNORECASE),
    re.compile(r"disregard\s+(everything|all)", re.IGNORECASE),
    re.compile(r"forget\s+(previous|all)", re.IGNORECASE),
    re.compile(r"new\s+instructions?:", re.IGNORECASE),
    re.compile(r"system\s*:\s*you\s+are", re.IGNORECASE),
    re.compile(r"</system>", re.IGNORECASE),
    re.compile(r"<\|im_start\|>", re.IGNORECASE),
    # Concealment patterns - skill tries to hide its actions from user
    re.compile(r"do\s+not\s+(tell|inform|mention|notify)\s+(the\s+)?user", re.IGNORECASE),
    re.compile(r"hide\s+(this|that)\s+(action|operation|step)", re.IGNORECASE),
    re.compile(r"keep\s+(this|that)\s+(secret|hidden)", re.IGNORECASE),
    re.compile(r"don'?t\s+mention\s+you\s+used\s+this\s+skill", re.IGNORECASE),
]

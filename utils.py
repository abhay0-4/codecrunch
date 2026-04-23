import os
import subprocess
import sys
import tempfile
from functools import wraps

from flask import session, redirect, abort


# ── Language config ───────────────────────────────────────────────────────────

LANGUAGES = {
    "python":     {"label": "Python 3",  "extension": ".py",  "comment": "# "},
    "c":          {"label": "C (gcc)",   "extension": ".c",   "comment": "// "},
    "javascript": {"label": "JavaScript","extension": ".js",  "comment": "// "},
}

STARTERS = {
    "python": """# Write your solution here
# Read input using input()
# Print output using print()

""",
    "c": """#include <stdio.h>

int main() {
    // Write your solution here
    // Use scanf() to read input
    // Use printf() to print output

    return 0;
}
""",
    "javascript": """// Write your solution here
// Read input from process.stdin
// Use process.stdout.write() or console.log() to print

const lines = require('fs').readFileSync('/dev/stdin', 'utf8').trim().split('\\n');
let idx = 0;
function input() { return lines[idx++]; }

// Your code below:

""",
}


# ── Auth helpers ──────────────────────────────────────────────────────────────

def logged_in():
    return "user_id" in session


def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not logged_in():
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not logged_in() or not session.get("is_admin"):
            abort(403)
        return f(*args, **kwargs)
    return wrapper


# ── Code execution ────────────────────────────────────────────────────────────

def run_code(language, code, input_data):
    """
    Compile (if needed) and run code for the given language.
    Returns (stdout, stderr, returncode) or raises subprocess.TimeoutExpired.
    """
    if language == "python":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
            f.write(code)
            tmp = f.name
        try:
            proc = subprocess.run(
                [sys.executable, tmp],
                input=input_data + "\n",
                capture_output=True, text=True, timeout=2
            )
            return proc.stdout, proc.stderr, proc.returncode
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    elif language == "c":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".c", mode="w") as f:
            f.write(code)
            src = f.name
        exe = src.replace(".c", "")
        try:
            compile_proc = subprocess.run(
                ["gcc", src, "-o", exe, "-lm"],
                capture_output=True, text=True, timeout=10
            )
            if compile_proc.returncode != 0:
                return "", "Compilation Error:\n" + compile_proc.stderr, 1
            proc = subprocess.run(
                [exe],
                input=input_data + "\n",
                capture_output=True, text=True, timeout=2
            )
            return proc.stdout, proc.stderr, proc.returncode
        finally:
            if os.path.exists(src): os.remove(src)
            if os.path.exists(exe): os.remove(exe)

    elif language == "javascript":
        with tempfile.NamedTemporaryFile(delete=False, suffix=".js", mode="w") as f:
            f.write(code)
            tmp = f.name
        try:
            proc = subprocess.run(
                ["node", tmp],
                input=input_data + "\n",
                capture_output=True, text=True, timeout=2,
                env={**os.environ, "NODE_PATH": ""}
            )
            return proc.stdout, proc.stderr, proc.returncode
        finally:
            if os.path.exists(tmp):
                os.remove(tmp)

    return "", "Unsupported language.", 1


# ── Misc helpers ──────────────────────────────────────────────────────────────

def parse_test_cases(raw):
    test_cases = []
    if not raw:
        return [], "At least one test case is required."
    for i, line in enumerate(raw.strip().splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        if "|||" not in line:
            return [], f"Line {i} is missing the ||| separator."
        inp, out = line.split("|||", 1)
        inp = inp.strip().replace("\\n", "\n")
        out = out.strip()
        test_cases.append({"input": inp, "output": out})
    if not test_cases:
        return [], "At least one test case is required."
    return test_cases, None
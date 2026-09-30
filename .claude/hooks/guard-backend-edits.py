#!/usr/bin/env python3
"""PreToolUse guard: Claude may freely write only frontend/, docs/ and CLAUDE.md.

Any other write inside the project (backend code, build scripts, migrations,
CI, .claude/ itself) is escalated to an explicit user confirmation ("ask").
Paths outside the project (scratchpad, memory) are not touched by this guard.
"""
import json
import os
import re
import shlex
import sys

ALLOWED_PREFIXES = ("frontend/", "docs/")
ALLOWED_FILES = ("CLAUDE.md",)

REASON = (
    "Правило проекта (CLAUDE.md): бэкенд, сборку, миграции, CI и настройки .claude "
    "пишет пользователь. Claude свободно правит только frontend/, docs/ и CLAUDE.md. "
    "Подтвердите, только если вы явно разрешили эту правку."
)

REDIRECT_PATTERN = re.compile(r">|\btee\b")
WRITE_PATTERN = re.compile(
    r"(\bsed\b[^|;&]*\s(-[a-zA-Z]*i\b|--in-place)|\bperl\b[^|;&]*\s-[a-zA-Z]*i|"
    r"\b(cp|mv|rm|rmdir|touch|mkdir|ln|install|dd|truncate|patch|chmod|unzip|tar)\b|"
    r"\bgit\s+(apply|am|checkout|restore|reset|stash|mv|rm|clean|revert|cherry-pick|merge|rebase|pull)\b|"
    r"open\([^)]*['\"][wa]|write_text|write_bytes|writeFile)"
)
HARMLESS_REDIRECTS = re.compile(r"\d*>&\d|&?>{1,2}\s*/dev/null|\d>\s*/dev/null")


def rel_in_project(path: str, cwd: str, project: str):
    """Return path relative to project, or None when it lies outside it."""
    full = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))
    proj = os.path.realpath(project)
    if full == proj:
        return ""
    if full.startswith(proj + os.sep):
        return os.path.relpath(full, proj)
    return None


def is_allowed(rel: str) -> bool:
    return rel in ALLOWED_FILES or any(rel.startswith(p) for p in ALLOWED_PREFIXES)


def ask():
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": REASON,
        }
    }, ensure_ascii=False))
    sys.exit(0)


def check_file_tool(tool_input, cwd, project):
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not path:
        return
    rel = rel_in_project(path, cwd, project)
    if rel is not None and not is_allowed(rel):
        ask()


def check_bash(command, cwd, project):
    cleaned = HARMLESS_REDIRECTS.sub(" ", command)
    writes_anywhere = bool(WRITE_PATTERN.search(cleaned))
    if not writes_anywhere and not REDIRECT_PATTERN.search(cleaned):
        return
    spaced = re.sub(r"([<>|;&()])", r" \1 ", cleaned)
    try:
        tokens = shlex.split(spaced, posix=True)
    except ValueError:
        tokens = spaced.split()
    if not writes_anywhere:
        # Only redirects / tee: check just their targets, not the files being read.
        targets, grab = [], False
        for tok in tokens:
            if tok in (">", "tee"):
                grab = True
            elif tok in ("|", ";", "&", "<"):
                grab = False
            elif grab and not tok.startswith("-"):
                targets.append(tok)
                grab = False
        tokens = targets
    in_project_cwd = rel_in_project(".", cwd, project) is not None
    for tok in tokens:
        if not tok or tok.startswith("-") or tok in "<>|;&()":
            continue
        looks_like_path = "/" in tok or "." in tok or os.path.exists(os.path.join(cwd, tok))
        if not looks_like_path:
            continue
        if not tok.startswith(("/", "~")) and not in_project_cwd:
            continue
        rel = rel_in_project(tok, cwd, project)
        if rel is None:
            continue
        if rel == "" or not is_allowed(rel):
            ask()


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    project = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or os.getcwd()
    cwd = data.get("cwd") or project
    tool = data.get("tool_name", "")
    tool_input = data.get("tool_input") or {}
    if tool in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
        check_file_tool(tool_input, cwd, project)
    elif tool == "Bash":
        check_bash(tool_input.get("command", ""), cwd, project)


if __name__ == "__main__":
    main()

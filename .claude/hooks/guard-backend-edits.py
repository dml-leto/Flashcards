#!/usr/bin/env python3
"""PreToolUse guard: Claude may freely write only frontend/, docs/ and CLAUDE.md.

Any other write inside the project (backend code, build scripts, migrations,
CI, .claude/ itself) is escalated to an explicit user confirmation ("ask"),
and the confirmation names the offending path.
Paths outside the project (scratchpad, memory) are not touched by this guard.

Bash detection is heuristic: it looks only at real write targets (redirects,
tee, rm/mv/cp/..., sed -i, dd of=, git commands that rewrite the working tree,
literal paths in open(..., 'w') and similar calls). Paths built from shell
variables cannot be resolved and are not checked.
"""
import json
import os
import re
import shlex
import sys

ALLOWED_PREFIXES = ("frontend/", "docs/")
ALLOWED_FILES = ("CLAUDE.md",)

RULE = (
    "Правило проекта (CLAUDE.md): бэкенд, сборку, миграции, CI и настройки .claude "
    "пишет пользователь. Claude свободно правит только frontend/, docs/ и CLAUDE.md. "
    "Подтвердите, только если вы явно разрешили эту правку."
)

# Commands whose every non-option argument is modified.
ALL_ARGS_WRITERS = {"rm", "rmdir", "touch", "mkdir", "mv", "truncate", "chmod", "chown", "patch"}
# Commands that write only to the last argument (the destination).
LAST_ARG_WRITERS = {"cp", "ln", "install", "rsync"}
# Commands that unpack into the current directory.
CWD_WRITERS = {"unzip", "tar"}
GIT_WORKTREE_WRITERS = {
    "apply", "am", "checkout", "switch", "restore", "reset", "stash", "mv", "rm", "clean",
    "revert", "cherry-pick", "merge", "rebase", "pull",
}

HARMLESS_REDIRECTS = re.compile(r"\d*>&\d|&?>{1,2}\s*/dev/null")
HEREDOC = re.compile(r"<<-?\s*(['\"]?)(\w+)\1([^\n]*)\n.*?\n[ \t]*\2[ \t]*(?=\n|$)", re.S)
SEGMENT_SPLIT = re.compile(r"&&|\|\||[;\n|]")
LITERAL_WRITE_CALLS = re.compile(
    r"open\(\s*(['\"])(?P<a>[^'\"]+)\1\s*,\s*['\"][wax]"
    r"|Path\(\s*(['\"])(?P<b>[^'\"]+)\3\s*\)\.write_(?:text|bytes)"
    r"|writeFile(?:Sync)?\(\s*(['\"])(?P<c>[^'\"]+)\5"
)


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


def ask(rel: str):
    target = f"`{rel}`" if rel else "рабочую копию проекта (корень репозитория)"
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": f"Запись в {target}. {RULE}",
        }
    }, ensure_ascii=False))
    sys.exit(0)


def check_path(path: str, cwd, project: str):
    if not path or "$" in path or "`" in path:
        return  # unresolved shell expansion, cannot be checked
    if cwd is None and not path.startswith(("/", "~")):
        return  # relative path after an unresolvable cd
    rel = rel_in_project(path, cwd or project, project)
    if rel is not None and (rel == "" or not is_allowed(rel)):
        ask(rel)


def check_file_tool(tool_input, cwd, project):
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if path:
        check_path(path, cwd, project)


def tokenize(segment: str):
    spaced = re.sub(r"([<>()])", r" \1 ", segment)
    try:
        return shlex.split(spaced, posix=True)
    except ValueError:
        return spaced.split()


def write_targets(tokens):
    """Yield paths the command writes to; "" means the current directory."""
    # Redirect and tee targets.
    for i, tok in enumerate(tokens):
        if tok == ">" and i + 1 < len(tokens) and tokens[i + 1] != ">":
            yield tokens[i + 1]
    while tokens and re.fullmatch(r"\w+=.*", tokens[0]):
        tokens = tokens[1:]  # leading VAR=value assignments
    if not tokens:
        return
    cmd = os.path.basename(tokens[0])
    args = [t for t in tokens[1:] if t not in ("<", ">", "(", ")")]
    plain = [a for a in args if not a.startswith("-")]
    if cmd == "tee":
        yield from plain
    elif cmd in ALL_ARGS_WRITERS:
        yield from plain
    elif cmd in LAST_ARG_WRITERS and plain:
        yield plain[-1]
    elif cmd in CWD_WRITERS:
        yield ""
    elif cmd == "dd":
        yield from (a[3:] for a in args if a.startswith("of="))
    elif cmd in ("sed", "perl") and any(re.fullmatch(r"-[a-zA-Z]*i\w*|--in-place.*", a) for a in args):
        files = [a for a in plain if a]  # BSD sed takes an empty suffix: sed -i '' ...
        yield from (files[1:] if files and not any(a in ("-e", "-f") for a in args) else files)
    elif cmd == "git" and len(args) > 0 and args[0] in GIT_WORKTREE_WRITERS:
        yield ""


def check_bash(command, cwd, project):
    for m in LITERAL_WRITE_CALLS.finditer(command):
        check_path(m.group("a") or m.group("b") or m.group("c"), cwd, project)
    # Heredoc bodies are data or inline scripts, not shell arguments.
    stripped = HEREDOC.sub(lambda m: m.group(3), command)
    stripped = HARMLESS_REDIRECTS.sub(" ", stripped)
    seg_cwd = cwd
    for segment in SEGMENT_SPLIT.split(stripped):
        tokens = tokenize(segment.strip())
        if not tokens:
            continue
        if tokens[0] == "cd":
            target = tokens[1] if len(tokens) > 1 else "~"
            if "$" in target or seg_cwd is None and not target.startswith(("/", "~")):
                seg_cwd = None
            else:
                seg_cwd = os.path.realpath(os.path.join(seg_cwd or project, os.path.expanduser(target)))
            continue
        for path in write_targets(tokens):
            check_path(path if path else ".", seg_cwd, project)


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

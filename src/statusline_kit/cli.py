from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any, Iterable


CODEX_STATUS_LINE = """status_line = [
  "model-with-reasoning",
  "context-remaining",
  "used-tokens",
  "total-input-tokens",
  "total-output-tokens",
  "five-hour-limit",
  "weekly-limit",
]
status_line_use_colors = true"""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="kt-statusline",
        description="Status line kit for Claude Code and Codex CLI.",
    )
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("claude", help="Render one Claude Code status line from stdin JSON.")
    subparsers.add_parser("doctor", help="Show detected Claude/Codex config paths.")

    install_claude = subparsers.add_parser(
        "install-claude",
        help="Install this command as the Claude Code statusLine command.",
    )
    install_claude.add_argument("--settings", type=Path, default=default_claude_settings())
    install_claude.add_argument("--command", dest="status_command", default=default_command("claude"))

    install_codex = subparsers.add_parser(
        "install-codex",
        help="Install the recommended Codex CLI TUI status line config.",
    )
    install_codex.add_argument("--config", type=Path, default=default_codex_config())

    args = parser.parse_args(argv)

    if args.command == "claude":
        return render_claude_command()
    if args.command == "install-claude":
        backup = install_claude_statusline(args.settings, args.status_command)
        print(f"Installed Claude Code statusLine in {args.settings}")
        if backup:
            print(f"Backup: {backup}")
        return 0
    if args.command == "install-codex":
        backup = install_codex_statusline(args.config)
        print(f"Installed Codex CLI TUI status line in {args.config}")
        if backup:
            print(f"Backup: {backup}")
        return 0
    if args.command == "doctor":
        print_doctor()
        return 0

    parser.print_help()
    return 2


def default_claude_settings() -> Path:
    return Path(os.environ.get("CLAUDE_DIR", Path.home() / ".claude")) / "settings.json"


def default_codex_config() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "config.toml"


def default_command(mode: str) -> str:
    script = Path(__file__).resolve().parents[2] / "bin" / "kt-statusline"
    return f"{script} {mode}"


def render_claude_command() -> int:
    raw = sys.stdin.read().strip()
    try:
        payload = json.loads(raw) if raw else {}
    except json.JSONDecodeError:
        payload = {}
    print(format_claude_status(payload))
    return 0


def format_claude_status(payload: dict[str, Any]) -> str:
    model = first_text(
        nested(payload, "model", "display_name"),
        nested(payload, "model", "name"),
        nested(payload, "model", "id"),
        payload.get("model"),
        "Claude",
    )
    cwd = first_text(
        nested(payload, "workspace", "current_dir"),
        nested(payload, "workspace", "project_dir"),
        payload.get("cwd"),
        os.getcwd(),
    )
    project = Path(cwd).name if cwd else "workspace"
    branch = git_branch(cwd)

    input_tokens = first_int(
        nested(payload, "usage", "input_tokens"),
        nested(payload, "usage", "cache_creation_input_tokens"),
        nested(payload, "token_usage", "input_tokens"),
    )
    output_tokens = first_int(
        nested(payload, "usage", "output_tokens"),
        nested(payload, "token_usage", "output_tokens"),
    )
    cost = first_float(
        nested(payload, "cost", "total_cost_usd"),
        nested(payload, "cost", "usd"),
        payload.get("total_cost_usd"),
    )

    parts = [f"CC {model}", project]
    if branch:
        parts.append(branch)
    token_text = token_summary(input_tokens, output_tokens)
    if token_text:
        parts.append(token_text)
    if cost is not None:
        parts.append(f"${cost:.4f}")
    return " | ".join(parts)


def nested(data: dict[str, Any], *path: str) -> Any:
    current: Any = data
    for key in path:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
    return current


def first_text(*values: Any) -> str:
    for value in values:
        if isinstance(value, str) and value.strip():
            return value.strip()
        if isinstance(value, dict):
            display = value.get("display_name") or value.get("name") or value.get("id")
            if isinstance(display, str) and display.strip():
                return display.strip()
    return ""


def first_int(*values: Any) -> int | None:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, int):
            return value
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                continue
    return None


def first_float(*values: Any) -> float | None:
    for value in values:
        if isinstance(value, bool):
            continue
        if isinstance(value, (float, int)):
            return float(value)
        if isinstance(value, str):
            try:
                return float(value)
            except ValueError:
                continue
    return None


def token_summary(input_tokens: int | None, output_tokens: int | None) -> str:
    bits = []
    if input_tokens is not None:
        bits.append(f"in {compact_number(input_tokens)}")
    if output_tokens is not None:
        bits.append(f"out {compact_number(output_tokens)}")
    return " ".join(bits)


def compact_number(value: int) -> str:
    if abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}m"
    if abs(value) >= 10_000:
        return f"{value // 1_000}k"
    if abs(value) >= 1_000:
        return f"{value / 1_000:.1f}k"
    return str(value)


def git_branch(cwd: str) -> str:
    if not cwd:
        return ""
    try:
        result = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=0.2,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    branch = result.stdout.strip()
    if result.returncode != 0 or branch == "HEAD":
        return ""
    return branch


def install_claude_statusline(settings_path: Path, command: str) -> Path | None:
    settings = read_json_object(settings_path)
    backup = backup_file(settings_path)
    settings["statusLine"] = {
        "type": "command",
        "command": command,
    }
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
    return backup


def read_json_object(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Cannot parse JSON file {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"Expected JSON object in {path}")
    return data


def install_codex_statusline(config_path: Path) -> Path | None:
    text = config_path.read_text() if config_path.exists() else ""
    backup = backup_file(config_path)
    updated = upsert_tui_status_line(text)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(updated)
    return backup


def upsert_tui_status_line(text: str) -> str:
    lines = text.splitlines()
    start, end = find_table(lines, "tui")
    if start is None:
        prefix = text.rstrip()
        section = "[tui]\n" + CODEX_STATUS_LINE + "\n"
        return (prefix + "\n\n" if prefix else "") + section

    section_lines = lines[start + 1 : end]
    kept = remove_tui_status_keys(section_lines)
    replacement = ["[tui]"] + CODEX_STATUS_LINE.splitlines()
    if kept:
        replacement.extend([""] + kept)
    new_lines = lines[:start] + replacement + lines[end:]
    return "\n".join(new_lines).rstrip() + "\n"


def find_table(lines: list[str], table_name: str) -> tuple[int | None, int]:
    header = f"[{table_name}]"
    start = None
    for index, line in enumerate(lines):
        if line.strip() == header:
            start = index
            break
    if start is None:
        return None, len(lines)
    end = len(lines)
    for index in range(start + 1, len(lines)):
        stripped = lines[index].strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            end = index
            break
    return start, end


def remove_tui_status_keys(lines: Iterable[str]) -> list[str]:
    kept: list[str] = []
    skipping_array = False
    for line in lines:
        stripped = line.strip()
        if skipping_array:
            if stripped.endswith("]"):
                skipping_array = False
            continue
        if stripped.startswith("status_line_use_colors"):
            continue
        if stripped.startswith("status_line"):
            if "[" in stripped and "]" not in stripped:
                skipping_array = True
            continue
        kept.append(line)
    while kept and not kept[0].strip():
        kept.pop(0)
    while kept and not kept[-1].strip():
        kept.pop()
    return kept


def backup_file(path: Path) -> Path | None:
    if not path.exists():
        return None
    suffix = dt.datetime.now().strftime(".bak-%Y%m%d-%H%M%S")
    backup = path.with_name(path.name + suffix)
    shutil.copy2(path, backup)
    return backup


def print_doctor() -> None:
    claude = default_claude_settings()
    codex = default_codex_config()
    print(f"Claude settings: {claude} ({'exists' if claude.exists() else 'missing'})")
    print(f"Codex config:    {codex} ({'exists' if codex.exists() else 'missing'})")
    print(f"Command:         {default_command('claude')}")

# statusline-kit

Status line kit for Claude Code and Codex CLI.

This repository contains the first `kt-aicoding` CLI component: a small, dependency-free helper that makes model and usage information visible in day-to-day AI coding tools.

## What It Does

- Claude Code: installs a `statusLine` command that renders model, project, git branch, token usage, and cost when those fields are present in the status input.
- Codex CLI: installs a recommended `[tui]` status line configuration using Codex's built-in status line items.
- Doctor: prints the detected local config paths and command path.

## Install

```bash
git clone https://github.com/kt-aicoding/statusline-kit.git
cd statusline-kit
chmod +x bin/kt-statusline
```

Install Claude Code status line:

```bash
./bin/kt-statusline install-claude
```

Install Codex CLI status line:

```bash
./bin/kt-statusline install-codex
```

Both installers create timestamped backups before writing config files.

## Commands

```bash
./bin/kt-statusline claude
./bin/kt-statusline install-claude
./bin/kt-statusline install-codex
./bin/kt-statusline doctor
```

## Preview

```bash
printf '{"model":{"display_name":"Claude Sonnet"},"workspace":{"current_dir":"."},"usage":{"input_tokens":12450,"output_tokens":830},"cost":{"total_cost_usd":0.0214}}' \
  | ./bin/kt-statusline claude
```

Example output:

```text
CC Claude Sonnet | statusline-kit | main | in 12k out 830 | $0.0214
```

## Claude Code Config

`install-claude` writes this shape into `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/absolute/path/to/bin/kt-statusline claude"
  }
}
```

Claude Code sends session data to the command over stdin. The renderer is intentionally defensive and only displays fields that are present.

## Codex CLI Config

`install-codex` writes this block into `~/.codex/config.toml`:

```toml
[tui]
status_line = [
  "model-with-reasoning",
  "context-remaining",
  "used-tokens",
  "total-input-tokens",
  "total-output-tokens",
  "five-hour-limit",
  "weekly-limit",
]
status_line_use_colors = true
```

If `[tui]` already exists, only `status_line` and `status_line_use_colors` are replaced. Other keys in the section are preserved.

## Development

Run tests with the standard library:

```bash
python3 -m unittest
```

## Links

- Chinese README: [README.zh-CN.md](README.zh-CN.md)
- Claude Code status line docs: https://code.claude.com/docs/en/statusline

# statusline-kit

面向 Claude Code 和 Codex CLI 的状态栏组件。

这是 `kt-aicoding` 的第一个实际项目：一个无第三方依赖的小型 CLI，用来把模型、上下文和用量信息放到 AI Coding 工具的状态栏里。

## 功能

- Claude Code：安装 `statusLine` 命令，从 stdin 接收会话 JSON，并渲染模型、项目、Git 分支、token 用量和费用信息。
- Codex CLI：安装推荐的 `[tui]` 状态栏配置，使用 Codex 内置状态栏项展示模型和用量。
- Doctor：输出当前识别到的 Claude/Codex 配置路径和状态栏命令路径。

## 安装

```bash
git clone https://github.com/kt-aicoding/statusline-kit.git
cd statusline-kit
chmod +x bin/kt-statusline
```

安装 Claude Code 状态栏：

```bash
./bin/kt-statusline install-claude
```

安装 Codex CLI 状态栏：

```bash
./bin/kt-statusline install-codex
```

两个安装命令都会在写入前创建带时间戳的备份文件。

## 命令

```bash
./bin/kt-statusline claude
./bin/kt-statusline install-claude
./bin/kt-statusline install-codex
./bin/kt-statusline doctor
```

## 预览

```bash
printf '{"model":{"display_name":"Claude Sonnet"},"workspace":{"current_dir":"."},"usage":{"input_tokens":12450,"output_tokens":830},"cost":{"total_cost_usd":0.0214}}' \
  | ./bin/kt-statusline claude
```

示例输出：

```text
CC Claude Sonnet | statusline-kit | main | in 12k out 830 | $0.0214
```

## Claude Code 配置

`install-claude` 会向 `~/.claude/settings.json` 写入类似配置：

```json
{
  "statusLine": {
    "type": "command",
    "command": "/absolute/path/to/bin/kt-statusline claude"
  }
}
```

Claude Code 会把当前会话信息通过 stdin 传给这个命令。本项目的渲染逻辑会尽量兼容不同字段，缺失的字段不会显示。

## Codex CLI 配置

`install-codex` 会向 `~/.codex/config.toml` 写入：

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

如果 `[tui]` 已存在，只会替换 `status_line` 和 `status_line_use_colors`，保留该 section 内其他配置。

## 开发

运行测试：

```bash
python3 -m unittest
```

## 参考

- 英文 README：[README.md](README.md)
- Claude Code status line 文档：https://code.claude.com/docs/en/statusline

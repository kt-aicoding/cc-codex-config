# Codex CLI

来源：

- Codex CLI 本机版本：`codex-cli 0.142.2`
- 本机 `codex --help`
- Codex config 官方文档：https://github.com/openai/codex/blob/main/docs/config.md
- Codex CLI features 文档：https://developers.openai.com/codex/cli/features

## 高频命令

| 操作 | 命令 |
| --- | --- |
| 启动交互 TUI | `codex` |
| 指定工作目录 | `codex -C <dir>` |
| 添加可写目录 | `codex --add-dir <dir>` |
| 指定模型 | `codex -m <model>` |
| 使用 profile | `codex --profile <name>` |
| 临时覆盖配置 | `codex -c key=value` |
| 启用 web search | `codex --search` |
| 不使用 alt screen | `codex --no-alt-screen` |
| 严格校验配置 | `codex --strict-config --help` |
| 诊断安装和配置 | `codex doctor` |

## 非交互操作

| 操作 | 命令 |
| --- | --- |
| 非交互执行 | `codex exec "<prompt>"` |
| 代码审查 | `codex review` |
| 应用最近 diff | `codex apply` |
| 恢复会话 | `codex resume` |
| 恢复最近会话 | `codex resume --last` |
| fork 历史会话 | `codex fork` |
| 管理 MCP | `codex mcp` |
| 管理插件 | `codex plugin` |
| 查看 feature flags | `codex features list` |

## 交互 TUI 操作

Codex TUI 快捷键可能随版本和 keymap 变化。本机版本可从 TUI 底部提示进入快捷键帮助；以当前 TUI 的 `shortcuts` 面板为准。

常见交互习惯：

- 输入 `/` 使用命令。
- 输入 `!` 进入 shell 命令语境。
- 使用队列提交时，留意当前 TUI 底部的 submit / queue 提示。
- 长任务中优先让 Codex 更新 plan，避免只看滚动输出。

## Profile

本仓库提供 profile 模板：

```text
configs/codex/profiles/fast.config.toml
configs/codex/profiles/deep.config.toml
```

手动复制到：

```text
$CODEX_HOME/fast.config.toml
$CODEX_HOME/deep.config.toml
```

然后运行：

```bash
codex --profile fast
codex --profile deep
```

## 状态栏

本项目写入：

```toml
[tui]
status_line = [
  "model-with-reasoning",
  "context-used",
  "five-hour-limit",
  "weekly-limit",
  "git-branch",
]
status_line_use_colors = true
```

Codex CLI 目前使用内置状态栏项；本项目不注入外部状态栏命令。

## Warp 注意

- 在 Warp 中建议使用 `codex --no-alt-screen` 处理需要保留完整滚动历史的场景。
- 默认交互仍可使用 alt screen，状态栏由 Codex TUI 自己渲染。
- 如果快捷键和 Warp 冲突，优先在 Warp 的 Keyboard Shortcuts 中调整 Warp 绑定。

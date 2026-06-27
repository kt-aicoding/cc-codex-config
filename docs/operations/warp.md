# Warp 终端

来源：

- Warp keyboard shortcuts 官方文档：https://docs.warp.dev/getting-started/keyboard-shortcuts/
- Warp environment variables 官方文档：https://docs.warp.dev/knowledge-and-collaboration/warp-drive/environment-variables/
- 本机环境：`TERM_PROGRAM=WarpTerminal`、`TERM=dumb`、`NO_COLOR=1`

## 高频快捷键

| 操作 | 快捷键 |
| --- | --- |
| 打开 Command Palette | `Cmd+P` |
| 新建 Tab | `Cmd+T` |
| 新建 Pane | `Cmd+D` |
| 关闭 Pane / Tab | `Cmd+W` |
| 搜索会话输出 | `Cmd+F` |
| 清屏 | `Cmd+K` |
| 向上搜索历史命令 | `Ctrl+R` |
| 打开设置 | `Cmd+,` |

## AI Coding 使用习惯

- 一个 Warp workspace 里按项目开 Tab，cc 和 Codex 分开 pane。
- Claude Code 适合长上下文交互和状态栏风险颜色。
- Codex CLI 适合仓库内实现、审查、验证和配置管理。
- 如果输出很多，用 Warp 搜索定位命令块，不依赖滚动找历史。

## 环境变量注意

Warp 常见环境：

```text
TERM_PROGRAM=WarpTerminal
TERM=dumb
NO_COLOR=1
WARP_IS_LOCAL_SHELL_SESSION=1
```

本项目的 Claude Code 状态栏忽略通用 `NO_COLOR=1`，这样在 Warp 里仍能看到红/黄/绿预警。

如果要关闭本工具颜色：

```bash
export KT_STATUSLINE_NO_COLOR=1
```

## 排查

查看当前工具是否识别 Warp：

```bash
kt-aicoding-config doctor
```

或在仓库内：

```bash
./bin/kt-aicoding-config doctor
```

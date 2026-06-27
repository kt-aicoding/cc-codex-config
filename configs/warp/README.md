# Warp 使用建议

这个仓库默认按 Warp 终端使用场景优化。

当前观察到的 Warp 环境通常包含：

```text
TERM_PROGRAM=WarpTerminal
TERM=dumb
NO_COLOR=1
WARP_IS_LOCAL_SHELL_SESSION=1
```

因此本仓库的 Claude Code 状态栏渲染器不会使用 `NO_COLOR` 判断是否关闭颜色。这样即使 Warp 设置了 `NO_COLOR=1`，Claude Code 状态栏依然能显示红/黄/绿预警。

如果确实想关闭本工具的状态栏颜色，只设置：

```bash
export KT_STATUSLINE_NO_COLOR=1
```

建议：

- 在 Warp 里分别重启 Claude Code 和 Codex CLI，让它们重新读取配置。
- 不要把 API token、provider key、项目 trust 列表放进这个公开仓库。
- Warp 的环境变量和密钥适合放在 Warp 自己的工作流/环境管理里；本仓库只保留可公开审计的通用配置。
- 如果 Warp 中状态栏颜色异常，先运行 `kt-aicoding-config doctor` 或 `kt-statusline doctor` 看是否检测到 Warp。

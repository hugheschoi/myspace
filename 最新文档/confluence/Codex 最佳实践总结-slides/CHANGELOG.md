# Codex 最佳实践总结 Slides Changelog

## 修改批次

| 日期 | 变更摘要 | 页数 |
| --- | --- | --- |
| 2026-05-14 | 增补面向“看不懂文章”的导读页和可直接套用的 Prompt 模板页，并重新编号。 | 16 |
| 2026-05-13 | 新增基于 OpenAI Developers Codex Best practices 的中文 HTML slide deck。 | 14 |

## 本轮明细

- 2026-05-14：新增第 3 页“怎么读懂”四层成熟路径导读，新增第 15 页任务模板，帮助把文章从功能清单理解为工程协作系统。
- 2026-05-14：同步更新页码为 16 页，保留原 deck 视觉样式，并备份旧版 `index.html.bak.20260514-150340`。
- 2026-05-13：新增 `index.html`：14 页固定 16:9 HTML slide，使用当前目录已有 deck 的纸张色、侧边色带、页码、卡片和流程图风格。
- 内容覆盖：Prompt、Plan Mode、`AGENTS.md`、`config.toml`、测试评审、MCP、Skills、Automations、session controls、常见反模式和落地路线图。
- 所有正文均为中文转述和结构化总结，未复制官方长文原文。

## 内容来源

| 来源 | URL | 用途 |
| --- | --- | --- |
| 用户提供的知乎链接 | https://zhuanlan.zhihu.com/p/1938967453951571269 | 请求来源；直接访问触发知乎反爬/异常页，未取得正文 |
| OpenAI Developers - Best practices | https://developers.openai.com/codex/learn/best-practices | Markdown 总结和 16 页 slide 内容主来源 |

## 文件结构

| 文件 | 说明 |
| --- | --- |
| `../Codex 最佳实践总结.md` | 中文 Markdown 总结文档 |
| `index.html` | 单文件 HTML slide |
| `index.html.bak.20260514-150340` | 2026-05-14 修改前备份 |
| `CHANGELOG.md` | 本变更记录 |
| `preview-slides.png` | QA 脚本生成的总览预览图 |
| `slide-previews/` | 渲染预览输出目录，运行 QA 脚本后生成 |

## QA 记录

- 已运行：`python3 ~/.codex/skills/html-slide-report-qa/scripts/render_slide_previews.py "/Users/zhuangbing.cai/Documents/md/confluence/Codex 最佳实践总结-slides/index.html"`
- 渲染结果：成功生成 16 页预览到 `slide-previews/`。
- 尺寸检查：16 张单页预览均为 1280x720。
- 视觉抽查：contact sheet 中标题、正文、页码无明显重叠；16 页页码连续；底部无明显裁切。

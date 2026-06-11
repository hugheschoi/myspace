# AI 提效方案 Slides Changelog

## 修改批次

| 日期 | 变更摘要 | 页数 |
| --- | --- | --- |
| 2026-05-14 | 新增基于 Codex 最佳实践和生码 Harness 工程的 AI 研发提效 HTML slide deck。 | 15 |

## 本轮明细

- 新增 `index.html`：15 页固定 16:9 HTML slide，采用纸张色、侧边色带、页码、卡片、流程图和路线图布局。
- 同步扩展 `../AI提效.md`：从原始提效场景清单升级为完整 AI 研发提效 Harness 方案。
- 内容覆盖：核心判断、当前问题、两层方案、端到端链路、高 ROI 场景、Task Spec、上下文工程、工具网关、验证闭环、MVP、团队工作流、路线图、指标和首月行动。

## 内容来源

| 来源 | 用途 |
| --- | --- |
| `../Codex 最佳实践总结.md` | Codex 任务上下文、Plan、`AGENTS.md`、`config.toml`、验证、Skills、Automations 等实践来源 |
| `../harness阅读.md` | Harness 工程的 R.E.S.T、PPAF、工具网关、状态分离、验证反馈和治理框架来源 |
| `../从 0 到 1 实现生码 harness工程.md` | 生码 Harness 最小闭环、Task Spec、上下文、工具、沙盒、验证、路线图来源 |
| `../AI提效.md.bak.20260514-152236` | 原始 AI 提效场景清单备份 |

## 文件结构

| 文件 | 说明 |
| --- | --- |
| `../AI提效.md` | AI 研发提效 Harness 方案 Markdown |
| `index.html` | 单文件 HTML slide deck |
| `CHANGELOG.md` | 本变更记录 |
| `preview-slides.png` | QA 脚本生成的总览预览图 |
| `slide-previews/` | 单页渲染预览输出目录，运行 QA 脚本后生成 |

## QA 记录

- 已运行：`python3 ~/.codex/skills/html-slide-report-qa/scripts/render_slide_previews.py "/Users/zhuangbing.cai/Documents/md/confluence/AI提效方案-slides/index.html"`
- 渲染结果：成功生成 15 页预览到 `slide-previews/`。
- 尺寸检查：单页预览为 1280x720；`contact-sheet.png` 为 1040x2560。
- 视觉抽查：contact sheet 中标题、正文、页码无明显重叠；底部无明显裁切。

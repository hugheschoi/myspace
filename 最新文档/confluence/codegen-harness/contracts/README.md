# Codegen Harness Task Spec

这个目录是生码 Harness MVP 的第一层输入契约。它的目标不是把 Prompt 写长，而是在 Agent 改代码前先把任务边界、上下文来源、可编辑范围和验收标准规整成机器可检查的结构。

## Files

- `task-spec.schema.json`: Task Spec v1 的 JSON Schema，用于描述字段形状。
- `task-spec.template.json`: 新任务的填写模板。
- `task-spec.example.json`: 基于当前样板间模板文件的示例输入。
- `../scripts/validate-task-spec.mjs`: 零依赖校验脚本，用于判断输入是否可以进入下一步。

## Required Contract

每个任务至少要说明这些信息：

- `task`: 做什么页面或模块，目标路由是什么，任务是新建、扩展还是修复。
- `sources`: PRD 必填，后端 TD 和前端 TD 可选；每份文档可以是 URL、本地路径或内联文本。
- `interfaces`: YAPI/API 列表。没有接口时可以为空，但涉及接口接入时必须补齐。
- `template`: 样板间模板、相似页面或现有模板来源。
- `implementation`: 目标仓库、目标文件、框架、组件库、请求封装和状态管理方式。
- `constraints`: 可编辑范围、禁止事项、依赖策略。
- `acceptance`: 功能验收、数据契约、必须执行的质量门禁。
- `unknowns`: 还没确认的问题。这里不为空时，Agent 应该先停下来问人或输出待确认项。

## Validate

在 `codegen-harness` 目录下运行：

```bash
npm run validate:task
```

也可以直接指定任意任务文件：

```bash
node scripts/validate-task-spec.mjs contracts/task-spec.example.json
```

校验通过表示结构完整，且没有明显的占位符或阻塞性未知项。警告不会阻断，但会提醒后续上下文收集需要补强，例如接口列表为空。

## Agent Rule

后续 Harness 的 Agent 入口应先读取并校验 Task Spec：

1. 校验失败：不生成代码，返回缺失字段和阻塞问题。
2. 校验通过但有 warning：继续收集上下文，同时把 warning 写入计划。
3. `unknowns.open_questions` 不为空：停止执行，先向人确认。
4. 只有当 `editable_scope` 明确且验收标准明确时，才允许进入改码阶段。

# Codegen Harness MVP

这个目录把生码 Harness 拆成可逐层落地的小模块。

## Layers

- `contracts`: 第一层约束，任务输入契约。把散乱输入规整成 Task Spec。
- `context`: 第二层约束，上下文工程。按任务类型生成稳定的上下文注入计划。
- `scripts`: 当前 MVP 的校验、计划生成脚本。

## Quick Start

```bash
npm run validate:task
npm run context:plan
```

`validate:task` 判断任务输入是否足够明确；`context:plan` 判断这类任务需要注入哪些上下文，以及哪些上下文缺失或只能作为 warning 继续。

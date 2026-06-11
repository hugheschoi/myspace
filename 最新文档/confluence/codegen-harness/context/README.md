# Context Engineering

第二层约束解决的问题是：Agent 不应该一次塞满所有资料，也不应该凭感觉挑上下文。

这里把上下文拆成稳定的 slot，并按任务类型决定哪些 slot 必须注入、哪些 slot 推荐注入、哪些 slot 只有满足条件才注入。

## Core Rule

上下文注入遵循四条规则：

1. 先读 `Task Spec`，再生成 `Context Plan`。
2. 必需 slot 缺失时停止，不进入改码。
3. 推荐 slot 缺失时继续，但必须在计划里留下 warning。
4. 每个 slot 都有读取预算和读取策略，避免把仓库、PRD、TD、YAPI 一股脑塞进上下文。

## Slots

- `task_contract`: 任务边界、目标路由、任务类型、目标产物。
- `requirement_prd`: PRD 中与当前任务直接相关的需求和验收。
- `technical_design`: 后端 TD、前端 TD，按需摘要。
- `api_contracts`: YAPI/API 路径、方法、字段契约、请求用途。
- `primary_template`: 样板间模板或主参考模板。
- `template_reference`: 其他模板、相似模板、样板间辅助参考。
- `target_edit_scope`: 目标仓库、目标文件、可编辑范围。
- `repo_conventions`: `package.json`、`tsconfig`、lint 配置、README 等项目习惯。
- `component_usage`: 组件库文档、组件示例、已使用组件的本地用法。
- `similar_pages`: 同类型页面或组件，用于学习项目写法。
- `project_rules`: 项目规则、权限、i18n、埋点等长期约束。
- `constraints`: 禁止事项、只读范围、依赖策略。
- `acceptance`: 功能验收、数据契约、质量门禁。

## Generate Plan

```bash
npm run context:plan
```

指定任务文件：

```bash
node scripts/build-context-plan.mjs contracts/task-spec.example.json
```

写入报告文件：

```bash
node scripts/build-context-plan.mjs contracts/task-spec.example.json --write
```

默认输出 JSON 到 stdout；`--write` 会生成：

- `.ai-codegen/<task-id>/context-plan.json`
- `.ai-codegen/<task-id>/context-plan.md`

## Agent Rule

后续 Agent 入口应按这个顺序执行：

1. `validate-task-spec`
2. `build-context-plan`
3. 若 `status = blocked`，停止并返回缺失上下文。
4. 若 `status = ready_with_warnings`，继续收集上下文，但把 warning 写进生成计划。
5. 按 `injection_order` 注入上下文，不允许跳过必需 slot。

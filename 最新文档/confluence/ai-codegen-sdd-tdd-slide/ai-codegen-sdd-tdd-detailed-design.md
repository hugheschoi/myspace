# AI Codegen SDD/TDD 生码工程详细设计

## 1. 背景与目标

AI 生码的瓶颈通常不是“模型写不出代码”，而是缺少稳定工程约束：需求来源分散、代码上下文不完整、接口协议容易误读、测试验收被后置、最终 diff 难以 review。这个设计的目标是把一次 AI 生码任务变成一个可追踪、可验证、可复盘的工程流程。

本方案以 `ai-codegen-sdd-tdd` Codex skill 为载体，将需求输入、设计产物、测试产物、代码计划、代码修改、验证报告串成固定工作流。它适合 FRS / Lovito / SBS 这类多仓、多子应用、多 BLL/schema/API 适配层的前端工程，也可以扩展到后端或全栈任务。

核心目标：

- 让每个代码改动都能追溯到 PRD/TD/YAPI/代码上下文。
- 让模型先写清楚 SDD/TDD，再小步改代码。
- 让验证和 review 成为流程的一部分，而不是最后补一段说明。
- 让一次需求沉淀为可复盘的 `ai-codegen-runs/<name>` 目录。

非目标：

- 不追求一次 prompt 直接生成完整功能。
- 不替代人工产品决策、后端协议确认和代码 review。
- 不强制所有需求都写完整大文档，小需求可以轻量化，但不能跳过关键事实确认。

## 2. 核心理念

### 2.1 SDD 是实现合同

SDD 不是传统意义上的冗长设计文档，而是约束 AI 写代码的合同。它回答：

- 这个需求到底要改变什么行为？
- 影响哪些页面、路由、组件、状态、schema、API？
- 哪些信息来自 PRD/TD，哪些是推断？
- 边界条件、权限、区域、旧数据兼容是什么？

AI 后续写代码时，不能脱离 SDD 发散。

### 2.2 TDD 是验收合同

TDD 在这里不是狭义“先写单测代码”，而是测试设计。它回答：

- 哪些 case 必须验证？
- 哪些可以自动化，哪些只能手工验？
- 关键接口 payload 和响应字段应该怎么检查？
- 哪些旧流程要回归？

当仓库测试体系不完善时，TDD 至少要给出明确手工验收路径。

### 2.3 Plan 是执行合同

Implementation Plan 把设计转成可操作的 patch 顺序。它回答：

- 先改 types/constants，还是先改 schema/UI？
- 哪些文件必须改，哪些文件不该碰？
- 每一步改动后跑什么命令？
- 哪一步是风险最高的回滚点？

它避免模型一次性大改。

### 2.4 Verification Report 是收口合同

Verification Report 记录命令结果、diff review、warning 来源和剩余风险。它让交付结果不只是“我改好了”，而是“我改了这些，用这些方式验证过，还有这些风险”。

## 3. 工程结构

当前 skill 位于：

```text
~/.codex/skills/ai-codegen-sdd-tdd/
  SKILL.md
  references/
    codegen-run-template.md
    review-checklist.md
  scripts/
    create_codegen_run.py
```

### 3.1 `SKILL.md`

定义触发场景和主流程。它是 Codex 每次触发 skill 后首先读取的执行指南。

关键内容：

- 什么时候使用该 skill。
- 需要创建哪些核心产物。
- 从 Source Index 到 Verification 的七步工作流。
- 输出规则和与其它 skill 的协作关系。

### 3.2 `codegen-run-template.md`

定义一次需求运行的母模板，覆盖：

- Source Index
- SDD
- TDD
- Implementation Plan
- Verification Report

实际使用时不需要用户手填这个模板。它是 Codex 填写 `sdd.md`、`tdd.md`、`implementation-plan.md`、`verification-report.md` 的结构依据。

### 3.3 `review-checklist.md`

用于生成代码后的 review gate。重点检查：

- Traceability：代码是否能追溯到 SDD/TD。
- Frontend Behavior：是否污染原始数据、是否保留权限/区域逻辑。
- Code Quality：是否范围过大、是否引入 debug log。
- Verification：是否跑过 targeted command，warning 是否区分新旧。

### 3.4 `create_codegen_run.py`

脚本用于在目标仓库下创建一次生码任务目录：

```bash
python3 ~/.codex/skills/ai-codegen-sdd-tdd/scripts/create_codegen_run.py \
  --name supplier-origin-code \
  --root /Users/zhuangbing.cai/Documents/works/sbs-supplier-fe
```

生成结构：

```text
ai-codegen-runs/supplier-origin-code/
  README.md
  sdd.md
  tdd.md
  implementation-plan.md
  verification-report.md
```

## 4. 一次生码运行的数据流

```text
PRD / TD / YAPI / Confluence / Jira / Code Hint
  -> Source Index
  -> Repo Context
  -> SDD
  -> TDD
  -> Implementation Plan
  -> Code Patch
  -> Verification
  -> Review / Final Response
```

### 4.1 Source Index

Source Index 是所有后续结论的根。每个来源都需要稳定 ID：

| ID | 类型 | 示例 |
| --- | --- | --- |
| `PRD-1` | 产品需求 | Confluence PRD 页面 |
| `TD-1` | 后端技术文档 | Confluence TD 页面 |
| `YAPI-1` | 接口文档 | YAPI API detail |
| `CODE-1` | 代码上下文 | 路由/BLL/schema/API 文件 |

原则：

- 不能访问的来源必须标记为 unresolved。
- 不允许把推断写成已确认事实。
- API path、字段名、枚举值必须保持原文。

### 4.2 Repo Context

Repo Context 用来避免“AI 猜项目结构”。在 FRS / SBS 场景，至少要识别：

- 目标仓库和子应用，例如 `sbs-supplier-fe/projects/lovito-supplier-pms-fe`。
- 路由定义和页面组件。
- BLL、hooks、schema、api helper、type 文件。
- 现有字段格式化、提交格式化、详情展示逻辑。
- 当前 dirty worktree 中哪些变更不是本次产生的。

如果是路由相关任务，应优先配合 `frs-route-locator` skill。

### 4.3 SDD

SDD 的粒度建议以 `FEAT-*` 拆分。一个 feature 应该能被一个开发者独立理解和实现。

每个 feature 至少包含：

- Source：来自哪个 PRD/TD/CODE。
- User entry：用户从哪个页面/按钮/路由进入。
- Current behavior：当前行为。
- Target behavior：目标行为。
- UI changes：表单、表格、弹窗、状态展示。
- State/model changes：前端状态和数据结构变化。
- Data transform：展示值、提交值、接口值的转换。
- API protocol：接口、触发时机、请求、响应使用。
- Compatibility：旧数据、区域、权限、灰度。
- Open questions：不能确定的问题。

### 4.4 TDD

TDD 根据 SDD 生成测试矩阵。测试类型不局限于自动化：

- Unit：纯函数、format、helper。
- Component：表单字段、下拉、表格展示。
- Integration/API mock：接口 payload、响应驱动 UI。
- Manual：无法自动化时的手工验收路径。
- Regression：旧功能回归。

测试 case 需要反查到 SDD feature：

| Test ID | Feature ID | Type | Scenario | Expected |
| --- | --- | --- | --- | --- |
| `TEST-1` | `FEAT-1` | Manual | 创建页默认值 | payload 正确 |

### 4.5 Implementation Plan

Plan 需要按最小风险顺序组织：

1. Types/constants
2. API helpers
3. Data transform/state
4. UI/schema/components
5. Tests/mocks
6. Cleanup

每个文件都要说明：

- 为什么改。
- 对应哪个 feature/API。
- 风险等级。
- 是否已有用户改动需要避让。

### 4.6 Code Patch

代码修改要遵守当前 repo 模式：

- 手动编辑用 `apply_patch`。
- 不做无关重构。
- 不用展示字符串污染接口原始字段。
- 复用现有 `schema`、`BLL`、`format`、`api` 模式。
- 如果遇到用户已有改动，优先共存，不回滚。

### 4.7 Verification

Verification 至少记录：

- 命令。
- 结果。
- warning 是否本次新增。
- 无法运行的原因。
- 手工验证建议。

例如：

```text
pnpm --filter lovito-supplier-pms-fe exec eslint src/views/supplier/bll/edit/index.ts
Result: 0 errors, existing warnings only
```

## 5. 与现有 skill 的关系

### 5.1 `frontend-task-doc-from-prd-td`

这个 skill 擅长把 PRD/TD 变成前端任务文档。它可以作为 Source Index 和 SDD 的前置步骤。

适合场景：

- 需求很大。
- PRD/TD 很多。
- 需要先产出一份给人看的前端任务拆解。

### 5.2 `frs-route-locator`

这个 skill 用来找路由对应页面文件。它通常在 Repo Context 阶段调用。

适合场景：

- 用户给的是 `/frs/...` 路由。
- 需要跨 `frs-admin-fe`、`sbs-supplier-fe`、`sbs-purchase-fe` 等仓库定位页面。

### 5.3 `ai-codegen-sdd-tdd`

这个 skill 是编排层。它不替代前两个 skill，而是把它们纳入完整生码流程。

## 6. 可能出现的问题与风险

### 6.1 来源资料不完整

问题：

- PRD 写了页面行为，但 TD 没给接口。
- TD 给了接口字段，但 PRD 没说明使用场景。
- Confluence 页面不可访问或内容过期。

后果：

- AI 可能自行补齐协议。
- 代码实现和后端真实契约不一致。
- 测试只能覆盖推断路径。

应对：

- Source Index 中标记 `TD missing`、`PRD missing`、`Unresolved`。
- 关键协议缺失时暂停确认。
- 非关键缺失可以保守实现，并在 SDD 中标记 `Inference`。

### 6.2 路由或页面定位错误

问题：

- 同名路由存在 PMS/SRM/SCM 多份实现。
- 主应用只注册菜单，真实页面在子应用。
- `window.open` / `router.push` 只是调用点，不是页面归属。

后果：

- 改错仓库或改错页面。
- 自测路径和真实用户路径不一致。

应对：

- Repo Context 阶段必须定位 route definition、component、BLL。
- 使用 `frs-route-locator`。
- 回答和文档中记录路由链路。

### 6.3 展示值污染原始数据

问题：

- 为了 UI 展示，把接口返回的原始字段改成拼接字符串。
- 例如把 `code` 改成 `code (name)` 后继续传给后续逻辑。

后果：

- 提交 payload 错误。
- 详情页、编辑页、审核页共享同一份数据时出现隐性 bug。

应对：

- SDD 中区分 raw value、display value、submit value。
- Review checklist 强制检查“Form values are not mutated into display-only strings”。
- 展示拼接放在 render/format display 层，不改接口原始对象。

### 6.4 API 字段名或枚举误读

问题：

- 后端要求 `origin_code: HK/GZ`，前端误传 `company_code: BNLHK/LVTGZ`。
- 字段名大小写、下划线、枚举数字含义被模型“规范化”。

后果：

- 接口能发出但业务不生效。
- 后端排查困难。

应对：

- API Protocol 表保留原始字段名和枚举。
- 对每个 payload 字段写清“请求来源”。
- TDD 中加入 expected network payload。

### 6.5 过度依赖模板，忽略实际仓库模式

问题：

- 模板里建议先改 types，但当前 Vue 老项目可能没有严格类型入口。
- 模板建议写测试，但仓库缺少测试框架。

后果：

- 生成计划看起来完整，但落地不自然。
- 代码风格和现有工程不一致。

应对：

- 模板是栏杆，不是绝对流程。
- Repo Context 阶段记录本仓库真实模式。
- 若无自动测试，TDD 转为手工验收和 targeted lint。

### 6.6 上下文窗口过载

问题：

- 一次加载多个 PRD、TD、长代码文件、模板、日志。
- 模型丢失早期约束。

后果：

- 设计和实现不一致。
- 输出遗漏关键字段。

应对：

- Progressive disclosure：先读索引，再按需要读细节。
- 长文档做摘要和 source ID，不把全文常驻上下文。
- 大需求拆成多个 `FEAT-*` 或多个 codegen run。

### 6.7 验证命令不可运行

问题：

- Node 版本不对。
- 依赖没安装。
- monorepo filter 名称不确定。
- lint 有大量历史 warning。

后果：

- 用户误以为未验证。
- 新旧问题混在一起。

应对：

- Verification Report 记录环境问题和 fallback。
- 尽量跑 targeted command。
- 区分 `0 errors with existing warnings` 和 `new errors`。

### 6.8 AI 修改范围膨胀

问题：

- 为了“顺手优化”，改了无关格式、抽象、命名。
- 自动格式化影响大批文件。

后果：

- PR 难 review。
- 回归风险变大。

应对：

- Implementation Plan 必须列文件 map。
- Patch 只改 plan 中的文件。
- 格式化只跑 touched files。
- 发现 unrelated dirty changes 时避让。

### 6.9 SDD/TDD 变成形式主义

问题：

- 文档只是复制 PRD，缺少工程判断。
- TDD 只写“测试正常/异常”，没有 payload 和场景。

后果：

- 文档不能约束生码。
- 代码 review 仍然靠人重新读需求。

应对：

- SDD 必须包含 feature/API mapping。
- TDD 必须包含 expected UI 和 expected network payload。
- Verification Report 必须引用 Test ID 或 Feature ID。

### 6.10 人机责任边界不清

问题：

- AI 对产品决策做了最终判断。
- 用户以为 AI 已确认后端协议。

后果：

- 需求偏差直到上线才暴露。

应对：

- 文档中明确 `Confirmed`、`Inference`、`Open Question`。
- 高风险产品决策必须暂停确认。
- 低风险实现假设要在最终回答里说明。

## 7. 推荐执行策略

### 7.1 小需求

适合字段、接口参数、简单 UI 展示调整。

流程可以轻量化：

1. Source Index 简写。
2. SDD/TDD 合并到一个小节。
3. Plan 只列 touched files。
4. 直接 patch。
5. targeted lint + final summary。

但仍要保留：

- 字段来源。
- 请求 payload。
- 验证结果。

### 7.2 中型需求

适合一个页面或一个业务流程。

建议完整生成：

- `sdd.md`
- `tdd.md`
- `implementation-plan.md`
- `verification-report.md`

实现前应先让用户确认 SDD/Plan 中的关键假设。

### 7.3 大型需求

适合多个页面、多个接口、多仓联动。

建议拆成多个 run：

```text
ai-codegen-runs/lovito-phase2-supplier/
ai-codegen-runs/lovito-phase2-inventory/
ai-codegen-runs/lovito-phase2-rts/
```

每个 run 独立 SDD/TDD/Plan，最后再有一个总集成验证报告。

## 8. 后续可增强方向

### 8.1 自动生成 Source Index

可以扩展脚本读取输入链接和本地文件，自动生成 `source-index.json`，让 SDD 引用更稳定。

### 8.2 与 Confluence / YAPI / Jira 集成

可以把已有 MCP 工具接入成固定 adapters：

- `confluence -> source markdown`
- `yapi -> API protocol`
- `jira -> acceptance criteria`

### 8.3 Diff 到 Feature 的机器校验

可以增加脚本检查：

- 改动文件是否在 `implementation-plan.md` 中登记。
- final diff 是否包含未声明文件。
- API path 是否出现在 SDD/TDD。

### 8.4 验证命令模板化

可以按仓库生成默认命令：

- `sbs-supplier-fe`: `pnpm --filter lovito-supplier-pms-fe exec eslint ...`
- `sbs-purchase-fe`: `pnpm --filter lovito-purchase-pms-fe exec eslint ...`
- `scs-inventory-admin-fe`: `pnpm --filter lovito-inventory-admin-fe exec eslint ...`

### 8.5 引入 CR Shift-left

如果接入 CR 工具，可以在 Verification 后追加自动审查阶段：

```text
diff -> CR rules -> issues -> fix or explain
```

这样 AI 生码不会只停在“能跑”，还会进入团队 review 质量线。

## 9. 一次标准使用示例

用户输入：

```text
用 ai-codegen-sdd-tdd 帮我做这个需求：
PRD: https://confluence...pageId=xxx
TD: https://confluence...pageId=yyy
目标仓库: sbs-supplier-fe
页面: /frs/supplier/request/create
要求:
- 先生成 SDD/TDD/Plan
- 再实现代码
- 最后跑 targeted lint 并写 verification report
```

执行行为：

1. 创建 `ai-codegen-runs/<name>`。
2. 读取 PRD/TD，生成 Source Index。
3. 用 route locator 找到页面文件和 BLL。
4. 写 SDD 和 TDD。
5. 写 implementation plan。
6. 通过 `apply_patch` 小步改代码。
7. 跑 targeted lint/typecheck/test。
8. 更新 verification report。
9. 最终回答说明改动、验证和风险。

## 10. 结论

这套工程的重点不是“多写文档”，而是把 AI 的自由度放进工程栏杆里。SDD 约束实现，TDD 约束验收，Plan 约束修改范围，Verification 约束交付可信度。

当需求变复杂、仓库变多、接口变细时，这套流程会比直接让 AI 改代码慢一点，但它能显著降低改错页面、误读字段、污染原始数据、遗漏回归和最终无法 review 的风险。

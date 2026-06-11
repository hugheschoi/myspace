# CHANGELOG

| Round | Date | Summary | Page Count |
| --- | --- | --- | --- |
| 1 | 2026-06-09 | Created an HTML slide deck explaining the AI Codegen SDD/TDD workflow and local skill usage. | 10 |
| 2 | 2026-06-09 | Added a detailed Markdown design document with architecture, execution model, risk analysis, and enhancement roadmap. | 10 |

## Round 1 Details

- Added `index.html` with ten fixed 16:9 slides.
- Covered motivation, workflow, local skill structure, run command, artifact usage, review gate, and example prompt.
- Used source material from the local `ai-codegen-sdd-tdd` skill files:
  - `/Users/zhuangbing.cai/.codex/skills/ai-codegen-sdd-tdd/SKILL.md`
  - `/Users/zhuangbing.cai/.codex/skills/ai-codegen-sdd-tdd/references/codegen-run-template.md`
  - `/Users/zhuangbing.cai/.codex/skills/ai-codegen-sdd-tdd/references/review-checklist.md`
  - `/Users/zhuangbing.cai/.codex/skills/ai-codegen-sdd-tdd/scripts/create_codegen_run.py`

## Round 2 Details

- Added `ai-codegen-sdd-tdd-detailed-design.md`.
- Expanded the slide concepts into a detailed engineering design.
- Added deeper analysis of common failure modes, including incomplete sources, wrong route ownership, raw-data pollution, API enum mistakes, context overload, verification gaps, and scope creep.
- Added recommended strategies for small, medium, and large requirements.

## File Structure

| File | Purpose |
| --- | --- |
| `index.html` | HTML slide deck |
| `ai-codegen-sdd-tdd-detailed-design.md` | Detailed design document |
| `CHANGELOG.md` | Change log and source summary |
| `slide-previews/` | Generated QA previews |

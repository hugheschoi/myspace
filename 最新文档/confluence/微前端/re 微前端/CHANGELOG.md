# CHANGELOG

## Modification Rounds

| Round | Date | Summary | Page Count Change |
| --- | --- | --- | --- |
| 1 | 2026-05-29 | Created a new fixed-canvas HTML slide deck explaining the Retail micro-frontend architecture with code-backed diagrams, local-debug flow, risks, and troubleshooting guidance. | 0 -> 18 |
| 2 | 2026-05-29 | Ran visual QA, regenerated exact 1280x720 Chrome previews, shortened source labels, and removed the presentation overlay hint. | 18 -> 18 |

## Round 1 Details

- Added `index.html` as a self-contained 16:9 slide deck.
- Introduced a restrained Retail-style technical visual system using orange, blue, teal, green, and neutral colors.
- Added architecture diagrams for the host/base/remote relationship, Bootstrap sequence, remote loading, router/menu merge, shared instances, and React/Vue interop.
- Added practical slides for local debugging, common risks, troubleshooting order, and a speaker-friendly explanation spine.

## Round 2 Details

- Rendered every slide as an isolated `1280x720` Chrome screenshot and verified all 18 output dimensions.
- Created `slide-previews-exact/contact-sheet.png` for whole-deck visual QA.
- Tightened the appendix source table so long Confluence URLs do not crowd the right edge.
- Removed the floating keyboard/print hint from the live deck so it does not appear during presentation.

## Content Sources Summary

| Source | URL / Path | Sections Informed |
| --- | --- | --- |
| Retail 主子应用独立架构优化方案 | https://confluence.shopee.io/pages/viewpage.action?pageId=2385944962 | Background, goals, architecture roles, Micro Base capability modules, target state, risks |
| 沉淀 Micro Base - 支持多 Portal 加载 React 子应用 | https://confluence.shopee.io/pages/viewpage.action?pageId=2184252778 | Universal Micro Base rationale, Framework/Shared Module distinction, React sub-app loading, local debug flow |
| vmi-admin-fe | `/Users/zhuangbing.cai/Documents/works/scs/vmi-admin-fe` | Host remotes, Module Federation config, bootstrap props/plugin, layout/menu, global data |
| micro-base | `/Users/zhuangbing.cai/Documents/works/micro-base` | BootstrapApp, lifecycle manager, core router/store instances, module load/register APIs, React/Vue wrappers |
| sbs-product-fe | `/Users/zhuangbing.cai/Documents/works/sbs-product-fe` | `scsProductPms` and `scmProduct` remote exposes, product module contract, shared singleton dependencies |

## File Structure

| File / Directory | Purpose |
| --- | --- |
| `index.html` | Final HTML slide deck |
| `CHANGELOG.md` | Change and source record |
| `slide-previews/` | Initial generated per-slide QA previews |
| `slide-previews-exact/` | Exact 1280x720 per-slide Chrome screenshots |
| `slide-previews-exact/contact-sheet.png` | Whole-deck visual QA contact sheet |

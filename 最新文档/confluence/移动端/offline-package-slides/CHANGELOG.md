# Offline Package Slides Changelog

## Modification Rounds

| Round | Date | Summary | Page Count Change |
| --- | --- | --- | --- |
| 1 | 2026-06-10 | Created a 21-slide HTML deck from the offline package and dual-end architecture document. | 0 -> 21 |

## Round 1 Details

- Added `index.html` as a fixed 16:9 HTML slide deck.
- Covered offline package motivation, single-app package model, build plugin workflow, APP runtime loading, multi-app app_id/biz_id model, Order Tracking split, version publishing, gray release, upgrade UX, rollback, version-mgr SDK, dual-end adapter architecture, WMS implementation, PC FMS remoteEntry loading, and debugging checklist.
- Added slide-safe CSS with fixed `1280px x 720px` canvases, stable header/body/footer zones, and compact card/table layouts.
- No existing HTML deck was overwritten, so no backup file was needed.

## Content Sources Summary

| Source | Type | Sections Informed |
| --- | --- | --- |
| `../mgmt-offline-dual-end-architecture.md` | Markdown summary | All slides |
| `Management App - 离线包方案设计.pdf` | PDF | Slides 3-8, 11, 14, 20 |
| `多应用离线包方案.pdf` | PDF | Slides 9, 11, 14 |
| `多应用离线包：SPX-mgmt的Order tracking业务拆分.pdf` | PDF | Slide 10 |
| `离线包灰度与即时版本更新方案.pdf` | PDF | Slide 12 |
| `mgmt APP 版本升级问题及优化方案.pdf` | PDF | Slide 13 |
| `PC和移动端适配技术方案.pdf` | PDF | Slides 16-18 |
| `双端适配集成研发模式技术分析方案.pdf` | PDF | Slides 16-18 |
| `Mgmt PC FMS 异步化加载技术方案调研.pdf` | PDF | Slide 19 |
| `mgmt-app-h5-release` source code | Code | Code references and implementation mapping |
| `ssc-fe-version-mgr-sdk-master` source code | Code | Slides 11, 15, 18, 19 |

## File Structure

| Path | Purpose |
| --- | --- |
| `index.html` | HTML slide deck |
| `CHANGELOG.md` | Change log and source tracking |
| `slide-previews/` | Generated single-slide QA previews |
| `preview-slides.png` | Generated long preview contact image |

# Transify HTML Slide Changelog

## Round Table

| Round | Date | Summary | Page Count Change |
| --- | --- | --- | --- |
| 1 | 2026-06-12 | Created a 10-slide HTML deck for resume/project-experience storytelling. | 0 -> 10 |

## Round 1 Details

- Added `index.html` as a fixed 1280x720 HTML slide deck.
- Covered project background, problem statement, goals, architecture, runtime flow, key algorithm, vue-i18n wrapper, collection/upload pipeline, solution trade-offs, and resume-ready phrasing.
- Used local source code excerpts from `src/transify/common.ts`, `src/transify/gt-vue.ts`, and `src/transify/upload-tool.ts`.
- Used local documentation from `docs/transify-tool-overview.md` and `docs/项目经验.md`.
- Rendered all 10 slides as single-slide previews and verified each preview is 1280x720.
- The local Python environment does not include Pillow, so preview screenshots were manually top-cropped after rendering; contact-sheet and long-preview generation were skipped by the render script.

## Content Sources Summary

| Source | Type | Used For |
| --- | --- | --- |
| `docs/transify-tool-overview.md` | Local Markdown | Overall tool chain, API behavior, CLI relationship, known limitations. |
| `docs/项目经验.md` | Local Markdown | Resume positioning and project contribution summary. |
| `src/transify/common.ts` | Source Code | MD5 16-bit key generation implementation. |
| `src/transify/gt-vue.ts` | Source Code | Runtime `$gt` wrapper and fallback logic. |
| `src/transify/upload-tool.ts` | Source Code | Development key collection, export, and commented upload state. |

## File Structure

| File | Purpose |
| --- | --- |
| `index.html` | Self-contained HTML slide deck. |
| `CHANGELOG.md` | Change tracking and source summary for the deck. |
| `slide-previews/` | Generated per-slide QA screenshots, if rendering is available. |

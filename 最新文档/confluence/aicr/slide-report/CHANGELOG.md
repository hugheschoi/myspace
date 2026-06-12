# IBS CLI Slide Report Changelog

## Modification Rounds

| Round | Date | Summary | Page Count Change |
|---|---:|---|---:|
| 1 | 2026-06-12 | Created a standalone HTML slide/report deck for the `@shopee/ibs-cli` project, covering project structure, CLI commands, CR workflow, Git diff parsing, Cursor integration, Git hooks, protocol handling, risks, and improvement roadmap. | +31 slides |

## Round 1 Details

- Added `index.html` as a fixed 1280x720 HTML slide deck with 31 sections: 1 cover slide and 30 numbered content slides.
- Used a self-contained CSS layout with no external runtime assets.
- Organized content into six sections:
  - Project overview and repository structure
  - CLI entry and command matrix
  - CR Shift-Left workflow
  - Git data collection and diff parsing
  - Cursor deep link and `ibs://` protocol
  - Git hooks, risks, and recommended improvements
- Included code excerpts and implementation notes from key project files.
- Added risk analysis for the inconsistent final diff compression, shell command construction, global hooksPath override, stale `--no-cr` documentation, unregistered lifecycle scripts, and missing automated tests.

## Content Sources Summary

| Source | Type | Sections Informed |
|---|---|---|
| `package.json` | Source code / package metadata | Package identity, CLI bin entry, dependencies, lifecycle caveat |
| `bin/index.js` | Source code | CLI bootstrap, registered commands, CR/update/hooks command dispatch, Cursor deep link sending |
| `lib/code-review.js` | Source code | CR modes, HTTP session setup, payload fields, MR/rerun behavior |
| `lib/git-utils.js` | Source code | Git command usage, diff parsing, commit metadata, rule scanning, compression behavior |
| `lib/filter-config-cache.js` | Source code | Remote/default file filtering strategy |
| `lib/clipboard-manager.js` | Source code | Cursor deep link and legacy clipboard automation |
| `lib/git-hooks-manager.js` | Source code | Global hooks, local hook injection, wrapper behavior, uninstall/restore flow |
| `lib/ibs-protocal.js` | Source code | macOS `ibs://` protocol registration and Terminal command launcher |
| `scripts/postinstall.js` / `scripts/preuninstall.js` | Source code | Local install/uninstall hook lifecycle intent |
| `README.md` | Documentation | User-facing command descriptions and environment variables |
| `docs/exclude-delete-files.md` | Documentation | Rationale for excluding deleted files with `--diff-filter=d` |

## File Structure

| File | Purpose |
|---|---|
| `docs/ibs-cli-slide-report/index.html` | Main HTML slide deck |
| `docs/ibs-cli-slide-report/CHANGELOG.md` | Change record and source summary |
| `docs/ibs-cli-slide-report/slide-previews/` | Rendered per-slide preview images generated during QA |
| `docs/ibs-cli-slide-report/preview-slides.png` | Contact preview generated during QA when available |

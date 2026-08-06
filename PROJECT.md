# Project: JSON Best Practices Summary Injection

## Architecture
- **Source file**: `json_best_practices.html` (embedded `<style>` block + inner container content lines 148–200).
- **Target file**: `docs/interactive_learning.html` (7936 lines, dark glassmorphism design system `--bg-0: #0b0f19`).
- **Scoping Strategy**: Wrapped injected HTML in `<section class="json-best-practices-section" id="json-best-practices-section">`. Scoped all injected CSS selectors under `#json-best-practices-section` (`.jbp-card`, `.jbp-grid`, `.jbp-subtitle`, etc.) guaranteeing 100% style isolation without external libraries.
- **Insertion Point**: Lines 7931–8137 in `docs/interactive_learning.html` immediately preceding `</body>` at line 8139.

## Feature Inventory
| # | Feature | Description | Milestone | Source | Status |
|---|---------|-------------|-----------|--------|--------|
| 1 | Content Injection | Extract inner container (lines 148–200) from `json_best_practices.html` and inject before `</body>` tag | M1 | R1 | DONE |
| 2 | CSS Rule Scoping | Scope all extracted CSS under `#json-best-practices-section` and rename colliding classes to `.jbp-*` | M1 | R2 | DONE |
| 3 | Layout & Theme Integrity | Ensure existing modules m1–m8 retain dark glassmorphic cards and global theme (`#0b0f19`) | M1 | R2 | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| 1 | HTML Injection & CSS Scoping | Inject content before `</body>` and apply scoped CSS styles | none | DONE |

## Interface Contracts
### `json_best_practices.html` ↔ `docs/interactive_learning.html`
- Wrapper element: `<section class="json-best-practices-section" id="json-best-practices-section">`
- Placement: Lines 7931–8137 (immediately before `</body>` at line 8139).
- Style isolation: All selectors scoped with `#json-best-practices-section`.
- Visibility: Independent document footer section, preserving `App.switchTab` behavior.

## Code Layout
- `docs/interactive_learning.html`: Modified target document containing injected JSON best practices summary section.
- `json_best_practices.html`: Read-only source document.

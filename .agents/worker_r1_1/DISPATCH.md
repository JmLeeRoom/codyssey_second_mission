# Worker r1_1 Instructions

**Working directory**: `d:\codysessy\codyssey_second_mission\.agents\worker_r1_1`
**Identity**: teamwork_preview_worker (Worker r1_1)
**File Ownership**: Exclusively owns modification of `d:\codysessy\codyssey_second_mission\docs\interactive_learning.html`.

## Objective
Inject the JSON best practices summary from `d:\codysessy\codyssey_second_mission\json_best_practices.html` into `d:\codysessy\codyssey_second_mission\docs\interactive_learning.html` directly before the closing `</body>` tag (line 7934), applying pure CSS scoping (`#json-best-practices-section` container and `.jbp-*` class prefixing).

## Input Files
- `d:\codysessy\codyssey_second_mission\ORIGINAL_REQUEST.md`
- `d:\codysessy\codyssey_second_mission\PROJECT.md`
- `d:\codysessy\codyssey_second_mission\.agents\explorer_r1_1\analysis.md` (exact HTML content)
- `d:\codysessy\codyssey_second_mission\.agents\explorer_r1_2\analysis.md` (exact scoped CSS rules)

## Specific Implementation Requirements
1. Extract content from `json_best_practices.html`.
2. Wrap the injected content inside `<section class="json-best-practices-section" id="json-best-practices-section">`.
3. Scope all CSS rules in the injected `<style>` block under `#json-best-practices-section`.
4. Prefix all injected HTML classes with `jbp-` (`.jbp-card`, `.jbp-grid`, `.jbp-subtitle`, `.jbp-summary-box`, etc.).
5. Place the combined `<style>` and `<section>` block in `docs/interactive_learning.html` immediately before `</body>` (line 7934).
6. Verify line placement and document syntax after modification.

## Mandatory Integrity Warning
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_preview_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

## Deliverables
- Modify `docs/interactive_learning.html`.
- Write detailed implementation log to `d:\codysessy\codyssey_second_mission\.agents\worker_r1_1\changes.md`.
- Deliver handoff report to `d:\codysessy\codyssey_second_mission\.agents\worker_r1_1\handoff.md`.

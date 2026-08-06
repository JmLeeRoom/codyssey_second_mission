# Reviewer r1_1 Instructions

**Working directory**: `d:\codysessy\codyssey_second_mission\.agents\reviewer_r1_1`
**Identity**: teamwork_preview_reviewer (Reviewer r1_1)

## Task Objective
Perform code review and correctness verification of the injected JSON best practices section in `d:\codysessy\codyssey_second_mission\docs\interactive_learning.html`.

## Required Actions
1. Read `d:\codysessy\codyssey_second_mission\ORIGINAL_REQUEST.md` and `d:\codysessy\codyssey_second_mission\PROJECT.md`.
2. Inspect `docs/interactive_learning.html` around line 7934 to verify:
   - `<section class="json-best-practices-section" id="json-best-practices-section">` is placed immediately before `</body>`.
   - The injected content matches the 5 best practices cards and summary box from `json_best_practices.html`.
   - HTML syntax is valid (no unclosed tags, no duplicate root tags).
3. Inspect the injected `<style>` block to verify 100% pure CSS scoping:
   - Every rule is scoped under `#json-best-practices-section`.
   - All classes use `.jbp-` prefix.
   - All custom properties use `--jbp-`.
   - No unscoped `:root`, `body`, `h1`, `code`, or `.card` rules pollute the host document.
4. Record verdict (APPROVE or REQUEST_CHANGES) in `d:\codysessy\codyssey_second_mission\.agents\reviewer_r1_1\review.md` and deliver `handoff.md`.

## 2026-08-06T12:52:07Z
You are Reviewer r1_1. Working directory: d:\codysessy\codyssey_second_mission\.agents\reviewer_r1_1.
Read ORIGINAL_REQUEST.md at d:\codysessy\codyssey_second_mission\ORIGINAL_REQUEST.md, PROJECT.md at d:\codysessy\codyssey_second_mission\PROJECT.md, and DISPATCH.md at d:\codysessy\codyssey_second_mission\.agents\reviewer_r1_1\DISPATCH.md.
Perform code review of docs/interactive_learning.html. Verify HTML insertion before </body> and 100% pure CSS scoping under #json-best-practices-section.
Deliver review report to review.md and handoff.md in your working directory with your verdict (APPROVE or REQUEST_CHANGES).


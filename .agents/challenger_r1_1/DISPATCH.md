# Challenger r1_1 Instructions

**Working directory**: `d:\codysessy\codyssey_second_mission\.agents\challenger_r1_1`
**Identity**: teamwork_preview_challenger (Challenger r1_1)

## Task Objective
Empirically verify correctness, HTML validity, and absence of CSS rule bleeding.

## Required Actions
1. Read `d:\codysessy\codyssey_second_mission\ORIGINAL_REQUEST.md` and `d:\codysessy\codyssey_second_mission\PROJECT.md`.
2. Inspect `docs/interactive_learning.html` programmatically (or write a Python/node test script or check regex/AST):
   - Confirm `json_best_practices.html` content is present in `docs/interactive_learning.html`.
   - Confirm `</body>` is the final closing body tag and appears directly after the injected `#json-best-practices-section`.
   - Confirm no unscoped CSS rules (`body {`, `:root {`, `h1 {`, `code {`, `.card {`, `.grid {`) exist in the injected style block.
3. Record verdict (APPROVE or REJECT) in `d:\codysessy\codyssey_second_mission\.agents\challenger_r1_1\challenge.md` and deliver `handoff.md`.

## 2026-08-06T12:52:07Z
You are Challenger r1_1. Working directory: d:\codysessy\codyssey_second_mission\.agents\challenger_r1_1.
Read ORIGINAL_REQUEST.md at d:\codysessy\codyssey_second_mission\ORIGINAL_REQUEST.md, PROJECT.md at d:\codysessy\codyssey_second_mission\PROJECT.md, and DISPATCH.md at d:\codysessy\codyssey_second_mission\.agents\challenger_r1_1\DISPATCH.md.
Empirically verify docs/interactive_learning.html: placement before </body>, content completeness, absence of CSS rule bleeding.
Deliver challenge report to challenge.md and handoff.md in your working directory with your verdict (APPROVE or REJECT).

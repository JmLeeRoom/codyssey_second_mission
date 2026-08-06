# Forensic Auditor r1_1 Instructions

**Working directory**: `d:\codysessy\codyssey_second_mission\.agents\auditor_r1_1`
**Identity**: teamwork_preview_auditor (Auditor r1_1)

## Task Objective
Perform forensic integrity audit of the modifications to `docs/interactive_learning.html`.

## Required Actions
1. Read `d:\codysessy\codyssey_second_mission\ORIGINAL_REQUEST.md` and `d:\codysessy\codyssey_second_mission\PROJECT.md`.
2. Inspect `docs/interactive_learning.html` and compare with `json_best_practices.html`.
3. Check for integrity violations:
   - Is the HTML injection real and complete (all 5 best practices cards + summary box present)?
   - Are there dummy/facade implementations or shortcuts taken?
   - Is the insertion location authentic (immediately before `</body>`)?
   - Is CSS scoping genuine and fully implemented?
4. Deliver verdict (**CLEAN** or **INTEGRITY VIOLATION**) with full evidence report in `d:\codysessy\codyssey_second_mission\.agents\auditor_r1_1\audit.md` and `handoff.md`.

# Master Plan — JSON Best Practices Injection

## 1. Objective
Inject the JSON best practices summary from `json_best_practices.html` into `docs/interactive_learning.html` directly before the closing `</body>` tag while preserving layout integrity and avoiding CSS collisions.

## 2. Execution Phases

### Phase 0: Survey & Exploration
- Dispatch 3 parallel Explorer agents (`teamwork_preview_explorer`) to inspect `json_best_practices.html`, `docs/interactive_learning.html`, and any associated CSS/JS files.
- Deliverables: Explorer reports on content structure, DOM tree, CSS rules, class collisions, and insertion boundary.

### Phase 1: PROJECT.md Initialization
- Aggregate Explorer findings into `PROJECT.md` at project root.
- Document Feature Inventory, Architecture, Interface Contracts, and Code Layout.

### Phase 2: Iteration 1 Loop
- **Explorers (3)**: Analyze insertion strategy and CSS merging plan.
- **Worker (1)**: Perform exact HTML injection before `</body>` tag and merge CSS rules safely. Run verification.
- **Reviewers (2)**: Independently review HTML validity, CSS scoping, and spec adherence.
- **Challengers (2)**: Empirically test HTML rendering, DOM integrity, and layout side-effects.
- **Auditor (1)**: Perform forensic integrity audit (detect hardcoding, facades, cheats).
- **Gate Check**: Validate all verdicts in `GATE_STATUS.md`.

### Phase 3: Final Hand-off & Sentinel Notification
- Verify completion criteria.
- Notify Sentinel / User of successful task execution.

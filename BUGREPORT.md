# ChillMCP Bug Report

## 1. Background updater deferred until first tool call
- **Severity:** Medium – Auto stress increase/cooldown relies on an initial tool invocation.
- **Location:** `main.py:91-98`, `main.py:252-332`
- **Details:** `ensure_background_task()` starts the scheduler only when the first tool is executed. If validators expect stress to rise or boss alert to cool down immediately after process start (without calling a tool), they will not see changes.
- **Suggested Fix:** Kick off the background task during startup (before `mcp.run`) so timing logic runs even before any tool usage.

## 2. Company dinner always reduces stress
- **Severity:** Low – Narrative deviation; spec allowed stress increase events.
- **Location:** `main.py:206-243`
- **Details:** The current implementation draws `random.randint(1, 100)` and always decreases stress, whereas earlier versions (and hackathon flavor text) hinted that some 회식 이벤트 could raise stress instead.
- **Suggested Fix:** Reintroduce mixed outcomes (positive and negative stress deltas) if we want to mirror the original behavior; otherwise, document the intentional simplification.

---
name: implement-feature
description: Implement a repository feature using a test-first, behavior-focused workflow.
---

# Implement a feature

1. Read the task, root `AGENTS.md`, applicable scoped guidance, and any relevant project documentation.
2. Inspect the implementation and existing tests related to the requested behavior.
3. State the expected behavior and identify the files that need to change.
4. Write a behavioral test for the expected success case and relevant failure or edge cases. Run it and confirm it fails for the intended reason.
5. Implement the smallest change that satisfies the behavior while preserving existing behavior.
6. Run `pytest` and review the changes for unintended effects.
7. Summarize the changes, test results, and any remaining risks.

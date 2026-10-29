# Week 4: Structuring a Repository for Agents

## 1. Root repository guidance

The root `AGENTS.md` introduces the project as a small FastAPI and SQLite link-shortening service and identifies the application, tests, task list, and dependency file. It gives the installation, server, and pytest commands, sets product boundaries against unrelated endpoints or infrastructure, and describes an Understand → Test → Implement → Verify workflow. This central orientation gives an agent the minimum context needed to begin work without repeating implementation detail.

## 2. Scoped test guidance

`tests/AGENTS.md` applies specifically to files under `tests/`. It asks for public-API, behavior-focused assertions, success and failure coverage, and independent tests that do not depend on execution order or persistent database contents. The existing `test_main.py` remains at the repository root, so this scoped file does not govern it. Keeping test-specific advice scoped prevents it from being applied to application code or other unrelated files; root-level expectations belong in the root guide instead.

## 3. Reusable implementation skill

The reusable `.github/skills/implement-feature/SKILL.md` describes a seven-step procedure: read the task and applicable guidance; inspect relevant implementation and tests; state expected behavior and affected files; write behavioral tests and confirm their expected failure; make the smallest implementation; run pytest and review the change; and summarize changes, results, and risks. This turns the repository’s general workflow into a repeatable, test-first task procedure.

## 4. Copilot discovery and invocation

The root guidance is placed at the repository root so Copilot can use it as general workspace context. The tests guide is nested under `tests/` to scope its instructions to that directory. The skill is located at `.github/skills/implement-feature/SKILL.md`, where GitHub Copilot Agent Skills can discover it; explicitly requesting the skill in the implementation prompt made its procedure part of the task.

## 5. Plan, implementation, and review

In Plan, I selected Task 1, Custom Alias, and identified the API and test changes. In Implement, I first added behavioral tests; the original suite had three passing tests, and the new validation cases initially failed. The implementation then accepted optional aliases, returned 409 for duplicates, and skipped generated codes already occupied by aliases. Review returned REVISE because unrestricted aliases could break redirects and the collision test used shared database state. The fix restricted aliases to 1–64 ASCII letters, digits, hyphens, or underscores, rejected FastAPI’s reserved `docs` and `redoc` paths, and isolated tests with `tmp_path`, `monkeypatch`, and `main.init_db()`. The follow-up review accepted the result. The final suite had 15 passing tests.

## 6. Lessons

Concise guidance is effective when it identifies where to look, how to test, and what boundaries to respect, rather than duplicating the codebase. Scoped instructions must match the actual directory layout: the nested test guide does not silently apply to root-level tests. A reusable skill provides more procedural detail without making every repository instruction lengthy. Finally, behavior-focused tests and an independent review exposed important edge cases—URL-path validity, reserved routes, and database isolation—that the initial happy path did not capture. Pytest reported a non-blocking Starlette/httpx deprecation warning.

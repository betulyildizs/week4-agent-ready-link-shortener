# Agent Guide

## Application

This repository contains a small FastAPI and SQLite link-shortening service.

## Important files

- `main.py` — application, database setup, `POST /shorten`, and redirect endpoint.
- `test_main.py` — public API behavior tests.
- `docs/TASKS.md` — available feature tasks.
- `requirements.txt` — Python dependencies.

## Setup, run, and test

- Install dependencies: `pip install -r requirements.txt`
- Run the service: `uvicorn main:app --reload`
- Run tests: `pytest`

## Product boundaries

- Keep changes focused on the selected task and the existing link-shortener API.
- Preserve existing behavior unless a task explicitly requires a change.
- Do not add unrelated endpoints, dependencies, or infrastructure.
- Keep SQLite persistence and the existing API response conventions unless a task requires otherwise.

## Workflow

1. **Understand:** Read the task, this guide, relevant scoped guidance, implementation, and tests. Identify expected behavior and affected files.
2. **Test:** Add or update behavior-focused tests, including relevant success and failure cases. Run them to confirm the expected behavior.
3. **Implement:** Make the smallest complete change that satisfies the task and follows existing patterns.
4. **Verify:** Run `pytest`, inspect the final changes, and report what changed, test results, and remaining risks.

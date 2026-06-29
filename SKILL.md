# Frappe / ERPNext Agent Skill

Short name: frappe-erpnext-agent

Purpose
- Enable an assistant to work effectively on Frappe and ERPNext projects: diagnosing issues, implementing doctypes/pages, writing server/client code, and following ERPNext conventions.

When to use
- Workspace-scoped skill for repositories built on Frappe/ERPNext.
- Use when tasks require knowledge of Frappe doctypes, hooks, fixtures, js front-end, or common ERPNext patterns.

Inputs the agent expects
- Project layout (apps, module paths, doctypes). Example: `apps/<app_name>/` with `doctype/`, `page/`, `public/`.
- Ticket or user story describing desired change.
- Target branch or file path to modify.

Step-by-step process (recommended)
1. Explore: list top-level app folders and `doctype/`, `page/`, `public/`, `hooks.py` files.
2. Reproduce: run or simulate minimal steps to reproduce the issue (log inspection, search for error strings, open tests).
3. Identify: find the responsible file(s) and relevant functions/classes.
4. Propose fix: provide a concise patch or code change that follows Frappe patterns (use `frappe.get_all`, `frappe.get_doc`, `frappe.db.get_value`, whitelist, permissions, and `frappe.msgprint` where appropriate).
5. Validate: run existing tests or add a small test (if repo has test harness). Mention manual verification steps if tests not available.
6. Iterate: ask clarifying questions and refine the change.

Decision points / Branching logic
- If change affects DB schema (doctype changes): recommend migration via patches and avoid direct schema edits.
- If change affects public JS/CSS: ensure assets are built/compiled where applicable and note `bench build` or `yarn` steps.
- If change touches permissions or docstatus: enforce checks and tests for role-based behavior.

Quality criteria / Completion checks
- Code follows Frappe naming and import patterns.
- No raw SQL unless necessary; use `frappe.db` helpers.
- Database-affecting changes include a patch or migration plan.
- Unit tests added or existing tests updated when reasonable.
- Add or update docs (README or module docs) for significant behavior changes.

Examples (prompts to use)
- "Search the repo for `frappe.throw` occurrences related to booking validation and propose a non-blocking warning alternative." 
- "Add `@frappe.whitelist()` to `get_unavailable_resources` and ensure type hints are compatible with Python versions used in this repo." 
- "Create a unit test for `Safari Operations Sheet` validate() that covers `set_booking_details()` behavior."

Template checks and best practices
- Always run a workspace-wide grep for function/class names before renaming.
- Prefer small, focused commits with a short message and a descriptive body.
- When adding API endpoints, include permission checks and document expected params.

Ambiguities to clarify with user
- Should the skill be applied workspace-wide or as a personal helper for the user?
- Does the project use a specific bench/ERPNext version that constrains APIs or typing?
- Are there CI/test constraints to follow (e.g., slow integration tests)?

Iteration guidance
1. Draft change and include a minimal test or a manual verification checklist.
2. Run tests or request the user to run `bench --site <site> migrate` and `bench build` if assets changed.
3. If failing tests, collect tracebacks and iterate.

Example usage snippets (for the assistant)
- "I'll search `doctype/*` for calls to `get_unavailable_resources()` and collect usages before editing."
- "I'll add a small unit test in `doctype/safari_booking/test_safari_booking.py` that creates a booking and asserts vehicle assignment conflicts are reported."

Related customizations to create next
- A `CHECKLIST.md` that encodes the repo's preferred PR checklist.
- A `TEST_GUIDE.md` describing how to run unit/integration tests in this repo.

Maintainer notes
- Keep the skill updated when the project upgrades ERPNext major versions.
- Record common patterns (e.g., where `frappe.get_all` is preferred over raw queries) in `/memories/repo/`.

---

Created by the assistant to support Frappe/ERPNext tasks in this repository.
# Frappe / ERPNext Agent Skill

## Purpose
Provide a reusable skill for an agent that is expert in the Frappe framework and ERPNext conventions. The skill encodes a recommended step-by-step workflow, decision points, quality checks, and example prompts so other agents (or users) can follow the same process consistently.

## When to use
- Workspace-scoped: use when working inside a Frappe app repository (implementations, doctypes, pages, tests).
- Use for: debugging, creating doctypes/pages, writing server-side Python hooks, client-side JS, patches, and test cases that follow ERPNext conventions.

## Expected inputs
- Repository path or a reference to the target doctype/module/file.
- Brief description of goal (bugfix, new feature, refactor, test, or packaging).
- Optional constraints (ERPNext version, target branch, or backward-compatibility requirements).

## Step-by-step process
1. Explore repository structure and identify the app and doctype(s) involved.
2. Reproduce the problem or confirm the requested change: run relevant tests or inspect failing logs (if available).
3. Locate canonical files: doctypes, controllers, hooks.py, patches, public assets, and test files.
4. Propose minimal, targeted changes that follow Frappe patterns (DB-level queries via ORM, Document methods, whitelisted functions, client events).
5. Implement the change in the smallest scope possible; add unit tests or update existing tests when relevant.
6. Run tests or linting locally if possible; fix any introduced errors.
7. Prepare a short summary of changes and next steps (commit message, tests to run, potential migration steps).

## Decision points and branching
- If change requires DB migrations/patches, create a patch entry and include idempotency checks.
- If the change affects public API or data model, require a compatibility note and release notes entry.
- If the change is purely UI (client JS/CSS), prefer non-breaking DOM selectors and progressive enhancement.

## Quality criteria / Acceptance checks
- Code follows Frappe conventions (use Document methods, avoid raw SQL unless necessary).
- No direct prints/logging in production code; use `frappe.log_error` for exceptions as needed.
- Tests cover edge cases for business rules and permissions.
- Patch/fixture application is idempotent and safe to re-run.
- Client-side code is resilient to missing DOM elements and respects roles/permissions.

## Examples / Example prompts
- "Add server-side validation to `Safari Booking` so `end_date >= start_date` and include a unit test." 
- "Find why `get_unavailable_resources` returns duplicates and fix the sorting/unique logic." 
- "Create a patch to migrate `vehicle` field values to new naming convention and ensure idempotency."

## Templates and snippets
- Issue triage checklist: reproduction steps, logs, failing tests, minimal reproduction branch.
- Patch stub: add a function under `patches/` that checks existence and updates records with safety.

## Notes for iterating
1. Start with minimal changes and tests.
2. Ask reviewer for clarifying business rules when needed (e.g., seasonal booking overlaps, driver rest constraints).
3. When uncertain about ERPNext API behavior, consult the Frappe docs or run an interactive shell (`bench console`).

## Suggested follow-ups
- Map common repo locations (doctypes, pages, hooks) in a repo-scoped README for faster onboarding.
- Add linting/formatting pre-commit hooks and a `pyproject.toml` section for tools used.

---
Generated for: an agent specialized in Frappe and ERPNext development. Adjust scope (workspace vs personal) before publishing as a shared skill.

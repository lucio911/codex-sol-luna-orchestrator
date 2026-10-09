# Execution work-package contract

The primary agent should send `luna_executor` work packages with these fields (plain text is fine):

| Field | Required content |
|---|---|
| Objective | Verifiable behavior or deliverable |
| Context | Relevant functions, files, design decisions, repository instructions |
| Allowed scope | Paths/modules authorized for edits; files that must remain untouched |
| Constraints | Compatibility, performance, security, scientific assumptions, coding style |
| Acceptance tests | Specific commands or verifiable outcomes; distinguish runnable from unavailable |
| Return format | Files changed, what changed, tests + results, warnings, unresolved questions |

Example:

> Objective: Fix incorrect displacement unit conversion in `src/postprocess.py`.
> Context: Input data is meters; plotting uses millimeters; maintain public API.
> Allowed scope: `src/postprocess.py` and `tests/test_postprocess.py` only.
> Acceptance: Run `python -m pytest tests/test_postprocess.py` (if available); show a regression test for 0.005 m -> 5 mm.
> Return: concise diff summary, test command and output, any remaining concerns.

The primary agent owns the overall plan, acceptance criteria, final review, and communication with the user. Luna owns only the delegated implementation, its local tests, and accurate reporting.

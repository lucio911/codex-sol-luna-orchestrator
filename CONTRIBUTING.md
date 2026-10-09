# Contributing

1. Open an issue with a reproducible scenario or improvement proposal.
2. Fork the repository and make changes on a branch.
3. Run `python scripts/validate.py` and `python -m unittest discover -s tests -v` using Python 3.11+.
4. Submit a pull request describing motivation, tests, and limitations.

Keep the package dependency-free whenever feasible. Never include API keys, session tokens, identifiable research data, or real credentials in examples. Model IDs are configurable and may require independent entitlements; do not promise live multi-model routing without recorded evidence.
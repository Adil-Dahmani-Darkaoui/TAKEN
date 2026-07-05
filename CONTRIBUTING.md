# Contributing to TAKEN

Thanks for your interest. TAKEN is a **defensive** privacy toolkit, and
contributions must keep it that way.

## The one hard rule

TAKEN audits and protects the **operator's own** exposure. It does not
de-anonymise, locate, or profile other people. Before opening a pull request,
read [`docs/SCOPE.md`](docs/SCOPE.md).

Contributions that add any of the excluded capabilities — third-party
de-anonymisation, cross-account correlation / stylometric unmasking, GEOINT
against others, social-circle or review scraping to locate someone, bulk
targeting, or account-recovery probing of third parties — are **out of scope**
and will be closed. So will changes that generalise a self-scoped feature into
one that targets other people.

Good contributions make it easier for a person to understand and reduce their
own footprint, improve the accuracy of the defensive guidance, or harden the
existing self-scoped features.

## Development setup

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

- Core code stays on the Python standard library; heavier dependencies belong
  behind an optional extra (see `pyproject.toml`).
- Add tests for new behaviour. The suite must pass on Python 3.9–3.12 (CI
  enforces this).
- Keep new user-facing text clear about *who* a feature acts on — it should
  always be the operator themselves.

## Reporting a security or scope concern

If you believe a feature could be misused against third parties, open an issue
describing the concern. Narrowing a capability toward pure self-defense is
always in scope.

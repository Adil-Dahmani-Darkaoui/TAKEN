import pytest

from taken import footprint


def test_preview_mode_makes_no_requests(monkeypatch):
    # If consent is not given, _profile_exists must never be called.
    def _boom(*args, **kwargs):
        raise AssertionError("no network call should happen in preview mode")

    monkeypatch.setattr(footprint, "_profile_exists", _boom)
    results = footprint.audit("someone", consent=False)
    assert len(results) == len(footprint.PLATFORMS)
    assert all(r.checked is False for r in results)
    assert all(r.found is None for r in results)
    assert all(r.remediation for r in results)


def test_handle_is_normalised():
    results = footprint.audit("@Handle", consent=False)
    assert all("@" not in r.url.split("//", 1)[1] for r in results)


def test_empty_handle_rejected():
    with pytest.raises(ValueError):
        footprint.audit("   ", consent=False)


def test_consent_triggers_checks(monkeypatch):
    calls = []

    def _fake(url, *, timeout):
        calls.append(url)
        return True

    monkeypatch.setattr(footprint, "_profile_exists", _fake)
    results = footprint.audit("me", consent=True)
    assert len(calls) == len(footprint.PLATFORMS)
    assert all(r.checked and r.found is True for r in results)

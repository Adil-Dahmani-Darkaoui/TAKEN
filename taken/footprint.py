"""Footprint self-audit (defensive, self-scoped, consent-gated).

This module helps you see where *your own* handle is publicly discoverable so
you can lock down or delete accounts you forgot about. It is deliberately not
a general username scanner:

  - It only runs live checks when you explicitly pass ``consent=True``,
    affirming that the handle is your own.
  - It checks a small, fixed list of major consumer platforms via their
    public profile URLs — the same thing you could do by typing the handle
    into each site's address bar.
  - Its output is a *remediation* checklist, not an intelligence dossier. It
    does not resolve a handle to a real name, location, email, or any other
    identity attribute.

If you want to know what an attacker could infer about someone *else*, the
answer this project gives is: that is doxxing, and Taken will not help do it.
See ``docs/SCOPE.md``.
"""

from __future__ import annotations

import urllib.error
import urllib.request
from dataclasses import dataclass

# Public profile URL templates for major consumer platforms. A 200 means a
# profile page renders at that path; it is not proof of account ownership and
# some sites soft-404 with a 200, so results are hints, not verdicts.
PLATFORMS: dict[str, str] = {
    "GitHub": "https://github.com/{handle}",
    "GitLab": "https://gitlab.com/{handle}",
    "Reddit": "https://www.reddit.com/user/{handle}",
    "Instagram": "https://www.instagram.com/{handle}/",
    "Twitch": "https://www.twitch.tv/{handle}",
    "Flickr": "https://www.flickr.com/people/{handle}",
    "Pinterest": "https://www.pinterest.com/{handle}/",
    "Steam": "https://steamcommunity.com/id/{handle}",
}

_REMEDIATION: dict[str, str] = {
    "GitHub": "Review your public repos, gists, commit emails, and profile "
    "README. Set a no-reply commit email in Settings > Emails.",
    "GitLab": "Check public projects and your activity feed visibility in "
    "profile settings.",
    "Reddit": "Old comments are a stylometry and location goldmine. Review "
    "your history; consider editing/deleting posts that place you.",
    "Instagram": "Set the account private; remove location tags from past "
    "posts; strip the bio of your city/employer.",
    "Twitch": "Check your About panel and past clips for background details "
    "that reveal your home or workplace.",
    "Flickr": "Turn off 'import EXIF location data' and scrub geotags from "
    "existing photos; Flickr can expose GPS publicly.",
    "Pinterest": "Make boards secret if they reveal your neighbourhood, "
    "workplace, or routines.",
    "Steam": "Set your profile and game details to Friends-only; a public "
    "profile leaks your activity schedule.",
}

_USER_AGENT = "Taken-footprint-self-audit/0.1 (+defensive privacy self-check)"


@dataclass
class PlatformResult:
    platform: str
    url: str
    checked: bool
    found: bool | None  # None when not live-checked
    remediation: str


def audit(handle: str, *, consent: bool = False, timeout: float = 8.0) -> list[PlatformResult]:
    """Audit where ``handle`` is publicly present across major platforms.

    When ``consent`` is False (the default) no network requests are made: the
    function returns the list of URLs it *would* check plus remediation advice,
    so you can review the scope first. Pass ``consent=True`` only for a handle
    you own to run the live checks.
    """
    handle = handle.strip().lstrip("@")
    if not handle:
        raise ValueError("handle must not be empty")

    results: list[PlatformResult] = []
    for platform, template in PLATFORMS.items():
        url = template.format(handle=urllib.request.quote(handle))
        remediation = _REMEDIATION.get(platform, "Review this profile's privacy settings.")
        if not consent:
            results.append(
                PlatformResult(platform, url, checked=False, found=None, remediation=remediation)
            )
            continue
        found = _profile_exists(url, timeout=timeout)
        results.append(
            PlatformResult(platform, url, checked=True, found=found, remediation=remediation)
        )
    return results


def _profile_exists(url: str, *, timeout: float) -> bool | None:
    """Best-effort check for whether a public profile renders at ``url``.

    Returns True/False, or None if the check was inconclusive (network error,
    rate limit, etc.). Uses a GET with a short read to respect the sites.
    """
    request = urllib.request.Request(url, method="GET", headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= response.status < 300
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return False
        if exc.code in (403, 429):
            return None  # blocked / rate-limited: inconclusive, not absent
        return None
    except (urllib.error.URLError, TimeoutError, OSError):
        return None

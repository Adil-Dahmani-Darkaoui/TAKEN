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
    "GitHub": "Passez en revue vos dépôts publics, gists, e-mails de commit et le "
    "README de profil. Définissez un e-mail de commit no-reply dans Settings > Emails.",
    "GitLab": "Vérifiez les projets publics et la visibilité de votre fil "
    "d'activité dans les réglages du profil.",
    "Reddit": "Les vieux commentaires sont une mine pour la stylométrie et la "
    "localisation. Passez en revue votre historique ; envisagez de modifier/"
    "supprimer les messages qui vous situent.",
    "Instagram": "Passez le compte en privé ; retirez les tags de lieu des "
    "anciennes publications ; nettoyez la bio de votre ville/employeur.",
    "Twitch": "Vérifiez votre panneau « À propos » et vos anciens clips pour les "
    "détails d'arrière-plan qui révèlent votre domicile ou lieu de travail.",
    "Flickr": "Désactivez « importer les données de localisation EXIF » et "
    "retirez les géotags des photos existantes ; Flickr peut exposer le GPS "
    "publiquement.",
    "Pinterest": "Rendez les tableaux secrets s'ils révèlent votre quartier, "
    "votre lieu de travail ou vos habitudes.",
    "Steam": "Passez votre profil et vos détails de jeu en « Amis uniquement » ; "
    "un profil public divulgue votre emploi du temps d'activité.",
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
        raise ValueError("le pseudo ne doit pas être vide")

    results: list[PlatformResult] = []
    for platform, template in PLATFORMS.items():
        url = template.format(handle=urllib.request.quote(handle))
        remediation = _REMEDIATION.get(
            platform, "Passez en revue les réglages de confidentialité de ce profil."
        )
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

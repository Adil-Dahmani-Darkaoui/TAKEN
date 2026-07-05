"""Legal framework and victim-support resources (defensive content).

Doxxing — publishing information to identify or locate someone in order to
expose them to harm — is a crime in France (Article 223-1-1 of the Penal
Code) and elsewhere. This module surfaces the law and, more importantly, the
help available to people who are being targeted.

The URLs and legal details below are France-focused because the source
material is French. If you are elsewhere, contact your local equivalent
(national cybercrime reporting portal, victim-support hotline, and police).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    name: str
    what: str
    url: str


LEGAL_NOTE = (
    "France — Article 223-1-1 of the Penal Code (created by the law of "
    "24 August 2021):\n"
    "  Revealing, spreading, or transmitting by any means information that "
    "identifies or locates a person, with intent to expose them or their "
    "family to a direct risk of harm to person or property, is punishable by "
    "3 years' imprisonment and a 45,000 EUR fine.\n"
    "  This rises to 5 years and 75,000 EUR when the victim is a minor, an "
    "elected official, a journalist, or a public official.\n\n"
    "Doxxing is distinct from lawful OSINT by its intent to cause harm. This "
    "toolkit is defensive: it helps people protect themselves and does not "
    "de-anonymise or locate others."
)

IF_YOU_ARE_TARGETED = (
    "If you are being doxxed or harassed:\n"
    "  1. Do NOT delete your accounts impulsively — first preserve evidence.\n"
    "  2. Take dated screenshots capturing the content, the URLs, usernames, "
    "and timestamps.\n"
    "  3. Report the content to the platform and to the authorities below.\n"
    "  4. Reach out to a support service — you do not have to handle this "
    "alone.\n"
    "  5. If you are in immediate physical danger, call your local emergency "
    "number (112 in the EU)."
)

SUPPORT_RESOURCES: tuple[Resource, ...] = (
    Resource(
        "Pharos",
        "French government portal for reporting illegal online content.",
        "https://www.internet-signalement.gouv.fr/",
    ),
    Resource(
        "3018",
        "Free, anonymous national hotline for victims of cyberviolence and "
        "harassment (France).",
        "https://www.3018.fr/",
    ),
    Resource(
        "e-Enfance",
        "Public-interest association protecting minors online (France).",
        "https://e-enfance.org/",
    ),
    Resource(
        "Stop Fisha",
        "Collective fighting sexist and sexual cyber-harassment and raids.",
        "https://stopfisha.org/",
    ),
    Resource(
        "France Victimes",
        "National network providing legal and psychological support to "
        "victims of crime.",
        "https://www.france-victimes.fr/",
    ),
)


def render_resources() -> str:
    """Return the legal note and support resources as readable text."""
    lines = ["LEGAL FRAMEWORK", "=" * 15, "", LEGAL_NOTE, "", "", "IF YOU ARE TARGETED", "=" * 19, "", IF_YOU_ARE_TARGETED, "", "", "SUPPORT RESOURCES", "=" * 17, ""]
    for r in SUPPORT_RESOURCES:
        lines.append(f"- {r.name}: {r.what}")
        lines.append(f"    {r.url}")
    return "\n".join(lines)

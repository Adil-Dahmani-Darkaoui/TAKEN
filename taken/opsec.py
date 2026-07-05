"""OPSEC hardening playbook (defensive content).

Each entry inverts one technique from the source awareness video into a
concrete countermeasure the reader can apply to themselves. The goal is the
same as the video's: help people understand how exposure happens so they can
reduce it.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Countermeasure:
    attack: str
    why_it_works: str
    defenses: tuple[str, ...]


PLAYBOOK: tuple[Countermeasure, ...] = (
    Countermeasure(
        attack="Username enumeration across platforms (Sherlock / WhatsMyName style)",
        why_it_works=(
            "One reused handle links every account that shares it, collapsing "
            "compartmentalisation instantly."
        ),
        defenses=(
            "Use a distinct, unrelated username for each identity sphere "
            "(work, gaming, activism, personal).",
            "Never let a throwaway handle touch an account tied to your real name.",
            "Generate random handles rather than variations on a favourite word — "
            "'argentic', 'argentic.34', 'argentic34' are one enumeration away "
            "from each other.",
            "Periodically self-audit your own handles (see `taken footprint`).",
        ),
    ),
    Countermeasure(
        attack="Email discovery via account-recovery probing (Holehe style)",
        why_it_works=(
            "Login and password-reset forms often reveal whether an email is "
            "registered, mapping an address to a service."
        ),
        defenses=(
            "Use a separate email address per identity sphere.",
            "Use email aliases / plus-addressing or a relay (e.g. hide-my-email) "
            "so a leaked address cannot be pivoted to your primary inbox.",
            "Prefer providers that do not disclose registration status on their "
            "recovery forms.",
            "Check your addresses against breach notifications and rotate any "
            "that appear.",
        ),
    ),
    Countermeasure(
        attack="Discord Snowflake timestamp extraction",
        why_it_works=(
            "The ID itself encodes the exact creation time in milliseconds — a "
            "fixed anchor for a pattern-of-life timeline."
        ),
        defenses=(
            "Assume your Discord ID's timestamp is public; you cannot hide it.",
            "Do not pair a compartmentalised Discord account with a handle or "
            "avatar you use elsewhere — the timestamp only helps an analyst "
            "once it is matched to another account.",
            "Lock down your profile and disable message history where possible.",
        ),
    ),
    Countermeasure(
        attack="Archive mining (Wayback Machine / CDX history)",
        why_it_works=(
            "The web remembers. A cleaned-up profile from today may have an "
            "un-redacted snapshot from years ago exposing an old email or name."
        ),
        defenses=(
            "Assume anything you ever posted publicly is permanently archived — "
            "deletion today does not remove yesterday's snapshot.",
            "Before publishing, ask whether you would be comfortable with it "
            "surviving forever; if not, do not post it.",
            "Request removal of specific archived pages where a service offers "
            "it, but treat that as best-effort, not a guarantee.",
            "Rotate emails/handles that appear in old archives so a leaked "
            "fragment no longer maps to a live account.",
        ),
    ),
    Countermeasure(
        attack="Stylometry (writing-style fingerprinting to link identities)",
        why_it_works=(
            "Sentence length, punctuation habits, and vocabulary are largely "
            "unconscious and persist across pseudonyms."
        ),
        defenses=(
            "Understand you cannot fully mask your style; the strongest defense "
            "is to not co-locate two identities that must stay separate in the "
            "first place.",
            "Keep sensitive identities low-volume — the less text you produce "
            "under a pseudonym, the weaker any stylometric model against it.",
            "Be aware that machine translation or heavy paraphrasing changes "
            "some markers but not all.",
        ),
    ),
    Countermeasure(
        attack="Chronobiological correlation (activity-timing heatmaps)",
        why_it_works=(
            "When two 'unrelated' accounts post on the same daily/weekly rhythm "
            "and time zone, the overlap becomes strong linking evidence."
        ),
        defenses=(
            "Do not assume different accounts are unlinkable just because the "
            "names differ; their timing correlates them.",
            "Schedule/queue posts rather than posting live if a rhythm would be "
            "revealing.",
            "Be mindful that a time zone leaks from posting hours alone.",
        ),
    ),
    Countermeasure(
        attack="EXIF / GPS metadata harvesting from photos",
        why_it_works=(
            "Phones geotag photos by default; a single un-stripped image pins "
            "you to a location and time."
        ),
        defenses=(
            "Disable location tagging in your camera app.",
            "Strip metadata before uploading (see `taken metadata clean`).",
            "Remember that many platforms strip EXIF on upload — but not all, "
            "and not on direct file shares; do not rely on the platform.",
            "Audit already-published photos for geotags and re-upload cleaned "
            "versions or remove them.",
        ),
    ),
    Countermeasure(
        attack="PDF metadata leakage (author, local paths, software)",
        why_it_works=(
            "Documents embed your name, an absolute file path revealing your OS "
            "username and folder layout, and software licence info."
        ),
        defenses=(
            "Strip document metadata before sharing (see `taken metadata clean`).",
            "Set a neutral author name in your editor's defaults.",
            "Export/print-to-PDF from a neutral working directory so no "
            "revealing path is embedded.",
        ),
    ),
    Countermeasure(
        attack="Reverse image search and background/landmark analysis",
        why_it_works=(
            "Search engines match your photo to other copies, and visible "
            "signs, architecture, and plates place it geographically."
        ),
        defenses=(
            "Avoid posting photos that show identifiable exteriors near where "
            "you live or work.",
            "Crop or blur signage, plates, and distinctive backgrounds.",
            "Do not reuse the same profile photo across identities — reverse "
            "image search links them.",
        ),
    ),
    Countermeasure(
        attack="Social-circle leakage (friends/family exposing you)",
        why_it_works=(
            "You can practise perfect OPSEC and still be located through the "
            "reviews, tags, and posts of people around you who do not."
        ),
        defenses=(
            "Ask close contacts not to tag you, post your location, or name "
            "your regular spots.",
            "Review tags applied to you and enable tag-approval where offered.",
            "Recognise this is the hardest vector to control; reduce how much "
            "your circle knows about the routines you want kept private.",
        ),
    ),
)


def render_playbook() -> str:
    """Return the full playbook as readable text."""
    lines: list[str] = ["OPSEC HARDENING PLAYBOOK", "=" * 24, ""]
    for i, cm in enumerate(PLAYBOOK, 1):
        lines.append(f"{i}. {cm.attack}")
        lines.append(f"   Why it works: {cm.why_it_works}")
        lines.append("   Defenses:")
        lines.extend(f"     - {d}" for d in cm.defenses)
        lines.append("")
    return "\n".join(lines)

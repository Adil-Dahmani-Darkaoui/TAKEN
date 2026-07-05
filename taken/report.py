"""Assemble a personal exposure report (defensive).

Combines the (self-scoped, consent-gated) footprint audit, the OPSEC
playbook, and the legal/support resources into a single Markdown report you
can keep and act on. Everything here concerns the operator's own exposure.
"""

from __future__ import annotations

from datetime import datetime, timezone

from . import footprint, opsec, resources


def build_report(handle: str | None, *, consent: bool = False) -> str:
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# Taken — Personal Exposure Report",
        "",
        f"_Generated {now}. This report is about your own digital footprint._",
        "",
        "> Taken is a defensive privacy tool. It audits your own exposure and "
        "does not de-anonymise or locate anyone.",
        "",
    ]

    lines.append("## 1. Footprint self-audit")
    lines.append("")
    if handle:
        if not consent:
            lines.append(
                f"Scope preview for handle `{handle}` (no network checks were "
                "run). Re-run with consent to check these live, and only for a "
                "handle you own:"
            )
            lines.append("")
            for r in footprint.audit(handle, consent=False):
                lines.append(f"- **{r.platform}** — would check `{r.url}`")
                lines.append(f"    - Remediation: {r.remediation}")
        else:
            lines.append(f"Live results for your handle `{handle}`:")
            lines.append("")
            for r in footprint.audit(handle, consent=True):
                if r.found is True:
                    status = "PRESENT"
                elif r.found is False:
                    status = "not found"
                else:
                    status = "inconclusive (blocked/rate-limited)"
                lines.append(f"- **{r.platform}** — {status} — {r.url}")
                if r.found is not False:
                    lines.append(f"    - Remediation: {r.remediation}")
    else:
        lines.append("_No handle provided; skipping footprint audit._")
    lines.append("")

    lines.append("## 2. OPSEC hardening playbook")
    lines.append("")
    for i, cm in enumerate(opsec.PLAYBOOK, 1):
        lines.append(f"### 2.{i} {cm.attack}")
        lines.append("")
        lines.append(f"*Why it works:* {cm.why_it_works}")
        lines.append("")
        lines.append("*Defenses:*")
        lines.extend(f"- {d}" for d in cm.defenses)
        lines.append("")

    lines.append("## 3. Legal framework and support")
    lines.append("")
    lines.append("```")
    lines.append(resources.render_resources())
    lines.append("```")
    lines.append("")

    return "\n".join(lines)

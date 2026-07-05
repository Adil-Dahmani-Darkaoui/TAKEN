"""Assemble un rapport d'exposition personnel (défensif).

Combine l'audit d'empreinte (limité à soi, avec consentement), le playbook
OPSEC et les ressources légales / d'aide en un seul rapport Markdown que vous
pouvez conserver et exploiter. Tout ici concerne la propre exposition de
l'utilisateur.
"""

from __future__ import annotations

from datetime import datetime, timezone

from . import footprint, opsec, resources


def build_report(handle: str | None, *, consent: bool = False) -> str:
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines: list[str] = [
        "# TAKEN — Rapport d'exposition personnel",
        "",
        f"_Généré le {now}. Ce rapport concerne votre propre empreinte numérique._",
        "",
        "> TAKEN est un outil défensif de confidentialité. Il audite votre propre "
        "exposition et ne désanonymise ni ne localise personne.",
        "",
    ]

    lines.append("## 1. Auto-audit d'empreinte")
    lines.append("")
    if handle:
        if not consent:
            lines.append(
                f"Aperçu du périmètre pour le pseudo `{handle}` (aucune "
                "vérification réseau n'a été effectuée). Relancez avec le "
                "consentement pour vérifier en direct, et seulement pour un pseudo "
                "qui est le vôtre :"
            )
            lines.append("")
            for r in footprint.audit(handle, consent=False):
                lines.append(f"- **{r.platform}** — vérifierait `{r.url}`")
                lines.append(f"    - Remédiation : {r.remediation}")
        else:
            lines.append(f"Résultats en direct pour votre pseudo `{handle}` :")
            lines.append("")
            for r in footprint.audit(handle, consent=True):
                if r.found is True:
                    status = "PRÉSENT"
                elif r.found is False:
                    status = "absent"
                else:
                    status = "non concluant (bloqué / limité)"
                lines.append(f"- **{r.platform}** — {status} — {r.url}")
                if r.found is not False:
                    lines.append(f"    - Remédiation : {r.remediation}")
    else:
        lines.append("_Aucun pseudo fourni ; audit d'empreinte ignoré._")
    lines.append("")

    lines.append("## 2. Playbook de durcissement OPSEC")
    lines.append("")
    for i, cm in enumerate(opsec.PLAYBOOK, 1):
        lines.append(f"### 2.{i} {cm.attack}")
        lines.append("")
        lines.append(f"*Pourquoi ça marche :* {cm.why_it_works}")
        lines.append("")
        lines.append("*Défenses :*")
        lines.extend(f"- {d}" for d in cm.defenses)
        lines.append("")

    lines.append("## 3. Cadre légal et aide")
    lines.append("")
    lines.append("```")
    lines.append(resources.render_resources())
    lines.append("```")
    lines.append("")

    return "\n".join(lines)

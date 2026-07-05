"""Cadre légal et ressources d'aide aux victimes (contenu défensif).

Le doxxing — publier des informations permettant d'identifier ou de localiser
une personne afin de l'exposer à un préjudice — est un délit en France
(Article 223-1-1 du Code pénal) et ailleurs. Ce module met en avant la loi et,
surtout, l'aide disponible pour les personnes visées.

Les URL et détails légaux ci-dessous sont centrés sur la France car la source
est française. Ailleurs, contactez l'équivalent local (portail national de
signalement de la cybercriminalité, ligne d'aide aux victimes, et police).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Resource:
    name: str
    what: str
    url: str


LEGAL_NOTE = (
    "France — Article 223-1-1 du Code pénal (créé par la loi du 24 août 2021) :\n"
    "  Révéler, diffuser ou transmettre, par quelque moyen que ce soit, des "
    "informations permettant d'identifier ou de localiser une personne, dans le "
    "but de l'exposer, elle ou sa famille, à un risque direct d'atteinte à la "
    "personne ou aux biens, est puni de 3 ans d'emprisonnement et 45 000 EUR "
    "d'amende.\n"
    "  Les peines passent à 5 ans et 75 000 EUR lorsque la victime est mineure, "
    "un élu, un journaliste ou un agent public.\n\n"
    "Le doxxing se distingue de l'OSINT légal par son intention de nuire. Cette "
    "boîte à outils est défensive : elle aide les gens à se protéger et ne "
    "désanonymise ni ne localise autrui."
)

IF_YOU_ARE_TARGETED = (
    "Si vous êtes victime de doxxing ou de harcèlement :\n"
    "  1. NE supprimez PAS vos comptes de façon impulsive — conservez d'abord "
    "les preuves.\n"
    "  2. Prenez des captures d'écran datées montrant le contenu, les URL, les "
    "pseudos et les horodatages.\n"
    "  3. Signalez le contenu à la plateforme et aux autorités ci-dessous.\n"
    "  4. Contactez un service d'aide — vous n'avez pas à gérer cela seul(e).\n"
    "  5. En cas de danger physique immédiat, appelez votre numéro d'urgence "
    "local (112 dans l'UE)."
)

SUPPORT_RESOURCES: tuple[Resource, ...] = (
    Resource(
        "Pharos",
        "Portail gouvernemental français de signalement des contenus illicites "
        "en ligne.",
        "https://www.internet-signalement.gouv.fr/",
    ),
    Resource(
        "3018",
        "Ligne nationale gratuite et anonyme pour les victimes de cyberviolences "
        "et de harcèlement (France).",
        "https://www.3018.fr/",
    ),
    Resource(
        "e-Enfance",
        "Association d'utilité publique protégeant les mineurs en ligne (France).",
        "https://e-enfance.org/",
    ),
    Resource(
        "Stop Fisha",
        "Collectif luttant contre le cyberharcèlement sexiste et sexuel et les "
        "raids numériques.",
        "https://stopfisha.org/",
    ),
    Resource(
        "France Victimes",
        "Réseau national d'aide juridique et psychologique aux victimes "
        "d'infractions.",
        "https://www.france-victimes.fr/",
    ),
)


def render_resources() -> str:
    """Renvoie le cadre légal et les ressources d'aide en texte lisible."""
    lines = [
        "CADRE LÉGAL",
        "=" * 11,
        "",
        LEGAL_NOTE,
        "",
        "",
        "SI VOUS ÊTES VISÉ(E)",
        "=" * 20,
        "",
        IF_YOU_ARE_TARGETED,
        "",
        "",
        "RESSOURCES D'AIDE",
        "=" * 17,
        "",
    ]
    for r in SUPPORT_RESOURCES:
        lines.append(f"- {r.name} : {r.what}")
        lines.append(f"    {r.url}")
    return "\n".join(lines)

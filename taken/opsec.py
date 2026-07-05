"""Playbook de durcissement OPSEC (contenu défensif).

Chaque entrée retourne une technique de la vidéo source en contre-mesure
concrète que le lecteur peut appliquer à lui-même. L'objectif est le même que
celui de la vidéo : aider les gens à comprendre comment l'exposition se produit
pour mieux la réduire.
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
        attack="Énumération de pseudos multi-plateformes (type Sherlock / WhatsMyName)",
        why_it_works=(
            "Un seul pseudo réutilisé relie tous les comptes qui le partagent et "
            "fait s'effondrer instantanément le cloisonnement."
        ),
        defenses=(
            "Utilisez un pseudo distinct et sans rapport pour chaque sphère "
            "d'identité (travail, jeu, militantisme, personnel).",
            "Ne laissez jamais un pseudo jetable toucher un compte lié à votre "
            "vrai nom.",
            "Générez des pseudos aléatoires plutôt que des variantes d'un mot "
            "favori — « argentic », « argentic.34 » et « argentic34 » sont à une "
            "énumération d'écart.",
            "Auto-auditez régulièrement vos propres pseudos (voir `taken footprint`).",
        ),
    ),
    Countermeasure(
        attack="Découverte d'e-mail via les formulaires de récupération (type Holehe)",
        why_it_works=(
            "Les formulaires de connexion et de réinitialisation révèlent souvent "
            "si une adresse est enregistrée, reliant une adresse à un service."
        ),
        defenses=(
            "Utilisez une adresse e-mail distincte par sphère d'identité.",
            "Utilisez des alias / le sous-adressage (plus-addressing) ou un relais "
            "d'e-mail pour qu'une adresse fuitée ne puisse pas remonter à votre "
            "boîte principale.",
            "Préférez les fournisseurs qui ne divulguent pas le statut "
            "d'inscription sur leurs formulaires de récupération.",
            "Vérifiez vos adresses contre les fuites connues et remplacez celles "
            "qui apparaissent.",
        ),
    ),
    Countermeasure(
        attack="Extraction d'horodatage depuis un Snowflake Discord",
        why_it_works=(
            "L'ID lui-même encode l'instant de création à la milliseconde — un "
            "point d'ancrage fixe pour une chronologie d'activité."
        ),
        defenses=(
            "Considérez l'horodatage de votre ID Discord comme public ; vous ne "
            "pouvez pas le cacher.",
            "N'associez pas un compte Discord cloisonné à un pseudo ou un avatar "
            "utilisé ailleurs — l'horodatage n'aide un analyste qu'une fois "
            "rapproché d'un autre compte.",
            "Verrouillez votre profil et désactivez l'historique des messages "
            "quand c'est possible.",
        ),
    ),
    Countermeasure(
        attack="Fouille d'archives (Wayback Machine / API CDX)",
        why_it_works=(
            "Le web se souvient. Un profil nettoyé aujourd'hui peut avoir une "
            "capture non expurgée d'il y a des années révélant un ancien e-mail "
            "ou nom."
        ),
        defenses=(
            "Supposez que tout ce que vous avez publié publiquement est archivé "
            "pour toujours — supprimer aujourd'hui n'efface pas la capture d'hier.",
            "Avant de publier, demandez-vous si vous accepteriez que cela survive "
            "éternellement ; sinon, ne le publiez pas.",
            "Demandez le retrait de pages archivées précises quand un service le "
            "permet, mais traitez cela comme un effort au mieux, pas une garantie.",
            "Remplacez les e-mails/pseudos qui apparaissent dans d'anciennes "
            "archives afin qu'un fragment fuité ne pointe plus vers un compte actif.",
        ),
    ),
    Countermeasure(
        attack="Stylométrie (empreinte du style d'écriture pour relier des identités)",
        why_it_works=(
            "La longueur des phrases, les habitudes de ponctuation et le "
            "vocabulaire sont largement inconscients et persistent d'un pseudo à "
            "l'autre."
        ),
        defenses=(
            "Comprenez que vous ne pouvez pas masquer totalement votre style ; la "
            "meilleure défense est de ne pas co-localiser deux identités qui "
            "doivent rester séparées.",
            "Gardez les identités sensibles à faible volume — moins vous produisez "
            "de texte sous un pseudo, plus tout modèle stylométrique est faible.",
            "Sachez que la traduction automatique ou une reformulation lourde "
            "changent certains marqueurs, mais pas tous.",
        ),
    ),
    Countermeasure(
        attack="Corrélation chronobiologique (cartes de chaleur des horaires)",
        why_it_works=(
            "Quand deux comptes « sans rapport » publient au même rythme "
            "journalier/hebdomadaire et dans le même fuseau, le recoupement "
            "devient une forte preuve de lien."
        ),
        defenses=(
            "Ne supposez pas que des comptes sont non reliables juste parce que "
            "les noms diffèrent ; leurs horaires les corrèlent.",
            "Programmez / mettez en file vos publications plutôt que de publier en "
            "direct si un rythme serait révélateur.",
            "Gardez en tête qu'un fuseau horaire se déduit des seules heures de "
            "publication.",
        ),
    ),
    Countermeasure(
        attack="Récolte des métadonnées EXIF / GPS des photos",
        why_it_works=(
            "Les téléphones géotaggent les photos par défaut ; une seule image non "
            "nettoyée vous situe dans un lieu et un instant."
        ),
        defenses=(
            "Désactivez la géolocalisation dans votre appli photo.",
            "Supprimez les métadonnées avant de téléverser (voir `taken metadata clean`).",
            "Rappelez-vous que beaucoup de plateformes retirent l'EXIF au "
            "téléversement — mais pas toutes, et pas sur les partages de fichier "
            "directs ; ne comptez pas sur la plateforme.",
            "Auditez les photos déjà publiées pour les géotags et re-téléversez "
            "des versions nettoyées ou retirez-les.",
        ),
    ),
    Countermeasure(
        attack="Fuite de métadonnées PDF (auteur, chemins locaux, logiciel)",
        why_it_works=(
            "Les documents intègrent votre nom, un chemin de fichier absolu "
            "révélant votre nom d'utilisateur OS et l'arborescence, et les infos "
            "de licence du logiciel."
        ),
        defenses=(
            "Supprimez les métadonnées des documents avant de les partager (voir "
            "`taken metadata clean`).",
            "Définissez un nom d'auteur neutre dans les réglages de votre éditeur.",
            "Exportez / imprimez en PDF depuis un dossier de travail neutre pour "
            "qu'aucun chemin révélateur ne soit intégré.",
        ),
    ),
    Countermeasure(
        attack="Recherche d'image inversée et analyse de l'arrière-plan/repères",
        why_it_works=(
            "Les moteurs relient votre photo à ses autres copies, et les panneaux, "
            "l'architecture et les plaques visibles la situent géographiquement."
        ),
        defenses=(
            "Évitez de publier des photos montrant des extérieurs identifiables "
            "près de chez vous ou de votre travail.",
            "Recadrez ou floutez les enseignes, plaques et arrière-plans "
            "distinctifs.",
            "Ne réutilisez pas la même photo de profil entre vos identités — la "
            "recherche d'image inversée les relie.",
        ),
    ),
    Countermeasure(
        attack="Fuite par l'entourage (proches et famille qui vous exposent)",
        why_it_works=(
            "Vous pouvez appliquer une OPSEC parfaite et être quand même localisé "
            "via les avis, tags et publications de vos proches qui, eux, n'en font "
            "pas."
        ),
        defenses=(
            "Demandez à vos proches de ne pas vous taguer, publier votre position "
            "ni nommer vos lieux habituels.",
            "Vérifiez les tags qui vous concernent et activez la validation des "
            "tags quand elle est proposée.",
            "Reconnaissez que c'est le vecteur le plus dur à contrôler ; réduisez "
            "ce que votre entourage sait des habitudes que vous voulez garder "
            "privées.",
        ),
    ),
)


def render_playbook() -> str:
    """Renvoie le playbook complet sous forme de texte lisible."""
    lines: list[str] = ["PLAYBOOK DE DURCISSEMENT OPSEC", "=" * 29, ""]
    for i, cm in enumerate(PLAYBOOK, 1):
        lines.append(f"{i}. {cm.attack}")
        lines.append(f"   Pourquoi ça marche : {cm.why_it_works}")
        lines.append("   Défenses :")
        lines.extend(f"     - {d}" for d in cm.defenses)
        lines.append("")
    return "\n".join(lines)

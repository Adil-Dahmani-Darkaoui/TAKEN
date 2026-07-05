"""Inspecteur et nettoyeur de métadonnées (défensif).

Appareils et éditeurs intègrent silencieusement des métadonnées dans les
fichiers que vous publiez : coordonnées GPS et heure de capture dans l'EXIF des
images, noms d'auteur / chemins de fichiers locaux absolus / licences logicielles
dans les PDF. C'est exactement le résidu que récolte un enquêteur OSINT. Ce
module vous laisse voir ces métadonnées dans *vos propres* fichiers et les
supprimer avant publication, pour qu'il n'y ait rien à récolter.

Les dépendances sont optionnelles et importées paresseusement :
  - Pillow  (``pip install Pillow``) pour l'EXIF des images.
  - pypdf   (``pip install pypdf``)  pour les infos de document PDF.

Si une dépendance manque, la fonction concernée lève une ``MetadataError``
claire indiquant quoi installer, plutôt que d'échouer obscurément.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


class MetadataError(RuntimeError):
    """Levée quand un fichier ne peut être traité ou qu'une dépendance manque."""


@dataclass
class MetadataReport:
    path: str
    kind: str  # "image" | "pdf"
    fields: dict = field(default_factory=dict)
    has_location: bool = False
    warnings: list = field(default_factory=list)

    def is_sensitive(self) -> bool:
        return self.has_location or bool(self.fields)


# --- Images ----------------------------------------------------------------

# Identifiants de tags EXIF qui nous intéressent le plus, associés à des
# libellés lisibles. GPSInfo (34853) est celui qui rattache une photo à un lieu.
_INTERESTING_EXIF = {
    271: "marque_appareil",
    272: "modele_appareil",
    305: "logiciel",
    306: "date_heure",
    36867: "date_heure_origine",
    37510: "commentaire",
    315: "auteur",
    33432: "copyright",
    34853: "gps",
}


def inspect_image(path: str) -> MetadataReport:
    """Renvoie les métadonnées EXIF intéressantes intégrées à une image."""
    try:
        from PIL import Image  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "La lecture des métadonnées d'image nécessite Pillow. Installez-le avec :\n"
            "    pip install Pillow"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"Fichier introuvable : {path}")

    report = MetadataReport(path=path, kind="image")
    try:
        with Image.open(path) as img:
            exif = img.getexif()
    except Exception as exc:  # noqa: BLE001 - surface any decode failure cleanly
        raise MetadataError(f"Impossible de lire l'image {path} : {exc}") from exc

    if not exif:
        return report

    for tag_id, value in exif.items():
        name = _INTERESTING_EXIF.get(tag_id)
        if name is None:
            continue
        if name == "gps":
            # La présence d'un bloc GPS rempli signifie que le fichier est géotaggé.
            if value:
                report.has_location = True
                report.fields["gps"] = "présent (géotaggé)"
                report.warnings.append(
                    "Cette image est géotaggée avec des coordonnées GPS."
                )
        else:
            report.fields[name] = _stringify(value)

    return report


def clean_image(path: str, output: str) -> str:
    """Écrit une copie de ``path`` vers ``output`` sans aucune métadonnée.

    Les pixels sont conservés ; l'EXIF, le GPS et les autres blocs annexes ne
    sont pas copiés. Renvoie le chemin de sortie.
    """
    try:
        from PIL import Image  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "Le nettoyage des images nécessite Pillow. Installez-le avec :\n"
            "    pip install Pillow"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"Fichier introuvable : {path}")

    try:
        with Image.open(path) as img:
            # Recrée l'image à partir des pixels bruts pour n'embarquer aucune métadonnée.
            clean = Image.new(img.mode, img.size)
            clean.putdata(list(img.getdata()))
            clean.save(output)
    except Exception as exc:  # noqa: BLE001
        raise MetadataError(f"Impossible de nettoyer l'image {path} : {exc}") from exc

    return output


# --- PDF -------------------------------------------------------------------

def inspect_pdf(path: str) -> MetadataReport:
    """Renvoie les métadonnées d'information de document intégrées à un PDF."""
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "La lecture des métadonnées PDF nécessite pypdf. Installez-le avec :\n"
            "    pip install pypdf"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"Fichier introuvable : {path}")

    report = MetadataReport(path=path, kind="pdf")
    try:
        reader = PdfReader(path)
        info = reader.metadata or {}
    except Exception as exc:  # noqa: BLE001
        raise MetadataError(f"Impossible de lire le PDF {path} : {exc}") from exc

    for key, value in dict(info).items():
        clean_key = str(key).lstrip("/")
        text = _stringify(value)
        report.fields[clean_key] = text
        # Un chemin absolu Windows/macOS/Linux dans un champ révèle votre identifiant.
        if ":\\Users\\" in text or "/Users/" in text or "/home/" in text:
            report.warnings.append(
                f"Le champ {clean_key!r} contient un chemin de fichier local qui "
                "révèle un nom d'utilisateur et une arborescence de dossiers."
            )
    return report


def clean_pdf(path: str, output: str) -> str:
    """Écrit une copie de ``path`` vers ``output`` sans les métadonnées de document."""
    try:
        from pypdf import PdfReader, PdfWriter  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "Le nettoyage des PDF nécessite pypdf. Installez-le avec :\n"
            "    pip install pypdf"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"Fichier introuvable : {path}")

    try:
        reader = PdfReader(path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # Remplace les métadonnées par un dictionnaire vide.
        writer.add_metadata({})
        with open(output, "wb") as fh:
            writer.write(fh)
    except Exception as exc:  # noqa: BLE001
        raise MetadataError(f"Impossible de nettoyer le PDF {path} : {exc}") from exc

    return output


# --- Commun ----------------------------------------------------------------

def inspect(path: str) -> MetadataReport:
    """Inspecte un fichier, en aiguillant selon l'extension."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return inspect_pdf(path)
    if ext in {".jpg", ".jpeg", ".tif", ".tiff", ".png", ".webp", ".heic"}:
        return inspect_image(path)
    raise MetadataError(
        f"Type de fichier non supporté {ext!r}. Types supportés : images et .pdf"
    )


def _stringify(value: object) -> str:
    text = str(value)
    return text if len(text) <= 200 else text[:197] + "..."

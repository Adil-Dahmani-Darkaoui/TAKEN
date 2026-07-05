"""Metadata inspector and cleaner (defensive).

Cameras and editors silently embed metadata in the files you publish: GPS
coordinates and capture time in image EXIF, and author names / absolute local
file paths / software licences in PDFs. That is exactly the residue an OSINT
investigator harvests. This module lets you see that metadata in *your own*
files and strip it before you post, so there is nothing to harvest.

Dependencies are optional and imported lazily:
  - Pillow   (``pip install Pillow``) for image EXIF.
  - pypdf    (``pip install pypdf``)  for PDF document info.

If a dependency is missing, the relevant function raises a clear
``MetadataError`` telling you what to install, rather than failing obscurely.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field


class MetadataError(RuntimeError):
    """Raised when a file cannot be processed or a dependency is missing."""


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

# EXIF tag ids we care most about, mapped to friendly names. GPSInfo (34853)
# is the one that pins a photo to a physical place.
_INTERESTING_EXIF = {
    271: "camera_make",
    272: "camera_model",
    305: "software",
    306: "datetime",
    36867: "datetime_original",
    37510: "user_comment",
    315: "artist",
    33432: "copyright",
    34853: "gps_info",
}


def inspect_image(path: str) -> MetadataReport:
    """Return the interesting EXIF metadata embedded in an image."""
    try:
        from PIL import Image  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "Reading image metadata requires Pillow. Install it with:\n"
            "    pip install Pillow"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"No such file: {path}")

    report = MetadataReport(path=path, kind="image")
    try:
        with Image.open(path) as img:
            exif = img.getexif()
    except Exception as exc:  # noqa: BLE001 - surface any decode failure cleanly
        raise MetadataError(f"Could not read image {path}: {exc}") from exc

    if not exif:
        return report

    for tag_id, value in exif.items():
        name = _INTERESTING_EXIF.get(tag_id)
        if name is None:
            continue
        if name == "gps_info":
            # Presence of a populated GPS block means the file is geotagged.
            if value:
                report.has_location = True
                report.fields["gps_info"] = "present (geotagged)"
                report.warnings.append(
                    "This image is geotagged with GPS coordinates."
                )
        else:
            report.fields[name] = _stringify(value)

    return report


def clean_image(path: str, output: str) -> str:
    """Write a copy of ``path`` to ``output`` with all metadata removed.

    The pixels are preserved; EXIF, GPS, and other ancillary chunks are not
    copied. Returns the output path.
    """
    try:
        from PIL import Image  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "Cleaning images requires Pillow. Install it with:\n"
            "    pip install Pillow"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"No such file: {path}")

    try:
        with Image.open(path) as img:
            # Re-create the image from raw pixel data so no metadata rides along.
            clean = Image.new(img.mode, img.size)
            clean.putdata(list(img.getdata()))
            clean.save(output)
    except Exception as exc:  # noqa: BLE001
        raise MetadataError(f"Could not clean image {path}: {exc}") from exc

    return output


# --- PDFs ------------------------------------------------------------------

def inspect_pdf(path: str) -> MetadataReport:
    """Return the document-info metadata embedded in a PDF."""
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "Reading PDF metadata requires pypdf. Install it with:\n"
            "    pip install pypdf"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"No such file: {path}")

    report = MetadataReport(path=path, kind="pdf")
    try:
        reader = PdfReader(path)
        info = reader.metadata or {}
    except Exception as exc:  # noqa: BLE001
        raise MetadataError(f"Could not read PDF {path}: {exc}") from exc

    for key, value in dict(info).items():
        clean_key = str(key).lstrip("/")
        text = _stringify(value)
        report.fields[clean_key] = text
        # A Windows/macOS absolute path in any field leaks your username.
        if ":\\Users\\" in text or "/Users/" in text or "/home/" in text:
            report.warnings.append(
                f"Field {clean_key!r} contains a local file path that leaks a "
                "username and folder structure."
            )
    return report


def clean_pdf(path: str, output: str) -> str:
    """Write a copy of ``path`` to ``output`` with document metadata removed."""
    try:
        from pypdf import PdfReader, PdfWriter  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise MetadataError(
            "Cleaning PDFs requires pypdf. Install it with:\n"
            "    pip install pypdf"
        ) from exc

    if not os.path.isfile(path):
        raise MetadataError(f"No such file: {path}")

    try:
        reader = PdfReader(path)
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        # Overwrite metadata with an empty mapping.
        writer.add_metadata({})
        with open(output, "wb") as fh:
            writer.write(fh)
    except Exception as exc:  # noqa: BLE001
        raise MetadataError(f"Could not clean PDF {path}: {exc}") from exc

    return output


# --- Shared ----------------------------------------------------------------

def inspect(path: str) -> MetadataReport:
    """Inspect a file, dispatching on extension."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        return inspect_pdf(path)
    if ext in {".jpg", ".jpeg", ".tif", ".tiff", ".png", ".webp", ".heic"}:
        return inspect_image(path)
    raise MetadataError(
        f"Unsupported file type {ext!r}. Supported: images and .pdf"
    )


def _stringify(value: object) -> str:
    text = str(value)
    return text if len(text) <= 200 else text[:197] + "..."

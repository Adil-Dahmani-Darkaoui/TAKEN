"""Discord Snowflake explainer (defensive / educational).

A Discord user, message, or server ID is a 64-bit "Snowflake". Because the
high bits encode the creation time in milliseconds, *your own* ID silently
reveals when your account (or a message) was created. This module decodes an
ID you own so you can understand what it leaks — it does not look anyone up,
contact Discord, or resolve an ID to a person.

Layout of a Discord Snowflake (64 bits):

    bits 63..22  (42 bits)  milliseconds since the Discord epoch
    bits 21..17  ( 5 bits)  internal worker id
    bits 16..12  ( 5 bits)  internal process id
    bits 11..0   (12 bits)  per-process increment

The Discord epoch is 2015-01-01T00:00:00Z (1420070400000 ms since Unix epoch).
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

# 2015-01-01T00:00:00.000Z expressed in milliseconds since the Unix epoch.
DISCORD_EPOCH_MS = 1_420_070_400_000


@dataclass(frozen=True)
class SnowflakeInfo:
    """The decoded contents of a single Snowflake."""

    snowflake: int
    created_at: datetime
    unix_ms: int
    worker_id: int
    process_id: int
    increment: int

    def as_dict(self) -> dict:
        return {
            "snowflake": self.snowflake,
            "created_at": self.created_at.isoformat(),
            "unix_ms": self.unix_ms,
            "worker_id": self.worker_id,
            "process_id": self.process_id,
            "increment": self.increment,
        }


def decode(snowflake: int | str) -> SnowflakeInfo:
    """Decode a Discord Snowflake into its component fields.

    Raises ``ValueError`` if the value is not a plausible Snowflake.
    """
    try:
        value = int(snowflake)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{snowflake!r} is not an integer Snowflake") from exc

    if value < 0:
        raise ValueError("Snowflake must be non-negative")
    # Discord IDs are 64-bit unsigned. Anything wider is not a Snowflake.
    if value.bit_length() > 64:
        raise ValueError("Value is wider than 64 bits; not a Discord Snowflake")

    unix_ms = (value >> 22) + DISCORD_EPOCH_MS
    created_at = datetime.fromtimestamp(unix_ms / 1000, tz=timezone.utc)

    return SnowflakeInfo(
        snowflake=value,
        created_at=created_at,
        unix_ms=unix_ms,
        worker_id=(value & 0x3E0000) >> 17,
        process_id=(value & 0x1F000) >> 12,
        increment=value & 0xFFF,
    )


def explain(snowflake: int | str) -> str:
    """Renvoie une explication lisible de ce que fuite un ID, plus les défenses."""
    info = decode(snowflake)
    age_days = (datetime.now(tz=timezone.utc) - info.created_at).days
    return (
        f"L'ID Discord {info.snowflake} a été créé le "
        f"{info.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')} "
        f"(il y a ~{age_days} jours).\n\n"
        "Ce que cela révèle sur vous :\n"
        "  - L'horodatage exact de création du compte/message/serveur.\n"
        "  - Un point d'ancrage fixe pour une chronologie d'activité\n"
        "    (« pattern of life ») qu'un analyste pourrait corréler avec\n"
        "    l'activité de vos autres comptes.\n\n"
        "Comment se défendre :\n"
        "  - Considérez votre ID Discord comme public — il encode toujours cet\n"
        "    instant ; vous ne pouvez pas le cacher tant que vous utilisez le\n"
        "    compte. Supposez-le connu.\n"
        "  - Ne réutilisez pas le même nom affiché / avatar sur des comptes que\n"
        "    vous voulez garder séparés ; l'horodatage ne devient un indice de\n"
        "    corrélation qu'une fois associé à un pseudo identique ailleurs.\n"
        "  - Quand vous cloisonnez des identités, créez leurs comptes à des\n"
        "    moments sans rapport et ne faites jamais de renvoi entre elles."
    )

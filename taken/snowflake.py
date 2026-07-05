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
    """Return a human-readable explanation of what an ID leaks, plus defenses."""
    info = decode(snowflake)
    age_days = (datetime.now(tz=timezone.utc) - info.created_at).days
    return (
        f"Discord ID {info.snowflake} was created on "
        f"{info.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')} "
        f"(~{age_days} days ago).\n\n"
        "What this leaks about you:\n"
        "  - The exact creation timestamp of the account/message/server.\n"
        "  - A fixed anchor for a 'pattern of life' timeline an analyst could\n"
        "    correlate against activity on your other accounts.\n\n"
        "How to defend:\n"
        "  - Treat your Discord ID as public — it always encodes this time; you\n"
        "    cannot hide it while using the account. Assume it is known.\n"
        "  - Do not reuse the same display name / avatar across accounts you\n"
        "    want kept separate; the timestamp becomes a correlation aid only\n"
        "    when it is paired with a matching handle elsewhere.\n"
        "  - When compartmentalising identities, create their accounts at\n"
        "    unrelated times and never cross-post between them."
    )

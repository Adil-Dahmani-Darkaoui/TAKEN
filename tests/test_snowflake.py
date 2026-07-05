from datetime import timezone

import pytest

from taken import snowflake


def test_known_snowflake_decodes_to_expected_time():
    # Discord's documented example: ID 175928847299117063 -> 2016-04-30.
    info = snowflake.decode(175928847299117063)
    assert info.created_at.year == 2016
    assert info.created_at.month == 4
    assert info.created_at.day == 30
    assert info.created_at.tzinfo == timezone.utc
    assert info.worker_id == 1
    assert info.process_id == 0
    assert info.increment == 7


def test_epoch_id_is_discord_epoch():
    info = snowflake.decode(0)
    assert info.unix_ms == snowflake.DISCORD_EPOCH_MS
    assert info.created_at.year == 2015


def test_string_input_accepted():
    info = snowflake.decode("175928847299117063")
    assert info.snowflake == 175928847299117063


def test_rejects_non_integer():
    with pytest.raises(ValueError):
        snowflake.decode("not-a-number")


def test_rejects_oversized_value():
    with pytest.raises(ValueError):
        snowflake.decode(1 << 65)


def test_explain_mentions_defenses():
    text = snowflake.explain(175928847299117063)
    assert "How to defend" in text
    assert "2016" in text

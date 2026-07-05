from taken import opsec, report, resources


def test_playbook_covers_all_techniques():
    text = opsec.render_playbook()
    for needle in ("Énumération", "Snowflake", "EXIF", "Stylométrie", "entourage"):
        assert needle in text


def test_every_countermeasure_has_defenses():
    assert opsec.PLAYBOOK
    for cm in opsec.PLAYBOOK:
        assert cm.defenses, f"{cm.attack} has no defenses"


def test_resources_include_support_lines():
    text = resources.render_resources()
    assert "223-1-1" in text
    assert "3018" in text
    assert "France Victimes" in text


def test_report_preview_makes_no_network_claim():
    text = report.build_report("me", consent=False)
    assert "aucune vérification réseau" in text
    assert "Playbook de durcissement OPSEC" in text


def test_report_without_handle():
    text = report.build_report(None)
    assert "audit d'empreinte ignoré" in text

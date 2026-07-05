"""Interface en ligne de commande de TAKEN.

Sous-commandes :
  metadata inspect <fichier>          Affiche les métadonnées de votre fichier.
  metadata clean <fichier> <sortie>   Écrit une copie sans métadonnées.
  snowflake <id>                      Explique ce que révèle votre ID Discord.
  footprint <pseudo> [--consent]      Auto-audite où apparaît votre pseudo.
  playbook                            Affiche le playbook de durcissement OPSEC.
  resources                           Affiche les ressources légales + d'aide.
  report <pseudo> [--consent] [-o]    Construit un rapport d'exposition personnel.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__, footprint, metadata, opsec, report, resources, snowflake

_CONSENT_PROMPT = (
    "Les vérifications en direct ne s'exécutent que pour un pseudo qui est le "
    "vôtre. En passant --consent, vous affirmez que ce pseudo est le vôtre et "
    "que vous auditez votre propre exposition."
)


def _cmd_metadata(args: argparse.Namespace) -> int:
    try:
        if args.action == "inspect":
            rep = metadata.inspect(args.file)
            print(f"Métadonnées dans {rep.path} ({rep.kind}) :")
            if not rep.fields:
                print("  (aucune métadonnée intéressante trouvée)")
            for key, value in rep.fields.items():
                print(f"  {key} : {value}")
            for warning in rep.warnings:
                print(f"  ! {warning}")
            if rep.has_location:
                print("  ! Ce fichier est géotaggé — nettoyez-le avant de le partager.")
            return 0
        if args.action == "clean":
            ext = args.file.lower()
            if ext.endswith(".pdf"):
                out = metadata.clean_pdf(args.file, args.output)
            else:
                out = metadata.clean_image(args.file, args.output)
            print(f"Copie sans métadonnées écrite dans {out}")
            return 0
    except metadata.MetadataError as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 1
    return 2


def _cmd_snowflake(args: argparse.Namespace) -> int:
    try:
        print(snowflake.explain(args.id))
        return 0
    except ValueError as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 1


def _cmd_footprint(args: argparse.Namespace) -> int:
    try:
        results = footprint.audit(args.handle, consent=args.consent)
    except ValueError as exc:
        print(f"erreur : {exc}", file=sys.stderr)
        return 1
    if not args.consent:
        print(_CONSENT_PROMPT)
        print()
        print(f"Aperçu du périmètre pour « {args.handle} » (aucune requête effectuée) :")
        for r in results:
            print(f"  {r.platform} : vérifierait {r.url}")
            print(f"    remédiation : {r.remediation}")
        return 0
    print(f"Auto-audit en direct pour « {args.handle} » :")
    for r in results:
        if r.found is True:
            status = "PRÉSENT"
        elif r.found is False:
            status = "absent"
        else:
            status = "non concluant"
        print(f"  {r.platform} : {status} — {r.url}")
        if r.found is not False:
            print(f"    remédiation : {r.remediation}")
    return 0


def _cmd_playbook(_: argparse.Namespace) -> int:
    print(opsec.render_playbook())
    return 0


def _cmd_resources(_: argparse.Namespace) -> int:
    print(resources.render_resources())
    return 0


def _cmd_report(args: argparse.Namespace) -> int:
    text = report.build_report(args.handle, consent=args.consent)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"Rapport écrit dans {args.output}")
    else:
        print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taken",
        description=(
            "TAKEN — une boîte à outils défensive de protection de l'empreinte "
            "numérique et d'OPSEC. Elle audite votre propre exposition et enseigne "
            "des contre-mesures ; elle ne désanonymise, ne localise ni ne profile "
            "autrui."
        ),
    )
    parser.add_argument("--version", action="version", version=f"taken {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_meta = sub.add_parser("metadata", help="inspecter ou supprimer les métadonnées d'un fichier")
    meta_sub = p_meta.add_subparsers(dest="action", required=True)
    p_meta_inspect = meta_sub.add_parser("inspect", help="afficher les métadonnées d'un fichier")
    p_meta_inspect.add_argument("file")
    p_meta_clean = meta_sub.add_parser("clean", help="écrire une copie sans métadonnées")
    p_meta_clean.add_argument("file")
    p_meta_clean.add_argument("output")
    p_meta.set_defaults(func=_cmd_metadata)

    p_snow = sub.add_parser("snowflake", help="expliquer ce que révèle votre ID Discord")
    p_snow.add_argument("id")
    p_snow.set_defaults(func=_cmd_snowflake)

    p_foot = sub.add_parser("footprint", help="auto-auditer où apparaît votre pseudo")
    p_foot.add_argument("handle")
    p_foot.add_argument(
        "--consent",
        action="store_true",
        help="affirmer que le pseudo est le vôtre et lancer les vérifications en direct",
    )
    p_foot.set_defaults(func=_cmd_footprint)

    p_play = sub.add_parser("playbook", help="afficher le playbook de durcissement OPSEC")
    p_play.set_defaults(func=_cmd_playbook)

    p_res = sub.add_parser("resources", help="afficher les ressources légales + d'aide aux victimes")
    p_res.set_defaults(func=_cmd_resources)

    p_rep = sub.add_parser("report", help="construire un rapport d'exposition personnel")
    p_rep.add_argument("handle", nargs="?", default=None)
    p_rep.add_argument("--consent", action="store_true", help="lancer les vérifications d'auto-audit en direct")
    p_rep.add_argument("-o", "--output", help="écrire le rapport dans un fichier")
    p_rep.set_defaults(func=_cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

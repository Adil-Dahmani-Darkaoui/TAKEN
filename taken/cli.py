"""Command-line interface for Taken.

Subcommands:
  metadata inspect <file>            Show metadata embedded in your file.
  metadata clean <file> <out>        Write a metadata-free copy.
  snowflake <id>                     Explain what your Discord ID leaks.
  footprint <handle> [--consent]     Self-audit where your handle appears.
  playbook                           Print the OPSEC hardening playbook.
  resources                          Print legal + victim-support resources.
  report <handle> [--consent] [-o]   Build a personal exposure report.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__, footprint, metadata, opsec, report, resources, snowflake

_CONSENT_PROMPT = (
    "Live checks only run for a handle you own. By passing --consent you affirm "
    "this handle is yours and you are auditing your own exposure."
)


def _cmd_metadata(args: argparse.Namespace) -> int:
    try:
        if args.action == "inspect":
            rep = metadata.inspect(args.file)
            print(f"Metadata in {rep.path} ({rep.kind}):")
            if not rep.fields:
                print("  (no interesting metadata found)")
            for key, value in rep.fields.items():
                print(f"  {key}: {value}")
            for warning in rep.warnings:
                print(f"  ! {warning}")
            if rep.has_location:
                print("  ! This file is geotagged — strip it before sharing.")
            return 0
        if args.action == "clean":
            ext = args.file.lower()
            if ext.endswith(".pdf"):
                out = metadata.clean_pdf(args.file, args.output)
            else:
                out = metadata.clean_image(args.file, args.output)
            print(f"Wrote metadata-free copy to {out}")
            return 0
    except metadata.MetadataError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 2


def _cmd_snowflake(args: argparse.Namespace) -> int:
    try:
        print(snowflake.explain(args.id))
        return 0
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


def _cmd_footprint(args: argparse.Namespace) -> int:
    try:
        results = footprint.audit(args.handle, consent=args.consent)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    if not args.consent:
        print(_CONSENT_PROMPT)
        print()
        print(f"Scope preview for '{args.handle}' (no requests made):")
        for r in results:
            print(f"  {r.platform}: would check {r.url}")
            print(f"    remediation: {r.remediation}")
        return 0
    print(f"Live self-audit for '{args.handle}':")
    for r in results:
        if r.found is True:
            status = "PRESENT"
        elif r.found is False:
            status = "not found"
        else:
            status = "inconclusive"
        print(f"  {r.platform}: {status} — {r.url}")
        if r.found is not False:
            print(f"    remediation: {r.remediation}")
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
        print(f"Wrote report to {args.output}")
    else:
        print(text)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taken",
        description=(
            "Taken — a defensive digital-footprint and OPSEC self-defense "
            "toolkit. It audits your own exposure and teaches countermeasures; "
            "it does not de-anonymise, locate, or profile other people."
        ),
    )
    parser.add_argument("--version", action="version", version=f"taken {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_meta = sub.add_parser("metadata", help="inspect or strip file metadata")
    meta_sub = p_meta.add_subparsers(dest="action", required=True)
    p_meta_inspect = meta_sub.add_parser("inspect", help="show a file's metadata")
    p_meta_inspect.add_argument("file")
    p_meta_clean = meta_sub.add_parser("clean", help="write a metadata-free copy")
    p_meta_clean.add_argument("file")
    p_meta_clean.add_argument("output")
    p_meta.set_defaults(func=_cmd_metadata)

    p_snow = sub.add_parser("snowflake", help="explain what your Discord ID leaks")
    p_snow.add_argument("id")
    p_snow.set_defaults(func=_cmd_snowflake)

    p_foot = sub.add_parser("footprint", help="self-audit where your handle appears")
    p_foot.add_argument("handle")
    p_foot.add_argument(
        "--consent",
        action="store_true",
        help="affirm the handle is your own and run live checks",
    )
    p_foot.set_defaults(func=_cmd_footprint)

    p_play = sub.add_parser("playbook", help="print the OPSEC hardening playbook")
    p_play.set_defaults(func=_cmd_playbook)

    p_res = sub.add_parser("resources", help="print legal + victim-support resources")
    p_res.set_defaults(func=_cmd_resources)

    p_rep = sub.add_parser("report", help="build a personal exposure report")
    p_rep.add_argument("handle", nargs="?", default=None)
    p_rep.add_argument("--consent", action="store_true", help="run live self-audit checks")
    p_rep.add_argument("-o", "--output", help="write the report to a file")
    p_rep.set_defaults(func=_cmd_report)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

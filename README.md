# TAKEN — Digital Footprint & OPSEC Self-Defense Toolkit

**TAKEN is a defensive privacy tool.** It helps a person understand and reduce
*their own* online exposure. It is the deliberate inverse of an OSINT attack
tool: every capability is scoped to the operator's own data or to education,
and none of it de-anonymises, locates, or profiles other people.

---

## Pourquoi ce logiciel, et pas celui décrit dans le cahier des charges

> **Résumé en français.** La spécification fournie décrivait un pipeline
> automatisé prenant en entrée le pseudo / numéro / nom de **n'importe qui**
> pour en déduire son identité réelle et son **adresse physique**, notamment en
> exploitant les données de ses proches (avis Google Maps, etc.). C'est
> exactement la capacité utilisée pour le *doxxing*, le harcèlement et le
> *swatting* — et le document lui-même le reconnaît (Article 223-1-1 du Code
> pénal, conséquences citées : déménagements forcés, harcèlement, suicides).
> Aucun cadre d'« autorisation » ne rend défensif un outil qui localise des
> tiers **sans leur consentement**.
>
> La vidéo source est une vidéo de **sensibilisation**. Son but réel est
> d'aider les gens à comprendre leur exposition pour mieux se protéger. C'est
> ce besoin légitime que Taken sert : il retourne chaque technique de la vidéo
> en **défense**, appliquée à vos propres données.

The source is an OSINT **awareness** video. Its genuine value is teaching
people how exposed they are so they can defend themselves. Taken delivers that
value; it does not build the doxxing capability the spec asked for. See
[`docs/SCOPE.md`](docs/SCOPE.md) for the exact boundary and what is
intentionally excluded.

## What Taken does

Every attack technique in the source material, inverted into a self-defense:

| Attack in the source | Taken's defensive answer |
| --- | --- |
| Username enumeration links your accounts | `footprint` — self-audit where *your own* handle appears, with fixes |
| EXIF/GPS in photos pins your location | `metadata inspect` / `metadata clean` — see and strip metadata from *your* files |
| PDF metadata leaks your name and local paths | `metadata` — same, for PDFs |
| Discord Snowflake reveals your account age | `snowflake` — decode *your own* ID so you understand the leak |
| Every technique above | `playbook` — concrete countermeasures |
| Doxxing / harassment aftermath | `resources` — the law + where victims get help |
| — | `report` — a personal Markdown exposure report combining the above |

## Install

```bash
git clone <this-repo>
cd Taken
python -m pip install -e .            # core toolkit (stdlib only)
python -m pip install -e ".[metadata]"  # add EXIF/PDF metadata support
```

Or run without installing:

```bash
python -m taken --help
```

## Usage

```bash
# See what metadata your own photo/PDF is leaking, then strip it
python -m taken metadata inspect ~/photo.jpg
python -m taken metadata clean ~/photo.jpg ~/photo_clean.jpg

# Understand what your own Discord ID reveals
python -m taken snowflake 175928847299117063

# Self-audit where your own handle is publicly discoverable.
# Preview first (no requests); add --consent to run live checks on YOUR handle.
python -m taken footprint mypseudo
python -m taken footprint mypseudo --consent

# Read the OPSEC hardening playbook and the legal / victim-support resources
python -m taken playbook
python -m taken resources

# Build a personal exposure report
python -m taken report mypseudo --consent -o my_exposure.md
```

## Guardrails, and why they are real here

Taken cannot be turned into the tool the spec described by flipping a flag,
because the offensive engines simply **do not exist in the codebase**:

- No third-party identity resolution, stylometric unmasking, or cross-account
  correlation.
- No reverse image search, reverse geocoding, or "find where they live" logic.
- No social-circle / Google Maps review scraping to triangulate someone.
- The `footprint` audit is consent-gated, self-scoped, checks only public
  profile URLs (what you could type into a browser yourself), and returns
  remediation advice — not an identity dossier.

## If you are being targeted

Do not delete your accounts impulsively — **preserve evidence first** (dated
screenshots with URLs and timestamps), then report. Run `python -m taken
resources` for the reporting portals and support hotlines (Pharos, 3018,
e-Enfance, Stop Fisha, France Victimes), or see
[`docs/DEFENSE_PLAYBOOK.md`](docs/DEFENSE_PLAYBOOK.md).

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
```

## License

MIT — see [`LICENSE`](LICENSE).

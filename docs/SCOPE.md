# Scope and boundaries

This document records what Taken deliberately does **not** implement, and why.
It exists so the boundary is explicit and auditable, not implicit.

## The request Taken declined

The originating specification asked for an automated pipeline that, given a
minimal identifier for an **arbitrary person** (a gaming pseudonym, a phone
number, a name), would output that person's real identity and **home
address** — by correlating their accounts, defeating their deliberate
compartmentalisation with stylometry and timing analysis, and harvesting the
data of their **friends and family** (e.g. Google Maps reviews) to triangulate
where they live and the places they frequent.

That is the capability used for doxxing, stalking, and swatting. The spec
itself acknowledges this: it cites **Article 223-1-1 of the French Penal
Code** and lists the real-world outcomes of these techniques — forced
relocations, coordinated harassment (disproportionately against women and
abuse victims), and suicide.

An audit log and a warning dialog do not change what such a tool *does*. A
tool that resolves a stranger's pseudonym to their home address operates on
non-consenting third parties, and its output is precisely the information used
to reach and harm them offline. No "authorization framework" makes that
defensive.

## Capabilities intentionally excluded

Taken does **not** contain, and will not contain:

- **Third-party de-anonymisation.** No resolving a handle/email/phone/name to
  a real identity of someone other than the operator.
- **Cross-account correlation / stylometric unmasking.** No linking of
  "unconnected" pseudonyms belonging to a target to prove a single author.
- **Chronobiological targeting.** No activity-timing analysis aimed at
  correlating a target's separate accounts.
- **Reverse image search / GEOINT against others.** No landmark analysis,
  reverse geocoding, or "where was this taken / where do they live" pipeline.
- **Social-circle mapping.** No scraping of a target's contacts, or of Google
  Maps / review platforms, to triangulate a person's location or relationships.
- **Bulk / automated targeting** of people who are not the operator.
- **Password-reset / recovery-form probing** to enumerate a third party's
  accounts or emails.

## What Taken does instead (the allowed surface)

- **Self-scoped audits.** The `footprint` command checks where the operator's
  **own** handle is publicly present. It is consent-gated, queries only public
  profile URLs (equivalent to typing the handle into a browser), and returns
  remediation advice rather than an identity profile.
- **Metadata hygiene on the operator's own files.** Inspect and strip
  EXIF/GPS/PDF metadata *before* publishing.
- **Education.** Decode the operator's own Discord ID; the OPSEC playbook; the
  legal framework; victim-support resources.

## Contribution rule

Pull requests that add any excluded capability — or that generalise a
self-scoped feature into a third-party targeting one — are out of scope for
this project and will not be accepted. Keep Taken a shield, not a weapon.

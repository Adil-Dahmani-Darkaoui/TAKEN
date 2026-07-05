# Defense playbook

A plain-language companion to `taken playbook` and `taken resources`. Each
section takes a technique from the source awareness video and answers the only
question that matters for a defender: **how do I make this not work on me?**

## 1. Reused usernames link your accounts

An investigator's first move is to take one handle and enumerate it across
hundreds of platforms. A single reused pseudonym collapses your
compartmentalisation instantly.

- Use a distinct, unrelated username per identity sphere (work, gaming,
  activism, personal).
- Prefer random handles over variations on a favourite word — `argentic`,
  `argentic.34`, and `argentic34` are one guess apart.
- Never let a throwaway handle touch an account tied to your real name.
- Self-audit periodically: `python -m taken footprint <your-handle>`.

## 2. Recovery forms reveal your email

Login and password-reset pages often disclose whether an address is
registered, mapping an email to a service.

- One email address per identity sphere.
- Use aliases / plus-addressing / an email relay so a leaked address cannot be
  pivoted to your primary inbox.
- Watch breach notifications and rotate exposed addresses.

## 3. Your Discord ID encodes a timestamp

The ID itself contains the creation time in milliseconds — a permanent anchor
for a timeline. You cannot hide it while using the account.

- Assume it is public.
- Do not pair a compartmentalised Discord account with a handle or avatar you
  use elsewhere; the timestamp only helps once it is matched to another
  account.
- Inspect your own: `python -m taken snowflake <your-id>`.

## 4. The web never forgets (archives)

A profile you cleaned today may have an un-redacted snapshot from years ago.

- Assume everything you post publicly is permanently archived.
- Before publishing, ask whether you would accept it surviving forever.
- Rotate emails/handles that appear in old archives.

## 5. Your writing style is a fingerprint (stylometry)

Sentence length, punctuation, and vocabulary persist across pseudonyms and are
largely unconscious.

- The real defense is not co-locating identities that must stay separate.
- Keep sensitive identities low-volume; less text means a weaker model.

## 6. Your posting rhythm correlates your accounts

Two "unrelated" accounts on the same daily/weekly rhythm and time zone reveal
a single person.

- Do not assume different names mean unlinkable accounts.
- Queue/schedule posts if a live rhythm would be revealing.

## 7. Photos carry GPS (EXIF)

Phones geotag by default; one un-stripped image pins you to a place and time.

- Disable location tagging in your camera app.
- Strip metadata before uploading: `python -m taken metadata clean in.jpg out.jpg`.
- Do not rely on platforms to strip EXIF — many do, some do not.

## 8. Documents leak your name and local paths (PDF metadata)

PDFs embed author names, absolute file paths (revealing your OS username), and
software details.

- Strip document metadata before sharing: `python -m taken metadata clean in.pdf out.pdf`.
- Set a neutral author name in your editor and export from a neutral folder.

## 9. Reverse image search and backgrounds place you

Search engines match your photo elsewhere; signage, plates, and architecture
geolocate it.

- Avoid posting identifiable exteriors near where you live/work.
- Crop or blur signage, plates, distinctive backgrounds.
- Do not reuse a profile photo across identities.

## 10. Your circle exposes you

You can practise perfect OPSEC and still be located through friends' and
family's reviews, tags, and posts.

- Ask close contacts not to tag you or name your regular places.
- Enable tag-approval; review tags applied to you.
- This is the hardest vector — reduce what your circle knows about the
  routines you want kept private.

---

## If you are being targeted

1. **Do not** delete your accounts impulsively — preserve evidence first.
2. Take dated screenshots capturing content, URLs, usernames, and timestamps.
3. Report to the platform and to the authorities below.
4. Reach out for support — you do not have to handle this alone.
5. In immediate physical danger, call your local emergency number (112 in the EU).

### Support resources (France)

- **Pharos** — report illegal online content: <https://www.internet-signalement.gouv.fr/>
- **3018** — free, anonymous cyberviolence hotline: <https://www.3018.fr/>
- **e-Enfance** — protection of minors online: <https://e-enfance.org/>
- **Stop Fisha** — against sexist/sexual cyber-harassment: <https://stopfisha.org/>
- **France Victimes** — legal and psychological victim support: <https://www.france-victimes.fr/>

Outside France, contact your national cybercrime reporting portal, a local
victim-support hotline, and the police.

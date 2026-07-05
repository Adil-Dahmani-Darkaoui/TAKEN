# TAKEN — Boîte à outils défensive de protection de l'empreinte numérique

**TAKEN est un outil défensif de confidentialité.** Il aide une personne à
comprendre et à réduire *sa propre* exposition en ligne. C'est l'inverse
assumé d'un outil d'attaque OSINT : chaque fonctionnalité est limitée aux
données de l'utilisateur lui‑même ou à la pédagogie, et rien dans ce projet ne
sert à désanonymiser, localiser ou profiler autrui.

---

## Démonstration concrète

Le scénario le plus parlant : **une photo de vacances géotaggée**. Un smartphone
enregistre par défaut les coordonnées GPS et l'horodatage dans les métadonnées
EXIF. Une seule photo non nettoyée suffit à un enquêteur pour vous situer.
Voici TAKEN qui révèle la fuite, puis la neutralise (sortie réelle de l'outil) :

**1) On inspecte la photo brute — TAKEN montre ce qu'elle révèle :**

```console
$ python -m taken metadata inspect photo_vacances.jpg
Metadata in photo_vacances.jpg (image):
  gps_info: present (geotagged)
  camera_make: ACME
  camera_model: Phone 12
  software: PhoneOS 4.2
  datetime: 2026:07:05 14:30:00
  ! This image is geotagged with GPS coordinates.
  ! This file is geotagged — strip it before sharing.
```

La photo trahit : les **coordonnées GPS** (donc le lieu), la **marque et le
modèle** de l'appareil, le **logiciel**, et la **date/heure** exactes de la prise.

**2) On nettoie la photo — TAKEN en écrit une copie sans métadonnées :**

```console
$ python -m taken metadata clean photo_vacances.jpg photo_propre.jpg
Wrote metadata-free copy to photo_propre.jpg
```

**3) On ré‑inspecte la copie — plus rien à récolter :**

```console
$ python -m taken metadata inspect photo_propre.jpg
Metadata in photo_propre.jpg (image):
  (no interesting metadata found)
```

Les pixels sont conservés, mais la couche de métadonnées a disparu. C'est
exactement la contre‑mesure à la « fuite EXIF oubliée une seule fois » décrite
dans la vidéo source. La même commande fonctionne sur les **PDF** (elle y
supprime l'auteur, les chemins de fichiers locaux qui révèlent votre nom
d'utilisateur, etc.).

> Reproduire la démo : voir la section [Reproduire la démonstration](#reproduire-la-démonstration).
> Les messages de l'outil sont actuellement en anglais — la traduction de
> l'interface en français est possible sur demande.

---

## Pourquoi ce logiciel (et pas celui du cahier des charges)

La spécification de départ décrivait un pipeline automatisé prenant en entrée
le pseudo / numéro / nom de **n'importe qui** pour en déduire son identité
réelle et son **adresse physique**, notamment en exploitant les données de ses
proches (avis Google Maps, etc.). C'est exactement la capacité utilisée pour le
*doxxing*, le harcèlement et le *swatting* — et le document lui‑même le
reconnaît (Article 223‑1‑1 du Code pénal ; conséquences citées : déménagements
forcés, harcèlement, suicides). Un journal d'audit et une fenêtre
d'avertissement ne changent rien à ce que **fait** un tel outil : localiser des
tiers **sans leur consentement**. Aucun cadre d'« autorisation » ne rend cela
défensif.

La vidéo source est une vidéo de **sensibilisation**. Son vrai but est d'aider
les gens à comprendre leur exposition pour se protéger. C'est ce besoin
légitime que TAKEN sert : il **retourne chaque technique de la vidéo en
défense**, appliquée à *vos propres* données. Le détail de ce qui est
volontairement exclu se trouve dans [`docs/SCOPE.md`](docs/SCOPE.md).

---

## Ce que fait TAKEN

Chaque technique d'attaque de la vidéo, retournée en outil de défense :

| Technique d'attaque (source) | Réponse défensive de TAKEN |
| --- | --- |
| L'énumération de pseudos relie vos comptes entre eux | `footprint` — auto‑audit de la présence publique de **votre** pseudo, avec remédiations |
| Le GPS/EXIF des photos révèle votre position | `metadata inspect` / `metadata clean` — voir et supprimer les métadonnées de **vos** fichiers |
| Les métadonnées PDF trahissent votre nom et vos chemins locaux | `metadata` — idem pour les PDF |
| L'ID Discord (Snowflake) révèle l'âge de votre compte | `snowflake` — décoder **votre** ID pour comprendre la fuite |
| Toutes les techniques ci‑dessus | `playbook` — contre‑mesures concrètes |
| Doxxing / conséquences du harcèlement | `resources` — la loi + où les victimes trouvent de l'aide |
| — | `report` — un rapport d'exposition personnel regroupant tout |

---

## Installation

```bash
git clone https://github.com/Adil-Dahmani-Darkaoui/TAKEN
cd TAKEN
python -m pip install -e .              # cœur de l'outil (bibliothèque standard uniquement)
python -m pip install -e ".[metadata]"  # ajoute le support EXIF/PDF (Pillow, pypdf)
```

Ou sans installation :

```bash
python -m taken --help
```

---

## Utilisation

```bash
# Voir puis supprimer les métadonnées de vos propres photos/PDF
python -m taken metadata inspect ~/photo.jpg
python -m taken metadata clean ~/photo.jpg ~/photo_propre.jpg

# Comprendre ce que révèle votre propre ID Discord
python -m taken snowflake 175928847299117063

# Auto‑audit de votre présence publique.
# Aperçu d'abord (aucune requête) ; ajoutez --consent pour vérifier en direct VOTRE pseudo.
python -m taken footprint monpseudo
python -m taken footprint monpseudo --consent

# Le playbook OPSEC et les ressources légales / d'aide aux victimes
python -m taken playbook
python -m taken resources

# Construire un rapport d'exposition personnel
python -m taken report monpseudo --consent -o mon_exposition.md
```

### Autres exemples réels

**Décoder son propre ID Discord** (le Snowflake encode l'instant de création) :

```console
$ python -m taken snowflake 175928847299117063
Discord ID 175928847299117063 was created on 2016-04-30 11:18:25 UTC (~3718 days ago).

What this leaks about you:
  - The exact creation timestamp of the account/message/server.
  - A fixed anchor for a 'pattern of life' timeline an analyst could
    correlate against activity on your other accounts.

How to defend:
  ...
```

**Auto‑audit d'empreinte** (l'aperçu ne fait *aucune* requête réseau ; il faut
`--consent`, qui affirme que le pseudo est le vôtre, pour lancer les vérifications) :

```console
$ python -m taken footprint monpseudo
Live checks only run for a handle you own. By passing --consent you affirm this handle is yours and you are auditing your own exposure.

Scope preview for 'monpseudo' (no requests made):
  GitHub: would check https://github.com/monpseudo
    remediation: Review your public repos, gists, commit emails, and profile README. ...
```

---

## Garde‑fous — et pourquoi ils sont réels ici

On ne peut pas transformer TAKEN en l'outil du cahier des charges en activant
une option, parce que les moteurs offensifs **n'existent tout simplement pas
dans le code** :

- Aucune résolution d'identité de tiers, aucune démasquage stylométrique,
  aucune corrélation inter‑comptes.
- Aucune recherche d'image inversée, aucun géocodage inversé, aucune logique
  « trouver où ils habitent ».
- Aucun *scraping* de l'entourage / des avis Google Maps pour trianguler
  quelqu'un.
- L'audit `footprint` exige le consentement, se limite à *votre* pseudo,
  n'interroge que des URL de profils publics (ce que vous pourriez taper
  vous‑même dans un navigateur) et renvoie des conseils de remédiation — pas un
  dossier d'identité.

---

## Si vous êtes visé(e)

Ne supprimez pas vos comptes de façon impulsive — **conservez d'abord les
preuves** (captures d'écran datées avec URL et horodatages), puis signalez.
Lancez `python -m taken resources` pour les portails de signalement et les
lignes d'aide (Pharos, 3018, e‑Enfance, Stop Fisha, France Victimes), ou
consultez [`docs/DEFENSE_PLAYBOOK.md`](docs/DEFENSE_PLAYBOOK.md).

---

## Reproduire la démonstration

```bash
python -m pip install -e ".[metadata]" piexif   # piexif sert uniquement à fabriquer la photo de test
python - <<'PY'
import piexif
from PIL import Image
def dms(deg):
    d=int(deg); m=int((deg-d)*60); s=round((deg-d-m/60)*3600,4)
    return ((d,1),(m,1),(int(s*100),100))
zeroth = {piexif.ImageIFD.Make:"ACME", piexif.ImageIFD.Model:"Phone 12",
          piexif.ImageIFD.Software:"PhoneOS 4.2",
          piexif.ImageIFD.DateTime:"2026:07:05 14:30:00"}
gps = {piexif.GPSIFD.GPSLatitudeRef:'N', piexif.GPSIFD.GPSLatitude:dms(48.8584),
       piexif.GPSIFD.GPSLongitudeRef:'E', piexif.GPSIFD.GPSLongitude:dms(2.2945)}
Image.new("RGB",(96,96),(70,130,180)).save(
    "photo_vacances.jpg", exif=piexif.dump({"0th":zeroth,"Exif":{},"GPS":gps}))
PY
python -m taken metadata inspect photo_vacances.jpg
python -m taken metadata clean photo_vacances.jpg photo_propre.jpg
python -m taken metadata inspect photo_propre.jpg
```

---

## Développement

```bash
python -m pip install -e ".[dev]"
python -m pytest        # 15 tests
```

## Licence

MIT — voir [`LICENSE`](LICENSE).

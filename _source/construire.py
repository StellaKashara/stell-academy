#!/usr/bin/env python3
"""Construit les pages du site Stell'A-cademy.

Chaque page est décrite dans _source/pages/*.html :
    chemin: poles/formation-coaching/
    titre: Titre de l'onglet
    description: Description pour les moteurs de recherche
    menu: poles
    ---
    (contenu HTML de la page)

Le gabarit commun (menu, pied de page) est dans _source/gabarit.html.
Dans les contenus :
    {{racine}}            -> chemin relatif vers la racine du site
    [[numéro BCE]]        -> emplacement signalé « À COMPLÉTER »
    {{photo:06}}          -> photo n°06 de la banque d'images (voir PHOTOS ci-dessous).
                             Tant que le fichier images/06-....webp n'existe pas, un bloc
                             de couleur avec une étiquette le remplace. Mots ajoutés après
                             le numéro = classes CSS ; « hero » = chargement immédiat.
    {{autres-poles:3}}    -> liens vers les cinq autres pôles (ici : sauf le pôle 3)
    {{formulaire:contact}} -> formulaire de demande (contact, devis ou consultation)

Utilisation :
    python3 _source/construire.py              # écrit le site à la racine du dépôt
    python3 _source/construire.py --apercu DIR # copie d'aperçu (liens vers index.html)

Le dossier _source n'est pas publié par GitHub Pages (dossier commençant par « _ »).
"""
import pathlib
import re
import shutil
import sys

SOURCE = pathlib.Path(__file__).resolve().parent
RACINE_DEPOT = SOURCE.parent


# Banque d'images : numéro -> (fichier, description de la photo prévue, couleur d'attente)
PHOTOS = {
    "01": ("01-entrepreneure-bureau", "Entrepreneure à son bureau, lumière du matin", "Une entrepreneure souriante, en blazer beige, réfléchit à son bureau devant son ordinateur portable.", "#D9B9A0"),
    "02": ("02-atelier-groupe", "Atelier en petit groupe", "Un formateur anime un atelier devant un petit groupe attentif réuni autour d’une table.", "#E8DCCB"),
    "03": ("03-tete-a-tete-cafe", "Tête-à-tête autour d’un café", "Deux femmes travaillent ensemble autour d’un carnet ouvert, une tasse de café sur la table.", "#C9AE97"),
    "04": ("04-mise-en-relation", "Mise en relation", "Trois professionnels échangent leurs cartes de visite lors d’un événement de réseautage.", "#A88B74"),
    "05": ("05-flat-lay-communication", "Communication", "Vue du dessus d’un carnet, d’un smartphone, d’un nuancier beige et d’un stylo doré sur fond de lin.", "#F1E7DA"),
    "06": ("06-prise-de-parole", "Prise de parole", "Une intervenante s’adresse à un petit public, vue de trois-quarts.", "#B89A82"),
    "07": ("07-mains-planning", "Rendez-vous de travail", "Une conseillère présente des documents à deux personnes autour d’un bureau.", "#DCC6B2"),
    "08": ("08-ordinateur-strategie", "Ordinateur et stratégie", "Ordinateur portable ouvert, tasse et documents posés sur un bureau épuré.", "#E5D3C1"),
    "09": ("09-ombres-plantes", "Ombres et plantes", "Ombre de feuillage sur un mur beige.", "#EADFD0"),
    "10": ("10-portrait-fondatrice", "Portrait de la fondatrice", "Portrait de la fondatrice de Stell’A-cademy, assise, sur fond crème.", "#6B4A36"),
    "11": ("11-texture-lin", "Texture lin", "Gros plan d’une texture de lin beige.", "#F3ECE1"),
    "12": ("12-details-bureau", "Détails de bureau", "Tasse en céramique, fleurs séchées et livres empilés sur un bureau.", "#CFB59E"),
}

# Les 6 pôles : numéro -> (adresse, nom)
POLES = {
    1: ("poles/formation-coaching/", "Formation &amp; Coaching"),
    2: ("poles/reseautage-mise-en-relation/", "Réseautage &amp; Mise en relation"),
    3: ("poles/comptabilite-fiscalite-entrepreneuriat/", "Comptabilité, Fiscalité &amp; Entrepreneuriat"),
    4: ("poles/project-facility-management/", "Project &amp; Facility Management"),
    5: ("poles/image-creativite/", "Image &amp; Créativité"),
    6: ("poles/innovation-intelligence-artificielle/", "Innovation &amp; Intelligence Artificielle"),
}

# Adresse d'envoi du formulaire.
# TODO (à configurer une fois) : créer un formulaire gratuit sur https://formspree.io avec
# l'adresse e-mail de Stell’A-cademy, puis remplacer VOTRE-IDENTIFIANT par le code fourni.
# Tant que ce n'est pas fait, le formulaire affiche un message d'aperçu sans rien envoyer.
FORMULAIRE_ACTION = "https://formspree.io/f/VOTRE-IDENTIFIANT"

FORMULAIRES = {
    "contact": ("Quel pôle vous intéresse ?", "Votre message", "Envoyer ma demande", "Nouveau message depuis le site"),
    "devis": ("Pour quel pôle souhaitez-vous un devis ?", "Décrivez votre besoin (quoi, pour quand, en quelle quantité)", "Demander mon devis", "Demande de devis depuis le site"),
    "consultation": ("Sur quel sujet souhaitez-vous faire le point ?", "Vos disponibilités et ce que vous aimeriez aborder", "Demander ma consultation", "Demande de consultation découverte"),
}


def photo(m):
    numero, reste = m.group(1), m.group(2).split()
    fichier, titre, alt, ton = PHOTOS[numero]
    classes = " ".join(c for c in reste if c != "hero")
    chargement = "eager" if "hero" in reste else "lazy"
    chemin = RACINE_DEPOT / "images" / f"{fichier}.webp"
    if chemin.exists():
        dedans = (f'<img src="{{{{racine}}}}images/{fichier}.webp" alt="{alt}" '
                  f'width="1672" height="941" loading="{chargement}" decoding="async">')
        return f'<div class="photo {classes}">{dedans}</div>'
    return (f'<div class="photo photo--attente {classes}" style="--ton:{ton}" role="img" aria-label="{alt}" '
            f'data-fichier="images/{fichier}.webp"><span class="photo__etiquette" aria-hidden="true">'
            f'Photo {numero} · {titre}</span></div>')


def autres_poles(m):
    actuel = int(m.group(1))
    liens = []
    for numero, (adresse, nom) in POLES.items():
        if numero == actuel:
            continue
        liens.append(f'<li><a class="pole-lien" href="{{{{racine}}}}{adresse}"><span>'
                     f'<span class="numero">0{numero}</span> <strong>{nom}</strong></span>'
                     f'<span aria-hidden="true">→</span></a></li>')
    return '<ul class="pole-liens">\n' + "\n".join(liens) + "\n</ul>"


def formulaire(m):
    sorte = m.group(1)
    legende, libelle_message, bouton, sujet = FORMULAIRES[sorte]
    choix = [(str(n), nom) for n, (_, nom) in POLES.items()] + [("autre", "Je ne sais pas encore")]
    cases = "\n".join(
        f'<label class="choix"><input type="radio" name="pole" value="{valeur}"'
        f'{" checked" if valeur == "autre" else ""}><span>{nom}</span></label>'
        for valeur, nom in choix
    )
    return f'''<div class="formulaire-carte" data-formulaire>
  <form class="formulaire" action="{FORMULAIRE_ACTION}" method="post">
    <input type="hidden" name="_subject" value="{sujet}">
    <fieldset class="formulaire__poles">
      <legend>{legende}</legend>
      <div class="choix-grille">
{cases}
      </div>
    </fieldset>
    <div class="champs-duo">
      <label class="champ">Prénom et nom
        <input type="text" name="nom" autocomplete="name" required>
      </label>
      <label class="champ">E-mail
        <input type="email" name="email" autocomplete="email" required>
      </label>
    </div>
    <label class="champ">Votre activité <span class="champ__aide">(facultatif)</span>
      <input type="text" name="activite" autocomplete="organization-title">
    </label>
    <label class="champ">{libelle_message}
      <textarea name="message" rows="5" required></textarea>
    </label>
    <div class="formulaire__pied">
      <p class="formulaire__note">Vos données servent uniquement à vous recontacter. <a href="{{{{racine}}}}confidentialite/">Confidentialité</a></p>
      <button class="bouton bouton--plein" type="submit">{bouton}</button>
    </div>
    <p class="formulaire__erreur" role="alert" hidden>L’envoi n’a pas fonctionné. Réessayez dans un instant ou écrivez-nous directement par e-mail.</p>
  </form>
  <div class="formulaire__merci" tabindex="-1" hidden>
    <span class="formulaire__merci-mot">Merci.</span>
    <h2>Votre demande est bien envoyée.</h2>
    <p>Nous revenons vers vous sous [[délai de réponse]] pour convenir d’un rendez-vous.</p>
    <p class="formulaire__apercu" hidden>Aperçu : le formulaire n’est pas encore relié à une boîte e-mail, rien n’a été envoyé.</p>
    <button class="bouton bouton--trait" type="button" data-nouvelle-demande>Envoyer une autre demande</button>
  </div>
</div>'''


def lire_page(fichier):
    texte = fichier.read_text(encoding="utf-8")
    entete, contenu = texte.split("\n---\n", 1)
    infos = {}
    for ligne in entete.strip().splitlines():
        cle, valeur = ligne.split(":", 1)
        infos[cle.strip()] = valeur.strip()
    infos["contenu"] = contenu
    return infos


def emplacements(html):
    return re.sub(
        r"\[\[(.+?)\]\]",
        r'<span class="a-completer">[À COMPLÉTER : \1]</span>',
        html,
    )


def construire_page(gabarit, page):
    chemin = page["chemin"].strip("/")
    profondeur = 0 if not chemin else chemin.count("/") + 1
    racine = "../" * profondeur or "./"
    html = gabarit.replace("{{contenu}}", page["contenu"].strip())
    html = re.sub(r"\{\{formulaire:([a-z]+)\}\}", formulaire, html)
    html = re.sub(r"\{\{photo:(\d\d)([^}]*)\}\}", photo, html)
    html = re.sub(r"\{\{autres-poles:(\d)\}\}", autres_poles, html)
    html = html.replace("{{titre}}", page["titre"])
    html = html.replace("{{description}}", page["description"])
    menu = page.get("menu", "")
    html = re.sub(
        r"\{\{actif:([a-z-]+)\}\}",
        lambda m: ' aria-current="page"' if m.group(1) == menu else "",
        html,
    )
    html = html.replace("{{racine}}", racine)
    html = emplacements(html)
    return chemin, html


def vers_apercu(html, est_accueil):
    # Liens « dossier/ » -> « dossier/index.html » (l'aperçu ne devine pas index.html)
    def corriger(m):
        attr, url = m.group(1), m.group(2)
        if url.startswith(("http", "mailto:", "tel:", "#")):
            return m.group(0)
        base, ancre = (url.split("#", 1) + [""])[:2]
        base, requete = (base.split("?", 1) + [""])[:2]
        if base.endswith("/"):
            base += "index.html"
        return f'{attr}="{base}{"?" + requete if requete else ""}{"#" + ancre if ancre else ""}"'

    html = re.sub(r'(href)="([^"]*)"', corriger, html)
    if est_accueil:
        html = re.sub(r"<!doctype html>\s*|</?html[^>]*>\s*|</?head>\s*|</?body>\s*", "", html, flags=re.I)
    return html


def main():
    apercu = None
    if len(sys.argv) == 3 and sys.argv[1] == "--apercu":
        apercu = pathlib.Path(sys.argv[2]).resolve()
    gabarit = (SOURCE / "gabarit.html").read_text(encoding="utf-8")
    sortie = apercu or RACINE_DEPOT
    if apercu:
        shutil.rmtree(apercu, ignore_errors=True)
        shutil.copytree(RACINE_DEPOT / "assets", apercu / "assets")
        if (RACINE_DEPOT / "images").exists():
            shutil.copytree(RACINE_DEPOT / "images", apercu / "images")
    for fichier in sorted((SOURCE / "pages").glob("*.html")):
        chemin, html = construire_page(gabarit, lire_page(fichier))
        if apercu:
            html = vers_apercu(html, est_accueil=(chemin == ""))
        cible = sortie / chemin / "index.html" if chemin else sortie / "index.html"
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(html, encoding="utf-8")
        print("écrit", cible.relative_to(sortie))


if __name__ == "__main__":
    main()

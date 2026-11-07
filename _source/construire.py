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
        if base.endswith("/"):
            base += "index.html"
        return f'{attr}="{base}{"#" + ancre if ancre else ""}"'

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

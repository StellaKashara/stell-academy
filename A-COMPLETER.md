# À compléter — site Stell’A-cademy

Sur le site, chaque emplacement à remplir apparaît en jaune : **[À COMPLÉTER : …]**.
Envoyez simplement les informations ; elles seront intégrées puis le site sera reconstruit.

## 1. Coordonnées et informations légales
(pied de page, page Contact, Mentions légales)

- [ ] E-mail de contact professionnel
- [ ] Numéro de téléphone
- [ ] Ville (et adresse du lieu de rendez-vous, page Consultation découverte)
- [ ] Adresse du siège
- [ ] Nom légal et forme juridique
- [ ] Nom de la responsable de la publication
- [ ] Numéro d’entreprise (BCE)
- [ ] Numéro de TVA (si assujettie) et mention « TVA comprise » ou « hors TVA » sur les tarifs
- [ ] Lien Instagram (et LinkedIn si vous souhaitez l’afficher)
- [ ] Délai de réponse annoncé après l’envoi d’un formulaire (ex. « 48 heures »)

## 2. Prix
Seuls les prix déjà fournis sont affichés (pôle Image & Créativité : 129 €, 149 €, 149 €, 79 €, mini-site sur devis).

- [ ] Pôle 1 Formation & Coaching : formations et ateliers, coaching (durée et prix, ou « sur devis »)
- [ ] Étudiants-Profs : prix d’un cours et frais de mise en relation
- [ ] Pôle 2 Réseautage : réseau, mise en relation, animation et partenariats
- [ ] Pôle 3 Bras droit administratif : aide ponctuelle et suivi mensuel
- [ ] Pôle 4 Project & Facility : gestion de projets, organisation interne, digitalisation (à l’unité / en pack)
- [ ] Pôle 6 Innovation & IA : découverte, automatisation, innovation digitale

## 3. Agendas (dates, thèmes, lieux)
- [ ] Pôle 1 : prochaines sessions de formation
- [ ] Pôle 2 : prochaines rencontres réseau
- [ ] Pôle 6 : prochains ateliers IA
- [ ] Lien vers un agenda de réservation en ligne, si vous en utilisez un (page Consultation découverte)

## 4. Page « À propos »
- [ ] Votre histoire : d’où vient l’idée, votre parcours
- [ ] Le sens de la devise « Exception is you »
- [ ] Trois valeurs, avec une phrase chacune

## 5. Textes à relire
Les descriptions courtes des offres de chaque pôle ont été rédigées à partir des intitulés existants : merci de les relire et de les corriger si besoin.
Pages encore vides : Confidentialité, Conditions générales, Cookies.
Aucun témoignage ni référence client n’est affiché : à fournir si vous le souhaitez.

## 6. Photos
✅ = photo déjà en place. Pour les autres, des blocs de couleur indiquent l’emplacement de chaque photo.
Déposez les photos dans un dossier `images/` avec exactement ces noms : elles remplaceront automatiquement les blocs.
Format WebP, moins de 300 Ko ; grandes photos 2400 × 1600 px, cartes en portrait 4:5.

| N° | Fichier | Photo | Utilisée sur |
|----|---------|-------|--------------|
| 01 | `images/01-entrepreneure-bureau.webp` | ✅ Entrepreneure à son bureau | Accueil, Services phares |
| 02 | `images/02-atelier-groupe.webp` | ✅ Atelier en petit groupe | Accueil, Pôle 1, Services phares |
| 03 | `images/03-tete-a-tete-cafe.webp` | ✅ Tête-à-tête autour d’un café | Pôle 4, Consultation |
| 04 | `images/04-mise-en-relation.webp` | ✅ Mise en relation | Accueil, Pôle 2 |
| 05 | `images/05-flat-lay-communication.webp` | Vue du dessus : carnet, téléphone, nuancier | Pôle 5 |
| 06 | `images/06-prise-de-parole.webp` | Prise de parole devant un petit public | (réserve) |
| 07 | `images/07-mains-planning.webp` | ✅ Rendez-vous de travail autour de documents | Pôle 3, Services phares, Devis |
| 08 | `images/08-ordinateur-strategie.webp` | Ordinateur et stratégie | Pôle 6 |
| 09 | `images/09-ombres-plantes.webp` | Ombres et plantes sur mur beige | (réserve) |
| 10 | `images/10-portrait-fondatrice.webp` | **Votre portrait** | À propos, Contact |
| 11 | `images/11-texture-lin.webp` | Texture lin | (réserve) |
| 12 | `images/12-details-bureau.webp` | Détails de bureau | Pôle 4 |

Image de partage (aperçu sur les réseaux sociaux, 1200 × 630 px) : à prévoir avec les photos.

## 7. Logo
- [ ] Fichier du logo officiel (en attendant, le nom est écrit en texte et l’icône d’onglet est un simple aplat de couleur).

## 8. Formulaires (contact, devis, consultation) — configuration technique, une seule fois
Le site n’a pas de serveur : les formulaires passent par le service gratuit Formspree.
1. Créer un compte sur formspree.io avec l’e-mail de Stell’A-cademy et créer un formulaire.
2. Copier son identifiant (ex. `xyzabcd`) et le remplacer dans `_source/construire.py`, ligne `FORMULAIRE_ACTION`.
3. Reconstruire le site.
Tant que ce n’est pas fait, le formulaire affiche le message de remerciement avec la mention « Aperçu : rien n’a été envoyé ».

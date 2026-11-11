// Stell’A-cademy — petits comportements du site. Sans JavaScript, tout reste lisible et utilisable.
document.addEventListener("DOMContentLoaded", function () {
  // 1. Menu repliable sur petit écran
  var bouton = document.querySelector(".menu-bouton");
  var menu = document.getElementById("menu");
  if (bouton && menu) {
    bouton.addEventListener("click", function () {
      var ouvert = menu.classList.toggle("est-ouvert");
      bouton.setAttribute("aria-expanded", ouvert ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && menu.classList.contains("est-ouvert")) {
        menu.classList.remove("est-ouvert");
        bouton.setAttribute("aria-expanded", "false");
        bouton.focus();
      }
    });
  }

  // 2. Sélecteur de pôles (accueil) : un bouton = un panneau
  var boutons = document.querySelectorAll("[data-selecteur] button[aria-controls]");
  if (boutons.length) {
    var choisir = function (actif) {
      boutons.forEach(function (b) {
        var on = b === actif;
        b.setAttribute("aria-pressed", on ? "true" : "false");
        document.getElementById(b.getAttribute("aria-controls")).hidden = !on;
      });
    };
    boutons.forEach(function (b) {
      b.addEventListener("click", function () { choisir(b); });
    });
    choisir(boutons[0]);
  }

  // 3. Formulaires de demande
  document.querySelectorAll("[data-formulaire]").forEach(function (bloc) {
    var form = bloc.querySelector("form");
    var merci = bloc.querySelector(".formulaire__merci");
    var erreur = bloc.querySelector(".formulaire__erreur");
    var apercu = bloc.querySelector(".formulaire__apercu");

    // Pôle présélectionné depuis un lien « …/contact/?pole=3 »
    var pole = new URLSearchParams(window.location.search).get("pole");
    if (pole) {
      var radio = form.querySelector('input[name="pole"][value="' + pole.replace(/[^a-z0-9]/gi, "") + '"]');
      if (radio) radio.checked = true;
    }

    var afficherMerci = function (estApercu) {
      form.hidden = true;
      apercu.hidden = !estApercu;
      merci.hidden = false;
      merci.focus();
    };

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      erreur.hidden = true;
      // TODO : tant que l'identifiant Formspree n'est pas renseigné, on montre seulement le message.
      if (form.action.indexOf("VOTRE-IDENTIFIANT") !== -1) {
        afficherMerci(true);
        return;
      }
      var envoi = form.querySelector('button[type="submit"]');
      envoi.disabled = true;
      fetch(form.action, {
        method: "POST",
        body: new FormData(form),
        headers: { Accept: "application/json" }
      }).then(function (r) {
        if (!r.ok) throw new Error("envoi");
        form.reset();
        afficherMerci(false);
      }).catch(function () {
        erreur.hidden = false;
      }).then(function () {
        envoi.disabled = false;
      });
    });

    bloc.querySelector("[data-nouvelle-demande]").addEventListener("click", function () {
      merci.hidden = true;
      form.hidden = false;
      form.querySelector("input:not([type=hidden]), textarea").focus();
    });
  });
});

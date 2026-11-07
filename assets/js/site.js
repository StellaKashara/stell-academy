// Menu repliable sur petit écran. Sans JavaScript, le menu reste simplement affiché.
document.addEventListener("DOMContentLoaded", function () {
  var bouton = document.querySelector(".menu-bouton");
  var menu = document.getElementById("menu");
  if (!bouton || !menu) return;
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
});

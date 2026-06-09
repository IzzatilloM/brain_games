/* BrainGames — umumiy interfeys: sidebar, tema, toast */
(function () {
  "use strict";
  var root = document.documentElement;

  // Sidebar toggle (desktop: yig'ish / mobil: ochish)
  var toggle = document.getElementById("navToggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      if (window.innerWidth >= 992) {
        root.classList.toggle("nav-collapsed");
        localStorage.setItem("bg_nav", root.classList.contains("nav-collapsed") ? "collapsed" : "open");
      } else {
        root.classList.toggle("nav-open");
      }
    });
  }
  var scrim = document.getElementById("scrim");
  if (scrim) scrim.addEventListener("click", function () { root.classList.remove("nav-open"); });

  // Tema almashtirish
  var themeBtn = document.getElementById("themeToggle");
  function syncThemeIcon() {
    if (!themeBtn) return;
    var dark = root.getAttribute("data-theme") === "dark";
    themeBtn.innerHTML = dark ? '<i class="bi bi-sun-fill"></i>' : '<i class="bi bi-moon-stars"></i>';
  }
  syncThemeIcon();
  if (themeBtn) {
    themeBtn.addEventListener("click", function () {
      var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("bg_theme", next);
      syncThemeIcon();
    });
  }

  // Toastlarni avtomatik yopish
  document.querySelectorAll(".ms-toast").forEach(function (t, i) {
    setTimeout(function () {
      t.style.transition = "opacity .4s, transform .4s";
      t.style.opacity = "0";
      t.style.transform = "translateX(40px)";
      setTimeout(function () { t.remove(); }, 400);
    }, 3600 + i * 400);
  });
})();

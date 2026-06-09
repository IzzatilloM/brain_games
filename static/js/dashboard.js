/* Kabinet: haftalik faollik bar-chartini chizish */
(function () {
  "use strict";
  const chart = document.getElementById("weekChart");
  if (!chart) return;

  const labels = (chart.dataset.labels || "").split(",").filter(Boolean);
  const values = (chart.dataset.values || "").split(",").map(Number);
  const max = Math.max(1, ...values);

  chart.innerHTML = "";
  values.forEach((v, i) => {
    const pct = Math.round((v / max) * 100);
    const wrap = document.createElement("div");
    wrap.className = "bar-wrap";
    wrap.innerHTML =
      '<span class="bar-val">' + (v || "") + "</span>" +
      '<div class="bar" data-zero="' + (v === 0 ? 1 : 0) + '" style="height:0%"></div>' +
      '<span class="bar-lbl">' + (labels[i] || "") + "</span>";
    chart.appendChild(wrap);
    const bar = wrap.querySelector(".bar");
    requestAnimationFrame(() =>
      setTimeout(() => (bar.style.height = Math.max(4, pct) + "%"), 60 * i)
    );
  });
})();

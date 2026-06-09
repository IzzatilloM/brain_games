/* Abakus (soroban) — ko'rsatilgan sonni o'qish o'yini */
(function () {
  "use strict";
  const R = MindSkillsGame.randInt;

  function bead(top, active) {
    return '<div class="bead' + (active ? " active" : "") + '" style="top:' + top + 'px"></div>';
  }

  // Bitta ustun (xona) — 0..9 qiymat
  function column(value) {
    const heavenOn = value >= 5;
    const earthOn = value % 5;
    let html = '<div class="aba-col"><div class="aba-frame">';
    html += '<div class="aba-rod"></div>';
    // Osmon (5 lik bead)
    html += '<div class="aba-heaven">' + bead(heavenOn ? 42 : 2, heavenOn) + "</div>";
    // Yer (4 ta 1 lik bead)
    html += '<div class="aba-earth">';
    for (let i = 0; i < earthOn; i++) html += bead(2 + i * 30, true);     // tepaga (bar yoniga)
    for (let j = 0; j < 4 - earthOn; j++) html += bead(170 - j * 30, false); // pastga
    html += "</div></div>";
    html += '<div class="aba-val">' + value + "</div>";
    html += "</div>";
    return html;
  }

  function render(container, digits) {
    container.innerHTML = digits.map(column).join("");
  }

  function genDigits(d) {
    const count = Math.min(5, Math.ceil(d / 2));
    const digits = [];
    for (let i = 0; i < count; i++) {
      digits.push(i === 0 && count > 1 ? R(1, 9) : R(0, 9));
    }
    if (count === 1) digits[0] = R(1, 9);
    return digits;
  }

  MindSkillsGame.play({
    totalQuestions: 10,
    lives: 3,
    round: function (ctx) {
      const digits = genDigits(ctx.difficulty);
      const number = Number(digits.join(""));
      const places = ["birlik", "o'nlik", "yuzlik", "minglik", "o'n minglik"];
      const hint = digits
        .slice()
        .reverse()
        .map((v, i) => v + " " + places[i])
        .reverse()
        .join(" + ");

      ctx.stage.innerHTML =
        '<div class="prompt-sub">Abakusdagi sonni yozing:</div>' +
        '<div id="abacusBox" class="abacus"></div>' +
        '<div class="answer-row">' +
        '<input type="text" inputmode="numeric" class="answer-input" id="ansIn" autocomplete="off" placeholder="?">' +
        '<button class="btn" id="ansBtn">→</button>' +
        "</div>";

      render(ctx.stage.querySelector("#abacusBox"), digits);
      const input = ctx.stage.querySelector("#ansIn");
      input.focus();
      const hintTimer = setTimeout(() => ctx.showHint(hint), 8000);

      function submit() {
        clearTimeout(hintTimer);
        const val = input.value.trim();
        if (val === "") { input.focus(); return; }
        ctx.answer({
          isCorrect: Number(val) === number,
          prompt: "Abakus: " + number,
          correctAnswer: number,
          userAnswer: val,
        });
      }
      ctx.stage.querySelector("#ansBtn").addEventListener("click", submit);
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") submit(); });
    },
  });
})();

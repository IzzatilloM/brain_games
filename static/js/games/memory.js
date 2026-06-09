/* Xotira — yonib o'tgan kataklar ketma-ketligini takrorlash o'yini */
(function () {
  "use strict";
  const R = MindSkillsGame.randInt;

  function gridSize(d) {
    if (d <= 4) return 9;
    if (d <= 8) return 12;
    return 16;
  }

  MindSkillsGame.play({
    totalQuestions: 8,
    lives: 3,
    round: function (ctx) {
      const N = gridSize(ctx.difficulty);
      const cols = N <= 9 ? 3 : 4;
      const seqLen = Math.min(N - 2, 2 + Math.floor(ctx.difficulty * 0.7));

      // Tasodifiy ketma-ketlik (takrorsiz)
      const all = Array.from({ length: N }, (_, i) => i);
      MindSkillsGame.shuffle(all);
      const seq = all.slice(0, seqLen);

      ctx.stage.innerHTML =
        '<div class="prompt-sub" id="ml">Diqqat bilan kuzating... (' + seqLen + " ta)</div>" +
        '<div id="mb" class="memo-grid" style="grid-template-columns:repeat(' + cols + ',1fr)"></div>';

      const label = ctx.stage.querySelector("#ml");
      const box = ctx.stage.querySelector("#mb");
      const cells = [];
      for (let i = 0; i < N; i++) {
        const c = document.createElement("div");
        c.className = "memo-cell";
        c.textContent = i + 1;
        box.appendChild(c);
        cells.push(c);
      }

      const flashMs = Math.max(320, 720 - ctx.difficulty * 25);
      let step = 0;

      // Ketma-ketlikni ko'rsatish
      const playSeq = setInterval(() => {
        if (step > 0) cells[seq[step - 1]].classList.remove("show");
        if (step >= seq.length) {
          clearInterval(playSeq);
          setTimeout(startInput, 250);
          return;
        }
        cells[seq[step]].classList.add("show");
        step++;
      }, flashMs);

      function startInput() {
        label.textContent = "Endi takrorlang! 👆";
        let pos = 0;
        const inputStart = Date.now();
        const picks = [];

        cells.forEach((c, idx) => {
          c.addEventListener("click", function onClick() {
            if (c.classList.contains("good") || c.classList.contains("bad")) return;
            picks.push(idx);
            if (idx === seq[pos]) {
              c.classList.add("good");
              pos++;
              if (pos === seq.length) finish(true);
            } else {
              c.classList.add("bad");
              // To'g'ri ketma-ketlikni ko'rsatish
              seq.forEach((s) => cells[s].classList.add("picked"));
              finish(false);
            }
          });
        });

        function finish(correct) {
          cells.forEach((c) => (c.style.pointerEvents = "none"));
          ctx.answer({
            isCorrect: correct,
            prompt: "Ketma-ketlik (" + seqLen + " ta)",
            correctAnswer: seq.map((i) => i + 1).join("-"),
            userAnswer: picks.map((i) => i + 1).join("-"),
            timeMs: Date.now() - inputStart,
          });
        }
      }
    },
  });
})();

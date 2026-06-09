/* Tez o'qish — yonib o'chgan so'zni tanib olish o'yini */
(function () {
  "use strict";
  const shuffle = MindSkillsGame.shuffle;

  // O'zbekcha so'zlar (uzunligi bo'yicha guruhlangan)
  const WORDS = {
    short: ["olma", "kitob", "quyosh", "daraxt", "bola", "gul", "non", "suv", "tog'", "uy", "yo'l", "ko'l", "ot", "qush", "baliq"],
    mid: ["maktab", "do'stlik", "bahor", "kapalak", "chiroyli", "yulduz", "dengiz", "shamol", "qalam", "daftar", "oyna", "bog'cha", "asalari", "telefon", "koptok"],
    long: ["kompyuter", "samolyot", "kutubxona", "matematika", "tabiat", "geografiya", "do'kondor", "musiqachi", "rassomchilik", "sayohatchi", "mustaqillik", "ona-Vatan", "bilimdon", "qahramon", "gulzorbog'"],
  };

  function poolFor(d) {
    if (d <= 4) return WORDS.short;
    if (d <= 8) return WORDS.mid;
    return WORDS.long;
  }

  MindSkillsGame.play({
    totalQuestions: 8,
    lives: 3,
    round: function (ctx) {
      const pool = poolFor(ctx.difficulty);
      const bag = shuffle(pool.slice());
      const target = bag[0];
      const options = shuffle([target, bag[1], bag[2], bag[3]]);
      const flashMs = Math.max(250, 1250 - ctx.difficulty * 85);

      ctx.stage.innerHTML =
        '<div class="prompt-sub" id="rl">Diqqat bilan qarang...</div>' +
        '<div class="reader" id="rw">' + target + "</div>" +
        '<div class="options hidden" id="ro"></div>';

      const label = ctx.stage.querySelector("#rl");
      const word = ctx.stage.querySelector("#rw");
      const optBox = ctx.stage.querySelector("#ro");

      // So'zni belgilangan vaqtdan keyin yashirish
      setTimeout(() => {
        word.textContent = "🔒";
        word.style.opacity = "0.25";
        label.innerHTML = 'Qaysi so\'zni ko\'rdingiz? <span class="wpm-tag">' + Math.round(60000 / flashMs / (target.length / 5)) + " so'z/daq</span>";
        optBox.classList.remove("hidden");
        optBox.innerHTML = options
          .map((w) => '<button class="opt-btn" data-w="' + w + '">' + w + "</button>")
          .join("");

        optBox.querySelectorAll(".opt-btn").forEach((btn) => {
          btn.addEventListener("click", () => {
            const picked = btn.dataset.w;
            const correct = picked === target;
            optBox.querySelectorAll(".opt-btn").forEach((b) => {
              if (b.dataset.w === target) b.classList.add("correct");
              else if (b === btn) b.classList.add("wrong");
              b.disabled = true;
            });
            ctx.answer({
              isCorrect: correct,
              prompt: "So'z: " + target,
              correctAnswer: target,
              userAnswer: picked,
            });
          });
        });
      }, flashMs);
    },
  });
})();

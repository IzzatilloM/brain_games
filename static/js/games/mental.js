/* Mental arifmetika — xayolan hisoblash o'yini */
(function () {
  "use strict";
  const R = MindSkillsGame.randInt;

  function gen(d) {
    let a, b, op, answer, hint;

    if (d <= 2) {
      a = R(1, 9); b = R(1, 9);
      if (a >= b && Math.random() < 0.4) { op = "−"; answer = a - b; }
      else { op = "+"; answer = a + b; }
      hint = "Barmoqlaringizda sanab ko'ring.";
    } else if (d <= 4) {
      a = R(5, 20); b = R(2, 9);
      if (a >= b && Math.random() < 0.5) { op = "−"; answer = a - b; }
      else { op = "+"; answer = a + b; }
      hint = "Avval o'nliklarni, keyin birliklarni hisoblang.";
    } else if (d <= 6) {
      a = R(10, 50); b = R(10, 40);
      if (a >= b && Math.random() < 0.5) { op = "−"; answer = a - b; }
      else { op = "+"; answer = a + b; }
      hint = "Sonni yaxlitlab oling: masalan " + a + " ≈ " + Math.round(a / 10) * 10 + ".";
    } else if (d <= 8) {
      // ko'paytirish kiradi
      if (Math.random() < 0.5) {
        a = R(2, 9); b = R(2, 9); op = "×"; answer = a * b;
        hint = a + " ni " + b + " marta qo'shing.";
      } else {
        a = R(20, 80); b = R(10, 60);
        if (a >= b && Math.random() < 0.5) { op = "−"; answer = a - b; }
        else { op = "+"; answer = a + b; }
        hint = "Bosqichma-bosqich: o'nliklar + birliklar.";
      }
    } else {
      // uch hadli yoki kattaroq ko'paytma
      if (Math.random() < 0.5) {
        const x = R(2, 12), y = R(2, 9);
        return { text: x + " × " + y, answer: x * y, hint: x + " ni " + y + " marta qo'shing." };
      }
      const x = R(20, 90), y = R(10, 50), z = R(5, 20);
      return { text: x + " + " + y + " − " + z, answer: x + y - z, hint: "Chapdan o'ngga: avval qo'shing, keyin ayiring." };
    }
    return { text: a + " " + op + " " + b, answer: answer, hint: hint };
  }

  MindSkillsGame.play({
    totalQuestions: 10,
    lives: 3,
    round: function (ctx) {
      const q = gen(ctx.difficulty);
      ctx.stage.innerHTML =
        '<div class="prompt-sub">Yeching:</div>' +
        '<div class="question">' + q.text + " = ?</div>" +
        '<div class="answer-row">' +
        '<input type="text" inputmode="numeric" class="answer-input" id="ansIn" autocomplete="off" placeholder="?">' +
        '<button class="btn" id="ansBtn">→</button>' +
        "</div>";

      const input = ctx.stage.querySelector("#ansIn");
      input.focus();
      const hintTimer = setTimeout(() => ctx.showHint(q.hint), 9000);

      function submit() {
        clearTimeout(hintTimer);
        const val = input.value.trim().replace(/\s/g, "");
        if (val === "") { input.focus(); return; }
        ctx.answer({
          isCorrect: Number(val) === q.answer,
          prompt: q.text,
          correctAnswer: q.answer,
          userAnswer: val,
        });
      }
      ctx.stage.querySelector("#ansBtn").addEventListener("click", submit);
      input.addEventListener("keydown", (e) => { if (e.key === "Enter") submit(); });
    },
  });
})();

/* ============================================================
   MindSkills — umumiy o'yin dvigateli (engine)
   Har bir o'yin `MindSkillsGame.play({...})` ni chaqiradi va faqat
   bitta `round(ctx)` funksiyasini taqdim etadi. Dvigatel HUD, taymer,
   adaptiv qiyinlik, ball, jonlar va natijani serverga yuborishni boshqaradi.
   ============================================================ */
window.MindSkillsGame = (function () {
  "use strict";

  function $(id) { return document.getElementById(id); }

  function getCsrf(root) {
    const el = root.querySelector('[name="csrfmiddlewaretoken"]');
    return el ? el.value : "";
  }

  function play(opts) {
    const root = $("gameRoot");
    if (!root) return;

    const cfg = {
      slug: root.dataset.slug,
      submitUrl: root.dataset.submitUrl,
      maxDiff: parseInt(root.dataset.maxDiff, 10) || 12,
      startDiff: parseInt(root.dataset.startDiff, 10) || 1,
    };
    const totalQuestions = opts.totalQuestions || 10;
    const maxLives = opts.lives == null ? 3 : opts.lives;

    // DOM
    const intro = $("introScreen");
    const playScreen = $("playScreen");
    const resultScreen = $("resultScreen");
    const gameArea = $("gameArea");
    const feedback = $("feedback");
    const hintBox = $("hintBox");
    const adaptiveBar = $("adaptiveBar");
    const adaptiveMsg = $("adaptiveMsg");
    const timerRing = $("timerRing");
    const timerBar = $("timerBar");
    const timerText = $("timerText");

    const hud = {
      score: $("hudScore"),
      q: $("hudQ"),
      diff: $("hudDiff"),
      lives: $("hudLives"),
    };

    // Holat
    let state;
    let timerId = null;

    function resetState() {
      state = {
        difficulty: cfg.startDiff,
        index: 0,
        score: 0,
        lives: maxLives,
        attempts: [],
        startedAt: Date.now(),
        roundStart: 0,
        locked: false,
      };
    }

    function renderHud() {
      hud.score.textContent = state.score;
      hud.q.textContent = state.index + "/" + totalQuestions;
      hud.diff.textContent = state.difficulty;
      if (maxLives > 0) {
        hud.lives.textContent = "❤️".repeat(state.lives) + "🖤".repeat(Math.max(0, maxLives - state.lives));
      } else {
        hud.lives.textContent = "∞";
      }
    }

    function showAdaptive(direction, msg) {
      if (!msg) { adaptiveBar.classList.add("hidden"); return; }
      adaptiveBar.classList.remove("hidden", "up", "down");
      if (direction === "up") adaptiveBar.classList.add("up");
      if (direction === "down") adaptiveBar.classList.add("down");
      adaptiveMsg.textContent = msg;
    }

    function showHint(text) {
      if (!text) { hintBox.classList.add("hidden"); return; }
      hintBox.classList.remove("hidden");
      hintBox.textContent = "💡 " + text;
    }

    // --- Taymer (ixtiyoriy) ---
    function startTimer(seconds, onExpire) {
      stopTimer();
      timerRing.classList.remove("hidden");
      const C = 144.5; // 2πr (r=23)
      let remaining = seconds;
      timerText.textContent = remaining;
      timerBar.style.strokeDashoffset = "0";
      const t0 = Date.now();
      timerId = setInterval(() => {
        const elapsed = (Date.now() - t0) / 1000;
        const frac = Math.min(1, elapsed / seconds);
        timerBar.style.strokeDashoffset = (C * frac).toFixed(1);
        const left = Math.ceil(seconds - elapsed);
        if (left !== remaining) { remaining = left; timerText.textContent = Math.max(0, left); }
        if (elapsed >= seconds) { stopTimer(); onExpire && onExpire(); }
      }, 80);
    }
    function stopTimer() {
      if (timerId) { clearInterval(timerId); timerId = null; }
      timerRing.classList.add("hidden");
    }

    // --- Bitta savol ---
    function nextRound() {
      if (state.index >= totalQuestions || (maxLives > 0 && state.lives <= 0)) {
        return finish();
      }
      state.index++;
      state.locked = false;
      state.roundStart = Date.now();
      feedback.textContent = "";
      feedback.className = "feedback";
      gameArea.innerHTML = "";
      renderHud();

      const ctx = {
        difficulty: state.difficulty,
        index: state.index,
        total: totalQuestions,
        stage: gameArea,
        startTimer: startTimer,
        stopTimer: stopTimer,
        showHint: showHint,
        answer: handleAnswer,
      };
      // O'yinning o'z mantig'i
      opts.round(ctx);
    }

    function handleAnswer(result) {
      if (state.locked) return;
      state.locked = true;
      stopTimer();
      showHint("");

      const timeMs = result.timeMs != null ? result.timeMs : Date.now() - state.roundStart;
      const isCorrect = !!result.isCorrect;

      state.attempts.push({
        isCorrect: isCorrect,
        time_ms: timeMs,
        timeMs: timeMs,
        difficulty: state.difficulty,
        prompt: String(result.prompt || ""),
        correct_answer: String(result.correctAnswer == null ? "" : result.correctAnswer),
        user_answer: String(result.userAnswer == null ? "" : result.userAnswer),
      });

      if (isCorrect) {
        state.score += 10 * state.difficulty;
        feedback.textContent = pick(["To'g'ri! ✅", "Zo'r! 🎉", "Aniq javob! 👏", "Ajoyib! ⭐"]);
        feedback.className = "feedback ok";
      } else {
        if (maxLives > 0) state.lives--;
        feedback.textContent = result.correctAnswer != null
          ? "To'g'ri javob: " + result.correctAnswer + " ❌"
          : "Xato ❌";
        feedback.className = "feedback no";
      }
      renderHud();

      // Adaptiv baholash
      const decision = window.Adaptive.evaluate(state.difficulty, state.attempts, cfg.maxDiff);
      const changed = decision.difficulty !== state.difficulty;
      state.difficulty = decision.difficulty;
      if (changed) showAdaptive(decision.direction, decision.reason);
      else showAdaptive(null, "");

      // Keyingi savolga o'tish
      const delay = isCorrect ? 750 : 1300;
      setTimeout(nextRound, delay);
    }

    // --- Yakun ---
    function finish() {
      stopTimer();
      const duration = Math.round((Date.now() - state.startedAt) / 1000);
      const correct = state.attempts.filter((a) => a.isCorrect).length;
      const total = state.attempts.length || 1;
      const acc = Math.round((correct / total) * 100);

      playScreen.classList.add("hidden");
      resultScreen.classList.remove("hidden");
      showAdaptive(null, "");

      $("resultTrophy").textContent = acc >= 80 ? "🏆" : acc >= 50 ? "🌟" : "💪";
      $("resultTitle").textContent = acc >= 80 ? "Ajoyib natija!" : acc >= 50 ? "Yaxshi ish!" : "Mashq qilamiz!";
      $("rScore").textContent = state.score;
      $("rAcc").textContent = acc + "%";
      $("rDiff").textContent = state.difficulty;
      $("resultCoins").textContent = "...";

      // Serverga yuborish
      fetch(cfg.submitUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json", "X-CSRFToken": getCsrf(root) },
        body: JSON.stringify({
          attempts: state.attempts.map((a) => ({
            is_correct: a.isCorrect,
            difficulty: a.difficulty,
            time_ms: a.time_ms,
            prompt: a.prompt,
            correct_answer: a.correct_answer,
            user_answer: a.user_answer,
          })),
          duration_seconds: duration,
          difficulty_start: cfg.startDiff,
        }),
      })
        .then((r) => r.json())
        .then((data) => {
          if (!data.ok) { $("resultCoins").textContent = data.reason || "Saqlashda xato"; return; }
          $("resultCoins").textContent = "+" + data.coins_earned + " 🪙";
          $("rDiff").textContent = data.new_difficulty;
          // Navbardagi tangani yangilash
          const coinEl = document.querySelector(".avatar-chip .coins");
          if (coinEl) coinEl.textContent = "🪙 " + data.total_coins;
          // Yangi yutuqlar
          if (data.achievements && data.achievements.length) {
            const box = $("earnedBadges");
            box.classList.remove("hidden");
            box.innerHTML = data.achievements
              .map((b) => '<span class="earned-badge">' + b.icon + " " + b.title + " +" + b.coins + "🪙</span>")
              .join("");
          }
        })
        .catch(() => { $("resultCoins").textContent = "Tarmoq xatosi"; });
    }

    function pick(arr) { return arr[Math.floor(Math.random() * arr.length)]; }

    function begin() {
      resetState();
      intro.classList.add("hidden");
      resultScreen.classList.add("hidden");
      playScreen.classList.remove("hidden");
      renderHud();
      nextRound();
    }

    // Tugmalarni ulash
    const startBtn = $("startBtn");
    if (startBtn) startBtn.addEventListener("click", begin);
    const replayBtn = $("replayBtn");
    if (replayBtn) replayBtn.addEventListener("click", begin);

    // Tashqi yordamchilar (o'yin JS uchun)
    return { begin: begin, pick: pick };
  }

  // Umumiy yordamchilar
  function randInt(min, max) { return Math.floor(Math.random() * (max - min + 1)) + min; }
  function shuffle(arr) {
    for (let i = arr.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [arr[i], arr[j]] = [arr[j], arr[i]];
    }
    return arr;
  }

  return { play: play, randInt: randInt, shuffle: shuffle };
})();

/* ============================================================
   Adaptiv qiyinlik tizimi (mijoz tomoni)
   Server tomonidagi games/adaptive.py bilan bir xil mantiq.
   ============================================================ */
window.Adaptive = (function () {
  "use strict";

  const MIN = 1;
  const MAX = 12;
  const PROMOTE_STREAK = 3; // ketma-ket to'g'ri javob → daraja oshadi
  const DEMOTE_STREAK = 2; // ketma-ket xato → daraja tushadi
  const SLOW_MS = 12000; // bundan sekin javob "qiynalish"

  function clamp(v, hi) {
    return Math.max(MIN, Math.min(hi || MAX, v));
  }

  /**
   * attempts: [{isCorrect:Bool, timeMs:Number}, ...] (eski→yangi)
   * Qaytaradi: {difficulty, direction:'up'|'down'|'hold', hint:Bool, reason}
   */
  function evaluate(current, attempts, maxDiff) {
    const max = maxDiff || MAX;
    let diff = clamp(current, max);
    if (!attempts.length) {
      return { difficulty: diff, direction: "hold", hint: false, reason: "" };
    }

    let correctRun = 0;
    let wrongRun = 0;
    for (let i = attempts.length - 1; i >= 0; i--) {
      const a = attempts[i];
      if (a.isCorrect && wrongRun === 0) correctRun++;
      else if (!a.isCorrect && correctRun === 0) wrongRun++;
      else break;
    }

    const last = attempts[attempts.length - 1];
    const slow = (last.timeMs || 0) >= SLOW_MS;

    if (correctRun >= PROMOTE_STREAK && diff < max) {
      return {
        difficulty: clamp(diff + 1, max),
        direction: "up",
        hint: false,
        reason: correctRun + " ta ketma-ket to'g'ri — daraja oshdi! 📈",
      };
    }
    if (wrongRun >= DEMOTE_STREAK || (!last.isCorrect && slow)) {
      return {
        difficulty: clamp(diff - 1, max),
        direction: "down",
        hint: true,
        reason: "Sekinroq olamiz — daraja pasaytirildi, yordam beramiz 💡",
      };
    }
    return { difficulty: diff, direction: "hold", hint: false, reason: "" };
  }

  return { evaluate: evaluate, clamp: clamp, MIN: MIN, MAX: MAX };
})();

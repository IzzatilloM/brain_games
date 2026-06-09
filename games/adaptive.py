"""
Adaptiv qiyinlik tizimi (adaptive learning algoritmi).

Tizim bolaning har bir topshiriqqa sarflagan vaqtini va to'g'ri javoblar
foizini tahlil qiladi:

* Agar bola ketma-ket 3 ta topshiriqni to'g'ri bajarsa — qiyinlik darajasi
  avtomatik bir pog'ona oshadi.
* Agar bola qiynalsa (ketma-ket 2 xato yoki javob vaqti juda cho'zilsa) —
  daraja pasayadi va tizim yordam (ko'rsatma) berishni tavsiya qiladi.

Bir xil mantiq mijoz tomonida (`static/js/adaptive.js`) ham takrorlanadi, shunda
o'yin davomida qiyinlik real vaqtda o'zgaradi; bu yerdagi server mantiqi esa
sessiyalar orasida darajani saqlab boradi.
"""

from dataclasses import dataclass

MIN_DIFFICULTY = 1
MAX_DIFFICULTY = 12

# Ketma-ket nechta to'g'ri javobdan keyin daraja oshadi
PROMOTE_STREAK = 3
# Ketma-ket nechta xatodan keyin daraja tushadi
DEMOTE_STREAK = 2
# Javob bu chegaradan sekin bo'lsa "qiynalish" deb hisoblanadi (ms)
SLOW_ANSWER_MS = 12_000


@dataclass
class AdaptiveDecision:
    difficulty: int
    direction: str  # "up" | "down" | "hold"
    hint_recommended: bool
    reason: str


def clamp(value: int, low: int = MIN_DIFFICULTY, high: int = MAX_DIFFICULTY) -> int:
    return max(low, min(high, value))


def evaluate(current_difficulty: int, attempts, max_difficulty: int = MAX_DIFFICULTY) -> AdaptiveDecision:
    """
    `attempts` — sessiyadagi urinishlar ketma-ketligi (eng eski → eng yangi).
    Har bir element `is_correct` (bool) va `time_ms` (int) atributlariga ega
    bo'lishi kerak (Attempt obyekti yoki shunga o'xshash dataklass).
    """
    difficulty = clamp(current_difficulty, high=max_difficulty)
    if not attempts:
        return AdaptiveDecision(difficulty, "hold", False, "Ma'lumot yetarli emas")

    # Oxiridan boshlab ketma-ket to'g'ri / xato sonini hisoblaymiz
    correct_run = 0
    wrong_run = 0
    for attempt in reversed(attempts):
        if attempt.is_correct and wrong_run == 0:
            correct_run += 1
        elif not attempt.is_correct and correct_run == 0:
            wrong_run += 1
        else:
            break

    last = attempts[-1]
    slow = getattr(last, "time_ms", 0) >= SLOW_ANSWER_MS

    # 3 ta ketma-ket to'g'ri → daraja oshadi
    if correct_run >= PROMOTE_STREAK and difficulty < max_difficulty:
        return AdaptiveDecision(
            clamp(difficulty + 1, high=max_difficulty),
            "up",
            False,
            f"{correct_run} ta ketma-ket to'g'ri javob — daraja oshdi!",
        )

    # 2 ta ketma-ket xato yoki juda sekin javob → daraja pasayadi + yordam
    if wrong_run >= DEMOTE_STREAK or (not last.is_correct and slow):
        return AdaptiveDecision(
            clamp(difficulty - 1),
            "down",
            True,
            "Bola qiynaldi — daraja pasaytirildi va yordam ko'rsatiladi.",
        )

    return AdaptiveDecision(difficulty, "hold", False, "Daraja barqaror saqlanadi.")


def session_accuracy(attempts) -> int:
    if not attempts:
        return 0
    correct = sum(1 for a in attempts if a.is_correct)
    return round(correct / len(attempts) * 100)


def recommended_start_difficulty(progress, max_difficulty: int = MAX_DIFFICULTY) -> int:
    """
    Yangi sessiya uchun boshlang'ich darajani tavsiya qiladi: oldingi progress
    aniqligi past bo'lsa, biroz pasaytirib boshlaymiz.
    """
    base = clamp(progress.difficulty, high=max_difficulty)
    if progress.total_questions >= 10 and progress.accuracy < 50 and base > MIN_DIFFICULTY:
        return base - 1
    return base

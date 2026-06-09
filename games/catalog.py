"""O'yinlar katalogi — kategoriyalar, o'yinlar va fan testlari (savol banklari).

`kind` qaysi React komponenti o'ynashini belgilaydi.
"""

CATEGORIES = [
    {
        "slug": "mental", "name": "Mental arifmetika", "color": "#7c5cff",
        "grad": "linear-gradient(135deg,#a78bfa,#7c5cff)", "icon": "🧮",
        "tagline": "Sonlarni xayolan qo'shing va ayiring",
        "games": [
            {"slug": "flash", "name": "Flash kartalar", "icon": "🃏", "kind": "flash", "tagline": "Chaqnagan sonlar yig'indisi"},
            {"slug": "ustunlar", "name": "Ustunlar", "icon": "➕", "kind": "columns", "tagline": "Ustundagi sonlarni qo'shing"},
            {"slug": "forsaj", "name": "Forsaj", "icon": "🚀", "kind": "forsaj", "tagline": "Tezkor mental hisob"},
            {"slug": "kopaytirgich", "name": "Ko'paytirgich", "icon": "✖️", "kind": "kopaytir", "tagline": "Ko'paytirishni mashq qiling"},
            {"slug": "qoshish", "name": "Qo'shish", "icon": "➕", "kind": "quiz", "gen": "add", "tagline": "Tez qo'shish"},
            {"slug": "ayirish", "name": "Ayirish", "icon": "➖", "kind": "quiz", "gen": "sub", "tagline": "Tez ayirish"},
            {"slug": "bolish", "name": "Bo'lish", "icon": "➗", "kind": "quiz", "gen": "div", "tagline": "Tez bo'lish"},
        ],
    },
    {
        "slug": "xotira", "name": "Xotirani rivojlantirish", "color": "#19b5c9",
        "grad": "linear-gradient(135deg,#5eead4,#19b5c9)", "icon": "🧠",
        "tagline": "Eslab qolish va diqqatni mustahkamlang",
        "games": [
            {"slug": "juft-topish", "name": "Juft topish", "icon": "🃏", "kind": "memory", "tagline": "Bir xil kartalarni juftlang"},
            {"slug": "sonni-eslab", "name": "Sonni eslab qol", "icon": "🔢", "kind": "numrecall", "tagline": "Ko'rsatilgan sonni yodda saqlang"},
            {"slug": "uzun-son", "name": "Uzun son", "icon": "🧠", "kind": "numrecall", "tagline": "Tobora uzayuvchi sonlar"},
            {"slug": "rangli-juftlar", "name": "Rangli juftlar", "icon": "🎴", "kind": "memory", "tagline": "Juftlarni tez toping"},
        ],
    },
    {
        "slug": "tezoqish", "name": "Tez o'qish", "color": "#ef4d6b",
        "grad": "linear-gradient(135deg,#fb7185,#ef4d6b)", "icon": "📖",
        "tagline": "O'qish tezligi va idrokni oshiring",
        "games": [
            {"slug": "soz-chaqnashi", "name": "So'z chaqnashi", "icon": "⚡", "kind": "wordflash", "tagline": "Ko'rsatilgan so'zni tanlang"},
            {"slug": "harf-sanash", "name": "Harf sanash", "icon": "🔤", "kind": "lettercount", "tagline": "Harfni sanang"},
            {"slug": "soz-yomgiri", "name": "So'z yomg'iri", "icon": "🌧️", "kind": "wordflash", "tagline": "Tez chaqnagan so'zlar"},
            {"slug": "harf-ovi", "name": "Harf ovi", "icon": "🎯", "kind": "lettercount", "tagline": "Harflarni toping"},
        ],
    },
    {
        "slug": "diqqat", "name": "Diqqat", "color": "#22b07d",
        "grad": "linear-gradient(135deg,#4ade80,#22b07d)", "icon": "🎯",
        "tagline": "Diqqat va reaksiyani charxlang",
        "games": [
            {"slug": "schulte", "name": "Schulte jadvali", "icon": "🔢", "kind": "schulte", "tagline": "1-25 tartib bilan"},
            {"slug": "farqni-top", "name": "Farqni top", "icon": "🔎", "kind": "finddiff", "tagline": "Boshqacha belgini toping"},
            {"slug": "rang-soz", "name": "Rang-so'z", "icon": "🎨", "kind": "stroop", "tagline": "Yozilgan rangni tanlang"},
            {"slug": "tez-reaksiya", "name": "Tez reaksiya", "icon": "⚡", "kind": "reaction", "tagline": "Yashilda tez bosing"},
            {"slug": "eng-katta", "name": "Eng katta son", "icon": "🔝", "kind": "quiz", "gen": "max", "tagline": "Eng katta sonni toping"},
            {"slug": "keyingi-son", "name": "Keyingi son", "icon": "➡️", "kind": "quiz", "gen": "seq", "tagline": "Ketma-ketlikni davom eting"},
        ],
    },
    {
        "slug": "matematika", "name": "Matematika", "color": "#f5a623",
        "grad": "linear-gradient(135deg,#fcd34d,#f5a623)", "icon": "🔢",
        "tagline": "Maktab matematikasini o'yin orqali",
        "games": [
            {"slug": "hisoblash-tizimlari", "name": "Hisoblash tizimlari", "symbol": "5→2", "kind": "quiz", "gen": "base", "tagline": "Sanoq sistemalari"},
            {"slug": "darajalar", "name": "Darajalar, ildizlar va logarifmlar", "symbol": "³√8", "kind": "quiz", "gen": "power", "tagline": "Daraja va ildizlar"},
            {"slug": "ekub-ekuk", "name": "EKUB va EKUK", "symbol": "(m,n)", "kind": "quiz", "gen": "gcd", "tagline": "Bo'luvchilar"},
            {"slug": "kasrlar", "name": "Kasrlar", "symbol": "2⁄3", "kind": "quiz", "gen": "frac", "tagline": "Kasrlar ustida amallar"},
            {"slug": "foizlar", "name": "Foizlar", "symbol": "4%", "kind": "quiz", "gen": "percent", "tagline": "Foizlarni hisoblang"},
            {"slug": "matritsa", "name": "Matritsa", "symbol": "[1]", "kind": "quiz", "gen": "matrix", "tagline": "Matritsa elementlari"},
            {"slug": "ikkilantir", "name": "Ikkilantir", "symbol": "×2", "kind": "quiz", "gen": "double", "tagline": "Sonni ikkilantiring"},
            {"slug": "yarmini-top", "name": "Yarmini top", "symbol": "½", "kind": "quiz", "gen": "half", "tagline": "Sonning yarmi"},
            {"slug": "taqqoslash", "name": "Taqqoslash", "symbol": "⚖️", "kind": "quiz", "gen": "compare", "tagline": "Sonlarni solishtiring"},
            {"slug": "juft-toq", "name": "Juft yoki toq", "symbol": "½", "kind": "quiz", "gen": "eo", "tagline": "Juft yoki toq?"},
        ],
    },
]

# ============================================================
# BARCHA FANLAR — har fanda 4 ta aqliy test o'yini (savol banki)
# ============================================================
SUBJECTS = [
    {
        "slug": "fan-matematika", "name": "Matematika", "color": "#2b8af0", "icon": "🔢",
        "modes": ["Tezkor hisob", "Mantiqiy masala", "Geometriya", "Aralash"],
        "bank": [
            {"q": "7 × 8 = ?", "o": ["54", "56", "58", "64"], "a": 1},
            {"q": "144 ÷ 12 = ?", "o": ["11", "12", "13", "14"], "a": 1},
            {"q": "Uchburchak ichki burchaklari yig'indisi?", "o": ["90°", "180°", "270°", "360°"], "a": 1},
            {"q": "2, 4, 8, 16, … keyingi son?", "o": ["18", "24", "32", "20"], "a": 2},
            {"q": "Kvadratning nechta tomoni bor?", "o": ["3", "4", "5", "6"], "a": 1},
            {"q": "100 ning 25% i?", "o": ["20", "25", "40", "50"], "a": 1},
            {"q": "Eng kichik tub son?", "o": ["0", "1", "2", "3"], "a": 2},
            {"q": "(6 + 4) × 2 = ?", "o": ["16", "20", "14", "12"], "a": 1},
        ],
    },
    {
        "slug": "fan-ona-tili", "name": "Ona tili", "color": "#ef4d6b", "icon": "📖",
        "modes": ["So'z boyligi", "Grammatika", "Imlo", "Maqollar"],
        "bank": [
            {"q": "«Kitob» so'zining ko'pligi?", "o": ["Kitobchalar", "Kitoblar", "Kitobi", "Kitobcha"], "a": 1},
            {"q": "Qaysi so'z to'g'ri yozilgan?", "o": ["maktep", "maktab", "mektab", "maktap"], "a": 1},
            {"q": "«Tez» so'ziga zid ma'no?", "o": ["Sekin", "Baland", "Yaqin", "Issiq"], "a": 0},
            {"q": "Ot — bu …?", "o": ["Harakat", "Predmet nomi", "Belgi", "Son"], "a": 1},
            {"q": "«Mehnat — …ning ko'rki» maqolini to'ldiring", "o": ["yer", "el", "inson", "non"], "a": 2},
            {"q": "Qaysi so'z fe'l?", "o": ["Daraxt", "Yugurmoq", "Chiroyli", "Tez"], "a": 1},
            {"q": "«Bahor» qaysi fasl?", "o": ["Qish", "Yoz", "Bahor fasli", "Kuz"], "a": 2},
            {"q": "Sinonim juftlikni toping:", "o": ["Katta-kichik", "Aql-zakovat", "Oq-qora", "Issiq-sovuq"], "a": 1},
        ],
    },
    {
        "slug": "fan-ingliz", "name": "Ingliz tili", "color": "#7c5cff", "icon": "🔤",
        "modes": ["Vocabulary", "Grammar", "Translation", "Mixed"],
        "bank": [
            {"q": "«Olma» inglizcha?", "o": ["Orange", "Apple", "Banana", "Grape"], "a": 1},
            {"q": "«Cat» o'zbekcha?", "o": ["It", "Mushuk", "Sigir", "Quyon"], "a": 1},
            {"q": "I ___ a student.", "o": ["am", "is", "are", "be"], "a": 0},
            {"q": "«Maktab» inglizcha?", "o": ["House", "School", "Shop", "Park"], "a": 1},
            {"q": "Plural of «book»?", "o": ["books", "bookes", "bookies", "book"], "a": 0},
            {"q": "«Red» rangi?", "o": ["Ko'k", "Yashil", "Qizil", "Sariq"], "a": 2},
            {"q": "She ___ to school.", "o": ["go", "goes", "going", "gone"], "a": 1},
            {"q": "«Suv» inglizcha?", "o": ["Milk", "Water", "Juice", "Tea"], "a": 1},
        ],
    },
    {
        "slug": "fan-tabiat", "name": "Tabiatshunoslik", "color": "#22b07d", "icon": "🌿",
        "modes": ["Hayvonot", "O'simliklar", "Tana", "Tabiat hodisalari"],
        "bank": [
            {"q": "Quyosh — bu …?", "o": ["Sayyora", "Yulduz", "Yo'ldosh", "Kometa"], "a": 1},
            {"q": "O'simlik nafas oladigan gaz?", "o": ["Kislorod", "Karbonat angidrid", "Azot", "Vodorod"], "a": 1},
            {"q": "Inson yuragi nechta bo'lmaga ega?", "o": ["2", "3", "4", "5"], "a": 2},
            {"q": "Suv qaysi haroratda muzlaydi?", "o": ["0°C", "10°C", "100°C", "-10°C"], "a": 0},
            {"q": "Eng katta sayyora?", "o": ["Mars", "Yer", "Yupiter", "Venera"], "a": 2},
            {"q": "Asalarilar nima ishlab chiqaradi?", "o": ["Sut", "Asal", "Ipak", "Yog'"], "a": 1},
            {"q": "Baliq nima orqali nafas oladi?", "o": ["O'pka", "Jabra", "Teri", "Burun"], "a": 1},
            {"q": "Kamalakda nechta rang bor?", "o": ["5", "6", "7", "8"], "a": 2},
        ],
    },
    {
        "slug": "fan-geografiya", "name": "Geografiya", "color": "#19b5c9", "icon": "🌍",
        "modes": ["Materiklar", "Davlatlar", "Tabiat", "O'zbekiston"],
        "bank": [
            {"q": "O'zbekiston poytaxti?", "o": ["Samarqand", "Toshkent", "Buxoro", "Xiva"], "a": 1},
            {"q": "Eng katta okean?", "o": ["Atlantika", "Hind", "Tinch", "Shimoliy"], "a": 2},
            {"q": "Nechta materik bor?", "o": ["5", "6", "7", "8"], "a": 1},
            {"q": "Eng baland tog' cho'qqisi?", "o": ["Everest", "Tirich", "Pomir", "Olimp"], "a": 0},
            {"q": "O'zbekistondagi daryo?", "o": ["Nil", "Amudaryo", "Volga", "Tigr"], "a": 1},
            {"q": "Sahroyi Kabir qayerda?", "o": ["Osiyo", "Afrika", "Yevropa", "Amerika"], "a": 1},
            {"q": "Quyosh qayerdan chiqadi?", "o": ["G'arb", "Sharq", "Shimol", "Janub"], "a": 1},
            {"q": "Orol dengizi qayerda?", "o": ["Yevropa", "O'rta Osiyo", "Afrika", "Amerika"], "a": 1},
        ],
    },
    {
        "slug": "fan-tarix", "name": "Tarix", "color": "#f5a623", "icon": "🏛️",
        "modes": ["Qadimgi davr", "O'rta asrlar", "Yangi davr", "Aralash"],
        "bank": [
            {"q": "Amir Temur poytaxti?", "o": ["Toshkent", "Samarqand", "Buxoro", "Xiva"], "a": 1},
            {"q": "Mustaqillik kuni?", "o": ["1 sentyabr", "8 dekabr", "31 avgust", "9 may"], "a": 0},
            {"q": "Al-Xorazmiy qaysi fan asoschisi?", "o": ["Fizika", "Algebra", "Biologiya", "Kimyo"], "a": 1},
            {"q": "Buyuk ipak yo'li nimani bog'lagan?", "o": ["Sharq-G'arb", "Shimol-Janub", "Faqat Osiyo", "Faqat Yevropa"], "a": 0},
            {"q": "Registon maydoni qayerda?", "o": ["Toshkent", "Samarqand", "Buxoro", "Xiva"], "a": 1},
            {"q": "Birinchi yozuv qaysi xalqda?", "o": ["Shumerlar", "Yunonlar", "Rimliklar", "Misrliklar"], "a": 0},
            {"q": "Ibn Sino qaysi sohada mashhur?", "o": ["Tibbiyot", "Astronomiya", "Geografiya", "Tarix"], "a": 0},
            {"q": "Mustaqillik yili?", "o": ["1989", "1990", "1991", "1992"], "a": 2},
        ],
    },
    {
        "slug": "fan-mantiq", "name": "Mantiq", "color": "#ef6fa3", "icon": "🧩",
        "modes": ["Ketma-ketlik", "Analogiya", "Topishmoq", "Naqsh"],
        "bank": [
            {"q": "2, 4, 6, 8, … ?", "o": ["9", "10", "11", "12"], "a": 1},
            {"q": "Ortiqchasini toping:", "o": ["Olma", "Nok", "Sabzi", "Banan"], "a": 2},
            {"q": "Qush — qanot. Baliq — …?", "o": ["Oyoq", "Suzgich", "Quloq", "Dum"], "a": 1},
            {"q": "1, 1, 2, 3, 5, … (Fibonachchi)?", "o": ["6", "7", "8", "9"], "a": 2},
            {"q": "Otamning o'g'li, akam emas. Bu kim?", "o": ["Amaki", "O'zim", "Bobo", "Jiyan"], "a": 1},
            {"q": "◯ △ ◯ △ ◯ … ?", "o": ["◯", "△", "▢", "✕"], "a": 1},
            {"q": "81, 27, 9, … ?", "o": ["1", "3", "6", "9"], "a": 1},
            {"q": "Kun — Quyosh. Tun — …?", "o": ["Yulduz", "Oy", "Bulut", "Shamol"], "a": 1},
        ],
    },
    {
        "slug": "fan-informatika", "name": "Informatika", "color": "#5b6cff", "icon": "💻",
        "modes": ["Asoslar", "Internet", "Algoritm", "Aralash"],
        "bank": [
            {"q": "Kompyuter «miyasi»?", "o": ["Monitor", "Protsessor", "Klaviatura", "Sichqoncha"], "a": 1},
            {"q": "1 baytda nechta bit bor?", "o": ["4", "8", "16", "32"], "a": 1},
            {"q": "WWW nimaning qisqartmasi?", "o": ["World Wide Web", "Web Work World", "Wide World Web", "World Web Wide"], "a": 0},
            {"q": "Faylni saqlash tugmasi?", "o": ["Ctrl+S", "Ctrl+C", "Ctrl+V", "Ctrl+Z"], "a": 0},
            {"q": "Internet — bu …?", "o": ["Bitta kompyuter", "Tarmoqlar tarmog'i", "Dastur", "O'yin"], "a": 1},
            {"q": "Algoritm nima?", "o": ["Rasm", "Amallar ketma-ketligi", "Fayl", "Tugma"], "a": 1},
            {"q": "Sichqoncha nima uchun?", "o": ["Yozish", "Boshqarish", "Chop etish", "Eshitish"], "a": 1},
            {"q": "Eng kichik xotira birligi?", "o": ["Bayt", "Bit", "Kilobayt", "Megabayt"], "a": 1},
        ],
    },
]


LOC_NAMES = {
    "mental": {"ru": "Ментальная арифметика", "en": "Mental arithmetic"},
    "xotira": {"ru": "Развитие памяти", "en": "Memory development"},
    "tezoqish": {"ru": "Скорочтение", "en": "Speed reading"},
    "diqqat": {"ru": "Внимание", "en": "Attention"},
    "matematika": {"ru": "Математика", "en": "Mathematics"},
    "fan-matematika": {"ru": "Математика", "en": "Mathematics"},
    "fan-ona-tili": {"ru": "Родной язык", "en": "Native language"},
    "fan-ingliz": {"ru": "Английский язык", "en": "English"},
    "fan-tabiat": {"ru": "Природоведение", "en": "Natural science"},
    "fan-geografiya": {"ru": "География", "en": "Geography"},
    "fan-tarix": {"ru": "История", "en": "History"},
    "fan-mantiq": {"ru": "Логика", "en": "Logic"},
    "fan-informatika": {"ru": "Информатика", "en": "Computer science"},
}


def loc_name(slug, name_uz, lang):
    if lang == "uz":
        return name_uz
    return LOC_NAMES.get(slug, {}).get(lang, name_uz)


def categories_loc(lang):
    out = []
    for c in CATEGORIES:
        d = dict(c)
        d["name"] = loc_name(c["slug"], c["name"], lang)
        d["count"] = len(c["games"])
        out.append(d)
    return out


def subjects_loc(lang):
    out = []
    for s in SUBJECTS:
        d = dict(s)
        d["name"] = loc_name(s["slug"], s["name"], lang)
        d["count"] = len(s["modes"])
        out.append(d)
    return out


def all_games():
    out = []
    for cat in CATEGORIES:
        for g in cat["games"]:
            item = dict(g)
            item.update({"category": cat["slug"], "category_name": cat["name"], "color": cat["color"]})
            out.append(item)
    return out


def subject_games():
    out = []
    for sub in SUBJECTS:
        for i, mode in enumerate(sub["modes"], start=1):
            out.append({
                "slug": f"{sub['slug']}-{i}", "name": mode, "kind": "subjectquiz",
                "category": sub["slug"], "category_name": sub["name"],
                "color": sub["color"], "icon": sub["icon"], "tagline": f"{sub['name']} — {mode}",
                "questions": sub["bank"],
            })
    return out


def get_category(slug):
    return next((c for c in CATEGORIES if c["slug"] == slug), None)


def get_subject(slug):
    return next((s for s in SUBJECTS if s["slug"] == slug), None)


def get_game(slug):
    for g in all_games():
        if g["slug"] == slug:
            return g
    for g in subject_games():
        if g["slug"] == slug:
            return g
    return None


def siblings_of(slug):
    """O'sha kategoriya/fan ichidagi o'yinlar ro'yxati (slug+name)."""
    g = get_game(slug)
    if not g:
        return []
    pool = all_games() + subject_games()
    return [{"slug": x["slug"], "name": x["name"]} for x in pool if x["category"] == g["category"]]

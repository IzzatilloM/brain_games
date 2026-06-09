# -*- coding: utf-8 -*-
"""Yengil ko'p tillilik tizimi (uz / ru / en).

gettext'siz, sof Python lug'at asosida — Windows va PythonAnywhere'da
hech qanday qo'shimcha vositasiz ishlaydi.
"""

LANGS = [
    ("uz", "O'zbek tili", "UZ"),
    ("ru", "Русский", "RU"),
    ("en", "English", "EN"),
]
LANG_CODES = [c for c, _, _ in LANGS]
DEFAULT_LANG = "uz"

STRINGS = {
    # --- Umumiy ---
    "brand": {"uz": "MindSkills", "ru": "MindSkills", "en": "MindSkills"},
    "days": {"uz": "kun", "ru": "дн.", "en": "days"},
    "minutes": {"uz": "daqiqa", "ru": "минут", "en": "minutes"},
    "min_short": {"uz": "daq", "ru": "мин", "en": "min"},
    "save": {"uz": "Saqlash", "ru": "Сохранить", "en": "Save"},
    "cancel": {"uz": "Bekor qilish", "ru": "Отмена", "en": "Cancel"},
    "back": {"uz": "Orqaga", "ru": "Назад", "en": "Back"},
    "loading": {"uz": "Yuklanmoqda...", "ru": "Загрузка...", "en": "Loading..."},
    "all": {"uz": "Barchasi", "ru": "Все", "en": "All"},
    "level": {"uz": "Daraja", "ru": "Уровень", "en": "Level"},
    "coins": {"uz": "Tangalar", "ru": "Монеты", "en": "Coins"},
    "accuracy": {"uz": "Aniqlik", "ru": "Точность", "en": "Accuracy"},
    "sessions": {"uz": "Sessiyalar", "ru": "Сессии", "en": "Sessions"},
    "score": {"uz": "Ball", "ru": "Очки", "en": "Score"},

    # --- Navbar / sidebar ---
    "nav.new_design": {"uz": "Yangi dizayn", "ru": "Новый дизайн", "en": "New design"},
    "nav.home": {"uz": "Bosh", "ru": "Главная", "en": "Home"},
    "nav.tasks": {"uz": "Vazifalar", "ru": "Задания", "en": "Tasks"},
    "nav.multiplayer": {"uz": "Multipleyer", "ru": "Мультиплеер", "en": "Multiplayer"},
    "nav.games": {"uz": "O'yinlar", "ru": "Игры", "en": "Games"},
    "nav.rating": {"uz": "Reyting", "ru": "Рейтинг", "en": "Rating"},
    "nav.help": {"uz": "Yordam", "ru": "Помощь", "en": "Help"},
    "nav.profile": {"uz": "Profil", "ru": "Профиль", "en": "Profile"},
    "nav.parent": {"uz": "Ota-ona nazorati", "ru": "Родительский контроль", "en": "Parental control"},
    "nav.logout": {"uz": "Chiqish", "ru": "Выйти", "en": "Logout"},
    "nav.login": {"uz": "Kirish", "ru": "Войти", "en": "Login"},
    "nav.register": {"uz": "Ro'yxatdan o'tish", "ru": "Регистрация", "en": "Sign up"},
    "section.lesson": {"uz": "Darsga", "ru": "Учёба", "en": "Lesson"},
    "section.students": {"uz": "O'quvchilar", "ru": "Ученики", "en": "Students"},
    "section.other": {"uz": "Har xil", "ru": "Разное", "en": "Other"},
    "section.parents": {"uz": "Ota-onalar", "ru": "Родители", "en": "Parents"},

    # --- Home (o'quvchi) ---
    "home.greeting": {"uz": "Salom", "ru": "Привет", "en": "Hello"},
    "home.welcome_sub": {"uz": "Bugun nimani o'rganamiz?", "ru": "Что изучим сегодня?", "en": "What shall we learn today?"},
    "home.btn.games": {"uz": "O'yinlar", "ru": "Игры", "en": "Games"},
    "home.btn.homework": {"uz": "Uy vazifalari", "ru": "Домашние задания", "en": "Homework"},
    "home.btn.rating": {"uz": "Reyting", "ru": "Рейтинг", "en": "Rating"},
    "home.btn.multiplayer": {"uz": "Multipleyer", "ru": "Мультиплеер", "en": "Multiplayer"},
    "home.btn.profile": {"uz": "Profil", "ru": "Профиль", "en": "Profile"},
    "home.btn.stats": {"uz": "Statistika", "ru": "Статистика", "en": "Statistics"},
    "home.continue": {"uz": "Davom etish", "ru": "Продолжить", "en": "Continue"},
    "home.today": {"uz": "Bugun", "ru": "Сегодня", "en": "Today"},
    "home.streak": {"uz": "Ketma-ket kun", "ru": "Дней подряд", "en": "Day streak"},

    # --- Games ---
    "games.title": {"uz": "O'yinlar", "ru": "Игры", "en": "Games"},
    "games.subtitle": {"uz": "Aqlni charxlovchi o'yinlar to'plami", "ru": "Набор игр для тренировки ума", "en": "A collection of brain-training games"},
    "games.multiplayer": {"uz": "Multipleyer", "ru": "Мультиплеер", "en": "Multiplayer"},
    "games.play": {"uz": "O'ynash", "ru": "Играть", "en": "Play"},
    "games.start": {"uz": "Boshlamoq", "ru": "Начать", "en": "Start"},
    "games.check": {"uz": "Tekshirish", "ru": "Проверить", "en": "Check"},
    "games.answer": {"uz": "Javob", "ru": "Ответ", "en": "Answer"},
    "games.stop": {"uz": "Stop", "ru": "Стоп", "en": "Stop"},
    "games.next": {"uz": "Keyingi", "ru": "Дальше", "en": "Next"},
    "games.locked": {"uz": "Bloklangan", "ru": "Заблокировано", "en": "Locked"},
    "games.choose_mode": {"uz": "Rejimni tanlang", "ru": "Выберите режим", "en": "Choose a mode"},
    "games.result": {"uz": "Natija", "ru": "Результат", "en": "Result"},
    "games.replay": {"uz": "Yana o'ynash", "ru": "Играть снова", "en": "Play again"},
    "games.seconds": {"uz": "soniya", "ru": "секунд", "en": "seconds"},
    "games.watch": {"uz": "Diqqat bilan kuzating", "ru": "Внимательно следите", "en": "Watch carefully"},
    "games.your_turn": {"uz": "Endi siz!", "ru": "Теперь вы!", "en": "Your turn!"},

    # --- Settings panel (in-game) ---
    "set.module": {"uz": "Modul", "ru": "Модуль", "en": "Module"},
    "set.operations": {"uz": "Operatsiyalar", "ru": "Операции", "en": "Operations"},
    "set.digit": {"uz": "Raqam", "ru": "Разряд", "en": "Digit"},
    "set.rows": {"uz": "Qatorlar", "ru": "Строки", "en": "Rows"},
    "set.interval": {"uz": "Interval", "ru": "Интервал", "en": "Interval"},
    "set.limit": {"uz": "Limit", "ru": "Лимит", "en": "Limit"},
    "set.no_limit": {"uz": "Cheklov yo'q", "ru": "Без лимита", "en": "No limit"},
    "set.level_mode": {"uz": "Darajalar rejimi", "ru": "Режим уровней", "en": "Level mode"},
    "set.all_levels": {"uz": "Barcha darajalar", "ru": "Все уровни", "en": "All levels"},
    "set.adaptive": {"uz": "Adaptiv rejim", "ru": "Адаптивный режим", "en": "Adaptive mode"},
    "set.sound": {"uz": "Ovoz", "ru": "Звук", "en": "Sound"},

    # --- Rating ---
    "rating.title": {"uz": "Reyting", "ru": "Рейтинг", "en": "Rating"},
    "rating.subtitle": {"uz": "Eng faol o'yinchilar", "ru": "Самые активные игроки", "en": "Top players"},
    "rating.rank": {"uz": "O'rin", "ru": "Место", "en": "Rank"},
    "rating.player": {"uz": "O'yinchi", "ru": "Игрок", "en": "Player"},
    "rating.you": {"uz": "Siz", "ru": "Вы", "en": "You"},
    "rating.week": {"uz": "Hafta", "ru": "Неделя", "en": "Week"},
    "rating.alltime": {"uz": "Umumiy", "ru": "За всё время", "en": "All time"},

    # --- Profile ---
    "profile.title": {"uz": "Profil", "ru": "Профиль", "en": "Profile"},
    "profile.edit": {"uz": "Profilni tahrirlash", "ru": "Редактировать профиль", "en": "Edit profile"},
    "profile.photo": {"uz": "Profil rasmi", "ru": "Фото профиля", "en": "Profile photo"},
    "profile.upload": {"uz": "Rasm yuklash", "ru": "Загрузить фото", "en": "Upload photo"},
    "profile.change_photo": {"uz": "Rasmni o'zgartirish", "ru": "Изменить фото", "en": "Change photo"},
    "profile.fullname": {"uz": "To'liq ism", "ru": "Полное имя", "en": "Full name"},
    "profile.grade": {"uz": "Sinf", "ru": "Класс", "en": "Grade"},
    "profile.birth": {"uz": "Tug'ilgan sana", "ru": "Дата рождения", "en": "Date of birth"},
    "profile.account": {"uz": "Hisob ma'lumotlari", "ru": "Данные аккаунта", "en": "Account info"},
    "profile.achievements": {"uz": "Yutuqlar", "ru": "Достижения", "en": "Achievements"},
    "profile.stats": {"uz": "Statistika", "ru": "Статистика", "en": "Statistics"},
    "profile.saved": {"uz": "Profil saqlandi", "ru": "Профиль сохранён", "en": "Profile saved"},

    # --- Parent ---
    "parent.title": {"uz": "Ota-ona nazorati", "ru": "Родительский контроль", "en": "Parental control"},
    "parent.children": {"uz": "Farzandlar", "ru": "Дети", "en": "Children"},
    "parent.add_child": {"uz": "Farzand qo'shish", "ru": "Добавить ребёнка", "en": "Add child"},
    "parent.daily_limit": {"uz": "Kunlik vaqt chegarasi", "ru": "Дневной лимит", "en": "Daily time limit"},
    "parent.bedtime": {"uz": "Tunlik bloklash", "ru": "Ночная блокировка", "en": "Bedtime block"},
    "parent.max_diff": {"uz": "Maksimal qiyinlik", "ru": "Макс. сложность", "en": "Max difficulty"},
    "parent.allowed_games": {"uz": "Ruxsat etilgan o'yinlar", "ru": "Разрешённые игры", "en": "Allowed games"},
    "parent.block": {"uz": "Hisobni bloklash", "ru": "Заблокировать аккаунт", "en": "Block account"},
    "parent.report": {"uz": "Hisobot", "ru": "Отчёт", "en": "Report"},
    "parent.manage": {"uz": "Boshqarish", "ru": "Управление", "en": "Manage"},
    "parent.saved": {"uz": "Sozlamalar saqlandi", "ru": "Настройки сохранены", "en": "Settings saved"},

    # --- Auth ---
    "auth.login_title": {"uz": "Hisobga kirish", "ru": "Вход в аккаунт", "en": "Sign in"},
    "auth.login_sub": {"uz": "Login va parolingizni kiriting", "ru": "Введите логин и пароль", "en": "Enter your login and password"},
    "auth.register_title": {"uz": "Ro'yxatdan o'tish", "ru": "Регистрация", "en": "Sign up"},
    "auth.register_sub": {"uz": "Bir necha qadamda hisob yarating", "ru": "Создайте аккаунт за пару шагов", "en": "Create an account in a few steps"},
    "auth.username": {"uz": "Login", "ru": "Логин", "en": "Login"},
    "auth.password": {"uz": "Parol", "ru": "Пароль", "en": "Password"},
    "auth.password2": {"uz": "Parolni tasdiqlang", "ru": "Подтвердите пароль", "en": "Confirm password"},
    "auth.no_account": {"uz": "Hisobingiz yo'qmi?", "ru": "Нет аккаунта?", "en": "No account?"},
    "auth.have_account": {"uz": "Hisobingiz bormi?", "ru": "Уже есть аккаунт?", "en": "Have an account?"},
    "auth.role_q": {"uz": "Kim sifatida ro'yxatdan o'tasiz?", "ru": "Кто вы?", "en": "Who are you?"},
    "auth.as_parent": {"uz": "Ota-ona", "ru": "Родитель", "en": "Parent"},
    "auth.as_child": {"uz": "O'quvchi", "ru": "Ученик", "en": "Student"},

    # --- Landing ---
    "land.hero_badge": {"uz": "Adaptiv ta'lim platformasi", "ru": "Платформа адаптивного обучения", "en": "Adaptive learning platform"},
    "land.hero_title": {"uz": "Bolangiz aqlini o'yin orqali charxlang", "ru": "Развивайте ум ребёнка через игру", "en": "Sharpen your child's mind through play"},
    "land.hero_sub": {"uz": "Mental arifmetika, abakus va tez o'qish — barchasi bitta platformada.", "ru": "Ментальная арифметика, абакус и скорочтение — всё на одной платформе.", "en": "Mental arithmetic, abacus and speed reading — all in one platform."},
    "land.start_free": {"uz": "Bepul boshlash", "ru": "Начать бесплатно", "en": "Start free"},
    "land.learn_more": {"uz": "Batafsil", "ru": "Подробнее", "en": "Learn more"},

    # --- Qo'shimcha (BrainGames) ---
    "nav.subjects": {"uz": "Barcha fanlar", "ru": "Все предметы", "en": "All subjects"},
    "nav.stats": {"uz": "Statistika", "ru": "Статистика", "en": "Statistics"},
    "footer.terms": {"uz": "Foydalanuvchi shartnomasi", "ru": "Пользовательское соглашение", "en": "Terms of use"},
    "footer.offer": {"uz": "Oferta shartnomasi", "ru": "Договор оферты", "en": "Offer agreement"},
    "home.categories": {"uz": "Kategoriyalar", "ru": "Категории", "en": "Categories"},
    "home.next_level": {"uz": "Keyingi darajagacha", "ru": "До следующего уровня", "en": "To next level"},
    "home.day_streak": {"uz": "kun ketma-ket", "ru": "дней подряд", "en": "day streak"},
    "common.games": {"uz": "O'yin", "ru": "игр", "en": "games"},
    "common.coin": {"uz": "Tanga", "ru": "Монеты", "en": "Coins"},
    "common.star": {"uz": "Yulduz", "ru": "Звёзды", "en": "Stars"},
    "common.level": {"uz": "daraja", "ru": "уровень", "en": "level"},
    "subjects.title": {"uz": "Barcha fanlar", "ru": "Все предметы", "en": "All subjects"},
    "subjects.sub": {"uz": "Har bir fan ichida aqlni charxlaydigan 4 ta test bor.", "ru": "В каждом предмете 4 теста для тренировки ума.", "en": "Each subject has 4 brain-training tests."},
    "subjects.test": {"uz": "ta test", "ru": "тестов", "en": "tests"},
    "subjects.brain": {"uz": "Aqliy test", "ru": "Тест на ум", "en": "Brain test"},
    "stats.title": {"uz": "Statistika", "ru": "Статистика", "en": "Statistics"},
    "stats.weekly": {"uz": "Haftalik XP", "ru": "XP за неделю", "en": "Weekly XP"},
    "stats.total_games": {"uz": "Jami o'yinlar", "ru": "Всего игр", "en": "Total games"},
    "stats.best": {"uz": "Eng yaxshi", "ru": "Лучший", "en": "Best"},
    "stats.minutes": {"uz": "Daqiqa", "ru": "Минут", "en": "Minutes"},
    "help.title": {"uz": "Yordam markazi", "ru": "Центр помощи", "en": "Help center"},
    "rating.participants": {"uz": "Reytingdagi ishtirokchilar", "ru": "Участников в рейтинге", "en": "Participants"},
    "rating.score_col": {"uz": "Oddiy ballar", "ru": "Обычные баллы", "en": "Score"},
    "rating.by_week": {"uz": "Haftalar bo'yicha", "ru": "По неделям", "en": "By week"},
    "rating.by_month": {"uz": "Oylar bo'yicha", "ru": "По месяцам", "en": "By month"},
    "rating.search": {"uz": "Qidirmoq", "ru": "Поиск", "en": "Search"},
    "rating.city": {"uz": "Shahar", "ru": "Город", "en": "City"},
    "multiplayer.title": {"uz": "Multipleyer", "ru": "Мультиплеер", "en": "Multiplayer"},
    "homework.title": {"uz": "Uy vazifalari", "ru": "Домашние задания", "en": "Homework"},
    "btn.games": {"uz": "O'yinlar", "ru": "Игры", "en": "Games"},

    # --- Profil ---
    "profile.settings": {"uz": "Sozlamalar", "ru": "Настройки", "en": "Settings"},
    "profile.name": {"uz": "Ism", "ru": "Имя", "en": "Name"},
    "profile.age_group": {"uz": "Yosh guruhi", "ru": "Возрастная группа", "en": "Age group"},
    "profile.avatar": {"uz": "Avatar", "ru": "Аватар", "en": "Avatar"},
    "profile.sound": {"uz": "Ovoz effektlari", "ru": "Звуковые эффекты", "en": "Sound effects"},
    "common.save": {"uz": "Saqlash", "ru": "Сохранить", "en": "Save"},
    "common.year": {"uz": "yosh", "ru": "лет", "en": "y.o."},

    # --- Multiplayer / Homework ---
    "mp.compete": {"uz": "Do'stlaring bilan musobaqalash", "ru": "Соревнуйся с друзьями", "en": "Compete with friends"},
    "mp.desc": {"uz": "Tez orada! Real vaqtda boshqa o'yinchilar bilan musobaqalashasiz.", "ru": "Скоро! Соревнования с другими игроками в реальном времени.", "en": "Coming soon! Real-time competitions with other players."},
    "mp.try": {"uz": "Hozircha o'yinlarni sinab ko'ring", "ru": "Пока попробуйте игры", "en": "Try the games for now"},
    "hw.head": {"uz": "Vazifalaringiz shu yerda bo'ladi", "ru": "Ваши задания будут здесь", "en": "Your tasks will appear here"},
    "hw.desc": {"uz": "O'qituvchingiz bergan uy vazifalari shu bo'limda paydo bo'ladi.", "ru": "Домашние задания от учителя появятся здесь.", "en": "Homework from your teacher will appear here."},
    "hw.math": {"uz": "Matematika mashqlari", "ru": "Упражнения по математике", "en": "Math exercises"},

    # --- Parent register ---
    "preg.title": {"uz": "Ota-ona ro'yxati", "ru": "Регистрация родителя", "en": "Parent registration"},
    "preg.sub": {"uz": "Ota-ona sifatida ro'yxatdan o'ting. Tasdiq emailingizga yuboriladi.", "ru": "Зарегистрируйтесь как родитель. Подтверждение придёт на email.", "en": "Register as a parent. Confirmation will be sent to your email."},
    "preg.who": {"uz": "Kim ro'yxatdan o'tmoqda?", "ru": "Кто регистрируется?", "en": "Who is registering?"},
    "preg.father": {"uz": "Ota", "ru": "Отец", "en": "Father"},
    "preg.mother": {"uz": "Ona", "ru": "Мать", "en": "Mother"},
    "preg.fname": {"uz": "Ism", "ru": "Имя", "en": "Name"},
    "preg.lname": {"uz": "Familiya", "ru": "Фамилия", "en": "Surname"},
    "preg.age": {"uz": "Yoshi", "ru": "Возраст", "en": "Age"},
    "preg.work": {"uz": "Ish joyi", "ru": "Место работы", "en": "Workplace"},
    "preg.child_name": {"uz": "Bola ismi", "ru": "Имя ребёнка", "en": "Child's name"},
    "preg.child_lname": {"uz": "Bola familiyasi", "ru": "Фамилия ребёнка", "en": "Child's surname"},
    "preg.email": {"uz": "Email (Gmail) — tasdiq shu yerga keladi", "ru": "Email (Gmail) — сюда придёт подтверждение", "en": "Email (Gmail) — confirmation goes here"},
    "preg.submit": {"uz": "Ro'yxatdan o'tish va yoqish", "ru": "Зарегистрироваться и включить", "en": "Register and enable"},
    "pc.enabled": {"uz": "Yoqilgan", "ru": "Включено", "en": "Enabled"},
    "pc.child": {"uz": "Farzand", "ru": "Ребёнок", "en": "Child"},
    "pc.sub": {"uz": "Farzandingiz uchun vaqt chegarasi va ruxsatlarni sozlang.", "ru": "Настройте лимит времени и разрешения для ребёнка.", "en": "Set time limit and permissions for your child."},
    "pc.pin": {"uz": "PIN kod", "ru": "PIN-код", "en": "PIN code"},
    "pc.block": {"uz": "Hisobni bloklash", "ru": "Заблокировать аккаунт", "en": "Block account"},
    "pc.daily": {"uz": "Kunlik vaqt chegarasi (daqiqa)", "ru": "Дневной лимит (минут)", "en": "Daily limit (minutes)"},
    "pc.weekly": {"uz": "Haftalik maqsad (daqiqa)", "ru": "Недельная цель (минут)", "en": "Weekly goal (minutes)"},
    "pc.bed_start": {"uz": "Tunlik bloklash (boshlanishi)", "ru": "Ночная блокировка (начало)", "en": "Bedtime block (start)"},
    "pc.bed_end": {"uz": "Tunlik bloklash (tugashi)", "ru": "Ночная блокировка (конец)", "en": "Bedtime block (end)"},
    "pc.cats": {"uz": "Ruxsat etilgan kategoriyalar", "ru": "Разрешённые категории", "en": "Allowed categories"},
    "pc.save": {"uz": "Saqlash va yoqish", "ru": "Сохранить и включить", "en": "Save and enable"},
    "pc.modal_title": {"uz": "Ota-ona nazorati muvaffaqiyatli yoqildi!", "ru": "Родительский контроль успешно включён!", "en": "Parental control successfully enabled!"},
    "pc.modal_sub": {"uz": "Tasdiq xabari emailingizga yuborildi 📧.", "ru": "Подтверждение отправлено на ваш email 📧.", "en": "Confirmation was sent to your email 📧."},
    "pc.ok": {"uz": "Tushunarli", "ru": "Понятно", "en": "Got it"},

    # --- Auth (qo'shimcha) ---
    "auth.login_btn": {"uz": "Kirish", "ru": "Войти", "en": "Sign in"},
    "auth.register_btn": {"uz": "Ro'yxatdan o'tish", "ru": "Регистрация", "en": "Sign up"},
    "auth.name": {"uz": "Ism", "ru": "Имя", "en": "Name"},
    "auth.your_age": {"uz": "Yoshingiz", "ru": "Ваш возраст", "en": "Your age"},
    "auth.pick_avatar": {"uz": "Avatar tanlang", "ru": "Выберите аватар", "en": "Choose an avatar"},
    "auth.hero": {"uz": "O'yna, o'rgan, yulduz yig'!", "ru": "Играй, учись, собирай звёзды!", "en": "Play, learn, collect stars!"},
    "auth.hero_sub": {"uz": "6–14 yoshdagi bolalar uchun interaktiv ta'limiy o'yinlar platformasi.", "ru": "Платформа обучающих игр для детей 6–14 лет.", "en": "Interactive educational games platform for kids aged 6–14."},

    # --- Stats / Help ---
    "stats.sub": {"uz": "Sizning o'sishingiz va faolligingiz", "ru": "Ваш прогресс и активность", "en": "Your progress and activity"},
    "help.sub": {"uz": "Ko'p so'raladigan savollar va qo'llanma", "ru": "Частые вопросы и руководство", "en": "FAQ and guide"},
    "group.brain": {"uz": "Aqliy test", "ru": "Тест на ум", "en": "Brain test"},

    # --- Rating filtrlari ---
    "rating.month": {"uz": "Oy", "ru": "Месяц", "en": "Month"},
    "rating.filter_rating": {"uz": "Reyting:", "ru": "Рейтинг:", "en": "Rating:"},
    "rating.students": {"uz": "O'quvchilar", "ru": "Ученики", "en": "Students"},
    "rating.teachers": {"uz": "O'qituvchilar", "ru": "Учителя", "en": "Teachers"},
    "rating.module": {"uz": "Modul", "ru": "Модуль", "en": "Module"},
    "rating.all": {"uz": "Barchasi", "ru": "Все", "en": "All"},
    "rating.mental": {"uz": "Mental", "ru": "Ментальная", "en": "Mental"},
    "rating.math": {"uz": "Matematika", "ru": "Математика", "en": "Math"},
    "rating.difficulty": {"uz": "Qiyinchilik", "ru": "Сложность", "en": "Difficulty"},
    "rating.easy": {"uz": "Oson", "ru": "Лёгкий", "en": "Easy"},
    "rating.hard": {"uz": "Qiyin", "ru": "Сложный", "en": "Hard"},
    "rating.geography": {"uz": "Geografiya", "ru": "География", "en": "Geography"},
    "rating.at_school": {"uz": "Maktabda", "ru": "В школе", "en": "At school"},
    "rating.in_city": {"uz": "Shaharda", "ru": "В городе", "en": "In city"},
    "rating.in_republic": {"uz": "Respublikada", "ru": "В республике", "en": "In republic"},
    "rating.scoring": {"uz": "Ballashtirish", "ru": "Начисление баллов", "en": "Scoring"},
    "rating.simple": {"uz": "Oddiy", "ru": "Обычное", "en": "Simple"},
    "rating.complex": {"uz": "Murakkab", "ru": "Сложное", "en": "Complex"},
}


def t(key, lang=DEFAULT_LANG):
    entry = STRINGS.get(key)
    if not entry:
        return key
    return entry.get(lang) or entry.get(DEFAULT_LANG) or key


def table_for(lang):
    """Joriy til uchun {kalit: matn} flat lug'atini qaytaradi."""
    lang = lang if lang in LANG_CODES else DEFAULT_LANG
    return {k: (v.get(lang) or v.get(DEFAULT_LANG) or k) for k, v in STRINGS.items()}

# 🧠 MindSkills — BrainGames

Bolalar uchun aqliy ko'nikmalarni rivojlantiruvchi **adaptiv o'yin platformasi**.
To'liq **Django (MVT — Model-View-Template)** asosida qurilgan: barcha HTML
fayllar `templates/` ichida, barcha CSS/JS esa `static/` ichida.

O'zbek tilida, o'zbek madaniyatiga moslangan dizayn (Samarqand feruzasi + tilla naqsh
ranglari), **ota-ona nazorati** va **adaptiv qiyinlik tizimi** bilan.

---

## ✨ Asosiy imkoniyatlar

| Bo'lim | Tavsif |
|--------|--------|
| 🧮 **Mental arifmetika** | Sonlarni xayolan qo'shish va ayirish |
| 🔢 **Abakus (soroban)** | Abakusda ko'rsatilgan sonni o'qish — ko'rish xotirasi |
| 📖 **Tez o'qish** | Yonib o'chgan so'zni tanib olish — tez idrok |
| 🧠 **Xotira mashqi** | Kataklar ketma-ketligini eslab qolish |
| 🎯 **Adaptiv tizim** | Vaqt + aniqlikni tahlil qilib qiyinlikni avtomatik sozlaydi |
| 👨‍👩‍👧 **Ota-ona nazorati** | Vaqt chegarasi, tunlik rejim, o'yin ruxsatlari, hisobotlar |
| 🏆 **Gamifikatsiya** | Tangalar, darajalar, ketma-ket kunlar, yutuq nishonlari |

### Adaptiv learning algoritmi
Tizim bolaning har bir topshiriqqa sarflagan vaqti va to'g'ri javoblar foizini
tahlil qiladi. Bola **ketma-ket 3 ta** topshiriqni to'g'ri bajarsa, qiyinlik darajasi
avtomatik oshadi. Bola qiynalsa (ketma-ket xato yoki sekin javob), daraja tushadi va
**yordam ko'rsatmalar** beriladi. Mantiq ham serverda (`games/adaptive.py`), ham
mijozda (`static/js/adaptive.js`) bir xil ishlaydi.

---

## 🗂️ Loyiha tuzilmasi

```
BrainGames/
├── config/              # Django sozlamalari (settings, urls, wsgi)
├── accounts/            # Foydalanuvchi (bola/ota-ona/admin) + ota-ona nazorati
├── games/               # O'yinlar, sessiyalar, urinishlar, adaptiv dvigatel
├── dashboard/           # O'quvchi paneli + ota-ona nazorat paneli
├── core/                # Landing sahifa + seed buyrug'i
├── templates/           # Barcha HTML fayllar (MVT)
│   ├── base.html
│   ├── core/  accounts/  dashboard/  games/play/
├── static/              # Barcha CSS va JS
│   ├── css/  (base, auth, dashboard, games)
│   └── js/   (main, auth, dashboard, adaptive, game-core, games/*)
├── manage.py
└── requirements.txt
```

---

## 🚀 Lokal ishga tushirish

```bash
# 1. Virtual muhit (allaqachon mavjud bo'lsa o'tkazib yuboring)
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # Linux/Mac

# 2. Kutubxonalar
pip install -r requirements.txt

# 3. Ma'lumotlar bazasi
python manage.py migrate

# 4. Demo ma'lumotlar (o'yinlar, yutuqlar, namuna hisoblar)
python manage.py seed

# 5. Server
python manage.py runserver
```

Brauzerda: <http://127.0.0.1:8000>

### Demo hisoblar
| Rol | Login | Parol |
|-----|-------|-------|
| Ota-ona | `ota_demo` | `demo1234` |
| Bola | `dilnoza` | `demo1234` |
| Bola | `jasur` | `demo1234` |
| Admin | `admin` | (o'zingiz `createsuperuser` bilan) |

---

## ☁️ PythonAnywhere'ga joylash

1. **Kodni yuklang** (git yoki yuklab tashlash) va virtual muhit yarating:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 braingames
   pip install -r requirements.txt
   ```

2. **Atrof-muhit o'zgaruvchilari** (Web → "Environment variables" yoki WSGI faylda):
   ```
   DJANGO_SECRET_KEY = <uzun-tasodifiy-kalit>
   DJANGO_DEBUG = False
   DJANGO_ALLOWED_HOSTS = foydalanuvchi.pythonanywhere.com
   ```

3. **Web app** (Manual config, Python 3.11). WSGI faylda:
   ```python
   import os, sys
   path = "/home/foydalanuvchi/BrainGames"
   if path not in sys.path:
       sys.path.append(path)
   os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"
   from config.wsgi import application
   ```

4. **Bazani tayyorlang**:
   ```bash
   python manage.py migrate
   python manage.py seed
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

5. **Statik fayllar** (Web → Static files):
   - URL: `/static/`  →  Directory: `/home/foydalanuvchi/BrainGames/staticfiles`

   > Loyiha `whitenoise` bilan ham keladi, shuning uchun statik fayllar ishlab
   > chiqarishda ham muammosiz xizmat qiladi.

6. **Reload** tugmasini bosing. Tayyor! 🎉

---

## 🛠️ Texnologiyalar
- **Django 5.1** (MVT) — Model-View-Template
- **SQLite** (ishlab chiqarishda PostgreSQL/MySQL'ga oson o'tadi)
- **WhiteNoise** — statik fayllar
- **Vanilla JS** — o'yin dvigateli (tashqi kutubxonasiz)
- Maxsus `User` modeli (rollar) va `ParentalControl` modeli

---

© MindSkills · O'zbekiston

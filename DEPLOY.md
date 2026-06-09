# BrainGames — PythonAnywhere'ga joylash (deploy)

To'liq qadam-baqadam yo'riqnoma. Loyiha **Django 5.1 + WhiteNoise** (statik fayllar uchun),
ma'lumotlar bazasi **SQLite**. Hech qanday qo'shimcha xizmat (Redis, Postgres) shart emas.

Sozlamalar allaqachon production uchun tayyor:
- `DEBUG = False` (standart)
- `ALLOWED_HOSTS = ['*']`
- Statik: WhiteNoise + `CompressedManifestStaticFilesStorage` (avtomatik kesh-busting)

---

## 1. Kodni PythonAnywhere'ga yuklash

PythonAnywhere'da **Bash console** oching va loyihani torting (yoki ZIP yuklang):

```bash
cd ~
git clone <REPO_URL> BrainGames        # yoki Files'dan yuklab, BrainGames papkasiga joylang
cd BrainGames
```

> `db.sqlite3`, `staticfiles/`, `.venv/` ni yubormang — ular serverda yangidan yaratiladi.

---

## 2. Virtual muhit va kutubxonalar

PythonAnywhere'da Python 3.10–3.13 ishlaydi (Django 5.1 shularni qo'llaydi):

```bash
cd ~/BrainGames
python3.13 -m venv .venv          # yoki python3.10 ...
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 3. Ma'lumotlar bazasi va demo

```bash
python manage.py migrate
python manage.py seed              # o'yinlar, yutuqlar + demo hisob (ali2015 / demo1234)
python manage.py createsuperuser   # admin uchun (ixtiyoriy)
```

---

## 4. Statik fayllarni yig'ish

```bash
python manage.py collectstatic --noinput
```

Bu `staticfiles/` papkasiga hash-nomli fayllarni yig'adi. WhiteNoise ularni o'zi
tarqatadi — PythonAnywhere'da alohida static mapping **shart emas** (lekin xohlasangiz
qo'shsa bo'ladi, 7-bandga qarang).

---

## 5. Web ilovani sozlash (Web bo'limi)

PythonAnywhere → **Web** → **Add a new web app** → **Manual configuration** →
Python versiyasini venv bilan bir xil tanlang (mas. 3.13).

So'ng **Web** sahifasida:

| Maydon | Qiymat |
|---|---|
| **Source code** | `/home/FOYDALANUVCHI/BrainGames` |
| **Working directory** | `/home/FOYDALANUVCHI/BrainGames` |
| **Virtualenv** | `/home/FOYDALANUVCHI/BrainGames/.venv` |

`FOYDALANUVCHI` — sizning PythonAnywhere foydalanuvchi nomingiz.

---

## 6. WSGI faylini tahrirlash

**Web** sahifasidagi **WSGI configuration file** havolasini bosing va ichidagi
hammasini o'chirib, quyidagini qo'ying (`FOYDALANUVCHI` ni o'zingiznikiga almashtiring):

```python
import os
import sys

path = '/home/FOYDALANUVCHI/BrainGames'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# --- Ixtiyoriy, lekin tavsiya etiladi (production) ---
# os.environ['DJANGO_SECRET_KEY'] = 'uzun-tasodifiy-maxfiy-kalit'
# os.environ['DJANGO_ALLOWED_HOSTS'] = 'FOYDALANUVCHI.pythonanywhere.com'
# Gmail orqali ota-ona tasdig'i kerak bo'lsa:
# os.environ['DJANGO_EMAIL_HOST_USER'] = 'siz@gmail.com'
# os.environ['DJANGO_EMAIL_HOST_PASSWORD'] = 'gmail-app-password'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

> **Eslatma:** PythonAnywhere'da web ilova konsol `env` ni o'qimaydi —
> muhit o'zgaruvchilarini ayni shu WSGI faylida `os.environ[...]` orqali bering.

---

## 7. (Ixtiyoriy) Static mapping

WhiteNoise statikani o'zi tarqatadi, shuning uchun bu shart emas. Lekin biroz
tezroq bo'lishi uchun **Web → Static files** bo'limiga qo'shsangiz bo'ladi:

| URL | Directory |
|---|---|
| `/static/` | `/home/FOYDALANUVCHI/BrainGames/staticfiles` |

---

## 8. Ishga tushirish

**Web** sahifasidagi katta yashil **Reload** tugmasini bosing.

Sayt ochiladi: `https://FOYDALANUVCHI.pythonanywhere.com`
Demo kirish: **ali2015 / demo1234**, ota-ona PIN: **0000**.

---

## Kodni yangilaganda (keyingi safar)

```bash
cd ~/BrainGames
git pull
source .venv/bin/activate
pip install -r requirements.txt        # bog'liqlik o'zgargan bo'lsa
python manage.py migrate               # yangi migratsiya bo'lsa
python manage.py collectstatic --noinput
# So'ng Web sahifasida Reload bosing
```

---

## Muhim eslatmalar

- **`collectstatic` ni har safar statik (CSS/JS/rasm) o'zgarganda qayta ishga tushiring** —
  aks holda eski hash-nomli fayllar qoladi yoki sahifa statikani topa olmaydi.
- **SECRET_KEY**: hozir kodda zaxira (insecure) kalit bor — sayt shusiz ham ishlaydi,
  lekin haqiqiy production uchun WSGI faylida `DJANGO_SECRET_KEY` ni bering.
- **Lokal ishlash** uchun DEBUG'ni yoqing: `DJANGO_DEBUG=True` muhit o'zgaruvchisi
  bilan `runserver` qiling.
- **O'zingizning domeningiz** bo'lsa, WSGI faylida `DJANGO_CSRF_TRUSTED` ga
  `https://sizning-domen.uz` qo'shing (forma/login ishlashi uchun).

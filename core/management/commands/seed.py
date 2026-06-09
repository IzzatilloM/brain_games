"""Demo ma'lumotlar: o'yinlar, yutuqlar, 50 ta student va demo hisob.

Foydalanish:  python manage.py seed
"""

import random

from django.core.management.base import BaseCommand

from accounts.models import AVATARS, ParentalControl, User
from games.catalog import all_games, subject_games
from games.models import Achievement, Game

ACHIEVEMENTS = [
    {"code": "first_game", "icon": "🎮", "title": "Birinchi qadam", "description": "Birinchi o'yiningizni yakunladingiz", "coins": 50},
    {"code": "ten_games", "icon": "🎯", "title": "Faol o'yinchi", "description": "10 ta o'yin o'ynadingiz", "coins": 100},
    {"code": "streak_3", "icon": "🔥", "title": "3 kun ketma-ket", "description": "3 kun ketma-ket o'ynadingiz", "coins": 75},
    {"code": "streak_7", "icon": "🗓️", "title": "Haftalik chempion", "description": "7 kun ketma-ket o'ynadingiz", "coins": 150},
    {"code": "stars_25", "icon": "⭐", "title": "Yulduz yig'uvchi", "description": "25 ta yulduz to'pladingiz", "coins": 100},
    {"code": "level_5", "icon": "🏅", "title": "Beshinchi daraja", "description": "5-darajaga yetib bordingiz", "coins": 120},
]

FIRST = ["Ali", "Vali", "Sardor", "Diyor", "Aziz", "Jasur", "Bek", "Doston", "Otabek", "Sherzod",
         "Dilnoza", "Madina", "Shahnoza", "Zilola", "Gulnoza", "Sevara", "Nilufar", "Malika", "Oysha", "Komila",
         "Islom", "Umar", "Hasan", "Husan", "Akmal", "Bobur", "Temur", "Jahongir", "Sarvar", "Eldor",
         "Safiya", "Muslima", "Robiya", "Sumbula", "Iroda", "Yulduz", "Charos", "Munisa", "Dildora", "Laylo"]
LAST = ["Karimov", "Aliyev", "Yusupov", "Rahmonov", "Sodiqov", "Tursunov", "Ismoilov", "Qodirov", "Saidov", "Umarov",
        "Karimova", "Aliyeva", "Yusupova", "Rahmonova", "Sodiqova", "Tursunova", "Ismoilova", "Qodirova", "Saidova", "Umarova"]
CITIES = ["Toshkent", "Samarqand", "Buxoro", "Andijon", "Farg'ona", "Namangan", "Qarshi", "Nukus", "Xiva", "Jizzax", "Navoiy", "Termiz"]
AGES = ["6-8", "9-11", "12-14"]


class Command(BaseCommand):
    help = "O'yinlar, yutuqlar, 50 student va demo hisobni yaratadi"

    def handle(self, *args, **options):
        games = all_games() + subject_games()
        made = 0
        for g in games:
            Game.objects.update_or_create(
                slug=g["slug"],
                defaults={"title": g["name"], "category": g["category"], "kind": g.get("kind", "quiz"),
                          "icon": g.get("icon", "🎮"), "color": g.get("color", "#7c5cff"), "tagline": g.get("tagline", "")},
            )
            made += 1
        self.stdout.write(self.style.SUCCESS(f"[OK] {made} ta o'yin tayyor"))

        for data in ACHIEVEMENTS:
            Achievement.objects.update_or_create(code=data["code"], defaults=data)
        self.stdout.write(self.style.SUCCESS(f"[OK] {len(ACHIEVEMENTS)} ta yutuq tayyor"))

        # Demo hisob
        demo, created = User.objects.get_or_create(
            username="ali2015",
            defaults={"full_name": "Ali Valiyev", "avatar": "🦊", "age_group": "9-11", "city": "Toshkent",
                      "xp": 1240, "coins": 320, "stars": 28, "streak_days": 5},
        )
        if created:
            demo.set_password("demo1234")
            demo.save()
        ParentalControl.objects.get_or_create(user=demo)

        # 50 ta student
        random.seed(42)
        count = 0
        for i in range(1, 51):
            uname = f"student{i:02d}"
            xp = random.randint(300, 9800)
            fn = f"{random.choice(FIRST)} {random.choice(LAST)}"
            u, c = User.objects.get_or_create(
                username=uname,
                defaults={"full_name": fn, "avatar": random.choice(AVATARS),
                          "age_group": random.choice(AGES), "city": random.choice(CITIES),
                          "xp": xp, "coins": xp // 4, "stars": xp // 80,
                          "streak_days": random.randint(0, 30)},
            )
            if c:
                u.set_password("demo1234")
                u.save()
                ParentalControl.objects.get_or_create(user=u)
                count += 1
        self.stdout.write(self.style.SUCCESS(f"[OK] {count} ta student qo'shildi (login: student01..student50 / demo1234)"))

        self.stdout.write(self.style.SUCCESS("\n[OK] Demo hisob:"))
        self.stdout.write("   login: ali2015   parol: demo1234   (ota-ona PIN: 0000)")
        self.stdout.write(self.style.SUCCESS("Tayyor! python manage.py runserver"))

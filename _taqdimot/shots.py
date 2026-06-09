# -*- coding: utf-8 -*-
"""BrainGames sahifalaridan skrinshot olish (Playwright + tizimdagi Chrome)."""
import os, time
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8011"
OUT = os.path.join(os.path.dirname(__file__), "img")
os.makedirs(OUT, exist_ok=True)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

KILL_ANIM = """
(() => { const s=document.createElement('style');
 s.textContent='*,*::before,*::after{animation:none !important;transition:none !important;}';
 document.head.appendChild(s); })()
"""

# (fayl nomi, URL, kutish ms)
PAGES = [
    ("01_login",      "/hisob/kirish/",                 600),
    ("02_home",       "/",                              900),
    ("03_games",      "/oyinlar/",                      900),
    ("04_subjects",   "/oyinlar/fanlar/",               900),
    ("05_mental_flash","/oyinlar/play/flash/",          1200),
    ("06_forsaj",     "/oyinlar/play/forsaj/",          1200),
    ("07_ustunlar",   "/oyinlar/play/ustunlar/",        1200),
    ("08_memory_juft","/oyinlar/play/juft-topish/",     1200),
    ("09_numrecall",  "/oyinlar/play/sonni-eslab/",     1200),
    ("10_schulte",    "/oyinlar/play/schulte/",         1200),
    ("11_reading",    "/oyinlar/play/soz-chaqnashi/",   1200),
    ("12_quiz",       "/oyinlar/play/qoshish/",         1200),
    ("13_subjectquiz","/oyinlar/play/fan-matematika-1/",1200),
    ("14_rating",     "/reyting/",                      900),
    ("15_stats",      "/statistika/",                   900),
    ("16_profile",    "/hisob/profil/",                 900),
    ("17_homework",   "/uy-vazifalari/",                900),
    ("18_multiplayer","/multipleyer/",                  900),
    ("19_parental",   "/hisob/ota-ona-nazorati/",       900),
]

def shoot(page, name, path, wait):
    try:
        page.goto(BASE + path, wait_until="load", timeout=20000)
    except Exception as e:
        print(f"  ! goto {path}: {e}")
    try:
        page.evaluate(KILL_ANIM)
    except Exception:
        pass
    page.wait_for_timeout(wait)
    try:
        page.evaluate("document.fonts.ready")
    except Exception:
        pass
    page.wait_for_timeout(250)
    fp = os.path.join(OUT, name + ".png")
    page.screenshot(path=fp)
    print(f"  + {name}.png  ({path})")

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=CHROME, headless=True)
    ctx = browser.new_context(viewport={"width": 1280, "height": 800},
                              device_scale_factor=2, locale="uz-UZ")
    page = ctx.new_page()

    # --- login (bola hisobi) ---
    page.goto(BASE + "/hisob/kirish/", wait_until="load", timeout=20000)
    # avval login sahifasini olib qo'yamiz (chiroyli auth hero)
    page.evaluate(KILL_ANIM); page.wait_for_timeout(600)
    page.screenshot(path=os.path.join(OUT, "01_login.png"))
    print("  + 01_login.png  (/hisob/kirish/)")
    page.fill("input[name=username]", "ali2015")
    page.fill("input[name=password]", "demo1234")
    with page.expect_navigation(wait_until="load", timeout=20000):
        page.click("button.btn-ms")
    page.wait_for_timeout(800)
    print("  logged in as ali2015 ->", page.url)

    for name, path, wait in PAGES[1:]:
        shoot(page, name, path, wait)

    browser.close()
print("DONE")

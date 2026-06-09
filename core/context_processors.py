"""Shablonlarga umumiy kontekst (sayt + til)."""

from .translations import DEFAULT_LANG, LANGS, table_for


def site_context(request):
    lang = DEFAULT_LANG
    if hasattr(request, "session"):
        lang = request.session.get("lang", DEFAULT_LANG)
    return {
        "SITE_NAME": "BrainGames",
        "SITE_TAGLINE": "O'yna, o'rgan, yulduz yig'!",
        "APP_VERSION": "v1.0.0",
        "COPYRIGHT_YEARS": "2024 – 2026",
        "LANG": lang,
        "LANGS": LANGS,
        "T": table_for(lang),
    }

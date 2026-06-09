from whitenoise.storage import CompressedManifestStaticFilesStorage


class WhiteNoiseStaticStorage(CompressedManifestStaticFilesStorage):
    """Manifestda topilmagan statik fayl butun sahifani qulatmasin.

    manifest_strict=False bo'lganda, manifestda yo'q fayl uchun ValueError
    o'rniga faylning oddiy (hash'siz) nomi qaytariladi. Bu eski/chala
    collectstatic manifest tufayli sayt to'liq ishdan chiqishini oldini oladi.
    """

    manifest_strict = False

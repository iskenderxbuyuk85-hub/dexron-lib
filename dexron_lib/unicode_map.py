# DEXRON Unicode Homoglif - GEORGIAN (Gurcuce) Alfabesi
# Kaynak: 0x10A0-0x10FF (Asomtavruli) + 0x2D00-0x2D2F (Nuskhuri)
# Lyrox'un CJK'sindan farkli, benzersiz
# Ornek: ა ბ გ დ ე ვ ზ თ ი კ ლ მ ნ ო პ ჟ რ ს ტ უ ფ ქ ღ ყ შ ჩ ც ძ წ ჭ ხ ჯ ჰ

GEO_BASE    = 0x10A0   # Asomtavruli (eski Gürcüce)
GEO_OFFSET  = 0x2D00   # Nuskhuri (kilise Gürcücesi)
PAD         = 0x10


def embed_unicode(data: bytes) -> str:
    """Byte dizisini 2x Gurcuce karaktere gomer."""
    out = []
    for b in data:
        blok = (b >> 4) & 0xF
        offset = b & 0xF
        c1 = chr(GEO_BASE + blok * 0x10 + PAD)
        c2 = chr(GEO_OFFSET + offset * 0x10 + PAD)
        out.append(c1 + c2)
    return "".join(out)


def extract_unicode(s: str) -> bytes:
    """Gomulu Gurcuce karakterlerden byte'lari cikarir."""
    out = bytearray()
    for i in range(0, len(s), 2):
        c1 = ord(s[i])
        c2 = ord(s[i + 1])
        blok = (c1 - GEO_BASE - PAD) // 0x10
        offset = (c2 - GEO_OFFSET - PAD) // 0x10
        b = ((blok & 0xF) << 4) | (offset & 0xF)
        out.append(b)
    return bytes(out)


# Alternatif: Hangul (Korece) - yedek
HANGUL_BASE = 0xAC00


def embed_hangul(data: bytes) -> str:
    return "".join(chr(HANGUL_BASE + b) for b in data)


def extract_hangul(s: str) -> bytes:
    return bytes(ord(c) - HANGUL_BASE for c in s)

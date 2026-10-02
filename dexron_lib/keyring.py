import hashlib
import hmac
import secrets


def derive_key(seed: str, length: int = 32) -> bytes:
    h = hashlib.sha256(seed.encode("utf-8")).digest()
    while len(h) < length:
        h += hashlib.sha256(h).digest()
    return h[:length]


def xor_bytes(data: bytes, key: bytes) -> bytes:
    return bytes(data[i] ^ key[i % len(key)] for i in range(len(data)))


def rotate_key(key: bytes, rounds: int = 3) -> bytes:
    k = key
    for _ in range(rounds):
        k = hashlib.sha256(k).digest()
    return k


def hmac_sign(data: bytes, key: bytes) -> str:
    return hmac.new(key, data, hashlib.sha256).hexdigest()


def random_key(length: int = 32) -> bytes:
    return secrets.token_bytes(length)

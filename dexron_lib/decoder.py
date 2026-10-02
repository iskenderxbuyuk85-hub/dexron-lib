import base64
import hashlib
import marshal
import zlib
import sys
import os

from .keyring import derive_key, xor_bytes, hmac_sign
from .unicode_map import embed_unicode, extract_unicode

DEFAULT_SEED = "dexron-v1-2024"


def encode(source: bytes, seed: str = DEFAULT_SEED) -> str:
    key = derive_key(seed)
    compressed = zlib.compress(source, 9)
    b64 = base64.b64encode(compressed)
    xored = xor_bytes(b64, key)
    return embed_unicode(xored)


def decode(payload: str, seed: str = DEFAULT_SEED) -> bytes:
    key = derive_key(seed)
    xored = extract_unicode(payload)
    b64 = xor_bytes(xored, key)
    compressed = base64.b64decode(b64)
    return zlib.decompress(compressed)


def encode_source(source_code: str, seed: str = DEFAULT_SEED) -> str:
    compiled = compile(source_code, "<DEXRON>", "exec")
    m = marshal.dumps(compiled)
    return encode(m, seed)


def decode_and_exec(payload: str, seed: str = DEFAULT_SEED):
    m = decode(payload, seed)
    code = marshal.loads(m)
    exec(code)


def install_hook():
    def _hook(event, args):
        if event in ("sys.settrace", "sys.setprofile"):
            os._exit(1)
        if event in ("exec", "compile", "marshal.loads"):
            if sys.gettrace() is not None or sys.getprofile() is not None:
                os._exit(1)
    sys.addaudithook(_hook)


def self_check(payload: str, expected_sig: str, seed: str = DEFAULT_SEED) -> bool:
    try:
        m = decode(payload, seed)
        key = derive_key(seed)
        sig = hmac_sign(m, key)
        return sig == expected_sig
    except Exception:
        return False


def build_loader(payload: str, seed: str = DEFAULT_SEED,
                 repo_url: str = None, install: bool = True) -> str:
    """
    Lyrox tarzi tam loader uretir.
    """
    if repo_url is None:
        repo_url = "https://github.com/iskenderxbuyuk85-hub/dexron-lib/archive/refs/heads/main.zip"

    install_block = ""
    if install:
        install_block = f'''
import subprocess as _sp, sys as _ss
_sp.run([_ss.executable, "-m", "pip", "install", "--upgrade",
         "--force-reinstall", "--no-cache-dir", {repo_url!r}],
        capture_output=True)
'''

    var_name = "龍" + hashlib.sha256(os.urandom(8)).hexdigest()[:8]

    return f'''# DEXRON LIB LOADER v1 - @iskenderxbuyuk85-hub
{install_block}
import dexron_lib as _dl
import marshal as _m

{var_name} = {payload!r}

_dl.install_hook()
_compressed = _dl.decode({var_name})
exec(_m.loads(_compressed))
'''


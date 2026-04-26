import string

BASE62 = string.digits + string.ascii_letters  # 0-9, a-z, A-Z
BASE = len(BASE62)


def encode_base62(num: int) -> str:
    if num == 0:
        return BASE62[0]
    encoded = []
    while num > 0:
        num, rem = divmod(num, BASE)
        encoded.append(BASE62[rem])
    return "".join(reversed(encoded))


def decode_base62(code: str) -> int:
    num = 0
    for char in code:
        if char not in BASE62:
            raise ValueError(f"Invalid character in short code: {char!r}")
        num = num * BASE + BASE62.index(char)
    return num
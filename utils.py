import string

BASE62 = string.ascii_letters + string.digits

def encode_base62(num):
    base = len(BASE62)
    encoded = []

    while num > 0:
        num, rem = divmod(num, base)
        encoded.append(BASE62[rem])

    return ''.join(reversed(encoded)) or "a"
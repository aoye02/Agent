# This Python file uses the following encoding: utf-8
import hashlib
import os


def hash_password(password: str, salt: bytes = None) -> str:
    """把密码哈希。返回 "salt$hash" 格式的字符串。"""
    if salt is None:
        salt = os.urandom(16)      # 随机 16 字节 salt
    pwd_bytes = password.encode("utf-8")
    # 用 pbkdf2_hmac 做"慢哈希"（抗暴力破解）
    hashed = hashlib.pbkdf2_hmac(
        "sha256",
        pwd_bytes,
        salt,
        100000,                    # 迭代 10 万次
    )
    return salt.hex() + "$" + hashed.hex()


def verify_password(password: str, stored: str) -> bool:
    """验证密码是否匹配。stored 是 "salt$hash" 格式。"""
    try:
        salt_hex, hash_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
        pwd_bytes = password.encode("utf-8")
        hashed = hashlib.pbkdf2_hmac(
            "sha256",
            pwd_bytes,
            salt,
            100000,
        )
        return hashed.hex() == hash_hex
    except Exception:
        return False
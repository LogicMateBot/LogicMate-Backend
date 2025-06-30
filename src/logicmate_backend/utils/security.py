from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12,
)


def hash_password(password: str) -> str:
    return pwd_context.hash(secret=password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(secret=plain, hash=hashed)

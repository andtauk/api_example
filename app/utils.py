from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plaintext_password):
    return pwd_context.hash(plaintext_password)

def check_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
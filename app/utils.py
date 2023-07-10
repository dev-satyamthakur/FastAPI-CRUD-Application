from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify(plain_pass, hash_pass):
    return pwd_context.verify(plain_pass, hash_pass)
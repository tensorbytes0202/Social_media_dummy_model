from datetime import datetime, timedelta
# 👉 Time handle karne ke liye
# datetime.utcnow() → current time (UTC)
# timedelta() → time add karne ke liye (expiry set karte हैं)

from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "mysecretkey"   # change in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# password hash
def hash_password(password: str):
    return pwd_context.hash(password)

# verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# create token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
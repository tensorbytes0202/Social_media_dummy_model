from datetime import datetime, timedelta
# 👉 Time handle karne ke liye
# datetime.utcnow() → current time (UTC)
# timedelta() → time add karne ke liye (expiry set karte हैं)

from jose import JWTError, jwt
# JWT (JSON Web Token) handle करने के लिए

# jwt.encode() → token create
# jwt.decode() → token verify
# JWTError → error handling
from passlib.context import CryptContext
# Password hashing library
# Plain password ko secure hashed form me convert karta hai

SECRET_KEY = "mysecretkey"   # change in production
# Ye secret key hai

# JWT sign karne ke liye use hoti hai
# Server ke alawa kisi ko nahi pata honi chahiye
ALGORITHM = "HS256"
# Encryption algorithm
# HS256 = symmetric key (same key encode + decode)
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ye password hashing engine hai
# bcrypt = secure hashing algorithm
# deprecated="auto" → future compatibility

# password hash
def hash_password(password: str):
    return pwd_context.hash(password)
    # Plain password → hashed password

# verify password
def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
    # Login ke time:
    # user input password vs DB stored hash compare
    # ✔ Returns:

# create token
def create_access_token(data: dict):
    # 👉 Ye function JWT token banata hai
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


#     🔐 Signup
# user password देता है
# hash_password()
# DB में store
# 🔑 Login
# user password देता है
# verify_password()
# match → token generate
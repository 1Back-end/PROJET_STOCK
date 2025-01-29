import re
import os
from random import randint, choice
import string
import random
import bcrypt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from typing import Any, Optional, Union
from sqlalchemy.orm import Session
from datetime import datetime, timedelta,timezone
from app.main import models,crud
import jwt
from passlib.context import CryptContext
# from jose import JWTError, jwt

from .config import Config
ALGORITHM = "HS256"




# Création d'un contexte pour bcrypt (ou tout autre algorithme de hachage)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def password_hash(password: str) -> str:
    return pwd_context.hash(password)

def generate_password(length: int = 12) -> str:
    """Génère un mot de passe sécurisé aléatoire."""
    # Définir les caractères autorisés pour le mot de passe
    characters = string.ascii_letters + string.digits + string.punctuation
    # Générer un mot de passe aléatoire de la longueur spécifiée
    password = ''.join(random.choice(characters) for _ in range(length))
    return password

def password_hash(password: str) -> str:
    return pwd_context.hash(password)



def validate_email(email):
    email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return email_regex.match(email)

# def authenticate_user(db:Session, email: str, password: str):
#     user:models.User = crud.user.get_user_by_email(db = db, email = email)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

def create_access_token(
        subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def verify_token(token: str):
#     try:
#         payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
#         return payload
#     except JWTError:
#         raise Exception("Token invalid or expired")

def create_refresh_token(data: dict ):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(Config.REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# def authenticate_user(fake_db, username: str, password: str):
#     user = get_user(fake_db, username)
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

def generate_code(length=10):
    """Generate a random string of fixed length """

    end = random.choice([True, False])

    string_length = round(length / 3)
    letters = string.ascii_lowercase
    random_string = (''.join(choice(letters) for i in range(string_length))).upper()
    range_start = 10 ** ((length - string_length) - 1)
    range_end = (10 ** (length - string_length)) - 1
    random_number = randint(range_start, range_end)
    if not end:
        final_string = f"{random_string}{random_number}"
    else:
        final_string = f"{random_number}{random_string}"
    return final_string


def decode_access_token(token: str):
    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return decoded_token
    except Exception as e:
        if token:
            print("Failed to decode token")
            print(token)
            print(e)
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()

    # Hashing the password
    return (bcrypt.hashpw(password.encode('utf-8'), salt)).decode('utf-8')


# def get_password_hash(password: str) -> str:
#     return pwd_context.hash(password)


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=Config.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, Config.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.InvalidTokenError:
        return None


def generate_code(length=6, end=True):
    string_length = round(length/2)
    letters = string.ascii_lowercase
    random_string = (''.join(choice(letters) for i in range(string_length))).upper()
    range_start = 10**((length-string_length)-1)
    range_end = (10**(length-string_length))-1
    random_number =  randint(range_start, range_end)
    if not end:
        final_string = f"{random_string}{random_number}"
    else:
        final_string = f"{random_number}{random_string}"

    return final_string
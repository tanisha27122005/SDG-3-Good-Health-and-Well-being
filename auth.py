import streamlit as st
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from database import db_session

ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    try:
        return ph.verify(password_hash, password)
    except VerifyMismatchError:
        return False

def register_user(username: str, password: str, role: str = "user") -> tuple[bool, str]:
    if not username or not password:
        return False, "Username and password cannot be empty."
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if role == "admin":
        return False, "Public registration as administrator is strictly prohibited."
    
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                return False, "Username already exists."
            
            pwd_hash = hash_password(password)
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, pwd_hash, role)
            )
        return True, "Registration successful! Please log in."
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def authenticate_user(username: str, password: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, password_hash, role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        if user and verify_password(user["password_hash"], password):
            return {"id": user["id"], "username": user["username"], "role": user["role"]}
    return None

def create_first_admin(username: str, password: str):
    with db_session() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE role = 'admin'")
        if cursor.fetchone():
            print("Admin already exists.")
            return
        pwd_hash = hash_password(password)
        cursor.execute(
            "INSERT INTO users (username, password_hash, role) VALUES (?, ?, 'admin')",
            (username, pwd_hash)
        )
        print(f"First administrator '{username}' created securely.")

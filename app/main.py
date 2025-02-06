from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
import random
import string
import os
import sqlite3
import secrets
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

# FastAPI app instance
app = FastAPI(title="Password Generator API with Admin Authentication & API Key Management")

# Secret key for JWT tokens (Change for production security!)
SECRET_KEY = "super-secret-jwt-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour token expiry

# Admin credentials (Replace with a database in production)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD_HASH = "$2b$12$FikqD98PY7txfQ4m8y5Nne7YQIjf1OGZT/UzMuopWqdnzRovHiWcG"  # Hash of "securepassword123"

# Use environment variable for DB_PATH with a default fallback
DB_PATH = os.getenv('DB_PATH', '/app/data/passwords.db')

# ✅ Path to Diceware wordlist
WORDLIST_PATH = "/app/data/diceware.txt"

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Ensure the Diceware wordlist exists
if not os.path.exists(WORDLIST_PATH):
    raise FileNotFoundError(f"❌ Diceware wordlist not found at {WORDLIST_PATH}")

# Request model for password generation
class PasswordRequest(BaseModel):
    length: int
    use_uppercase: bool
    use_lowercase: bool
    use_numbers: bool
    use_specials: bool

# Request model for passphrase generation
class PassphraseRequest(BaseModel):
    num_words: int

@app.get("/")
def read_root():
    return {"message": "Password Generator API is running"}

@app.get("/health")
def health_check():
    """Checks if the API and database are running properly."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        return {"status": "ok", "database": "reachable"}
    except Exception as e:
        return {"status": "error", "database": f"unreachable: {str(e)}"}

# ✅ Generate Secure Password
@app.post("/generate_password")
def generate_password(request: PasswordRequest):
    """Generate a random secure password."""
    characters = ""
    if request.use_uppercase:
        characters += string.ascii_uppercase
    if request.use_lowercase:
        characters += string.ascii_lowercase
    if request.use_numbers:
        characters += string.digits
    if request.use_specials:
        characters += "!@#$%^&*()_+-=[]{}|;:,.<>?/"

    if not characters:
        raise HTTPException(status_code=400, detail="No character set selected")

    password = "".join(random.choice(characters) for _ in range(request.length))
    return {"password": password}

# ✅ Generate Secure Passphrase
@app.post("/generate_passphrase")
def generate_passphrase(request: PassphraseRequest):
    """Generate a secure passphrase using a Diceware wordlist."""
    if not os.path.exists(WORDLIST_PATH):
        raise HTTPException(status_code=500, detail="Diceware wordlist file not found")

    with open(WORDLIST_PATH, "r") as file:
        # ✅ Extract only the words, ignoring numbers
        words = [line.strip().split("\t")[-1] for line in file.readlines()]

    if len(words) == 0:
        raise HTTPException(status_code=500, detail="Diceware wordlist is empty")

    # ✅ Return a passphrase as a single string with no spaces
    passphrase = "".join(random.choice(words) for _ in range(request.num_words))
    return {"passphrase": passphrase}

# Run FastAPI when executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
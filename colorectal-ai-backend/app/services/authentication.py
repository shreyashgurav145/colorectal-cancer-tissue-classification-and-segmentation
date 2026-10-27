from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from ..config import settings
from ..database import get_db
from ..models import Admin, User
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2 = OAuth2PasswordBearer(tokenUrl="/api/auth/login")
def hash_password(value: str): return pwd.hash(value)
def verify_password(raw: str, hashed: str): return pwd.verify(raw, hashed)
def create_token(subject: int, role: str):
    payload = {"sub": str(subject), "role": role, "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm="HS256")
def current_claims(token: str = Depends(oauth2)):
    try: return jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
    except JWTError: raise HTTPException(status_code=401, detail="Invalid or expired access token")
def current_user(claims=Depends(current_claims), db: Session = Depends(get_db)):
    if claims.get("role") != "user": raise HTTPException(403, "User access required")
    user = db.get(User, int(claims["sub"]))
    if not user or user.status != "APPROVED": raise HTTPException(403, "Approved user access required")
    return user
def current_admin(claims=Depends(current_claims), db: Session = Depends(get_db)):
    if claims.get("role") != "admin": raise HTTPException(403, "Administrator access required")
    admin = db.get(Admin, int(claims["sub"]))
    if not admin: raise HTTPException(401, "Administrator not found")
    return admin

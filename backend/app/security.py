import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .config import get_settings
from .database import get_database, is_connected

security = HTTPBearer(auto_error=False)
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 480

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, password_hash: str) -> bool:
    try: return bcrypt.checkpw(password.encode(), password_hash.encode())
    except (ValueError, TypeError): return False

def create_access_token(user_id: str) -> str:
    now=datetime.now(timezone.utc)
    payload={"sub":user_id,"iat":now,"exp":now+timedelta(minutes=ACCESS_TOKEN_MINUTES)}
    return jwt.encode(payload,get_settings().jwt_secret,algorithm=ALGORITHM)

def get_current_user(credentials: HTTPAuthorizationCredentials=Depends(security)):
    if credentials is None:
        raise HTTPException(401,"Authentication required",headers={"WWW-Authenticate":"Bearer"})
    try:
        payload=jwt.decode(credentials.credentials,get_settings().jwt_secret,algorithms=[ALGORITHM])
        uid=payload.get("sub")
        if not uid or not ObjectId.is_valid(uid): raise ValueError()
    except (jwt.ExpiredSignatureError,jwt.InvalidTokenError,ValueError):
        raise HTTPException(401,"Invalid or expired token",headers={"WWW-Authenticate":"Bearer"})
    if not is_connected(): raise HTTPException(503,"MongoDB is not connected")
    user=get_database()["users"].find_one({"_id":ObjectId(uid)},{"password_hash":0})
    if not user: raise HTTPException(401,"User not found",headers={"WWW-Authenticate":"Bearer"})
    user["id"]=str(user.pop("_id")); return user

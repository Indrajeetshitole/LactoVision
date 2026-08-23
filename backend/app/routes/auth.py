from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_database, is_connected
from ..schemas.auth import *
from ..security import create_access_token,get_current_user,hash_password,verify_password
router=APIRouter(prefix="/auth",tags=["Authentication"])
def public_user(u): return UserResponse(id=str(u.get("_id",u.get("id"))),full_name=u["full_name"],email=u["email"],role=u["role"])
@router.post("/register",response_model=AuthResponse,status_code=201)
def register(p:RegisterRequest):
    if not is_connected(): raise HTTPException(503,"MongoDB is not connected")
    users=get_database()["users"]; email=p.email.lower()
    if users.find_one({"email":email}): raise HTTPException(409,"An account with this email already exists")
    now=datetime.now(timezone.utc); doc={"full_name":p.full_name.strip(),"email":email,"password_hash":hash_password(p.password),"role":p.role,"created_at":now,"updated_at":now}
    r=users.insert_one(doc); doc["_id"]=r.inserted_id
    return AuthResponse(access_token=create_access_token(str(r.inserted_id)),user=public_user(doc))
@router.post("/login",response_model=AuthResponse)
def login(p:LoginRequest):
    if not is_connected(): raise HTTPException(503,"MongoDB is not connected")
    u=get_database()["users"].find_one({"email":p.email.lower()})
    if not u or not verify_password(p.password,u["password_hash"]): raise HTTPException(401,"Invalid email or password",headers={"WWW-Authenticate":"Bearer"})
    return AuthResponse(access_token=create_access_token(str(u["_id"])),user=public_user(u))
@router.get("/me",response_model=UserResponse)
def me(u=Depends(get_current_user)): return UserResponse(**u)
@router.post("/logout",response_model=MessageResponse)
def logout(u=Depends(get_current_user)): return MessageResponse(message="Logged out successfully")

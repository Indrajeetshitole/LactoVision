from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from ..database import get_database
from ..schemas.farm import *
from ..security import get_current_user
router=APIRouter(prefix="/farms",tags=["Farms"])
def oid(v):
    if not ObjectId.is_valid(v): raise HTTPException(400,"Invalid farm id")
    return ObjectId(v)
def out(d): return FarmResponse(id=str(d["_id"]),user_id=str(d["user_id"]),farm_name=d["farm_name"],owner=d["owner"],location=d["location"],contact=d["contact"],farm_type=d["farm_type"],number_of_cows=d["number_of_cows"])
@router.post("",response_model=FarmResponse,status_code=201)
def create(p:FarmCreate,u=Depends(get_current_user)):
    now=datetime.now(timezone.utc); d=p.model_dump(); d.update(user_id=ObjectId(u["id"]),created_at=now,updated_at=now); r=get_database()["farms"].insert_one(d); d["_id"]=r.inserted_id; return out(d)
@router.get("",response_model=list[FarmResponse])
def list_all(u=Depends(get_current_user)):
    return [out(d) for d in get_database()["farms"].find({"user_id":ObjectId(u["id"])}).sort("created_at",-1)]
@router.get("/{farm_id}",response_model=FarmResponse)
def get_one(farm_id:str,u=Depends(get_current_user)):
    d=get_database()["farms"].find_one({"_id":oid(farm_id),"user_id":ObjectId(u["id"])})
    if not d: raise HTTPException(404,"Farm not found")
    return out(d)
@router.put("/{farm_id}",response_model=FarmResponse)
def update(farm_id:str,p:FarmUpdate,u=Depends(get_current_user)):
    q={"_id":oid(farm_id),"user_id":ObjectId(u["id"])}; r=get_database()["farms"].update_one(q,{"$set":{**p.model_dump(),"updated_at":datetime.now(timezone.utc)}})
    if not r.matched_count: raise HTTPException(404,"Farm not found")
    return out(get_database()["farms"].find_one(q))

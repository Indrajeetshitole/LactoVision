from datetime import datetime, timezone
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query
from ..database import get_database
from ..schemas.cow import *
from ..security import get_current_user
router=APIRouter(prefix="/cows",tags=["Cattle"])
def oid(v,label="id"):
    if not ObjectId.is_valid(v): raise HTTPException(400,f"Invalid {label}")
    return ObjectId(v)
def out(d): return CowResponse(id=str(d["_id"]),user_id=str(d["user_id"]),cow_id=d["cow_id"],name=d["name"],breed=d["breed"],age=d["age"],weight=d["weight"],lactation_stage=d["lactation_stage"],parity=d["parity"],health_status=d["health_status"],farm_id=str(d["farm_id"]))
def ensure_farm(fid,uid):
    if not get_database()["farms"].find_one({"_id":oid(fid,"farm id"),"user_id":ObjectId(uid)}): raise HTTPException(404,"Farm not found or not owned by current user")
@router.post("",response_model=CowResponse,status_code=201)
def create(p:CowCreate,u=Depends(get_current_user)):
    ensure_farm(p.farm_id,u["id"]); cows=get_database()["cows"]
    if cows.find_one({"cow_id":p.cow_id,"user_id":ObjectId(u["id"])}): raise HTTPException(409,"Cow ID already exists for this user")
    d=p.model_dump(); d.update(farm_id=oid(p.farm_id,"farm id"),user_id=ObjectId(u["id"])); now=datetime.now(timezone.utc); d.update(created_at=now,updated_at=now); r=cows.insert_one(d); d["_id"]=r.inserted_id
    n=cows.count_documents({"farm_id":d["farm_id"],"user_id":d["user_id"]}); get_database()["farms"].update_one({"_id":d["farm_id"],"user_id":d["user_id"]},{"$set":{"number_of_cows":n,"updated_at":now}}); return out(d)
@router.get("",response_model=list[CowResponse])
def list_all(search:str|None=Query(None),breed:str|None=Query(None),farm_id:str|None=Query(None),u=Depends(get_current_user)):
    q={"user_id":ObjectId(u["id"])}
    if search: q["$or"]=[{"cow_id":{"$regex":search,"$options":"i"}},{"name":{"$regex":search,"$options":"i"}},{"breed":{"$regex":search,"$options":"i"}}]
    if breed: q["breed"]={"$regex":breed,"$options":"i"}
    if farm_id: q["farm_id"]=oid(farm_id,"farm id")
    return [out(d) for d in get_database()["cows"].find(q).sort("created_at",-1)]
@router.get("/{cow_id}",response_model=CowResponse)
def get_one(cow_id:str,u=Depends(get_current_user)):
    d=get_database()["cows"].find_one({"_id":oid(cow_id,"cow id"),"user_id":ObjectId(u["id"])})
    if not d: raise HTTPException(404,"Cow not found")
    return out(d)
@router.put("/{cow_id}",response_model=CowResponse)
def update(cow_id:str,p:CowUpdate,u=Depends(get_current_user)):
    ensure_farm(p.farm_id,u["id"]); coid=oid(cow_id,"cow id"); q={"_id":coid,"user_id":ObjectId(u["id"])}; r=get_database()["cows"].update_one(q,{"$set":{**p.model_dump(exclude={"farm_id"}),"farm_id":oid(p.farm_id,"farm id"),"updated_at":datetime.now(timezone.utc)}})
    if not r.matched_count: raise HTTPException(404,"Cow not found")
    return out(get_database()["cows"].find_one(q))
@router.delete("/{cow_id}")
def delete(cow_id:str,u=Depends(get_current_user)):
    cows=get_database()["cows"]; q={"_id":oid(cow_id,"cow id"),"user_id":ObjectId(u["id"])}; d=cows.find_one(q)
    if not d: raise HTTPException(404,"Cow not found")
    cows.delete_one(q); now=datetime.now(timezone.utc); n=cows.count_documents({"farm_id":d["farm_id"],"user_id":ObjectId(u["id"])}); get_database()["farms"].update_one({"_id":d["farm_id"],"user_id":ObjectId(u["id"])},{"$set":{"number_of_cows":n,"updated_at":now}}); return {"message":"Cow deleted successfully"}

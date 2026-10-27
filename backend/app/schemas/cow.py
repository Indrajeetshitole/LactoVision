from pydantic import BaseModel, Field
class CowCreate(BaseModel):
    cow_id:str=Field(min_length=1,max_length=50); name:str=Field(min_length=1,max_length=100)
    breed:str=Field(min_length=1,max_length=100); age:float=Field(gt=0,le=40); weight:float=Field(gt=0,le=1500)
    lactation_stage:str=Field(min_length=1,max_length=50); parity:int=Field(ge=0,le=20)
    health_status:str=Field(min_length=1,max_length=50); farm_id:str=Field(min_length=1)
class CowUpdate(CowCreate): pass
class CowResponse(CowCreate): id:str; user_id:str

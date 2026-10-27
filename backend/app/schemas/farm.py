from pydantic import BaseModel, Field
class FarmCreate(BaseModel):
    farm_name:str=Field(min_length=2,max_length=120); owner:str=Field(min_length=2,max_length=120)
    location:str=Field(min_length=2,max_length=200); contact:str=Field(min_length=3,max_length=40)
    farm_type:str=Field(min_length=2,max_length=80); number_of_cows:int=Field(default=0,ge=0)
class FarmUpdate(FarmCreate): pass
class FarmResponse(FarmCreate): id:str; user_id:str

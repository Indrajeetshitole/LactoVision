from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .config import FEATURES
from .predict import predict_milk_yield
from .recommendations import generate_recommendations

router=APIRouter(prefix="/predict",tags=["AI Prediction"])

class PredictionRequest(BaseModel):
    breed:str; breed_group:str; sex:str="Female"; age_years:float=Field(gt=0); body_weight_kg:float=Field(gt=0); parity:int=Field(ge=0); lactation_number:int=Field(ge=0); days_in_milk:int=Field(ge=0); lactation_stage:str; days_since_calving:int=Field(ge=0); feed_type:str; feed_quantity_kg_dm:float=Field(gt=0); feed_frequency:int=Field(ge=0); morning_feed_kg:float=Field(ge=0); afternoon_feed_kg:float=Field(ge=0); evening_feed_kg:float=Field(ge=0); feed_quality_score:float=Field(ge=0); dry_matter_kg:float=Field(ge=0); crude_protein_g:float=Field(ge=0); metabolizable_energy_mj:float=Field(ge=0); ndf_g:float=Field(ge=0); fat_g:float=Field(ge=0); calcium_g:float=Field(ge=0); phosphorus_g:float=Field(ge=0); water_intake_l:float=Field(ge=0); body_condition_score:float=Field(ge=0); health_status:str; disease_status:str; disease_type:str="None"; symptoms:str="None"; vaccination_status:str="Up-to-date"; treatment_status:str="None"; body_temperature_c:float=Field(gt=0); heart_rate_bpm:float=Field(gt=0); respiration_rate_bpm:float=Field(gt=0); ambient_temperature_c:float; relative_humidity_pct:float=Field(ge=0,le=100); thi:float; weather_condition:str; season:str

@router.post("")
def predict(req:PredictionRequest):
    try:
        result=predict_milk_yield(req.model_dump())
        rec,alerts=generate_recommendations(req.model_dump(),result["predicted_milk_yield_kg"])
        result.update({"recommendations":rec,"health_alerts":alerts})
        return result
    except FileNotFoundError as e: raise HTTPException(status_code=503,detail=str(e))
    except Exception as e: raise HTTPException(status_code=400,detail=str(e))

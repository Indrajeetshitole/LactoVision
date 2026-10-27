from pydantic import BaseModel, EmailStr, Field
class RegisterRequest(BaseModel):
    full_name:str=Field(min_length=2,max_length=100)
    email:EmailStr
    password:str=Field(min_length=8,max_length=128)
    role:str=Field(default="farmer",pattern="^(farmer|veterinarian|admin)$")
class LoginRequest(BaseModel):
    email:EmailStr
    password:str=Field(min_length=1,max_length=128)
class UserResponse(BaseModel):
    id:str; full_name:str; email:EmailStr; role:str
class AuthResponse(BaseModel):
    access_token:str; token_type:str="bearer"; user:UserResponse
class MessageResponse(BaseModel): message:str

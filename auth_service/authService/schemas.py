from ninja.schema import Schema
from pydantic import EmailStr, field_validator, BaseModel
import re
from ninja import Field
from ninja.errors import ValidationError
from .models import Account
from typing import Any, Dict, Optional

class LoginDTO(Schema):
    email:EmailStr
    password:str=Field(..., min_length=7)

class RegisterDTO(Schema):
    email:EmailStr
    password:str
    phone_number:str=Field(..., min_length=7)
    first_name:str=Field(...,min_length=3)
    last_name:str=Field(...,min_length=3)
    country:str
    
    @field_validator("email" )
    @classmethod
    def verify_email(clx, email:EmailStr):
        if Account.objects.filter(email= email).exists():
            error = [
                {
                    "type": 'email',
                    "loc": ['email'],
                    "msg":"Email already exist"
                }
            ]
            raise ValidationError(errors=error)
        return email
    @field_validator("password" )
    @classmethod
    def validate_pass(cls, v):
        pattern = re.compile(
            r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?=\S+$).{8,20}$'
        )
        if not pattern.match(v):
            error = [
                {
                    "type": 'password',
                    "loc": ['password'],
                    "msg":'Password must be 8-20 characters long, include at least one digit, one lowercase letter, one uppercase letter, and one special character (no spaces).'
                }
            ]
            raise ValidationError(errors=error)
        return v
    @field_validator("phone_number" )
    @classmethod
    def validate_password(cls, v):
        pattern = re.compile(
            r"(?:([+]\d{1,4})[-.\s]?)?(?:[(](\d{1,3})[)][-.\s]?)?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})"
        )
        if not pattern.match(v):
            error = [
                {
                    "type": 'phone_number',
                    "loc": ['phone_number'],
                    "msg":'Incorrect Phone number format'
                }
            ]
            raise ValidationError(errors=error)
        return v
    
class InitiateRequestDTO(Schema):
    email:EmailStr
    token:Optional[str]=None
    otp:Optional[str]=None

class ChangePasswordDTO(Schema):
    password: str
    confirm_password:str
    
    @field_validator("password" )
    @classmethod
    def validate_pass(cls, v):
        pattern = re.compile(
            r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])(?=.*[^a-zA-Z0-9])(?=\S+$).{8,20}$'
        )
        if not pattern.match(v):
            error = [
                {
                    "type": 'password',
                    "loc": ['password'],
                    "msg":'Password must be 8-20 characters long, include at least one digit, one lowercase letter, one uppercase letter, and one special character (no spaces).'
                }
            ]
            raise ValidationError(errors=error)
        return v
            
class SetPinDTO(Schema):
    email: EmailStr
    pin: int=Field(...,max_length=4)

class AuthResponse(Schema):
    email:EmailStr
    username:str
    first_name:str
    last_name:str
    phone_number:str
    country:str
    
    class Config:
        from_attributes = True

class KafkaMessageModel(BaseModel):
    actions: str
    data: dict

class ResponserMessage(Schema):
    status: int
    message: str
    data: Any=None
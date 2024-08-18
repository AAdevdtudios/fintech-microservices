from authService.schemas import AuthResponse, ChangePasswordDTO, LoginDTO, RegisterDTO, ResponserMessage, InitiateRequestDTO, SetPinDTO
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password, check_password
from ninja_jwt.tokens import RefreshToken
from authService.models import Account
from authService.utils import create_token,verify_token
import pyotp

def login_user_services(request, loginDTO:LoginDTO)->ResponserMessage:
    try:
        values ={}
        user = authenticate(request, email=loginDTO.email, password=loginDTO.password)
        if user:
            tokens = RefreshToken.for_user(user)
            account = Account.objects.get(id=user.pk)
            if not account.is_verified:
                values["url"]= create_token(account)
            values["refresh_token"] = str(tokens)
            values["access_token"] = str(tokens.access_token)
            return ResponserMessage(status=200, message="Welcome back to Splice", data=values)
        raise Exception("User not registered")
    except Exception as e:
        return ResponserMessage(status=400, message= str(e))
    
def register_user_services(registerDTO:RegisterDTO)->ResponserMessage:
    try:
        req = registerDTO.model_dump()
        user = Account.objects.create_user(**req)
        validate_url = create_token(user)
        # return 200, {'status':200, 'message': f"Please check email to verify your account url is {validate_url}"}
        return ResponserMessage(status=200, message=f"Please check email to verify your account url is {validate_url}")
    except Exception as e:
        return ResponserMessage(status=400, message= str(e))

def verify_user_services(tokenId:str, token:str)->ResponserMessage:
    value = verify_token(uid64=tokenId, token=token)
    if not value:
        # return 400, {'status':400, 'message': "Token not valid"}
        return ResponserMessage(status=400, message="Token not valid")
    # return 200, {'status':200, 'message': "Welcome to Splice"}
    return ResponserMessage(status=200, message="Welcome to Splice")

def initiate_reset_services(email:InitiateRequestDTO)->ResponserMessage:
    try:
        value= {}
        value["token"] = pyotp.random_base32()
        totp = pyotp.TOTP(value["token"], interval=60)
        print(totp.now())
    except Exception as ex:
        print(ex)
    return ResponserMessage(status=200, message="Email would be sent if you didn't get the any email from user you haven't registered", data=value)

def validate_reset_otp_services(req:InitiateRequestDTO)->ResponserMessage:
    otp = pyotp.TOTP(req.token, interval=60)
    print(otp.verify(req.otp))
    if otp.verify(req.otp):
        values ={}
        user = Account.objects.get(email=req.email)
        tokens = RefreshToken.for_user(user)
        # values["refresh_token"] = str(tokens)
        values["access_token"] = str(tokens.access_token)
        
        return ResponserMessage(status=200, message="OTP is valid",data=values)
    return ResponserMessage(status=400, message="OTP is incorrect",)

def change_user_password_service(userEmail:str, resetDTO:ChangePasswordDTO)->ResponserMessage:
    if resetDTO.confirm_password != resetDTO.password:
        return ResponserMessage(status=400, message="Password doesn't match")
    user = Account.objects.get(email=userEmail)
    user.set_password(resetDTO.password)
    user.save()
    return ResponserMessage(status=200, message="Password change successfully")

def get_user_service(userEmail:str)->ResponserMessage:
    user = Account.objects.get(email = userEmail)
    v= AuthResponse.from_orm(user)
    return ResponserMessage(status=200, message="Successful", data=v)

def set_pin_service(setPin:SetPinDTO)->ResponserMessage:
    user = Account.objects.get(email=setPin.email)
    user.pin = make_password(str(setPin.pin))
    user.save()
    return ResponserMessage(status=200, message="Successful")

def login_pin_service(setPin:SetPinDTO)->ResponserMessage:
    user = Account.objects.get(email=setPin.email)
    check_pin = check_password(str(setPin.pin), user.pin)
    if check_pin:
        values={}
        tokens = RefreshToken.for_user(user)
        values["refresh_token"] = str(tokens)
        values["access_token"] = str(tokens.access_token)
        return ResponserMessage(status=200, message="Successful", data=values)
    return ResponserMessage(status=400, message="Pin is incorrect or badly formatted")
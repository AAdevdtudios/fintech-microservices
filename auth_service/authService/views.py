from ninja import NinjaAPI
from authService.services import change_user_password_service, get_user_service, initiate_reset_services, login_pin_service, login_user_services, register_user_services, set_pin_service, validate_reset_otp_services, verify_user_services
from .schemas import ChangePasswordDTO, InitiateRequestDTO, RegisterDTO, ResponserMessage, LoginDTO, SetPinDTO
from ninja_jwt.authentication import JWTAuth
from ninja_jwt.tokens import RefreshToken

import json
from django.http import HttpResponse
from ninja.errors import ValidationError
from ninja_extra import exceptions

api = NinjaAPI(version='1.0',title="TScore Auth Service Api", auth=JWTAuth())

@api.exception_handler(ValidationError)
def validationError(request, exc):
    return HttpResponse(json.dumps({'status':400, 'error': exc.errors[0]['loc'][-1], 'massage': exc.errors[0]["msg"],}), status=400)

@api.exception_handler(exceptions.APIException)
def auth_exception_handler(request,exc):
    headers ={}
    if isinstance(exc.detail, (list,dict)):
        data = exc.detail
    else:
        data = {"detail": exc.detail}
    response =api.create_response(request, data, status=exc.status_code)
    for k, v in headers.items():
        response.setdefault(k,v)
    return response

@api.post("register/",auth=None,url_name="register", tags=["Authentication"], description="This route registers the user", response=ResponserMessage)
def register_user(request, registerDTO:RegisterDTO):
    res = register_user_services(registerDTO)
    return api.create_response(request, res, status=res.status)

@api.get("confirm-email/{tokenId}/{token}",url_name="confirm", tags=["Authentication"], description="This route takes care of verifying the user", response=ResponserMessage)
def verify_user(request, tokenId:str, token:str):
    res = verify_user_services(tokenId=tokenId, token=token)
    return api.create_response(request, res, status=res.status)

@api.post("login/", auth=None, url_name="login",tags=["Authentication"],description="This is login route for users", response=ResponserMessage)
def login_user(request, loginDTO:LoginDTO):
    res = login_user_services(request,loginDTO)
    return api.create_response(request, res, status=res.status)

@api.post("initiate-reset/",auth=None, url_name="reset",tags=["Authentication"],description="This is login route for users", response=ResponserMessage)
def initiate_reset(request, email:InitiateRequestDTO):
    res = initiate_reset_services(email)
    return api.create_response(request, res, status=res.status)

@api.post("verify-reset/", auth=None, tags=["Authentication"],url_name="verify", description="This endpoint is to verify a user", response=ResponserMessage)
def verify_reset(request, req:InitiateRequestDTO):
    res = validate_reset_otp_services(req)
    return api.create_response(request, res, status=res.status)

@api.post("change-password/", tags=["Authentication"], url_name="change-password", description="This endpoint is to change password authenticated users", response=ResponserMessage)
def change_password(request, req:ChangePasswordDTO):
    res = change_user_password_service(request.auth.email,req)
    return api.create_response(request, res, status=res.status)

@api.post("logout/", auth=None, url_name="logout", tags=["Authentication"], description="Logout A user")
def logout_user(request, refresh_token:str):
    RefreshToken(refresh_token).blacklist()
    return api.create_response(request, {"message":"Success"}, status=201)

@api.get("/user",tags=["User"],)
def getUser(request):
    res = get_user_service(userEmail=request.auth.email)
    return api.create_response(request, res, status=res.status)

@api.post("set-pin/", tags=["User"],url_name="set-pin", description="Set Users Pin")
def set_user_pin(request,setPin:SetPinDTO):
    res = set_pin_service(setPin)
    return api.create_response(request, res, status=res.status)

@api.post("login-pin/", tags=["User"],url_name="login-pin", description="Login Users with Pin")
def login_user_pin(request,setPin:SetPinDTO):
    res = login_pin_service(setPin)
    return api.create_response(request, res, status=res.status)
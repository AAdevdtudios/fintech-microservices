from authService.models import Account
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str
from django.shortcuts import get_object_or_404

def create_token(user:Account)->str:
    uid64 = urlsafe_base64_encode(smart_bytes(user.id))
    token = PasswordResetTokenGenerator().make_token(user)
    return uid64+"/"+token

def verify_token(uid64: str, token:str,)->bool|str:
    try:
        user_id = smart_str(urlsafe_base64_decode(uid64))
        user = get_object_or_404(Account, id=user_id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            return False
        user.is_verified = True
        user.save()
        return True
    except:
        return False

def initiate_token(user:Account):
    return PasswordResetTokenGenerator().make_token(user)

def send_email():
    pass

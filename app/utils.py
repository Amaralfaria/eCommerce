from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

def get_jwt_tokens(usuario):
    token = AccessToken.for_user(usuario)
    refresh = RefreshToken.for_user(usuario)

    return {"acess": str(token), "refresh":str(refresh)}
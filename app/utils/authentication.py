from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework_jwt.settings import api_settings


class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        print("request.data==================", request.data)
        if 'token' in request.data:
            try:
                token = request.data['token']
                print("token===>", token)
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                user_dict = jwt_decode_handler(token)
                return user_dict, token
            except Exception as ex:
                raise exceptions.AuthenticationFailed(detail={'code': 401, 'msg': 'token已过期'})
        else:
            raise exceptions.AuthenticationFailed(detail={'code': 400, 'msg': '缺少token'})

    def authenticate_header(self, request):
        pass

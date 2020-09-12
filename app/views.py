from django.shortcuts import render
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import Permission, User
from app import models
from rest_framework.versioning import URLPathVersioning
from rest_framework.request import Request
from app.utils import throttle
# Create your views here.

class APIResponse(Response):
    def __init__(self, data_status=0, data_msg='ok', results=None
                 , http_status=None, headers=None, exception=False, **kwargs):
        # data的初始状态：状态码与状态信息
        data = {
            'stauts': data_status,
            'msg': data_msg,
        }
        # data的响应数据体
        # results可能是False、0等数据，这些数据某些情况下也会作为合法数据返回
        if results is not None:
            data['results'] = results
        # data响应的其他内容
        # if kwargs is not None:
        #     for k, v in kwargs:
        #         setattr(data, k, v)
        data.update(kwargs)

        # 重写父类的Response的__init__方法
        super().__init__(data=data, status=http_status, headers=headers, exception=exception)


# 第一个请求
class LoginJWTAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()
    throttle_classes = [throttle.VisitThrottle]

    def get(self, request, *args, **kwargs):
        # 获取版本
        print(request.version)
        # 获取版本管理的类
        print(request.versioning_scheme)
        print(request.query_params.get("version",None))
        # 反向生成URL
        reverse_url = request.versioning_scheme.reverse('getAuthToken', request=request)
        print(reverse_url)
        return APIResponse(1, '密码错误')

    def post(self, request, *args, **kwargs):
        # username可能携带的不止是用户名，可能还是用户的其它唯一标识 手机号 邮箱
        print(request.data)
        appid = request.data.get('appid', None)
        secret = request.data.get('secret', None)
        if appid is None or secret is None:
            return APIResponse(-1, 'appid或secret不能为空!')
        appmanager = models.appManager.objects.filter(appid=appid, secret=secret, state=1)
        if appmanager is None:
            return APIResponse(-2, 'appid或secret无效,请检查秘钥!')
        user = User.objects.filter(username=appid).first()
        if user is None:
            return APIResponse(-2, 'appid或secret输入有误')
        # 获得用户后，校验密码并签发token
        if not user.check_password(secret):
            return APIResponse(-3, '密码错误')
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return APIResponse(0, 'ok', results={
            'username': user.username,
            'token': token
        })

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings
from rest_framework.response import Response

from rest_framework import serializers
from rest_framework.views import APIView
from django.contrib.auth.models import Permission, User
from app import models
from rest_framework.versioning import URLPathVersioning
from rest_framework.request import Request
from app.utils import throttle
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


# Create your views here.

def h(request):
    return render(request, 'h.html')


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
        print(request.query_params.get("version", None))
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


class PasswordValidator(object):
    def __init__(self, base):
        self.base = str(base)

    def __call__(self, value):
        if value != self.base:
            message = 'This field must be %s.' % self.base
            raise serializers.ValidationError(message)

    def set_context(self, serializer_field):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # 执行验证之前调用,serializer_fields是当前字段对象
        pass


class ModelBossInfoSerializer(serializers.ModelSerializer):
    # 自定义字段
    xxxxxxx = serializers.CharField(source="get_gender_display")
    mmmmmmm = serializers.SerializerMethodField()  # 自定义函数显示

    class Meta:
        model = models.bossInfo
        # fields = "__all__"
        fields = ['name', 'age', 'xxxxxxx', 'mmmmmmm', 'rls', 'sports', "likeFruit", "userUrl", ]
        depth = 2
        # extra_kwargs = {'user': {'min_length': 6}, 'pwd': {'validators': [PasswordValidator(666), ]}}

    # 函数名必须以get_开头  否则会报错
    def get_mmmmmmm(self, row):
        return ["A", "B", "C"]


class StandardResultsSetPagination(LimitOffsetPagination):
    # 默认每页显示的数据条数
    default_limit = 10
    # URL中传入的显示数据条数的参数
    limit_query_param = 'limit'
    # URL中传入的数据位置的参数
    offset_query_param = 'offset'
    # 最大每页显得条数
    max_limit = None


# 继承关系
# View 基类
# 复杂的逻辑继承 GenericViewSet 或 APIView
# 基本的增删改查就继承 ModelViewSet

class GetBossInfo(APIView):
    # 获取信息
    def get(self, request, *args, **kwargs):
        print(request.version)
        bInfos = models.bossInfo.objects.all().order_by('id')
        ser = ModelBossInfoSerializer(instance=bInfos, many=True)  # 全部返回生成环境 基本不可能

        # 实例化分页对象，获取数据库中的分页数据
        paginator = StandardResultsSetPagination()
        page_user_list = paginator.paginate_queryset(bInfos, self.request, view=self)

        # 生成分页和数据
        response = paginator.get_paginated_response(ser.data)

        # return APIResponse(0, 'ok', results={'infos': ser.data,})
        return response

    # 提交信息
    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.user["username"])
        bInfos = models.bossInfo.objects.all()
        ser = ModelBossInfoSerializer(instance=bInfos, many=True)
        return APIResponse(0, 'ok', results={
            'infos': ser.data,
        })

    # 更新信息
    def put(self, request, *args, **kwargs):
        return APIResponse(0, 'ok', results={
            'method': request.method.upper(),
        })

    # 删除信息
    def delete(self, request, *args, **kwargs):
        return APIResponse(0, 'ok', results={
            'method': request.method.upper(),
        })


from rest_framework.viewsets import ModelViewSet


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.role
        fields = "__all__"


class UserViewSet(ModelViewSet):
    queryset = models.role.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination

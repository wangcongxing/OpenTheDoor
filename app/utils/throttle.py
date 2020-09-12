from rest_framework.throttling import SimpleRateThrottle
import time

# 匿名用户认证规则
class VisitThrottle(SimpleRateThrottle):
    scope = "anon"
    def get_cache_key(self, request, view):
        return self.get_ident(request)

# 授权用户认证规则
class UserThrottle(SimpleRateThrottle):
    scope = "user" #当key用的
    def get_cache_key(self, request, view):
        return request.user  # 认证通过后，认证方法authenticate的返回值之一


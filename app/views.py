from django.shortcuts import render
from django.http import HttpResponse
import logging

logger = logging.getLogger(__name__)
# Create your views here.

# 第一个请求
# 直接返回响应体
def helloWorld(request):
    return HttpResponse("very nice")


# 返回html页面
def helloH5(request):
    logger.error('Something went wrong!')
    return render(request, "helloH3.html")

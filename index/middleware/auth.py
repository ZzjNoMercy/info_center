from django.shortcuts import HttpResponse, redirect, reverse
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):

    @staticmethod
    def process_request(request):
        # 读取session信息
        if 'login' in request.path or 'sign' in request.path:
            return
        infos = request.session.get("info")
        if infos:
            return
        return redirect(reverse("index:login"))

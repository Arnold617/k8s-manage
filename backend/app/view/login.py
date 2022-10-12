from django.views import View
import json
from django.shortcuts import render, HttpResponse


class Login(View):

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        # print(username, password)
        # print(request.user)

        if username == "admin" and password == "123456":
            res = {"code": 200, "msg": "请求成功", "user": {
                "avatar": "https://raw.githubusercontent.com/taylorchen709/markdown-images/master/vueadmin/user.png",
                "id": 1, "name": "张三", "username": "admin"}}
            return HttpResponse(json.dumps(res))
        else:
            res = {"code": 400, "msg": "用户名密码错误", "user": {}}
            return HttpResponse(json.dumps(res))
import re

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from user.models import User


# Create your views here.


def register(request):
    '''显示注册页面'''
    return render(request, 'register.html')


def register_handle(request):
    '''注册逻辑处理'''

    # 获取提交的参数
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
    cpwd = request.POST.get('cpwd')

    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请同意天天生鲜用户使用协议'})

    # 非空校验
    if not all([username, password, email]):
        return render(request, 'register.html', {'errmsg': '数据不完整'})

    # 校验两次密码是否一致
    if password != cpwd:
        return render(request, 'register.html', {'errmsg': '两次密码不一致'})

    # 校验用户名是否重复
    try:
        user = User.objects.get(username__exact=username)
    except User.DoesNotExist:
        user = None

    if user:
        # 用户已存在
        return render(request, 'register.html', {'errmsg': '用户已存在'})

    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

    registerUser = User.objects.create_user(username, email, password)
    registerUser.is_active = 0
    registerUser.save()

    # 注册成功，重定向到首页
    return redirect(reverse('goods:index'))

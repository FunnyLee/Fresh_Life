import re

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import View

from user.models import User
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from fresh_life import settings
from celery_tasks.tasks import send_register_active_email

# Create your views here.
from utils.fdfs.mixin import LoginRequiredMixin


class RegisterView(View):
    '''注册类视图'''

    def get(self, request):
        '''显示注册页面'''
        return render(request, 'register.html')

    def post(self, request):
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

        # 发送激活邮件
        # 加密用户id
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': registerUser.id}
        token = serializer.dumps(info)
        # 这里需要解码
        token = bytes.decode(token)

        '''
        subject = '天天生鲜欢迎你'
        addr = "http://127.0.0.1:8000/user/active/%s" % token
        html_message = '<h2>天天生鲜激活邮件</h2> <br/> <a href="' + addr + '"> ' + addr + '</a>'

        receive_list = [email]

        # 发送邮件，这个方法是同步返回的，可能会造成阻塞
        send_mail(subject, '', settings.EMAIL_FROM, receive_list, html_message=html_message)
        '''

        # 使用celery发送邮件
        send_register_active_email.delay(email, token)

        # 注册成功，重定向到首页
        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''激活类视图'''

    def get(self, request, token):
        serializer = Serializer(settings.SECRET_KEY, 3600)

        try:
            # 对token进行解密，得到user_id
            info = serializer.loads(token)
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 重定向跳转到登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            return HttpResponse('激活邮件已过期')


class LoginView(View):
    '''登录类视图'''

    def get(self, request):
        '''显示登录页面'''
        cookies = request.COOKIES;

        if 'username' in cookies:
            username = cookies.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''

        return render(request, 'login.html', {'username': username, 'checked': checked})

    def post(self, request):
        '''登录逻辑校验'''

        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 非空校验
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 使用django内置的认证功能
        user = authenticate(username=username, password=password)

        if user is not None:
            # 用户名和密码正确

            # 判断是否为激活用户
            if user.is_active:
                # django内置方法保存session,保存登录状态
                login(request, user)

                # 获取登录后要跳转的url(得到get请求中next的url)，默认是跳转到首页
                # http://127.0.0.1:8000/user/login?next=/user/order
                next_url = request.GET.get('next',reverse('goods:index'))
                response = redirect(next_url)

                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=3600 * 12 * 7)
                else:
                    response.delete_cookie('username')

                # 跳转到首页
                return response

            else:
                return render(request, 'login.html', {'errmsg': '用户未激活'})

        else:
            # 用户名和密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})


class UserInfoView(View):
    '''用户信息View'''

    def get(self, request):
        return render(request, 'user_center_info.html')


class UserOrderView(LoginRequiredMixin,View):
    '''用户订单View'''

    def get(self, request):
        return render(request, 'user_center_order.html')


class UserAddressView(LoginRequiredMixin, View):
    '''用户地址View'''

    def get(self, request):
        return render(request, 'user_center_site.html')

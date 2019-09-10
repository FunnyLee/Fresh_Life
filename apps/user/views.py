from django.shortcuts import render


# Create your views here.

def register(request):
    '''显示注册页面'''
    return render(request, 'register.html')


def register_handle(request):
    '''注册逻辑处理'''

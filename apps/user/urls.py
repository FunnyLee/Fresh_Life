from django.conf.urls import include, url

from apps.user import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),  # 注册页面
    url(r'^register_handler$', views.register_handle, name='register_handler'),  # 注册逻辑处理
]

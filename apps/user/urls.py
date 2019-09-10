from django.conf.urls import include, url

from apps.user import views

urlpatterns = [
    url(r'^register$', views.register, name='register'),  # 注册页面
]

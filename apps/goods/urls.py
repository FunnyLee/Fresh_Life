from django.conf.urls import include, url

from apps.goods import views

urlpatterns = [
    url(r'', views.index, name='index'),  # 显示首页
]

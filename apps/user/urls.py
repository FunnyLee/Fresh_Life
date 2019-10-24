from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from apps.user import views
from apps.user.views import RegisterView, ActiveView, LoginView, UserInfoView, UserOrderView, UserAddressView

urlpatterns = [
    url(r'^register$', RegisterView.as_view(), name='register'),  # 注册
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 激活
    url(r'^login$', LoginView.as_view(), name='login'),  # 登录

    url(r'^info$', login_required(UserInfoView.as_view()), name='info'),  # 用户中心-信息页
    url(r'^order$', UserOrderView.as_view(), name='order'),  # 用户中心-订单页
    url(r'^address$', UserAddressView.as_view(), name='address'),  # 用户中心-地址页
]

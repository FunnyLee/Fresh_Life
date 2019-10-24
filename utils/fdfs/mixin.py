from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    '''封装login_required方法'''

    @classmethod
    def as_view(cls, **kwargs):
        # 调用父类的as_view方法
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)

        return login_required(view)



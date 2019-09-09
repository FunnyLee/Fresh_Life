from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel


class User(AbstractUser, BaseModel):
    '''用户模型类'''

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        # 指定模型的复数形式是什么,如果不指定Django会自动在模型名称后加一个’s’
        verbose_name_plural = verbose_name

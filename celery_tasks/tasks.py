# 使用celery异步任务
import django
from celery import Celery
import time
import os

# 创建celery对象，指定redis8号数据库作为中间人
from django.conf import settings
from django.core.mail import send_mail

# worker需要手动初始化django项目，让settings.EMAIL_FROM可以使用
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fresh_life.settings")
django.setup()


app = Celery('celery_tasks.tasks', broker='redis://127.0.0.1:6379/8')


# 定义任务函数
@app.task
def send_register_active_email(email, token):
    subject = '天天生鲜欢迎你'
    addr = "http://127.0.0.1:8000/user/active/%s" % token
    html_message = '<h2>天天生鲜激活邮件</h2> <br/> <a href="' + addr + '"> ' + addr + '</a>'

    receive_list = [email]
    send_mail(subject, '', settings.EMAIL_FROM, receive_list, html_message=html_message)
    time.sleep(5)

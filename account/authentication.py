# coding=utf-8
from django.contrib.auth.models import User


class EmailAuthBackend(object):
    '''
    用邮箱作为认证账号
    包含authenticate和get_user两个方法的类就可以是一个认证后台
    '''
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):   # check_password方法时User模型内置的
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

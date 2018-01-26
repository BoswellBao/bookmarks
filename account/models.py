from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)   # AUTH_USER_MODEL = 'auth.User'
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)

class Contact(models.Model):
    user_from = models.ForeignKey(User, related_name='rel_from_set')
    user_to = models.ForeignKey(User, related_name='rel_to_set')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

# 给User模型动态增加一个字段 following：我关注了哪些人。 followers：哪些人关注了我
User.add_to_class('following', models.ManyToManyField('self',   # 这里是填另一个模型的名称，因为例子是用户与用户的关系，因此用self即可
                                                      through=Contact,
                                                      related_name='followers',
                                                      symmetrical=False))   # 非对称：“甲关注乙，乙不会自动关注甲”
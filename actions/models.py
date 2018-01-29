from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class Action(models.Model):
    user = models.ForeignKey(User, related_name='actions', db_index=True)
    # 动作描述
    verb = models.CharField(max_length=255)
    # 外键关联ContentType
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj')
    # 存储被关联对象的primary key
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    # 通过前面两个字段来确定关联的对象
    target = GenericForeignKey('target_ct', 'target_id')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    
# coding=utf-8
import datetime

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

from .models import Action


def create_action(user, verb, target=None):
    '''
    有了这个函数，可以在任何地方随时创建一个活动流
    :param user:
    :param verb:
    :param target:
    :return:
    '''

    # 检查一分钟内是否有相同的操作
    now = timezone.now()
    last_minute = now - timezone.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte = last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:
        # 没有找到动作
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
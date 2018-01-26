# coding=utf-8
from django.http import HttpResponseBadRequest


def ajax_required(f):
    '''
    为视图添加，验证请求是不是ajax请求的功能
    :param f:
    :return:
    '''
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        return f(request, *args, **kwargs)
    wrap.__doc__=f.__doc__
    wrap.__name__=f.__name__
    return wrap
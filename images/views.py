from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .forms import ImageCreateForm
from .models import Image
from common.decorators import ajax_required
from actions.utils import create_action


@login_required
def image_create(request):
    """
    视图：用JS书签创建一个图像
    """
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            try:
                cd = form.cleaned_data
                new_item = form.save(commit=False)
                # 把当前用户依附到图片上
                new_item.user = request.user
                new_item.save()
                create_action(request.user, '给图片打标签', new_item)
                new_item.user_like.add(new_item.user)
                messages.success(request, 'Image added successfully')
                # 重定向到新添加图片的详细信息页面
                return redirect(new_item.get_absolute_url())
            except Exception as e:
                messages.error(request, "图片源地址有误！")

    else:
        # 通过GET方法的数据创建表单，get的url是bookmarklet.js中拼接的，其中包括url和title参数
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/image-create.html', {'section': 'images', 'form': form})

def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    print(image.user_like.count())
    return render(request, 'images/image/detail.html', {"section": 'images', 'image': image})

@ajax_required
@login_required   # 防止未登录的用户
@require_POST   # 只允许post方法请求使用改视图，不然返回一个HttpResponseNotAllowed对象（错误码：405）
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})

@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 15)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # 如果给的page不是整数就返回第一页
        images = paginator.page(1)
    except EmptyPage:
        # 如果请求时ajax并且页数超过范围就返回空，停止ajax分页
        if request.is_ajax():
            return HttpResponse()
        # 如果只是超过范围就返回最后一页
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        # 是ajax的话就在原来页面上继续加载
        return render(request, 'images/image/ajax_list.html', {'section':' images', 'images': images})
    # 非ajax请求就要重新加载页面
    return render(request, 'images/image/list.html', {'section': 'images', 'images': images})

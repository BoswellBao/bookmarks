from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm


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
                messages.success(request, 'Image added successfully')
                # 重定向到新添加图片的详细信息页面
                return redirect(new_item.get_absolute_url())
            except Exception as e:
                messages.error(request, "图片源地址有误！")

    else:
        # 通过GET方法的数据创建表单
        form = ImageCreateForm(data=request.GET)

    return render(request, 'images/image/image-create.html', {'section': 'images', 'form': form})

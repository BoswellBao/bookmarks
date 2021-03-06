# coding=utf-8
from django import forms
from .models import Image
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify


class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {
            'url': forms.HiddenInput,
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg','jpeg','png']
        extension = url.rsplit('.', 1)[1].lower()   # rsplit从右边开始分割
        if extension not in valid_extensions:
            raise forms.ValidationError("图片格式错误")

        return url   # 验证哪个字段就返回哪个字段

    def save(self, force_insert=False, force_update=False, commit=True):
        image_obj = super(ImageCreateForm, self).save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = "{}.{}".format(slugify(image_obj.title), image_url.split('.', 1)[1].lower())
        # 从给定的url中下载图片
        response = request.urlopen(image_url)
        image_obj.image.save(image_name, ContentFile(response.read()), save=False)   # 这个save方法是继承FieldFile类的save方法

        if commit:
            image_obj.save()
        return image_obj
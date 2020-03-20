from django.db import models


class IMG(models.Model):
    img = models.ImageField(upload_to='img')  # upload_to 指定图片存储的文件夹名称,上传文件后自动创建
    name = models.CharField(max_length=100)

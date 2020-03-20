from django.shortcuts import render
from .models import IMG
# http://127.0.0.1:8001/upload/media 访问地址,上传图片或文件

def uploadImg(request):
    if request.method == 'POST':
        new_img = IMG(
            img=request.FILES.get('img'),
            name=request.FILES.get('img').name  # ??
        )
        new_img.save()
    return render(request, 'img_tem/uploadimg.html')


def showImg(request):
    imgs = IMG.objects.all()
    content = {'img': imgs}
    for i in imgs:
        print(i.img.url)
    return render(request, 'img_tem/showimg.html', content)

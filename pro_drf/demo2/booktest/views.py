from django.http import JsonResponse
from django.views import View
from .models import BookInfo, HeroInfo
from .serializers import BookSerializer, HeroSerializer
from .serializers import BookModelSerializer
import json


class BooksView(View):
    def post(self, request):
        param_dict = json.loads(request.body.decode())

        # 1.将接收的数据赋给data参数
        serializer = BookSerializer(data=param_dict)
        # 2.验证
        if serializer.is_valid():
            # 验证成功===》创建对象
            book = serializer.save()

            serializer = BookSerializer(book)
            book_dict = serializer.data
            return JsonResponse(book_dict, status=201)
        else:
            # 验证失败
            return JsonResponse(serializer.errors)


class BookView(View):
    def get(self, request, pk):
        book = BookInfo.objects.get(pk=pk)

        # serializer = BookSerializer(book)
        # book_dict = serializer.data

        serializer = BookModelSerializer(book)
        book_dict = serializer.data

        return JsonResponse(book_dict)

    def put(self, request, pk):
        param_dict = json.loads(request.body.decode())

        book = BookInfo.objects.get(pk=pk)

        serializer = BookSerializer(book, data=param_dict)
        if serializer.is_valid():    ###is_valid() 注意有括号
            book = serializer.save()

            serializer = BookSerializer(book)
            book_dict = serializer.data
            return JsonResponse(book_dict, status=201)
        else:
            return JsonResponse(serializer.errors)


class HeroView(View):
    def get(self, request, pk):
        hero = HeroInfo.objects.get(pk=pk)

        serializer = HeroSerializer(hero)
        hero_dict = serializer.data

        return JsonResponse(hero_dict)

from .models import BookInfo
from django.http import JsonResponse, Http404
from django.views import View
import json
from .serializers import Book2Serializer


class BooksView(View):
    def get(self, request):
        '''
        查询所有
        '''
        # 处理
        book_list = BookInfo.objects.all()

        # 将book对象转换成字典
        '''
        {'code':***,'errmsg':***,'***_list':[{},{},...]}

        [
            {},
            {},
            ...
        ]
        pep8
        '''
        # book_dict_list = []
        # for book in book_list:
        #     book_dict_list.append({
        #         'id': book.id,
        #         'btitle': book.btitle,
        #         'bpub_date': book.bpub_date
        #     })
        book_serializer = Book2Serializer(book_list, many=True)
        book_dict_list = book_serializer.data

        # 响应
        return JsonResponse(book_dict_list, safe=False)

    def post(self, request):
        '''
        增加
        '''
        # 接收方式  GET,POST,body,此处是用body方式接收
        param_dict = json.loads(request.body.decode())
        btitle = param_dict.get('btitle')
        bpub_date = param_dict.get('bpub_date')

        # 验证  [书名和日期没有什么可验证的]

        # 处理
        book = BookInfo.objects.create(btitle=btitle, bpub_date=bpub_date)

        # 将对象转换成字典
        # book_dict = {
        #     'id': book.id,
        #     'btitle': book.btitle,
        #     'bpub_date': book.bpub_date
        # }
        book_serializer = Book2Serializer(book)
        book_dict = book_serializer.data

        # 响应
        return JsonResponse(book_dict, status=201)


'''
  {
    "bpub_date": "2019-5-29",
    "btitle": "西游记"
  }
'''


class BookView(View):
    def get(self, request, pk):
        '''
        根据主键查询一个对象

        '''
        #对于pk,本身路由中正则表达式中就有验证功能,所以不需要再对PK接收,验证
        # 处理
        try:
            book = BookInfo.objects.get(pk=pk)
        except:
            return Http404('数据不存在')

        # 将对象转换成字典
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date
        }

        # 响应
        return JsonResponse(book_dict)

    def put(self, request, pk):
        '''
        修改指定主键的对象
        '''
        # 接收
        param_dict = json.loads(request.body.decode())
        btitle = param_dict.get('btitle')
        bpub_date = param_dict.get('bpub_date')

        # 验证

        # 处理
        book = BookInfo.objects.get(pk=pk)
        book.btitle = btitle
        book.bpub_date = bpub_date
        book.save()

        # 将对象转换成字典
        book_dict = {
            'id': book.id,
            'btitle': book.btitle,
            'bpub_date': book.bpub_date,
        }

        # 响应
        return JsonResponse(book_dict, status=201)

    def delete(self, request, pk):
        '''
        删除指定主键的对象
        '''
        book = BookInfo.objects.get(pk=pk)
        book.delete()

        return JsonResponse({}, status=204)


from rest_framework.viewsets import ModelViewSet
from .serializers import BookSerializer


class BookModelViewSet(ModelViewSet):
    queryset = BookInfo.objects.all()
    serializer_class = BookSerializer

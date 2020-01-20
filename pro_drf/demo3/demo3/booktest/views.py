from rest_framework.views import APIView
from rest_framework.response import Response
from .models import BookInfo
from .serializers import BookModelSerializer
from rest_framework import status
from rest_framework import serializers
from rest_framework import mixins
from rest_framework.generics import GenericAPIView
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter


# 不同模型类，视图中不同的代码为：查询集，序列化器类型

class BooksView(APIView):
    def get(self, request):
        blist = BookInfo.objects.filter(pk__lt=5).order_by('-id')
        serializer = BookModelSerializer(blist, many=True)
        return Response(serializer.data)

    def post(self, request):
        param_dict = request.data

        serializer = BookModelSerializer(data=param_dict)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()

        serializer = BookModelSerializer(book)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


'''
    {
        "btitle": "红楼123",
        "bpub_date": "1980-05-01"
    }
'''


class BookView(APIView):
    def get(self, request, pk):
        try:
            book = BookInfo.objects.get(pk=pk)
        except:
            raise serializers.ValidationError('编号无效')

        serializer = BookModelSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        param_dict = request.data

        try:
            book = BookInfo.objects.get(pk=pk)
        except:
            raise serializers.ValidationError('编号无效')

        serializer = BookModelSerializer(book, data=param_dict)
        serializer.is_valid(raise_exception=True)
        book = serializer.save()

        serializer = BookModelSerializer(book)
        return Response(serializer.data, status=201)

    def delete(self, request, pk):
        try:
            book = BookInfo.objects.get(pk=pk)
        except:
            raise serializers.ValidationError('编号无效')
        book.delete()
        return Response(status=204)


class BooksGenericAPIView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class BookGenericAPIView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
    def get_queryset(self):
        return BookInfo.objects.all()

    def get_serializer_class(self):
        return BookModelSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)

    def put(self, request, pk):
        return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)


class BooksView2(generics.ListCreateAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer


class BookView2(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookInfo.objects.all()
    serializer_class = BookModelSerializer


class BooksViewSet(viewsets.ModelViewSet):
    '''
    list:
    查询指定条件的图书，可以分页
    '''
    # queryset = BookInfo.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

    # 过滤字段
    # filter_fields = ('btitle', 'bread')

    # 排序
    # filter_backends = [OrderingFilter]
    # ordering_fields = ('id', 'bread', 'bpub_date')

    def get_queryset(self):
        ordering = self.request.query_params.get('ordering')
        bread = self.request.query_params.get('bread')
        btitle = self.request.query_params.get('btitle')

        queryset = BookInfo.objects.filter(is_delete=False)

        if btitle:
            queryset = queryset.filter(btitle__contains=btitle)
        if bread:
            queryset = queryset.filter(bread=bread)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset

    @action(methods=['get'], detail=False)
    def hot(self, request):
        # 查询阅读量最高的两本图书
        hot_list = self.get_queryset().order_by('-bread')[0:2]

        serializer = self.get_serializer(hot_list, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def btitle(self, request, pk):
        # 获取指定图书的书名
        # request.query_params===>GET
        book = self.get_object()
        return Response({'btitle': book.btitle})

from rest_framework import serializers
from .models import BookInfo


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = '__all__'


class Book2Serializer(serializers.Serializer):
    id = serializers.IntegerField()
    btitle = serializers.CharField()
    bpub_date = serializers.DateField()
    bread = serializers.IntegerField()
    bcomment = serializers.IntegerField()

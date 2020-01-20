from rest_framework import serializers
from .models import BookInfo


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookInfo
        fields = ('id', 'btitle', 'bpub_date')
        read_only_fields = ('id',)
        extra_kwargs={
            'btitle':{
                'label':'书名',
                'help_text':'请输入书名'
            }
        }

    def validate_btitle(self, attr):
        if len(attr) < 3:
            raise serializers.ValidationError('书名长度必须大于3个字符')

        return attr

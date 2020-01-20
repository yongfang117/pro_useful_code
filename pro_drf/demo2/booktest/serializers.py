from rest_framework import serializers
from .models import BookInfo


class HeroRelatedSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    hname = serializers.CharField()


def check(value):
    # 验证value必须是偶数
    if value % 2 != 0:
        raise serializers.ValidationError('必须为偶数')


class BookSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    btitle = serializers.CharField(
        min_length=3,
        max_length=10,
        error_messages={
            'min_length': '书名必须大于3个字符串',
            'max_length': '书名必须小于10个字符串'
        },
        label='书名',
        help_text='请输入书名'
    )
    bpub_date = serializers.DateField(write_only=True)
    bread = serializers.IntegerField(
        min_value=10,
        max_value=100,
        required=False,
        validators=[check] ##不用加单引号
    )
    bcomment = serializers.IntegerField(
        min_value=10,
        max_value=100,
        required=False
    )
    # heroinfo_set====>heros
    # 1.主键
    # heros = serializers.PrimaryKeyRelatedField(read_only=True, many=True)
    # 2.字符串
    # heros = serializers.StringRelatedField(read_only=True, many=True)
    # 3.自定义
    heros = HeroRelatedSerializer(read_only=True, many=True)

    # 验证书名的自定义方法
    def validate_btitle(self, attr):
        # attr===>请求报文中书名的数据
        # 要求：书名包含django字符串
        if 'django' in attr:
            # 如果验证成功，则返回接收的值
            return attr
        else:
            # 如果验证失败，则抛异常，指定提示文本
            raise serializers.ValidationError('书名必须包含django')

    # 将多个属性进行验证
    def validate(self, attrs):
        # attrs==>字典，可以接收所有请求报文中的数据
        # 用于多属性对比

        # 验证：阅读量必须大于评论量
        bread = attrs.get('bread')
        bcomment = attrs.get('bcomment')
        if all([bread, bcomment]):
            if bread < bcomment:
                raise serializers.ValidationError('阅读量必须大于评论量')

        return attrs

    def create(self, validated_data):
        # 当调用serializer.save()时，如果是增加则调用这个方法
        # 参数validated_data表示验证后的数据
        book = BookInfo.objects.create(**validated_data)
        return book

    def update(self, instance, validated_data):
        # 当调用serializer.save()时，如果是修改则调用这个方法
        # 参数instance：需要被修改的对象
        # 参数validated_data：验证后的数据
        instance.btitle = validated_data.get('btitle')
        instance.bpub_date = validated_data.get('bpub_date')
        instance.save()
        return instance


class HeroSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    hname = serializers.CharField()
    # hbook_id = serializers.IntegerField()
    # 将关系属性相关对象的主键输出
    # hbook = serializers.PrimaryKeyRelatedField(read_only=True)
    # 将关系属性相关对象转成字符串输出，会调用str方法
    # hbook = serializers.StringRelatedField(read_only=True)
    # 调用关系属性的自定义序列化器
    # hbook = BookSerializer(read_only=True)


class BookModelSerializer(serializers.ModelSerializer):
    # 定义属性，指定类型与参数
    # 定义验证方法
    # 定义保存方法：create()，update()
    # 省略的代码：定义属性，指定类型，定义保存方法
    # 需要写的代码：定义验证方法
    heros = HeroRelatedSerializer(read_only=True, many=True)  ##!!注意加的位置,在class Meta 上面,加到里面不起作用

    class Meta:
        model = BookInfo
        # fields='__all__'
        exclude = ('is_delete',) ##一个内容时后边的, 必须有,否则报错TypeError: The `exclude` option must be a list or tuple. Got str.
        
        fields = ('id', 'btitle', 'heros')
        read_only_fields = ('id',)    ###只读的字段,修改时不会报错,只是不起作用,还会显示原来的值

    def validate_btitle(self, attr):  ##验证部分跟原来一样
        return attr

    def validate(self, attrs):
        return attrs
